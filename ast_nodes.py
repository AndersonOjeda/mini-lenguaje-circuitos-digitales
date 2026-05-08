from dataclasses import dataclass
from typing import Union


@dataclass(frozen=True)
class GateDecl:
    nombre: str
    tipo: str
    entradas: list[str]
    linea: int


@dataclass(frozen=True)
class Connection:
    origen: str
    destino: str
    linea: int


@dataclass(frozen=True)
class OutputDecl:
    senal: str
    linea: int


Statement = Union[GateDecl, Connection, OutputDecl]


@dataclass(frozen=True)
class Program:
    instrucciones: list[Statement]
