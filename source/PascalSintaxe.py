from source.LexicalResult import LexicalResult
from source.ScopeStack import ScopeStack
import inspect;

TOKEN = 0
SYMBOL = 1
LINE = 2

class BailoutException(Exception):
    #Exception type that does not necessarily imply parsing error
    def __init__(self, message=None):
        super(BailoutException, self).__init__(message)

class PascalSintaxe:

    tokens = []
    counter = 0
    currentSymbol = None
    scopeStack = ScopeStack()

    def parseTokensToList(self, tokenSequence):
        for i in range(len(tokenSequence)):
            self.tokens.append(tokenSequence[i])

    def getNextToken(self):
        tokenLine = self.tokens[self.counter]
        self.counter += 1

        #Debug Order of Tokens
        print(tokenLine)
        return tokenLine

    def getCurrentFrameFunctionName(self):
        this_function_name = inspect.currentframe().f_code.co_name
        print(this_function_name)
    
    def StartSintaxeAnalyzer(self):
        print()
        self.currentSymbol = self.getNextToken()
        if (self.currentSymbol[TOKEN] == "program"):
            self.scopeStack.new_scope()
            self.program()
        else:
            raise Exception(
                "Program did not start with program keyword. Started with {} instead" \
                .format(self.currentSymbol[TOKEN])
            )
    
    def program(self):
        #Debug Function Name
        this_function_name = inspect.currentframe().f_code.co_name
        print(this_function_name)
        self.currentSymbol = self.getNextToken()
        if (self.currentSymbol[SYMBOL] == "identifier"):
            self.scopeStack.create_id(self.currentSymbol[TOKEN], "program_declaration")
        else:
            raise Exception(
            "Error parsing {} at line {}: missing program identifier" \
            .format(self.currentSymbol[TOKEN], self.currentSymbol[LINE])
            )
        self.currentSymbol = self.getNextToken()
        
        if (self.currentSymbol[TOKEN] != ";"):
            raise Exception("Missing ; at line {}".format(self.currentSymbol[LINE]))
        self.currentSymbol = self.getNextToken()
        
        self.VariableDeclarations()
        self.SubprogramDeclarations()
        self.CompoundCommand()

        if (self.currentSymbol[TOKEN] != "."):
            raise Exception("Missing . at the end of the program")
    
    def VariableDeclarations(self):
        #Debug Function Name
        this_function_name = inspect.currentframe().f_code.co_name
        print(this_function_name)
        if (self.currentSymbol[TOKEN] == "var"):
            self.currentSymbol = self.getNextToken()
            self.ListOfVariableDeclarations()
    
    def ListOfVariableDeclarations(self):
        #Debug Function Name
        this_function_name = inspect.currentframe().f_code.co_name
        print(this_function_name)
        listIds = self.ListOfIds()

        if (self.currentSymbol[TOKEN] != ":"):
            raise Exception("Missing : at line {}".format(self.currentSymbol[LINE]))
        self.currentSymbol = self.getNextToken()
        
        aux_type = self.currentSymbol[TOKEN]
        self.Type()

        for i in listIds:
            self.scopeStack.create_id(i, aux_type);
        
        if(self.currentSymbol[TOKEN] != ";"):
            raise Exception("Missing ; at line {}".format(self.currentSymbol[LINE]))
        self.currentSymbol = self.getNextToken()
        
        self.ListOfVariableDeclarations_L()
    
    def ListOfVariableDeclarations_L(self):
        #Debug Function Name
        this_function_name = inspect.currentframe().f_code.co_name
        print(this_function_name)
        try:
            listIds = self.ListOfIds()
        except BailoutException:
            return

        if (self.currentSymbol[TOKEN] != ":"):
            raise Exception("Missing : at line {}".format(self.currentSymbol[LINE]))
        self.currentSymbol = self.getNextToken()
        
        aux_type = self.currentSymbol[TOKEN]
        self.Type()

        for i in listIds:
            self.scopeStack.create_id(i, aux_type);
        
        if(self.currentSymbol[TOKEN] != ";"):
            raise Exception("Missing ; at line {}".format(self.currentSymbol[LINE]))
        self.currentSymbol = self.getNextToken()
        
        self.ListOfVariableDeclarations_L()

    def ListOfIds(self):
        #Debug Function Name
        this_function_name = inspect.currentframe().f_code.co_name
        print(this_function_name)
        if (self.currentSymbol[SYMBOL] == "identifier"):
            aux = [self.currentSymbol[TOKEN]]
            self.currentSymbol = self.getNextToken()
            return aux + self.ListOfIds_L()
        else:
            raise BailoutException(
                'Expected an identifier but got {} at line {}' \
                .format(self.currentSymbol[SYMBOL], self.currentSymbol[LINE])
            )
    
    def ListOfIds_L(self):
        #Debug Function Name
        this_function_name = inspect.currentframe().f_code.co_name
        print(this_function_name)
        if (self.currentSymbol[TOKEN] != ","):
            return []

        self.currentSymbol = self.getNextToken()

        if (self.currentSymbol[SYMBOL] == "identifier"):
            aux = [self.currentSymbol[TOKEN]]
            self.currentSymbol = self.getNextToken()
            return aux + self.ListOfIds_L()

    def Type(self):
        #Debug Function Name
        this_function_name = inspect.currentframe().f_code.co_name
        print(this_function_name)
        if (self.currentSymbol[TOKEN] not in ["integer", "real", "boolean"]):
            raise Exception(
            "{} is not a valid type at line {}".format(self.currentSymbol[TOKEN], self.currentSymbol[LINE])
            )
        self.currentSymbol = self.getNextToken()

    def SubprogramDeclarations(self):
        #Debug Function Name
        this_function_name = inspect.currentframe().f_code.co_name
        print(this_function_name)
        self.SubprogramsDeclarations_L()

    def SubprogramsDeclarations_L(self):
        #Debug Function Name
        this_function_name = inspect.currentframe().f_code.co_name
        print(this_function_name)
        try:
            self.SubprogramDeclaration()
        except:
            return
        
        if(self.currentSymbol[TOKEN] != ";"):
            raise Exception("Expected ; at line {}, got {} instead.".format(self.currentSymbol[LINE], self.currentSymbol[TOKEN]))
        self.currentSymbol = self.getNextToken()
        
        self.SubprogramsDeclarations_L()
    
    def SubprogramDeclaration(self):
        #Debug Function Name
        this_function_name = inspect.currentframe().f_code.co_name
        print(this_function_name)
        if (self.currentSymbol[TOKEN] != 'procedure'):
            raise BailoutException(
                'Expected procedure at line {}, got {} instead' \
                .format(self.currentSymbol[LINE], self.currentSymbol[TOKEN])
                )
        self.currentSymbol = self.getNextToken()
        
        if (self.currentSymbol[SYMBOL] == 'identifier'):
            self.scopeStack.create_id(self.currentSymbol[TOKEN], 'proc')
            self.scopeStack.new_scope()
        else:
            raise Exception(
                'Expected procedure identifier at line {}, got {} instead' \
                .format(self.currentSymbol[LINE], self.currentSymbol[TOKEN])
                )
        self.currentSymbol = self.getNextToken()
        
        self.Arguments()

        if (self.currentSymbol[TOKEN] != ';'):
            raise Exception(
                'Expected ;, got {} at line {} instead' \
                .format(self.currentSymbol[TOKEN], self.currentSymbol[LINE])
                )
        self.currentSymbol = self.getNextToken()
        
        self.VariableDeclarations()
        self.SubprogramDeclarations()
        self.CompoundCommand()

        self.scopeStack.end_scope()
    
    def Arguments(self):
        #Debug Function Name
        this_function_name = inspect.currentframe().f_code.co_name
        print(this_function_name)
        if (self.currentSymbol[TOKEN] != "("):
            return
        self.currentSymbol = self.getNextToken()

        self.ListOfParameters()

        if (self.currentSymbol[TOKEN] != ")"):
            raise Exception(
            "Expected ) at line {}, got {} instead" \
            .format(self.currentSymbol[LINE], self.currentSymbol[TOKEN])
            )
        self.currentSymbol = self.getNextToken()
    
    def ListOfParameters(self):
        #Debug Function Name
        this_function_name = inspect.currentframe().f_code.co_name
        print(this_function_name)
        aux_ids = self.ListOfIds()

        if(self.currentSymbol != ":"):
            raise Exception("Missing : at line {}".format(self.currentSymbol[LINE]))
        self.currentSymbol = self.getNextToken()

        aux_type = self.currentSymbol[TOKEN]
        self.Type()

        for identifier in aux_ids:
            self.scopeStack.create_id(identifier, aux_type)

        self.ListOfParameters_L()
    
    def ListOfParameters_L(self):
        #Debug Function Name
        this_function_name = inspect.currentframe().f_code.co_name
        print(this_function_name)
        if (self.currentSymbol[TOKEN] != ';'):
            return []
            #raise Exception("Missing ; at line {}".format(self.currentSymbol[LINE]))
        self.currentSymbol = self.getNextToken()

        aux_ids = self.ListOfIds()

        if (self.currentSymbol[TOKEN] != ':'):
            raise Exception('Missing : at line {}'.format(self.currentSymbol[LINE]))
        self.currentSymbol = self.getNextToken()
        
        aux_type = self.currentSymbol[TOKEN]
        self.Type()

        for identifier in aux_ids:
            self.scopeStack.create_id(identifier, aux_type)

        self.ListOfParameters_L()
    
    def CompoundCommand(self):
        #Debug Function Name
        this_function_name = inspect.currentframe().f_code.co_name
        print(this_function_name)
        if (self.currentSymbol[TOKEN] != "begin"):
            raise BailoutException(
                'Expected begin at line {}, got {} instead' \
                .format(self.currentSymbol[LINE], self.currentSymbol[TOKEN])
                )
        self.scopeStack.new_scope()
        self.currentSymbol = self.getNextToken()

        self.OptionalCommands()

        self.scopeStack.end_scope()

        if (self.currentSymbol[TOKEN] != "end"):
            raise Exception(
                'Expected end at line {}, got {} instead' \
                .format(self.currentSymbol[LINE], self.currentSymbol[TOKEN])
                )
        self.currentSymbol = self.getNextToken()
    
    def OptionalCommands(self):
        #Debug Function Name
        this_function_name = inspect.currentframe().f_code.co_name
        print(this_function_name)
        try:
            self.ListOfCommands()
        except BailoutException:
            return
    
    def ListOfCommands(self):
        #Debug Function Name
        this_function_name = inspect.currentframe().f_code.co_name
        print(this_function_name)
        self.Command()
        self.ListOfCommands_L()

    def ListOfCommands_L(self):
        #Debug Function Name
        this_function_name = inspect.currentframe().f_code.co_name
        print(this_function_name)
        if (self.currentSymbol[TOKEN] != ';'):
            return
        self.currentSymbol = self.getNextToken()
        
        self.Command()
        self.ListOfCommands_L()

    def Command(self):
        #Debug Function Name
        this_function_name = inspect.currentframe().f_code.co_name
        print(this_function_name)
        try:
            self.Variable()
            if(self.currentSymbol[TOKEN] == ":="):
                self.currentSymbol = self.getNextToken()
                self.Expression()
                return
            raise BailoutException
        except BailoutException:
            pass

        try:
            self.ProcedureActivation()
            return
        except BailoutException:
            pass

        try:
            self.CompoundCommand()
            return
        except BailoutException:
            pass

        try:
            if(self.currentSymbol[TOKEN] != "if"):
                raise BailoutException
            self.currentSymbol = self.getNextToken()

            self.Expression()

            if(self.currentSymbol[TOKEN] != "then"):
                raise Exception("Missing then after if at line {}.".format(self.currentSymbol[LINE]))
            self.currentSymbol = self.getNextToken()
            
            self.Command()
            self.ElsePart()
            return
        except BailoutException:
            pass

        try:
            if(self.currentSymbol[TOKEN] != "while"):
               raise BailoutException
            self.currentSymbol = self.getNextToken()

            self.Expression()

            if(self.currentSymbol[TOKEN] != "do"):
                raise Exception("Missing do after while at line {}.".format(self.currentSymbol[LINE]))
            self.currentSymbol = self.getNextToken()

            self.Command()
            
            return
        except BailoutException:
            raise Exception("Expected a command at line {}".format(self.currentSymbol[LINE]))
    
    def ElsePart(self):
        #Debug Function Name
        this_function_name = inspect.currentframe().f_code.co_name
        print(this_function_name)
        if (self.currentSymbol[TOKEN] != "else"):
            return
        self.currentSymbol = self.getNextToken()

        self.Command()

    def Variable(self):
        #Debug Function Name
        this_function_name = inspect.currentframe().f_code.co_name
        print(this_function_name)
        if (self.currentSymbol[SYMBOL] != "identifier"):
            raise BailoutException
        self.scopeStack.search(self.currentSymbol[TOKEN])
        self.currentSymbol = self.getNextToken()

    def ProcedureActivation(self):
        #Debug Function Name
        this_function_name = inspect.currentframe().f_code.co_name
        print(this_function_name)
        if (self.currentSymbol[SYMBOL] != "identifier"):
            raise BailoutException
        self.currentSymbol = self.getNextToken()
        
        self.ProcedureActivation_L()
    
    def ProcedureActivation_L(self):
        #Debug Function Name
        this_function_name = inspect.currentframe().f_code.co_name
        print(this_function_name)
        try:
            self.ListOfExpressions()
        except BailoutException:
            return
    
    def ListOfExpressions(self):
        #Debug Function Name
        this_function_name = inspect.currentframe().f_code.co_name
        print(this_function_name)
        self.Expression()
        self.ListOfExpressions_L()

    def ListOfExpressions_L(self):
        #Debug Function Name
        this_function_name = inspect.currentframe().f_code.co_name
        print(this_function_name)
        if (self.currentSymbol[TOKEN] == ","):
            self.Expression()
            self.ListOfExpressions_L()
    
    def Expression(self):
        #Debug Function Name
        this_function_name = inspect.currentframe().f_code.co_name
        print(this_function_name)
        self.SimpleExpression()

        try:
            self.RelationalOp()
        except BailoutException:
            return
        
        self.SimpleExpression()
    
    def SimpleExpression(self):
        #Debug Function Name
        this_function_name = inspect.currentframe().f_code.co_name
        print(this_function_name)
        try:
            self.Term()
        except BailoutException:
            try:
                self.Signal()
            except BailoutException:
                raise Exception(
                    "Expected signal at line {}, got {} instead." \
                    .format(self.currentSymbol[LINE], self.currentSymbol[TOKEN])
                    )
            self.Term()
            self.SimpleExpression_L()
        self.SimpleExpression_L()
    
    def SimpleExpression_L(self):
        #Debug Function Name
        this_function_name = inspect.currentframe().f_code.co_name
        print(this_function_name)
        try:
            self.AdditiveOp()
        except BailoutException:
            return
        self.Term()
        self.SimpleExpression_L()

    def Term(self):
        #Debug Function Name
        this_function_name = inspect.currentframe().f_code.co_name
        print(this_function_name)
        self.Factor()
        self.Term_L()
    
    def Term_L(self):
        #Debug Function Name
        this_function_name = inspect.currentframe().f_code.co_name
        print(this_function_name)
        try:
            self.MultiOp()
        except BailoutException:
            return
        self.Factor()
        self.Term_L()
    
    def Factor(self):
        #Debug Function Name
        this_function_name = inspect.currentframe().f_code.co_name
        print(this_function_name)
        if (self.currentSymbol[SYMBOL] == "identifier"):
            self.currentSymbol = self.getNextToken()
            if (self.currentSymbol[TOKEN] == "("):
                self.ListOfExpressions()
                if (self.currentSymbol[TOKEN] != ")"):
                    raise Exception("Unclosed parenthesis at line {}.".format(self.currentSymbol[LINE]))
                return
            return
        
        try:
            self.TypeNum()
        except BailoutException:
            if (self.currentSymbol[TOKEN] in ["true", "false"]):
                self.currentSymbol = self.getNextToken()
                return
            if (self.currentSymbol[TOKEN] == "("):   
                self.currentSymbol = self.getNextToken()
                self.Expression()
                if (self.currentSymbol[TOKEN] != ")"):
                    raise Exception("Unclosed parenthesis at line {}.".format(self.currentSymbol[LINE]))   
                self.currentSymbol = self.getNextToken()
            else:
                if (self.currentSymbol[TOKEN] == "not"):        
                    self.currentSymbol = self.getNextToken()
                    self.Factor()
                else:
                    raise Exception(
                        "Expected factor at line {}, got {} instead." \
                        .format(self.currentSymbol[LINE], self.currentSymbol[TOKEN])
                        )
    
    def TypeNum(self):
        #Debug Function Name
        this_function_name = inspect.currentframe().f_code.co_name
        print(this_function_name)
        if (self.currentSymbol[SYMBOL] not in ["integer", "realNumber"]):
            raise BailoutException(
                "{} is not a valid type at line {}, expected a number" \
                .format(self.currentSymbol[TOKEN], self.currentSymbol[LINE])
                )
        self.currentSymbol = self.getNextToken()
    
    def Signal(self):
        #Debug Function Name
        this_function_name = inspect.currentframe().f_code.co_name
        print(this_function_name)
        if (self.currentSymbol[TOKEN] not in ['+', '-']):
            raise BailoutException
        self.currentSymbol = self.getNextToken()

    def RelationalOp(self):
        #Debug Function Name
        this_function_name = inspect.currentframe().f_code.co_name
        print(this_function_name)
        if (self.currentSymbol[TOKEN] not in ['=', '<', '>', '<=', '>=', '<>']):
            raise BailoutException
        self.currentSymbol = self.getNextToken()

    def AdditiveOp(self):
        #Debug Function Name
        this_function_name = inspect.currentframe().f_code.co_name
        print(this_function_name)
        if (self.currentSymbol[TOKEN] not in ['+', '-', 'or']):
            raise BailoutException
        self.currentSymbol = self.getNextToken()

    def MultiOp(self):
        #Debug Function Name
        this_function_name = inspect.currentframe().f_code.co_name
        print(this_function_name)
        if (self.currentSymbol[TOKEN] not in ['*', '/', 'and']):
            raise BailoutException
        self.currentSymbol = self.getNextToken()
