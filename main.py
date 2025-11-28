from analisador_lexico import AnalisadorLexico
from analisador_sintatico import AnalisadorSintatico
from analisador_semantico import AnalisadorSemantico


def compilar(codigo):
    print(f"{"-"*9}Código Fonte{"-"*9}\n")
    print(codigo)
    print(f"\n{"-"*30}\n")
    
    try:
        print("1. Análise Léxica...")
        lexico = AnalisadorLexico(codigo)
        tokens = lexico.tokenizar()
        print("Tokens gerados:")
        print([str(t) for t in tokens])
        
        print("\n2. Análise Sintática...")
        
        ast_instrucoes = []
        sintatico_reset = AnalisadorSintatico(tokens)
        while sintatico_reset.token_atual.tipo != 'FIM_DE_ARQUIVO':
            if sintatico_reset.token_atual.tipo == 'FUNCAO':
                sintatico_reset.consumir('FUNCAO')
                nome_funcao = sintatico_reset.consumir('IDENTIFICADOR')
                sintatico_reset.consumir('ABRE_PARENTESES')
                parametros = sintatico_reset.lista_parametros()
                sintatico_reset.consumir('FECHA_PARENTESES')
                sintatico_reset.consumir('ATRIBUICAO')
                expressao_corpo = sintatico_reset.expressao()
                
                ast_instrucoes.append({
                    'tipo': 'declaracao_funcao',
                    'nome': nome_funcao,
                    'parametros': parametros,
                    'corpo': expressao_corpo
                })
            
            elif sintatico_reset.token_atual.tipo == 'IDENTIFICADOR' and sintatico_reset.tokens[sintatico_reset.indice + 1].tipo == 'ATRIBUICAO':
                nome_variavel = sintatico_reset.consumir('IDENTIFICADOR')
                sintatico_reset.consumir('ATRIBUICAO')
                expressao_valor = sintatico_reset.expressao()
                
                ast_instrucoes.append({
                    'tipo': 'atribuicao',
                    'nome': nome_variavel,
                    'valor': expressao_valor
                })
            
            else:
                expressao_isolada = sintatico_reset.expressao()
                ast_instrucoes.append({
                    'tipo': 'expressao',
                    'corpo': expressao_isolada
                })

            if sintatico_reset.token_atual.tipo == 'FIM_DE_LINHA':
                sintatico_reset.consumir('FIM_DE_LINHA')
            elif sintatico_reset.token_atual.tipo != 'FIM_DE_ARQUIVO':
                raise Exception(f"Erro sintático: Esperado FIM_DE_LINHA ou FIM_DE_ARQUIVO, encontrado {sintatico_reset.token_atual.tipo}")

        print("Análise Sintática concluída. AST gerada.")

        print("\n3. Análise Semântica e Execução...")
        semantico = AnalisadorSemantico()
        resultados = semantico.analisar(ast_instrucoes)
        
        print("\nResultados da Execução:")
        for resultado in resultados:
            print(f"-> {resultado}")
        
        print("\nTabela de Símbolos Final:")
        for nome, simbolo in semantico.escopo_global.items():
            if simbolo['tipo'] == 'variavel':
                print(f"Variável {nome}: {simbolo['valor']} ({simbolo['tipo_dado']})")
            elif simbolo['tipo'] == 'funcao':
                params = ', '.join(simbolo['parametros'])
                print(f"Função {nome}({params})")

    except Exception as e:
        print(f"\nERRO: {e}")


casos_teste = [
"""
x = 10 + 5 * 2
x
""",

"""
pi = 3.14159
area = pi * 5 ^ 2
area
""",

"""
funcao dobro(a) = a * 2
funcao soma(x, y) = x + y

res1 = dobro(15)
res2 = soma(res1, 5)
res2
""",

"""
y = -3 + 4 * (2 - 1) ^ 2
y
""",

"""
a = 10 / 0
""",

"""
resultado = funcao_nao_existe(1)
""",

"""
z = (1 + 2
""",
]

if __name__ == "__main__":
    for i, codigo in enumerate(casos_teste):
        print(f"\n{"="*30}")
        print(f"{" "*7}CASO DE TESTE {i+1}{" "*7}")
        print(f"{"="*30}\n")
        compilar(codigo.strip())
        print("\n")
