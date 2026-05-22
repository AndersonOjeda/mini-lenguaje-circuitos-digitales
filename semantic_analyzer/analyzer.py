# Este modulo implementa la fase semantica: valida que el circuito tenga sentido.
from dataclasses import dataclass

# Nodos del AST que llegan desde ast_builder.py.
from ast_nodes import Connection, GateDecl, OutputDecl, Program
# Tipos de error usados para reportar problemas semanticos.
from compiler_errors import CompilerMessage, SemanticError


# Entradas externas permitidas por decision de diseno del proyecto.
DEFAULT_EXTERNAL_VALUES = {
    # x se asume verdadero cuando se genera Python.
    "x": True,
    # y se asume falso para que los ejemplos tengan resultados visibles.
    "y": False,
    # z se deja disponible para circuitos un poco mas grandes.
    "z": True,
}


@dataclass(frozen=True)
class SemanticContext:
    """Resumen de informacion valida que otras fases necesitan despues del analisis."""

    # Entradas externas admitidas por el lenguaje.
    senales_externas: set[str]
    # Entradas externas que el programa realmente uso.
    senales_externas_usadas: set[str]
    # Compuertas declaradas, indexadas por nombre.
    compuertas: dict[str, GateDecl]
    # Todas las senales que ya existen en algun punto del programa.
    senales_conocidas: set[str]
    # Grafo de dependencias usado para detectar ciclos.
    dependencias: dict[str, list[str]]


