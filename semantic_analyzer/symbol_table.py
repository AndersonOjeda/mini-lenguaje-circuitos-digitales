# Este modulo centraliza la tabla de simbolos usada por el analisis semantico.
from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from enum import Enum

from ast_nodes import Connection, GateDecl


class SymbolKind(str, Enum):
    """Clasifica el origen de cada simbolo del programa."""

    EXTERNAL = "entrada_externa"
    GATE = "compuerta"
    CONNECTION = "conexion"


@dataclass(frozen=True)
class Symbol:
    """Entrada individual de la tabla de simbolos."""

    name: str
    kind: SymbolKind
    line: int
    declaration: GateDecl | Connection | None = None


class SymbolTable:
    """Guarda simbolos, entradas externas usadas y dependencias entre senales."""

    def __init__(self, external_signals: Iterable[str]):
        self._external_signals = set(external_signals)
        self._symbols: dict[str, Symbol] = {}
        self._gates: dict[str, GateDecl] = {}
        self._used_external_signals: set[str] = set()
        self._dependencies: dict[str, list[str]] = {}

        for signal in sorted(self._external_signals):
            self._symbols[signal] = Symbol(signal, SymbolKind.EXTERNAL, 0)
            self._dependencies[signal] = []

    def contains(self, name: str) -> bool:
        """Indica si una senal ya existe en la tabla."""
        return name in self._symbols

    def is_external(self, name: str) -> bool:
        """Indica si el nombre pertenece a una entrada externa reservada."""
        return name in self._external_signals

    def has_gate(self, name: str) -> bool:
        """Indica si ya existe una compuerta declarada con ese nombre."""
        return name in self._gates

    def define_gate(self, gate: GateDecl) -> None:
        """Registra una compuerta valida como simbolo y como nodo de dependencias."""
        self._symbols[gate.nombre] = Symbol(gate.nombre, SymbolKind.GATE, gate.linea, gate)
        self._gates[gate.nombre] = gate
        self.ensure_dependency_node(gate.nombre)

    def define_connection_target(self, connection: Connection) -> None:
        """Registra el destino de una conexion si aun no existe como senal."""
        if not self.contains(connection.destino):
            self._symbols[connection.destino] = Symbol(
                connection.destino,
                SymbolKind.CONNECTION,
                connection.linea,
                connection,
            )

        self.ensure_dependency_node(connection.destino)

    def mark_external_used(self, name: str) -> None:
        """Marca una entrada externa como usada por el programa."""
        if self.is_external(name):
            self._used_external_signals.add(name)

    def ensure_dependency_node(self, name: str) -> None:
        """Asegura que una senal aparezca como nodo en el grafo de dependencias."""
        self._dependencies.setdefault(name, [])

    def add_dependency(self, target: str, source: str) -> None:
        """Registra que target depende de source sin duplicar aristas."""
        dependencies = self._dependencies.setdefault(target, [])
        if source not in dependencies:
            dependencies.append(source)

    @property
    def symbols(self) -> dict[str, Symbol]:
        """Entrega una copia de los simbolos registrados."""
        return dict(self._symbols)

    @property
    def external_signals(self) -> set[str]:
        """Entrega una copia de las entradas externas permitidas."""
        return set(self._external_signals)

    @property
    def used_external_signals(self) -> set[str]:
        """Entrega una copia de las entradas externas usadas."""
        return set(self._used_external_signals)

    @property
    def gates(self) -> dict[str, GateDecl]:
        """Entrega una copia de las compuertas declaradas."""
        return dict(self._gates)

    @property
    def known_signals(self) -> set[str]:
        """Entrega una copia de todas las senales conocidas."""
        return set(self._symbols)

    @property
    def dependencies(self) -> dict[str, list[str]]:
        """Entrega una copia del grafo de dependencias."""
        return {name: list(dependencies) for name, dependencies in self._dependencies.items()}
