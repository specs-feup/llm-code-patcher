from declaration import DeclParser, DeclConverter

from utils import compile_with_clang

def evaluate_experiment_result(llm_answer, code_snippet):
    decls_tree, lexer_error_listener, parser_error_listener = DeclParser.parse(llm_answer)

    errors = []
    errors += lexer_error_listener.get_errors()
    errors += parser_error_listener.get_errors()

    '''
    if lexer_error_listener.has_errors():
        print("Lexer errors found")

        for error in lexer_error_listener.get_errors():
            print(error)
    
    if parser_error_listener.has_errors():
        print("Parser errors found")
        for error in parser_error_listener.get_errors():
            print(error)
    '''

    if len(errors) > 0:
        print("Errors found")
        for error in errors:
            print(error.message)
        return


    decls = DeclParser.get_declarations_as_obj(decls_tree)


    #for decl in decls:
        #print(decl)

    c_decls = DeclConverter.get_declarations_as_c_decls(decls)

    # TODO do we need to add the main? currently we are adding it because the linker is complaining
    patched_code = "\n".join(c_decls) + code_snippet

    with open("temp.c", "w") as f:
        f.write(patched_code)
        f.close()

    temp_file_path = "temp.c"

    code_compiled, err = compile_with_clang(temp_file_path)

    print(patched_code)
    if code_compiled:
        print("Code compiled successfully")
    else:
        print("Compilation failed")
        print(err)
    #for c_decl in c_decls:
    #    print(c_decl, end="\n")


