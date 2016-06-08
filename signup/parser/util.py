from antlr4 import InputStream, CommonTokenStream
from StaffSheetLexer import StaffSheetLexer
from StaffSheetParser import StaffSheetParser
from antlr4.error.ErrorStrategy import DefaultErrorStrategy
from antlr4.error.Errors import ParseCancellationException, InputMismatchException
from antlr4.error.ErrorListener import ErrorListener

class ReportedException(ParseCancellationException) :
    def __init__(self, s, l) :
        self.symbol = s
        self.line = l 
        self.message = "Parse error on line " + str(self.line) + "."
        if s is not None :
            self.message = self.message + " Something went wrong around \"" + self.symbol.text + "\""
        
    def __str__(self):
        return "message " + self.message
        
class ValidateErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise ReportedException(offendingSymbol, line)

class ValidationErrorStrategy(DefaultErrorStrategy):
    def recover(self, recognizer, e):        
        context = recognizer._ctx
        raise ReportedException(context.start, context.start.line)

    def recoverInline(self, recognizer):
        self.recover(recognizer, InputMismatchException(recognizer))

    def sync(self, recognizer):
        pass

def test_parse(source):
    text = InputStream(source)
    lexer = StaffSheetLexer(text)
    stream = CommonTokenStream(lexer)
    parser = StaffSheetParser(stream)
    
    strat = ValidationErrorStrategy()
    parser._errHandler = strat
    
    errs = ValidateErrorListener()
    parser.addErrorListener(errs)
    lexer.addErrorListener(errs)
    
    parser.rolefragment("testparse")

