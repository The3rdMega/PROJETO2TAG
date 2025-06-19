import re

import matplotlib.pyplot as plt
import networkx as nx
from copy import deepcopy
import seaborn as sns
import pandas as pd

def coletaDados(estado_final, alunos, projetos):
    alunos_inscritos = set()
    projetos_realizados = set()
    total_alocados = 0
    inscricoes = []

    for projeto, lista in estado_final.items():
        if lista:
            projetos_realizados.add(projeto)
            for nota, aluno in lista:
                alunos_inscritos.add(aluno)
                inscricoes.append((aluno, projeto))
                total_alocados += 1

    todos_alunos = set(alunos.keys())
    alunos_nao_inscritos = list(todos_alunos - alunos_inscritos)

    todos_projetos = set(projetos.keys())
    projetos_vazios = list(todos_projetos - projetos_realizados)

    media_alunos = total_alocados / len(projetos_realizados) if projetos_realizados else 0

    tamanho_emparelhamento = sum(len(v) for v in estado_final.values())

    return {
        "num_alunos_inscritos": len(alunos_inscritos),
        "lista_alunos_inscritos": inscricoes,
        "num_alunos_nao_inscritos": len(alunos_nao_inscritos),
        "lista_alunos_nao_inscritos": alunos_nao_inscritos,
        "num_projetos_vazios": len(projetos_vazios),
        "lista_projetos_vazios": projetos_vazios,
        "num_projetos_realizados": len(projetos_realizados),
        "lista_projetos_realizados": list(projetos_realizados),
        "media_alunos_por_projeto": media_alunos,
        "tamanho_emparelhamento": tamanho_emparelhamento
}

def desenhar_grafo(historico, alunos, projetos, showNonConnected=True):
    for i, estado in enumerate(historico):
        G = nx.Graph()

        # Criar arestas a partir do estado atual (iterações do algoritmo)
        edges = [(a, p) for p, lista in estado.items() for (_, a) in lista]

        # Adicionar nós conforme configuração
        if showNonConnected:
            G.add_nodes_from(alunos.keys(), bipartite=0)
            G.add_nodes_from(projetos.keys(), bipartite=1)
        else:
            conectados = set()
            for a, p in edges:
                conectados.add(a)
                conectados.add(p)
            G.add_nodes_from(conectados)

        # Adicionar arestas
        G.add_edges_from(edges)

        # Layout bipartido
        left_nodes = [n for n in G.nodes if n in alunos]
        pos = nx.bipartite_layout(G, left_nodes)
        # Aumenta o espaçamento horizontal e vertical
        pos = {n: (x , y * 100) for n, (x, y) in pos.items()}


        # Cores por tipo de nó
        cores = ['skyblue' if n in alunos else 'lightgreen' for n in G.nodes]

        # Desenhar o grafo
        plt.figure(figsize=(12, 6))
        nx.draw(
            G, pos,
            with_labels=True,
            node_color=cores,
            edge_color='gray',
            node_size=1000, #Alterar caso vizualisação incerta
            font_size=10
        )
        plt.title(f"Iteração {i + 1}")
        plt.show()

def ler_dados_alunos(caminho_arquivo):
    alunos = {}
    with open(caminho_arquivo, 'r') as f:
        for linha in f:
            linha = linha.strip()
            match = match = re.match(r"\((A\d+)\):\((P\d+)(?:,\s*(P\d+))?(?:,\s*(P\d+))?\)\s*\((\d)\)", linha)
            if match:
                aluno_id = match.group(1)
                preferencias = [p for p in match.group(2, 3, 4) if p]
                nota = int(match.group(5))
                alunos[aluno_id] = {
                    "preferencias": preferencias,
                    "nota": nota
                }
            else:
                print(f"Linha ignorada (formato inválido): {linha}")
    return alunos

# Funcão que realiza a leitura do arquivo dadosProjetos.txt
def ler_dados_projetos(caminho_arquivo):
    projetos = {}
    with open(caminho_arquivo, 'r') as f:
        for linha in f:
            linha = linha.strip()
            match = re.match(r"\((P\d+),\s*(\d+),\s*(\d+)\)", linha)
            if match:
                projeto_id = match.group(1)
                vagas = int(match.group(2))
                nota_min = int(match.group(3))
                projetos[projeto_id] = {
                    "vagas": vagas,
                    "nota_min": nota_min,
                    "candidatos": []  # será usado posteriormente
                }
            else:
                print(f"Linha ignorada (formato inválido): {linha}")
    return projetos


def retornaIndice(alunos, projetos):
    # Inicializa o dicionário com todos os projetos de P1 a P50 com valor 0
    indice = {f'P{i}': 0 for i in range(1, 51)}
    totalPontos = 0

    for aluno_id, info in alunos.items():
        preferencias = info["preferencias"]

        for i, projeto_id in enumerate(preferencias):  # Não há mais slicing
            if projeto_id in projetos:
                pontos = 3 - i  # 3 para o 1º, 2 para o 2º, 1 para o 3º
                indice[projeto_id] += pontos
                totalPontos += pontos

    # Gera dicionário final com porcentagens
    if totalPontos == 0:
        print("Nenhum ponto foi computado.")
        return

    porcentagens = {
        k: (v / totalPontos) * 100 for k, v in indice.items()
    }
    '''
    # Printa o resultado
    for k, v in porcentagens.items():
        print(f"{k}: {v:.2f}%")
    '''
    return porcentagens





def geraMatriz(emparelhamento):
    # Cria listas ordenadas
    alunos_ids = [f'A{i}' for i in range(1, 201)]
    projetos_ids = [f'P{i}' for i in range(1, 51)]

    # Inicializa matriz como DataFrame (linhas = projetos, colunas = alunos)
    matriz_df = pd.DataFrame(0, index=projetos_ids, columns=alunos_ids)

    # Preenche a matriz com base no emparelhamento
    for projeto, tuplas in emparelhamento.items():
        for nota, aluno in tuplas:
            if projeto in matriz_df.index and aluno in matriz_df.columns:
                matriz_df.at[projeto, aluno] = 1

    # Plot com seaborn
    plt.figure(figsize=(20, 10))
    sns.heatmap(matriz_df, cmap="Greys", cbar=False, linewidths=0.1, linecolor='lightgray')
    plt.title("Matriz de Alocação (Projetos vs Alunos)", fontsize=16)
    plt.xlabel("Alunos")
    plt.ylabel("Projetos")
    plt.xticks(rotation=90, fontsize=6)
    plt.yticks(rotation=0, fontsize=8)
    plt.tight_layout()
    plt.show()


