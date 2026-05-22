# Este modulo traduce el IR/TAC a codigo Python ejecutable.
from codegen.ir_generator import IRInstruction
from semantic_analyzer import DEFAULT_EXTERNAL_VALUES, SemanticContext


class PythonGenerator:
    """Genera Python equivalente al circuito digital validado."""

    def __init__(self, valores_externos: dict[str, bool] | None = None):
        # valores_externos define con que valores se ejecutan x, y, z en la demo.
        self.valores_externos = valores_externos or DEFAULT_EXTERNAL_VALUES

    def generate(self, ir: list[IRInstruction], contexto: SemanticContext) -> str:
        """Convierte instrucciones IR en lineas de Python."""
        # Encabezado del archivo generado para identificar su origen.
        lineas = ["# Codigo Python generado por MiniCompilador"]

        # Se declaran solo las entradas externas realmente usadas por el circuito.
        lineas.extend(self._generar_entradas(contexto.senales_externas_usadas))

        # Cada instruccion IR se transforma en una instruccion Python.
        for instruccion in ir:
            if instruccion.op == "AND":
                lineas.append(f"# Compuerta AND: {instruccion.target} es verdadera si todas sus entradas son verdaderas.")
                lineas.append(f"{instruccion.target} = {' and '.join(instruccion.args)}")
            elif instruccion.op == "OR":
                lineas.append(f"# Compuerta OR: {instruccion.target} es verdadera si alguna entrada es verdadera.")
                lineas.append(f"{instruccion.target} = {' or '.join(instruccion.args)}")
            elif instruccion.op == "NOT":
                lineas.append(f"# Compuerta NOT: {instruccion.target} invierte el valor de {instruccion.args[0]}.")
                lineas.append(f"{instruccion.target} = not {instruccion.args[0]}")
            elif instruccion.op == "ASSIGN":
                lineas.append(f"# Conexion: {instruccion.target} recibe el valor de {instruccion.args[0]}.")
                lineas.append(f"{instruccion.target} = {instruccion.args[0]}")
            elif instruccion.op == "PRINT":
                lineas.append(f"# Salida: se muestra el valor final de {instruccion.args[0]}.")
                lineas.append(f"print({instruccion.args[0]})")
            else:
                # Si aparece una operacion no soportada, es un error de implementacion.
                raise ValueError(f"Operacion IR no soportada: {instruccion.op}")

        # El salto final deja el archivo generado con formato estandar.
        return "\n".join(lineas) + "\n"

    def _generar_entradas(self, usadas: set[str]) -> list[str]:
        """Genera la linea Python que inicializa las entradas externas usadas."""
        # Se respeta el orden x, y, z definido en DEFAULT_EXTERNAL_VALUES.
        ordenadas = [senal for senal in self.valores_externos if senal in usadas]

        # Si aparecieran externas personalizadas, se agregan ordenadas alfabeticamente.
        ordenadas.extend(sorted(usadas - set(self.valores_externos)))

        # Si el circuito no usa entradas externas, no hay nada que inicializar.
        if not ordenadas:
            return []

        # nombres arma el lado izquierdo: x, y, z.
        nombres = ", ".join(ordenadas)

        # valores arma el lado derecho: True, False, True.
        valores = ", ".join("True" if self.valores_externos.get(senal, False) else "False" for senal in ordenadas)

        # Se devuelve comentario y asignacion para que output_program.py tambien sea explicativo.
        return [
            "# Entradas externas usadas por el circuito.",
            f"{nombres} = {valores}",
        ]
