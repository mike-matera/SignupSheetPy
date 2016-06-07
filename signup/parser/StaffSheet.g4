grammar StaffSheet;          

sheet 
	: statement* 
	; 
	
statement 
	: campout
	| role 
	;

campout 
	: 'campout' 'starts' QUOTE
	;
	
role
	: 'role' QUOTE '(' coordinator+ description job+ ')'
	;

coordinator 
	: 'coordinator' QUOTE QUOTE QUOTE
	;

description 
	: 'description' QUOTE
	;

job 
	: ('protected')? 'job' QUOTE needs? timespec QUOTE?
	;

needs
	: 'needs' NUMBER 
	;
	
timespec 
	: ('repeat' NUMBER 'times' 'starting' TIME
		| 'repeat' 'from' TIME 'to' TIME
		| 'starting' TIME		
		) duration
	;

duration : 'for' NUMBER ('hour'|'hours'|'minutes') ;

NUMBER : DIGIT+ ('.' DIGIT+)? ; 

QUOTE : '{' ~[}]* '}' 
	  | '"' ~["]* '"' 
	  ;
	   
TIME  : '@[' ' '* DAY ' '+ TIMEOFDAY ' '* ']' ;

fragment DAY 
	: [Tt] 'hursday'
	| [Ff] 'riday'
	| [Ss] 'aturday'
	| [Ss] 'unday'
	| [Mm] 'onday'
	| [Tt] 'uesday'
	| [Ww] 'ednsday'
	;

fragment TIMEOFDAY
	: ( DIGIT+ ':' DIGIT+ ('am' | 'pm') )
	| ('M' | 'm') 'idnight'
	| ('N' | 'n') 'oon'
	; 
	
fragment DIGIT : [0-9] ; 
	
// Ignore whitespace when it's not a part of a token.
WS    : [ \t\r\n]+ -> skip ; 