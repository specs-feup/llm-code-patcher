# Generated from Declaration.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .DeclarationParser import DeclarationParser
else:
    from DeclarationParser import DeclarationParser

# This class defines a complete listener for a parse tree produced by DeclarationParser.
class DeclarationListener(ParseTreeListener):

    # Enter a parse tree produced by DeclarationParser#start.
    def enterStart(self, ctx:DeclarationParser.StartContext):
        pass

    # Exit a parse tree produced by DeclarationParser#start.
    def exitStart(self, ctx:DeclarationParser.StartContext):
        pass


    # Enter a parse tree produced by DeclarationParser#declaration.
    def enterDeclaration(self, ctx:DeclarationParser.DeclarationContext):
        pass

    # Exit a parse tree produced by DeclarationParser#declaration.
    def exitDeclaration(self, ctx:DeclarationParser.DeclarationContext):
        pass


    # Enter a parse tree produced by DeclarationParser#member.
    def enterMember(self, ctx:DeclarationParser.MemberContext):
        pass

    # Exit a parse tree produced by DeclarationParser#member.
    def exitMember(self, ctx:DeclarationParser.MemberContext):
        pass



del DeclarationParser