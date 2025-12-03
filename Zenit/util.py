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
    """Classe para gerenciar operações de data e tempo"""
    
    @staticmethod
    def agora():
        """Retorna a data/hora atual como string formatada"""
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    @staticmethod
    def hoje():
        """Retorna apenas a data atual (sem hora)"""
        return datetime.now().strftime("%d/%m/%Y")
    
    @staticmethod
    def adicionar_dias(dias=1, comeco=None):
        """Retorna uma data somada à X dias."""
        if comeco is None:
            comeco = datetime.now()
        elif isinstance(comeco, str):
            # Converte string para datetime
            comeco = Tempo.string_para_datetime(comeco)
        
        return (comeco + timedelta(days=int(dias))).strftime("%d/%m/%Y %H:%M:%S")
    
    @staticmethod
    def string_para_datetime(data_str):
        """Converte string de data para objeto datetime"""
        try:
            # Tenta com hora
            return datetime.strptime(data_str, "%d/%m/%Y %H:%M:%S")
        except ValueError:
            try:
                # Tenta sem hora
                return datetime.strptime(data_str, "%d/%m/%Y")
            except ValueError:
                return None
    
    @staticmethod
    def extrair_data(data_str):
        """Extrai apenas a parte da data (dd/mm/yyyy) de uma string"""
        if not data_str:
            return None
        return data_str.split()[0] if ' ' in data_str else data_str
    
    @staticmethod
    def e_hoje(data_str):
        """Verifica se uma data string é hoje"""
        if not data_str:
            return False
        
        data_comparar = Tempo.extrair_data(data_str)
        data_hoje = Tempo.hoje()
        
        return data_comparar == data_hoje
    
    @staticmethod
    def e_antes_de_hoje(data_str):
        """Verifica se uma data é anterior a hoje"""
        if not data_str:
            return False
        
        data_obj = Tempo.string_para_datetime(data_str)
        if not data_obj:
            return False
        
        hoje_obj = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        data_obj = data_obj.replace(hour=0, minute=0, second=0, microsecond=0)
        
        return data_obj < hoje_obj
    
    @staticmethod
    def e_depois_de_hoje(data_str):
        """Verifica se uma data é posterior a hoje"""
        if not data_str:
            return False
        
        data_obj = Tempo.string_para_datetime(data_str)
        if not data_obj:
            return False
        
        hoje_obj = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        data_obj = data_obj.replace(hour=0, minute=0, second=0, microsecond=0)
        
        return data_obj > hoje_obj
    
    @staticmethod
    def diferenca_dias(data1_str, data2_str=None):
        """Calcula a diferença em dias entre duas datas (data1 - data2)"""
        if data2_str is None:
            data2_str = Tempo.agora()
        
        data1 = Tempo.string_para_datetime(data1_str)
        data2 = Tempo.string_para_datetime(data2_str)
        
        if not data1 or not data2:
            return None
        
        # Remove a parte de hora para comparar apenas datas
        data1 = data1.replace(hour=0, minute=0, second=0, microsecond=0)
        data2 = data2.replace(hour=0, minute=0, second=0, microsecond=0)
        
        diferenca = (data1 - data2).days
        return diferenca
    
    @staticmethod
    def foi_ontem(data_str):
        """Verifica se uma data foi ontem"""
        diferenca = Tempo.diferenca_dias(data_str)
        return diferenca == -1
    
    @staticmethod
    def formatar_tempo_relativo(data_str):
        """Retorna uma descrição compreensível do tempo relativo"""
        if Tempo.e_hoje(data_str):
            return "Hoje"
        elif Tempo.foi_ontem(data_str):
            return "Ontem"
        
        diferenca = Tempo.diferenca_dias(data_str)
        
        if diferenca is None:
            return "Data inválida"
        elif diferenca < 0:
            return f"Há {abs(diferenca)} dia(s)"
        else:
            return f"Em {diferenca} dia(s)"