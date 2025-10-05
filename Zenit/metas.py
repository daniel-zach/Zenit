from util import limpar_terminal
listametas = {}

# falta muita coisa aqui ainda mas essa é a base
# escolha o nome, a descrição da meta (talvez depois a dificuldade e o tempo? vamos ver)
# e estará adicionada a lista
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