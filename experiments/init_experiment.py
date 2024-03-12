from antlr4 import *
from declparser.DeclarationLexer import DeclarationLexer
from declparser.DeclarationParser import DeclarationParser
import json
import re
import os

def parse_errors(file):
    errors = {}

    typename_matches = list(set(re.findall("unknown type name '([^']+)'", file)))
    identifier_matches = list(set(re.findall("use of undeclared identifier '([^']+)'", file)))
    function_matches = list(set(re.findall("call to undeclared function '([^']+)'", file)))
    library_function_matches = list(set(re.findall("call to undeclared library function '([^']+)'", file)))

    if len(typename_matches) != 0:
        errors["unknown_type_name"] = typename_matches

    if len(identifier_matches) != 0:
        errors["use_undeclared_identifier"] = identifier_matches
    
    if len(function_matches) != 0:
        errors["call_undeclared_function"] = function_matches

    if len(library_function_matches) != 0:
        errors["call_undeclared_library_function"] = library_function_matches

    return errors

def parse_declarations(file):
    input_stream = InputStream(file)
    lexer = DeclarationLexer(input_stream)
    token_stream = CommonTokenStream(lexer)

    parser = DeclarationParser(token_stream)
    tree = parser.start()

    #print(tree.toStringTree(recog=parser))

    return tree

def get_declarations_as_json(tree):
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

def main():
    experiment = {}

    metadata_path = input("Enter experiment metadata path (press enter for default path \"./metadata\"): ")

    metadata_path = "./metadata" if metadata_path == "" else metadata_path
    
    if os.path.exists(metadata_path):
        if os.path.isfile(metadata_path):
            print("Provided metadata path is a file, not a directory")
            return
    else:
        os.mkdir(metadata_path)

    project_path = input("Enter experiment project path (relative to metadata path): ")

    project_path = os.path.join(metadata_path, project_path)

    if os.path.exists(project_path):
        if os.path.isfile(project_path):
            print("Provided experiment project path is a file")
            return

        project_metadata_path = os.path.join(project_path, "project.json")

        try:
            with open(project_metadata_path, "r") as metadata_file:
                project_metadata = json.load(metadata_file)
                metadata_file.close()
        except Exception:
            print("Couldn't open project metadata")
            return

    else:
        project_metadata = {
            "org": input("Enter project organization: "),
            "project": input("Enter project name: "),
            "repository": input("Enter project repository: "),
            "license": input("Enter project license: ")
        }

        os.mkdir(project_path)

        project_metadata_path = os.path.join(project_path, "project.json")

        try:
            with open(project_metadata_path, 'w') as metadata_file:
                metadata_file.write(json.dumps(project_metadata, indent=4))
                metadata_file.close()
        except Exception:
            print("Couldn't create project metadata")
            return

    project = project_metadata["project"]
    org = project_metadata["org"]
    print(f"Using project {project} from organization {org}")

    experiment["name"] = input("Enter the experiment name (press enter for same name as the snippet): ")
    experiment["snippet"] = input("Enter the snippet name: ")
    experiment["name"] = experiment["snippet"] if experiment["name"] == "" else experiment["name"]
    experiment["commit_hash"] = input("Enter the commit hash: ")
    experiment["function_name"] = input("Enter the function name: ")
    experiment["function_path"] = input("Enter the function path: ")

    while True:
        experiment["language"] = input("Enter the language (c/cpp): ")

        if experiment["language"] in ["c", "cpp"]:
            break

        print("Invalid language. Please enter a valid language.")
           
    #errors_filepath = input("Enter the path to the LLVM errors file: ")
    #declarations_filepath = input("Enter the path to the LLVM declarations file: ")

    errors_filepath = "./errors.txt"
    declarations_filepath = "./declarations.txt"

    try:
        with open(errors_filepath, 'r') as file:
            errors_file = file.read()
            experiment["errors"] = parse_errors(errors_file)
            file.close()
    except FileNotFoundError:
        print("Errors file does not exist.")
        return

    try:
        with open(declarations_filepath, 'r') as file:
            declarations_file = file.read()
            #print(declarations_file)
            tree = parse_declarations(declarations_file)
            experiment["declarations"] = get_declarations_as_json(tree)
            file.close()
    except FileNotFoundError:
        print("Declarations file does not exist.")
        return

    experiment_name = experiment["name"]
    experiment_metadata_path = os.path.join(project_path, f"{experiment_name}.json")

    try:
        with open(experiment_metadata_path, 'w') as experiment_file:
            experiment_file.write(json.dumps(experiment, indent=4))
            experiment_file.close()
    except Exception:
        print("Couldn't create experiment file")
        return

    print("Experiment created correctly")
    #print(json.dumps(experiment, indent=4))

if __name__ == "__main__":
    main()