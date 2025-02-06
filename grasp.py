import random
import copy
import sys

def ler_entrada(arquivo):
    with open(arquivo, 'r') as f:
        linhas = f.readlines()
    
    n = int(linhas[0].split()[0])  # Número de aviões
    R, E, T, L, a, b = [], [], [], [], [], []
    S = [[0.0] * n for _ in range(n)]
    
    index = 1
    for i in range(n):
        valores = list(map(float, linhas[index].split()))
        R.append(valores[0])
        E.append(valores[1])
        T.append(valores[2])
        L.append(valores[3])
        a.append(valores[4])
        b.append(valores[5])
        index += 1
        
        S[i] = list(map(float, linhas[index].split()))
        index += 1
    
    return n, R, E, T, L, a, b, S

def calcular_penalidade(sequencia, R, E, T, L, a, b, S):
    penalidade_total = 0.0
    tempo_pouso = [0.0] * len(sequencia)

    for i in range(len(sequencia)):
        aviao_atual = sequencia[i]
        if i == 0:
            tempo_pouso[i] = max(R[aviao_atual], E[aviao_atual])
        else:
            aviao_anterior = sequencia[i - 1]
            tempo_pouso[i] = max(tempo_pouso[i - 1] + S[aviao_anterior][aviao_atual], R[aviao_atual], E[aviao_atual])

        if tempo_pouso[i] < T[aviao_atual]:
            penalidade_total += a[aviao_atual] * (T[aviao_atual] - tempo_pouso[i])
        elif tempo_pouso[i] > T[aviao_atual]:
            penalidade_total += b[aviao_atual] * (tempo_pouso[i] - T[aviao_atual])

    return penalidade_total

def construir_solucao(n, R, E, T, L, a, b, S, alpha):
    candidatos = list(range(n))
    sequencia = []
    while len(candidatos) > 0:
        custos = []
        for aviao in candidatos:
            sequencia_teste = sequencia + [aviao]
            custo = calcular_penalidade(sequencia_teste, R, E, T, L, a, b, S)
            custos.append(custo)
        
        custo_min = min(custos)
        custo_max = max(custos)
        limiar = custo_min + alpha * (custo_max - custo_min)
        rcl = [aviao for aviao, custo in zip(candidatos, custos) if custo <= limiar]
        
        escolhido = random.choice(rcl)
        sequencia.append(escolhido)
        candidatos.remove(escolhido)
    
    return sequencia

def busca_local(sequencia, R, E, T, L, a, b, S):
    melhor_sequencia = sequencia.copy()
    melhor_penalidade = calcular_penalidade(melhor_sequencia, R, E, T, L, a, b, S)

    for i in range(len(sequencia)):
        for j in range(i + 1, len(sequencia)):
            nova_sequencia = sequencia.copy()
            nova_sequencia[i], nova_sequencia[j] = nova_sequencia[j], nova_sequencia[i]
            nova_penalidade = calcular_penalidade(nova_sequencia, R, E, T, L, a, b, S)

            if nova_penalidade < melhor_penalidade:
                melhor_sequencia = nova_sequencia
                melhor_penalidade = nova_penalidade

    return melhor_sequencia, melhor_penalidade

def grasp(n, R, E, T, L, a, b, S, alpha, max_iteracoes):
    melhor_sequencia = None
    melhor_penalidade = float('inf')

    for _ in range(max_iteracoes):
        sequencia = construir_solucao(n, R, E, T, L, a, b, S, alpha)
        sequencia, penalidade = busca_local(sequencia, R, E, T, L, a, b, S)

        if penalidade < melhor_penalidade:
            melhor_sequencia = sequencia
            melhor_penalidade = penalidade

    return melhor_sequencia, melhor_penalidade

if __name__ == "__main__":
    arquivo_entrada = sys.argv[1]  # Nome do arquivo de entrada
    n, R, E, T, L, a, b, S = ler_entrada(arquivo_entrada)

    alpha = float(sys.argv[2])
    max_iteracoes = int(sys.argv[3])

    melhor_sequencia, melhor_penalidade = grasp(n, R, E, T, L, a, b, S, alpha, max_iteracoes)

    print("Melhor sequência de pouso:", melhor_sequencia)
    print("Penalidade total:", round(melhor_penalidade, 2))

