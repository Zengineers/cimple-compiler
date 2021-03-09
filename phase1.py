#   Antoniou Christodoulos 2641 cs02641@uoi.gr
#   Tsiouri Angeliki 3354 cs03354@uoi.gr


import sys


#region Variable Assignments

# States
startState = 0
digState = 1
idkState = 2
asgnState = 3
smallerState = 4
largerState = 5
remState = 6


# Errors
Invalid_Symbol_Error_Code = -1
Not_An_Integer_Error_Code = -2
Assignment_Error_Code = -3
Comment_EOF_Error_Code = -4


# Characters
space = 0
tab = 1
newLine = 2
digit = 3
letter = 4
plus = 5
minus = 6
mul = 7
div = 8
leftCurlyBracket = 9
rightCurlyBracket = 10
leftParenthesis = 11
rightParenthesis = 12
leftSquareBracket = 13
rightSquareBracket = 14
comma = 15
semicolon = 16
colon = 17
equals = 18
lesser = 19
greater = 20
hashtag = 21
EOF = 22
dot = 23
other = 24


# Token Types - KEYWORDS
programToken = 25
declareToken = 26
ifToken = 27
elseToken = 28
whileToken = 29
switchcaseToken = 30
forcaseToken = 31
incaseToken = 32
caseToken = 33
defaultToken = 34
notToken = 35
andToken = 36
orToken = 37
functionToken = 38
procedureToken = 39
callToken = 40
returnToken = 41
inToken = 42
inoutToken = 43
inputToken = 44
printToken = 45


# Token Types
identifierToken = 46
numberToken = 47
plusToken = 48
minusToken = 49
mulToken = 50
divToken = 51
leftCurlyBracketToken = 52
rightCurlyBracketToken = 53
leftParenthesisToken = 54
rightParenthesisToken = 55
leftSquareBracketToken = 56
rightSquareBracketToken = 57
commaToken = 58
semicolonToken = 59
assignmentToken = 60
greaterToken = 61
greaterOrEqualToken = 62
lesserToken = 63
lesserOrEqualToken = 64
equalToken = 65
notEqualToken = 66
EOFToken = 67
dotToken = 68
hashtagToken = 69

#endregion


#region Tables

lexTable = [ 
                                  
    # start state
    [startState, startState, startState, digState, idkState, plusToken, minusToken, mulToken, divToken,
    leftCurlyBracketToken, rightCurlyBracketToken, leftParenthesisToken, rightParenthesisToken,
    leftSquareBracketToken, rightSquareBracketToken, commaToken, semicolonToken, asgnState,
    equalToken, smallerState, largerState, remState, EOFToken, dotToken, Invalid_Symbol_Error_Code],

    # dig state
    [numberToken, numberToken, numberToken, digState, Not_An_Integer_Error_Code, numberToken,
    numberToken, numberToken, numberToken, numberToken, numberToken, numberToken, numberToken,
    numberToken, numberToken, numberToken, numberToken, numberToken, numberToken, numberToken,
    numberToken, numberToken, numberToken, numberToken, Invalid_Symbol_Error_Code],

    # idk state
    [identifierToken , identifierToken , identifierToken , idkState , idkState , identifierToken , identifierToken , identifierToken , identifierToken,
    identifierToken , identifierToken ,identifierToken , identifierToken , identifierToken , identifierToken , identifierToken , identifierToken , identifierToken,
    identifierToken , identifierToken , identifierToken , identifierToken , identifierToken , identifierToken , identifierToken],

    # asgn state
    [Assignment_Error_Code , Assignment_Error_Code , Assignment_Error_Code , Assignment_Error_Code , Assignment_Error_Code , Assignment_Error_Code,
    Assignment_Error_Code , Assignment_Error_Code , Assignment_Error_Code , Assignment_Error_Code , Assignment_Error_Code , Assignment_Error_Code,
    Assignment_Error_Code , Assignment_Error_Code , Assignment_Error_Code , Assignment_Error_Code , Assignment_Error_Code , Assignment_Error_Code,
    assignmentToken , Assignment_Error_Code , Assignment_Error_Code , Assignment_Error_Code,Assignment_Error_Code , Assignment_Error_Code , Invalid_Symbol_Error_Code],

    # smaller state
     [lesserToken , lesserToken , lesserToken , lesserToken , lesserToken , lesserToken,
     lesserToken , lesserToken , lesserToken , lesserToken , lesserToken , lesserToken,
     lesserToken , lesserToken ,lesserToken , lesserToken , lesserToken , lesserToken,
     lesserOrEqualToken , lesserToken , notEqualToken , lesserToken , lesserToken , lesserToken , Invalid_Symbol_Error_Code],

    # larger state 
    [greaterToken, greaterToken, greaterToken, greaterToken, greaterToken, greaterToken,
    greaterToken, greaterToken, greaterToken, greaterToken, greaterToken, greaterToken,
    greaterToken, greaterToken, greaterToken, greaterToken, greaterToken, greaterToken,
    greaterOrEqualToken, greaterToken, greaterToken, greaterToken, greaterToken, greaterToken, Invalid_Symbol_Error_Code],

    # rem state
    [remState, remState, remState, remState, remState, remState, remState, remState, remState,
    remState, remState, remState, remState, remState, remState, remState, remState, remState,
    remState, remState, remState, startState, Comment_EOF_Error_Code, remState, remState]

]


