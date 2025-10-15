import os

class cores:
    # utilização das cores, sempre voltar ao normal depois de usar uma cor
    # se não, tudo vai ficar na cor que você escolheu
    NORMAL = "\x1b[39m"
    VERMELHO = "\x1b[31m"
    VERDE = "\x1b[32m"
    AMARELO = "\x1b[33m"
    AZUL = "\x1b[34m"

def limpar_terminal():
    # já que linux e windows usa comandos diferentes para limpar a tela,
    # nós vemos qual sistema operacional o usuario está utilizando
    if os.name == "nt":
        _ = os.system("cls")
    else:
        _ = os.system("clear")