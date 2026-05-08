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
