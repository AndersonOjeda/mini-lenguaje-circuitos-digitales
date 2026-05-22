# Este modulo traduce el arbol sintactico de ANTLR a un AST propio del proyecto.
from pathlib import Path
import sys

# Nodos simples que representan las instrucciones del lenguaje.
from ast_nodes import Connection, GateDecl, OutputDecl, Program


# Carpeta con las clases generadas desde gramatica.g4.
GENERATED_DIR = Path(__file__).resolve().parent / "generated"

# Se agrega generated/ al path para importar gramaticaVisitor.
if str(GENERATED_DIR) not in sys.path:
    sys.path.insert(0, str(GENERATED_DIR))

try:
    # gramaticaVisitor contiene los metodos base visitX que ANTLR genera.
    from gramaticaVisitor import gramaticaVisitor
except ImportError as exc:  # pragma: no cover - se reporta desde antlr_driver.
    # Si falta este archivo, el problema real es que no se genero ANTLR.
    raise ImportError("No se encontraron los archivos generados por ANTLR4.") from exc


class ASTBuilder(gramaticaVisitor):
    """Convierte el parse tree de ANTLR en un AST pequeno y facil de validar."""

    def visitProgram(self, ctx):
        """Visita el programa completo y junta todas sus instrucciones."""
        # Aqui se acumulan puertas, conexiones y salidas en el orden original.
        instrucciones = []

        # Se recorren todos los hijos del nodo program, incluyendo el EOF.
        for indice in range(ctx.getChildCount()):
            hijo = ctx.getChild(indice)

            # EOF solo marca el final del archivo, no es una instruccion del lenguaje.
            if hijo.getText() == "<EOF>":
                continue

            # self.visit llama al metodo correcto segun el tipo de hijo.
            instruccion = self.visit(hijo)

            # Si el visitor devuelve una instruccion real, se agrega al programa.
            if instruccion is not None:
                instrucciones.append(instruccion)

        # Program es el nodo raiz del AST propio.
        return Program(instrucciones)

    def visitGateDecl(self, ctx):
        """Convierte una declaracion 'puerta A = AND(x, y);' en un GateDecl."""
        # ctx.inputs().ID() devuelve todos los identificadores usados como entradas.
        entradas = [token.getText() for token in ctx.inputs().ID()]

        # Se guardan nombre, tipo, entradas y linea para errores posteriores.
        return GateDecl(
            nombre=ctx.ID().getText(),
            tipo=ctx.GATETYPE().getText(),
            entradas=entradas,
            linea=ctx.start.line,
        )

    def visitConnection(self, ctx):
        """Convierte 'conectar B a salida;' en una conexion origen-destino."""
        # ID(0) es el origen y ID(1) es el destino segun la regla de la gramatica.
        return Connection(
            origen=ctx.ID(0).getText(),
            destino=ctx.ID(1).getText(),
            linea=ctx.start.line,
        )

    def visitOutputDecl(self, ctx):
        """Convierte 'mostrar salida;' en una instruccion de salida."""
        # Solo se necesita saber que senal se quiere imprimir y en que linea aparece.
        return OutputDecl(
            senal=ctx.ID().getText(),
            linea=ctx.start.line,
        )
