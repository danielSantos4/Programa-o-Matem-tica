# Gerenciamento de Aterrissagem de Aeronaves

Este repositório apresenta a modelagem e implementação de um problema de **Gerenciamento de Aterrissagem de Aeronaves** em um aeroporto. O objetivo é determinar a melhor sequência de pouso dos aviões, minimizando as penalidades associadas a pousos antecipados ou atrasados.

## 📌 Descrição do Problema

Um grande aeroporto brasileiro recebeu uma rodada de investimentos privados e pretende automatizar o processo de gerenciamento da aterrissagem de aeronaves em seu pátio principal. 

Diariamente, um conjunto de **n** aviões pousa nesse aeroporto. Cada avião **i** possui as seguintes informações:

- **$R_i$**: Tempo de sua detecção pelo radar;
- **$E_i$**: Tempo inicial de pouso;
- **$T_i$**: Tempo ideal para o pouso;
- **$L_i$**: Tempo final que o avião **i** pode pousar;
- **$g_i$**: Penalidade por unidade de tempo se o avião **i** pousar antes do tempo ideal;
- **$h_i$**: Penalidade por unidade de tempo se o avião **i** pousar depois do tempo ideal.

Considere uma matriz **S = $[s_{ij}]$** com valores **$s_{ij}$**, onde **i, j = 1, ..., n**, representando o tempo de separação requerido após o pouso do avião **i** e antes do pouso do próximo avião **j**. 

A gerência de operações do aeroporto deseja determinar a sequência de aterrissagem dos aviões considerando apenas a pista principal de voo, bem como o tempo **$t_i$** em que cada avião deve aterrissar. 

Como critério de qualidade, pretende-se minimizar as penalidades em relação ao espaço de tempo em que cada avião **i** pousou antes ou depois do tempo ideal para pouso.


## 🛠️ Modelagem Matemática

O problema é modelado como um problema de **Programação Linear Inteira Mista (MILP)**, com as seguintes variáveis de decisão:

- **$t_i$**: Tempo de pouso do avião **i** (variável contínua);
- **$x_{ij}$**: Variável binária que indica se o avião **i** pousa antes do avião **j**.

### 🎯 Função Objetivo
Minimizar as penalidades totais associadas a pousos antecipados ou atrasados:

```math
Z = \sum_{i=1}^{n} \left( g_i \cdot d_i + h_i \cdot a_i \right)
```

Onde:
- **$d_i = max(0, T_i - t_i)$** representa o tempo que um avião pousa antes do ideal;
- **$a_i = max(0, t_i - T_i)$** representa o tempo que um avião pousa depois do ideal.

### ✅ Restrições

1. **Tempo de pouso dentro da janela permitida:**
   ```math
   E_i \leq t_i \leq L_i, \forall i = 1, \dots, n
   ```

2. **Tempo de separação entre aviões:**
   ```math
   t_j \geq t_i + s_{ij} - M \cdot (1 - x_{ij}), \forall i, j = 1, \dots, n, i \neq j
   ```

3. **Restrição de ordem:**
   ```math
   x_{ij} + x_{ji} = 1, \forall i, j = 1, \dots, n, i \neq j
   ```

4. **Linearização das penalidades:**
   ```math
   d_i \geq T_i - t_i, \quad a_i \geq t_i - T_i, \quad d_i \geq 0, \quad a_i \geq 0
   ```


## 🚀 Implementação

Este repositório contém duas abordagens para resolver o problema:

### 1️⃣ **Usando Gurobi**
A primeira abordagem utiliza o solver **Gurobi** para resolver o modelo de otimização de forma exata.


### 2️⃣ **Usando GRASP**
A segunda abordagem implementa um **algoritmo heurístico baseado em GRASP (Greedy Randomized Adaptive Search Procedure)**, que busca boas soluções de forma iterativa.

### 📥 Instalação das Dependências
```bash
pip install gurobipy
```

### ▶️ Executando o Código
#### 📌 Solução com Gurobi:
```bash
python gurobi.py caminho_do_arquivo
```

#### 📌 Solução com GRASP:
```bash
python problema_grasp.py caminho_do_arquivo fator_aleatoriedade numero_de_iteracoes

```

---

## 📊 Comparação das Soluções

Os resultados das duas abordagens são comparados considerando:
- **Tempo de execução**;
- **Qualidade da solução** .

As instâncias podem ser encontradas no diretório **`instancias/`**.
Os resultados das instâncias podem ser encontradas no diretório **`resultados/`**.


---


