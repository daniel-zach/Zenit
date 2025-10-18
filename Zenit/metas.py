from util import limpar_terminal
listametas = dict()

def criarmetas():
    limpar_terminal()
    nome = input("Defina o nome da meta: ")
    if not nome:
        criarmetas()
        return
    descricao = input("Defina a descrição da meta: ")
    index = len(listametas) + 1
    novameta = {
        "nome": nome,
        "descrição": descricao,
        "index": index,
        "missoes": {}
    }
    listametas.update({str(index) : novameta})
    limpar_terminal()

def criarmissao(x):
    limpar_terminal()
    nome = input("Defina o nome da missão: ")
    if not nome:
        criarmissao(x)
        return
    index = len(listametas[x]["missoes"]) + 1
    novamissao = {
        "nome": nome,
        "index": index,
        "completa": False
    }
    listametas[x]["missoes"].update({str(index) : novamissao})
    limpar_terminal()