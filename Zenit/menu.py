from util import cores, limpar_terminal
from metas import criarmetas, listametas, criarmissao

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
        print("[1] Missões")
        print("[2] Editar meta")
        print("[3] Excluir meta")
        print("[0] Voltar ao menu de metas")
        opcao = input("Escolha uma opção: ")
        limpar_terminal()

        if opcao == "1":
            menumissoes(index)
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

def menumissoes(index):
    opcao = ''
    while opcao != "0":
        print("Missões de " + listametas[index]["nome"] + "\n")
        print("[C] Criar uma nova missão")
        for i in listametas[index]['missoes']:
            print("[" + str(listametas[index]['missoes'][i]['index']) + "] " + str(listametas[index]['missoes'][i]['nome']))
        print("[0] Voltar ao menu da meta " + listametas[index]["nome"])
        opcao = input("Escolha uma opção: ")
        limpar_terminal()
        if opcao.casefold() == "c":
            criarmissao(index)
        elif opcao == "0":
            return
        else:
            if opcao in listametas[index]['missoes']:
                menuvizualizarmissao(index, opcao)
            else:
                print(cores.VERMELHO + "Opção não reconhecida!" + cores.NORMAL)

def menuvizualizarmissao(metaindex, missaoindex):
    opcao = ''
    while opcao != "0":
        print("Nome da missão: " + listametas[metaindex]['missoes'][missaoindex]["nome"])
        print("[1] Marcar como completa")
        print("[2] Editar missão")
        print("[3] Excluir missão")
        print("[0] Voltar ao menu de missões")
        opcao = input("Escolha uma opção: ")
        limpar_terminal()

        if opcao == "1":
            listametas[metaindex]['missoes'][missaoindex]["completa"] = True
            # TODO: integrar com o sistema de streaks, resetar isso para false em 24 horas
        elif opcao == "2":
                x = input("Define o nome da meta: ")
                listametas[metaindex]['missoes'][missaoindex]["nome"] = x
                limpar_terminal()
        elif opcao == "3":
            listametas[metaindex]['missoes'].pop(missaoindex)
            return
        elif opcao == "0":
            return
        else:
            print(cores.VERMELHO + "Opção não reconhecida!" + cores.NORMAL)

menu()