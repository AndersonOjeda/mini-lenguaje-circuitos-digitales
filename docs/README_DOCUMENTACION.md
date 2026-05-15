# README de documentacion

## Objetivo

Esta carpeta contiene la documentacion tecnica del MiniCompilador para circuitos digitales. Los archivos estan ordenados para construir un PDF academico universitario.

## Orden recomendado

1. `01_introduccion.md`
2. `02_arquitectura.md`
3. `03_gramatica.md`
4. `04_semantica.md`
5. `05_codegen.md`
6. `06_pruebas.md`
7. `07_ejecucion.md`
8. `08_conclusiones.md`
9. `09_referencias.md`

## Anexos opcionales

Tambien se pueden incluir:

- `diagramas/arquitectura.mmd`
- `diagramas/modulos.mmd`
- `diagramas/ciclo_dfs.mmd`
- capturas de consola
- codigo fuente relevante

## Comando sugerido con Pandoc

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

## Verificacion antes de entregar

Ejecutar:

```bash
python main.py --run-tests
```

Resultado esperado:

```txt
Resumen: 20/20 casos correctos.
```

## Archivos que no deben subirse

No incluir en el commit:

```txt
*.zip
*.code-workspace
tools/*.jar
__pycache__/
*.pyc
```

