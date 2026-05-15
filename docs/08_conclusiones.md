# 08. Conclusiones

## Conclusiones tecnicas

El MiniCompilador implementa una cadena de compilacion completa para un lenguaje pequeno y controlado. El proyecto separa correctamente las fases principales: analisis lexico, analisis sintactico, AST, analisis semantico, IR/TAC y traduccion a Python.

## Aprendizajes

El proyecto evidencia que la gramatica no es suficiente para validar todo un lenguaje. Reglas como la cantidad de entradas de `NOT`, `AND` y `OR` se resuelven semanticamente, no solo sintacticamente.

Tambien muestra la utilidad de una tabla de simbolos para detectar duplicados, senales inexistentes y dependencias circulares.

## Ventajas

- Arquitectura clara y modular.
- Uso real de ANTLR4.
- AST propio simple.
- Errores claros por fase.
- IR/TAC legible.
- Python generado ejecutable.
- Pruebas validas e invalidas automatizadas.
- Soporte de comentarios de linea y bloque.

## Limitaciones reales

- No existe declaracion explicita de entradas.
- Solo existen compuertas `AND`, `OR` y `NOT`.
- No hay optimizacion de codigo.
- No hay interfaz grafica.
- No hay simulacion temporal de circuitos.
- No se genera codigo maquina ni bytecode.

## Mejoras futuras

- Agregar declaracion formal de entradas.
- Agregar compuertas `XOR`, `NAND` y `NOR`.
- Mejorar la linea reportada para ciclos.
- Agregar pruebas unitarias con `pytest`.
- Exportar el grafo del circuito a Mermaid.
- Permitir configurar valores de entrada desde consola.

