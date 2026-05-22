from __future__ import annotations

# Este archivo es el punto de entrada del proyecto: recibe argumentos,
# llama al pipeline del compilador y escribe los archivos de salida.
import argparse
import os
from pathlib import Path
import sys
import traceback

# Se importa la funcion principal de compilacion y el banner que se muestra en consola.
from compiler_pipeline import BANNER, compilar_codigo
# Se importa el error base para capturar fallos controlados del compilador.
from compiler_errors import CompilerError
# Se importa el runner de pruebas para activar la opcion --run-tests.
from tests.run_tests import run_tests


# ROOT representa la carpeta raiz del proyecto, sin depender de desde donde se ejecute Python.
ROOT = Path(__file__).resolve().parent


# Codigos ANSI usados para pintar mensajes en terminales compatibles.
COLOR_RESET = "\033[0m"
COLOR_VERDE = "\033[92m"
COLOR_ROJO = "\033[91m"
COLOR_AMARILLO = "\033[93m"
COLOR_CYAN = "\033[96m"


def soporta_color(stream) -> bool:
    """Indica si la terminal permite colores y si el usuario no los desactivo."""
    return stream.isatty() and os.environ.get("NO_COLOR") is None


def colorear_linea(linea: str, usar_color: bool) -> str:
    """Recibe una linea del log y la devuelve con color segun su significado."""
    if not usar_color:
        return linea

    # Verde para compilacion correcta y fases exitosas.
    if linea.startswith("MiniCompilador - compilacion exitosa") or ": OK" in linea:
        return f"{COLOR_VERDE}{linea}{COLOR_RESET}"

    # Rojo para errores generales reportados por el compilador.
    if linea.startswith("MiniCompilador - errores") or linea.startswith("MiniCompilador - error"):
        return f"{COLOR_ROJO}{linea}{COLOR_RESET}"

    # Rojo para errores semanticos, lexicos y sintacticos.
    if linea.startswith("[semantico]"):
        return f"{COLOR_ROJO}{linea}{COLOR_RESET}"
    if linea.startswith("[lexico]") or linea.startswith("[sintactico]"):
        return f"{COLOR_ROJO}{linea}{COLOR_RESET}"

    # Amarillo para advertencias.
    if linea.startswith("[WARN]") or "advertencia" in linea.lower():
        return f"{COLOR_AMARILLO}{linea}{COLOR_RESET}"

    # Cyan para encabezados y separadores visuales.
    if linea.startswith("=") or linea.startswith(" MiniCompilador") or linea.startswith("==="):
        return f"{COLOR_CYAN}{linea}{COLOR_RESET}"

    # Las demas lineas se imprimen sin cambios.
    return linea


def imprimir_log(log: str, es_error: bool = False) -> None:
    """Imprime el log completo en stdout o stderr, aplicando colores si se puede."""
    stream = sys.stderr if es_error else sys.stdout
    usar_color = soporta_color(stream)

    # Se colorea linea por linea para que cada fase o error tenga su propio color.
    for linea in log.rstrip().splitlines():
        print(colorear_linea(linea, usar_color), file=stream)

    # Linea final en blanco para separar visualmente una ejecucion de otra.
    print(file=stream)


def compilar_archivo(input_path: Path, output_program_path: Path, output_log_path: Path) -> bool:
    """Compila un archivo fuente y deja como resultado un Python generado y un log."""
    try:
        # Se lee el programa escrito en el mini lenguaje.
        codigo_fuente = input_path.read_text(encoding="utf-8")

        # Se ejecutan todas las fases del compilador y tambien el Python generado.
        resultado = compilar_codigo(codigo_fuente, ejecutar=True)

        # Se guardan los artefactos principales para revisarlos despues de compilar.
        output_program_path.write_text(resultado.python_code, encoding="utf-8")
        output_log_path.write_text(resultado.log, encoding="utf-8")

        # Se muestra en consola el mismo log que queda guardado en output.txt.
        imprimir_log(resultado.log)
        return True
    except CompilerError as exc:
        # Si el error es controlado, se arma un log pedagogico en lugar de mostrar traceback.
        log = BANNER + "\n\nMiniCompilador - errores encontrados\n\n" + exc.as_text() + "\n"

        # Si hay errores, no se deja un programa Python incompleto o peligroso.
        output_program_path.write_text("# No se genero codigo por errores de compilacion.\n", encoding="utf-8")
        output_log_path.write_text(log, encoding="utf-8")

        # Los errores se imprimen por stderr para diferenciarlos de una compilacion correcta.
        imprimir_log(log, es_error=True)
        return False


def main() -> int:
    """Configura la linea de comandos y decide si compilar o correr pruebas."""
    # argparse define las opciones disponibles al ejecutar python main.py.
    parser = argparse.ArgumentParser(description="MiniCompilador para circuitos digitales.")
    parser.add_argument("--input", default="input.txt", help="Archivo fuente del lenguaje.")
    parser.add_argument("--output-python", default="output_program.py", help="Archivo Python generado.")
    parser.add_argument("--output-log", default="output.txt", help="Archivo de logs/resultados.")
    parser.add_argument("--run-tests", action="store_true", help="Ejecuta todos los casos en tests/.")
    parser.add_argument("--debug", action="store_true", help="Muestra traceback si ocurre un error inesperado.")
    args = parser.parse_args()

    # La ruta del log se calcula desde la raiz del proyecto para ser estable.
    output_log_path = ROOT / args.output_log

    try:
        # Con --run-tests no se compila input.txt, sino toda la bateria de pruebas.
        if args.run_tests:
            return 0 if run_tests(output_log_path, usar_color=soporta_color(sys.stdout)) else 1

        # En modo normal se compila el archivo indicado por --input.
        input_path = ROOT / args.input
        output_program_path = ROOT / args.output_python
        return 0 if compilar_archivo(input_path, output_program_path, output_log_path) else 1
    except Exception as exc:  # Proteccion para errores no esperados durante la demo academica.
        # --debug permite ver el traceback completo si se necesita diagnosticar el problema.
        if args.debug:
            traceback.print_exc()

        # Sin --debug, se muestra un mensaje compacto para no ensuciar la presentacion.
        log = f"{BANNER}\n\nMiniCompilador - error inesperado\n\n{type(exc).__name__}: {exc}\n"
        output_log_path.write_text(log, encoding="utf-8")
        imprimir_log(log, es_error=True)
        return 1


# Permite que el archivo se ejecute como script: python main.py.
if __name__ == "__main__":
    raise SystemExit(main())
