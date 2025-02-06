from gurobipy import Model, GRB, quicksum
import sys

def ler_arquivo_input(caminho_arquivo):
    with open(caminho_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()

    # Ignorar a primeira linha (qtdeDeAvioes desconsidereEsseInput)
    linhas = linhas[1:]

    n = len(linhas) // 2  # Número de aviões
    R, E, T, L, g, h = [], [], [], [], [], []
    S = []

    for i in range(n):
        # Ler os dados do avião i
        dados_aviao = linhas[2 * i].strip().split()
        R.append(float(dados_aviao[0]))
        E.append(float(dados_aviao[1]))
        T.append(float(dados_aviao[2]))
        L.append(float(dados_aviao[3]))
        g.append(float(dados_aviao[4]))
        h.append(float(dados_aviao[5]))

        # Ler a linha de separação para o avião i
        separacao = list(map(float, linhas[2 * i + 1].strip().split()))
        S.append(separacao)

    return n, R, E, T, L, g, h, S

def resolver_problema(n, R, E, T, L, g, h, S):
    # Criação do modelo
    model = Model("Gerenciamento de Aterrissagem")

    # Variáveis de decisão
    t = model.addVars(n, lb=0, vtype=GRB.CONTINUOUS, name="t")  # Tempo de pouso
    x = model.addVars(n, n, vtype=GRB.BINARY, name="x")  # Ordem de pouso
    d = model.addVars(n, lb=0, vtype=GRB.CONTINUOUS, name="d")  # Penalidade por pouso antecipado
    a = model.addVars(n, lb=0, vtype=GRB.CONTINUOUS, name="a")  # Penalidade por pouso atrasado

    # Função objetivo
    model.setObjective(quicksum(g[i] * d[i] + h[i] * a[i] for i in range(n)), GRB.MINIMIZE)

    # Restrições
    for i in range(n):
        # Restrição de janela de tempo
        model.addConstr(t[i] >= E[i], name=f"tempo_inicial_{i}")
        model.addConstr(t[i] <= L[i], name=f"tempo_final_{i}")

        # Linearização das penalidades
        model.addConstr(d[i] >= T[i] - t[i], name=f"penalidade_antecipada_{i}")
        model.addConstr(a[i] >= t[i] - T[i], name=f"penalidade_atrasada_{i}")

    for i in range(n):
        for j in range(n):
            if i != j:
                # Restrição de separação entre aviões
                M = 1000  # Número grande o suficiente
                model.addConstr(t[j] >= t[i] + S[i][j] - M * (1 - x[i, j]), name=f"separacao_{i}_{j}")

                # Restrição de ordem
                model.addConstr(x[i, j] + x[j, i] == 1, name=f"ordem_{i}_{j}")

    # Resolver o modelo
    model.optimize()

    # Exibir resultados
    if model.status == GRB.OPTIMAL:
        print("Solução ótima encontrada!")
        print(f"Valor da função objetivo: {model.objVal}")
        for i in range(n):
            print(f"Avião {i+1}: Tempo de pouso = {t[i].X}, Penalidade antecipada = {d[i].X}, Penalidade atrasada = {a[i].X}")
    else:
        print("Não foi possível encontrar uma solução ótima.")

# Caminho do arquivo de input
if len(sys.argv) < 1:
    print("Uso: python script.py caminho_do_arquivo")
    sys.exit(1)
caminho_arquivo = sys.argv[1]  # Substitua pelo caminho do seu arquivo

# Ler os dados do arquivo
n, R, E, T, L, g, h, S = ler_arquivo_input(caminho_arquivo)

# Resolver o problema
resolver_problema(n, R, E, T, L, g, h, S)
