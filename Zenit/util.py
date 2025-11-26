import os
from datetime import datetime, timedelta

class cores:
    NORMAL = "\x1b[39m"
    VERMELHO = "\x1b[31m"
    VERDE = "\x1b[32m"
    AMARELO = "\x1b[33m"
    AZUL = "\x1b[34m"

def limpar_terminal():
    # já que linux e windows usam comandos diferentes para limpar a tela,
    # nós vemos qual sistema operacional o usuario está utilizando
    if os.name == "nt":
        _ = os.system("cls")
    else:
        _ = os.system("clear")

def enter_continuar():
    input("\nPressione Enter para continuar...")

class Tempo:
    def __init__(self):
        pass

    def adicionar_dias(self, dias=1, comeco=None):
        """Retorna uma data somada à X dias."""
        if comeco is None:
            comeco = datetime.now()
        return (comeco + timedelta(days=dias)).strftime("%d/%m/%Y %H:%M:%S")
    
    def checar_datas(self, data_p_checar, data):
        pass