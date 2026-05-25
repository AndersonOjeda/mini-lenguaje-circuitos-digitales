# Este modulo implementa la fase semantica: valida que el circuito tenga sentido.
from dataclasses import dataclass

# Nodos del AST que llegan desde ast_builder.py.
from ast_nodes import Connection, GateDecl, OutputDecl, Program
# Tipos de error usados para reportar problemas semanticos.
from compiler_errors import CompilerMessage, SemanticError
from semantic_analyzer.symbol_table import Symbol, SymbolTable


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

    # Snapshot de la tabla de simbolos despues del analisis.
    simbolos: dict[str, Symbol]
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
        # Lista acumulada de errores; se reportan todos juntos al final.
        self.errores: list[CompilerMessage] = []

        # La tabla de simbolos concentra nombres, externas usadas y dependencias.
        externas = senales_externas or set(DEFAULT_EXTERNAL_VALUES)
        self.tabla_simbolos = SymbolTable(externas)

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
        return self._crear_contexto()

    def _validar_puerta(self, puerta: GateDecl) -> None:
        """Valida una declaracion de compuerta y registra sus dependencias."""
        # No se permite declarar dos compuertas con el mismo nombre.
        nombre_valido = True
        if self.tabla_simbolos.has_gate(puerta.nombre):
            self._error(puerta.linea, f"La puerta '{puerta.nombre}' ya fue declarada previamente.")
            nombre_valido = False

        # Tampoco se permite usar x, y o z como nombre de compuerta.
        elif self.tabla_simbolos.is_external(puerta.nombre):
            self._error(
                puerta.linea,
                f"La puerta '{puerta.nombre}' usa el nombre de una entrada externa reservada.",
            )
            nombre_valido = False

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
            if not self.tabla_simbolos.contains(entrada):
                self._error(
                    puerta.linea,
                    f"La senal '{entrada}' se usa como entrada de '{puerta.nombre}' antes de declararse. "
                    f"Usa una puerta previa, una conexion previa o una entrada externa permitida: {self._externas_texto()}.",
                )

            # Si la entrada existe y es externa, se marca para generar su valor en Python.
            else:
                self.tabla_simbolos.mark_external_used(entrada)

        # Si el nombre es valido, la nueva compuerta pasa a ser una senal conocida.
        if nombre_valido:
            self.tabla_simbolos.define_gate(puerta)
        else:
            self.tabla_simbolos.ensure_dependency_node(puerta.nombre)

        # Cada entrada crea una arista: puerta depende de entrada.
        for entrada in puerta.entradas:
            self.tabla_simbolos.add_dependency(puerta.nombre, entrada)

    def _validar_conexion(self, conexion: Connection) -> None:
        """Valida una conexion y registra que destino depende de origen."""
        # El origen debe existir; no se puede conectar desde una senal desconocida.
        if not self.tabla_simbolos.contains(conexion.origen):
            self._error(
                conexion.linea,
                f"No se puede conectar desde '{conexion.origen}' porque esa senal no existe todavia.",
            )

        # Si se conecta directamente una entrada externa, tambien debe generarse en Python.
        else:
            self.tabla_simbolos.mark_external_used(conexion.origen)

        # El destino se considera una nueva senal conocida despues de la conexion.
        self.tabla_simbolos.define_connection_target(conexion)

        # Se registra que destino depende del origen.
        self.tabla_simbolos.add_dependency(conexion.destino, conexion.origen)

    def _validar_salida(self, salida: OutputDecl) -> None:
        """Valida que la senal solicitada por mostrar exista."""
        # No se puede imprimir una senal que nunca fue declarada ni conectada.
        if not self.tabla_simbolos.contains(salida.senal):
            self._error(salida.linea, f"No se puede mostrar '{salida.senal}' porque esa senal no existe.")

        # Mostrar una entrada externa obliga a declarar su valor en el Python generado.
        else:
            self.tabla_simbolos.mark_external_used(salida.senal)

    def _detectar_ciclos(self) -> None:
        """Detecta dependencias circulares con busqueda en profundidad."""
        # visitados contiene senales que ya terminaron su exploracion DFS.
        visitados: set[str] = set()

        # pila representa el camino actual de la busqueda.
        pila: list[str] = []

        # reportados evita mostrar el mismo ciclo varias veces.
        reportados: set[tuple[str, ...]] = set()

        # Se trabaja con un snapshot para que el DFS no dependa de mutaciones externas.
        dependencias = self.tabla_simbolos.dependencies

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
            for dependencia in dependencias.get(senal, []):
                # Solo se hace DFS sobre senales que tambien son nodos del grafo.
                if dependencia in dependencias:
                    dfs(dependencia)

            # Al terminar, la senal sale del camino activo.
            pila.pop()

            # La senal queda marcada como explorada.
            visitados.add(senal)

        # Se revisan todas las senales registradas en el grafo de dependencias.
        for senal in sorted(dependencias):
            dfs(senal)

    def _crear_contexto(self) -> SemanticContext:
        """Construye un snapshot inmutable del resultado semantico."""
        return SemanticContext(
            simbolos=self.tabla_simbolos.symbols,
            senales_externas=self.tabla_simbolos.external_signals,
            senales_externas_usadas=self.tabla_simbolos.used_external_signals,
            compuertas=self.tabla_simbolos.gates,
            senales_conocidas=self.tabla_simbolos.known_signals,
            dependencias=self.tabla_simbolos.dependencies,
        )

    def _error(self, linea: int, mensaje: str) -> None:
        """Registra un error semantico en la lista acumulada."""
        self.errores.append(CompilerMessage("semantico", linea, 0, mensaje))

    def _externas_texto(self) -> str:
        """Devuelve las entradas externas como texto para los mensajes de ayuda."""
        return ", ".join(sorted(self.tabla_simbolos.external_signals))
