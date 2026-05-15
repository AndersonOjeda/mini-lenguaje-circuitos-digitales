# 07. Ejecucion

## Requisitos

- Python 3.10 o superior.
- Java.
- Dependencia `antlr4-python3-runtime==4.13.2`.
- JAR de ANTLR4 descargado localmente en `tools/`.

## Instalacion

```bash
pip install -r requirements.txt
```

Descargar ANTLR4:

```bash
mkdir -p tools
curl -L -o tools/antlr-4.13.2-complete.jar https://www.antlr.org/download/antlr-4.13.2-complete.jar
```

## Generar lexer/parser

```bash
java -jar tools/antlr-4.13.2-complete.jar -Dlanguage=Python3 -visitor -o generated gramatica.g4
```

## Ejecutar compilador

```bash
python main.py
```

Archivos usados:

- Entrada: `input.txt`
- Python generado: `output_program.py`
- Log: `output.txt`

## Ejecutar pruebas

```bash
python main.py --run-tests
```

o:

```bash
python tests/run_tests.py
```

## Ejecutar Python generado

```bash
python output_program.py
```

Salida esperada del ejemplo principal:

```txt
True
```

## Ejecucion sin modificar archivos rastreados

Para capturas temporales:

```bash
PYTHONDONTWRITEBYTECODE=1 python main.py --output-python /tmp/minic_output_program.py --output-log /tmp/minic_output.txt
```

Para pruebas temporales:

```bash
PYTHONDONTWRITEBYTECODE=1 python -c "from pathlib import Path; from tests.run_tests import run_tests; run_tests(Path('/tmp/minic_tests_output.txt'), usar_color=False)"
```

