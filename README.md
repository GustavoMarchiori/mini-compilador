# Mini Compilador de Expressões Matemáticas

Este projeto consiste na implementação de um mini compilador em Python para uma linguagem de expressões matemáticas simples, com suporte a variáveis, operadores aritméticos e funções definidas pelo usuário. O compilador segue as etapas clássicas de análise léxica, sintática e semântica.

## 🚀 Funcionalidades da Linguagem

A linguagem suporta as seguintes construções:

*   **Declaração de Funções**: Definição de funções de uma única linha com parâmetros.
    *   Sintaxe: `funcao nome(param1, param2) = expressao`
*   **Atribuição de Variáveis**: Atribuição de valores de expressões a identificadores.
    *   Sintaxe: `variavel = expressao`
*   **Operadores Aritméticos**: Suporte aos operadores básicos e potência, respeitando a precedência.
    *   Operadores: `+`, `-`, `*`, `/`, `^` (potência)
*   **Tipos de Dados**: Suporte nativo para números inteiros e de ponto flutuante.
*   **Escopo Simples**: Implementação de um escopo global para variáveis e funções.

## 🏗️ Arquitetura do Compilador

O compilador é modular e está dividido em três componentes principais, além do arquivo de execução:

| Arquivo | Componente | Descrição |
| :--- | :--- | :--- |
| `analisador_lexico.py` | **Analisador Léxico** (Lexer) | Responsável por ler o código-fonte e convertê-lo em uma sequência de *tokens* (unidades mínimas da linguagem), como `NUMERO`, `IDENTIFICADOR`, `OP_SOMA`, etc. |
| `analisador_sintatico.py` | **Analisador Sintático** (Parser) | Baseado em uma gramática LL(1) (implementada via análise descendente recursiva), verifica se a sequência de tokens está em conformidade com a sintaxe da linguagem e constrói a **Árvore de Sintaxe Abstrata (AST)**. |
| `analisador_semantico.py` | **Analisador Semântico** e **Interpretador** | Percorre a AST para realizar a verificação de tipos, escopo (simples) e chamadas de função. Ele também atua como um interpretador, avaliando as expressões e executando as atribuições e chamadas de função. |
| `main.py` | **Módulo Principal** | Orquestra as etapas de compilação (léxica, sintática e semântica) e contém os casos de teste para validação. |

## ⚙️ Como Executar

Para executar o mini compilador e rodar os casos de teste definidos, basta ter o Python instalado e executar o arquivo principal:

```bash
python3 main.py
```
