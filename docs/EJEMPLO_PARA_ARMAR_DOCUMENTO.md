# Ejemplo para armar el documento final

Este archivo es una guia para que cualquier integrante del grupo pueda construir el informe final a partir de la documentacion tecnica que ya esta en `docs/`.

## 1. Orden sugerido del documento

Usar los capitulos en este orden:

```txt
01_introduccion.md
02_arquitectura.md
03_gramatica.md
04_semantica.md
05_codegen.md
06_pruebas.md
07_ejecucion.md
08_conclusiones.md
09_referencias.md
```

## 2. Estructura recomendada del PDF

```txt
Portada
Tabla de contenido
1. Introduccion
2. Arquitectura del sistema
3. Gramatica del lenguaje
4. Analisis semantico
5. Generacion de codigo
6. Pruebas
7. Ejecucion
8. Conclusiones
9. Referencias
Anexos
```

## 3. Seccion de apropiacion personal

Agregar esta seccion en el documento, preferiblemente antes de conclusiones:

```md
## Apropiacion personal del proyecto

Durante el desarrollo del MiniCompilador comprendimos que una gramatica no es suficiente para garantizar que un programa sea correcto. ANTLR4 nos permitio reconocer la estructura del lenguaje, pero las reglas propias del dominio de circuitos digitales tuvieron que implementarse en el analizador semantico.

Una decision importante fue permitir las senales externas `x`, `y` y `z`, ya que el lenguaje disenado no incluye una instruccion explicita para declarar entradas. Esta decision nos permitio mantener el lenguaje simple y enfocado en compuertas, conexiones y salidas.

Tambien entendimos la utilidad de una representacion intermedia. El IR/TAC nos permitio separar la validacion del programa de la traduccion final a Python. Por ejemplo, `puerta A = AND(x, y);` se transforma primero en `A = AND x y` y luego en `A = x and y`.

El proyecto nos permitio aplicar de forma practica conceptos vistos en clase como analisis lexico, analisis sintactico, analisis semantico, tabla de simbolos, generacion de codigo intermedio y traduccion a codigo destino.
```

## 4. Aportes del equipo

Completar o ajustar segun lo que hizo cada integrante:

```md
## Aportes del equipo

- Anderson Ojeda: implementacion y pruebas del flujo principal del compilador.
- Samuel Ibarra: documentacion tecnica, estructura del informe y pruebas.
- Diego Ceron: analisis semantico, revision de errores y apoyo en generacion de codigo.
```

## 5. Comandos para verificar antes de entregar

Desde la raiz del proyecto:

```bash
python main.py
python main.py --run-tests
python output_program.py
```

El resultado esperado de pruebas es:

```txt
Resumen: 20/20 casos correctos.
```

## 6. Comando opcional para generar PDF con Pandoc

Si Pandoc esta instalado:

```bash
pandoc \
  docs/01_introduccion.md \
  docs/02_arquitectura.md \
  docs/03_gramatica.md \
  docs/04_semantica.md \
  docs/05_codegen.md \
  docs/06_pruebas.md \
  docs/07_ejecucion.md \
  docs/08_conclusiones.md \
  docs/09_referencias.md \
  -o docs/doc_proyecto_grupo1.pdf
```

## 7. Archivos que no se deben subir

Antes de hacer commit revisar que no aparezcan:

```txt
*.zip
*.code-workspace
tools/*.jar
__pycache__/
*.pyc
```

Comando para revisar:

```bash
git status --short
```

## 8. Commit sugerido

```bash
git add docs
git commit -m "agrega guia y documentacion tecnica del informe"
```

