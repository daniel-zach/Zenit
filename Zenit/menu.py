from util import cores, limpar_terminal
from metas import criarmetas, listametas

def menu():
    opcao = ''
    while opcao != "0":
        print(cores.VERDE + "Menu Principal \n" + cores.NORMAL)
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
            return
        elif opcao == "0":
            print("Esperamos te ver amanhã!")
        else:
            print(cores.VERMELHO + "Opção não reconhecida!" + cores.NORMAL)

def menumetas():
    opcao = ''
    while opcao != "0":
        print(cores.VERDE + "Gerenciar Metas \n" + cores.NORMAL)
        print("[C] Criar uma nova meta")
        for x in listametas:
            # TODO: deixar acessar um menu para todos as metas, incluindo o nome, a descrição, e opções para editar, remover
            # e poder marcar a meta como completo para o dia
            print("[" + str(listametas[x]['index']) + "] " + str(listametas[x]['nome']))
        print("[0] Voltar para o Menu Principal")
        opcao = input("Escolha uma opção: ").strip().lower()
        limpar_terminal()

        if opcao.casefold() == "c":
            criarmetas()
        elif opcao == "0":
            return
        else:
            if opcao in listametas:
                menuvizualizarmeta(opcao)
            else:
                print(cores.VERMELHO + "Opção não reconhecida!" + cores.NORMAL)

def menuvizualizarmeta(index):
    opcao = ''
    while opcao != "0":
        print("Nome da meta: " + listametas[index]["nome"])
        print("Descrição da meta: " + listametas[index]["descrição"] + "\n")
        print("[1] Marcar como completa")
        print("[2] Editar meta")
        print("[3] Excluir meta")
        print("[0] Voltar ao menu metas")
        opcao = input("Escolha uma opção: ")
        limpar_terminal()

        if opcao == "1":
            # TODO: funcionalidade de marcar como completa
            return
        elif opcao == "2":
            opcao = input("Editar nome ou descrição? ")
            if opcao.casefold() == "nome":
                x = input("Define o nome da meta: ")
                listametas[index]["nome"] = x
            elif opcao.casefold() == "descrição":
                x = input("Define a descrição da meta: ")
                listametas[index]["descrição"] = x
            else:
                print(cores.VERMELHO + "Opção não reconhecida!" + cores.NORMAL)
            limpar_terminal()
            
        elif opcao == "3":
            listametas.pop(index)
            return
        elif opcao == "0":
            return
        else:
            print(cores.VERMELHO + "Opção não reconhecida!" + cores.NORMAL)

menu()