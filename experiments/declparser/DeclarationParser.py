# Generated from ./antlr/Declaration.g4 by ANTLR 4.13.1
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
        4,1,12,63,2,0,7,0,2,1,7,1,2,2,7,2,1,0,5,0,8,8,0,10,0,12,0,11,9,0,
        1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
        5,1,29,8,1,10,1,12,1,32,9,1,3,1,34,8,1,1,1,1,1,1,1,1,1,5,1,40,8,
        1,10,1,12,1,43,9,1,1,1,1,1,1,1,1,1,1,1,1,1,5,1,51,8,1,10,1,12,1,
        54,9,1,3,1,56,8,1,1,2,1,2,1,2,1,2,1,2,1,2,0,0,3,0,2,4,0,0,68,0,9,
        1,0,0,0,2,55,1,0,0,0,4,57,1,0,0,0,6,8,3,2,1,0,7,6,1,0,0,0,8,11,1,
        0,0,0,9,7,1,0,0,0,9,10,1,0,0,0,10,1,1,0,0,0,11,9,1,0,0,0,12,13,5,
        9,0,0,13,14,5,11,0,0,14,15,5,1,0,0,15,56,5,12,0,0,16,17,5,5,0,0,
        17,18,5,11,0,0,18,19,5,1,0,0,19,56,5,12,0,0,20,21,5,6,0,0,21,22,
        5,11,0,0,22,23,5,1,0,0,23,33,5,12,0,0,24,25,5,2,0,0,25,30,5,12,0,
        0,26,27,5,3,0,0,27,29,5,12,0,0,28,26,1,0,0,0,29,32,1,0,0,0,30,28,
        1,0,0,0,30,31,1,0,0,0,31,34,1,0,0,0,32,30,1,0,0,0,33,24,1,0,0,0,
        33,34,1,0,0,0,34,56,1,0,0,0,35,36,5,7,0,0,36,37,5,11,0,0,37,41,5,
        1,0,0,38,40,3,4,2,0,39,38,1,0,0,0,40,43,1,0,0,0,41,39,1,0,0,0,41,
        42,1,0,0,0,42,56,1,0,0,0,43,41,1,0,0,0,44,45,5,8,0,0,45,46,5,11,
        0,0,46,47,5,1,0,0,47,52,5,11,0,0,48,49,5,3,0,0,49,51,5,11,0,0,50,
        48,1,0,0,0,51,54,1,0,0,0,52,50,1,0,0,0,52,53,1,0,0,0,53,56,1,0,0,
        0,54,52,1,0,0,0,55,12,1,0,0,0,55,16,1,0,0,0,55,20,1,0,0,0,55,35,
        1,0,0,0,55,44,1,0,0,0,56,3,1,0,0,0,57,58,5,10,0,0,58,59,5,11,0,0,
        59,60,5,1,0,0,60,61,5,12,0,0,61,5,1,0,0,0,6,9,30,33,41,52,55
    ]

