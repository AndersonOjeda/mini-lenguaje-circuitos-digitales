# README de documentacion

## Objetivo

Esta carpeta contiene la documentacion tecnica del MiniCompilador para circuitos digitales. Los archivos estan organizados para convertirse en un PDF academico universitario.

## Orden recomendado para el PDF

Unir los archivos en este orden:

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

Despues de las referencias se pueden agregar:

- `arquitectura.md`: documento previo de arquitectura resumida.
- `diagramas/arquitectura.mmd`
- `diagramas/modulos.mmd`
- `diagramas/ciclo_dfs.mmd`
- Capturas reales de consola.
- `doc_proyecto_grupo1.pdf`, si se conserva como version entregable anterior.

## Comando sugerido con Pandoc

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

## Recomendaciones para entrega

- Verificar que el PDF final conserve los bloques de codigo.
- Exportar los diagramas Mermaid como imagenes si el conversor no soporta Mermaid directamente.
- Completar portada institucional si la universidad lo exige.
- Incluir autores: Anderson Ojeda, Samuel Ibarra y Diego Ceron.
- Ejecutar pruebas antes de la defensa:

```bash
python main.py --run-tests
```

Resultado esperado:

```txt
Resumen: 20/20 casos correctos.
```

