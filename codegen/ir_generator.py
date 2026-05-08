from dataclasses import dataclass

from ast_nodes import Connection, GateDecl, OutputDecl, Program


@dataclass(frozen=True)
class IRInstruction:
    op: str
    target: str | None = None
    args: tuple[str, ...] = ()

    def __str__(self) -> str:
        if self.op in {"AND", "OR"}:
            return f"{self.target} = {self.op} {' '.join(self.args)}"
        if self.op == "NOT":
            return f"{self.target} = NOT {self.args[0]}"
        if self.op == "ASSIGN":
            return f"{self.target} = {self.args[0]}"
        if self.op == "PRINT":
            return f"PRINT {self.args[0]}"
        return f"{self.op} {self.target or ''} {' '.join(self.args)}".strip()


class IRGenerator:
    def generate(self, program: Program) -> list[IRInstruction]:
        instrucciones: list[IRInstruction] = []

        for instruccion in program.instrucciones:
            if isinstance(instruccion, GateDecl):
                instrucciones.append(
                    IRInstruction(
                        op=instruccion.tipo,
                        target=instruccion.nombre,
                        args=tuple(instruccion.entradas),
                    )
                )
            elif isinstance(instruccion, Connection):
                instrucciones.append(
                    IRInstruction(
                        op="ASSIGN",
                        target=instruccion.destino,
                        args=(instruccion.origen,),
                    )
                )
            elif isinstance(instruccion, OutputDecl):
                instrucciones.append(IRInstruction(op="PRINT", args=(instruccion.senal,)))

        return instrucciones
