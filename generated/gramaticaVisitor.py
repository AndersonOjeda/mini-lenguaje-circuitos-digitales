# Generated from gramatica.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .gramaticaParser import gramaticaParser
else:
    from gramaticaParser import gramaticaParser

# This class defines a complete generic visitor for a parse tree produced by gramaticaParser.

class gramaticaVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by gramaticaParser#program.
    def visitProgram(self, ctx:gramaticaParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gramaticaParser#gateDecl.
    def visitGateDecl(self, ctx:gramaticaParser.GateDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gramaticaParser#inputs.
    def visitInputs(self, ctx:gramaticaParser.InputsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gramaticaParser#connection.
    def visitConnection(self, ctx:gramaticaParser.ConnectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gramaticaParser#outputDecl.
    def visitOutputDecl(self, ctx:gramaticaParser.OutputDeclContext):
        return self.visitChildren(ctx)



del gramaticaParser