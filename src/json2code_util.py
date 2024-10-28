from argparse import ArgumentTypeError

C_KEYWORDS = ['auto', 'break', 'case', 'char', 'const',
              'continue', 'default', 'do', 'double', 'else',
              'enum', 'extern', 'float', 'for', 'goto',
              'if', 'int', 'long', 'register', 'return',
              'short', 'signed', 'sizeof', 'static', 'struct',
              'switch', 'typedef', 'union', 'unsigned', 'void',
              'volatile', 'while']

strlen = None
arrlen = None

# checks that the id can be used as a c variable name
# id - str
# returns nothing
def validate_id(id):
    assert id.isidentifier() and not id in C_KEYWORDS, f'{id} is an invalid identifier'

# passed to argparser to restrict inputs to positive integers
# s - str
# returns int
def positive(s):
    n = int(s)
    if n <= 0:
        raise ArgumentTypeError(f'{s} is not a positive integer')
    return n

# bool value to c-suitable code string
# v - bool
# returns str
def boolv2str(v):
    return str(1 if v else 0)

# int value to c-suitable code string
# v - int
# returns str
def intv2str(v):
    return str(v)

# float value to c-suitable code string
# v - float
# returns str
def floatv2str(v):
    return str(v)

# string value to c-suitable code string
# v - str
# returns str
def strv2str(v):
    return f'\"{v}\"'

# list value to c-suitable code string
# v - (validated) list
# cf - conversion function
# returns str
def listv2str(v, cf):
    f = cf
    # identify sublist type if list is nested
    if (type(v[0]) is list):
        f = lambda x : listv2str(x, cf)
    return '{' + f'{ ', '.join(f(x) for x in v) }' + '}'

# determines the needed "base" c type and conversion function
# t - type
# returns str, function
def base_cvsn(t):

    if t is int:
        lr = 'int', intv2str
    elif t is float:
        lr = 'double', floatv2str
    elif t is bool:
        lr = 'int', boolv2str
    elif t is str:
        lr = 'char', strv2str
    else:
        raise TypeError(f'{t} is not a supported type')
    
    return lr

# checks that lst is homogeneous under f
# lst - list
# f - function mapping elements of lst to types
# returns the type of elements of lst
def homogeneous(lst, f):
    t0 = f(lst[0])

    for x in lst[1:]:
        t = f(x)
        # ints are promoted to floats
        if t0 is int and t is float:
            t0 = float
        else:
            assert t0 is t or (t0 is float and t is int), f'{lst} is heterogeneous'
    
    return t0

# checks that a list can be converted to a c array
# lst - list
# returns type
def check_list(lst):
    # list must be nonempty
    assert lst, f'{lst} is an empty list'

    # list must be homogeneous
    t = homogeneous(lst, type)
    
    # nested lists must be homogeneous
    if t is list:
        t = homogeneous(lst, check_list)
    
    return t

# checks that a string length is in bounds (if it exists)
# n - int (string length)
# returns int
def check_strlen(n):
    if not strlen:
        return n
    assert n + 1 <= strlen, f'String of length {n} (+1 for null byte) exceeds maximum length of {strlen}'
    return strlen

# checks that an array length is in bounds (if it exists)
# n - int (array length)
# returns int
def check_arrlen(n):
    if not arrlen:
        return n
    assert n <= arrlen, f'Array of length {n} exceeds maximum length of {arrlen}'
    return arrlen

# decomposes a list into strings suitable for c-code
# lst - list
# returns str (left of =), str (right of =), str (brackets)
def list2str(lst : list):
    t = check_list(lst)
    s, cf = base_cvsn(t)

    brackets = f'[{check_arrlen(len(lst))}]' 

    x = lst
    while type(x[0]) is list:
        brackets += f'[{check_arrlen(max(len(sl) for sl in x))}]'
        x = x[0]

    if type(x[0]) is str:
        brackets += f'[{check_strlen(max(len(s) for s in x))}]'

    return s, listv2str(lst, cf), brackets
    
# decomposes a key value binding into strings suitable for c-code
# id - str
# v - any value
# returns str (left of =), str (right of =)
def binding2str(id, v):
    t = type(v)

    if t is list:
        # left, right, brackets
        l, r, b = list2str(v)
    else:
        l, cf = base_cvsn(t)
        r = cf(v)
        b = f'[{check_strlen(len(v))}]' if t is str else ''

    return f'{l} {id}{b}', r
        
