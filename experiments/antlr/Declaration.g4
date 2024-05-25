grammar Declaration;


WS: [ \t\r\n]+ -> skip ;

VAR: 'var' ;
FUNC: 'func' ;
STRUCT: 'struct' ;
ENUM: 'enum' ;
ALIAS: 'alias' ;
MEMBER: 'memb' ;


ID: [a-zA-Z_][a-zA-Z0-9_]* ;

PTRS: ('*' WS*)+ ;
ARRS: ('[' WS*']' WS*)+ ;
INT: [1-9][0-9]* ;

start : (enumeration? declaration)*  ;

// TODO think about pointers to functions
declaration
    : decl_type=ALIAS name=ID ':' aliased_type=type
    | decl_type=VAR name=ID ':' var_type=type
    | decl_type=FUNC name=ID ':' return_type=type ('->' arg_types+=type (',' arg_types+=type)* )?
    | decl_type=STRUCT name=ID ':' member*
    | decl_type=ENUM name=ID ':' enum_values+=ID (',' enum_values+=ID)*
    ;

member 
    : MEMBER name=ID ':' memb_type=type ;

// TODO think about pointers to arrays
type
    : type_specifier=ID ptr_n=PTRS? arr_n=ARRS?
    ;

enumeration
    : INT '.'
    ;