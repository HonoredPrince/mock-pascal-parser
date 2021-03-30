# -*- coding: utf-8 -*-
import sys
import re
import source.PascalAnalyzer as PascalAnalyzer
from source.LexicalResult import LexicalResult
from source.PascalSintaxe import PascalSintaxe


def argsTest():
    if len(sys.argv) < 2:
        print('ARGSERROR: Use: \'python3 main.py <input file>\' in the command line')
        quit()

    try:
        file = open(sys.argv[1], 'r')
        return file
    except:
        print("Não foi possível abrir o arquivo")
        raise

if __name__ == '__main__':
    tokens = []
    
    pascalFileContent = argsTest()

    lines = pascalFileContent.readlines()

    PascalAnalyzer.chechaParenteses(("".join(lines)))
    lines = PascalAnalyzer.removeComentarios(lines)

    #print(lines)

    for line_num, line in enumerate(lines):
        matchesForThisLine = []

        genericRegex, token_types = PascalAnalyzer.genericRegexCreator()
        
        iterator = re.finditer(genericRegex, line.lower())

        for match in iterator:
            tokenType = None

            for regexToken in token_types:
                currentMatch = re.match(regexToken[0], match.group(0))
                if currentMatch:
                    tokenType = regexToken[1]
                    break
            if tokenType == 'comment':
                continue
            if tokenType == 'raise_exception':
                raise Exception('`{}` não pode ser analisado.'.format(match.group(0)))
            tokens.append((currentMatch.group(0), tokenType, line_num + 1))

#Printa Resultados
print('##Tokens##','##Tipo##','##Linha##')
lexicalItems = []
for token in tokens:
    print('{},{},{}'.format(token[0].replace(',', '","'), token[1], token[2]))
    tokenSquence = LexicalResult(token[0], token[1], token[2])
    lexicalItems.append(tokenSquence)

pascalSintaxeController = PascalSintaxe()
pascalSintaxeController.parseTokensToList(tokens)
pascalSintaxeController.StartSintaxeAnalyzer()

# print("\n\n\n")
# for j in range(len(tokens)):
#     testClassInstance.symbolSituation()

