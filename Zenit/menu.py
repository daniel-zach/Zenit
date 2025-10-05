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
        opcao = input("Escolha uma opção: ")
        limpar_terminal()
         
        if opcao == "1":
            menumetas()
        elif opcao == "2":
            # TODO: fazer os outros menus
            return
        elif opcao == "3":
            return
        elif opcao == "0":
            # FIXME: resolver a questão que as vezes isso não funciona direito (fica preso no while ainda)
            print("Esperamos te ver amanhã!")
            return
        else:
            print(cores.VERMELHO + "Opção não reconhecida!" + cores.NORMAL)

def menumetas():
    opcao = ''
    while opcao != "0":
        print(cores.VERDE + "Gerenciar Metas \n" + cores.NORMAL)
        print("[C] Criar uma nova meta")
        for x in listametas:
            # TODO: listar tudo da lista de modo correto igual as outras opções
            # acho que é bom indexar uns numeros no dict também para poder escolher 
            # também deixar acessar um menu para todos as metas, incluindo o nome, a descrição, e opções para editar, remover
            # e marcar a meta como completo para o dia
            # é complexo, mais acho que vai valer a pena
            print(x)
        print("[0] Voltar para o Menu Principal")
        opcao = input("Escolha uma opção: ")
        limpar_terminal()

        if opcao == "c":
            criarmetas()
        if opcao == "0":
            menu()
        else:
            # FIXME: isso está sendo ativado após ir para o menu de criar metas
            print(cores.VERMELHO + "Opção não reconhecida!" + cores.NORMAL)
menu()