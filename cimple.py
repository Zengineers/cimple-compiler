#   Antoniou Christodoulos 2641 cs02641@uoi.gr
#   Tsiouri Angeliki 3354 cs03354@uoi.gr

# run command:
# python3 cimple.py <cimple file> <optional arg>
#
# <cimple file>: the cimple program file path to be compiled ending in .ci
# <optional arg>: can be one of the following
#       -lex: print lex tokens on screen
#       -ic: print intermediate code quad on screen
#       -st: print symbol table on screen
#       -asm: print final assembly code on screen
#
# by default the compiler creates 3 files:
#       .int file with the intermediate code
#       .sym file with the symbol table
#       .asm file with the final MIPS assembly code
# if the cimple program has no function or procedure an extra C file is created
# which contains the intermediate code quads as low level C code
#
# TODO expand args to allow user to specify which files are created
# TODO finish final code
# TODO switchcase

import sys
import os


#region Variable Assignments

# start the line, quad and temp variable counters
line = 1
quadCount = 1
tempCount = 0

buffer = ''     # just a buffer

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
quadsTable = []     # contains the full quads table
blockQuads = []     # contains only the quads of a specific block
tempTable = []
varTable = []



# list of scopes for the symbol table
scopes = []


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

        global quadsTable, blockQuads, quadCount

        counter = interCode.nextQuad()
        quad = Quad(counter, op, x, y, z)

        quadsTable.append(quad)     # full quads table
        blockQuads.append(quad)     # quads of a specific block
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

        # symbol table:
        # create temp variable entity and add it to the current scope 
        entity = Entity.TempVariable(temp, 'tmp', symbolTable.getOffset())
        symbolTable.addEntity(entity)

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
    def outputFile(file):

        global quadsTable, buffer

        buffer = ''
        F = open(file + '.int', 'w+')

        for i in range(len(quadsTable)):
            buffer += str(quadsTable[i].counter) + ' ' + str(quadsTable[i].operation) + ' ' + str(quadsTable[i].x) + ' ' + str(quadsTable[i].y) + ' ' + str(quadsTable[i].z) + '\n'

        # optional print
        if len(sys.argv) > 2:
            if sys.argv[2] == '-ic':
                print(buffer)
       
        F.write(buffer + '\n')
        F.close()


    # outputs the intermediate code quads as assembly-like C code - only works if the cimple program does not have any subprograms
    @staticmethod
    def outputFileC(file):
        
        global quadsTable, tempTable, varTable

        # check if the input cimple program contains a subprogram
        for i in range(1, len(quadsTable)):
            if quadsTable[i].operation == 'begin_block': print('Subprogram detected - C code will not be generated.'); return
            
        F = open(file + '.c', 'w+')

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


# entity class describing an entity of the symbols table
class Entity:

    # basic constructor
    def __init__(self, identifier, type):
        self.identifier = identifier
        self.type = type
        self.scope = -1 # uninitialized
    

    # variable entity constructor
    @classmethod
    def Variable(cls, identifier, type, offset):

        variable = cls(identifier, type)
        variable.offset = offset

        return variable


    # subprogram entity constructor
    @classmethod
    def Subprogram(cls, identifier, type):
        
        subprogram = cls(identifier, type)
        subprogram.startQuad = 0
        subprogram.arguments = []
        subprogram.framelength = 0

        return subprogram


    # parameter entity constructor
    @classmethod
    def Parameter(cls, identifier, type, parMode, offset):

        parameter = cls(identifier, type)
        parameter.parMode = parMode
        parameter.offset = offset

        return parameter


    # temp variable entity constrctor
    @classmethod
    def TempVariable(cls, identifier, type, offset):

        temp = cls(identifier, type)
        temp.offset = offset

        return temp

        
# scope class describing a scope of the symbols table
class Scope:

    def __init__(self, identifier, nestingLevel):
        self.identifier = identifier
        self. nestingLevel = nestingLevel
        self.entities = []


