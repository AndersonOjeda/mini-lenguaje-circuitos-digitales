# Este modulo centraliza los errores del compilador para reportarlos con formato uniforme.
from dataclasses import dataclass


@dataclass(frozen=True)
class CompilerMessage:
    """Mensaje individual con fase, ubicacion y descripcion del problema."""

    # Fase donde ocurrio el problema: lexico, sintactico, semantico, etc.
    fase: str
    # Linea del archivo fuente donde se detecto el error.
    linea: int
    # Columna del archivo fuente donde se detecto el error.
    columna: int
    # Explicacion entendible para el usuario.
    mensaje: str

    def format(self) -> str:
        """Devuelve el mensaje con el formato que aparece en consola."""
        return f"[{self.fase}] linea {self.linea}, columna {self.columna}: {self.mensaje}"


class CompilerError(Exception):
    """Error base del compilador; puede contener uno o varios mensajes."""

    # Fase generica usada cuando una subclase no define una fase especifica.
    fase = "compilador"

    def __init__(self, mensajes: list[CompilerMessage] | list[str] | str):
        # Si llega un solo string, se normaliza a lista para tratar todos los casos igual.
        if isinstance(mensajes, str):
            self.mensajes = [mensajes]
        else:
            self.mensajes = mensajes

        # Exception recibe el texto final para que str(error) tambien sea legible.
        super().__init__(self.as_text())

    def as_text(self) -> str:
        """Convierte todos los mensajes internos en un bloque de texto."""
        # partes acumula cada linea del reporte de error.
        partes: list[str] = []

        # Cada mensaje puede ser estructurado o un string simple.
        for mensaje in self.mensajes:
            if isinstance(mensaje, CompilerMessage):
                partes.append(mensaje.format())
            else:
                partes.append(f"[{self.fase}] {mensaje}")

        # El log final separa los errores por saltos de linea.
        return "\n".join(partes)


class LexicalSyntacticError(CompilerError):
    """Error usado cuando falla el lexer o el parser."""

    fase = "sintaxis"


class SemanticError(CompilerError):
    """Error usado cuando el programa esta bien escrito pero no tiene sentido semantico."""

    fase = "semantica"


class CompilerSetupError(CompilerError):
    """Error usado cuando faltan archivos generados o configuracion del entorno."""

    fase = "configuracion"
