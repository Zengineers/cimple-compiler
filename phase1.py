#   Antoniou Christodoulos 2641 cs02641@uoi.gr
#   Tsiouri Angeliki 3354 cs03354@uoi.gr


import sys
import time

#region Variable Assignments

# start the line, quad and temp variable counters
line = 1
quadCount = 1
tempCount = 0


# States
startState = 0
digState = 1
idkState = 2
asgnState = 3
smallerState = 4
largerState = 5
remState = 6


# Lex Errors
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

# tables for the intermediate code quads and temp variables and for the variables of the cimple program
quadsTable = []
tempTable = []
varTable = []


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


# quad class containing the info of a quad
class Quad:

    def __init__(self, counter, operation, x, y, z):
        self.counter = counter
        self.operation = operation
        self.x = x
        self.y = y
        self.z = z


# class containing all the functions that assist with the intermediate code generation
class interCode:

    # returns the number of the next quad
    @staticmethod
    def nextQuad():
        
        global quadCount

        #quadCount += 1

        return quadCount


    # creates the next quad
    @staticmethod
    def genQuad(op, x, y, z):

        global quadsTable, quadCount

        counter = interCode.nextQuad()
        quad = Quad(counter, op, x, y, z)

        quadsTable.append(quad)
        quadCount += 1

        return quad


    # creates and returns a new temp variable
    @staticmethod
    def newTemp():

        global tempCount
        global tempTable

        temp = 'T_'
        tempCount += 1
        temp = temp + str(tempCount)

        tempTable += [temp]

        return temp


    # creates an empty list of quads
    @staticmethod
    def emptyList():

        empty = []

        return empty


    # creates a list of quad tags
    @staticmethod
    def makeList(x):
        
        make = [x]

        return make


    # creates a list of quad tags of the merge of list1 and list2
    @staticmethod
    def merge(list1, list2):

        merge = []
        merge += list1 + list2

        return merge


    # fills the last field the quads list points to with z
    @staticmethod
    def backpatch(list, z):
        
        global quadsTable

        for i in range(len(list)):

            for j in range(len(quadsTable)):

                if list[i] == quadsTable[j].counter and quadsTable[j].z == '_':
                    quadsTable[j].z = z
                    break


    # outputs the table that contains the intermediate code quads to a .int file
    @staticmethod
    def outputFile():

        global quadsTable

        F = open('interCode.int', 'w+')

        for i in range(len(quadsTable)):
            F.write(str(quadsTable[i].counter) + ' ' + str(quadsTable[i].operation) + ' ' + str(quadsTable[i].x) + ' ' + str(quadsTable[i].y) + ' ' + str(quadsTable[i].z) + '\n')
       
    
    # outputs the intermediate code quads as assembly-like C code - only works if the cimple program does not have any subprograms
    @staticmethod
    def outputFileC():
        
        global quadsTable, tempTable, varTable

        # check if the input cimple program contains a subprogram
        for i in range(1, len(quadsTable)):
            if quadsTable[i].operation == 'begin_block': print('Subprogram detected - C code will not be generated.'); return
            
        F = open('interCode.c', 'w+')

        F.write('#include <stdio.h>\n\n\nint main()\n{\n\t')

        
        # declare temp variables
        if len(tempTable) > 0:
            F.write('int ')

            for i in range(len(tempTable)):
                F.write(tempTable[i])

                if i+1 == len(tempTable):
                    F.write(';\n\t')

                else:
                    F.write(', ')


        # declare variables
        if len(varTable) > 0:
            F.write('int ')

            for i in range(len(varTable)):
                F.write(varTable[i])

                if i+1 == len(varTable):
                    F.write(';\n\t')

                else:
                    F.write(', ')


        # convert the intermediate code quads to assembly-like C code
        for i in range(len(quadsTable)):

            if quadsTable[i].operation == 'begin_block':
                F.write('\n\tL_' + str(i+1) + ':')

            elif quadsTable[i].operation ==  ':=':
                F.write('\n\tL_' + str(i+1) + ':  ' + quadsTable[i].z + ' = ' + quadsTable[i].x + ';')

            elif quadsTable[i].operation == '+' or quadsTable[i].operation == '-' or quadsTable[i].operation == '*' or quadsTable[i].operation == '/':
                F.write('\n\tL_' + str(i+1) + ':  ' + quadsTable[i].z + ' = ' + quadsTable[i].x + ' ' + quadsTable[i].operation + ' ' + quadsTable[i].y + ';')

            elif quadsTable[i].operation == '<' or quadsTable[i].operation == '>' or quadsTable[i].operation == '<=' or quadsTable[i].operation == '>=':\
                F.write('\n\tL_' + str(i+1) + ':  if (' + str(quadsTable[i].x) + ' ' + str(quadsTable[i].operation) + ' ' + str(quadsTable[i].y) + ') goto L_' + str(quadsTable[i].z) + ';')

            elif quadsTable[i].operation == 'jump':
                F.write('\n\tL_' + str(i+1) + ':  goto L_' + str(quadsTable[i].z) + ';')

            elif quadsTable[i].operation == '=':
                F.write('\n\tL_' + str(i+1) + ':  if (' + str(quadsTable[i].x) + ' == ' + str(quadsTable[i].y) + ') goto L_' + str(quadsTable[i].z) + ';')

            elif quadsTable[i].operation == '<>':
                F.write('\n\tL_' + str(i+1) + ':  if (' + str(quadsTable[i].x) + ' != ' + str(quadsTable[i].y) + ') goto L_' + str(quadsTable[i].z) + ';')

            elif quadsTable[i].operation == 'inp':
                F.write('\n\tL_' + str(i+1) + ':  scanf("%d", &' + str(quadsTable[i].x + ');'))
                
            elif quadsTable[i].operation == 'out':
                F.write('\n\tL_' + str(i+1) + ':  printf("' + str(quadsTable[i].x) + ': %d\\n", ' + str(quadsTable[i].x + ');'))

            elif quadsTable[i].operation == 'halt':
                F.write('\n\tL_' + str(i+1) + ':  {}')

            elif quadsTable[i].operation == 'end_block':
                F.write('\n}')

            # write the quads as comments
            F.write('\t\t// (' + str(quadsTable[i].operation) + ', ' + str(quadsTable[i].x) + ', ' + str(quadsTable[i].y) + ', ' + str(quadsTable[i].z) + ')')


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
# in case of error the corresponding message is printed along with the line where it occured
def syn():


    # "program" is the starting symbol
    def program():

        # program : program ID block .

        global token
        token = lex()

        if token.tokenType == programToken:
            token = lex()

            if token.tokenType == identifierToken:
                programIdentifier = token.tokenString
                token = lex()

                block(programIdentifier, True)

                if token.tokenType == dotToken:
                    print('Syntax analysis successful.')

                else:
                    print('Dot_Not_Found_Error @ Line:', token.lineNo)

            else:
                print('Missing_Program_Name_Error @ Line:', token.lineNo)

        else:
            print('Program_Keyword_Not_Found_Error @ Line:', token.lineNo)


    # a block with declarations, subprogram and statements   
    def block(identifier, isProgram):

        # block : declarations subprograms statements

        global token

        declarations()
        subprograms()

        interCode.genQuad('begin_block', identifier, '_', '_')
        statements()
        if isProgram: interCode.genQuad('halt', '_', '_', '_')
        interCode.genQuad('end_block', identifier, '_', '_')


    # declaration of variables , zero or more "declare" allowed
    def declarations():

        # declarations : ( declare varlist ; )∗

        global token

        while token.tokenType == declareToken:

            token = lex()
            
            varlist()
            
            if token.tokenType == semicolonToken:
                token = lex()
                
            else:
                print('Semicolon_Not_Found_Error @ Line:', token.lineNo)


    # a list of variables following the declaration keyword
    def varlist():

        # varlist : ID ( , ID )∗
        # | ε

        global token, varTable

        if token.tokenType == identifierToken:
            varTable.append(token.tokenString)      # store variable for later use in outputFileC()
            token = lex()

            while token.tokenType == commaToken:

                token = lex()
                
                if token.tokenType == identifierToken:
                    varTable.append(token.tokenString)      # store variables for later use in outputFileC()
                    token = lex()
                    
                else:
                    print('Variable_Not_Found_Error @ Line:', token.lineNo)


    # zero or more subprograms allowed
    def subprograms():

        # subprograms : ( subprogram )*

        global token
        
        while token.tokenType == functionToken or token.tokenType == procedureToken:

            subprogram()


    # a subprogram is a function or a procedure
    def subprogram():

        # followed by parameters and block
        # subprogram : function ID ( formalparlist ) block
        # | procedure ID ( formalparlist ) block

        global token

        if token.tokenType == functionToken:
            token = lex()
            
            if token.tokenType == identifierToken:
                functionIdentifier = token.tokenString
                token = lex()
                
                if token.tokenType == leftParenthesisToken:
                    token = lex()
                    formalparlist()
                    
                    if token.tokenType == rightParenthesisToken:
                        token = lex()
                        block(functionIdentifier, False)

                    else:
                        print('Right_Parenthesis_Not_Found_Error @ Line:', token.lineNo)

                else:
                    print('Left_Parenthesis_Not_Found_Error @ Line:', token.lineNo)
                    
            else :
                print('Missing_Function_Name_Error @ Line:', token.lineNo)
        
        elif token.tokenType == procedureToken:
            token = lex()
            
            if token.tokenType == identifierToken:
                procedureIdentifier = token.tokenString
                token = lex()

                if token.tokenType == leftParenthesisToken:
                    token = lex()
                    formalparlist()

                    if token.tokenType == rightParenthesisToken:
                        token = lex()
                        block(procedureIdentifier, False)

                    else:
                        print('Right_Parenthesis_Not_Found_Error @ Line:', token.lineNo)
                    
                else:
                    print('Left_Parenthesis_Not_Found_Error @ Line:', token.lineNo)
                    
            else :
                print('Missing_Procedure_Name_Error @ Line:', token.lineNo)
            

    # list of formal parameters
    def formalparlist():

        # formalparlist : formalparitem ( , formalparitem )∗
        # | ε

        global token

        formalparitem()

        while token.tokenType == commaToken:

            token = lex()
            formalparitem()


    # a formal parameter (" in ": by value , " inout " by reference )
    def formalparitem():

        # formalparitem : in ID
        # | inout ID

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

            else:
                print('Variable_Not_Found_Error @ Line:', token.lineNo)


    # one or more statements
    def statements():

        #statements : statement ;
        # | { statement ( ; statement )∗ }

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
    def statement():
        
        # statement : assignStat
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
    def assignStat():
        
        # assignStat : ID := expression
        # S -> ID := E {P1}
        
        global token

        if token.tokenType == identifierToken:
            ID = token.tokenString
            token = lex()

            if token.tokenType == assignmentToken:
                token = lex()
                E = expression()
                
                # {P1} - generate a new quad for the assignment
                interCode.genQuad(':=', E, '_', ID)

            else:
                print('Assignment_Symbol_Not_Found_Error @ Line:', token.lineNo)

        else:
            print('Variable_Not_Found_Error @ Line:', token.lineNo)      


    # if statement 
    def ifStat():

        # ifStat : if ( condition ) statements elsepart
        # S -> if B then {P1} S1 {P2} TAIL {P3}
        # TAIL -> else S2 | TAIL -> ε

        global token
        
        token = lex()

        if token.tokenType == leftParenthesisToken:
            token = lex()
            B = condition()

            # {P1} - fill empty quad
            interCode.backpatch(B[0], interCode.nextQuad())

            if token.tokenType == rightParenthesisToken:
                token = lex()
                statements()

                # {P2} - fill empty quad and create a 'jump' quad to ensure that the else code doesn't get executed (if code gets executed)
                ifList = interCode.makeList(interCode.nextQuad())
                interCode.genQuad('jump', '_', '_', '_')
                interCode.backpatch(B[1], interCode.nextQuad())

                elsepart()

                # {P3} - ensure that the else code doesn't get executed (if code gets executed)
                interCode.backpatch(ifList, interCode.nextQuad())
            
            else:
                print('Right_Parenthesis_Not_Found_Error @ Line:', token.lineNo)

        else:
            print('Left_Parenthesis_Not_Found_Error @ Line:', token.lineNo)


    # boolean expression
    def condition():

        # condition : boolterm ( or boolterm )∗
        # C -> Q1 {P1} (or {P2} Q2 {P3})*

        global token

        Q1 = boolterm()

        # {P1} - transfer true and false quads from Q1
        conditionTrue = Q1[0]
        conditionFalse = Q1[1]

        while token.tokenType == orToken:

            token = lex()

            # {P2} - fill quads that can be filled within the rule
            interCode.backpatch(conditionFalse, interCode.nextQuad())

            Q2 = boolterm()

            # {P3} - merge the true quads together and transfer the false quad from Q2
            conditionTrue = interCode.merge(conditionTrue, Q2[0])
            conditionFalse = Q2[1] 

        return conditionTrue, conditionFalse


    # else statement
    def elsepart():

        # elsepart : else statements
        #| ε

        global token

        if token.tokenType == elseToken:
            token = lex()
            statements()


    # term in boolean expression
    def boolterm():

        # boolterm : boolfactor ( and boolfactor )∗
        # Q -> R1{P1} (and {P2} R2 {P3})*

        global token

        R1 = boolfactor()

        # {P1} - transfer true and false quads from R1
        booltermTrue = R1[0]
        booltermFalse = R1[1]

        while token.tokenType == andToken:
            
            token = lex()

            # {P2} - fill quads that can be filled within the rule
            interCode.backpatch(booltermTrue, interCode.nextQuad())

            R2 = boolfactor()

            # {P3} - transfer the true quad from R2 and merge the false quads together
            booltermTrue = R2[0] 
            booltermFalse = interCode.merge(booltermFalse, R2[1])

        return booltermTrue, booltermFalse


    # factor in boolean expression
    def boolfactor():
        
        # boolfactor : not [ condition ]
        # | [ condition ]
        # | expression REL_OP expression
        
        
        global token

        # R -> not ( B ) {P1}
        if token.tokenType == notToken:
            token = lex()

            if token.tokenType == leftSquareBracketToken:
                token = lex()
                B = condition()

                if token.tokenType == rightSquareBracketToken:
                    token = lex()

                    # {P1} - transfer true quads as false and false quads as true
                    boolfactorTrue = B[1]
                    boolfactorFalse = B[0]

                else:
                    print('Right_Square_Bracket_Not_Found_Error @ Line:', token.lineNo)

            else:
                print('Left_Square_Bracket_Not_Found_Error @ Line:', token.lineNo)

        # R -> ( B ) {P1}
        elif token.tokenType == leftSquareBracketToken:
            token = lex()
            B = condition()

            if token.tokenType == rightSquareBracketToken:
                token = lex()

                # {P1} - transfer true and false quads from B
                boolfactorTrue = B[0]
                boolfactorFalse = B[1]
                
            else:
                print('Right_Square_Bracket_Not_Found_Error @ Line:', token.lineNo)

        # R -> E1 relop E2 {P1}
        else:

            E1 = expression()
            relop = REL_OP()
            E2 = expression()

            # {P1} - create two empty quads for the true and false evaluation of relop respectively
            boolfactorTrue = interCode.makeList(interCode.nextQuad())
            interCode.genQuad(relop, E1, E2, '_')
            boolfactorFalse = interCode.makeList(interCode.nextQuad())
            interCode.genQuad('jump', '_', '_', '_')

        return boolfactorTrue, boolfactorFalse


    # while statement
    def whileStat():

        # whileStat : while ( condition ) statements
        # S -> while {P1} B do {P2} S1 {P3}

        global token

        token = lex()

        if token.tokenType == leftParenthesisToken:
            token = lex()

            # {P1}
            Bquad = interCode.nextQuad()

            B = condition()

            # {P2}
            interCode.backpatch(B[0], interCode.nextQuad())

            if token.tokenType == rightParenthesisToken:
                token = lex()
                statements()

                # {P3} - jump back to Bquad to evaluate the condition again
                interCode.genQuad('jump', '_', '_', Bquad)
                interCode.backpatch(B[1], interCode.nextQuad())

            else:
                print('Left_Parenthesis_Not_Found_Error @ Line:', token.lineNo)
                
        else:
            print('Right_Parenthesis_Not_Found_Error @ Line:', token.lineNo)


    # switch statement
    def switchcaseStat():

        # switchcaseStat: switchcase
        # ( case ( condition ) statements )∗
        # default statements
        # TODO
        
        global token

        token = lex()

        # {P1}
        
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
    def forcaseStat():

        # forcaseStat : forcase
        # ( case ( condition ) statements )∗
        # default statements
        # S -> forcase  {P1} (case (condition) {P2} statements {P3})*
        
        global token

        token = lex()
        
        # {P1}
        p1Quad = interCode.nextQuad()

        while token.tokenType == caseToken:

            token = lex()

            if token.tokenType == leftParenthesisToken:
                token = lex()
                C = condition()

                # {P2}
                interCode.backpatch(C[0], interCode.nextQuad())
                
                if token.tokenType == rightParenthesisToken:
                    token = lex()
                    statements()

                    # {P3}
                    interCode.genQuad('jump', '_', '_', p1Quad)
                    interCode.backpatch(C[1], interCode.nextQuad())

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
    def incaseStat():

        # incaseStat : incase
        # ( case ( condition ) statements )∗
        # S -> incase {P1} ( case ( condition ) {P2}  statements {P3} )∗ {P4}

        global token
        
        token = lex()

        # {P1}
        w = interCode.newTemp()
        p1Quad = interCode.nextQuad()
        interCode.genQuad(':=', '1', '_', w)

        while token.tokenType == caseToken:
            token = lex()

            if token.tokenType == leftParenthesisToken:
                token = lex()
                C = condition()

                # {P2}
                interCode.backpatch(C[0], interCode.nextQuad())
                interCode.genQuad(':=', '0', '_', w)


                if token.tokenType == rightParenthesisToken:
                    token= lex()
                    statements()

                    # {P3}
                    interCode.backpatch(C[1], interCode.nextQuad())

                else:
                    print('Right_Parenthesis_Not_Found_Error @ Line:', token.lineNo)

            else:
                print('Left_Parenthesis_Not_Found_Error @ Line:', token.lineNo)

        # {P4}
        interCode.genQuad('=', w, '0', p1Quad)  


    # return statement
    def returnStat():

        # returnStat : return( expression )
        # S -> return (E) {P1}
    
        global token

        token = lex()

        if token.tokenType == leftParenthesisToken:
            token = lex()
            E = expression()

            # {P1} - generate a new quad for the return statement
            interCode.genQuad('retv', E, '_', '_')

            if token.tokenType == rightParenthesisToken:
                token = lex()

            else:
                print('Right_Parenthesis_Not_Found_Error @ Line:', token.lineNo)
        
        else:
            print('Left_Parenthesis_Not_Found_Error @ Line:', token.lineNo)
            

    # call statement
    def callStat():

        # callStat : call ID( actualparlist )

        global token

        token = lex()
        
        if token.tokenType == identifierToken:
            procedureIdentifier = token.tokenString     # keep the procedure name identifier
            token = lex()
            
            if token.tokenType == leftParenthesisToken:
                token = lex()
                actualparlist()     # handle the procedure parameters first

                interCode.genQuad('call', procedureIdentifier, '_', '_')        # generate a new quad for the procedure call

                if token.tokenType == rightParenthesisToken:
                    token = lex()
                
                else:
                    print('Right_Parenthesis_Not_Found_Error @ Line:', token.lineNo)
           
            else:
                print('Left_Parenthesis_Not_Found_Error @ Line:', token.lineNo)
                
        else:
            print('Missing_Call_Identifier_Error @ Line:', token.lineNo)


    # print statement
    def printStat():

        # printStat : print( expression ) 
        # S -> print (E) {P2}

        global token

        token = lex()
        
        if token.tokenType == leftParenthesisToken:
            token = lex()
            E = expression()

            if token.tokenType == rightParenthesisToken:
                token = lex()

                # {P2} - generate a new quad for the print statement
                interCode.genQuad('out', E, '_', '_')

            else:
                print('Right_Parenthesis_Not_Found_Error @ Line:', token.lineNo)
        
        else:
            print('Left_Parenthesis_Not_Found_Error @ Line:', token.lineNo)
            
    
    # input statement
    def inputStat():

        # inputStat : input( ID )
        # S -> input (ID) {P1}

        global token

        token = lex()

        if token.tokenType == leftParenthesisToken:
            token = lex()

            if token.tokenType == identifierToken:
                ID = token.tokenString
                token = lex()

                if token.tokenType == rightParenthesisToken:
                    token = lex()

                    # {P1} - generate a new quad for the input statement
                    interCode.genQuad('inp',ID,'_','_')
                
                else:
                    print('Right_Parenthesis_Not_Found_Error @ Line:', token.lineNo)
            
            else:
                print('Input_Identifier_Not_Found_Error @ Line:', token.lineNo)

        else:
            print('Left_Parenthesis_Not_Found_Error @ Line:', token.lineNo)
            

    # list of actual parameters
    def actualparlist():

        # actualparlist : actualparitem ( , actualparitem )∗
        # | ε

        global token

        actualparitem()

        while token.tokenType == commaToken:
            token = lex()
            actualparitem()


    # an actual parameter (" in ": by value , " inout " by reference )
    def actualparitem():

        # actualparitem : in expression
        # | inout ID

        global token

        if token.tokenType == inToken:
            token = lex()
            E = expression()        # get the expression of the parameter

            interCode.genQuad('par', E, 'CV', '_')      # generate a new quad for the parameter (pass by value)
            
        elif token.tokenType == inoutToken:
            token = lex()
            
            if token.tokenType == identifierToken:
                parameterIdentifier = token.tokenString     # save the parameter identifier string
                token = lex()

                interCode.genQuad('par', parameterIdentifier, 'REF', '_')       # generate a new quad for the parameter (pass by reference)

            else:
                print('Variable_Name_Not_Found_Error @ Line:', token.lineNo)


    # arithmetic expression
    def expression():

        # expression : optionalSign term ( ADD_OP term )∗
        # E -> T1 (+|- T2 {P1})* {P2}

        global token

        optionalSign()
        T1 = term()

        while token.tokenType == plusToken or token.tokenType == minusToken:

            addOperator = ADD_OP()
            T2 = term()

            # {P1}
            w = interCode.newTemp()        # create new temp for the current expression result
            interCode.genQuad(addOperator, T1, T2, w)      # generate new quad for the current expression result
            T1 = w      # store the current expression result on T1 in case
        # {P2} - no other T2 so the final expression result is T1
        E = T1

        return E


    # term in arithmetic expression
    def term():

        # term : factor ( MUL_OP factor )∗ 
        # T -> F1 (*|/ F2 {P1})* {P2}

        global token

        F1 = factor()

        while token.tokenType == mulToken or token.tokenType == divToken:

            mulOperator = MUL_OP()
            F2 = factor()

            # {P1}
            w = interCode.newTemp()     # create new temp for the current expression result
            interCode.genQuad(mulOperator, F1, F2, w)       # generate new quad for the current expression result
            F1 = w      # store the current expression result on F1 in case there is another F2

        # {P2} - no other F2 so the final expression result is F1
        T = F1
        
        return T


    # MUL_OP : * | /
    def MUL_OP():

        global token
        
        if token.tokenType == mulToken:
            mulOperator = token.tokenString
            token = lex()

        elif token.tokenType == divToken:
            mulOperator = token.tokenString
            token = lex()

        return mulOperator


    # factor in arithmetic expression
    def factor():

        # factor : INTEGER
        # | ( expression )
        # | ID idtail
        # F -> (E) {P1}
        # F -> ID {P2}
        
        global token

        if token.tokenType == numberToken:
            F = token.tokenString
            token = lex()

        elif token.tokenType == leftParenthesisToken:
            token = lex()
            E = expression()

            if token.tokenType == rightParenthesisToken:
                # {P1} - transfer from E to F
                F = E
                token = lex()
            
            else:
                print('Right_Parenthesis_Not_Found_Error @ Line:', token.lineNo)

        elif token.tokenType == identifierToken:
            # {P2} - transfer identifier token string to F
            F = token.tokenString
            token = lex()
            F = idtail(F)
            
        else:
            print ('Missing_Expression_Error @ Line:', token.lineNo)

        return F


    # follows a function of procedure ( parethnesis and parameters )
    def idtail(functionIdentifier):

        # idtail : ( actualparlist )
        # | ε
        
        global token
        
        #functionIdentifier = token.tokenString

        if token.tokenType == leftParenthesisToken:
            token = lex()
            actualparlist()     # handle the function parameters first

            w = interCode.newTemp()     # new temp variable
            interCode.genQuad('par', w, 'RET', '_')     # generate a new quad for the function return value
            interCode.genQuad('call', functionIdentifier, '_', '_')     # generate a new quad for the function call
            #functionIdentifier = w
            
            if token.tokenType == rightParenthesisToken:
                token = lex()

            return w

        return functionIdentifier

    # sumbols "+" and " -" ( are optional )
    def optionalSign():

        # optionalSign : ADD_OP
        # | ε

        global token

        if token.tokenType == plusToken or token.tokenType == minusToken:
            #token = lex()
            ADD_OP()


    # ADD_OP : + | -
    def ADD_OP():

        global token

        if token.tokenType == plusToken:
            addOperator = token.tokenString
            token = lex()

        elif token.tokenType == minusToken:
            addOperator = token.tokenString
            token = lex()

        return addOperator


    # lexer rules : relational , arithentic operations , integers and ids
    def REL_OP():

        # REL_OP := | <= | >= | > | < | <>

        global token

        if token.tokenType == equalToken:
            relop = token.tokenString
            token = lex()

        elif token.tokenType == lesserOrEqualToken:
            relop = token.tokenString
            token = lex()

        elif token.tokenType ==  greaterOrEqualToken:
            relop = token.tokenString
            token = lex()

        elif token.tokenType == greaterToken:
            relop = token.tokenString
            token = lex()

        elif token.tokenType == lesserToken:
            relop = token.tokenString
            token = lex()

        elif token.tokenType == notEqualToken:
            relop = token.tokenString
            token = lex()

        else:
            print ('Missing_Relational_Operator_Error @ Line:', token.lineNo)

        return relop


    program()


#global quadCount, tempCount, quadsTable, tempTable, varTable, line





inputFile = open(sys.argv[1])   # open the file given as arg

syn()                           # start syntax analysis

interCode.outputFile()  # output intermediate code quads
interCode.outputFileC() # convert and output intermediate code quads as C code 