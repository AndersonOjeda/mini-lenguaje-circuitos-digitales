from pathlib import Path
import sys

from antlr4 import CommonTokenStream, InputStream
from antlr4.error.ErrorListener import ErrorListener

from compiler_errors import CompilerMessage, CompilerSetupError, LexicalSyntacticError


GENERATED_DIR = Path(__file__).resolve().parent / "generated"
if str(GENERATED_DIR) not in sys.path:
    sys.path.insert(0, str(GENERATED_DIR))


def _load_generated_classes():
    try:
        from gramaticaLexer import gramaticaLexer
        from gramaticaParser import gramaticaParser
        from ast_builder import ASTBuilder
        return gramaticaLexer, gramaticaParser, ASTBuilder
    except ImportError as exc:
        raise CompilerSetupError(
            [
                "No se encontraron los archivos generados de ANTLR4 en generated/.",
                "Ejecuta: java -jar antlr-4.13.2-complete.jar -Dlanguage=Python3 -visitor -o generated gramatica.g4",
            ]
        ) from exc


class CollectingErrorListener(ErrorListener):
    def __init__(self, fase: str, errores: list[CompilerMessage]):
        super().__init__()
        self.fase = fase
        self.errores = errores

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        texto = getattr(offendingSymbol, "text", None)
        mensaje = self._mensaje_pedagogico(texto, msg)
        self.errores.append(CompilerMessage(self.fase, line, column, mensaje))

    def _mensaje_pedagogico(self, texto: str | None, msg: str) -> str:
        if self.fase == "lexico":
            return f"Caracter no reconocido. Detalle de ANTLR: {msg}"

        if "expecting GATETYPE" in msg:
            token = texto or "<desconocido>"
            return f"Tipo de compuerta invalido '{token}'. Usa AND, OR o NOT."

        if "expecting ';'" in msg or "expecting {';'}" in msg:
            return "Falta punto y coma ';' al final de la instruccion."

        if texto in {"<EOF>", "EOF"}:
            return f"Fin de archivo inesperado. Detalle de ANTLR: {msg}"

        return f"Error sintactico cerca de '{texto}'. Detalle de ANTLR: {msg}"


def parse_source(codigo_fuente: str):
    gramaticaLexer, gramaticaParser, ASTBuilder = _load_generated_classes()
    errores: list[CompilerMessage] = []

    input_stream = InputStream(codigo_fuente)
    lexer = gramaticaLexer(input_stream)
    lexer.removeErrorListeners()
    lexer.addErrorListener(CollectingErrorListener("lexico", errores))

    token_stream = CommonTokenStream(lexer)
    parser = gramaticaParser(token_stream)
    parser.removeErrorListeners()
    parser.addErrorListener(CollectingErrorListener("sintactico", errores))

    tree = parser.program()
    if errores:
        raise LexicalSyntacticError(errores)

    return ASTBuilder().visit(tree)