digits = ('0', '1', '2', '3', '4', '5', '6', '7', '8','9')


letters = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
           'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
           'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
           'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z')


keywords = ('program', 'declare', 'if', 'else', 'while', 'switchcase', 'forcase', 'incase', 'case', 'default',
            'not', 'and', 'or', 'function', 'procedure', 'call', 'return', 'in', 'inout', 'input', 'print')

#endregion


# token class containing the info of a token
class Token:

    def __init__(self, tokenType, tokenString, lineNo):
        self.tokenType = tokenType
        self.tokenString = tokenString
        self.lineNo = lineNo


# lex() reads the characters of the input file and finds the next token
# returns a token class object
# in case of error the corresponding message is printed along with the line where it occured
def lex():
    
    state = startState
    tokenString = ''
    global line

    # findCharacterToken() finds and returns the token of the given character 
    def findCharacterToken():

        global line

        if character == ' ':
            token = space

        elif character == '\t':
            token = tab

        elif character == '\n':
            token = newLine
            line += 1

        elif character in digits:
            token = digit
        
        elif character in letters:
            token = letter
            
        elif character == '+':
            token = plus
            
        elif character == '-':
            token = minus

        elif character == '*':
            token = mul
        
        elif character == '/':
            token = div

        elif character == '{':
            token = leftCurlyBracket

        elif character == '}':
            token = rightCurlyBracket

        elif character == '(':
            token = leftParenthesis

        elif character == ')':
            token = rightParenthesis
        
        elif character == '[':
            token = leftSquareBracket

        elif character == ']':
            token = rightSquareBracket

        elif character == ',':
            token = comma

        elif character == ';':
            token = semicolon

        elif character == ':':
            token = colon

        elif character == '=':
            token = equals

        elif character == '<':
            token = lesser

        elif character == '>':
            token = greater
        
        elif character == '#':
            token = hashtag

        elif character == '':
            token = EOF

        elif character == '.':
            token = dot

        else:
            token = other
        
        return token

    # identifyToken() matches the tokenString with one of the keywords of cimple
    def identifyToken():

        if tokenString in keywords:

            if tokenString == keywords[0]:
                state = programToken

            elif tokenString == keywords[1]:
                state = declareToken

            elif tokenString == keywords[2]:
                state = ifToken
            
            elif tokenString == keywords[3]:
                state = elseToken

            elif tokenString == keywords[4]:
                state = whileToken

            elif tokenString == keywords[5]:
                state = switchcaseToken

            elif tokenString == keywords[6]:
                state = forcaseToken

            elif tokenString == keywords[7]:
                state = incaseToken

            elif tokenString == keywords[8]:
                state = caseToken

            elif tokenString == keywords[9]:
                state = defaultToken

            elif tokenString == keywords[10]:
                state = notToken

            elif tokenString == keywords[11]:
                state = andToken

            elif tokenString == keywords[12]:
                state = orToken

            elif tokenString == keywords[13]:
                state = functionToken
            
            elif tokenString == keywords[14]:
                state = procedureToken

            elif tokenString == keywords[15]:
                state = callToken

            elif tokenString == keywords[16]:
                state = returnToken

            elif tokenString == keywords[17]:
                state = inToken

            elif tokenString == keywords[18]:
                state = inoutToken

            elif tokenString ==  keywords[19]:
                state = inputToken

            elif tokenString == keywords[20]:
                state = printToken
        
        else:
            state = identifierToken 
        
        return state

    # errorCheck() checks for errors and prints the corresponding message along with the line found
    def errorCheck():

        if state == Invalid_Symbol_Error_Code:
            print('Invalid_Symbol_Error @ Line:', line)

        elif state == Not_An_Integer_Error_Code:
            print('Not_An_Integer_Error @ Line:', line)

        elif state == Assignment_Error_Code:
            print('Assignment_Error @ Line:', line)

        elif state == Comment_EOF_Error_Code:
            print('Comment_EOF_Error @ Line:', line)

        elif len(tokenString) > 30:
            print('Identifier_Too_Long_Error @ Line', line)
        
        elif state == numberToken and abs(int(tokenString)) > pow(2,32) - 1:
            print('Int_Out_Of_Bounds_Error @ Line', line)


    while state >=0 and state <= 6:
        
        character = inputFile.read(1)       # read next character        
        token = findCharacterToken()        # find the token it belongs to
        state = lexTable[state][token]      # move to the next state based on the lexTable using the current state and the token found

        if state != startState and state != remState:
            tokenString += character        # form the string of the token


    # if an extra character has been read
    if state == identifierToken or state == numberToken or state == lesserToken or state == greaterToken:

        if (character == '\n'):
            line -= 1
        
        position = inputFile.tell()         # find the current position in inputFile
        inputFile.seek(position-1, 0)       # move back by 1 position
        tokenString = tokenString[:-1]      # remove the last character in tokenString

    # match the token with a cimple keyword
    if state == identifierToken:
        state = identifyToken()

    # check for errors with the token
    errorCheck()

    # finally create the token object to be returned
    token = Token(state, tokenString, line)
    return token