class SemanticAnalyzer:
    """Valida reglas semanticas del lenguaje de circuitos digitales."""

    def __init__(self, senales_externas: set[str] | None = None):
        # Si no se pasan entradas externas personalizadas, se usan x, y, z.
        self.senales_externas = set(senales_externas or DEFAULT_EXTERNAL_VALUES.keys())

        # Lista acumulada de errores; se reportan todos juntos al final.
        self.errores: list[CompilerMessage] = []

        # Diccionario para detectar compuertas duplicadas y consultar declaraciones.
        self.compuertas: dict[str, GateDecl] = {}

        # Al inicio solo existen las senales externas.
        self.senales_conocidas: set[str] = set(self.senales_externas)

        # Se registra que entradas externas se usaron para generar solo las necesarias.
        self.senales_externas_usadas: set[str] = set()

        # Cada senal externa empieza sin dependencias.
        self.dependencias: dict[str, list[str]] = {senal: [] for senal in self.senales_externas}

    def analyze(self, program: Program) -> SemanticContext:
        """Recorre el AST, valida cada instruccion y devuelve contexto semantico."""
        # Se procesa cada instruccion en orden para respetar declaraciones previas.
        for instruccion in program.instrucciones:
            if isinstance(instruccion, GateDecl):
                self._validar_puerta(instruccion)
            elif isinstance(instruccion, Connection):
                self._validar_conexion(instruccion)
            elif isinstance(instruccion, OutputDecl):
                self._validar_salida(instruccion)

        # Al final se revisa el grafo completo para encontrar ciclos.
        self._detectar_ciclos()

        # Si se acumulo algun error, se detiene la compilacion antes del codegen.
        if self.errores:
            raise SemanticError(self.errores)

        # Si no hubo errores, se entrega una copia segura del estado semantico.
        return SemanticContext(
            senales_externas=set(self.senales_externas),
            senales_externas_usadas=set(self.senales_externas_usadas),
            compuertas=dict(self.compuertas),
            senales_conocidas=set(self.senales_conocidas),
            dependencias={clave: list(valor) for clave, valor in self.dependencias.items()},
        )

    def _validar_puerta(self, puerta: GateDecl) -> None:
        """Valida una declaracion de compuerta y registra sus dependencias."""
        # No se permite declarar dos compuertas con el mismo nombre.
        if puerta.nombre in self.compuertas:
            self._error(puerta.linea, f"La puerta '{puerta.nombre}' ya fue declarada previamente.")

        # Tampoco se permite usar x, y o z como nombre de compuerta.
        elif puerta.nombre in self.senales_externas:
            self._error(
                puerta.linea,
                f"La puerta '{puerta.nombre}' usa el nombre de una entrada externa reservada.",
            )

        # NOT representa negacion, por eso exactamente una entrada.
        if puerta.tipo == "NOT" and len(puerta.entradas) != 1:
            self._error(
                puerta.linea,
                f"La compuerta NOT '{puerta.nombre}' debe recibir exactamente una entrada; recibio {len(puerta.entradas)}.",
            )

        # AND y OR necesitan al menos dos entradas para ser operaciones binarias o n-arias.
        if puerta.tipo in {"AND", "OR"} and len(puerta.entradas) < 2:
            self._error(
                puerta.linea,
                f"La compuerta {puerta.tipo} '{puerta.nombre}' debe recibir minimo dos entradas; recibio {len(puerta.entradas)}.",
            )

        # Cada entrada debe existir antes de usarse.
        for entrada in puerta.entradas:
            if entrada not in self.senales_conocidas:
                self._error(
                    puerta.linea,
                    f"La senal '{entrada}' se usa como entrada de '{puerta.nombre}' antes de declararse. "
                    f"Usa una puerta previa, una conexion previa o una entrada externa permitida: {self._externas_texto()}.",
                )

            # Si la entrada existe y es externa, se marca para generar su valor en Python.
            elif entrada in self.senales_externas:
                self.senales_externas_usadas.add(entrada)

        # Si el nombre es valido, la nueva compuerta pasa a ser una senal conocida.
        if puerta.nombre not in self.compuertas and puerta.nombre not in self.senales_externas:
            self.compuertas[puerta.nombre] = puerta
            self.senales_conocidas.add(puerta.nombre)

        # Se asegura que la compuerta aparezca como nodo del grafo de dependencias.
        self.dependencias.setdefault(puerta.nombre, [])

        # Cada entrada crea una arista: puerta depende de entrada.
        for entrada in puerta.entradas:
            self._agregar_dependencia(puerta.nombre, entrada)

    def _validar_conexion(self, conexion: Connection) -> None:
        """Valida una conexion y registra que destino depende de origen."""
        # El origen debe existir; no se puede conectar desde una senal desconocida.
        if conexion.origen not in self.senales_conocidas:
            self._error(
                conexion.linea,
                f"No se puede conectar desde '{conexion.origen}' porque esa senal no existe todavia.",
            )

        # Si se conecta directamente una entrada externa, tambien debe generarse en Python.
        elif conexion.origen in self.senales_externas:
            self.senales_externas_usadas.add(conexion.origen)

        # El destino se considera una nueva senal conocida despues de la conexion.
        self.senales_conocidas.add(conexion.destino)

        # El destino debe existir como nodo del grafo.
        self.dependencias.setdefault(conexion.destino, [])

        # Se registra que destino depende del origen.
        self._agregar_dependencia(conexion.destino, conexion.origen)

    def _validar_salida(self, salida: OutputDecl) -> None:
        """Valida que la senal solicitada por mostrar exista."""
        # No se puede imprimir una senal que nunca fue declarada ni conectada.
        if salida.senal not in self.senales_conocidas:
            self._error(salida.linea, f"No se puede mostrar '{salida.senal}' porque esa senal no existe.")

        # Mostrar una entrada externa obliga a declarar su valor en el Python generado.
        elif salida.senal in self.senales_externas:
            self.senales_externas_usadas.add(salida.senal)

    def _detectar_ciclos(self) -> None:
        """Detecta dependencias circulares con busqueda en profundidad."""
        # visitados contiene senales que ya terminaron su exploracion DFS.
        visitados: set[str] = set()

        # pila representa el camino actual de la busqueda.
        pila: list[str] = []

        # reportados evita mostrar el mismo ciclo varias veces.
        reportados: set[tuple[str, ...]] = set()

        def dfs(senal: str) -> None:
            """Explora dependencias de una senal y reporta si vuelve a una senal activa."""
            # Si una senal reaparece en la pila, existe un ciclo.
            if senal in pila:
                indice = pila.index(senal)
                ciclo = tuple(pila[indice:] + [senal])

                # El ciclo se reporta solo una vez.
                if ciclo not in reportados:
                    reportados.add(ciclo)
                    self._error(0, "Conexion circular detectada: " + " -> ".join(ciclo) + ".")
                return

            # Si ya se exploro completamente, no hace falta repetir trabajo.
            if senal in visitados:
                return

            # Se agrega la senal al camino actual.
            pila.append(senal)

            # Se exploran sus dependencias directas.
            for dependencia in self.dependencias.get(senal, []):
                # Solo se hace DFS sobre senales que tambien son nodos del grafo.
                if dependencia in self.dependencias:
                    dfs(dependencia)

            # Al terminar, la senal sale del camino activo.
            pila.pop()

            # La senal queda marcada como explorada.
            visitados.add(senal)

        # Se revisan todas las senales registradas en el grafo de dependencias.
        for senal in sorted(self.dependencias):
            dfs(senal)

    def _agregar_dependencia(self, destino: str, origen: str) -> None:
        """Agrega una dependencia sin duplicarla."""
        # Obtiene la lista de dependencias del destino o la crea si no existe.
        dependencias = self.dependencias.setdefault(destino, [])

        # Evita aristas repetidas, lo que simplifica el DFS y el reporte.
        if origen not in dependencias:
            dependencias.append(origen)

    def _error(self, linea: int, mensaje: str) -> None:
        """Registra un error semantico en la lista acumulada."""
        self.errores.append(CompilerMessage("semantico", linea, 0, mensaje))

    def _externas_texto(self) -> str:
        """Devuelve las entradas externas como texto para los mensajes de ayuda."""
        return ", ".join(sorted(self.senales_externas))
