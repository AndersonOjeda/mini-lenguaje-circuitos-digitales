# Este modulo genera una representacion intermedia sencilla, parecida a TAC.
from dataclasses import dataclass

# Nodos del AST que se convierten en instrucciones IR.
from ast_nodes import Connection, GateDecl, OutputDecl, Program


@dataclass(frozen=True)
class IRInstruction:
    """Instruccion intermedia generica para operaciones logicas, asignacion e impresion."""

    # Operacion: AND, OR, NOT, ASSIGN o PRINT.
    op: str
    # Variable/senal que recibe el resultado; PRINT no necesita target.
    target: str | None = None
    # Argumentos de la operacion, por ejemplo las entradas de una compuerta.
    args: tuple[str, ...] = ()

    def __str__(self) -> str:
        """Convierte la instruccion IR a texto para mostrarla en el log."""
        # AND y OR pueden tener dos o mas argumentos.
        if self.op in {"AND", "OR"}:
            return f"{self.target} = {self.op} {' '.join(self.args)}"

        # NOT siempre tiene exactamente un argumento, validado en semantica.
        if self.op == "NOT":
            return f"{self.target} = NOT {self.args[0]}"

        # ASSIGN representa conectar origen a destino.
        if self.op == "ASSIGN":
            return f"{self.target} = {self.args[0]}"

        # PRINT representa mostrar una senal.
        if self.op == "PRINT":
            return f"PRINT {self.args[0]}"

        # Respaldo para operaciones futuras no contempladas en el formato bonito.
        return f"{self.op} {self.target or ''} {' '.join(self.args)}".strip()


class IRGenerator:
    """Recorre el AST y produce una lista lineal de instrucciones IR."""

    def generate(self, program: Program) -> list[IRInstruction]:
        """Traduce cada instruccion del AST a una instruccion intermedia."""
        # Lista final de instrucciones en el mismo orden del programa fuente.
        instrucciones: list[IRInstruction] = []

        # Se procesa cada nodo del AST segun su tipo.
        for instruccion in program.instrucciones:
            if isinstance(instruccion, GateDecl):
                # Una compuerta se convierte en una operacion logica con target.
                instrucciones.append(
                    IRInstruction(
                        op=instruccion.tipo,
                        target=instruccion.nombre,
                        args=tuple(instruccion.entradas),
                    )
                )
            elif isinstance(instruccion, Connection):
                # Una conexion se representa como asignacion: destino = origen.
                instrucciones.append(
                    IRInstruction(
                        op="ASSIGN",
                        target=instruccion.destino,
                        args=(instruccion.origen,),
                    )
                )
            elif isinstance(instruccion, OutputDecl):
                # Una instruccion mostrar se representa como PRINT.
                instrucciones.append(IRInstruction(op="PRINT", args=(instruccion.senal,)))

        # Se devuelve el IR completo para que PythonGenerator lo traduzca.
        return instrucciones
