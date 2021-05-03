import re

def checaParenteses(text):

    parenteses_abertos = 0

    for letter in text:
        if letter == "{":
            parenteses_abertos += 1
        elif letter == "}":
            parenteses_abertos -= 1
        elif parenteses_abertos < 0:
            raise Exception("Missing Brackets")
    if parenteses_abertos != 0:
        raise Exception("Brackets are not Closed")

def removeComentarios(lines):

    open_brackets = 0

    code_list = []
    for line in lines:
        l = ""
        for char in line:
            if char == "{":
                open_brackets += 1
            elif char == "}":
                open_brackets -= 1
            elif open_brackets == 0:
                l += char

        code_list.append(l)
    return code_list

def genericRegexCreator():
    token_types = [
        (r'program|var|integer|real|boolean|procedure|begin|end|if|then|else|while|for|do|not', 'keyWord'),

        (r':=', 'attribution'),
        (r'=|>|<|<=|>=|<>', 'comparison'),
        (r';|:|\(|\)|,', 'delimiter'),

        (r'\+|-|or', 'additive'),
        (r'\*|/|and', 'multiplicative'),

        (r'[0-9]+\.[0-9]*', 'realNumber'),
        (r'[0-9]+', 'integer'),

        (r'\.', 'delimiter'),
        
        (r'[a-z]+[a-z0-9_]*', 'identifier'),

        (r'[^ \n\r\t]+', 'raise_exception'),
    ]

    fullRegex = ''
    for r_tuple in token_types:
        fullRegex += '|({})'.format(r_tuple[0])
    fullRegex = fullRegex[1:]
    genericRegex = re.compile(fullRegex)

    return genericRegex, token_types

