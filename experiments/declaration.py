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

        struct_decls = [decl for decl in declarations if decl["decl_type"] == "struct"]
        enum_decls = [decl for decl in declarations if decl["decl_type"] == "enum"]
        alias_decls = [decl for decl in declarations if decl["decl_type"] == "alias"]
        function_decls = [decl for decl in declarations if decl["decl_type"] == "func"]
        var_decls = [decl for decl in declarations if decl["decl_type"] == "var"]

        c_declarations += DeclParser.get_struct_and_enum_decl_as_c_decls(struct_decls, enum_decls)

        for struct_decl in struct_decls:
            c_declarations.append(DeclParser.get_struct_decl_as_c_def(struct_decl))
    
        for enum_decl in enum_decls:
            c_declarations.append(DeclParser.get_enum_decl_as_c_def(enum_decl))

        for function_decl in function_decls:
            c_declarations.append(DeclParser._get_func_decl_as_c_decl(function_decl))

        for var_decl in var_decls:
            c_declarations.append(DeclParser._get_var_decl_as_c_decl(var_decl))

    # these are just forward declarations for those structs and enums to solve cyclic dependencies
    @staticmethod
    def get_struct_and_enum_decl_as_c_decls(struct_decls, enum_decls):
        c_declarations = []
        
        for struct_decl in struct_decls:
            struct_name = struct_decl["name"]
            c_declarations.append(f"struct {struct_name};")
        
        for enum_decl in enum_decls:
            enum_name = enum_decl["name"]
            c_declarations.append(f"enum {enum_name};")
        
        return c_declarations
    
    @staticmethod
    def get_struct_decl_as_c_def(struct_decl):
        struct_name = struct_decl["name"]
        struct_members = struct_decl["members"]

        # typedef struct <struct_name> {...} <struct_name>; in order to take into account cases where "struct <struct_name>" is used in the code
        c_def = f"typedef struct {struct_name} {{\n"

        for member in struct_members:
            c_def += f"\t{DeclParser._get_var_decl_as_c_decl(member)}\n"

        c_def += f"}} {struct_name};"

        return c_def

    @staticmethod
    def get_enum_decl_as_c_def(enum_decl):
        enum_name = enum_decl["name"]
        enum_values = enum_decl["values"]

        c_def = f"enum {enum_name} {{\n"

        for enum_value in enum_values:
            c_def += f"\t{enum_value},\n"

        c_def += f"}} {enum_name};"

        return c_def
    
    @staticmethod
    def _get_func_decl_as_c_decl(func_decl):
        name = func_decl["name"]
        return_type = DeclParser.func_decl["return_type"]
        arg_types = func_decl["argument_types"]

        type_specifier, pointer_n, _ = DeclParser._get_type_components(return_type)

        return_type_str = f"{type_specifier} {'*'*pointer_n}"

        c_decl = f"{return_type_str} {name}("

        for i, arg_type in enumerate(arg_types):
            type_specifier, pointer_n, array_n = DeclParser._get_type_components(arg_type)
            c_decl += f"{type_specifier} {'*'*pointer_n}arg{i}{f'[{ARRAY_SIZE}]'*array_n};"

        if len(arg_types) > 0:
            c_decl = c_decl[:-2]

        c_decl += ");"

        return c_decl

    @staticmethod
    def _get_var_decl_as_c_decl(var_decl):
        name = var_decl["name"]
        type = var_decl["type"]

        type_specifier, pointer_n, array_n = DeclParser._get_type_components(type)
        
        return f"{type_specifier} {'*'*pointer_n}{name}{f'[{ARRAY_SIZE}]'*array_n};"
    
    @staticmethod
    def _get_type_components(type):
        type2 = type.replace(" ", "")
            
        has_n_array, array_n = DeclParser._has_n_array(type2)
        
        type_specifier = type2

        if has_n_array:
            type_specifier = DeclParser._get_type_without_n_array(type_specifier)

        has_n_pointer, pointer_n = DeclParser._has_n_pointer(type_specifier)

        if has_n_pointer:
            type_specifier = DeclParser._get_type_without_n_pointer(type_specifier)

        if type_specifier in UNRESOLVED:
            type_specifier = DEFAULT_FOR_UNRESOLVED
        elif type_specifier in PROMPT_PRIMITIVE_TYPE_TO_C_TYPE:
            type_specifier = PROMPT_PRIMITIVE_TYPE_TO_C_TYPE[type_specifier]


        return type_specifier, pointer_n, array_n

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