# syn() is the main function that implements all the syntax rules of cimple
# using a nested function for each different syntax rule
def syn():


    # "program" is the starting symbol
    # program : program ID block .
    def program():

        global token
        token = lex()

        if token.tokenType == programToken:
            token = lex()

            if token.tokenType == identifierToken:
                token = lex()
                block()

                if token.tokenType == dotToken:
                    print('Syntax analysis successful.')

                else:
                    print('Dot_Not_Found_Error @ Line:', token.lineNo)

            else:
                print('Missing_Program_Name_Error @ Line:', token.lineNo)

        else:
            print('Program_Keyword_Not_Found_Error @ Line:', token.lineNo)


    # a block with declarations, subprogram and statements
    # block : declarations subprograms statements
    def block():

        global token

        declarations()
        subprograms()
        statements()


    # declaration of variables , zero or more "declare" allowed
    # declarations : ( declare varlist ; )∗
    def declarations():

        global token

        while token.tokenType == declareToken:

            token = lex()
            
            varlist()
            
            if token.tokenType == semicolonToken:
                token = lex()
                
            else:
                print('Semicolon_Not_Found_Error @ Line:', token.lineNo)


    # a list of variables following the declaration keyword
    # varlist : ID ( , ID )∗
    # | ε
    def varlist():

        global token

        if token.tokenType == identifierToken:
            token = lex()
        
            while token.tokenType == commaToken:

                token = lex()
                
                if token.tokenType == identifierToken:
                    token = lex()
                    
                else:
                    print('Variable_Not_Found_Error @ Line:', token.lineNo)


    # zero or more subprograms allowed
    # subprograms : ( subprogram )∗
    def subprograms():

        global token
        
        while token.tokenType == functionToken or token.tokenType == procedureToken:

            subprogram()


    # a subprogram is a function or a procedure,
    # followed by parameters and block
    # subprogram : function ID ( formalparlist ) block
    # | procedure ID ( formalparlist ) block
    def subprogram():

        global token

        if token.tokenType == functionToken:
            token = lex()
            
            if token.tokenType == identifierToken:
                token = lex()
                
                if token.tokenType == leftParenthesisToken:
                    token = lex()
                    formalparlist()
                    
                    if token.tokenType == rightParenthesisToken:
                        token = lex()
                        block()

                    else:
                        print('Right_Parenthesis_Not_Found_Error @ Line:', token.lineNo)

                else:
                    print('Left_Parenthesis_Not_Found_Error @ Line:', token.lineNo)
                    
            else :
                print('Missing_Function_Name_Error @ Line:', token.lineNo)
        
        elif token.tokenType == procedureToken:
            token = lex()
            
            if token.tokenType == identifierToken:
                token = lex()

                if token.tokenType == leftParenthesisToken:
                    token = lex()
                    formalparlist()

                    if token.tokenType == rightParenthesisToken:
                        token = lex()
                        block()

                    else:
                        print('Right_Parenthesis_Not_Found_Error @ Line:', token.lineNo)
                    
                else:
                    print('Left_Parenthesis_Not_Found_Error @ Line:', token.lineNo)
                    
            else :
                print('Missing_Procedure_Name_Error @ Line:', token.lineNo)
            

    # list of formal parameters
    # formalparlist : for
    def formalparlist():

        global token

        formalparitem()

        while token.tokenType == commaToken:
            formalparitem()


    # a formal parameter (" in ": by value , " inout " by reference )
    # formalparitem : in ID
    #| inout ID
    def formalparitem():

        global token

        if token.tokenType == inToken:
            token = lex()

            if token.tokenType == identifierToken:
                token =lex()

            else:
                print('Variable_Not_Found_Error @ Line:', token.lineNo)

        elif token.tokenType == inoutToken:
            token = lex()

            if token.tokenType == identifierToken:
                token = lex()

    # one or more statements
    #statements : statement ;
    # | { statement ( ; statement )∗ }
    def statements():

        global token
        
        if token.tokenType == leftCurlyBracketToken:  
            token = lex() 
            statement()
            
            while token.tokenType == semicolonToken:

                token = lex()
                statement()

            if token.tokenType == rightCurlyBracketToken:
                token = lex()
            
            else:
                print('Right_Curly_Bracket_Not_Found_Error @ Line', token.lineNo)              

        else:

            statement()

            if token.tokenType == semicolonToken:
                token = lex()

            else:
                print('Semicolon_Not_Found_Error @ Line:', token.lineNo)


    # one statement
    #statement : assignStat
    # | ifStat
    # | whileStat
    # | switchcaseStat
    # | forcaseStat
    # | incaseStat
    # | callStat
    # | returnStat
    # | inputStat
    # | printStat
    # | ε
    def statement():
        
        global token

        if token.tokenType == identifierToken:
            assignStat()

        elif token.tokenType == ifToken:
            ifStat()
        
        elif token.tokenType == whileToken:            
            whileStat()
        
        elif token.tokenType == switchcaseToken:
            switchcaseStat()
        
        elif token.tokenType == forcaseToken:
            forcaseStat()

        elif token.tokenType == incaseToken:
            incaseStat()

        elif token.tokenType == callToken:
            callStat()

        elif token.tokenType == returnToken:
            returnStat()
        
        elif token.tokenType == inputToken:
            inputStat()

        elif token.tokenType == printToken:
            printStat()


    # assignment statement
    # assignStat : ID := expression
    def assignStat():
        
        global token

        if token.tokenType == identifierToken:
            token = lex()

            if token.tokenType == assignmentToken:
                token = lex()
                expression()

            else:
                print('Assignment_Symbol_Not_Found_Error @ Line:', token.lineNo)

        else:
            print('Variable_Not_Found_Error @ Line:', token.lineNo)      


    # if statement
    # ifStat : if ( condition ) statements elsepart
    def ifStat():

        global token
        
        token = lex()

        if token.tokenType == leftParenthesisToken:
            token = lex()
            condition()

            if token.tokenType == rightParenthesisToken:
                token = lex()
                statements()
                elsepart()
            
            else:
                print('Right_Parenthesis_Not_Found_Error @ Line:', token.lineNo)

        else:
            print('Left_Parenthesis_Not_Found_Error @ Line:', token.lineNo)
            
    # boolean expression
    # condition : boolterm ( or boolterm )∗
    def condition():

        global token

        boolterm()

        while token.tokenType == orToken:
            token = lex()
            boolterm()


    def elsepart():

        global token

        if token.tokenType == elseToken:
            token = lex()
            statements()


    # term in boolean expression
    #boolterm : boolfactor ( and boolfactor )∗
    def boolterm():

        global token

        boolfactor()

        while token.tokenType == andToken:
            token = lex()
            boolfactor()


    # factor in boolean expression
    # boolfactor : not [ condition ]
    # | [ condition ]
    # | expression REL_OP expression
    def boolfactor():
        
        global token

        if token.tokenType == notToken:
            token = lex()

            if token.tokenType == leftSquareBracketToken:
                token = lex()
                condition()

                if token.tokenType == rightSquareBracketToken:
                    token = lex()
                
                else:
                    print('Right_Square_Bracket_Not_Found_Error @ Line:', token.lineNo)

            else:
                print('Left_Square_Bracket_Not_Found_Error @ Line:', token.lineNo)

        elif token.tokenType == leftSquareBracketToken:
            token = lex()
            condition()

            if token.tokenType == rightSquareBracketToken:
                token = lex()
                
            else:
                print('Right_Square_Bracket_Not_Found_Error @ Line:', token.lineNo)

        else:
            expression()
            REL_OP()
            expression()


    # while statement
    # whileStat : while ( condition ) statements
    def whileStat():

        global token

        token = lex()

        if token.tokenType == leftParenthesisToken:
            token = lex()
            condition()

            if token.tokenType == rightParenthesisToken:
                token = lex()
                statements()

            else:
                print('Left_Parenthesis_Not_Found_Error @ Line:', token.lineNo)
                
        else:
            print('Right_Parenthesis_Not_Found_Error @ Line:', token.lineNo)


    # switch statement
    # switchcaseStat: switchcase
    # ( case ( condition ) statements )∗
    # default statements
    def switchcaseStat():

        global token

        token = lex()
        
        while token.tokenType == caseToken:

            token = lex()

            if token.tokenType == leftParenthesisToken:
                token = lex()
                condition()

                if token.tokenType == rightParenthesisToken:
                    token = lex()
                    statements()

                else:
                    print('Right_Parenthesis_Not_Found_Error @ Line:', token.lineNo)

            else:
                print('Left_Parenthesis_Not_Found_Error @ Line:', token.lineNo)
                
        if token.tokenType == defaultToken:
            token = lex()
            statements()

        else:
            print('Forcase_Default_Missing_Error @ Line:', token.lineNo)


    # forcase statement
    # forcaseStat : forcase
    # ( case ( condition ) statements )∗
    # default statements
    def forcaseStat():

        global token

        token = lex()

        while token.tokenType == caseToken:

            token = lex()

            if token.tokenType == leftParenthesisToken:
                token = lex()
                condition()

                if token.tokenType == rightParenthesisToken:
                    token = lex()
                    statements()

                else:
                    print('Right_Parenthesis_Not_Found_Error @ Line:', token.lineNo)
                
            else:
                print('Left_Parenthesis_Not_Found_Error @ Line:', token.lineNo)
                
        if token.tokenType == defaultToken:
            token = lex()
            statements()

        else:
            print('Forcase_Default_Missing_Error @ Line:', token.lineNo) 


    # incase statement
    # incaseStat : incase
    # ( case ( condition ) statements )∗
    def incaseStat():

        global token
        
        token = lex()

        while token.tokenType == caseToken:
            token = lex()

            if token.tokenType == leftParenthesisToken:
                token = lex()
                condition()

                if token.tokenType == rightParenthesisToken:
                    token= lex()
                    statements()
                
                else:
                    print('Right_Parenthesis_Not_Found_Error @ Line:', token.lineNo)

            else:
                print('Left_Parenthesis_Not_Found_Error @ Line:', token.lineNo)
                

    # return statement
    # returnStat : return( expression )
    def returnStat():

        global token

        token = lex()

        if token.tokenType == leftParenthesisToken:
            token = lex()
            expression()

            if token.tokenType == rightParenthesisToken:
                token = lex()

            else:
                print('Right_Parenthesis_Not_Found_Error @ Line:', token.lineNo)
        
        else:
            print('Left_Parenthesis_Not_Found_Error @ Line:', token.lineNo)
            

    # call statement
    # callStat : call ID( actualparlist )
    def callStat():

        global token

        token = lex()
        
        if token.tokenType == identifierToken:
            token = lex()
            
            if token.tokenType == leftParenthesisToken:
                token = lex()
                actualparlist()

                if token.tokenType == rightParenthesisToken:
                    token = lex()
                
                else:
                    print('Right_Parenthesis_Not_Found_Error @ Line:', token.lineNo)
           
            else:
                print('Left_Parenthesis_Not_Found_Error @ Line:', token.lineNo)
                
        else:
            print('Missing_Call_Identifier_Error @ Line:', token.lineNo)


    # print statement
    # printStat : print( expression ) 
    def printStat():

        global token

        token = lex()
        
        if token.tokenType == leftParenthesisToken:
            token = lex()
            expression()

            if token.tokenType == rightParenthesisToken:
                token = lex()

            else:
                print('Right_Parenthesis_Not_Found_Error @ Line:', token.lineNo)
        
        else:
            print('Left_Parenthesis_Not_Found_Error @ Line:', token.lineNo)
            
    
    # input statement
    # inputStat : input( ID )
    def inputStat():

        global token

        token = lex()

        if token.tokenType == leftParenthesisToken:
            token = lex()

            if token.tokenType == identifierToken:
                token = lex()

                if token.tokenType == rightParenthesisToken:
                    token = lex()
                
                else:
                    print('Right_Parenthesis_Not_Found_Error @ Line:', token.lineNo)
            
            else:
                print('Input_Identifier_Not_Found_Error @ Line:', token.lineNo)

        else:
            print('Left_Parenthesis_Not_Found_Error @ Line:', token.lineNo)
            

    # list of actual parameters
    #ctualparlist : actualparitem ( , actualparitem )∗
    # | ε
    def actualparlist():

        global token

        actualparitem()

        while token.tokenType == commaToken:
            token = lex()
            actualparitem()


    # an actual parameter (" in ": by value , " inout " by reference )
    # actualparitem : in expression
    # | inout ID
    def actualparitem():

        global token

        if token.tokenType == inToken:
            token = lex()
            expression()
            
        elif token.tokenType == inoutToken:
            token = lex()
            
            if token.tokenType == identifierToken:
                token = lex()

            else:
                print('Variable_Name_Not_Found_Error @ Line:', token.lineNo)


    # boolean expression
    # condition : boolterm ( or boolterm )
    def condition():

        global token

        boolterm()

        while token.tokenType == orToken:
            
            token = lex()
            boolterm()


    # arithmetic expression
    # expression : optionalSign term ( ADD_OP term )∗
    def expression():

        global token

        optionalSign()
        term()

        while token.tokenType == plusToken or token.tokenType == minusToken:
            ADD_OP()
            term()

    # term in arithmetic expression
    # term : factor ( MUL_OP factor )∗ 
    def term():

        global token

        factor()

        while token.tokenType == mulToken or token.tokenType == divToken:

            #token = lex()
            MUL_OP()
            factor()


    # MUL_OP : * | /
    def MUL_OP():

        global token
        
        if token.tokenType == mulToken:
            token = lex()

        elif token.tokenType == divToken:
            token = lex()


    # factor in arithmetic expression
    # factor : INTEGER
    # | ( expression )
    # | ID idtail
    def factor():

        global token

        if token.tokenType == numberToken:
            token = lex()

        elif token.tokenType == leftParenthesisToken:
            token = lex()
            expression()

            if token.tokenType == rightParenthesisToken:
                token = lex()
            
            else:
                print('Right_Parenthesis_Not_Found_Error @ Line:', token.lineNo)

        elif token.tokenType == identifierToken:
            token = lex()
            idtail()

        else:
            print ('Missing_Expression_Error @ Line:', token.lineNo)


    # follows a function of procedure ( parethnesis and parameters )
    # idtail : ( actualparlist )
    # | ε
    def idtail():

        global token
        
        if token.tokenType == leftParenthesisToken:
            token = lex()
            actualparlist()

            if token.tokenType == rightParenthesisToken:
                token = lex()


    # sumbols "+" and " -" ( are optional )
    # optionalSign : ADD_OP
    # | ε
    def optionalSign():

        global token

        if token.tokenType == plusToken or token.tokenType == minusToken:
            #token = lex()
            ADD_OP()


    # ADD_OP : + | -
    def ADD_OP():

        global token

        if token.tokenType == plusToken:
            token = lex()

        elif token.tokenType == minusToken:
            token = lex()


    # lexer rules : relational , arithentic operations , integers and ids
    # REL_OP : = | <= | >= | > | < | <>
    def REL_OP():

        global token

        if token.tokenType == equalToken:
            token = lex()

        elif token.tokenType == lesserOrEqualToken:
            token = lex()

        elif token.tokenType ==  greaterOrEqualToken:
            token = lex()

        elif token.tokenType == greaterToken:
            token = lex()

        elif token.tokenType == lesserToken:
            token = lex()

        elif token.tokenType == notEqualToken:
            token = lex()

        else:
            print ('Missing_Relational_Operator_Error @ Line:', token.lineNo)


    program()


inputFile = open(sys.argv[1])   # open the file given as arg

global line
line = 1                        # start the line counter

syn()                           # start syntax analysis