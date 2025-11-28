import re

class Token:
    def __init__(self, tipo, valor=None):
        self.tipo = tipo
        self.valor = valor

    def __repr__(self):
        if self.valor:
            return f"<{self.tipo}:{self.valor}>"
        return f"<{self.tipo}>"

class AnalisadorLexico:
    def __init__(self, codigo):
        self.codigo = codigo
        self.posicao = 0
        self.tabela_tokens = [
            ('NUMERO', r'\d+(\.\d+)?'),
            ('IDENTIFICADOR', r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ('ATRIBUICAO', r'='),
            ('FUNCAO', r'funcao'),
            ('ABRE_PARENTESES', r'\('),
            ('FECHA_PARENTESES', r'\)'),
            ('VIRGULA', r','),
            ('OP_POTENCIA', r'\^'),
            ('OP_MULTIPLICACAO', r'\*'),
            ('OP_DIVISAO', r'/'),
            ('OP_SOMA', r'\+'),
            ('OP_SUBTRACAO', r'-'),
            ('FIM_DE_LINHA', r'[\n;]'),
            ('ESPACO', r'\s+'),
        ]
        self.palavras_reservadas = {
            'funcao': 'FUNCAO'
        }

    def proximo_token(self):
        while self.posicao < len(self.codigo):
            match = None
            for tipo, regex in self.tabela_tokens:
                padrao = re.compile(regex)
                m = padrao.match(self.codigo, self.posicao)
                if m:
                    match = m
                    break

            if match:
                valor = match.group(0)
                self.posicao = match.end()

                if tipo == 'ESPACO':
                    continue
                
                if tipo == 'FIM_DE_LINHA':
                    return Token(tipo)

                if tipo == 'IDENTIFICADOR':
                    tipo = self.palavras_reservadas.get(valor, 'IDENTIFICADOR')
                    return Token(tipo, valor)

                if tipo == 'NUMERO':
                    if '.' in valor:
                        return Token(tipo, float(valor))
                    return Token(tipo, int(valor))

                return Token(tipo, valor)
            
            raise Exception(f"Erro léxico: Caractere inválido na posição {self.posicao}: {self.codigo[self.posicao]}")

        return Token('FIM_DE_ARQUIVO')

    def tokenizar(self):
        tokens = []
        while True:
            token = self.proximo_token()
            tokens.append(token)
            if token.tipo == 'FIM_DE_ARQUIVO':
                break
        return tokens
