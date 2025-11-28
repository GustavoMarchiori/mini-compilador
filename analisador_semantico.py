class AnalisadorSemantico:
    def __init__(self):
        self.escopo_global = {}
        self.pilha_escopo = [self.escopo_global]

    def obter_escopo_atual(self):
        return self.pilha_escopo[-1]

    def analisar(self, ast):
        resultados = []
        for instrucao in ast:
            if instrucao['tipo'] == 'declaracao_funcao':
                self.declarar_funcao(instrucao)
            elif instrucao['tipo'] == 'atribuicao':
                self.atribuir_variavel(instrucao)
            elif instrucao['tipo'] == 'expressao':
                resultado = self.avaliar_expressao(instrucao['corpo'])
                resultados.append(resultado)
        return resultados

    def declarar_funcao(self, no):
        nome = no['nome']
        parametros = no['parametros']
        corpo = no['corpo']
        
        self.obter_escopo_atual()[nome] = {
            'tipo': 'funcao',
            'parametros': parametros,
            'corpo': corpo
        }

    def atribuir_variavel(self, no):
        nome = no['nome']
        valor = self.avaliar_expressao(no['valor'])
        
        self.obter_escopo_atual()[nome] = {
            'tipo': 'variavel',
            'valor': valor,
            'tipo_dado': type(valor).__name__
        }

    def avaliar_expressao(self, no):
        tipo = no['tipo']

        if tipo == 'numero':
            return no['valor']

        elif tipo == 'identificador':
            nome = no['nome']
            if nome not in self.obter_escopo_atual():
                raise Exception(f"Erro semântico: Variável ou função '{nome}' não definida.")
            
            simbolo = self.obter_escopo_atual()[nome]
            if simbolo['tipo'] == 'variavel':
                return simbolo['valor']
            else:
                raise Exception(f"Erro semântico: '{nome}' é uma função, não uma variável.")

        elif tipo == 'operacao':
            esquerda = self.avaliar_expressao(no['esquerda'])
            direita = self.avaliar_expressao(no['direita'])
            operador = no['operador']
            
            if not isinstance(esquerda, (int, float)) or not isinstance(direita, (int, float)):
                raise Exception(f"Erro semântico: Operação aritmética inválida entre tipos não numéricos.")

            if operador == 'OP_SOMA':
                return esquerda + direita
            elif operador == 'OP_SUBTRACAO':
                return esquerda - direita
            elif operador == 'OP_MULTIPLICACAO':
                return esquerda * direita
            elif operador == 'OP_DIVISAO':
                if direita == 0:
                    raise Exception("Erro semântico: Divisão por zero.")
                return esquerda / direita
            elif operador == 'OP_POTENCIA':
                return esquerda ** direita
            else:
                raise Exception(f"Erro semântico: Operador desconhecido {operador}")

        elif tipo == 'operacao_unaria':
            operando = self.avaliar_expressao(no['operando'])
            operador = no['operador']

            if not isinstance(operando, (int, float)):
                raise Exception(f"Erro semântico: Operação unária inválida em tipo não numérico.")

            if operador == 'OP_NEGACAO_UNARIA':
                return -operando
            else:
                raise Exception(f"Erro semântico: Operador unário desconhecido {operador}")

        elif tipo == 'chamada_funcao':
            nome = no['nome']
            argumentos_ast = no['argumentos']
            
            if nome not in self.obter_escopo_atual():
                raise Exception(f"Erro semântico: Função '{nome}' não definida.")
            
            funcao = self.obter_escopo_atual()[nome]
            if funcao['tipo'] != 'funcao':
                raise Exception(f"Erro semântico: '{nome}' não é uma função.")

            if len(argumentos_ast) != len(funcao['parametros']):
                raise Exception(f"Erro semântico: Função '{nome}' esperava {len(funcao['parametros'])} argumentos, mas recebeu {len(argumentos_ast)}.")

            valores_argumentos = [self.avaliar_expressao(arg_ast) for arg_ast in argumentos_ast]
            
            novo_escopo = self.obter_escopo_atual().copy()
            for nome_parametro, valor_argumento in zip(funcao['parametros'], valores_argumentos):
                novo_escopo[nome_parametro] = {'tipo': 'variavel', 'valor': valor_argumento, 'tipo_dado': type(valor_argumento).__name__}
            
            self.pilha_escopo.append(novo_escopo)

            resultado = self.avaliar_expressao(funcao['corpo'])

            self.pilha_escopo.pop()

            return resultado

        else:
            raise Exception(f"Erro semântico: Tipo de nó AST desconhecido: {tipo}")
