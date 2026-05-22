# Guion de exposicion del codigo

Este archivo sirve como apoyo rapido para explicar el proyecto sin leer cada linea literalmente.
La idea es contar el flujo completo del compilador y luego entrar a los archivos clave.

## Idea principal

Frase sugerida:

> Nuestro proyecto es un mini compilador para un lenguaje de circuitos digitales. El usuario escribe instrucciones como declarar compuertas AND, OR y NOT, conectar senales y mostrar una salida. El compilador valida ese programa y lo traduce a Python ejecutable.

## Flujo general

Frase sugerida:

> El compilador trabaja por fases: primero ANTLR hace analisis lexico y sintactico, despues construimos un AST propio, luego validamos reglas semanticas, generamos codigo intermedio IR/TAC y finalmente traducimos ese IR a Python.

Fases que debes mencionar:

1. `gramatica.g4`: define el lenguaje.
2. `antlr_driver.py`: usa ANTLR para crear tokens y parse tree.
3. `ast_builder.py`: convierte el parse tree en AST propio.
4. `semantic_analyzer/analyzer.py`: valida reglas del circuito.
5. `codegen/ir_generator.py`: genera IR/TAC.
6. `codegen/python_generator.py`: genera Python ejecutable.
7. `compiler_pipeline.py`: une todas las fases.
8. `main.py`: permite ejecutar el compilador desde consola.
9. `tests/run_tests.py`: demuestra que casos validos e invalidos funcionan.

## Archivo por archivo

### `gramatica.g4`

Que decir:

> Aqui esta la definicion formal del lenguaje. La regla inicial `program` acepta declaraciones de puertas, conexiones y salidas. `gateDecl` reconoce instrucciones como `puerta A = AND(x, y);`, `connection` reconoce `conectar B a salida;` y `outputDecl` reconoce `mostrar salida;`. Tambien se definen tokens como `ID`, comentarios y espacios.

### `ast_nodes.py`

Que decir:

> Este archivo define las estructuras de datos del AST. En vez de trabajar directamente con el arbol complejo de ANTLR, usamos clases simples: `GateDecl` para compuertas, `Connection` para conexiones, `OutputDecl` para mostrar una salida y `Program` como nodo raiz.

### `antlr_driver.py`

Que decir:

> Este modulo conecta nuestro codigo con ANTLR. Carga el lexer y parser generados, reemplaza los errores tecnicos por mensajes mas pedagogicos y, si no hay errores lexicos o sintacticos, llama al `ASTBuilder`.

### `ast_builder.py`

Que decir:

> Aqui usamos el patron visitor de ANTLR. Cada metodo `visit...` toma una regla de la gramatica y la transforma en un nodo propio del AST. Por ejemplo, `visitGateDecl` lee el nombre, tipo y entradas de una compuerta.

### `semantic_analyzer/analyzer.py`

Que decir:

> Esta es una de las partes mas importantes. Aunque el programa este bien escrito sintacticamente, aqui verificamos si tiene sentido. Validamos compuertas duplicadas, entradas no declaradas, cantidad correcta de entradas para AND, OR y NOT, senales inexistentes al conectar o mostrar, y conexiones circulares usando DFS.

Detalle para explicar DFS:

> Guardamos dependencias entre senales como un grafo. Si durante la busqueda una senal aparece otra vez en la pila actual, significa que hay una dependencia circular.

### `codegen/ir_generator.py`

Que decir:

> Despues de validar, el AST se convierte en una representacion intermedia. Esta representacion es mas simple que el AST y se parece a instrucciones TAC: `A = AND x y`, `salida = B`, `PRINT salida`.

### `codegen/python_generator.py`

Que decir:

> Este modulo traduce cada instruccion IR a Python. Por ejemplo, `AND` se convierte en `and`, `OR` en `or`, `NOT` en `not`, `ASSIGN` en una asignacion y `PRINT` en `print(...)`.

### `compiler_pipeline.py`

Que decir:

> Este archivo es el pegamento del compilador. Ejecuta todas las fases en orden, captura la salida del Python generado y arma el log final con las cinco fases, el IR, el codigo Python y la salida de ejecucion.

### `main.py`

Que decir:

> Este es el punto de entrada. Permite ejecutar `python main.py`, elegir archivo de entrada, elegir archivos de salida y correr pruebas con `--run-tests`. Tambien pinta mensajes con colores para que la demo sea mas clara.

### `tests/run_tests.py`

Que decir:

> Este runner prueba automaticamente programas validos e invalidos. Los validos deben compilar, y los invalidos deben producir errores. Esto demuestra que el compilador no solo genera codigo, sino que tambien detecta fallos.

## Demo recomendada

Comandos:

```bash
python main.py
python output_program.py
python main.py --run-tests
```

Orden para mostrar:

1. Abre `input.txt` y explica el programa de ejemplo.
2. Ejecuta `python main.py`.
3. Muestra `output.txt` para explicar fases, IR y Python generado.
4. Abre `output_program.py` para mostrar la traduccion a Python.
5. Ejecuta `python main.py --run-tests` para cerrar con validacion.

## Cierre sugerido

Frase sugerida:

> En conclusion, el proyecto implementa el flujo clasico de un compilador pequeno: gramatica, parseo, AST, semantica, codigo intermedio y codigo final. Lo aplicamos a circuitos digitales para que cada fase se pueda ver con ejemplos concretos y faciles de probar.
