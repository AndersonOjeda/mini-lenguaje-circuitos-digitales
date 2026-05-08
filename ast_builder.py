from pathlib import Path
import sys

from ast_nodes import Connection, GateDecl, OutputDecl, Program


GENERATED_DIR = Path(__file__).resolve().parent / "generated"
if str(GENERATED_DIR) not in sys.path:
    sys.path.insert(0, str(GENERATED_DIR))

try:
    from gramaticaVisitor import gramaticaVisitor
except ImportError as exc:  # pragma: no cover - se reporta desde antlr_driver.
    raise ImportError("No se encontraron los archivos generados por ANTLR4.") from exc


class ASTBuilder(gramaticaVisitor):
    """Convierte el parse tree de ANTLR en un AST pequeno y facil de validar."""

    def visitProgram(self, ctx):
        instrucciones = []
        for indice in range(ctx.getChildCount()):
            hijo = ctx.getChild(indice)
            if hijo.getText() == "<EOF>":
                continue
            instruccion = self.visit(hijo)
            if instruccion is not None:
                instrucciones.append(instruccion)
        return Program(instrucciones)

    def visitGateDecl(self, ctx):
        entradas = [token.getText() for token in ctx.inputs().ID()]
        return GateDecl(
            nombre=ctx.ID().getText(),
            tipo=ctx.GATETYPE().getText(),
            entradas=entradas,
            linea=ctx.start.line,
        )

    def visitConnection(self, ctx):
        return Connection(
            origen=ctx.ID(0).getText(),
            destino=ctx.ID(1).getText(),
            linea=ctx.start.line,
        )

    def visitOutputDecl(self, ctx):
        return OutputDecl(
            senal=ctx.ID().getText(),
            linea=ctx.start.line,
        )
