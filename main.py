from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys
import traceback

from compiler_pipeline import BANNER, compilar_codigo
from compiler_errors import CompilerError
from tests.run_tests import run_tests


ROOT = Path(__file__).resolve().parent


COLOR_RESET = "\033[0m"
COLOR_VERDE = "\033[92m"
COLOR_ROJO = "\033[91m"
COLOR_AMARILLO = "\033[93m"
COLOR_CYAN = "\033[96m"


def soporta_color(stream) -> bool:
    return stream.isatty() and os.environ.get("NO_COLOR") is None


def colorear_linea(linea: str, usar_color: bool) -> str:
    if not usar_color:
        return linea
    if linea.startswith("MiniCompilador - compilacion exitosa") or ": OK" in linea:
        return f"{COLOR_VERDE}{linea}{COLOR_RESET}"
    if linea.startswith("MiniCompilador - errores") or linea.startswith("MiniCompilador - error"):
        return f"{COLOR_ROJO}{linea}{COLOR_RESET}"
    if linea.startswith("[semantico]"):
        return f"{COLOR_ROJO}{linea}{COLOR_RESET}"
    if linea.startswith("[lexico]") or linea.startswith("[sintactico]"):
        return f"{COLOR_ROJO}{linea}{COLOR_RESET}"
    if linea.startswith("[WARN]") or "advertencia" in linea.lower():
        return f"{COLOR_AMARILLO}{linea}{COLOR_RESET}"
    if linea.startswith("=") or linea.startswith(" MiniCompilador") or linea.startswith("==="):
        return f"{COLOR_CYAN}{linea}{COLOR_RESET}"
    return linea


def imprimir_log(log: str, es_error: bool = False) -> None:
    stream = sys.stderr if es_error else sys.stdout
    usar_color = soporta_color(stream)
    for linea in log.rstrip().splitlines():
        print(colorear_linea(linea, usar_color), file=stream)
    print(file=stream)


def compilar_archivo(input_path: Path, output_program_path: Path, output_log_path: Path) -> bool:
    try:
        codigo_fuente = input_path.read_text(encoding="utf-8")
        resultado = compilar_codigo(codigo_fuente, ejecutar=True)
        output_program_path.write_text(resultado.python_code, encoding="utf-8")
        output_log_path.write_text(resultado.log, encoding="utf-8")
        imprimir_log(resultado.log)
        return True
    except CompilerError as exc:
        log = BANNER + "\n\nMiniCompilador - errores encontrados\n\n" + exc.as_text() + "\n"
        output_program_path.write_text("# No se genero codigo por errores de compilacion.\n", encoding="utf-8")
        output_log_path.write_text(log, encoding="utf-8")
        imprimir_log(log, es_error=True)
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description="MiniCompilador para circuitos digitales.")
    parser.add_argument("--input", default="input.txt", help="Archivo fuente del lenguaje.")
    parser.add_argument("--output-python", default="output_program.py", help="Archivo Python generado.")
    parser.add_argument("--output-log", default="output.txt", help="Archivo de logs/resultados.")
    parser.add_argument("--run-tests", action="store_true", help="Ejecuta todos los casos en tests/.")
    parser.add_argument("--debug", action="store_true", help="Muestra traceback si ocurre un error inesperado.")
    args = parser.parse_args()

    output_log_path = ROOT / args.output_log

    try:
        if args.run_tests:
            return 0 if run_tests(output_log_path, usar_color=soporta_color(sys.stdout)) else 1

        input_path = ROOT / args.input
        output_program_path = ROOT / args.output_python
        return 0 if compilar_archivo(input_path, output_program_path, output_log_path) else 1
    except Exception as exc:  # Proteccion para errores no esperados durante la demo academica.
        if args.debug:
            traceback.print_exc()
        log = f"{BANNER}\n\nMiniCompilador - error inesperado\n\n{type(exc).__name__}: {exc}\n"
        output_log_path.write_text(log, encoding="utf-8")
        imprimir_log(log, es_error=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
