"""
Especificações do Projeto Simplificadas:

Estrutura dos dados:
Aluno: (AN):(PN1,PN2,PN3) (N)
Onde AN é o número do aluno, PN1,PN2 e PN3 são as preferências de projeto do aluno e N é a nota dele entre 3,4,5

Projeto: (PN,NV,NM)
Onde PN é o número do projeto, NV é o número de vagas e NM é o requisito mínimo de nota do aluno


Possível estratégia:
Primeiro lemos o arquivo e adicionamos todos os Projetos e Alunos em dicionários. 
Depois, adicionamos todos eles como nós em um grafo,
Por fim, conectamos todos os nós que satisfaçam as condições:
- Aluno tem nota suficiente para o projeto
- Aluno tem o projeto em sua lista de preferências
"""
import GraphDataManager as gdm
import re

import matplotlib.pyplot as plt
import networkx as nx
from copy import deepcopy
import seaborn as sns
import pandas as pd


def gale_shapley_visual(alunos, projetos, max_iter=10):
    alunos_livres = {a for a in alunos}
    inscricoes = {a: [] for a in alunos}
    projeto_alocados = {p: [] for p in projetos}
    iteracao = 0
    historico = []

    while iteracao < max_iter:
        houve_alocacao = False
        for a in list(alunos_livres):
            aluno = alunos[a]
            prefs = aluno['preferencias']
            nota = aluno['nota']
            inscricoes_feitas = inscricoes[a]

            # Verificar se há algum projeto ainda não tentado
            projetos_a_tentar = [p for p in prefs if p not in inscricoes_feitas]
            if not projetos_a_tentar:
                continue  # nada mais a tentar

            p = projetos_a_tentar[0]
            inscricoes[a].append(p)
            projeto = projetos[p]
            min_nota = projeto['nota_min']
            vagas = projeto['vagas']
            alocados = projeto_alocados[p]

            if nota < min_nota:
                continue  # não qualifica

            if len(alocados) < vagas:
                alocados.append((nota, a))
                alunos_livres.remove(a)
                houve_alocacao = True

            else:
                # Já cheio, ver se substitui alguém
                pior_aluno = min(alocados, key=lambda x: x[0])  # menor nota
                if nota > pior_aluno[0]:
                    alocados.remove(pior_aluno)
                    alocados.append((nota, a))
                    alunos_livres.remove(a)
                    alunos_livres.add(pior_aluno[1])
                    houve_alocacao = True

        # Salvar estado do grafo atual para visualização
        historico.append(deepcopy(projeto_alocados))
        if not houve_alocacao:
            break  # não houve mudanças, estável
        iteracao += 1

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


'''
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
        #desenharGrafo(historico, alunos, projetos, showNonConnected=False)
        chooseIterationDraw(historico,alunos,projetos,showNonConnected=False)
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
'''

def visualizacao(lista_alunos,projetos,iteracoes,lista_dados, indice):
    print("Escolha a execução a ser feita:")
    print("1 - Coleta de Dados")
    print("2 - Desenho do Grafo")
    print("3 - Visualizar o Índice de Preferência por Projeto")
    print("4 - Visualizar a Matriz de Emparelhamento")
    print("5 - Retornar a escolha de Algoritmo")
    escolha = input("Digite 1, 2, 3, 4 ou 5: ").strip()

    if escolha == '1':
        print()
        print("Escolha a iteração de 1 a 10 para coletar os dados:")
        iteracaoEscolhida = input()
        if not (iteracaoEscolhida.isdigit() and 0 < int(iteracaoEscolhida) <= 10):
            print("Opção inválida. Por favor, escolha um número entre 1 e 10.")
            visualizacao(lista_alunos,projetos,iteracoes, lista_dados, indice)
        print("Mostrando Coleta de dados\n")
        realizarColeta(lista_dados[int(iteracaoEscolhida) - 1])
        visualizacao(lista_alunos,projetos,iteracoes,lista_dados, indice)
    elif escolha == '2':
        print()
        print("Escolha a iteração de 1 a 10 para desenhar o grafo:")
        iteracaoEscolhida = input()
        if not (iteracaoEscolhida.isdigit() and 0 < int(iteracaoEscolhida) <= 10):
            print("Opção inválida. Por favor, escolha um número entre 1 e 10.")
            visualizacao(lista_alunos,projetos,iteracoes, lista_dados, indice)
        print("Mostrando Grafos gerado (todas as iterações)\n")
        desenharGrafo(iteracoes[int(iteracaoEscolhida) - 1], lista_alunos[int(iteracaoEscolhida) - 1], projetos, showNonConnected=False)
        #chooseIterationDraw(historico,alunos,projetos,showNonConnected=False)
        visualizacao(lista_alunos,projetos,iteracoes,lista_dados, indice)
    elif escolha == '3':
        print()
        print("Mostrando índice de Preferência por Projeto\n")
        mostraIndice(indice)
        visualizacao(lista_alunos,projetos,iteracoes,lista_dados, indice)
    elif escolha == '4':
        print()
        print("Escolha a iteração de 1 a 10 para desenhar o grafo:")
        iteracaoEscolhida = input()
        if not (iteracaoEscolhida.isdigit() and 0 < int(iteracaoEscolhida) <= 10):
            print("Opção inválida. Por favor, escolha um número entre 1 e 10.")
            visualizacao(lista_alunos,projetos,iteracoes, lista_dados, indice)
        print('Mostrando Matriz de Emparelhamento\n')
        gdm.geraMatriz(iteracoes[int(iteracaoEscolhida) - 1][-1])

        visualizacao(lista_alunos,projetos,iteracoes,lista_dados, indice)
    elif escolha == '5':
        print()
        return
    else:
        print()
        print("Opção inválida. Por favor, escolha 1, 2, 3, 4 ou 5.")
        visualizacao(lista_alunos,projetos,iteracoes,lista_dados, indice)


import random
from copy import deepcopy

# ---------------------- MAIN ----------------------
def main():
    # Armazenamos os daods dentro de dicionários para fácil leitura
    alunos = gdm.ler_dados_alunos("dadosAlunos.txt")
    projetos = gdm.ler_dados_projetos("dadosProjetos.txt")

    indice = gdm.retornaIndice(alunos,projetos)

    iteracoes = []
    dados_iteracoes = []
    iteracoes_alunos = []

    for i in range(10):
        alunos_copy = deepcopy(alunos)
        #Limpa preferências inexistentes de alunos (P51+)
        for aluno_id, dados in alunos_copy.items():
            dados['preferencias'] = [p for p in dados['preferencias'] if p in projetos]
        
         # Embaralhar a ordem dos alunos
        chaves_embaralhadas = list(alunos_copy.keys())
        random.shuffle(chaves_embaralhadas)
        alunos_copy = {k: alunos_copy[k] for k in chaves_embaralhadas}

        historico = gale_shapley_visual(alunos_copy, projetos, max_iter=10)
        iteracoes.append(historico)
        dados = gdm.coletaDados(historico[-1], alunos_copy, projetos)
        dados_iteracoes.append(dados)
        iteracoes_alunos.append(alunos_copy)


    #visualizacao(alunos,projetos,historico,dados, indice)
    visualizacao(iteracoes_alunos, projetos, iteracoes,dados_iteracoes, indice)
    

if __name__ == "__main__":
    main()