import os
import re

from utils import compile_with_clang

def extract_errors(snippet_name, snippets_path):
    snippet = os.path.join(snippets_path, snippet_name)
    res = compile_with_clang(snippet)

    if not res:
        print("Error checking snippet errors")
        return None

    compile_errors = res[1]

    return compile_errors

def parse_errors(file):
    errors = {}

    typename_matches = list(set(re.findall("unknown type name '([^']+)'", file)))
    identifier_matches = list(set(re.findall("use of undeclared identifier '([^']+)'", file)))
    function_matches = list(set(re.findall("call to undeclared function '([^']+)'", file)))
    library_function_matches = list(set(re.findall("call to undeclared library function '([^']+)'", file)))
    incomplete_type_matches = list(set([match[1] for match in re.findall("has incomplete type '(union|struct|enum) ([^']+)'", file)]))

    if len(typename_matches) != 0:
        errors["unknown_type_name"] = typename_matches

    if len(identifier_matches) != 0:
        errors["use_undeclared_identifier"] = identifier_matches
    
    if len(function_matches) != 0:
        errors["call_undeclared_function"] = function_matches

    if len(library_function_matches) != 0:
        errors["call_undeclared_library_function"] = library_function_matches

    if len(incomplete_type_matches) != 0:
        errors["incomplete_type"] = incomplete_type_matches

    return errors

def get_single_error_type_as_str(metadata, error_type, error_msg_prefix=""):
    if not error_type in metadata["errors"]:
        return ""

    errors = metadata["errors"][error_type]

    error_str = error_msg_prefix + ": "
    
    for i in range(len(errors)):
        error_str += f"\'{errors[i]}\'"

        if i == len(errors) - 1:
            error_str += "."
        else:
            error_str += ", "
     
    return error_str

def get_errors_as_str(data):
    errors = [
        get_single_error_type_as_str(data, "unknown_type_name", "    - unknown type name"),
        get_single_error_type_as_str(data, "use_undeclared_identifier", "    - use of undeclared identifier"),
        get_single_error_type_as_str(data, "call_undeclared_function", "    - call to undeclared function"),
        get_single_error_type_as_str(data, "call_undeclared_library_function", "    - call to undeclared library function"),
        get_single_error_type_as_str(data, "incomplete_type", "    - incomplete type")]

    errors = filter(lambda x: x != "", errors)

    return "\n".join(errors)