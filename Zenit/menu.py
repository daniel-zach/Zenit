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
            # TODO: fazer os outros menus
            print(f"{cores.AMARELO}Opção de streak em desenvolvimento{cores.NORMAL}")
        elif opcao == "3":
            print(f"{cores.AMARELO}Opção de metas em desenvolvimento{cores.NORMAL}")
        elif opcao != "0":
            print(cores.VERMELHO + "Opção não reconhecida!" + cores.NORMAL)
        else:
            #BUG FIX: estava tendo que fechar o menu duas vezes porque menumetas() criava um segundo menu, corrigi deixando o loop apenas ser fechado sem criar um novo menu
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
            # TODO: listar tudo da lista de modo correto igual  as outras opções
            # acho que é bom indexar uns numeros no dict também para poder escolher 
            # também deixar acessar um menu para todos as metas, incluindo o nome, a descrição, e opções para editar, remover
            # e marcar a meta como completo para o dia

            # Recomendo criar a classe de "metas" para facilitar
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