class LexicalResult:
    def __init__(self, token, tipo, linha):
        self.token = token
        self.tipo = tipo
        self.linha = linha
    
    def getToken(self):
        return self.token
    
    def getTipo(self):
        return self.tipo
    
    def getLinha(self):
        return self.linha