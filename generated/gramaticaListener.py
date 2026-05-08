# Generated from gramatica.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .gramaticaParser import gramaticaParser
else:
    from gramaticaParser import gramaticaParser

# This class defines a complete listener for a parse tree produced by gramaticaParser.
class gramaticaListener(ParseTreeListener):

    # Enter a parse tree produced by gramaticaParser#program.
    def enterProgram(self, ctx:gramaticaParser.ProgramContext):
        pass

    # Exit a parse tree produced by gramaticaParser#program.
    def exitProgram(self, ctx:gramaticaParser.ProgramContext):
        pass


    # Enter a parse tree produced by gramaticaParser#gateDecl.
    def enterGateDecl(self, ctx:gramaticaParser.GateDeclContext):
        pass

    # Exit a parse tree produced by gramaticaParser#gateDecl.
    def exitGateDecl(self, ctx:gramaticaParser.GateDeclContext):
        pass


    # Enter a parse tree produced by gramaticaParser#inputs.
    def enterInputs(self, ctx:gramaticaParser.InputsContext):
        pass

    # Exit a parse tree produced by gramaticaParser#inputs.
    def exitInputs(self, ctx:gramaticaParser.InputsContext):
        pass


    # Enter a parse tree produced by gramaticaParser#connection.
    def enterConnection(self, ctx:gramaticaParser.ConnectionContext):
        pass

    # Exit a parse tree produced by gramaticaParser#connection.
    def exitConnection(self, ctx:gramaticaParser.ConnectionContext):
        pass


    # Enter a parse tree produced by gramaticaParser#outputDecl.
    def enterOutputDecl(self, ctx:gramaticaParser.OutputDeclContext):
        pass

    # Exit a parse tree produced by gramaticaParser#outputDecl.
    def exitOutputDecl(self, ctx:gramaticaParser.OutputDeclContext):
        pass



del gramaticaParser