grammar Declaration;


WS: [ \t\r\n]+ -> skip ;

VAR: 'var' ;
FUNC: 'func' ;
STRUCT: 'struct' ;
ENUM: 'enum' ;
ALIAS: 'alias' ;
MEMBER: 'memb' ;


ID: [a-zA-Z0-9_]+ ;

// TODO make this more stricted (pointers before arrays) and allow white space between pointers and arrays
// TODO think about pointers to arrays
TYPE: ID '*'* ('[' ']')*;

start : declaration*  ;
// TODO think about pointers to functions
declaration
    : decl_type=ALIAS name=ID ':' aliased_type=TYPE
    | decl_type=VAR name=ID ':' var_type=TYPE
    | decl_type=FUNC name=ID ':' return_type=TYPE ('->' arg_types+=TYPE (',' arg_types+=TYPE)* )?
    | decl_type=STRUCT name=ID ':' member*
    | decl_type=ENUM name=ID ':' enum_values+=ID (',' enum_values+=ID)*
    ;

member 
    : MEMBER name=ID ':' memb_type=TYPE ;