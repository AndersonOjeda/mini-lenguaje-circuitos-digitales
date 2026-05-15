# 01. Introduccion

## Descripcion general

MiniCompilador es un proyecto academico de Compiladores implementado en Python con ANTLR4. El sistema procesa un lenguaje pequeno orientado a circuitos digitales, donde se pueden declarar compuertas logicas, conectar senales y mostrar resultados.

El lenguaje fuente se escribe con instrucciones como:

```txt
puerta A = AND(x, y);
puerta B = NOT(A);
conectar B a salida;
mostrar salida;
```

El compilador valida el programa, genera una representacion intermedia IR/TAC y traduce el circuito a Python ejecutable.

## Objetivo general

Construir un mini compilador funcional para un lenguaje de circuitos digitales que integre analisis lexico, analisis sintactico, analisis semantico, generacion de codigo intermedio y traduccion a Python.

## Objetivos especificos

- Definir una gramatica ANTLR4 en `gramatica.g4`.
- Generar automaticamente lexer, parser, listener y visitor en `generated/`.
- Construir un AST propio a partir del parse tree de ANTLR.
- Validar reglas semanticas del dominio de circuitos digitales.
- Generar codigo intermedio IR/TAC legible.
- Traducir el IR/TAC a Python ejecutable.
- Automatizar pruebas validas e invalidas.
- Registrar salidas y errores de forma clara.

## Problematica

Un lenguaje puede ser correcto sintacticamente y aun asi ser incorrecto semanticamente. Por ejemplo, esta instruccion tiene forma valida:

```txt
puerta A = AND(q, y);
```

pero `q` no existe como entrada externa, puerta declarada o senal conectada previamente. Por eso el proyecto separa la validacion sintactica, realizada por ANTLR4, de la validacion semantica, realizada por `SemanticAnalyzer`.

## Finalidad del compilador

La finalidad del MiniCompilador es convertir descripciones textuales de circuitos digitales en codigo Python simple. Esto permite observar de forma practica el flujo de un compilador completo, desde el codigo fuente hasta un programa ejecutable.

## Tecnologias usadas

- Python: implementacion del pipeline, AST, semantica, IR/TAC y generador Python.
- ANTLR4: generacion de lexer, parser, listener y visitor.
- Java: ejecucion del archivo `tools/antlr-4.13.2-complete.jar`.
- `antlr4-python3-runtime==4.13.2`: runtime necesario para usar ANTLR4 desde Python.
- Mermaid: diagramas tecnicos en Markdown.

## ANTLR4 en el proyecto

ANTLR4 permite describir un lenguaje mediante reglas gramaticales y generar codigo para reconocerlo. En este proyecto, la gramatica `gramatica.g4` produce:

- `generated/gramaticaLexer.py`
- `generated/gramaticaParser.py`
- `generated/gramaticaListener.py`
- `generated/gramaticaVisitor.py`
- archivos auxiliares `.tokens` e `.interp`

El comando usado para generar esos archivos es:

```bash
java -jar tools/antlr-4.13.2-complete.jar -Dlanguage=Python3 -visitor -o generated gramatica.g4
```

## Flujo general

El flujo real de compilacion esta definido en `compiler_pipeline.py`:

1. `parse_source(codigo_fuente)` ejecuta lexer/parser y construye AST.
2. `SemanticAnalyzer().analyze(ast)` valida reglas semanticas.
3. `IRGenerator().generate(ast)` genera IR/TAC.
4. `PythonGenerator(...).generate(ir, contexto)` genera Python.
5. `main.py` escribe `output_program.py` y `output.txt`.

Captura textual de ejecucion:

```txt
====================================
 MiniCompilador Circuitos Digitales
 ANTLR4 + Python
====================================

MiniCompilador - compilacion exitosa

[1/5] Analisis lexico: OK
[2/5] Analisis sintactico: OK
[3/5] Analisis semantico: OK
[4/5] Generacion IR/TAC: OK
[5/5] Traduccion Python: OK
```

