grammar StaffSheet;          

sheet : role+ ; 

role : 'role' QUOTE '(' rolefragment ')' ; 

rolefragment
	: status coordinator+ contact description job*
	;

coordinator 
	: 'coordinator' QUOTE QUOTE QUOTE
	;

contact 
	: 'contact' QUOTE 
	; 
	
description 
	: 'description' QUOTE
	;

status 
	: 'status' ('active' | 'disabled' | 'working')
	; 
	
job 
	: ('protected')? 'job' QUOTE needs? timespec QUOTE?
	;

needs
	: 'needs' NUMBER 
	;
	
timespec 
	: ('repeats' NUMBER 'times' START TIME
		| 'repeats' START TIME 'until' TIME
		| START TIME		
		) duration
	;

duration : ('for'|'every') NUMBER ('hour'|'hours'|'minutes') ;

START : 'starts' | 'starting' ; 

NUMBER : DIGIT+ ('.' DIGIT+)? ; 

QUOTE : '{' ~[}]* '}' 
	  | '"' ~["]* '"' 
	  | '\'' ~[']* '\''
	  ;
	   
TIME  : DAY ' '+ TIMEOFDAY ;

fragment DAY 
	: [Tt] 'hursday'
	| [Ff] 'riday'
	| [Ss] 'aturday'
	| [Ss] 'unday'
	| [Mm] 'onday'
	| [Tt] 'uesday'
	| [Ww] 'ednesday'
	;

fragment TIMEOFDAY
	: ( DIGIT+ ':' DIGIT+ ('am' | 'pm') )
	| ('M' | 'm') 'idnight'
	| ('N' | 'n') 'oon'
	; 
	
fragment DIGIT : [0-9] ; 
	
// Ignore whitespace when it's not a part of a token.
WS    : [ \t\r\n]+ -> skip ; 
