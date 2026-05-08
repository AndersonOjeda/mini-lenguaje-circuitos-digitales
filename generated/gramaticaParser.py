# Generated from gramatica.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,14,47,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,1,0,1,0,1,0,4,
        0,14,8,0,11,0,12,0,15,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
        1,1,2,1,2,1,2,5,2,32,8,2,10,2,12,2,35,9,2,1,3,1,3,1,3,1,3,1,3,1,
        3,1,4,1,4,1,4,1,4,1,4,0,0,5,0,2,4,6,8,0,0,45,0,13,1,0,0,0,2,19,1,
        0,0,0,4,28,1,0,0,0,6,36,1,0,0,0,8,42,1,0,0,0,10,14,3,2,1,0,11,14,
        3,6,3,0,12,14,3,8,4,0,13,10,1,0,0,0,13,11,1,0,0,0,13,12,1,0,0,0,
        14,15,1,0,0,0,15,13,1,0,0,0,15,16,1,0,0,0,16,17,1,0,0,0,17,18,5,
        0,0,1,18,1,1,0,0,0,19,20,5,1,0,0,20,21,5,11,0,0,21,22,5,2,0,0,22,
        23,5,10,0,0,23,24,5,3,0,0,24,25,3,4,2,0,25,26,5,4,0,0,26,27,5,5,
        0,0,27,3,1,0,0,0,28,33,5,11,0,0,29,30,5,6,0,0,30,32,5,11,0,0,31,
        29,1,0,0,0,32,35,1,0,0,0,33,31,1,0,0,0,33,34,1,0,0,0,34,5,1,0,0,
        0,35,33,1,0,0,0,36,37,5,7,0,0,37,38,5,11,0,0,38,39,5,8,0,0,39,40,
        5,11,0,0,40,41,5,5,0,0,41,7,1,0,0,0,42,43,5,9,0,0,43,44,5,11,0,0,
        44,45,5,5,0,0,45,9,1,0,0,0,3,13,15,33
    ]

class gramaticaParser ( Parser ):

    grammarFileName = "gramatica.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'puerta'", "'='", "'('", "')'", "';'", 
                     "','", "'conectar'", "'a'", "'mostrar'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "GATETYPE", "ID", "LINE_COMMENT", 
                      "BLOCK_COMMENT", "WS" ]

    RULE_program = 0
    RULE_gateDecl = 1
    RULE_inputs = 2
    RULE_connection = 3
    RULE_outputDecl = 4

    ruleNames =  [ "program", "gateDecl", "inputs", "connection", "outputDecl" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    T__8=9
    GATETYPE=10
    ID=11
    LINE_COMMENT=12
    BLOCK_COMMENT=13
    WS=14

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(gramaticaParser.EOF, 0)

        def gateDecl(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(gramaticaParser.GateDeclContext)
            else:
                return self.getTypedRuleContext(gramaticaParser.GateDeclContext,i)


        def connection(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(gramaticaParser.ConnectionContext)
            else:
                return self.getTypedRuleContext(gramaticaParser.ConnectionContext,i)


        def outputDecl(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(gramaticaParser.OutputDeclContext)
            else:
                return self.getTypedRuleContext(gramaticaParser.OutputDeclContext,i)


        def getRuleIndex(self):
            return gramaticaParser.RULE_program

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProgram" ):
                listener.enterProgram(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProgram" ):
                listener.exitProgram(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProgram" ):
                return visitor.visitProgram(self)
            else:
                return visitor.visitChildren(self)




    def program(self):

        localctx = gramaticaParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 13 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 13
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [1]:
                    self.state = 10
                    self.gateDecl()
                    pass
                elif token in [7]:
                    self.state = 11
                    self.connection()
                    pass
                elif token in [9]:
                    self.state = 12
                    self.outputDecl()
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 15 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 642) != 0)):
                    break

            self.state = 17
            self.match(gramaticaParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class GateDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(gramaticaParser.ID, 0)

        def GATETYPE(self):
            return self.getToken(gramaticaParser.GATETYPE, 0)

        def inputs(self):
            return self.getTypedRuleContext(gramaticaParser.InputsContext,0)


        def getRuleIndex(self):
            return gramaticaParser.RULE_gateDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterGateDecl" ):
                listener.enterGateDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitGateDecl" ):
                listener.exitGateDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitGateDecl" ):
                return visitor.visitGateDecl(self)
            else:
                return visitor.visitChildren(self)




    def gateDecl(self):

        localctx = gramaticaParser.GateDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_gateDecl)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 19
            self.match(gramaticaParser.T__0)
            self.state = 20
            self.match(gramaticaParser.ID)
            self.state = 21
            self.match(gramaticaParser.T__1)
            self.state = 22
            self.match(gramaticaParser.GATETYPE)
            self.state = 23
            self.match(gramaticaParser.T__2)
            self.state = 24
            self.inputs()
            self.state = 25
            self.match(gramaticaParser.T__3)
            self.state = 26
            self.match(gramaticaParser.T__4)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class InputsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self, i:int=None):
            if i is None:
                return self.getTokens(gramaticaParser.ID)
            else:
                return self.getToken(gramaticaParser.ID, i)

        def getRuleIndex(self):
            return gramaticaParser.RULE_inputs

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInputs" ):
                listener.enterInputs(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInputs" ):
                listener.exitInputs(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInputs" ):
                return visitor.visitInputs(self)
            else:
                return visitor.visitChildren(self)




    def inputs(self):

        localctx = gramaticaParser.InputsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_inputs)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 28
            self.match(gramaticaParser.ID)
            self.state = 33
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==6:
                self.state = 29
                self.match(gramaticaParser.T__5)
                self.state = 30
                self.match(gramaticaParser.ID)
                self.state = 35
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ConnectionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self, i:int=None):
            if i is None:
                return self.getTokens(gramaticaParser.ID)
            else:
                return self.getToken(gramaticaParser.ID, i)

        def getRuleIndex(self):
            return gramaticaParser.RULE_connection

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterConnection" ):
                listener.enterConnection(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitConnection" ):
                listener.exitConnection(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitConnection" ):
                return visitor.visitConnection(self)
            else:
                return visitor.visitChildren(self)




    def connection(self):

        localctx = gramaticaParser.ConnectionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_connection)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 36
            self.match(gramaticaParser.T__6)
            self.state = 37
            self.match(gramaticaParser.ID)
            self.state = 38
            self.match(gramaticaParser.T__7)
            self.state = 39
            self.match(gramaticaParser.ID)
            self.state = 40
            self.match(gramaticaParser.T__4)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OutputDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(gramaticaParser.ID, 0)

        def getRuleIndex(self):
            return gramaticaParser.RULE_outputDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOutputDecl" ):
                listener.enterOutputDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOutputDecl" ):
                listener.exitOutputDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOutputDecl" ):
                return visitor.visitOutputDecl(self)
            else:
                return visitor.visitChildren(self)




    def outputDecl(self):

        localctx = gramaticaParser.OutputDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_outputDecl)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 42
            self.match(gramaticaParser.T__8)
            self.state = 43
            self.match(gramaticaParser.ID)
            self.state = 44
            self.match(gramaticaParser.T__4)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





