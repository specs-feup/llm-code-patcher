# Generated from ./antlr/Declaration.g4 by ANTLR 4.13.1
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO


def serializedATN():
    return [
        4,0,13,107,6,-1,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,
        2,6,7,6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,1,
        0,1,0,1,1,1,1,1,1,1,2,1,2,1,3,4,3,36,8,3,11,3,12,3,37,1,3,1,3,1,
        4,1,4,1,4,1,4,1,5,1,5,1,5,1,5,1,5,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,
        7,1,7,1,7,1,7,1,7,1,8,1,8,1,8,1,8,1,8,1,8,1,9,1,9,1,9,1,9,1,9,1,
        10,4,10,75,8,10,11,10,12,10,76,1,11,1,11,5,11,81,8,11,10,11,12,11,
        84,9,11,4,11,86,8,11,11,11,12,11,87,1,12,1,12,5,12,92,8,12,10,12,
        12,12,95,9,12,1,12,1,12,5,12,99,8,12,10,12,12,12,102,9,12,4,12,104,
        8,12,11,12,12,12,105,0,0,13,1,1,3,2,5,3,7,4,9,5,11,6,13,7,15,8,17,
        9,19,10,21,11,23,12,25,13,1,0,2,3,0,9,10,13,13,32,32,4,0,48,57,65,
        90,95,95,97,122,113,0,1,1,0,0,0,0,3,1,0,0,0,0,5,1,0,0,0,0,7,1,0,
        0,0,0,9,1,0,0,0,0,11,1,0,0,0,0,13,1,0,0,0,0,15,1,0,0,0,0,17,1,0,
        0,0,0,19,1,0,0,0,0,21,1,0,0,0,0,23,1,0,0,0,0,25,1,0,0,0,1,27,1,0,
        0,0,3,29,1,0,0,0,5,32,1,0,0,0,7,35,1,0,0,0,9,41,1,0,0,0,11,45,1,
        0,0,0,13,50,1,0,0,0,15,57,1,0,0,0,17,62,1,0,0,0,19,68,1,0,0,0,21,
        74,1,0,0,0,23,85,1,0,0,0,25,103,1,0,0,0,27,28,5,58,0,0,28,2,1,0,
        0,0,29,30,5,45,0,0,30,31,5,62,0,0,31,4,1,0,0,0,32,33,5,44,0,0,33,
        6,1,0,0,0,34,36,7,0,0,0,35,34,1,0,0,0,36,37,1,0,0,0,37,35,1,0,0,
        0,37,38,1,0,0,0,38,39,1,0,0,0,39,40,6,3,0,0,40,8,1,0,0,0,41,42,5,
        118,0,0,42,43,5,97,0,0,43,44,5,114,0,0,44,10,1,0,0,0,45,46,5,102,
        0,0,46,47,5,117,0,0,47,48,5,110,0,0,48,49,5,99,0,0,49,12,1,0,0,0,
        50,51,5,115,0,0,51,52,5,116,0,0,52,53,5,114,0,0,53,54,5,117,0,0,
        54,55,5,99,0,0,55,56,5,116,0,0,56,14,1,0,0,0,57,58,5,101,0,0,58,
        59,5,110,0,0,59,60,5,117,0,0,60,61,5,109,0,0,61,16,1,0,0,0,62,63,
        5,97,0,0,63,64,5,108,0,0,64,65,5,105,0,0,65,66,5,97,0,0,66,67,5,
        115,0,0,67,18,1,0,0,0,68,69,5,109,0,0,69,70,5,101,0,0,70,71,5,109,
        0,0,71,72,5,98,0,0,72,20,1,0,0,0,73,75,7,1,0,0,74,73,1,0,0,0,75,
        76,1,0,0,0,76,74,1,0,0,0,76,77,1,0,0,0,77,22,1,0,0,0,78,82,5,42,
        0,0,79,81,3,7,3,0,80,79,1,0,0,0,81,84,1,0,0,0,82,80,1,0,0,0,82,83,
        1,0,0,0,83,86,1,0,0,0,84,82,1,0,0,0,85,78,1,0,0,0,86,87,1,0,0,0,
        87,85,1,0,0,0,87,88,1,0,0,0,88,24,1,0,0,0,89,93,5,91,0,0,90,92,3,
        7,3,0,91,90,1,0,0,0,92,95,1,0,0,0,93,91,1,0,0,0,93,94,1,0,0,0,94,
        96,1,0,0,0,95,93,1,0,0,0,96,100,5,93,0,0,97,99,3,7,3,0,98,97,1,0,
        0,0,99,102,1,0,0,0,100,98,1,0,0,0,100,101,1,0,0,0,101,104,1,0,0,
        0,102,100,1,0,0,0,103,89,1,0,0,0,104,105,1,0,0,0,105,103,1,0,0,0,
        105,106,1,0,0,0,106,26,1,0,0,0,8,0,37,76,82,87,93,100,105,1,6,0,
        0
    ]

class DeclarationLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    T__0 = 1
    T__1 = 2
    T__2 = 3
    WS = 4
    VAR = 5
    FUNC = 6
    STRUCT = 7
    ENUM = 8
    ALIAS = 9
    MEMBER = 10
    ID = 11
    PTRS = 12
    ARRS = 13

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "':'", "'->'", "','", "'var'", "'func'", "'struct'", "'enum'", 
            "'alias'", "'memb'" ]

    symbolicNames = [ "<INVALID>",
            "WS", "VAR", "FUNC", "STRUCT", "ENUM", "ALIAS", "MEMBER", "ID", 
            "PTRS", "ARRS" ]

    ruleNames = [ "T__0", "T__1", "T__2", "WS", "VAR", "FUNC", "STRUCT", 
                  "ENUM", "ALIAS", "MEMBER", "ID", "PTRS", "ARRS" ]

    grammarFileName = "Declaration.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.1")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


