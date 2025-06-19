import GraphDataManager as gdm
import re

import matplotlib.pyplot as plt
import networkx as nx
from copy import deepcopy


from pulp import LpProblem, LpVariable, lpSum, LpMaximize, LpBinary, PULP_CBC_CMD
def max_cardinality_stable_matching(alunos, projetos):
    prob = LpProblem("MCSM", LpMaximize)
    # Variáveis binárias: x[a,p] == 1 se aluno a for alocado ao projeto p
    x = {
        (a, p): LpVariable(f"x_{a}_{p}", cat=LpBinary)
        for a, info in alunos.items()
        for p in info['preferencias']
        if p in projetos and info['nota'] >= projetos[p]['nota_min']
    }

    # 1. Cada aluno pode ter no máximo um projeto
    for a in alunos:
        prob += lpSum(x.get((a, p), 0) for p in alunos[a]['preferencias']) <= 1

    # 2. Cada projeto tem limite de vagas
    for p in projetos:
        prob += lpSum(x.get((a, p), 0) for a in alunos) <= projetos[p]['vagas']

    # 3. Impedir pares bloqueadores
    for a, info in alunos.items():
        prefs = info['preferencias']
        nota = info['nota']
        for p in prefs:
            if p not in projetos or nota < projetos[p]['nota_min']:
                continue

            # Estudante preferiria p a qualquer projeto alocado?
            worse_projects = prefs[prefs.index(p)+1:]

            # Constrói a condição de bloqueio:
            # se aluno não está alocado, ou está com projeto pior,
            # e projeto p tem vaga, então o par (a,p) é bloqueador — proibido.
            lhs = x.get((a, p), 0)
            rhs_aluno = lpSum(x.get((a, wp), 0) for wp in worse_projects)
            rhs_proj = lpSum(x.get((a2, p), 0) for a2 in alunos)

            prob += lhs + rhs_aluno + 1 <= projetos[p]['vagas'] + rhs_proj

    # 4. Função objetivo: maximizar o número de alocações
    prob += lpSum(x.values())

    # Resolver
    solver = PULP_CBC_CMD(msg=False)
    prob.solve(solver)

    # Interpretar solução
    emparelhamento = {}
    for (a, p), var in x.items():
        if var.varValue == 1:
            emparelhamento[a] = p

    return emparelhamento


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
    print("4 - Retornar a escolha de Algoritmo")
    escolha = input("Digite 1, 2, 3 ou 4: ").strip()

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
        return
    else:
        print()
        print("Opção inválida. Por favor, escolha 1, 2, 3 ou 4.")
        visualizacao(alunos,projetos,historico,dados, indice)



def inverter_emparelhamento(emparelhamento_aluno_projeto, alunos):
    # Inicializa o dicionário com todos os projetos de P1 a P50
    emparelhamento_projeto_aluno = {f'P{i}': [] for i in range(1, 51)}

    # Preenche com (nota, aluno) a partir do emparelhamento original
    for aluno_id, projeto_id in emparelhamento_aluno_projeto.items():
        if projeto_id in emparelhamento_projeto_aluno:
            nota = alunos[aluno_id]['nota']
            emparelhamento_projeto_aluno[projeto_id].append((nota, aluno_id))
        else:
            # Para projetos fora de P1 a P50 (opcional: pode ignorar ou incluir)
            nota = alunos[aluno_id]['nota']
            emparelhamento_projeto_aluno.setdefault(projeto_id, []).append((nota, aluno_id))

    return emparelhamento_projeto_aluno



# ---------------------- MAIN ----------------------
def main():
    # Armazenamos os daods dentro de dicionários para fácil leitura
    alunos = gdm.ler_dados_alunos("dadosAlunos.txt")
    projetos = gdm.ler_dados_projetos("dadosProjetos.txt")

    indice = gdm.retornaIndice(alunos,projetos)

    emparelhamento = max_cardinality_stable_matching(alunos, projetos, )
    emparelhamento = inverter_emparelhamento(emparelhamento, alunos)

    historico = []
    historico.append(emparelhamento)
    dados = gdm.coletaDados(historico[-1], alunos, projetos)

    

    visualizacao(alunos,projetos,historico,dados,indice)

    

if __name__ == "__main__":
    main()