grammar Declaration;


WS: [ \t\r\n]+ -> skip ;

VAR: 'var' ;
FUNC: 'func' ;
STRUCT: 'struct' ;
ENUM: 'enum' ;
ALIAS: 'alias' ;
MEMBER: 'memb' ;

// TODO make this more stricted (pointers before arrays) and allow white space between pointers and arrays
// TODO think about pointers to arrays
ID: [a-zA-Z0-9_]+('[]' | '*')* ;

start : declaration*  ;
// TODO think about pointers to functions
declaration
    : type=ALIAS name=ID ':' typename=ID
    | type=VAR name=ID ':' typename=ID
    | type=FUNC name=ID ':' return_typename=ID ('->' arg_typenames+=ID (',' arg_typenames+=ID)* )?
    | type=STRUCT name=ID ':' member*
    | type=ENUM name=ID ':' enum_values+=ID (',' enum_values+=ID)*
    ;

member 
    : MEMBER name=ID ':' typename=ID ;