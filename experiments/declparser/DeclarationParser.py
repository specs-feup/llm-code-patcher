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
        4,1,13,72,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,1,0,5,0,10,8,0,10,0,12,
        0,13,9,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
        1,1,1,1,5,1,31,8,1,10,1,12,1,34,9,1,3,1,36,8,1,1,1,1,1,1,1,1,1,5,
        1,42,8,1,10,1,12,1,45,9,1,1,1,1,1,1,1,1,1,1,1,1,1,5,1,53,8,1,10,
        1,12,1,56,9,1,3,1,58,8,1,1,2,1,2,1,2,1,2,1,2,1,3,1,3,3,3,67,8,3,
        1,3,3,3,70,8,3,1,3,0,0,4,0,2,4,6,0,0,78,0,11,1,0,0,0,2,57,1,0,0,
        0,4,59,1,0,0,0,6,64,1,0,0,0,8,10,3,2,1,0,9,8,1,0,0,0,10,13,1,0,0,
        0,11,9,1,0,0,0,11,12,1,0,0,0,12,1,1,0,0,0,13,11,1,0,0,0,14,15,5,
        9,0,0,15,16,5,11,0,0,16,17,5,1,0,0,17,58,3,6,3,0,18,19,5,5,0,0,19,
        20,5,11,0,0,20,21,5,1,0,0,21,58,3,6,3,0,22,23,5,6,0,0,23,24,5,11,
        0,0,24,25,5,1,0,0,25,35,3,6,3,0,26,27,5,2,0,0,27,32,3,6,3,0,28,29,
        5,3,0,0,29,31,3,6,3,0,30,28,1,0,0,0,31,34,1,0,0,0,32,30,1,0,0,0,
        32,33,1,0,0,0,33,36,1,0,0,0,34,32,1,0,0,0,35,26,1,0,0,0,35,36,1,
        0,0,0,36,58,1,0,0,0,37,38,5,7,0,0,38,39,5,11,0,0,39,43,5,1,0,0,40,
        42,3,4,2,0,41,40,1,0,0,0,42,45,1,0,0,0,43,41,1,0,0,0,43,44,1,0,0,
        0,44,58,1,0,0,0,45,43,1,0,0,0,46,47,5,8,0,0,47,48,5,11,0,0,48,49,
        5,1,0,0,49,54,5,11,0,0,50,51,5,3,0,0,51,53,5,11,0,0,52,50,1,0,0,
        0,53,56,1,0,0,0,54,52,1,0,0,0,54,55,1,0,0,0,55,58,1,0,0,0,56,54,
        1,0,0,0,57,14,1,0,0,0,57,18,1,0,0,0,57,22,1,0,0,0,57,37,1,0,0,0,
        57,46,1,0,0,0,58,3,1,0,0,0,59,60,5,10,0,0,60,61,5,11,0,0,61,62,5,
        1,0,0,62,63,3,6,3,0,63,5,1,0,0,0,64,66,5,11,0,0,65,67,5,12,0,0,66,
        65,1,0,0,0,66,67,1,0,0,0,67,69,1,0,0,0,68,70,5,13,0,0,69,68,1,0,
        0,0,69,70,1,0,0,0,70,7,1,0,0,0,8,11,32,35,43,54,57,66,69
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
                      "ID", "PTRS", "ARRS" ]

    RULE_start = 0
    RULE_declaration = 1
    RULE_member = 2
    RULE_type = 3

    ruleNames =  [ "start", "declaration", "member", "type" ]

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
    PTRS=12
    ARRS=13

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
            self.state = 11
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 992) != 0):
                self.state = 8
                self.declaration()
                self.state = 13
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
            self.decl_type = None # Token
            self.name = None # Token
            self.aliased_type = None # TypeContext
            self.var_type = None # TypeContext
            self.return_type = None # TypeContext
            self._type = None # TypeContext
            self.arg_types = list() # of TypeContexts
            self._ID = None # Token
            self.enum_values = list() # of Tokens

        def ALIAS(self):
            return self.getToken(DeclarationParser.ALIAS, 0)

        def ID(self, i:int=None):
            if i is None:
                return self.getTokens(DeclarationParser.ID)
            else:
                return self.getToken(DeclarationParser.ID, i)

        def type_(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DeclarationParser.TypeContext)
            else:
                return self.getTypedRuleContext(DeclarationParser.TypeContext,i)


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
            self.state = 57
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [9]:
                self.enterOuterAlt(localctx, 1)
                self.state = 14
                localctx.decl_type = self.match(DeclarationParser.ALIAS)
                self.state = 15
                localctx.name = self.match(DeclarationParser.ID)
                self.state = 16
                self.match(DeclarationParser.T__0)
                self.state = 17
                localctx.aliased_type = self.type_()
                pass
            elif token in [5]:
                self.enterOuterAlt(localctx, 2)
                self.state = 18
                localctx.decl_type = self.match(DeclarationParser.VAR)
                self.state = 19
                localctx.name = self.match(DeclarationParser.ID)
                self.state = 20
                self.match(DeclarationParser.T__0)
                self.state = 21
                localctx.var_type = self.type_()
                pass
            elif token in [6]:
                self.enterOuterAlt(localctx, 3)
                self.state = 22
                localctx.decl_type = self.match(DeclarationParser.FUNC)
                self.state = 23
                localctx.name = self.match(DeclarationParser.ID)
                self.state = 24
                self.match(DeclarationParser.T__0)
                self.state = 25
                localctx.return_type = self.type_()
                self.state = 35
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==2:
                    self.state = 26
                    self.match(DeclarationParser.T__1)
                    self.state = 27
                    localctx._type = self.type_()
                    localctx.arg_types.append(localctx._type)
                    self.state = 32
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while _la==3:
                        self.state = 28
                        self.match(DeclarationParser.T__2)
                        self.state = 29
                        localctx._type = self.type_()
                        localctx.arg_types.append(localctx._type)
                        self.state = 34
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)



                pass
            elif token in [7]:
                self.enterOuterAlt(localctx, 4)
                self.state = 37
                localctx.decl_type = self.match(DeclarationParser.STRUCT)
                self.state = 38
                localctx.name = self.match(DeclarationParser.ID)
                self.state = 39
                self.match(DeclarationParser.T__0)
                self.state = 43
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==10:
                    self.state = 40
                    self.member()
                    self.state = 45
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                pass
            elif token in [8]:
                self.enterOuterAlt(localctx, 5)
                self.state = 46
                localctx.decl_type = self.match(DeclarationParser.ENUM)
                self.state = 47
                localctx.name = self.match(DeclarationParser.ID)
                self.state = 48
                self.match(DeclarationParser.T__0)
                self.state = 49
                localctx._ID = self.match(DeclarationParser.ID)
                localctx.enum_values.append(localctx._ID)
                self.state = 54
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==3:
                    self.state = 50
                    self.match(DeclarationParser.T__2)
                    self.state = 51
                    localctx._ID = self.match(DeclarationParser.ID)
                    localctx.enum_values.append(localctx._ID)
                    self.state = 56
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
            self.memb_type = None # TypeContext

        def MEMBER(self):
            return self.getToken(DeclarationParser.MEMBER, 0)

        def ID(self):
            return self.getToken(DeclarationParser.ID, 0)

        def type_(self):
            return self.getTypedRuleContext(DeclarationParser.TypeContext,0)


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
            self.state = 59
            self.match(DeclarationParser.MEMBER)
            self.state = 60
            localctx.name = self.match(DeclarationParser.ID)
            self.state = 61
            self.match(DeclarationParser.T__0)
            self.state = 62
            localctx.memb_type = self.type_()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TypeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.type_specifier = None # Token
            self.ptr_n = None # Token
            self.arr_n = None # Token

        def ID(self):
            return self.getToken(DeclarationParser.ID, 0)

        def PTRS(self):
            return self.getToken(DeclarationParser.PTRS, 0)

        def ARRS(self):
            return self.getToken(DeclarationParser.ARRS, 0)

        def getRuleIndex(self):
            return DeclarationParser.RULE_type

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterType" ):
                listener.enterType(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitType" ):
                listener.exitType(self)




    def type_(self):

        localctx = DeclarationParser.TypeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_type)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 64
            localctx.type_specifier = self.match(DeclarationParser.ID)
            self.state = 66
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==12:
                self.state = 65
                localctx.ptr_n = self.match(DeclarationParser.PTRS)


            self.state = 69
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==13:
                self.state = 68
                localctx.arr_n = self.match(DeclarationParser.ARRS)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