# argument class describing an argument of the symbols table
class Argument:

    def __init__(self, identifier, type, parMode):
        self.identifier = identifier
        self.type = type       
        self.parMode = parMode


# class containing all the functions that assist with the symbol table generation
class symbolTable:

    # adds an entity to the current scope
    @staticmethod
    def addEntity(entity):

        global scopes

        if scopes:
            scopes[-1].entities.append(entity)


    # creates and adds a new scope to the list of scopes
    @staticmethod
    def addScope(identifier):

        global scopes

        scopes.append(Scope(identifier, len(scopes)))
        

    # removes and deletes the latest scope from the scopes list
    @staticmethod
    def removeScope():

        global scopes

        if scopes: 
            del scopes[-1]
            

    # adds an argument to the respective list of the latest subprogram entity
    @staticmethod
    def addArgument(argument):

        global scopes

        if scopes:
            if scopes[-1].entities:
                scopes[-1].entities[-1].arguments.append(argument)


    # converts arguments to parameter entities for the next scope
    @staticmethod
    def addParameters():

        global scopes

        if len(scopes) > 1:
            if scopes[-2].entities:

                # for every argument of the latest entity of the previous scope
                for arg in scopes[-2].entities[-1].arguments:

                    # create a parameter entity
                    parameter = Entity.Parameter(arg.identifier, 'prm', arg.parMode, symbolTable.getOffset())

                    # and add it to the entity list of the next scope
                    symbolTable.addEntity(parameter)
        

    # calculates and returns the stack offset for an entity
    @staticmethod
    def getOffset():

        global scopes

        # stack offset starts from 12 by default
        offset = 12

        if scopes:
            if scopes[-1].entities:

                # check all the entities of the current scope
                for ent in scopes[-1].entities:
                    
                    # and increment offset by 4 for any variable, temp variable or parameter
                    if ent.type == 'var' or ent.type == 'tmp' or ent.type == 'prm': offset += 4

        return offset


    # calculates the framelength of a subprogram entity and saves it in the respective field
    @staticmethod
    def getFramelength():

        global scopes

        if len(scopes) > 1:
            if scopes[-2].entities:
                scopes[-2].entities[-1].framelength = symbolTable.getOffset()


    # finds the number of the start quad of a subprogram entity and saves it in the respective field
    @staticmethod
    def getStartQuad():

        global scopes

        if len(scopes) > 1:
            if scopes[-2].entities:

                scopes[-2].entities[-1].startQuad = interCode.nextQuad()


    # searches the symbol table for an entity based on its identifier
    @staticmethod
    def search(identifier):

        global scopes

        if scopes:

            for scope in reversed(scopes):

                for ent in scope.entities:

                    if ent.identifier == identifier:
                        ent.scope = scope
                        return ent

        print('Entity_Not_Found_In_Symbol_Table_Error\nEntity Identifier: ', identifier); handleError()


    # outputs the symbol table to a .sym file
    @staticmethod
    def outputFile():

        global scopes, buffer

        buffer = ''
        F = open(sys.argv[1] + '.sym', 'a')

        for scope in reversed(scopes):
            
            buffer += 'Scope ' + str(scope.nestingLevel) + ':\t(' + scope.identifier + ')\n'

            for ent in scope.entities:
                
                if ent.type == 'var':
                    buffer += '\tVariable entity: [' + ent.identifier +']\toffset: ' + str(ent.offset) + '\n'

                elif ent.type == 'tmp':
                    buffer += '\tTemp variable entity: [' + ent.identifier +']\toffset: ' + str(ent.offset) + '\n'

                elif ent.type == 'prm':
                    buffer += '\tParameter entity: [' + ent.identifier + ']\tparMode: ' + str(ent.parMode) + '\toffset: ' + str(ent.offset) + '\n'

                elif ent.type == 'func':
                    buffer += '\tFunction entity: [' + ent.identifier + ']\tstartQuad: ' + str(ent.startQuad) + '\tframelength: ' + str(ent.framelength) + '\n'

                    for arg in ent.arguments:
                        buffer += '\t\t^ Argument: <' + arg.identifier + '>\ttype: ' + str(arg.type) + '\tparMode: ' + str(arg.parMode) + '\n'

                elif ent.type == 'proc':
                    buffer += '\tProcedure entity: [' + ent.identifier + ']\tstartQuad: ' + str(ent.startQuad) + '\tframelength: ' + str(ent.framelength) + '\n'

                    for arg in ent.arguments:
                        buffer += '\t\t^ Argument: <' + arg.identifier + '>\ttype: ' + str(arg.type) + '\tparMode: ' + str(arg.parMode) + '\n'

        # optional print
        if len(sys.argv) > 2:
            if sys.argv[2] == '-st':
                print(buffer)

        F.write(buffer + '\n')
        F.close()
        

