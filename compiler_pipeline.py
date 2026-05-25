from __future__ import annotations

# Este modulo orquesta las fases del compilador de principio a fin.
import contextlib
import io
from dataclasses import dataclass

# Parser/lexer + constructor de AST.
from antlr_driver import describir_tokens, parse_source
from ast_nodes import Connection, GateDecl, OutputDecl, Program
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
    # Se obtiene una explicacion de los tokens para mostrar que hizo la capa lexica.
    tokens_descritos = describir_tokens(codigo_fuente)

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
    log = construir_log_exito(codigo_fuente, tokens_descritos, ast, contexto, ir_text, python_code, execution_output)
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


def construir_log_exito(
    codigo_fuente: str,
    tokens_descritos: list[str],
    ast: Program,
    contexto,
    ir_text: str,
    python_code: str,
    execution_output: str,
) -> str:
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
        "=== Input ejecutado ===",
        codigo_fuente.rstrip() or "(sin codigo fuente)",
        "",
        "=== Capa 1: analisis lexico ===",
        "Que hace: separa el texto de entrada en tokens que el parser puede entender.",
        "Resultado:",
        *(_prefijar_lineas(tokens_descritos) or ["- (sin tokens)"]),
        "",
        "=== Capa 2: analisis sintactico y AST ===",
        "Que hace: verifica la estructura del programa y la convierte en nodos internos.",
        "Resultado:",
        *_prefijar_lineas(_describir_ast(ast)),
        "",
        "=== Capa 3: analisis semantico ===",
        "Que hace: valida que las senales, compuertas, conexiones y salidas tengan sentido.",
        "Resultado:",
        *_prefijar_lineas(_describir_contexto_semantico(contexto)),
        "",
        "=== Capa 4: representacion intermedia IR/TAC ===",
        "Que hace: transforma el AST validado en instrucciones simples e independientes de Python.",
        "Resultado:",
        ir_text or "(sin instrucciones)",
        "",
        "=== Capa 5: traduccion a Python ===",
        "Que hace: convierte el IR/TAC en codigo Python ejecutable.",
        "Resultado:",
        python_code.rstrip(),
        "",
        "=== Capa 6: ejecucion del Python generado ===",
        "Que hace: ejecuta el codigo generado y captura lo que imprime.",
        "Resultado:",
        execution_output.rstrip() or "(sin salida)",
    ]

    # Se agrega salto final para que output.txt sea comodo de leer.
    return "\n".join(partes) + "\n"


def _prefijar_lineas(lineas: list[str]) -> list[str]:
    """Agrega guion a lineas descriptivas para que el reporte sea mas legible."""
    return [f"- {linea}" for linea in lineas]


def _describir_ast(program: Program) -> list[str]:
    """Explica los nodos del AST producidos por la capa sintactica."""
    descripciones: list[str] = []

    for instruccion in program.instrucciones:
        if isinstance(instruccion, GateDecl):
            entradas = ", ".join(instruccion.entradas)
            descripciones.append(
                f"linea {instruccion.linea}: GateDecl -> puerta {instruccion.nombre} de tipo {instruccion.tipo} con entradas {entradas}"
            )
        elif isinstance(instruccion, Connection):
            descripciones.append(
                f"linea {instruccion.linea}: Connection -> conectar {instruccion.origen} a {instruccion.destino}"
            )
        elif isinstance(instruccion, OutputDecl):
            descripciones.append(f"linea {instruccion.linea}: OutputDecl -> mostrar {instruccion.senal}")

    return descripciones or ["No se generaron nodos AST."]


def _describir_contexto_semantico(contexto) -> list[str]:
    """Resume la informacion que dejo lista el analisis semantico."""
    simbolos = [
        _describir_simbolo(nombre, simbolo)
        for nombre, simbolo in sorted(contexto.simbolos.items())
    ]
    compuertas = [
        f"{nombre}({puerta.tipo})"
        for nombre, puerta in sorted(contexto.compuertas.items())
    ]
    dependencias = [
        f"{senal} depende de {', '.join(origenes)}"
        for senal, origenes in sorted(contexto.dependencias.items())
        if origenes
    ]

    lineas = [
        "Reglas validadas: declaracion antes de uso, entradas correctas por compuerta, duplicados, salidas existentes y ciclos.",
        "Tabla de simbolos: " + _unir_o_vacio(simbolos),
        "Entradas externas permitidas: " + _unir_o_vacio(sorted(contexto.senales_externas)),
        "Entradas externas usadas: " + _unir_o_vacio(sorted(contexto.senales_externas_usadas)),
        "Compuertas registradas: " + _unir_o_vacio(compuertas),
        "Senales conocidas: " + _unir_o_vacio(sorted(contexto.senales_conocidas)),
    ]

    if dependencias:
        lineas.append("Dependencias validadas: " + "; ".join(dependencias))
    else:
        lineas.append("Dependencias validadas: ninguna")

    return lineas


def _describir_simbolo(nombre: str, simbolo) -> str:
    """Convierte una entrada de la tabla de simbolos en texto compacto."""
    if simbolo.line:
        return f"{nombre}({simbolo.kind.value}, linea {simbolo.line})"

    return f"{nombre}({simbolo.kind.value})"


def _unir_o_vacio(valores: list[str]) -> str:
    """Une listas para el reporte y evita dejar campos vacios."""
    return ", ".join(valores) if valores else "(ninguna)"
