#   onoma Am username
#   onoma Am username


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
identifierToken = 50
numberToken = 100
plusToken = 150
minusToken = 200
mulToken = 250
divToken = 300
leftCurlyBracketToken = 350
rightCurlyBracketToken = 400
leftParenthesisToken = 450
rightParenthesisToken = 500
leftSquareBracketToken = 550
rightSquareBracketToken = 600
commaToken = 650
semicolonToken = 700
#colonToken = '35'
assignmentToken = 750
greaterToken = 800
greaterOrEqualToken = 850
lesserToken = 900
lesserOrEqualToken = 950
equalToken = 1000
notEqualToken = 1050
EOFToken = 2000
dotToken = 2050
hashtagToken = 2100

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
    identifierToken , identifierToken , identifierToken , identifierToken , identifierToken , identifierToken , Invalid_Symbol_Error_Code],

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


#inputFile = open(sys.argv[1])
inputFile = open("factorial.ci","r")

global line
line = 1

# lex reads the characters of the input file and finds the next token
# returns a token class object
# in case of error the corresponding message is printed along with the line where it occured
def lex():
    
    state = startState
    tokenString = ''
    global line

    while state >=0 and state <= 6:

        character = inputFile.read(1)
        #print('Character:', character)

        # TODO function for tokens
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
        

        state = lexTable[state][token]
        #print('state:', state)

        if state != startState and state != remState:
            tokenString += character


    if state == identifierToken or state == numberToken or state == lesserToken or state == greaterToken:

        if (character == '\n'):
            line -= 1

        character = inputFile.seek(inputFile.tell()-1,0)  #epistrefei to teleutaio char pou diabase sto File (px avd+)
        tokenString = tokenString[:-1]  



    #print('tokenString:', tokenString)
    

    # TODO function for identifier tokens
    if state == identifierToken:

        if tokenString in keywords:

            if tokenString == keywords[0]:
                state = programToken

            if tokenString == keywords[1]:
                state = declareToken

            if tokenString == keywords[2]:
                state = ifToken
            
            if tokenString == keywords[3]:
                state = elseToken

            if tokenString == keywords[4]:
                state = whileToken

            if tokenString == keywords[5]:
                state = switchcaseToken

            if tokenString == keywords[6]:
                state = forcaseToken

            if tokenString == keywords[7]:
                state = incaseToken

            if tokenString == keywords[8]:
                state = caseToken

            if tokenString == keywords[9]:
                state = defaultToken

            if tokenString == keywords[10]:
                state = notToken

            if tokenString == keywords[11]:
                state = andToken

            if tokenString == keywords[12]:
                state = orToken

            if tokenString == keywords[13]:
                state = functionToken
            
            if tokenString == keywords[14]:
                state = procedureToken

            if tokenString == keywords[15]:
                state = callToken

            if tokenString == keywords[16]:
                state = returnToken

            if tokenString == keywords[17]:
                state = inToken

            if tokenString == keywords[18]:
                state = inoutToken

            if tokenString ==  keywords[19]:
                state = inputToken

            if tokenString == keywords[20]:
                state = printToken

    #print(tokenString in keywords)

    #print('state:', state)


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


    token = Token(state, tokenString, line)

    return token



#newToken = lex()

#print(line)


while(True):

    token = lex()

    if (token.tokenType == EOFToken):
        break

    print(token.tokenType, token.tokenString, token.lineNo)



def syn():

    # TODO

    return 0