# class containing all the functions that assist with the final assembly code generation
class finalCode:

    @staticmethod
    def findFunctionIdentifier(counter):

        global blockQuads

        i = counter

        while i >= counter:

            if blockQuads[i].operation == 'call': return blockQuads[i].x

            i += 1

            if i > len(blockQuads): print('Missing_Function_Quad_Error'); handleError()

    # transfers the address of a non local variable to $t0
    @staticmethod
    def gnvlcode(ent):

        global scopes, buffer
        
        # parent stack
        buffer += '\tlw\t$t0, -4($sp)\n'

        # required reps
        times = scopes[-1].nestingLevel - ent.scope.nestingLevel - 1

        for i in range(0, times):
            buffer += '\tlw\t$t0, -4($t0)\n'
        
        buffer += '\taddi\t$t0, $t0, -' + str(ent.offset) + '\n'

        #print(buffer)


    # load variable to register
    @staticmethod
    def loadvr(var, reg):

        global scopes, buffer

        # var is a number scenario
        try:
            int(var)
            #print('digit: ' +var)
            buffer += '\tli\t' + reg + ', ' + var + '\n'

        except:
            #print('not digit: ' + var)
            ent = symbolTable.search(var)
            #print(ent.scope.nestingLevel < scopes[-1].nestingLevel)
            #print(ent.scope.nestingLevel, ent.type,  scopes[-1].nestingLevel)
            # var is a global variable or temp variable scenario
            if ent.scope.nestingLevel == 0 and (ent.type == 'var' or ent.type == 'tmp'):
                buffer += '\tlw\t' + reg + ', -' + str(ent.offset) + '($s0)\n'
                
            # var belongs to the current scope
            elif ent.scope.nestingLevel == scopes[-1].nestingLevel:
                
                # var is a local variable or temp variable scenario
                if ent.type == 'var' or ent.type == 'tmp':
                    buffer += '\tlw\t' + reg + ', -' + str(ent.offset) + '($sp)\n'

                # var is a parameter passed by value
                elif ent.type == 'prm' and ent.parMode == 'in':
                    buffer += '\tlw\t' + reg + ', -' + str(ent.offset) + '($sp)\n'

                # var is a parameter passed by reference
                elif ent.type == 'prm' and ent.parMode == 'inout':
                    buffer += '\tlw\t$t0, -' + str(ent.offset) + '($sp)\n\tlw\t' + reg + ', ($t0)\n'

            # var belongs to a previous scope
            elif ent.scope.nestingLevel < scopes[-1].nestingLevel:
                
                # var is a local variable or a parameter passed by value
                if ent.type == 'var' or (ent.type == 'prm' and ent.parMode == 'in'):
                    finalCode.gnvlcode(ent)
                    buffer += '\tlw\t' + reg + ', ($t0)\n'

                # var is a parameter passed by reference
                elif ent.type == 'prm' and ent.parMode == 'inout':
                    finalCode.gnvlcode(ent)
                    buffer += '\tlw\t$t0, ($t0)\n\tlw\t' + reg + ', ($t0)\n'


    # store register to variable
    @staticmethod
    def storerv(reg, var):

        global scopes, buffer

        ent = symbolTable.search(var)
        
        # var is a global variable or temp variable scenario
        if ent.scope.nestingLevel == 0 and (ent.type == 'var' or ent.type == 'tmp'):
            buffer += '\tsw\t' + reg + ', -' + str(ent.offset) + '($s0)\n'

        # var belongs to the current scope
        elif ent.scope.nestingLevel == scopes[-1].nestingLevel:

            # var is a local variable or temp variable scenario
            if ent.type == 'var' or ent.type == 'tmp':
                buffer += '\tsw\t' + reg + ', -' + str(ent.offset) + '($sp)\n'

            # var is a parameter passed by value
            elif ent.type == 'prm' and ent.parMode == 'in':
                buffer += '\tsw\t' + reg + ', -' + str(ent.offset) + '($sp)\n'

            # var is a parameter passed by reference
            elif ent.type == 'prm' and ent.parMode == 'inout':
                buffer += '\tlw\t$t0, -' + str(ent.offset) + '($sp)\n\tsw\t' + reg + ', ($t0)\n'

        # var belongs to a previous scope
        elif ent.scope.nestingLevel < scopes[-1].nestingLevel:

            # var is a local variable or a parameter passed by value
            if ent.type == 'var' or (ent.type == 'prm' and ent.parMode == 'in'):
                finalCode.gnvlcode(ent)
                buffer += '\tsw\t' + reg + ', ($t0)\n'

            # var is a parameter passed by reference
            elif ent.type == 'prm' and ent.parMode == 'inout':
                finalCode.gnvlcode(ent)
                buffer += '\tlw\t$t0, ($t0)\n\tsw\t' + reg + ', ($t0)\n'
            

    
    # TODO - par halt begin_block end_block
    @staticmethod
    def generate():

        global blockQuads, scopes, buffer

        buffer = ''
        turn = -1
        quadCounter = 0
        mainLabel = ''
        #F = open(sys.argv[1] + '.asm', 'a')

        for quad in blockQuads:

            #print(str(quad.counter) + ' ' + str(quad.operation) + ' ' + str(quad.x) + ' ' + str(quad.y) + ' ' + str(quad.z))
            quadCounter += 1

            # add a label for every quad
            buffer += 'L_' + str(quad.counter) + ':\n'
            buffer += '\t# ' + str(quad.counter) + ' ' + str(quad.operation) + ' ' + str(quad.x) + ' ' + str(quad.y) + ' ' + str(quad.z) + ' #\n'

            # assignment
            if quad.operation == ':=':
                finalCode.loadvr(quad.x, '$t1')
                finalCode.storerv('$t1', quad.z)

            # arithmetic operations
            elif quad.operation == '+' or quad.operation == '-' or quad.operation == '*' or quad.operation == '/':
                finalCode.loadvr(quad.x, '$t1')
                finalCode.loadvr(quad.y, '$t2')

                if quad.operation == '+': op = 'add'
                elif quad.operation == '-': op = 'sub'
                elif quad.operation == '*': op = 'mul'
                else: op = 'div'
                buffer += '\t' + op + '\t$t1, $t1, $t2\n'

                finalCode.storerv('$t1', quad.z)

            # conditional branches
            elif quad.operation == '<' or quad.operation == '>' or quad.operation == '<=' or \
                quad.operation == '>=' or quad.operation == '=' or quad.operation == '<>':
                    finalCode.loadvr(quad.x, '$t1')
                    finalCode.loadvr(quad.y, '$t2')

                    if quad.operation == '<': branch = 'blt'
                    elif quad.operation == '>': branch = 'bgt'
                    elif quad.operation == '<=': branch = 'ble'
                    elif quad.operation == '>=': branch = 'bge'
                    elif quad.operation == '=': branch = 'beq'
                    elif quad.operation == '<>': branch = 'bne'
                    buffer += '\t' + branch + '\t$t1, $t2, L_' + str(quad.z) + '\n'

            # jumps
            elif quad.operation == 'jump':
                buffer += '\tj\tL_' + str(quad.z) + '\n'

            # input
            elif quad.operation == 'inp':
                buffer += '\tli\t$v0, 5\n\tsyscall\n'
                finalCode.storerv('$v0', quad.x)

            # output    
            elif quad.operation == 'out':
                buffer += '\tli\t$v0, 1\n'
                finalCode.loadvr(quad.x, '$a0')
                buffer += '\tsyscall\n'

            # return value
            elif quad.operation == 'retv':
                finalCode.loadvr(quad.x, '$t1')
                buffer += '\tlw\t$t0, -8($sp)' + '\n\tsw\t$t1, ($t0)\n'

            # subprogram parameter
            elif quad.operation == 'par':
                
                # first parameter
                if turn == -1:
                    identifier = finalCode.findFunctionIdentifier(quadCounter)
                    ent = symbolTable.search(identifier)

                    buffer += '\tadd\t$fp, $sp, ' + str(ent.framelength) + '\n'
                    turn = 0

                if quad.y == 'CV':
                    finalCode.loadvr(quad.x, '$t0')
                    buffer += '\tsw\t$t0, -%d($fp)\n' % (12+4*turn)
                    turn += 1

                elif quad.y == 'RET':
                    ent = symbolTable.search(quad.x)

                    if ent.scope.nestingLevel == scopes[-1].nestingLevel:
                        
                        if ent.type == 'var' or (ent.type == 'prm' and ent.parMode == 'in'):
                            buffer += '\tadd\t$t0, $sp, -' + str(ent.offset) + '\n' 
                        
                        elif ent.type == 'prm' and ent.parMode == 'inout':
                            buffer += '\tlw\t$t0, -' + str(ent.offset) + '($sp)\n'

                        buffer += '\tsw\t$t0, -%d($fp)\n' % (12+4*turn)

                    elif ent.scope.nestingLevel < scopes[-1].nestingLevel:
                        finalCode.gnvlcode(ent)

                        if ent.type == 'prm' and ent.parMode == 'inout':
                            buffer += '\tlw\t$t0, ($t0)\n'
                        
                        buffer += '\tsw\t$t0, -%d($fp)\n' % (12+4*turn)

                    turn += 1

            # function call
            elif quad.operation == 'call':
                turn = -1   # reset turn
                ent = symbolTable.search(quad.x)

                # caller and called have same nesting level
                if ent.scope.nestingLevel == scopes[-1].nestingLevel:
                    buffer += '\tlw\t$t0, -4($sp)\n\tsw\t$t0, -4($fp)\n'

                # caller and called have different nesting level
                elif ent.scope.nestingLevel > scopes[-1].nestingLevel:
                    buffer += '\tsw\t$sp, -4($fp)\n'

                buffer += '\tadd\t$sp, $sp, ' + str(ent.framelength) + '\n' \
                    + '\tjal\tL' + str(ent.startQuad) + '\n' \
                    + '\tadd\t$sp, $sp, -' + str(ent.framelength) + '\n'

            # program halt
            elif quad.operation == 'halt':
                pass

            # begin block
            elif quad.operation == 'begin_block':
            
                # main progam block
                if scopes[-1].nestingLevel == 0:
                    #F = open(sys.argv[1] + '.asm', 'r+')
                    #F.seek(0)
                    #F.write('\tj\tL_' + str(quad.counter) + '\n\n')
                    mainLabel = '\tj\tL_' + str(quad.counter) + '\n\n'
                    #F.close()
                    buffer += '\tadd\t$sp, $sp, ' + str(symbolTable.getOffset()) + '\n'
                    buffer += '\tmove\t$s0, $sp\n'

                # subprogram block
                else:
                    buffer += '\tsw\t$ra, ($sp)\n'         

            # end block
            elif quad.operation == 'end_block':
                buffer += '\tlw\t$ra, ($sp)\n\tjr\t$ra\n'

        F = open(sys.argv[1] + '.asm', 'a')
        F.write(buffer)
        #F.close()

        '''if mainLabel != '':
            F.close()
            F = open(sys.argv[1] + '.asm', 'r+')
            F.write(mainLabel)'''

        # optional print
        if len(sys.argv) > 2:
            if sys.argv[2] == '-asm':
                print(buffer)

        blockQuads = [] # flush table contents to prepare for the next block


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
            print('Invalid_Symbol_Error @ Line:', line); handleError()

        elif state == Not_An_Integer_Error_Code:
            print('Not_An_Integer_Error @ Line:', line); handleError()

        elif state == Assignment_Error_Code:
            print('Assignment_Error @ Line:', line); handleError()

        elif state == Comment_EOF_Error_Code:
            print('Comment_EOF_Error @ Line:', line); handleError()

        elif len(tokenString) > 30:
            print('Identifier_Too_Long_Error @ Line:', line); handleError()
        
        elif state == numberToken and abs(int(tokenString)) > pow(2,32) - 1:
            print('Int_Out_Of_Bounds_Error @ Line:', line); handleError()


    while state >= 0 and state <= 6:
        
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

    # optional print
    if len(sys.argv) > 2:
        if sys.argv[2] == '-lex':
            print(token.tokenType, token.tokenString, token.lineNo)

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
                    print('Dot_Not_Found_Error @ Line:', token.lineNo); handleError()

            else:
                print('Missing_Program_Name_Error @ Line:', token.lineNo); handleError()

        else:
            print('Program_Keyword_Not_Found_Error @ Line:', token.lineNo); handleError()


    # a block with declarations, subprogram and statements   
    def block(identifier, isProgram):

        # block : declarations subprograms statements

        global token

        # create and add new scope
        symbolTable.addScope(identifier)

        # in case of subprogram add parameter entities to scope
        if not isProgram: symbolTable.addParameters()

        declarations()
        subprograms()

        # in case of subprogram save start quad
        if not isProgram: symbolTable.getStartQuad()

        # create begin_block quad
        interCode.genQuad('begin_block', identifier, '_', '_')      

        statements()

        # in case of program create halt quad
        if isProgram: interCode.genQuad('halt', '_', '_', '_')

        # in case of subprogram save framelength
        if not isProgram: symbolTable.getFramelength()

        # create end_block quad
        interCode.genQuad('end_block', identifier, '_', '_')    
        
        finalCode.generate()    # generate final code for each block

        symbolTable.outputFile()         # write symbol table output
        symbolTable.removeScope()       # finally remove and delete the scope


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
                print('Semicolon_Not_Found_Error @ Line:', token.lineNo); handleError()


    # a list of variables following the declaration keyword
    def varlist():

        # varlist : ID ( , ID )∗
        # | ε

        global token, varTable

        if token.tokenType == identifierToken:
            varTable.append(token.tokenString)      # store variable for later use in outputFileC()

            # symbol table:
            # create variable entity and add it to the current scope 
            entity = Entity.Variable(token.tokenString, 'var', symbolTable.getOffset())
            symbolTable.addEntity(entity)
            
            token = lex()

            while token.tokenType == commaToken:

                token = lex()
                
                if token.tokenType == identifierToken:
                    varTable.append(token.tokenString)      # store variables for later use in outputFileC()

                    # symbol table:
                    # create variable entity and add it to the current scope 
                    entity = Entity.Variable(token.tokenString, 'var', symbolTable.getOffset())
                    symbolTable.addEntity(entity)

                    token = lex()
                    
                else:
                    print('Variable_Not_Found_Error @ Line:', token.lineNo); handleError()


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

                # symbol table:
                # create subprogram entity and add it to the current scope 
                entity = Entity.Subprogram(functionIdentifier, 'func')
                symbolTable.addEntity(entity)

                token = lex()
                
                if token.tokenType == leftParenthesisToken:
                    token = lex()
                    formalparlist()
                    
                    if token.tokenType == rightParenthesisToken:
                        token = lex()
                        block(functionIdentifier, False)

                    else:
                        print('Right_Parenthesis_Not_Found_Error @ Line:', token.lineNo); handleError()

                else:
                    print('Left_Parenthesis_Not_Found_Error @ Line:', token.lineNo); handleError()
                    
            else :
                print('Missing_Function_Name_Error @ Line:', token.lineNo); handleError()
        
        elif token.tokenType == procedureToken:
            token = lex()
            
            if token.tokenType == identifierToken:
                procedureIdentifier = token.tokenString

                # symbol table:
                # create subprogram entity and add it to the current scope 
                entity = Entity.Subprogram(procedureIdentifier, 'proc')
                symbolTable.addEntity(entity)

                token = lex()

                if token.tokenType == leftParenthesisToken:
                    token = lex()
                    formalparlist()

                    if token.tokenType == rightParenthesisToken:
                        token = lex()
                        block(procedureIdentifier, False)

                    else:
                        print('Right_Parenthesis_Not_Found_Error @ Line:', token.lineNo); handleError()
                    
                else:
                    print('Left_Parenthesis_Not_Found_Error @ Line:', token.lineNo); handleError()
                    
            else :
                print('Missing_Procedure_Name_Error @ Line:', token.lineNo); handleError()
            

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
                # symbol table:
                # create argument and add it to the subprogram entity
                argument = Argument(token.tokenString, 'arg', 'in')
                symbolTable.addArgument(argument)

                token =lex()

            else:
                print('Variable_Not_Found_Error @ Line:', token.lineNo); handleError()

        elif token.tokenType == inoutToken:
            token = lex()

            if token.tokenType == identifierToken:
                # symbol table:
                # create argument and add it to the subprogram entity
                argument = Argument(token.tokenString, 'arg', 'inout')
                symbolTable.addArgument(argument)

                token = lex()

            else:
                print('Variable_Not_Found_Error @ Line:', token.lineNo); handleError()


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
                print('Semicolon_Not_Found_Error @ Line:', token.lineNo); handleError()


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
                print('Assignment_Symbol_Not_Found_Error @ Line:', token.lineNo); handleError()

        else:
            print('Variable_Not_Found_Error @ Line:', token.lineNo); handleError()      


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
                print('Right_Parenthesis_Not_Found_Error @ Line:', token.lineNo); handleError()

        else:
            print('Left_Parenthesis_Not_Found_Error @ Line:', token.lineNo); handleError()


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
                    print('Right_Square_Bracket_Not_Found_Error @ Line:', token.lineNo); handleError()

            else:
                print('Left_Square_Bracket_Not_Found_Error @ Line:', token.lineNo); handleError()

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
                print('Right_Square_Bracket_Not_Found_Error @ Line:', token.lineNo); handleError()

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
                print('Left_Parenthesis_Not_Found_Error @ Line:', token.lineNo); handleError()
                
        else:
            print('Right_Parenthesis_Not_Found_Error @ Line:', token.lineNo); handleError()


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
                    print('Right_Parenthesis_Not_Found_Error @ Line:', token.lineNo); handleError()

            else:
                print('Left_Parenthesis_Not_Found_Error @ Line:', token.lineNo); handleError()
                
        if token.tokenType == defaultToken:
            token = lex()
            statements()

        else:
            print('Forcase_Default_Missing_Error @ Line:', token.lineNo); handleError()


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
                    print('Right_Parenthesis_Not_Found_Error @ Line:', token.lineNo); handleError()
                
            else:
                print('Left_Parenthesis_Not_Found_Error @ Line:', token.lineNo); handleError()
                
        if token.tokenType == defaultToken:
            token = lex()
            statements()

        else:
            print('Forcase_Default_Missing_Error @ Line:', token.lineNo); handleError() 


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
                    print('Right_Parenthesis_Not_Found_Error @ Line:', token.lineNo); handleError()

            else:
                print('Left_Parenthesis_Not_Found_Error @ Line:', token.lineNo); handleError()

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
                print('Right_Parenthesis_Not_Found_Error @ Line:', token.lineNo); handleError()
        
        else:
            print('Left_Parenthesis_Not_Found_Error @ Line:', token.lineNo); handleError()
            

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
                    print('Right_Parenthesis_Not_Found_Error @ Line:', token.lineNo); handleError()
           
            else:
                print('Left_Parenthesis_Not_Found_Error @ Line:', token.lineNo); handleError()
                
        else:
            print('Missing_Call_Identifier_Error @ Line:', token.lineNo); handleError()


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
                print('Right_Parenthesis_Not_Found_Error @ Line:', token.lineNo); handleError()
        
        else:
            print('Left_Parenthesis_Not_Found_Error @ Line:', token.lineNo); handleError()
            
    
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
                    print('Right_Parenthesis_Not_Found_Error @ Line:', token.lineNo); handleError()
            
            else:
                print('Input_Identifier_Not_Found_Error @ Line:', token.lineNo); handleError()

        else:
            print('Left_Parenthesis_Not_Found_Error @ Line:', token.lineNo); handleError()
            

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
                print('Variable_Name_Not_Found_Error @ Line:', token.lineNo); handleError()


    # arithmetic expression
    def expression():

        # expression : optionalSign term ( ADD_OP term )∗
        # E -> T1 (+|- T2 {P1})* {P2}

        global token

        addOperator = optionalSign()
        T1 = term()

        # minus for negative numbers
        if addOperator == '-': 
            T1 = '-' + T1       

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
                print('Right_Parenthesis_Not_Found_Error @ Line:', token.lineNo); handleError()

        elif token.tokenType == identifierToken:
            # {P2} - transfer identifier token string to F
            F = token.tokenString
            token = lex()
            F = idtail(F)
            
        else:
            print ('Missing_Expression_Error @ Line:', token.lineNo); handleError()
        
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
            return ADD_OP()


    # ADD_OP : + | -
    def ADD_OP():

        global token

        if token.tokenType == plusToken:
            addOperator = token.tokenString
            token = lex()

        elif token.tokenType == minusToken:
            addOperator = token.tokenString
            token = lex()
            #token.tokenString = addOperator + token.tokenString

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
            print ('Missing_Relational_Operator_Error @ Line:', token.lineNo); handleError()

        return relop


    program()


