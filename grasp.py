import random

# Função para ler o arquivo de input
def ler_arquivo_input(caminho_arquivo):
    with open(caminho_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()

    # Ignorar a primeira linha (qtdeDeAvioes desconsidereEsseInput)
    linhas = linhas[1:]

    n = len(linhas) // 2  # Número de aviões
    R, E, T, L, a, b = [], [], [], [], [], []
    S = []

    for i in range(n):
        # Ler os dados do avião i
        dados_aviao = linhas[2 * i].strip().split()
        R.append(float(dados_aviao[0]))
        E.append(float(dados_aviao[1]))
        T.append(float(dados_aviao[2]))
        L.append(float(dados_aviao[3]))
        a.append(float(dados_aviao[4]))
        b.append(float(dados_aviao[5]))

        # Ler a linha de separação para o avião i
        separacao = list(map(float, linhas[2 * i + 1].strip().split()))
        S.append(separacao)

    return n, R, E, T, L, a, b, S

# Função para calcular a penalidade total de uma sequência de pouso
def calcular_penalidade(sequencia, R, E, T, L, a, b, S):
    penalidade_total = 0
    tempo_pouso = [0] * len(sequencia)

    for i in range(len(sequencia)):
        aviao_atual = sequencia[i]
        if i == 0:
            tempo_pouso[i] = max(R[aviao_atual], E[aviao_atual])
        else:
            aviao_anterior = sequencia[i - 1]
            tempo_pouso[i] = max(tempo_pouso[i - 1] + S[aviao_anterior][aviao_atual], R[aviao_atual], E[aviao_atual])

        # Penalidades por pouso antecipado ou atrasado
        if tempo_pouso[i] < T[aviao_atual]:
            penalidade_total += a[aviao_atual] * (T[aviao_atual] - tempo_pouso[i])
        elif tempo_pouso[i] > T[aviao_atual]:
            penalidade_total += b[aviao_atual] * (tempo_pouso[i] - T[aviao_atual])

    return penalidade_total

# Função para gerar uma solução inicial gulosa randomizada
def construir_solucao(n, R, E, T, L, a, b, S, alpha):
    candidatos = list(range(n))
    sequencia = []
    while len(candidatos) > 0:
        # Calcular o custo incremental de adicionar cada candidato
        custos = []
        for aviao in candidatos:
            sequencia_teste = sequencia + [aviao]
            custo = calcular_penalidade(sequencia_teste, R, E, T, L, a, b, S)
            custos.append(custo)

        # Criar a lista restrita de candidatos (RCL)
        custo_min = min(custos)
        custo_max = max(custos)
        limiar = custo_min + alpha * (custo_max - custo_min)
        rcl = [aviao for aviao, custo in zip(candidatos, custos) if custo <= limiar]

        # Selecionar aleatoriamente um avião da RCL
        escolhido = random.choice(rcl)
        sequencia.append(escolhido)
        candidatos.remove(escolhido)

    return sequencia

# Função de busca local (troca de posições)
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

# Algoritmo GRASP
def grasp(n, R, E, T, L, a, b, S, alpha, max_iteracoes):
    melhor_sequencia_inicial = None
    melhor_sequencia_final = None
    melhor_penalidade_final = float('inf')

    for _ in range(max_iteracoes):
        # Fase de construção
        sequencia_inicial = construir_solucao(n, R, E, T, L, a, b, S, alpha)
        penalidade_inicial = calcular_penalidade(sequencia_inicial, R, E, T, L, a, b, S)

        # Fase de busca local
        sequencia_final, penalidade_final = busca_local(sequencia_inicial, R, E, T, L, a, b, S)

        # Atualizar a melhor solução encontrada
        if penalidade_final < melhor_penalidade_final:
            melhor_sequencia_inicial = sequencia_inicial
            melhor_sequencia_final = sequencia_final
            melhor_penalidade_final = penalidade_final

    return melhor_sequencia_inicial, melhor_sequencia_final, melhor_penalidade_final

# Caminho do arquivo de input
caminho_arquivo = sys.argv[1]  # Substitua pelo caminho do seu arquivo

# Ler os dados do arquivo
n, R, E, T, L, a, b, S = ler_arquivo_input(caminho_arquivo)

# Parâmetros do GRASP
alpha = float(sys.argv[2])  # Parâmetro de aleatoriedade (0 = guloso, 1 = totalmente aleatório)
max_iteracoes = int(sys.argv[3])  # Número máximo de iterações

# Executar GRASP
melhor_sequencia_inicial, melhor_sequencia_final, melhor_penalidade_final = grasp(n, R, E, T, L, a, b, S, alpha, max_iteracoes)

# Exibir resultados
print("Melhor solução inicial:")
print("Sequência de pouso:", melhor_sequencia_inicial)
print("Penalidade inicial:", calcular_penalidade(melhor_sequencia_inicial, R, E, T, L, a, b, S))

print("\nMelhor solução final após busca local:")
print("Sequência de pouso:", melhor_sequencia_final)
print("Penalidade final:", melhor_penalidade_final)
