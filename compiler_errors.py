from dataclasses import dataclass


@dataclass(frozen=True)
class CompilerMessage:
    fase: str
    linea: int
    columna: int
    mensaje: str

    def format(self) -> str:
        return f"[{self.fase}] linea {self.linea}, columna {self.columna}: {self.mensaje}"


class CompilerError(Exception):
    fase = "compilador"

    def __init__(self, mensajes: list[CompilerMessage] | list[str] | str):
        if isinstance(mensajes, str):
            self.mensajes = [mensajes]
        else:
            self.mensajes = mensajes
        super().__init__(self.as_text())

    def as_text(self) -> str:
        partes: list[str] = []
        for mensaje in self.mensajes:
            if isinstance(mensaje, CompilerMessage):
                partes.append(mensaje.format())
            else:
                partes.append(f"[{self.fase}] {mensaje}")
        return "\n".join(partes)


class LexicalSyntacticError(CompilerError):
    fase = "sintaxis"


class SemanticError(CompilerError):
    fase = "semantica"


class CompilerSetupError(CompilerError):
    fase = "configuracion"
