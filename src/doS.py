#!/bin/env python

# CONSTANS
NUMBER = '0123456789.'
OPERATOR = '+-*/%'

# INIT

varlist = {}
def token( type_,value_,argv_ ):
    '''
    TYPE: [ keyword ]
    note: datatype is command   
    ARGV: ( argv )
    '''
    return (type_, value_, argv_)

def assign(argv_):
    '''
    ARGV: ( varName, value )
    '''
    varlist[argv_[0]] = argv_[1]

def get(varName):
    if varName in varlist:
        return varlist[varName]
    else:
        print (f'VarError: not found var {varName}')
        return ''

def out(argv_):
    '''
    ARGV: ( content )
    '''
    try:
        if argv_[0][0] == '\"':
            print(argv_[0][1:-1])
        elif argv_[0][0] in NUMBER or argv_[0][0] in OPERATOR:
            try:
                print(eval(argv_[0]))
            except:
                print(f'MathError: operator error, line: {LINE}')
        elif argv_[0][0] == '$':
            value = get(argv_[0])
            try:
                if value[0] == '\"':
                    print(value[1:-1])
                elif value[0] in NUMBER or value[0] in OPERATOR:
                    try:
                        print(eval(value))
                    except:
                        print(f'MathError: operator error, line: {LINE}')
            except IndexError:
                pass
    except TypeError:
        pass

def getInput(question,varName):
    '''
    question: string
    '''
    value = '\"' + input(question) + '\"'
    varlist[varName] = value

def getModule(moduleName):
    newCode = open(moduleName,'r').read()
    return newCode

def LEX(code):
    '''
    SET
    '''
    global line
    code += '\n'
    codes = list(code)
    token = ''
    token_ = ''
    tokens_ = []
    stateString = 0
    string = ''
    expr = ''
    varStarted = 0
    var = ''

    stateString = 0
    # run 
    for c in codes:
        token += c
        if token == '\n' or token == '\r' or token == '.end':
            if expr != '':
                tokens_.append(str(eval(expr)))
                expr = ''
            if var != '':
                tokens_.append(var)
                varStarted = 0
                var = ''
            token = ''
        elif token == ' ': 
            if stateString == 0:
                token = ''
            elif stateString == 1:
                token = ' '
        # KEYWORD
        elif token == '=':
            if expr != '':
                tokens_.append(str(eval(expr)))
                expr = ''
            if var != '':
                tokens_.append(var)
                varStarted = 0
                var = ''
            if tokens_[-1] == 'equals':
                tokens_[-1] = 'eqeq'
            else:
                tokens_.append('equals')
            token = ''
        # output
        elif token == 'out':
            tokens_.append('out')
            token = ''
        # variable
        elif token == '$':
            varStarted = 1
            var += token
            token = ''
        elif varStarted == 1:
            var += token
            token = ''
        # input
        elif token == 'input':
            tokens_.append('input')
            token = ''

        elif token == '#import':
            tokens_.append('#import')
            token = ''

        elif token == '\t' or token == '~':
            token = ''
        elif token == 'if':
            tokens_.append('if')
            token = ''
        elif token == 'else':
            tokens_.append('else')
            token = ''
        elif token == 'endif':
            tokens_.append('endif')
            token = ''
        elif token == ':' and stateString == 0:
            if expr != '':
                tokens_.append(str(eval(expr)))
                expr = ''
            if var != '':
                tokens_.append(var)
                varStarted = 0
                var = ''
            tokens_.append('then')
            token = '' 
        # DATATYPE
        # string
        elif token == '\"' or token == ' \"':
            if stateString == 0:
                if tokens_[-1] == '#import':
                    token = ''
                stateString = 1
            elif stateString == 1:
                tokens_.append(string + '\"')
                string = ''
                stateString = 0
                token = ''
        elif stateString == 1:
            string += token
            token = ''
        # number and expr
        elif token in NUMBER:
            expr += token
            token = ''
        elif token in OPERATOR:
            expr += token
            token = ''
    return tokens_

def INIT_TOKEN(tok):
    i = 0
    tokens__ = []
    #print(tok)
    '''
    token normal
        value = tok[i+1]
        tok_ = token('keyword','out',(value,'.end'))
        tokens__.append(tok_)
        i+=1 + length of argv - 1
    '''
    while i < len(tok):
        try:
            # out 
            if tok[i] == 'out':
                value = tok[i+1]
                tok_ = token('keyword','out',(value,'.end'))
                tokens__.append(tok_)
                i+=2
            # variable 
            elif tok[i][0] == '$' and tok[i+1] == 'equals':
                varName = tok[i]
                value = tok[i+2]
                tok_ = token('keyword','var',(varName,value,'.end'))
                tokens__.append(tok_)
                i+=3
            # input
            elif tok[i] == 'input':
                varName = tok[i+2]
                question = tok[i+1]
                tok_ =token('keyword','input',(question[1:-1] + ' ',varName,'.end'))
                tokens__.append(tok_)
                i+=3

            # if 
            elif tok[i] == 'if' and tok[i+4] == 'then':
                operator = tok[i+2]
                value1 = tok[i+1]
                value2 = tok[i+3]
                skipLine = tok[i+5]
                tok_ = token('if','if',(value1,operator,value2,skipLine,'.end'))
                tokens__.append(tok_)
                i += 5
            elif tok[i] == 'else' and tok[i+1] == 'then':
                skipLine = tok[i+2]
                tok_ = token('if','else',(skipLine,'.end'))
                tokens__.append(tok_)
                i += 3
            elif tok[i] == 'endif':
                i += 1
            else:
                print(f'TokenErr: Token \'{tok[i]}\' not link more token')
                i += 1
        except IndexError:
            print(f'TokenErr: Token \'{tok[i]}\' not link more token')
            i += 1
    return tokens__

def PARSE(toks):
    i = 0
    while i < len(toks):
        if toks[i][0] == 'keyword':
            if toks[i][1] == 'out':
                out(toks[i][2])
            elif toks[i][1] == 'var':
                assign(toks[i][2])
            elif toks[i][1] == 'input':
                getInput(toks[i][2][0],toks[i][2][1])
        elif toks[i][0] == 'if':
            skipElse = 0
            if toks[i][1] == 'if':
                if toks[i][2][1] == 'eqeq':
                    lineSkip_ = 0 
                    if toks[i][2][0] == toks[i][2][2]:
                        skipElse = 1
                    else:
                        skipElse = 0
                        lineSkip_ = int(toks[i][2][3])
                        i += lineSkip_ + 1
                        lineSkip_ = 0
            elif toks[i][1] == 'else':
                lineSkip_ = 0 
                if skipElse == 1:
                    lineSkip_ = int(toks[i][2][0])
                    i += lineSkip_ + 1
                    lineSkip_ = 0
                    skipElse = 0
                elif skipElse == 0:
                    i += 1 + lineSkip_ + 1
        i += 1

from sys import argv
def run():
    try:
        fn = argv[1]
        code = open(fn,'r').read()
        tok = LEX(code)
        toks = INIT_TOKEN(tok)
        PARSE(toks)
    except FileNotFoundError:
        print(f'FileError: file {fn} not found')
    except IndexError:
        print('usage: doS <file name>')
    except IsADirectoryError:
        print(f'DirError: {fn} is directory')
run()
