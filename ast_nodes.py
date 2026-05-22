# Este archivo define las estructuras del AST: son los datos que viajan entre fases.
from dataclasses import dataclass
from typing import Union


@dataclass(frozen=True)
class GateDecl:
    """Representa una declaracion de compuerta, por ejemplo: puerta A = AND(x, y);"""

    # Nombre de la compuerta o senal calculada.
    nombre: str
    # Tipo logico de la compuerta: AND, OR o NOT.
    tipo: str
    # Lista de senales que entran a la compuerta.
    entradas: list[str]
    # Linea del archivo fuente donde aparece, util para reportar errores.
    linea: int


@dataclass(frozen=True)
class Connection:
    """Representa una conexion, por ejemplo: conectar B a salida;"""

    # Senal que se copia o conecta.
    origen: str
    # Nueva senal o salida que recibe el valor del origen.
    destino: str
    # Linea de la conexion en el archivo fuente.
    linea: int


@dataclass(frozen=True)
class OutputDecl:
    """Representa una instruccion mostrar, por ejemplo: mostrar salida;"""

    # Senal que se va a imprimir al ejecutar el programa generado.
    senal: str
    # Linea de la instruccion mostrar en el archivo fuente.
    linea: int


# Una instruccion del programa puede ser cualquiera de los tres nodos anteriores.
Statement = Union[GateDecl, Connection, OutputDecl]


@dataclass(frozen=True)
class Program:
    """Nodo raiz del AST: contiene todas las instrucciones del programa."""

    # Lista ordenada de instrucciones tal como aparecieron en el codigo fuente.
    instrucciones: list[Statement]
