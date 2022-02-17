# Generated from StaffSheet.g4 by ANTLR 4.7.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys

def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\34")
        buf.write("c\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b")
        buf.write("\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\3\2\6\2\32\n\2")
        buf.write("\r\2\16\2\33\3\3\3\3\3\3\3\3\3\3\3\3\3\4\3\4\6\4&\n\4")
        buf.write("\r\4\16\4\'\3\4\3\4\3\4\7\4-\n\4\f\4\16\4\60\13\4\3\5")
        buf.write("\3\5\3\5\3\5\3\5\3\6\3\6\3\6\3\7\3\7\3\7\3\b\3\b\3\b\3")
        buf.write("\t\5\tA\n\t\3\t\3\t\3\t\5\tF\n\t\3\t\3\t\5\tJ\n\t\3\n")
        buf.write("\3\n\3\n\3\13\3\13\3\13\3\13\3\13\3\13\3\13\3\13\3\13")
        buf.write("\3\13\3\13\3\13\5\13[\n\13\3\13\3\13\3\f\3\f\3\f\3\f\3")
        buf.write("\f\2\2\r\2\4\6\b\n\f\16\20\22\24\26\2\5\3\2\n\f\3\2\23")
        buf.write("\24\3\2\25\27\2_\2\31\3\2\2\2\4\35\3\2\2\2\6#\3\2\2\2")
        buf.write("\b\61\3\2\2\2\n\66\3\2\2\2\f9\3\2\2\2\16<\3\2\2\2\20@")
        buf.write("\3\2\2\2\22K\3\2\2\2\24Z\3\2\2\2\26^\3\2\2\2\30\32\5\4")
        buf.write("\3\2\31\30\3\2\2\2\32\33\3\2\2\2\33\31\3\2\2\2\33\34\3")
        buf.write("\2\2\2\34\3\3\2\2\2\35\36\7\3\2\2\36\37\7\32\2\2\37 \7")
        buf.write("\4\2\2 !\5\6\4\2!\"\7\5\2\2\"\5\3\2\2\2#%\5\16\b\2$&\5")
        buf.write("\b\5\2%$\3\2\2\2&\'\3\2\2\2\'%\3\2\2\2\'(\3\2\2\2()\3")
        buf.write("\2\2\2)*\5\n\6\2*.\5\f\7\2+-\5\20\t\2,+\3\2\2\2-\60\3")
        buf.write("\2\2\2.,\3\2\2\2./\3\2\2\2/\7\3\2\2\2\60.\3\2\2\2\61\62")
        buf.write("\7\6\2\2\62\63\7\32\2\2\63\64\7\32\2\2\64\65\7\32\2\2")
        buf.write("\65\t\3\2\2\2\66\67\7\7\2\2\678\7\32\2\28\13\3\2\2\29")
        buf.write(":\7\b\2\2:;\7\32\2\2;\r\3\2\2\2<=\7\t\2\2=>\t\2\2\2>\17")
        buf.write("\3\2\2\2?A\7\r\2\2@?\3\2\2\2@A\3\2\2\2AB\3\2\2\2BC\7\16")
        buf.write("\2\2CE\7\32\2\2DF\5\22\n\2ED\3\2\2\2EF\3\2\2\2FG\3\2\2")
        buf.write("\2GI\5\24\13\2HJ\7\32\2\2IH\3\2\2\2IJ\3\2\2\2J\21\3\2")
        buf.write("\2\2KL\7\17\2\2LM\7\31\2\2M\23\3\2\2\2NO\7\20\2\2OP\7")
        buf.write("\31\2\2PQ\7\21\2\2QR\7\30\2\2R[\7\33\2\2ST\7\20\2\2TU")
        buf.write("\7\30\2\2UV\7\33\2\2VW\7\22\2\2W[\7\33\2\2XY\7\30\2\2")
        buf.write("Y[\7\33\2\2ZN\3\2\2\2ZS\3\2\2\2ZX\3\2\2\2[\\\3\2\2\2\\")
        buf.write("]\5\26\f\2]\25\3\2\2\2^_\t\3\2\2_`\7\31\2\2`a\t\4\2\2")
        buf.write("a\27\3\2\2\2\t\33\'.@EIZ")
        return buf.getvalue()


