# Generated from ./src/antlr/Declaration.g4 by ANTLR 4.13.1
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
        4,1,16,83,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,1,0,3,0,12,8,0,
        1,0,5,0,15,8,0,10,0,12,0,18,9,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
        1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,1,36,8,1,10,1,12,1,39,9,1,3,1,
        41,8,1,1,1,1,1,1,1,1,1,5,1,47,8,1,10,1,12,1,50,9,1,1,1,1,1,1,1,1,
        1,1,1,1,1,5,1,58,8,1,10,1,12,1,61,9,1,3,1,63,8,1,1,2,3,2,66,8,2,
        1,2,1,2,1,2,1,2,1,2,1,3,1,3,3,3,75,8,3,1,3,3,3,78,8,3,1,4,1,4,1,
        4,1,4,0,0,5,0,2,4,6,8,0,0,90,0,16,1,0,0,0,2,62,1,0,0,0,4,65,1,0,
        0,0,6,72,1,0,0,0,8,79,1,0,0,0,10,12,3,8,4,0,11,10,1,0,0,0,11,12,
        1,0,0,0,12,13,1,0,0,0,13,15,3,2,1,0,14,11,1,0,0,0,15,18,1,0,0,0,
        16,14,1,0,0,0,16,17,1,0,0,0,17,1,1,0,0,0,18,16,1,0,0,0,19,20,5,11,
        0,0,20,21,5,13,0,0,21,22,5,1,0,0,22,63,3,6,3,0,23,24,5,7,0,0,24,
        25,5,13,0,0,25,26,5,1,0,0,26,63,3,6,3,0,27,28,5,8,0,0,28,29,5,13,
        0,0,29,30,5,1,0,0,30,40,3,6,3,0,31,32,5,2,0,0,32,37,3,6,3,0,33,34,
        5,3,0,0,34,36,3,6,3,0,35,33,1,0,0,0,36,39,1,0,0,0,37,35,1,0,0,0,
        37,38,1,0,0,0,38,41,1,0,0,0,39,37,1,0,0,0,40,31,1,0,0,0,40,41,1,
        0,0,0,41,63,1,0,0,0,42,43,5,9,0,0,43,44,5,13,0,0,44,48,5,1,0,0,45,
        47,3,4,2,0,46,45,1,0,0,0,47,50,1,0,0,0,48,46,1,0,0,0,48,49,1,0,0,
        0,49,63,1,0,0,0,50,48,1,0,0,0,51,52,5,10,0,0,52,53,5,13,0,0,53,54,
        5,1,0,0,54,59,5,13,0,0,55,56,5,3,0,0,56,58,5,13,0,0,57,55,1,0,0,
        0,58,61,1,0,0,0,59,57,1,0,0,0,59,60,1,0,0,0,60,63,1,0,0,0,61,59,
        1,0,0,0,62,19,1,0,0,0,62,23,1,0,0,0,62,27,1,0,0,0,62,42,1,0,0,0,
        62,51,1,0,0,0,63,3,1,0,0,0,64,66,5,4,0,0,65,64,1,0,0,0,65,66,1,0,
        0,0,66,67,1,0,0,0,67,68,5,12,0,0,68,69,5,13,0,0,69,70,5,1,0,0,70,
        71,3,6,3,0,71,5,1,0,0,0,72,74,5,13,0,0,73,75,5,14,0,0,74,73,1,0,
        0,0,74,75,1,0,0,0,75,77,1,0,0,0,76,78,5,15,0,0,77,76,1,0,0,0,77,
        78,1,0,0,0,78,7,1,0,0,0,79,80,5,16,0,0,80,81,5,5,0,0,81,9,1,0,0,
        0,10,11,16,37,40,48,59,62,65,74,77
    ]

