from codegen.ir_generator import IRInstruction
from semantic_analyzer import DEFAULT_EXTERNAL_VALUES, SemanticContext


class PythonGenerator:
    def __init__(self, valores_externos: dict[str, bool] | None = None):
        self.valores_externos = valores_externos or DEFAULT_EXTERNAL_VALUES

    def generate(self, ir: list[IRInstruction], contexto: SemanticContext) -> str:
        lineas = ["# Codigo Python generado por MiniCompilador"]
        lineas.extend(self._generar_entradas(contexto.senales_externas_usadas))

        for instruccion in ir:
            if instruccion.op == "AND":
                lineas.append(f"{instruccion.target} = {' and '.join(instruccion.args)}")
            elif instruccion.op == "OR":
                lineas.append(f"{instruccion.target} = {' or '.join(instruccion.args)}")
            elif instruccion.op == "NOT":
                lineas.append(f"{instruccion.target} = not {instruccion.args[0]}")
            elif instruccion.op == "ASSIGN":
                lineas.append(f"{instruccion.target} = {instruccion.args[0]}")
            elif instruccion.op == "PRINT":
                lineas.append(f"print({instruccion.args[0]})")
            else:
                raise ValueError(f"Operacion IR no soportada: {instruccion.op}")

        return "\n".join(lineas) + "\n"

    def _generar_entradas(self, usadas: set[str]) -> list[str]:
        ordenadas = [senal for senal in self.valores_externos if senal in usadas]
        ordenadas.extend(sorted(usadas - set(self.valores_externos)))
        if not ordenadas:
            return []

        nombres = ", ".join(ordenadas)
        valores = ", ".join("True" if self.valores_externos.get(senal, False) else "False" for senal in ordenadas)
        return [f"{nombres} = {valores}"]
