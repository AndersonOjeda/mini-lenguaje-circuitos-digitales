# Reexporta el analizador semantico y sus datos publicos desde el paquete.
from semantic_analyzer.analyzer import DEFAULT_EXTERNAL_VALUES, SemanticAnalyzer, SemanticContext
from semantic_analyzer.symbol_table import Symbol, SymbolKind, SymbolTable

# Define la API publica del paquete semantic_analyzer.
__all__ = [
    "DEFAULT_EXTERNAL_VALUES",
    "SemanticAnalyzer",
    "SemanticContext",
    "Symbol",
    "SymbolKind",
    "SymbolTable",
]
