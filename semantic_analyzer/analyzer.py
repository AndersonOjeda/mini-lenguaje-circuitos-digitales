from dataclasses import dataclass

from ast_nodes import Connection, GateDecl, OutputDecl, Program
from compiler_errors import CompilerMessage, SemanticError


DEFAULT_EXTERNAL_VALUES = {
    "x": True,
    "y": False,
    "z": True,
}


@dataclass(frozen=True)
class SemanticContext:
    senales_externas: set[str]
    senales_externas_usadas: set[str]
    compuertas: dict[str, GateDecl]
    senales_conocidas: set[str]
    dependencias: dict[str, list[str]]


class SemanticAnalyzer:
    """Valida reglas semanticas del lenguaje de circuitos digitales."""

    def __init__(self, senales_externas: set[str] | None = None):
        self.senales_externas = set(senales_externas or DEFAULT_EXTERNAL_VALUES.keys())
        self.errores: list[CompilerMessage] = []
        self.compuertas: dict[str, GateDecl] = {}
        self.senales_conocidas: set[str] = set(self.senales_externas)
        self.senales_externas_usadas: set[str] = set()
        self.dependencias: dict[str, list[str]] = {senal: [] for senal in self.senales_externas}

    def analyze(self, program: Program) -> SemanticContext:
        for instruccion in program.instrucciones:
            if isinstance(instruccion, GateDecl):
                self._validar_puerta(instruccion)
            elif isinstance(instruccion, Connection):
                self._validar_conexion(instruccion)
            elif isinstance(instruccion, OutputDecl):
                self._validar_salida(instruccion)

        self._detectar_ciclos()

        if self.errores:
            raise SemanticError(self.errores)

        return SemanticContext(
            senales_externas=set(self.senales_externas),
            senales_externas_usadas=set(self.senales_externas_usadas),
            compuertas=dict(self.compuertas),
            senales_conocidas=set(self.senales_conocidas),
            dependencias={clave: list(valor) for clave, valor in self.dependencias.items()},
        )

    def _validar_puerta(self, puerta: GateDecl) -> None:
        if puerta.nombre in self.compuertas:
            self._error(puerta.linea, f"La puerta '{puerta.nombre}' ya fue declarada previamente.")
        elif puerta.nombre in self.senales_externas:
            self._error(
                puerta.linea,
                f"La puerta '{puerta.nombre}' usa el nombre de una entrada externa reservada.",
            )

        if puerta.tipo == "NOT" and len(puerta.entradas) != 1:
            self._error(
                puerta.linea,
                f"La compuerta NOT '{puerta.nombre}' debe recibir exactamente una entrada; recibio {len(puerta.entradas)}.",
            )

        if puerta.tipo in {"AND", "OR"} and len(puerta.entradas) < 2:
            self._error(
                puerta.linea,
                f"La compuerta {puerta.tipo} '{puerta.nombre}' debe recibir minimo dos entradas; recibio {len(puerta.entradas)}.",
            )

        for entrada in puerta.entradas:
            if entrada not in self.senales_conocidas:
                self._error(
                    puerta.linea,
                    f"La senal '{entrada}' se usa como entrada de '{puerta.nombre}' antes de declararse. "
                    f"Usa una puerta previa, una conexion previa o una entrada externa permitida: {self._externas_texto()}.",
                )
            elif entrada in self.senales_externas:
                self.senales_externas_usadas.add(entrada)

        if puerta.nombre not in self.compuertas and puerta.nombre not in self.senales_externas:
            self.compuertas[puerta.nombre] = puerta
            self.senales_conocidas.add(puerta.nombre)

        self.dependencias.setdefault(puerta.nombre, [])
        for entrada in puerta.entradas:
            self._agregar_dependencia(puerta.nombre, entrada)

    def _validar_conexion(self, conexion: Connection) -> None:
        if conexion.origen not in self.senales_conocidas:
            self._error(
                conexion.linea,
                f"No se puede conectar desde '{conexion.origen}' porque esa senal no existe todavia.",
            )
        elif conexion.origen in self.senales_externas:
            self.senales_externas_usadas.add(conexion.origen)

        self.senales_conocidas.add(conexion.destino)
        self.dependencias.setdefault(conexion.destino, [])
        self._agregar_dependencia(conexion.destino, conexion.origen)

    def _validar_salida(self, salida: OutputDecl) -> None:
        if salida.senal not in self.senales_conocidas:
            self._error(salida.linea, f"No se puede mostrar '{salida.senal}' porque esa senal no existe.")
        elif salida.senal in self.senales_externas:
            self.senales_externas_usadas.add(salida.senal)

    def _detectar_ciclos(self) -> None:
        visitados: set[str] = set()
        pila: list[str] = []
        reportados: set[tuple[str, ...]] = set()

        def dfs(senal: str) -> None:
            if senal in pila:
                indice = pila.index(senal)
                ciclo = tuple(pila[indice:] + [senal])
                if ciclo not in reportados:
                    reportados.add(ciclo)
                    self._error(0, "Conexion circular detectada: " + " -> ".join(ciclo) + ".")
                return

            if senal in visitados:
                return

            pila.append(senal)
            for dependencia in self.dependencias.get(senal, []):
                if dependencia in self.dependencias:
                    dfs(dependencia)
            pila.pop()
            visitados.add(senal)

        for senal in sorted(self.dependencias):
            dfs(senal)

    def _agregar_dependencia(self, destino: str, origen: str) -> None:
        dependencias = self.dependencias.setdefault(destino, [])
        if origen not in dependencias:
            dependencias.append(origen)

    def _error(self, linea: int, mensaje: str) -> None:
        self.errores.append(CompilerMessage("semantico", linea, 0, mensaje))

    def _externas_texto(self) -> str:
        return ", ".join(sorted(self.senales_externas))
