from util import limpar_terminal
listametas = {}

def criarmetas():
    limpar_terminal()
    nome = input("Defina o nome da meta: ")
    descricao = input("Defina a descrição da meta: ")
    novameta = {
        "nome": nome,
        "descrição": descricao
    }
    listametas.update({str(nome) : novameta})
    limpar_terminal()