class DeclarationParser ( Parser ):

    grammarFileName = "Declaration.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "':'", "'->'", "','", "<INVALID>", "'var'", 
                     "'func'", "'struct'", "'enum'", "'alias'", "'memb'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "WS", "VAR", "FUNC", "STRUCT", "ENUM", "ALIAS", "MEMBER", 
                      "ID", "TYPE" ]

    RULE_start = 0
    RULE_declaration = 1
    RULE_member = 2

    ruleNames =  [ "start", "declaration", "member" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    WS=4
    VAR=5
    FUNC=6
    STRUCT=7
    ENUM=8
    ALIAS=9
    MEMBER=10
    ID=11
    TYPE=12

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class StartContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def declaration(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DeclarationParser.DeclarationContext)
            else:
                return self.getTypedRuleContext(DeclarationParser.DeclarationContext,i)


        def getRuleIndex(self):
            return DeclarationParser.RULE_start

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStart" ):
                listener.enterStart(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStart" ):
                listener.exitStart(self)




    def start(self):

        localctx = DeclarationParser.StartContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_start)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 9
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 992) != 0):
                self.state = 6
                self.declaration()
                self.state = 11
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DeclarationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.type_ = None # Token
            self.name = None # Token
            self.typename = None # Token
            self.return_typename = None # Token
            self._TYPE = None # Token
            self.arg_typenames = list() # of Tokens
            self._ID = None # Token
            self.enum_values = list() # of Tokens

        def ALIAS(self):
            return self.getToken(DeclarationParser.ALIAS, 0)

        def ID(self, i:int=None):
            if i is None:
                return self.getTokens(DeclarationParser.ID)
            else:
                return self.getToken(DeclarationParser.ID, i)

        def TYPE(self, i:int=None):
            if i is None:
                return self.getTokens(DeclarationParser.TYPE)
            else:
                return self.getToken(DeclarationParser.TYPE, i)

        def VAR(self):
            return self.getToken(DeclarationParser.VAR, 0)

        def FUNC(self):
            return self.getToken(DeclarationParser.FUNC, 0)

        def STRUCT(self):
            return self.getToken(DeclarationParser.STRUCT, 0)

        def member(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DeclarationParser.MemberContext)
            else:
                return self.getTypedRuleContext(DeclarationParser.MemberContext,i)


        def ENUM(self):
            return self.getToken(DeclarationParser.ENUM, 0)

        def getRuleIndex(self):
            return DeclarationParser.RULE_declaration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDeclaration" ):
                listener.enterDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDeclaration" ):
                listener.exitDeclaration(self)




    def declaration(self):

        localctx = DeclarationParser.DeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_declaration)
        self._la = 0 # Token type
        try:
            self.state = 55
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [9]:
                self.enterOuterAlt(localctx, 1)
                self.state = 12
                localctx.type_ = self.match(DeclarationParser.ALIAS)
                self.state = 13
                localctx.name = self.match(DeclarationParser.ID)
                self.state = 14
                self.match(DeclarationParser.T__0)
                self.state = 15
                localctx.typename = self.match(DeclarationParser.TYPE)
                pass
            elif token in [5]:
                self.enterOuterAlt(localctx, 2)
                self.state = 16
                localctx.type_ = self.match(DeclarationParser.VAR)
                self.state = 17
                localctx.name = self.match(DeclarationParser.ID)
                self.state = 18
                self.match(DeclarationParser.T__0)
                self.state = 19
                localctx.typename = self.match(DeclarationParser.TYPE)
                pass
            elif token in [6]:
                self.enterOuterAlt(localctx, 3)
                self.state = 20
                localctx.type_ = self.match(DeclarationParser.FUNC)
                self.state = 21
                localctx.name = self.match(DeclarationParser.ID)
                self.state = 22
                self.match(DeclarationParser.T__0)
                self.state = 23
                localctx.return_typename = self.match(DeclarationParser.TYPE)
                self.state = 33
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==2:
                    self.state = 24
                    self.match(DeclarationParser.T__1)
                    self.state = 25
                    localctx._TYPE = self.match(DeclarationParser.TYPE)
                    localctx.arg_typenames.append(localctx._TYPE)
                    self.state = 30
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while _la==3:
                        self.state = 26
                        self.match(DeclarationParser.T__2)
                        self.state = 27
                        localctx._TYPE = self.match(DeclarationParser.TYPE)
                        localctx.arg_typenames.append(localctx._TYPE)
                        self.state = 32
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)



                pass
            elif token in [7]:
                self.enterOuterAlt(localctx, 4)
                self.state = 35
                localctx.type_ = self.match(DeclarationParser.STRUCT)
                self.state = 36
                localctx.name = self.match(DeclarationParser.ID)
                self.state = 37
                self.match(DeclarationParser.T__0)
                self.state = 41
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==10:
                    self.state = 38
                    self.member()
                    self.state = 43
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                pass
            elif token in [8]:
                self.enterOuterAlt(localctx, 5)
                self.state = 44
                localctx.type_ = self.match(DeclarationParser.ENUM)
                self.state = 45
                localctx.name = self.match(DeclarationParser.ID)
                self.state = 46
                self.match(DeclarationParser.T__0)
                self.state = 47
                localctx._ID = self.match(DeclarationParser.ID)
                localctx.enum_values.append(localctx._ID)
                self.state = 52
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==3:
                    self.state = 48
                    self.match(DeclarationParser.T__2)
                    self.state = 49
                    localctx._ID = self.match(DeclarationParser.ID)
                    localctx.enum_values.append(localctx._ID)
                    self.state = 54
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MemberContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.name = None # Token
            self.type_ = None # Token

        def MEMBER(self):
            return self.getToken(DeclarationParser.MEMBER, 0)

        def ID(self):
            return self.getToken(DeclarationParser.ID, 0)

        def TYPE(self):
            return self.getToken(DeclarationParser.TYPE, 0)

        def getRuleIndex(self):
            return DeclarationParser.RULE_member

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMember" ):
                listener.enterMember(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMember" ):
                listener.exitMember(self)




    def member(self):

        localctx = DeclarationParser.MemberContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_member)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 57
            self.match(DeclarationParser.MEMBER)
            self.state = 58
            localctx.name = self.match(DeclarationParser.ID)
            self.state = 59
            self.match(DeclarationParser.T__0)
            self.state = 60
            localctx.type_ = self.match(DeclarationParser.TYPE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





