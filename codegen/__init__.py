# Reexporta las clases principales de codegen para importarlas desde "codegen".
from codegen.ir_generator import IRGenerator, IRInstruction
from codegen.python_generator import PythonGenerator

# Define que nombres se consideran publicos cuando otro modulo importa codegen.
__all__ = ["IRGenerator", "IRInstruction", "PythonGenerator"]
