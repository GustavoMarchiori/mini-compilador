from analisador_lexico import Token

class AnalisadorSintatico:
    def __init__(self, tokens):
        self.tokens = tokens
        self.indice = 0
        self.token_atual = self.tokens[self.indice]
        self.tabela_simbolos = {}

    def avancar(self):
        self.indice += 1
        if self.indice < len(self.tokens):
            self.token_atual = self.tokens[self.indice]
        else:
            self.token_atual = Token('FIM_DE_ARQUIVO')

    def consumir(self, tipo_esperado):
        if self.token_atual.tipo == tipo_esperado:
            valor = self.token_atual.valor
            self.avancar()
            return valor
        else:
            raise Exception(f"Erro sintático: Esperado {tipo_esperado}, encontrado {self.token_atual.tipo}")

    def analisar(self):
        while self.token_atual.tipo != 'FIM_DE_ARQUIVO':
            self.instrucao()

    def instrucao(self):
        if self.token_atual.tipo == 'FUNCAO':
            self.declaracao_funcao()
        elif self.token_atual.tipo == 'IDENTIFICADOR' and self.tokens[self.indice + 1].tipo == 'ATRIBUICAO':
            self.atribuicao()
        else:
            self.expressao()
        
        if self.token_atual.tipo == 'FIM_DE_LINHA':
            self.consumir('FIM_DE_LINHA')
        elif self.token_atual.tipo != 'FIM_DE_ARQUIVO':
            raise Exception(f"Erro sintático: Esperado FIM_DE_LINHA ou FIM_DE_ARQUIVO, encontrado {self.token_atual.tipo}")

    def declaracao_funcao(self):
        self.consumir('FUNCAO')
        nome_funcao = self.consumir('IDENTIFICADOR')
        self.consumir('ABRE_PARENTESES')
        parametros = self.lista_parametros()
        self.consumir('FECHA_PARENTESES')
        self.consumir('ATRIBUICAO')
        
        expressao_corpo = self.expressao()
        
        self.tabela_simbolos[nome_funcao] = {'tipo': 'funcao', 'parametros': parametros, 'corpo': expressao_corpo}

    def lista_parametros(self):
        parametros = []
        if self.token_atual.tipo == 'IDENTIFICADOR':
            parametros.append(self.consumir('IDENTIFICADOR'))
            while self.token_atual.tipo == 'VIRGULA':
                self.consumir('VIRGULA')
                parametros.append(self.consumir('IDENTIFICADOR'))
        return parametros

    def atribuicao(self):
        nome_variavel = self.consumir('IDENTIFICADOR')
        self.consumir('ATRIBUICAO')
        
        expressao_valor = self.expressao()
        
        self.tabela_simbolos[nome_variavel] = {'tipo': 'variavel', 'valor': expressao_valor}


    def expressao(self):
        no = self.termo()
        while self.token_atual.tipo in ('OP_SOMA', 'OP_SUBTRACAO'):
            operador = self.token_atual.tipo
            self.avancar()
            direito = self.termo()
            no = {'tipo': 'operacao', 'operador': operador, 'esquerda': no, 'direita': direito}
        return no


    def termo(self):
        no = self.fator()
        while self.token_atual.tipo in ('OP_MULTIPLICACAO', 'OP_DIVISAO'):
            operador = self.token_atual.tipo
            self.avancar()
            direito = self.fator()
            no = {'tipo': 'operacao', 'operador': operador, 'esquerda': no, 'direita': direito}
        return no


    def fator(self):
        no = self.potencia()
        if self.token_atual.tipo == 'OP_POTENCIA':
            operador = self.token_atual.tipo
            self.avancar()
            direito = self.fator() 
            no = {'tipo': 'operacao', 'operador': operador, 'esquerda': no, 'direita': direito}
        return no


    def potencia(self):
        if self.token_atual.tipo == 'OP_SUBTRACAO':
            operador = 'OP_NEGACAO_UNARIA'
            self.avancar()
            no = self.primario()
            return {'tipo': 'operacao_unaria', 'operador': operador, 'operando': no}
        return self.primario()


    def primario(self):
        token = self.token_atual
        if token.tipo == 'NUMERO':
            self.consumir('NUMERO')
            return {'tipo': 'numero', 'valor': token.valor}
        
        elif token.tipo == 'IDENTIFICADOR':
            self.avancar()
            if self.token_atual.tipo == 'ABRE_PARENTESES':
                self.consumir('ABRE_PARENTESES')
                argumentos = self.lista_argumentos()
                self.consumir('FECHA_PARENTESES')
                return {'tipo': 'chamada_funcao', 'nome': token.valor, 'argumentos': argumentos}
            else:
                return {'tipo': 'identificador', 'nome': token.valor}

        elif token.tipo == 'ABRE_PARENTESES':
            self.consumir('ABRE_PARENTESES')
            no = self.expressao()
            self.consumir('FECHA_PARENTESES')
            return no
        
        else:
            raise Exception(f"Erro sintático: Esperado NUMERO, IDENTIFICADOR ou '(', encontrado {token.tipo}")


    def lista_argumentos(self):
        argumentos = []
        if self.token_atual.tipo != 'FECHA_PARENTESES':
            argumentos.append(self.expressao())
            while self.token_atual.tipo == 'VIRGULA':
                self.consumir('VIRGULA')
                argumentos.append(self.expressao())
        return argumentos
