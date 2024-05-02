from antlr4 import *
from declparser.DeclarationLexer import DeclarationLexer
from declparser.DeclarationParser import DeclarationParser


UNRESOLVED = ["UNRESOLVED", "Unresolved", "unresolved"] # give some leeway to the LLM for case sensitivity

DEFAULT_FOR_UNRESOLVED = "int"

PROMPT_PRIMITIVE_TYPE_TO_C_TYPE = {
    "char": "char",
    "uchar": "unsigned char",
    "int": "int",
    "uint": "unsigned int",
    "long": "long",
    "ulong": "unsigned long",
    "double": "double",
    "void": "void"
}

ARRAY_SIZE = 10000

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
                        "decl_type": "var",
                        "name": node.name.text,
                        "type": node.type.text
                    }
                )
            elif declaration_type == "func":
                declarations.append(
                    {
                        "decl_type": "func",
                        "name": node.name.text,
                        "return_type": node.return_type.text,
                        "argument_types": [type.text for type in node.arg_types]
                    }
                )
            elif declaration_type == "struct":
                members = []
                for child in node.children:
                    if isinstance(child, DeclarationParser.MemberContext):
                        members.append({
                            "name": child.name.text,
                            "type": child.type.text
                        })
                declarations.append({
                    "decl_type": "struct",
                    "name": node.name.text,
                    "members": members
                })

            elif declaration_type == "enum":
                declarations.append(
                    {
                        "decl_type": "enum",
                        "name": node.name.text,
                        "values": [enum_value.text for enum_value in node.enum_values]
                    }
                )
            elif declaration_type == "alias":
                declarations.append(
                    {
                        "decl_type": "alias",
                        "name": node.name.text,
                        "type": node.type.text
                    }
                )

        #print(declarations)

        return declarations

    @staticmethod
    def get_declarations_as_c_decls(declarations):
        c_declarations = []

        var_decls = [decl for decl in declarations if decl["decl_type"] == "var"]

        for var_decl in var_decls:
            c_declarations.append(DeclParser._get_var_declaration_as_c_str(var_decl))

    @staticmethod
    def _get_var_declaration_as_c_decl(var_decl):
        name = var_decl["name"]

        type = var_decl["type"].replace(" ", "")
            
        has_n_array, array_n = DeclParser._has_n_array(type)
        
        type_without_declarators = type

        if has_n_array:
            type_without_declarators = DeclParser._get_type_without_n_array(type_without_declarators)

        has_n_pointer, pointer_n = DeclParser._has_n_pointer(type_without_declarators)

        if has_n_pointer:
            type_without_declarators = DeclParser._get_type_without_n_pointer(type_without_declarators)

        if type_without_declarators in UNRESOLVED:
            type_without_declarators = DEFAULT_FOR_UNRESOLVED
        elif type_without_declarators in PROMPT_PRIMITIVE_TYPE_TO_C_TYPE:
            type_without_declarators = PROMPT_PRIMITIVE_TYPE_TO_C_TYPE[type_without_declarators]
        

        return f"{type_without_declarators} {'*'*pointer_n}{name}{f'[{ARRAY_SIZE}]'*array_n};"
    
    @staticmethod
    def _has_n_array(type):
        n = type.count("[]")

        return n > 0, n

    
    @staticmethod
    def _has_n_pointer(type):
        n = type.count("*")

        return n > 0, n
    
    @staticmethod
    def _get_type_without_n_array(type):
        occ = type.find("[")

        return type[:occ]

    @staticmethod
    def _get_type_without_n_pointer(type):
        occ = type.find("*")

        return type[:occ]

parser = DeclParser()

var_del = {
    "name": "a",
    "type": "ulong"
}

print(parser._get_var_declaration_as_c_decl(var_del))