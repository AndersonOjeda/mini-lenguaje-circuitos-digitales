from __future__ import annotations

import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from compiler_errors import CompilerError
from compiler_pipeline import BANNER, compilar_codigo


COLOR_RESET = "\033[0m"
COLOR_VERDE = "\033[92m"
COLOR_ROJO = "\033[91m"
COLOR_CYAN = "\033[96m"


def soporta_color() -> bool:
    return sys.stdout.isatty() and os.environ.get("NO_COLOR") is None


def color(texto: str, codigo: str, activo: bool) -> str:
    if not activo:
        return texto
    return f"{codigo}{texto}{COLOR_RESET}"


def run_tests(output_log_path: Path | None = None, usar_color: bool | None = None) -> bool:
    output_log_path = output_log_path or ROOT / "output.txt"
    usar_color = soporta_color() if usar_color is None else usar_color
    validos = sorted((ROOT / "tests" / "valid").glob("*.txt"))
    invalidos = sorted((ROOT / "tests" / "invalid").glob("*.txt"))

    lineas = [
        BANNER,
        "",
        "MiniCompilador - ejecucion automatica de pruebas",
        f"Casos validos encontrados: {len(validos)}",
        f"Casos con errores encontrados: {len(invalidos)}",
        "",
    ]

    fallos: list[str] = []

    for path in validos:
        try:
            compilar_codigo(path.read_text(encoding="utf-8"), ejecutar=True)
            lineas.append(f"[OK] valido   {path.name}")
        except CompilerError as exc:
            fallos.append(path.name)
            lineas.append(f"[FAIL] valido {path.name}: no debia fallar")
            lineas.append(exc.as_text())

    for path in invalidos:
        try:
            compilar_codigo(path.read_text(encoding="utf-8"), ejecutar=False)
            fallos.append(path.name)
            lineas.append(f"[FAIL] error  {path.name}: debia reportar error")
        except CompilerError as exc:
            primera_linea = exc.as_text().splitlines()[0]
            lineas.append(f"[OK] error    {path.name}: {primera_linea}")

    total = len(validos) + len(invalidos)
    correctos = total - len(fallos)
    lineas.extend(["", f"Resumen: {correctos}/{total} casos correctos."])

    if fallos:
        lineas.append("Casos fallidos: " + ", ".join(fallos))

    log = "\n".join(lineas) + "\n"
    output_log_path.write_text(log, encoding="utf-8")
    imprimir_resultado(log, usar_color)
    return not fallos


def imprimir_resultado(log: str, usar_color: bool) -> None:
    for linea in log.rstrip().splitlines():
        if linea.startswith("[OK]"):
            print(color(linea, COLOR_VERDE, usar_color))
        elif linea.startswith("[FAIL]") or linea.startswith("[semantico]") or linea.startswith("[sintactico]"):
            print(color(linea, COLOR_ROJO, usar_color))
        elif linea.startswith("=") or linea.startswith(" MiniCompilador"):
            print(color(linea, COLOR_CYAN, usar_color))
        else:
            print(linea)
    print()


if __name__ == "__main__":
    raise SystemExit(0 if run_tests() else 1)
