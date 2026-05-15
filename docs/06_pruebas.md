# 06. Pruebas

## Organizacion

Las pruebas estan en:

```txt
tests/
├── valid/
├── invalid/
└── run_tests.py
```

Comandos:

```bash
python main.py --run-tests
python tests/run_tests.py
```

## Casos validos

| Archivo | Que valida |
|---|---|
| `01_and_simple.txt` | Comentarios de linea y bloque, compuerta `AND`, salida directa. |
| `02_or_simple.txt` | Compuerta `OR`. |
| `03_not_simple.txt` | Compuerta `NOT`. |
| `04_varias_compuertas.txt` | Encadenamiento `AND`, `NOT`, `OR`. |
| `05_mostrar_puerta_directa.txt` | Mostrar una puerta directamente. |
| `06_conexion_salida.txt` | Conexion a `salida`. |
| `07_usa_z_externa.txt` | Uso de entrada externa `z`. |
| `08_varias_salidas.txt` | Multiples salidas. |
| `09_circuito_complejo.txt` | Circuito con varias dependencias. |
| `10_minimo_valido.txt` | Caso minimo `mostrar x;`. |

Ejemplo de caso valido con comentarios:

```txt
// Circuito simple con una compuerta AND.
puerta A = AND(x, y);
/* Se muestra directamente la senal generada por la puerta. */
mostrar A;
```

## Casos invalidos

| Archivo | Error esperado |
|---|---|
| `01_entrada_no_declarada.txt` | Entrada `q` no declarada. |
| `02_not_dos_entradas.txt` | `NOT` con dos entradas. |
| `03_and_una_entrada.txt` | `AND` con una entrada. |
| `04_or_una_entrada.txt` | `OR` con una entrada. |
| `05_puerta_duplicada.txt` | Puerta `A` duplicada. |
| `06_conectar_origen_inexistente.txt` | Conexion desde `q`. |
| `07_mostrar_inexistente.txt` | Mostrar `salida` inexistente. |
| `08_conexion_circular.txt` | Ciclo `A -> B -> A`. |
| `09_falta_punto_y_coma.txt` | Falta punto y coma. |
| `10_tipo_compuerta_invalido.txt` | Tipo `XOR` invalido. |

## Mensajes reales

```txt
[semantico] linea 1, columna 0: La senal 'q' se usa como entrada de 'A' antes de declararse. Usa una puerta previa, una conexion previa o una entrada externa permitida: x, y, z.
[semantico] linea 1, columna 0: La compuerta NOT 'A' debe recibir exactamente una entrada; recibio 2.
[semantico] linea 1, columna 0: La compuerta AND 'A' debe recibir minimo dos entradas; recibio 1.
[semantico] linea 1, columna 0: La compuerta OR 'A' debe recibir minimo dos entradas; recibio 1.
[semantico] linea 2, columna 0: La puerta 'A' ya fue declarada previamente.
[semantico] linea 1, columna 0: No se puede conectar desde 'q' porque esa senal no existe todavia.
[semantico] linea 1, columna 0: No se puede mostrar 'salida' porque esa senal no existe.
[semantico] linea 0, columna 0: Conexion circular detectada: A -> B -> A.
[sintactico] linea 2, columna 0: Error sintactico cerca de 'mostrar'. Detalle de ANTLR: missing ';' at 'mostrar'
[sintactico] linea 1, columna 11: Tipo de compuerta invalido 'XOR'. Usa AND, OR o NOT.
```

## Salida esperada

```txt
MiniCompilador - ejecucion automatica de pruebas
Casos validos encontrados: 10
Casos con errores encontrados: 10
...
Resumen: 20/20 casos correctos.
```

