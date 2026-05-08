# MiniCompilador para circuitos digitales

Proyecto final de Compiladores: un mini compilador en Python + ANTLR4 para un lenguaje academico de circuitos digitales.

El lenguaje permite declarar compuertas `AND`, `OR`, `NOT`, conectar senales y mostrar resultados. El compilador realiza analisis lexico, sintactico, semantico, generacion de codigo intermedio IR/TAC y traduccion a Python ejecutable.

## Requisitos

- Python 3.10 o superior.
- Java instalado para ejecutar ANTLR4.
- `antlr4-python3-runtime==4.13.2`.
- ANTLR `antlr-4.13.2-complete.jar` ubicado en `tools/`.

## Instalacion

Instalar dependencias de Python:

```bash
pip install -r requirements.txt
```

Crear la carpeta de herramientas y descargar ANTLR:

```bash
mkdir -p tools
curl -L -o tools/antlr-4.13.2-complete.jar https://www.antlr.org/download/antlr-4.13.2-complete.jar
```

Generar Lexer, Parser y Visitor:

```bash
java -jar tools/antlr-4.13.2-complete.jar -Dlanguage=Python3 -visitor -o generated gramatica.g4
```

## Comandos principales

Compilar el archivo `input.txt`:

```bash
python main.py
```

Ejecutar el Python generado:

```bash
python output_program.py
```

Ejecutar todas las pruebas:

```bash
python main.py --run-tests
```

Tambien se puede ejecutar el runner separado:

```bash
python tests/run_tests.py
```

## Estructura del proyecto

```txt
mini-lenguaje-circuitos-digitales/
├── main.py
├── input.txt
├── output_program.py
├── output.txt
├── requirements.txt
├── README.md
├── gramatica.g4
├── .gitignore
├── antlr_driver.py
├── ast_builder.py
├── ast_nodes.py
├── compiler_errors.py
├── compiler_pipeline.py
├── semantic_analyzer/
│   ├── __init__.py
│   └── analyzer.py
├── codegen/
│   ├── __init__.py
│   ├── ir_generator.py
│   └── python_generator.py
├── generated/
├── tests/
│   ├── valid/
│   ├── invalid/
│   └── run_tests.py
├── docs/
│   ├── doc_proyecto_grupo1.pdf
│   ├── arquitectura.md
│   └── diagramas/
└── tools/
    └── antlr-4.13.2-complete.jar
```

## Gramatica

Archivo principal: `gramatica.g4`.

```antlr
program : (gateDecl | connection | outputDecl)+ EOF ;
gateDecl : 'puerta' ID '=' GATETYPE '(' inputs ')' ';' ;
GATETYPE : 'AND' | 'OR' | 'NOT' ;
inputs : ID (',' ID)* ;
connection : 'conectar' ID 'a' ID ';' ;
outputDecl : 'mostrar' ID ';' ;
ID: [a-zA-Z_][a-zA-Z_0-9]* ;
WS: [ \t\r\n]+ -> skip ;
```

## Ejemplo

Entrada en `input.txt`:

```txt
puerta A = AND(x, y);
puerta B = NOT(A);
conectar B a salida;
mostrar salida;
```

IR/TAC generado:

```txt
A = AND x y
B = NOT A
salida = B
PRINT salida
```

Python generado:

```python
x, y = True, False
A = x and y
B = not A
salida = B
print(salida)
```

Salida:

```txt
True
```

## Fases del compilador

Al ejecutar `python main.py`, la consola muestra un banner y las fases:

```txt
====================================
 MiniCompilador Circuitos Digitales
 ANTLR4 + Python
====================================

[1/5] Analisis lexico: OK
[2/5] Analisis sintactico: OK
[3/5] Analisis semantico: OK
[4/5] Generacion IR/TAC: OK
[5/5] Traduccion Python: OK
```

En terminal compatible se usan colores:

- Verde: compilacion correcta y pruebas exitosas.
- Rojo: errores lexicos, sintacticos o semanticos.
- Amarillo: advertencias.
- Cyan: banner y secciones.

## Analisis semantico

El lenguaje base no incluye declaracion explicita de entradas. Por decision tecnica del proyecto, el analizador semantico permite las senales externas `x`, `y`, `z`.

Valores usados al traducir a Python:

```python
x = True
y = False
z = True
```

Validaciones implementadas:

- Senales usadas como entrada antes de declararse.
- `NOT` debe recibir exactamente una entrada.
- `AND` y `OR` deben recibir minimo dos entradas.
- No se permite declarar dos veces la misma puerta.
- No se permite conectar desde una senal inexistente.
- No se permite mostrar una senal inexistente.
- Deteccion de conexiones circulares con DFS.

Ejemplo de error semantico:

```txt
puerta A = AND(q, y);
mostrar A;
```

Resultado:

```txt
[semantico] linea 1, columna 0: La senal 'q' se usa como entrada de 'A' antes de declararse.
```

## Pruebas

La carpeta `tests/` contiene:

- `tests/valid/`: 10 programas validos.
- `tests/invalid/`: 10 programas con errores esperados.
- `tests/run_tests.py`: runner separado para la demo.

Cobertura:

- Circuitos `AND`, `OR`, `NOT`.
- Varias compuertas conectadas.
- Mostrar puertas directamente.
- Conexiones a salidas.
- Uso de `x`, `y`, `z` como entradas externas.
- Varias salidas.
- Casos semanticos invalidos.
- Errores sintacticos como falta de punto y coma.
- Tipo de compuerta invalido.

## Documentacion

La carpeta `docs/` contiene:

- `docs/arquitectura.md`: arquitectura y diagramas Mermaid.
- `docs/diagramas/`: diagramas separados para capturas o presentacion.
- `docs/doc_proyecto_grupo1.pdf`: documento final del grupo.

## Autores

Grupo 1.

Integrantes:

- Completar nombre 1.
- Completar nombre 2.
- Completar nombre 3.
