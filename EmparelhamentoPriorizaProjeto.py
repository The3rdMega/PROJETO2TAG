import GraphDataManager as gdm
import re

import matplotlib.pyplot as plt
import networkx as nx
from copy import deepcopy
import seaborn as sns
import pandas as pd

# ---------------------- GALE-SHAPLEY: PROJECT-PROPOSING ----------------------

def gale_shapley_projetos_propoem(alunos, projetos, max_iter=10):
    historico = []

    # Construir lista de candidatos qualificados para cada projeto
    for aluno, info in alunos.items():
        for proj in info['preferencias']:
            if proj in projetos and info['nota'] >= projetos[proj]['nota_min']:
                projetos[proj]['candidatos'].append((aluno, info['nota']))

    # Ordenar candidatos por nota (maior primeiro)
    for p in projetos:
        projetos[p]['candidatos'].sort(key=lambda x: -x[1])

    # Inicializações
    emparelhamento = {p: [] for p in projetos}
    alocados = {}  # aluno -> projeto atual

    for it in range(max_iter):
        mudou = False
        for p, info in projetos.items():    # Para cada projeto e Informação atual do projeto
            vagas = info['vagas']   # numero de vagas do projeto
            candidatos = info['candidatos'] # lista de candidatos possíveis para o projeto

            for a, n in candidatos: # para cada aluno e nota
                if a in alocados:   # se o aluno já estiver alocado a outro projeto
                    projeto_atual = alocados[a] # projeto_atual = projeto em que o aluno está alocado atualmente
                    prefs = alunos[a]['preferencias']   # pega a lista de preferencias do aluno
                    if prefs.index(p) < prefs.index(projeto_atual): # se o aluno prefere o projeto analisado ao seu projeto atual
                        # Só realoca se houver vaga no novo projeto
                        if len(emparelhamento[p]) < vagas:
                            # Remover do projeto anterior
                            emparelhamento[projeto_atual] = [
                                (nota, aid) for (nota, aid) in emparelhamento[projeto_atual] if aid != a
                            ]
                            # Adicionar ao novo projeto
                            emparelhamento[p].append((n, a))
                            alocados[a] = p
                            mudou = True
                else:
                    # Aluno livre
                    if len(emparelhamento[p]) < vagas:
                        emparelhamento[p].append((n, a))
                        alocados[a] = p
                        mudou = True

        historico.append({k: v.copy() for k, v in emparelhamento.items()})
        if not mudou:
            break

    return historico





def realizarColeta(dados):
    for k, v in dados.items():
        match k:
            case "num_alunos_inscritos": print(f'Número de Alunos Inscritos: {v}')
            case "lista_alunos_inscritos": 
                print('Lista de Alunos Inscritos:')
                for par in v:
                    if par == v[-1]:
                        print(f'{par[0]} inscrito em {par[1]}.')
                        break
                    print(f'{par[0]} inscrito em {par[1]}', end= ', ')
            case "num_alunos_nao_inscritos": print(f'Número de Alunos não Inscritos: {v}')
            case "lista_alunos_nao_inscritos":
                print('Lista de Alunos não Inscritos:')
                for aluno in v:
                    if aluno == v[-1]:
                        print(f'{aluno}.')
                        break
                    print(f'{aluno}', end= ', ')
            case "num_projetos_vazios": print(f'Número de Projetos Vazios: {v}')
            case "lista_projetos_vazios": 
                print('Lista de Projetos não Realizados (Sem Alunos):')
                for projeto in v:
                    if projeto == v[-1]:
                        print(f'{projeto}.')
                        break
                    print(f'{projeto}', end= ', ')
            case "num_projetos_realizados": print(f'Número de Projetos Realizados: {v}')
            case "lista_projetos_realizados": 
                print('Lista de Projetos Realizados:')
                for projeto in v:
                    if projeto == v[-1]:
                        print(f'{projeto}.')
                        break
                    print(f'{projeto}', end= ', ')
            case "media_alunos_por_projeto": print(f'Média de Alunos por Projeto: {v}')
            case "tamanho_emparelhamento": print(f'Tamanho do Emparelhamento (Arestas): {v}')
        print()

def desenharGrafo(historico, alunos, projetos, showNonConnected=False):
    gdm.desenhar_grafo(historico, alunos, projetos, showNonConnected)

def mostraIndice(indice):
    print('Porcentagem de preferência por projeto')
    print()
    for k, v in indice.items():
        print(f"{k}: {v:.2f}%")

def visualizacao(alunos,projetos,historico,dados, indice):
    print("Escolha a execução a ser feita:")
    print("1 - Coleta de Dados")
    print("2 - Desenho do Grafo")
    print("3 - Visualizar o Índice de Preferência por Projeto")
    print("4 - Visualizar a Matriz de Emparelhamento")
    print("5 - Retornar a escolha de Algoritmo")
    escolha = input("Digite 1, 2, 3, 4 ou 5: ").strip()

    if escolha == '1':
        print()
        print("Mostrando Coleta de dados\n")
        realizarColeta(dados)
        visualizacao(alunos,projetos,historico,dados, indice)
    elif escolha == '2':
        print()
        print("Mostrando Grafos gerado (todas as iterações)\n")
        desenharGrafo(historico, alunos, projetos, showNonConnected=False)
        visualizacao(alunos,projetos,historico,dados, indice)
    elif escolha == '3':
        print()
        print("Mostrando índice de Preferência por Projeto\n")
        mostraIndice(indice)
        visualizacao(alunos,projetos,historico,dados, indice)
    elif escolha == '4':
        print()
        print('Mostrando Matriz de Emparelhamento\n')
        gdm.geraMatriz(historico[-1])
        visualizacao(alunos,projetos,historico,dados, indice)
    elif escolha == '5':
        print()
        return
    else:
        print()
        print("Opção inválida. Por favor, escolha 1, 2, 3, 4 ou 5.")
        visualizacao(alunos,projetos,historico,dados, indice)



# ---------------------- MAIN ----------------------
def main():
    alunos = gdm.ler_dados_alunos("dadosAlunos.txt")
    projetos = gdm.ler_dados_projetos("dadosProjetos.txt")

    indice = gdm.retornaIndice(alunos,projetos)


    historico = gale_shapley_projetos_propoem(alunos, projetos, max_iter=10)
    dados = gdm.coletaDados(historico[-1], alunos, projetos)


    visualizacao(alunos,projetos,historico,dados, indice)


if __name__ == "__main__":
    main()