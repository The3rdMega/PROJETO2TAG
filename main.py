import EmparelhamentoPriorizaAluno as epa
import EmparelhamentoPriorizaProjeto as epp

def main():
    print("Escolha o algoritmo de Emparelhamento:")
    print("1 - Prioriza Aluno (Aluno propõe)")
    print("2 - Prioriza Projeto (Projeto propõe)")
    print("3 - Terminar Execução")
    escolha = input("Digite 1, 2 ou 3: ").strip()

    if escolha == '1':
        print()
        print("Executando Emparelhamento Prioriza Aluno...\n")
        epa.main()
    elif escolha == '2':
        print()
        print("Executando Emparelhamento Prioriza Projeto...\n")
        epp.main()
    elif escolha == '3':
        return
    else:
        print()
        print("Opção inválida. Por favor, escolha 1, 2 ou 3.")

    main()

if __name__ == "__main__":
    main()