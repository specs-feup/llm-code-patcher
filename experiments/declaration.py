from antlr4 import *
from declparser.DeclarationLexer import DeclarationLexer
from declparser.DeclarationParser import DeclarationParser
import json

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

            declaration_type = node.decl_type.text

            if declaration_type == "var":
                declarations.append(
                    {
                        "decl_type": "var",
                        "name": node.name.text,
                        "type": DeclParser.get_type_from_type_node(node.var_type)
                    }
                )
            elif declaration_type == "func":
                declarations.append(
                    {
                        "decl_type": "func",
                        "name": node.name.text,
                        "return_type": DeclParser.get_type_from_type_node(node.return_type),
                        "argument_types": [DeclParser.get_type_from_type_node(type) for type in node.arg_types]
                    }
                )
            elif declaration_type == "struct":
                members = []
                for child in node.children:
                    if isinstance(child, DeclarationParser.MemberContext):
                        members.append({
                            "name": child.name.text,
                            "type": DeclParser.get_type_from_type_node(child.memb_type)
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
                        "type": DeclParser.get_type_from_type_node(node.aliased_type)
                    }
                )

        #print(declarations)

        return declarations

    def get_type_from_type_node(node):
        return {
            "specifier": node.type_specifier.text,
            "ptr_n": 0 if node.ptr_n is None else node.ptr_n.text.count("*"),
            "arr_n": 0 if node.arr_n is None else node.arr_n.text.count("[")
        }

class DeclConverter:
    @staticmethod
    def get_declarations_as_c_decls(declarations):
        c_declarations = []

        struct_decls = [decl for decl in declarations if decl["decl_type"] == "struct"]
        enum_decls = [decl for decl in declarations if decl["decl_type"] == "enum"]
        alias_decls = [decl for decl in declarations if decl["decl_type"] == "alias"]
        function_decls = [decl for decl in declarations if decl["decl_type"] == "func"]
        var_decls = [decl for decl in declarations if decl["decl_type"] == "var"]

        c_declarations += DeclConverter._get_struct_and_enum_decl_as_c_decls(struct_decls, enum_decls)
        c_declarations += map(DeclConverter._get_alias_as_c_decl, alias_decls)
        c_declarations += map(DeclConverter._get_struct_decl_as_c_def, struct_decls)
        c_declarations += map(DeclConverter._get_enum_decl_as_c_def, enum_decls)
        c_declarations += map(DeclConverter._get_func_decl_as_c_decl, function_decls)
        c_declarations += map(DeclConverter._get_var_decl_as_c_decl, var_decls)

        for c_decl in c_declarations:
            print(c_decl)
            print()

        return c_declarations
    
    # We do forward declarations for the structs and enums in order
    #   to remove the need to perform dependency checking between
    #   structs, enums and aliases (and solve their cyclic dependencies)
    # Also, note that "struct <struct_name>" and "<struct_name>" can both referred in the code
    #   but the LLM cant use struct <struct_name> as a type name. As such, we typedef it to <struct_name>
    @staticmethod
    def _get_struct_and_enum_decl_as_c_decls(struct_decls, enum_decls):
        c_declarations = []
        
        for struct_decl in struct_decls:
            struct_name = struct_decl["name"]
            c_declarations.append(f"struct {struct_name};")
            c_declarations.append(f"typedef struct {struct_name} {struct_name};")
        
        for enum_decl in enum_decls:
            enum_name = enum_decl["name"]
            c_declarations.append(f"enum {enum_name};")
            c_declarations.append(f"typedef enum {enum_name} {enum_name};")
        
        return c_declarations
    
    @staticmethod
    def _get_struct_decl_as_c_def(struct_decl):
        struct_name = struct_decl["name"]
        struct_members = struct_decl["members"]

        c_def = f"struct {struct_name} {{\n"

        for member in struct_members:
            c_def += f"    {DeclConverter._get_var_decl_as_c_decl(member)}\n"

        c_def += f"}};"

        return c_def

    @staticmethod
    def _get_enum_decl_as_c_def(enum_decl):
        enum_name = enum_decl["name"]
        enum_values = enum_decl["values"]

        c_def = f"enum {enum_name} {{\n"

        for enum_value in enum_values:
            c_def += f"    {enum_value},\n"

        c_def += f"}};"

        return c_def
    
    @staticmethod
    def _get_func_decl_as_c_decl(func_decl):
        name = func_decl["name"]
        return_type = func_decl["return_type"]
        arg_types = func_decl["argument_types"]

        type_specifier = DeclConverter._get_type_specifier_as_c_type(return_type["specifier"])
        ptr_n = return_type["ptr_n"]
        # arrays are not allowed as return types in C
        return_type_str = f"{type_specifier} {'*'*ptr_n}"

        c_decl = f"{return_type_str}{name}("

        for i, arg_type in enumerate(arg_types):
            type_specifier = DeclConverter._get_type_specifier_as_c_type(arg_type["specifier"])
            ptr_n = arg_type["ptr_n"]
            arr_n = arg_type["arr_n"]

            c_decl += f"{type_specifier} {'*'*ptr_n}arg{i}{f'[{ARRAY_SIZE}]'*arr_n}, "

        if len(arg_types) > 0:
            c_decl = c_decl[:-2]

        c_decl += ");"

        return c_decl

    @staticmethod
    def _get_var_decl_as_c_decl(var_decl):
        name = var_decl["name"]
        type = var_decl["type"]

        type_specifier = DeclConverter._get_type_specifier_as_c_type(type["specifier"])
        ptr_n = type["ptr_n"]
        arr_n = type["arr_n"]

        return f"{type_specifier} {'*'*ptr_n}{name}{f'[{ARRAY_SIZE}]'*arr_n};"
    
    @staticmethod
    def _get_alias_as_c_decl(alias):
        name = alias["name"]
        type = alias["type"]

        type_specifier = DeclConverter._get_type_specifier_as_c_type(type["specifier"])
        ptr_n = type["ptr_n"]
        arr_n = type["arr_n"]

        return f"typedef {type_specifier} {'*'*ptr_n}{name}{f'[{ARRAY_SIZE}]'*arr_n};"

    @staticmethod
    def _get_type_specifier_as_c_type(type_specifier):
        if type_specifier in PROMPT_PRIMITIVE_TYPE_TO_C_TYPE:
            return PROMPT_PRIMITIVE_TYPE_TO_C_TYPE[type_specifier]
        elif type_specifier in UNRESOLVED:
            return DEFAULT_FOR_UNRESOLVED
        else:
            return type_specifier

with open("./decls.txt", "r") as f:
    decls = f.read()
    decls = DeclParser.get_declarations_as_obj(DeclParser.parse(decls))

    #for decl in decls:
        #print(decl)

    c_decls = DeclConverter.get_declarations_as_c_decls(decls)