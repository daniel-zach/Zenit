from util import cores, limpar_terminal
from metas import criarmetas, listametas

def menu():
    """Exibe o menu principal"""
    opcao = ''

    limpar_terminal()

    while opcao != "0":
        print(cores.VERDE + "\nMenu Principal \n" + cores.NORMAL)
        print("[1] Gerenciar Metas")
        print("[2] Streak")
        print("[3] Monitoramento de Progresso")
        print("[0] Sair do Programa")
        opcao = input("Escolha uma opção: ").strip()
        limpar_terminal()
         
        if opcao == "1":
            menumetas()
        elif opcao == "2":
            print(f"{cores.AMARELO}Opção de streak em desenvolvimento{cores.NORMAL}")
        elif opcao == "3":
            print(f"{cores.AMARELO}Opção de metas em desenvolvimento{cores.NORMAL}")
        elif opcao != "0":
            print(cores.VERMELHO + "Opção não reconhecida!" + cores.NORMAL)
        else:
            print("Esperamos te ver amanhã!")
            break

def menumetas():
    opcao = ''
    while opcao != "0":
        print(cores.VERDE + "Gerenciar Metas \n" + cores.NORMAL)
        if not listametas:
            print("Nenhuma meta definida")
        else:
            print("Metas atuais:")
        for x in listametas:
            print(x)
        print("\n[C] Criar uma nova meta")
        print("[0] Voltar para o Menu Principal")
        opcao = input("Escolha uma opção: ").strip().lower()
        limpar_terminal()

        if opcao == "c":
            criarmetas()
        elif opcao != "0":
            print(cores.VERMELHO + "Opção não reconhecida!" + cores.NORMAL)
menu()