#########################################################################
# Maryanna Conceição Silva.
# Esse programa foi desenvolvido durante uma iniciação cientifica
# na instituicao UNESP - IBILCE campus Sao Jose do Rio Preto
# sob orientacao da Profa. Dra. Maria do Socorro Nogueira Rangel
# data de ultima alteracao 01/02/2021
# no programa resolve-se o problema do Caxeiro Viajante
# Exercicio retirado do livro do Arenales, pagina 118 e ex. 3.11
# Dividido e o modelo são do Video do Prof Rafael Lima
#######################################################################
import gurobipy as gp
from gurobipy import GRB

def le_dados(nome_arq):
    with open(nome_arq, 'r') as f:
        linhas = f.readlines()#ler linhas
        valores = linhas[0].strip().split(' ')
        qtd_cidades = int(valores[0])
        del (linhas[0])
        custo = list()
        for linha in linhas:
            valores = linha.strip().split(' ')
            for i in range(0, len(valores)):
                valores[i] = int(valores[i])
            custo.append(valores)
    #retornar dados
    return qtd_cidades, custo


def solve_CaixeiroViajante(nome_arq):
    #ler dados
    cidades, mat_custos = le_dados(nome_arq)

    # Indices dos pontos de origem e destino
    origens = [i + 1 for i in range(cidades)]
    destinos = [i + 1 for i in range(cidades)]

    # Dicionário dos custos
    custos = dict()
    for i, origem in enumerate(origens):
        for j, destino in enumerate(destinos):
            custos[origem, destino] = mat_custos[i][j]

    # iniciar o modelo

    m = gp.Model()

    # variaveis de decisão
    x = m.addVars(origens, destinos, vtype=gp.GRB.BINARY)

    # Função Obj

    m.setObjective(x.prod(custos), sense=gp.GRB.MINIMIZE)

    # Restrições que garantem que cada ponto será origem exatamente uma vez
    c1 = m.addConstrs(
        gp.quicksum(x[i, j] for j in destinos if i != j) == 1
        for i in origens)

    # Restrições que garantem que cada ponto será origem exatamente uma vez
    c2 = m.addConstrs(
        gp.quicksum(x[i, j] for i in origens if i != j) == 1
        for j in destinos)

    # Restrições de eliminação de subrotas



    m.optimize()

    # Constrói o vetor com o circuito,
    circuito = [1]
    anterior = 1
    for ponto in range(cidades):
        for j in destinos:
            if round(x[anterior, j].X) == 1:
                circuito.append(j)
                anterior = j
                break
    for i in origens:
        print(f'{i:02d}:', end='')
        for j in destinos:
            print(round(x[i, j].X), '', end='')
        print('')

    return m.objVal, circuito



arq = 'inst_000 - Ramon.txt'
resultado, circuito= solve_CaixeiroViajante(arq)
print(resultado)
print(circuito)





