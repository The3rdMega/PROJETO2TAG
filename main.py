import EmparelhamentoPriorizaAluno as epa
import EmparelhamentoPriorizaProjeto as epp
import EmparelhamentoPerfeito as emc

def main():
    print("Escolha o algoritmo de Emparelhamento:")
    print("1 - Prioriza Aluno (Aluno propõe)")
    print("2 - Prioriza Projeto (Projeto propõe)")
    print("3 - Máxima Cardinalidade (Pulp Solver)")
    print("4 - Terminar Execução")
    escolha = input("Digite 1, 2, 3 ou 4: ").strip()

    if escolha == '1':
        print()
        print("Executando Emparelhamento Prioriza Aluno...\n")
        epa.main()
    elif escolha == '2':
        print()
        print("Executando Emparelhamento Prioriza Projeto...\n")
        epp.main()
    elif escolha == '3':
        print()
        print("Executando Emparelhamento de Máxima Cardinalidade...\n")
        emc.main()
    elif escolha == '4':
        print()
        return
    else:
        print()
        print("Opção inválida. Por favor, escolha 1, 2, 3 ou 4.")

    main()

if __name__ == "__main__":
    main()