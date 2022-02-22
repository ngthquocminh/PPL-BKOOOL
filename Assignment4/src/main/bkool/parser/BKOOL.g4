grammar BKOOL;

@lexer::header {
from lexererr import *
}

options{
	language=Python3;
}

program: 'class' ID LP member RP EOF; 

member: 'static' 'void' ID LB RB LP body RP ;

body: ID '.' ID LB exp RB SEMI;

exp: INTLIT '+' INTLIT | INTLIT;

ID: [a-zA-Z]+ ;

INTLIT: [0-9]+;

LB: '(' ;

RB: ')' ;

LP: '{';

RP: '}';

SEMI: ';' ;

WS : [ \t\r\n]+ -> skip ; // skip spaces, tabs, newlines


ERROR_CHAR: .;