// Nombre de la gramatica; ANTLR genera clases como gramaticaLexer y gramaticaParser.
grammar gramatica;

// Regla inicial: un programa tiene una o mas instrucciones y luego termina el archivo.
program : (gateDecl | connection | outputDecl)+ EOF ;

// Declaracion de compuerta: puerta A = AND(x, y);
gateDecl : 'puerta' ID '=' GATETYPE '(' inputs ')' ';' ;

// Tipos de compuerta permitidos por el lenguaje.
GATETYPE : 'AND' | 'OR' | 'NOT' ;

// Lista de entradas separadas por coma: x, y, A.
inputs : ID (',' ID)* ;

// Conexion de una senal origen hacia una senal destino: conectar B a salida;
connection : 'conectar' ID 'a' ID ';' ;

// Instruccion para imprimir una senal al final: mostrar salida;
outputDecl : 'mostrar' ID ';' ;

// Identificador valido para compuertas y senales.
ID: [a-zA-Z_][a-zA-Z_0-9]* ;

// Comentarios de una linea, ignorados por el lexer.
LINE_COMMENT: '//' ~[\r\n]* -> skip ;

// Comentarios de bloque, tambien ignorados por el lexer.
BLOCK_COMMENT: '/*' .*? '*/' -> skip ;

// Espacios, tabs y saltos de linea no generan tokens utiles para el parser.
WS: [ \t\r\n]+ -> skip ;
