# Este modulo conecta ANTLR con el resto del compilador.
from pathlib import Path
import sys

# Clases base de ANTLR para convertir texto en tokens y luego en arbol de parseo.
from antlr4 import CommonTokenStream, InputStream
from antlr4.error.ErrorListener import ErrorListener

# Errores propios del proyecto, con mensajes mas claros para el usuario.
from compiler_errors import CompilerMessage, CompilerSetupError, LexicalSyntacticError


# Carpeta donde ANTLR deja gramaticaLexer.py, gramaticaParser.py y gramaticaVisitor.py.
GENERATED_DIR = Path(__file__).resolve().parent / "generated"

# Se agrega generated/ al path para poder importar las clases producidas por ANTLR.
if str(GENERATED_DIR) not in sys.path:
    sys.path.insert(0, str(GENERATED_DIR))


def _load_generated_classes():
    """Carga las clases generadas por ANTLR y falla con una ayuda clara si no existen."""
    try:
        # Lexer: convierte caracteres del programa fuente en tokens.
        from gramaticaLexer import gramaticaLexer
        # Parser: convierte tokens en un arbol sintactico segun gramatica.g4.
        from gramaticaParser import gramaticaParser
        # ASTBuilder: visitante propio que convierte el arbol de ANTLR en nodos simples.
        from ast_builder import ASTBuilder

        return gramaticaLexer, gramaticaParser, ASTBuilder
    except ImportError as exc:
        # Este error suele pasar si no se ejecuto el comando de generacion de ANTLR.
        raise CompilerSetupError(
            [
                "No se encontraron los archivos generados de ANTLR4 en generated/.",
                "Ejecuta: java -jar antlr-4.13.2-complete.jar -Dlanguage=Python3 -visitor -o generated gramatica.g4",
            ]
        ) from exc


class CollectingErrorListener(ErrorListener):
    """Listener que acumula errores lexicos/sintacticos en vez de imprimirlos directo."""

    def __init__(self, fase: str, errores: list[CompilerMessage]):
        super().__init__()
        # fase permite distinguir si el error viene del lexer o del parser.
        self.fase = fase
        # errores es una lista compartida entre lexer y parser.
        self.errores = errores

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        """ANTLR llama este metodo cuando encuentra un error de token o de sintaxis."""
        # offendingSymbol no siempre existe en errores lexicos, por eso se usa getattr.
        texto = getattr(offendingSymbol, "text", None)

        # Se transforma el mensaje tecnico de ANTLR en un mensaje mas pedagogico.
        mensaje = self._mensaje_pedagogico(texto, msg)

        # El error se guarda para reportarlo todo junto al final del parseo.
        self.errores.append(CompilerMessage(self.fase, line, column, mensaje))

    def _mensaje_pedagogico(self, texto: str | None, msg: str) -> str:
        """Convierte mensajes genericos de ANTLR en explicaciones faciles de exponer."""
        # Si falla el lexer, el problema es un caracter que no pertenece al lenguaje.
        if self.fase == "lexico":
            return f"Caracter no reconocido. Detalle de ANTLR: {msg}"

        # Caso comun: se escribio un tipo de compuerta distinto de AND, OR o NOT.
        if "expecting GATETYPE" in msg:
            token = texto or "<desconocido>"
            return f"Tipo de compuerta invalido '{token}'. Usa AND, OR o NOT."

        # Caso comun: falto el punto y coma obligatorio al final de una instruccion.
        if "expecting ';'" in msg or "expecting {';'}" in msg:
            return "Falta punto y coma ';' al final de la instruccion."

        # Si el parser esperaba mas tokens y llego al final, se reporta como EOF inesperado.
        if texto in {"<EOF>", "EOF"}:
            return f"Fin de archivo inesperado. Detalle de ANTLR: {msg}"

        # Mensaje de respaldo para cualquier otro error sintactico.
        return f"Error sintactico cerca de '{texto}'. Detalle de ANTLR: {msg}"


def parse_source(codigo_fuente: str):
    """Recibe texto del mini lenguaje y devuelve un AST validado sintacticamente."""
    # Se importan dinamicamente las clases generadas para poder dar un error claro.
    gramaticaLexer, gramaticaParser, ASTBuilder = _load_generated_classes()

    # Lista compartida donde se acumulan errores lexicos y sintacticos.
    errores: list[CompilerMessage] = []

    # InputStream adapta el string de Python al formato que espera ANTLR.
    input_stream = InputStream(codigo_fuente)

    # El lexer separa el texto en tokens.
    lexer = gramaticaLexer(input_stream)

    # Se reemplazan los listeners por defecto para controlar el formato de errores.
    lexer.removeErrorListeners()
    lexer.addErrorListener(CollectingErrorListener("lexico", errores))

    # CommonTokenStream guarda los tokens que consume el parser.
    token_stream = CommonTokenStream(lexer)

    # El parser aplica las reglas de gramatica.g4.
    parser = gramaticaParser(token_stream)
    parser.removeErrorListeners()
    parser.addErrorListener(CollectingErrorListener("sintactico", errores))

    # program() es la regla inicial de la gramatica.
    tree = parser.program()

    # Si lexer o parser encontraron errores, se detiene antes de construir el AST.
    if errores:
        raise LexicalSyntacticError(errores)

    # Si todo esta bien, el visitor propio convierte el parse tree en AST.
    return ASTBuilder().visit(tree)