# function responsible for cleaning and terminating the compiler in case of error detection
def handleError():

    if len(sys.argv) > 1:
        if os.path.exists(sys.argv[1] + '.int'):
            os.remove(sys.argv[1] + '.int')

        if os.path.exists(sys.argv[1] + '.c'):
            os.remove(sys.argv[1] + '.c')

        if os.path.exists(sys.argv[1] + '.sym'):
            os.remove(sys.argv[1] + '.sym')

        if os.path.exists(sys.argv[1] + '.asm'):
            os.remove(sys.argv[1] + '.asm')

    exit(-1)



# try to open the file given as arg
try:
    inputFile = open(sys.argv[1])
    sys.argv[1] = sys.argv[1].replace('.ci', '')    # remove .ci from filename

# invalid args scenario
except:
    print('Invalid args!\n\n' +
        'run command:\n' +
        'python3 cimple.py <cimple file> <optional arg>\n\n' +
        '<cimple file>: the cimple program file path to be compiled ending in .ci\n' +
        '<optional arg>: can be one of the following\n' +
        '\t\t-lex: print lex tokens on screen\n' +
        '\t\t-ic: print intermediate code quad on screen\n' +
        '\t\t-st: print symbol table on screen\n' +
        '\t\t-asm: print final assembly code on screen\n')
    handleError()


open(sys.argv[1] + '.sym', 'w').close()     # clear symbol table output file if it already exists
open(sys.argv[1] + '.asm', 'w').close()     # clear assembly output file if it already exists

syn()                           # start syntax analysis

interCode.outputFile(sys.argv[1])  # output intermediate code quads
interCode.outputFileC(sys.argv[1]) # convert and output intermediate code quads as C code 

