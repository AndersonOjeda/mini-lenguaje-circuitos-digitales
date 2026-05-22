from __future__ import annotations

# Este archivo ejecuta automaticamente casos validos e invalidos para demostrar el compilador.
import os
from pathlib import Path
import sys

# ROOT apunta a la carpeta principal del proyecto desde tests/.
ROOT = Path(__file__).resolve().parents[1]

# Permite importar modulos del proyecto aunque este archivo se ejecute directamente.
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Se captura el error base para saber si una prueba fallo como se esperaba.
from compiler_errors import CompilerError
# Se reutiliza el mismo pipeline real que usa main.py.
from compiler_pipeline import BANNER, compilar_codigo


# Codigos ANSI para colorear el resumen de pruebas.
COLOR_RESET = "\033[0m"
COLOR_VERDE = "\033[92m"
COLOR_ROJO = "\033[91m"
COLOR_CYAN = "\033[96m"


def soporta_color() -> bool:
    """Indica si la terminal permite imprimir colores."""
    return sys.stdout.isatty() and os.environ.get("NO_COLOR") is None


def color(texto: str, codigo: str, activo: bool) -> str:
    """Envuelve un texto con codigo ANSI si los colores estan activos."""
    if not activo:
        return texto
    return f"{codigo}{texto}{COLOR_RESET}"


def run_tests(output_log_path: Path | None = None, usar_color: bool | None = None) -> bool:
    """Ejecuta todos los casos de tests/valid y tests/invalid."""
    # Si no se pasa ruta, el resultado se escribe en output.txt.
    output_log_path = output_log_path or ROOT / "output.txt"

    # usar_color puede llegar desde main.py o calcularse aqui.
    usar_color = soporta_color() if usar_color is None else usar_color

    # Casos que deben compilar sin errores.
    validos = sorted((ROOT / "tests" / "valid").glob("*.txt"))

    # Casos que deben producir errores lexicos, sintacticos o semanticos.
    invalidos = sorted((ROOT / "tests" / "invalid").glob("*.txt"))

    # Encabezado del reporte de pruebas.
    lineas = [
        BANNER,
        "",
        "MiniCompilador - ejecucion automatica de pruebas",
        f"Casos validos encontrados: {len(validos)}",
        f"Casos con errores encontrados: {len(invalidos)}",
        "",
    ]

    # Aqui se guardan los nombres de casos que no se comporten como se esperaba.
    fallos: list[str] = []

    # Primero se prueban programas validos: todos deben compilar y ejecutar.
    for path in validos:
        try:
            compilar_codigo(path.read_text(encoding="utf-8"), ejecutar=True)
            lineas.append(f"[OK] valido   {path.name}")
        except CompilerError as exc:
            # Si un valido lanza error, el compilador fallo esa prueba.
            fallos.append(path.name)
            lineas.append(f"[FAIL] valido {path.name}: no debia fallar")
            lineas.append(exc.as_text())

    # Luego se prueban programas invalidos: todos deben reportar error.
    for path in invalidos:
        try:
            compilar_codigo(path.read_text(encoding="utf-8"), ejecutar=False)
            # Si un invalido compila, falta alguna validacion.
            fallos.append(path.name)
            lineas.append(f"[FAIL] error  {path.name}: debia reportar error")
        except CompilerError as exc:
            # Para invalidos, capturar un CompilerError significa que la prueba paso.
            primera_linea = exc.as_text().splitlines()[0]
            lineas.append(f"[OK] error    {path.name}: {primera_linea}")

    # Se calcula el resumen total.
    total = len(validos) + len(invalidos)
    correctos = total - len(fallos)
    lineas.extend(["", f"Resumen: {correctos}/{total} casos correctos."])

    # Si hubo fallos, se listan para encontrarlos rapido.
    if fallos:
        lineas.append("Casos fallidos: " + ", ".join(fallos))

    # El log completo se escribe en archivo y en consola.
    log = "\n".join(lineas) + "\n"
    output_log_path.write_text(log, encoding="utf-8")
    imprimir_resultado(log, usar_color)

    # True significa que todos los casos pasaron.
    return not fallos


def imprimir_resultado(log: str, usar_color: bool) -> None:
    """Imprime el reporte de pruebas con colores segun el tipo de linea."""
    # Se procesa linea por linea para colorear OK, FAIL y encabezados.
    for linea in log.rstrip().splitlines():
        if linea.startswith("[OK]"):
            print(color(linea, COLOR_VERDE, usar_color))
        elif linea.startswith("[FAIL]") or linea.startswith("[semantico]") or linea.startswith("[sintactico]"):
            print(color(linea, COLOR_ROJO, usar_color))
        elif linea.startswith("=") or linea.startswith(" MiniCompilador"):
            print(color(linea, COLOR_CYAN, usar_color))
        else:
            print(linea)

    # Linea en blanco final para separar la salida de otros comandos.
    print()


# Permite ejecutar este archivo directamente con python tests/run_tests.py.
if __name__ == "__main__":
    raise SystemExit(0 if run_tests() else 1)
