# 03. Gramatica

## Archivo `gramatica.g4`

La gramatica real del lenguaje es:

```antlr
grammar gramatica;

program : (gateDecl | connection | outputDecl)+ EOF ;

gateDecl : 'puerta' ID '=' GATETYPE '(' inputs ')' ';' ;

GATETYPE : 'AND' | 'OR' | 'NOT' ;

inputs : ID (',' ID)* ;

connection : 'conectar' ID 'a' ID ';' ;

outputDecl : 'mostrar' ID ';' ;

ID: [a-zA-Z_][a-zA-Z_0-9]* ;

LINE_COMMENT: '//' ~[\r\n]* -> skip ;

BLOCK_COMMENT: '/*' .*? '*/' -> skip ;

WS: [ \t\r\n]+ -> skip ;
```

## Reglas sintacticas

### `program`

```antlr
program : (gateDecl | connection | outputDecl)+ EOF ;
```

Un programa contiene una o mas instrucciones y termina en fin de archivo.

### `gateDecl`

```antlr
gateDecl : 'puerta' ID '=' GATETYPE '(' inputs ')' ';' ;
```

Declara una compuerta:

```txt
puerta A = AND(x, y);
```

### `inputs`

```antlr
inputs : ID (',' ID)* ;
```

Acepta una lista de identificadores separados por coma. La gramatica permite una o mas entradas; la cantidad correcta se valida en semantica.

### `connection`

```antlr
connection : 'conectar' ID 'a' ID ';' ;
```

Conecta una senal origen a una senal destino.

### `outputDecl`

```antlr
outputDecl : 'mostrar' ID ';' ;
```

Indica que una senal debe imprimirse en el Python generado.

## Reglas lexicas

### `GATETYPE`

```antlr
GATETYPE : 'AND' | 'OR' | 'NOT' ;
```

Solo existen tres tipos de compuertas.

### `ID`

```antlr
ID: [a-zA-Z_][a-zA-Z_0-9]* ;
```

Los identificadores inician con letra o guion bajo y luego pueden tener letras, numeros o guion bajo.

### `LINE_COMMENT`

```antlr
LINE_COMMENT: '//' ~[\r\n]* -> skip ;
```

Permite comentarios de linea. El lexer los ignora.

### `BLOCK_COMMENT`

```antlr
BLOCK_COMMENT: '/*' .*? '*/' -> skip ;
```

Permite comentarios de bloque. Tambien son ignorados por el lexer.

### `WS`

```antlr
WS: [ \t\r\n]+ -> skip ;
```

Ignora espacios, tabulaciones y saltos de linea.

## Ejemplos validos

```txt
// Circuito simple con una compuerta AND.
puerta A = AND(x, y);
/* Se muestra directamente la senal generada por la puerta. */
mostrar A;
```

```txt
puerta A = OR(x, y);
mostrar A;
```

```txt
puerta A = AND(x, y);
puerta B = NOT(A);
conectar B a salida;
mostrar salida;
```

## Ejemplos invalidos

Tipo de compuerta no soportado:

```txt
puerta A = XOR(x, y);
mostrar A;
```

Falta de punto y coma:

```txt
puerta A = AND(x, y)
mostrar A;
```

`NOT` con dos entradas:

```txt
puerta A = NOT(x, y);
mostrar A;
```

Este ultimo programa es sintacticamente aceptado porque `inputs` permite listas, pero se rechaza en analisis semantico.

## Precedencia

No existe precedencia de operadores en la gramatica. El lenguaje no permite expresiones booleanas anidadas como `x and y or z`. En su lugar, cada operacion se representa con una declaracion de puerta.

## Deteccion de errores

Los errores lexicos y sintacticos se recolectan en `antlr_driver.py` con `CollectingErrorListener`.

Ejemplos reales:

```txt
[sintactico] linea 2, columna 0: Error sintactico cerca de 'mostrar'. Detalle de ANTLR: missing ';' at 'mostrar'
```

```txt
[sintactico] linea 1, columna 11: Tipo de compuerta invalido 'XOR'. Usa AND, OR o NOT.
```