class DeclarationParser ( Parser ):

    grammarFileName = "Declaration.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "':'", "'->'", "','", "'-'", "'.'", "<INVALID>", 
                     "'var'", "'func'", "'struct'", "'enum'", "'alias'", 
                     "'memb'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "WS", "VAR", "FUNC", "STRUCT", 
                      "ENUM", "ALIAS", "MEMBER", "ID", "PTRS", "ARRS", "INT" ]

    RULE_start = 0
    RULE_declaration = 1
    RULE_member = 2
    RULE_type = 3
    RULE_enumeration = 4

    ruleNames =  [ "start", "declaration", "member", "type", "enumeration" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    WS=6
    VAR=7
    FUNC=8
    STRUCT=9
    ENUM=10
    ALIAS=11
    MEMBER=12
    ID=13
    PTRS=14
    ARRS=15
    INT=16

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


        def enumeration(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DeclarationParser.EnumerationContext)
            else:
                return self.getTypedRuleContext(DeclarationParser.EnumerationContext,i)


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
            self.state = 16
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 69504) != 0):
                self.state = 11
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==16:
                    self.state = 10
                    self.enumeration()


                self.state = 13
                self.declaration()
                self.state = 18
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
            self.state = 62
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [11]:
                self.enterOuterAlt(localctx, 1)
                self.state = 19
                localctx.decl_type = self.match(DeclarationParser.ALIAS)
                self.state = 20
                localctx.name = self.match(DeclarationParser.ID)
                self.state = 21
                self.match(DeclarationParser.T__0)
                self.state = 22
                localctx.aliased_type = self.type_()
                pass
            elif token in [7]:
                self.enterOuterAlt(localctx, 2)
                self.state = 23
                localctx.decl_type = self.match(DeclarationParser.VAR)
                self.state = 24
                localctx.name = self.match(DeclarationParser.ID)
                self.state = 25
                self.match(DeclarationParser.T__0)
                self.state = 26
                localctx.var_type = self.type_()
                pass
            elif token in [8]:
                self.enterOuterAlt(localctx, 3)
                self.state = 27
                localctx.decl_type = self.match(DeclarationParser.FUNC)
                self.state = 28
                localctx.name = self.match(DeclarationParser.ID)
                self.state = 29
                self.match(DeclarationParser.T__0)
                self.state = 30
                localctx.return_type = self.type_()
                self.state = 40
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==2:
                    self.state = 31
                    self.match(DeclarationParser.T__1)
                    self.state = 32
                    localctx._type = self.type_()
                    localctx.arg_types.append(localctx._type)
                    self.state = 37
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while _la==3:
                        self.state = 33
                        self.match(DeclarationParser.T__2)
                        self.state = 34
                        localctx._type = self.type_()
                        localctx.arg_types.append(localctx._type)
                        self.state = 39
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)



                pass
            elif token in [9]:
                self.enterOuterAlt(localctx, 4)
                self.state = 42
                localctx.decl_type = self.match(DeclarationParser.STRUCT)
                self.state = 43
                localctx.name = self.match(DeclarationParser.ID)
                self.state = 44
                self.match(DeclarationParser.T__0)
                self.state = 48
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==4 or _la==12:
                    self.state = 45
                    self.member()
                    self.state = 50
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                pass
            elif token in [10]:
                self.enterOuterAlt(localctx, 5)
                self.state = 51
                localctx.decl_type = self.match(DeclarationParser.ENUM)
                self.state = 52
                localctx.name = self.match(DeclarationParser.ID)
                self.state = 53
                self.match(DeclarationParser.T__0)
                self.state = 54
                localctx._ID = self.match(DeclarationParser.ID)
                localctx.enum_values.append(localctx._ID)
                self.state = 59
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==3:
                    self.state = 55
                    self.match(DeclarationParser.T__2)
                    self.state = 56
                    localctx._ID = self.match(DeclarationParser.ID)
                    localctx.enum_values.append(localctx._ID)
                    self.state = 61
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
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 65
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==4:
                self.state = 64
                self.match(DeclarationParser.T__3)


            self.state = 67
            self.match(DeclarationParser.MEMBER)
            self.state = 68
            localctx.name = self.match(DeclarationParser.ID)
            self.state = 69
            self.match(DeclarationParser.T__0)
            self.state = 70
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
            self.state = 72
            localctx.type_specifier = self.match(DeclarationParser.ID)
            self.state = 74
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==14:
                self.state = 73
                localctx.ptr_n = self.match(DeclarationParser.PTRS)


            self.state = 77
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==15:
                self.state = 76
                localctx.arr_n = self.match(DeclarationParser.ARRS)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class EnumerationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INT(self):
            return self.getToken(DeclarationParser.INT, 0)

        def getRuleIndex(self):
            return DeclarationParser.RULE_enumeration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEnumeration" ):
                listener.enterEnumeration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEnumeration" ):
                listener.exitEnumeration(self)




    def enumeration(self):

        localctx = DeclarationParser.EnumerationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_enumeration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 79
            self.match(DeclarationParser.INT)
            self.state = 80
            self.match(DeclarationParser.T__4)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





