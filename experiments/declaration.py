from antlr4 import *
from declparser.DeclarationLexer import DeclarationLexer
from declparser.DeclarationParser import DeclarationParser

class DeclParser:
    @staticmethod
    def parse(declarations):
        input_stream = InputStream(declarations)
        lexer = DeclarationLexer(input_stream)
        token_stream = CommonTokenStream(lexer)

        parser = DeclarationParser(token_stream)
        tree = parser.start()

        #print(tree.toStringTree(recog=parser))

        return tree

    @staticmethod
    def get_declarations_as_obj(tree):
        declarations = []

        for node in tree.children:
            if isinstance(tree, TerminalNode):
                return

            declaration_type = node.type_.text

            if declaration_type == "var":
                declarations.append(
                    {
                        "type": "var",
                        "name": node.name.text,
                        "typename": node.typename.text
                    }
                )
            elif declaration_type == "func":
                declarations.append(
                    {
                        "type": "func",
                        "name": node.name.text,
                        "return_typename": node.return_typename.text,
                        "argument_typenames": [typename.text for typename in node.arg_typenames]
                    }
                )
            elif declaration_type == "struct":
                members = []
                for child in node.children:
                    if isinstance(child, DeclarationParser.MemberContext):
                        members.append({
                            "name": child.name.text,
                            "typename": child.typename.text
                        })
                declarations.append({
                    "type": "struct",
                    "name": node.name.text,
                    "members": members
                })

            elif declaration_type == "enum":
                declarations.append(
                    {
                        "type": "enum",
                        "name": node.name.text,
                        "values": [enum_value.text for enum_value in node.enum_values]
                    }
                )
            elif declaration_type == "alias":
                declarations.append(
                    {
                        "type": "alias",
                        "name": node.name.text,
                        "typename": node.typename.text
                    }
                )

        #print(declarations)

        return declarations

    @staticmethod
    def get_declarations_as_c_str(declarations):
        pass