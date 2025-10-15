from util import limpar_terminal
listametas = dict()

# falta muita coisa aqui ainda mas essa é a base
# escolha o nome, a descrição da meta (talvez depois a dificuldade e o tempo? vamos ver)
# e estará adicionada a lista
# FIXME: não é bloqueado a criação de metas com o mesmo nome, mas trás resultados não desejados.
# deve ser criado o bloqueio para apenas metas com o mesmo nome serem criados
def criarmetas():
    limpar_terminal()
    nome = input("Defina o nome da meta: ")
    descricao = input("Defina a descrição da meta: ")
    index = len(listametas) + 1
    novameta = {
        "nome": nome,
        "descrição": descricao,
        "index": index
    }
    listametas.update({str(index) : novameta})
    limpar_terminal()
    print(listametas) # só por questões de teste