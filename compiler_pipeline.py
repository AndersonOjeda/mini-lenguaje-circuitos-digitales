from __future__ import annotations

import contextlib
import io
from dataclasses import dataclass

from antlr_driver import parse_source
from codegen import IRGenerator, PythonGenerator
from semantic_analyzer import DEFAULT_EXTERNAL_VALUES, SemanticAnalyzer


BANNER = """====================================
 MiniCompilador Circuitos Digitales
 ANTLR4 + Python
===================================="""


@dataclass(frozen=True)
class CompilationResult:
    ir_text: str
    python_code: str
    execution_output: str
    log: str


def compilar_codigo(codigo_fuente: str, ejecutar: bool = True) -> CompilationResult:
    ast = parse_source(codigo_fuente)
    contexto = SemanticAnalyzer().analyze(ast)
    ir = IRGenerator().generate(ast)
    python_code = PythonGenerator(DEFAULT_EXTERNAL_VALUES).generate(ir, contexto)
    execution_output = ejecutar_python_generado(python_code) if ejecutar else ""

    ir_text = "\n".join(str(instruccion) for instruccion in ir)
    log = construir_log_exito(ir_text, python_code, execution_output)
    return CompilationResult(ir_text, python_code, execution_output, log)


def ejecutar_python_generado(python_code: str) -> str:
    salida = io.StringIO()
    with contextlib.redirect_stdout(salida):
        exec(compile(python_code, "output_program.py", "exec"), {})
    return salida.getvalue()


def construir_log_exito(ir_text: str, python_code: str, execution_output: str) -> str:
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
    return "\n".join(partes) + "\n"
