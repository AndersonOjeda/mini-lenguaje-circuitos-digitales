from __future__ import annotations

# Este modulo orquesta las fases del compilador de principio a fin.
import contextlib
import io
from dataclasses import dataclass

# Parser/lexer + constructor de AST.
from antlr_driver import parse_source
# Generadores de codigo intermedio y codigo Python final.
from codegen import IRGenerator, PythonGenerator
# Analizador semantico y valores por defecto de entradas externas.
from semantic_analyzer import DEFAULT_EXTERNAL_VALUES, SemanticAnalyzer


# Banner reutilizado tanto por la compilacion normal como por las pruebas.
BANNER = """====================================
 MiniCompilador Circuitos Digitales
 ANTLR4 + Python
===================================="""


@dataclass(frozen=True)
class CompilationResult:
    """Agrupa todos los artefactos que produce una compilacion exitosa."""

    # Texto del codigo intermedio tipo TAC.
    ir_text: str
    # Codigo Python que representa el circuito compilado.
    python_code: str
    # Salida real al ejecutar el Python generado.
    execution_output: str
    # Log completo que se muestra al usuario y se guarda en output.txt.
    log: str


def compilar_codigo(codigo_fuente: str, ejecutar: bool = True) -> CompilationResult:
    """Ejecuta las cinco fases: parseo, semantica, IR, Python y ejecucion opcional."""
    # Fase 1 y 2: ANTLR hace analisis lexico/sintactico y luego se construye el AST.
    ast = parse_source(codigo_fuente)

    # Fase 3: se valida que el programa tenga sentido como circuito digital.
    contexto = SemanticAnalyzer().analyze(ast)

    # Fase 4: se traduce el AST a instrucciones intermedias simples.
    ir = IRGenerator().generate(ast)

    # Fase 5: se traduce el IR a Python ejecutable.
    python_code = PythonGenerator(DEFAULT_EXTERNAL_VALUES).generate(ir, contexto)

    # Para la demo, se puede ejecutar el Python generado y capturar su salida.
    execution_output = ejecutar_python_generado(python_code) if ejecutar else ""

    # El IR se convierte a texto para mostrarlo en el log.
    ir_text = "\n".join(str(instruccion) for instruccion in ir)

    # Se arma un reporte unico con fases, IR, Python generado y salida.
    log = construir_log_exito(ir_text, python_code, execution_output)
    return CompilationResult(ir_text, python_code, execution_output, log)


def ejecutar_python_generado(python_code: str) -> str:
    """Ejecuta el Python generado en memoria y captura lo que imprime."""
    # StringIO simula una salida de consola para guardar el resultado de print().
    salida = io.StringIO()

    # redirect_stdout evita que el codigo generado imprima directamente en la terminal.
    with contextlib.redirect_stdout(salida):
        # compile asigna un nombre de archivo virtual para que los errores apunten a output_program.py.
        exec(compile(python_code, "output_program.py", "exec"), {})

    # Se devuelve todo lo que imprimio el programa generado.
    return salida.getvalue()


def construir_log_exito(ir_text: str, python_code: str, execution_output: str) -> str:
    """Construye el texto que resume una compilacion correcta."""
    # La lista permite mantener el orden del reporte sin concatenaciones largas.
    partes = [
        BANNER,
        "",
        "MiniCompilador - compilacion exitosa",
        "",
        "[1/5] Analisis lexico: OK",
        "[2/5] Analisis sintactico: OK",
        "[3/5] Analisis semantico: OK",
        "[4/5] Generacion IR/TAC: OK",
        "[5/5] Traduccion Python: OK",
        "",
        "=== IR/TAC ===",
        ir_text or "(sin instrucciones)",
        "",
        "=== Python generado ===",
        python_code.rstrip(),
        "",
        "=== Salida de ejecucion ===",
        execution_output.rstrip() or "(sin salida)",
    ]

    # Se agrega salto final para que output.txt sea comodo de leer.
    return "\n".join(partes) + "\n"
