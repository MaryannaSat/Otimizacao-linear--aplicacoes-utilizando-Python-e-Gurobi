#########################################################################
# Maryanna Conceição Silva
# Esse programa foi desenvolvido durante uma iniciação cientifica
# na instituicao UNESP - IBILCE campus Sao Jose do Rio Preto
# sob orientacao da Profa. Dra. Maria do Socorro Nogueira Rangel
# data de ultima alteracao 01/02/2021
# no programa resolve-se o problema da Mochila
# Exercicio retirado da a lista 3, da materia de Otimização Linear do Prof. Silvio.
# Está dividido e os dados vem do 'Ex.txt'.
#######################################################################

import gurobipy as gp

def le_dados(nome_arq):
    with open(nome_arq, 'r') as f:
        linhas = f.readlines()#ler linhas
        #strip= tirar espacamento
        #split= quebrar
        valores = linhas[0].strip().split(' ')#elemento da linha 0
        qtd_itens = int(valores[0])#linha 0 e coluna 0
        capacidade = int(valores[1])#linha 0 e coluna 1
        #vetores de  valor e peso
        vet_pesos = list()
        vet_valores = list()
        del(linhas[0]) #apagar a primeira linha, como se não contase mais a primeira linha
        for linha in linhas:
            valores = linha.strip().split(' ')
            vet_pesos.append(int(valores[0]))
            vet_valores.append(int(valores[1]))

        #copiar e mudar algumas coisas do GurobiExOLLista2.py
        #rotulo
        itens = list()#nitens
        for i in range(qtd_itens):
            rotulo = 'Item_{}'.format(i + 1)
            itens.append(rotulo)

        #dicionario peso
        pesos = dict()
        for idx, peso in enumerate(vet_pesos):
            rotulo = itens[idx]
            pesos[rotulo] = peso

        # dicionario valores
        valores = dict()
        for idx, valor in enumerate(vet_valores):
            rotulo = itens[idx]
            valores[rotulo] = valor

    return itens, capacidade, pesos, valores#qtd_itens


def solve_ProblemaMochila(nome_arq):
    #ler dados
    itens, capacidade, pesos, valores = le_dados(nome_arq)

    # construir o modelo

    m = gp.Model()

    # variaveis

    x = m.addVars(itens, vtype=gp.GRB.BINARY)

    # função objetiva
    m.setObjective(gp.quicksum(x[i] * valores[i] for i in itens),
                   sense=gp.GRB.MAXIMIZE)  # quicksum = somatoria, sense = sentido

    # restrição

    c = m.addConstr(gp.quicksum(x[i] * pesos[i] for i in itens) <= capacidade)

    # executar
    m.optimize()
    return m.objVal
arq = 'inst_000.txt'
resultado = solve_ProblemaMochila(arq)
print(resultado)



