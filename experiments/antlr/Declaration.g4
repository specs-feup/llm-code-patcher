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
TYPE: ID ('[]' | '*')*;

start : declaration*  ;
// TODO think about pointers to functions
declaration
    : type=ALIAS name=ID ':' typename=TYPE
    | type=VAR name=ID ':' typename=TYPE
    | type=FUNC name=ID ':' return_typename=TYPE ('->' arg_typenames+=TYPE (',' arg_typenames+=TYPE)* )?
    | type=STRUCT name=ID ':' member*
    | type=ENUM name=ID ':' enum_values+=ID (',' enum_values+=ID)*
    ;

member 
    : MEMBER name=ID ':' type=TYPE ;