class StaffSheetParser ( Parser ):

    grammarFileName = "StaffSheet.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'role'", "'('", "')'", "'coordinator'", 
                     "'contact'", "'description'", "'status'", "'active'", 
                     "'disabled'", "'working'", "'protected'", "'job'", 
                     "'needs'", "'repeats'", "'times'", "'until'", "'for'", 
                     "'every'", "'hour'", "'hours'", "'minutes'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "START", "NUMBER", "QUOTE", 
                      "TIME", "WS" ]

    RULE_sheet = 0
    RULE_role = 1
    RULE_rolefragment = 2
    RULE_coordinator = 3
    RULE_contact = 4
    RULE_description = 5
    RULE_status = 6
    RULE_job = 7
    RULE_needs = 8
    RULE_timespec = 9
    RULE_duration = 10

    ruleNames =  [ "sheet", "role", "rolefragment", "coordinator", "contact", 
                   "description", "status", "job", "needs", "timespec", 
                   "duration" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    T__8=9
    T__9=10
    T__10=11
    T__11=12
    T__12=13
    T__13=14
    T__14=15
    T__15=16
    T__16=17
    T__17=18
    T__18=19
    T__19=20
    T__20=21
    START=22
    NUMBER=23
    QUOTE=24
    TIME=25
    WS=26

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None



    class SheetContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def role(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(StaffSheetParser.RoleContext)
            else:
                return self.getTypedRuleContext(StaffSheetParser.RoleContext,i)


        def getRuleIndex(self):
            return StaffSheetParser.RULE_sheet

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSheet" ):
                listener.enterSheet(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSheet" ):
                listener.exitSheet(self)




    def sheet(self):

        localctx = StaffSheetParser.SheetContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_sheet)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 23 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 22
                self.role()
                self.state = 25 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==StaffSheetParser.T__0):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class RoleContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def QUOTE(self):
            return self.getToken(StaffSheetParser.QUOTE, 0)

        def rolefragment(self):
            return self.getTypedRuleContext(StaffSheetParser.RolefragmentContext,0)


        def getRuleIndex(self):
            return StaffSheetParser.RULE_role

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRole" ):
                listener.enterRole(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRole" ):
                listener.exitRole(self)




    def role(self):

        localctx = StaffSheetParser.RoleContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_role)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 27
            self.match(StaffSheetParser.T__0)
            self.state = 28
            self.match(StaffSheetParser.QUOTE)
            self.state = 29
            self.match(StaffSheetParser.T__1)
            self.state = 30
            self.rolefragment()
            self.state = 31
            self.match(StaffSheetParser.T__2)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class RolefragmentContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def status(self):
            return self.getTypedRuleContext(StaffSheetParser.StatusContext,0)


        def contact(self):
            return self.getTypedRuleContext(StaffSheetParser.ContactContext,0)


        def description(self):
            return self.getTypedRuleContext(StaffSheetParser.DescriptionContext,0)


        def coordinator(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(StaffSheetParser.CoordinatorContext)
            else:
                return self.getTypedRuleContext(StaffSheetParser.CoordinatorContext,i)


        def job(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(StaffSheetParser.JobContext)
            else:
                return self.getTypedRuleContext(StaffSheetParser.JobContext,i)


        def getRuleIndex(self):
            return StaffSheetParser.RULE_rolefragment

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRolefragment" ):
                listener.enterRolefragment(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRolefragment" ):
                listener.exitRolefragment(self)




    def rolefragment(self):

        localctx = StaffSheetParser.RolefragmentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_rolefragment)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 33
            self.status()
            self.state = 35 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 34
                self.coordinator()
                self.state = 37 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==StaffSheetParser.T__3):
                    break

            self.state = 39
            self.contact()
            self.state = 40
            self.description()
            self.state = 44
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==StaffSheetParser.T__10 or _la==StaffSheetParser.T__11:
                self.state = 41
                self.job()
                self.state = 46
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class CoordinatorContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def QUOTE(self, i:int=None):
            if i is None:
                return self.getTokens(StaffSheetParser.QUOTE)
            else:
                return self.getToken(StaffSheetParser.QUOTE, i)

        def getRuleIndex(self):
            return StaffSheetParser.RULE_coordinator

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCoordinator" ):
                listener.enterCoordinator(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCoordinator" ):
                listener.exitCoordinator(self)




    def coordinator(self):

        localctx = StaffSheetParser.CoordinatorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_coordinator)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 47
            self.match(StaffSheetParser.T__3)
            self.state = 48
            self.match(StaffSheetParser.QUOTE)
            self.state = 49
            self.match(StaffSheetParser.QUOTE)
            self.state = 50
            self.match(StaffSheetParser.QUOTE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ContactContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def QUOTE(self):
            return self.getToken(StaffSheetParser.QUOTE, 0)

        def getRuleIndex(self):
            return StaffSheetParser.RULE_contact

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterContact" ):
                listener.enterContact(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitContact" ):
                listener.exitContact(self)




    def contact(self):

        localctx = StaffSheetParser.ContactContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_contact)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 52
            self.match(StaffSheetParser.T__4)
            self.state = 53
            self.match(StaffSheetParser.QUOTE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class DescriptionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def QUOTE(self):
            return self.getToken(StaffSheetParser.QUOTE, 0)

        def getRuleIndex(self):
            return StaffSheetParser.RULE_description

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDescription" ):
                listener.enterDescription(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDescription" ):
                listener.exitDescription(self)




    def description(self):

        localctx = StaffSheetParser.DescriptionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_description)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 55
            self.match(StaffSheetParser.T__5)
            self.state = 56
            self.match(StaffSheetParser.QUOTE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class StatusContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return StaffSheetParser.RULE_status

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStatus" ):
                listener.enterStatus(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStatus" ):
                listener.exitStatus(self)




    def status(self):

        localctx = StaffSheetParser.StatusContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_status)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 58
            self.match(StaffSheetParser.T__6)
            self.state = 59
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << StaffSheetParser.T__7) | (1 << StaffSheetParser.T__8) | (1 << StaffSheetParser.T__9))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class JobContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def QUOTE(self, i:int=None):
            if i is None:
                return self.getTokens(StaffSheetParser.QUOTE)
            else:
                return self.getToken(StaffSheetParser.QUOTE, i)

        def timespec(self):
            return self.getTypedRuleContext(StaffSheetParser.TimespecContext,0)


        def needs(self):
            return self.getTypedRuleContext(StaffSheetParser.NeedsContext,0)


        def getRuleIndex(self):
            return StaffSheetParser.RULE_job

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterJob" ):
                listener.enterJob(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitJob" ):
                listener.exitJob(self)




    def job(self):

        localctx = StaffSheetParser.JobContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_job)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 62
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==StaffSheetParser.T__10:
                self.state = 61
                self.match(StaffSheetParser.T__10)


            self.state = 64
            self.match(StaffSheetParser.T__11)
            self.state = 65
            self.match(StaffSheetParser.QUOTE)
            self.state = 67
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==StaffSheetParser.T__12:
                self.state = 66
                self.needs()


            self.state = 69
            self.timespec()
            self.state = 71
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==StaffSheetParser.QUOTE:
                self.state = 70
                self.match(StaffSheetParser.QUOTE)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class NeedsContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NUMBER(self):
            return self.getToken(StaffSheetParser.NUMBER, 0)

        def getRuleIndex(self):
            return StaffSheetParser.RULE_needs

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNeeds" ):
                listener.enterNeeds(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNeeds" ):
                listener.exitNeeds(self)




    def needs(self):

        localctx = StaffSheetParser.NeedsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_needs)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 73
            self.match(StaffSheetParser.T__12)
            self.state = 74
            self.match(StaffSheetParser.NUMBER)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class TimespecContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def duration(self):
            return self.getTypedRuleContext(StaffSheetParser.DurationContext,0)


        def NUMBER(self):
            return self.getToken(StaffSheetParser.NUMBER, 0)

        def START(self):
            return self.getToken(StaffSheetParser.START, 0)

        def TIME(self, i:int=None):
            if i is None:
                return self.getTokens(StaffSheetParser.TIME)
            else:
                return self.getToken(StaffSheetParser.TIME, i)

        def getRuleIndex(self):
            return StaffSheetParser.RULE_timespec

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTimespec" ):
                listener.enterTimespec(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTimespec" ):
                listener.exitTimespec(self)




    def timespec(self):

        localctx = StaffSheetParser.TimespecContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_timespec)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 88
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,6,self._ctx)
            if la_ == 1:
                self.state = 76
                self.match(StaffSheetParser.T__13)
                self.state = 77
                self.match(StaffSheetParser.NUMBER)
                self.state = 78
                self.match(StaffSheetParser.T__14)
                self.state = 79
                self.match(StaffSheetParser.START)
                self.state = 80
                self.match(StaffSheetParser.TIME)
                pass

            elif la_ == 2:
                self.state = 81
                self.match(StaffSheetParser.T__13)
                self.state = 82
                self.match(StaffSheetParser.START)
                self.state = 83
                self.match(StaffSheetParser.TIME)
                self.state = 84
                self.match(StaffSheetParser.T__15)
                self.state = 85
                self.match(StaffSheetParser.TIME)
                pass

            elif la_ == 3:
                self.state = 86
                self.match(StaffSheetParser.START)
                self.state = 87
                self.match(StaffSheetParser.TIME)
                pass


            self.state = 90
            self.duration()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class DurationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NUMBER(self):
            return self.getToken(StaffSheetParser.NUMBER, 0)

        def getRuleIndex(self):
            return StaffSheetParser.RULE_duration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDuration" ):
                listener.enterDuration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDuration" ):
                listener.exitDuration(self)




    def duration(self):

        localctx = StaffSheetParser.DurationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_duration)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 92
            _la = self._input.LA(1)
            if not(_la==StaffSheetParser.T__16 or _la==StaffSheetParser.T__17):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 93
            self.match(StaffSheetParser.NUMBER)
            self.state = 94
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << StaffSheetParser.T__18) | (1 << StaffSheetParser.T__19) | (1 << StaffSheetParser.T__20))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





