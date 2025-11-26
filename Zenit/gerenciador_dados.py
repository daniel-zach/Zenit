import json
import os
from datetime import datetime
from util import cores, Tempo

class GerenciadorDados:
    """
    Gerenciador centralizado de dados do sistema.
    Estrutura JSON hierárquica: usuários > metas > missões
    """
    
    def __init__(self, arquivo='dados.json'):
        self.arquivo = arquivo
        self.dados = self.carregar_dados()
    
    def carregar_dados(self):
        """Carrega dados do arquivo JSON"""
        if os.path.exists(self.arquivo):
            try:
                with open(self.arquivo, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}
    
    def salvar_dados(self):
        """Salva dados no arquivo JSON"""
        with open(self.arquivo, 'w', encoding='utf-8') as f:
            json.dump(self.dados, f, ensure_ascii=False, indent=4)
    
    # ============= OPERAÇÕES DE USUÁRIO ============
    
    def criar_usuario(self, username, nome_real, tempo_diario, tempo_label):
        """Cria um novo usuário"""
        if username in self.dados:
            return False, "Usuário já existe!"
        
        self.dados[username] = {
            "nome_real": nome_real,
            "tempo_diario": tempo_diario,
            "tempo_label": tempo_label,
            "data_criacao": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "streak": 0,
            "pontos":0,
            "metas": {}
        }
        self.salvar_dados()
        return True, "Usuário criado com sucesso!"
    
    def obter_usuario(self, username):
        """Retorna dados de um usuário específico"""
        return self.dados.get(username, None)
    
    def listar_usuarios(self):
        """Retorna lista de todos os usuários"""
        return self.dados
    
    def atualizar_usuario(self, username, nome_real=None, tempo_diario=None, tempo_label=None):
        """Atualiza informações de um usuário"""
        if username not in self.dados:
            return False, "Usuário não encontrado!"
        
        if nome_real is not None:
            self.dados[username]["nome_real"] = nome_real
        if tempo_diario is not None:
            self.dados[username]["tempo_diario"] = tempo_diario
        if tempo_label is not None:
            self.dados[username]["tempo_label"] = tempo_label
        
        self.salvar_dados()
        return True, "Usuário atualizado com sucesso!"
    
    def excluir_usuario(self, username):
        """Exclui um usuário e TODAS suas metas e missões"""
        if username not in self.dados:
            return False, "Usuário não encontrado!"
        
        del self.dados[username]
        self.salvar_dados()
        return True, f"Usuário '{username}' e todos seus dados excluídos!"
    
    # =========== OPERAÇÕES DE METAS ===============
    
    def criar_meta(self, username, nome, descricao=""):
        """Cria uma nova meta para um usuário"""
        if username not in self.dados:
            return False, "Usuário não encontrado!"
        
        metas = self.dados[username]["metas"]
        index = str(len(metas) + 1)
        
        metas[index] = {
            "nome": nome,
            "descricao": descricao,
            "index": index,
            "data_criacao": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "missoes": {}
        }
        
        self.salvar_dados()
        return True, f"Meta '{nome}' criada com sucesso!"
    
    def obter_meta(self, username, meta_index):
        """Retorna uma meta específica"""
        if username not in self.dados:
            return None
        if meta_index not in self.dados[username]["metas"]:
            return None
        return self.dados[username]["metas"][meta_index]
    
    def listar_metas(self, username):
        """Retorna todas as metas de um usuário"""
        if username not in self.dados:
            return {}
        return self.dados[username]["metas"]
    
    def atualizar_meta(self, username, meta_index, nome=None, descricao=None):
        """Atualiza informações de uma meta"""
        if username not in self.dados:
            return False, "Usuário não encontrado!"
        if meta_index not in self.dados[username]["metas"]:
            return False, "Meta não encontrada!"
        
        meta = self.dados[username]["metas"][meta_index]
        
        if nome is not None:
            meta["nome"] = nome
        if descricao is not None:
            meta["descricao"] = descricao
        
        self.salvar_dados()
        return True, "Meta atualizada com sucesso!"
    
    def excluir_meta(self, username, meta_index):
        """Exclui uma meta e TODAS suas missões"""
        if username not in self.dados:
            return False, "Usuário não encontrado!"
        if meta_index not in self.dados[username]["metas"]:
            return False, "Meta não encontrada!"
        
        nome_meta = self.dados[username]["metas"][meta_index]["nome"]
        del self.dados[username]["metas"][meta_index]
        self.salvar_dados()
        return True, f"Meta '{nome_meta}' excluída!"
    
    # ============= OPERAÇÕES DE MISSÃO ==============
    
    def criar_missao(self, username, meta_index, nome, dias_repeticao=1):
        """Cria uma nova missão para uma meta"""
        if username not in self.dados:
            return False, "Usuário não encontrado!"
        if meta_index not in self.dados[username]["metas"]:
            return False, "Meta não encontrada!"
        
        missoes = self.dados[username]["metas"][meta_index]["missoes"]
        index = str(len(missoes) + 1)
        data_pendente = Tempo.adicionar_dias((dias_repeticao))
        
        missoes[index] = {
            "nome": nome,
            "index": index,
            "completa": False,
            "frequencia": dias_repeticao,
            "data_criacao": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "data_pendente": data_pendente
        }
        
        self.salvar_dados()
        return True, f"Missão '{nome}' criada com sucesso!"
    
    def obter_missao(self, username, meta_index, missao_index):
        """Retorna uma missão específica"""
        if username not in self.dados:
            return None
        if meta_index not in self.dados[username]["metas"]:
            return None
        if missao_index not in self.dados[username]["metas"][meta_index]["missoes"]:
            return None
        return self.dados[username]["metas"][meta_index]["missoes"][missao_index]
    
    def listar_missoes(self, username, meta_index):
        """Retorna todas as missões de uma meta"""
        if username not in self.dados:
            return {}
        if meta_index not in self.dados[username]["metas"]:
            return {}
        return self.dados[username]["metas"][meta_index]["missoes"]
    
    def atualizar_missao(self, username, meta_index, missao_index, nome=None, status=None, frequencia=None):
        """Atualiza informações de uma missão"""
        if username not in self.dados:
            return False, "Usuário não encontrado!"
        if meta_index not in self.dados[username]["metas"]:
            return False, "Meta não encontrada!"
        if missao_index not in self.dados[username]["metas"][meta_index]["missoes"]:
            return False, "Missão não encontrada!"
        
        missao = self.dados[username]["metas"][meta_index]["missoes"][missao_index]
        
        if nome is not None:
            missao["nome"] = nome
        if status is not None:
            missao["completa"] = status
            if status:
                missao["data_conclusao"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        if frequencia is not None:
            missao["frequencia"] = frequencia
        
        self.salvar_dados()
        return True, "Missão atualizada com sucesso!"
    
    def excluir_missao(self, username, meta_index, missao_index):
        """Exclui uma missão"""
        if username not in self.dados:
            return False, "Usuário não encontrado!"
        if meta_index not in self.dados[username]["metas"]:
            return False, "Meta não encontrada!"
        if missao_index not in self.dados[username]["metas"][meta_index]["missoes"]:
            return False, "Missão não encontrada!"
        
        nome_missao = self.dados[username]["metas"][meta_index]["missoes"][missao_index]["nome"]
        del self.dados[username]["metas"][meta_index]["missoes"][missao_index]
        self.salvar_dados()
        return True, f"Missão '{nome_missao}' excluída!"
    
    # ============ UTILITÁRIOS ===============
    
    def resetar_missoes_diarias(self, username):
        """Reseta todas as missões completas de um usuário (para sistema de streak)"""
        if username not in self.dados:
            return False, "Usuário não encontrado!"
        
        contador = 0
        for meta_index in self.dados[username]["metas"]:
            for missao_index in self.dados[username]["metas"][meta_index]["missoes"]:
                missao = self.dados[username]["metas"][meta_index]["missoes"][missao_index]
                if missao["completa"]:
                    missao["completa"] = False
                    contador += 1
        
        if contador > 0:
            self.salvar_dados()
        else:
            return False, f"Missões já estão zeradas"
        
        return True, f"{contador} missões resetadas!"
    
    def obter_estatisticas(self, username):
        """Retorna estatísticas de um usuário"""
        if username not in self.dados:
            return None
        
        usuario = self.dados[username]
        total_metas = len(usuario["metas"])
        total_missoes = 0
        missoes_completas = 0
        
        for meta in usuario["metas"].values():
            total_missoes += len(meta["missoes"])
            for missao in meta["missoes"].values():
                if missao["completa"]:
                    missoes_completas += 1
        
        return {
            "total_metas": total_metas,
            "total_missoes": total_missoes,
            "missoes_completas": missoes_completas,
            "missoes_pendentes": total_missoes - missoes_completas,
            "taxa_conclusao": (missoes_completas / total_missoes * 100) if total_missoes > 0 else 0
        }


# Teste do sistema
if __name__ == "__main__":
    gd = GerenciadorDados()
    
    # Criar usuário
    sucesso, msg = gd.criar_usuario("jose", "José Silva", 1, "1 hora")
    print(msg)
    
    # Criar meta
    sucesso, msg = gd.criar_meta("jose", "Estudar Python", "Melhorar habilidades em programação")
    print(msg)
    
    # Criar missões
    gd.criar_missao("jose", "1", "Estudar listas")
    gd.criar_missao("jose", "1", "Estudar dicionários")
    gd.criar_missao("jose", "1", "Fazer exercícios")
    
    # Marcar missão como completa
    gd.atualizar_missao("jose", "1", "1", completa=True)
    
    # Estatísticas
    stats = gd.obter_estatisticas("jose")
    print(f"\nEstatísticas de João:")
    print(f"Metas: {stats['total_metas']}")
    print(f"Missões: {stats['total_missoes']}")
    print(f"Completas: {stats['missoes_completas']}")
    print(f"Taxa de conclusão: {stats['taxa_conclusao']:.1f}%")
    
    #sucesso, msg = gd.excluir_meta("jose", "1")
    #print(f"\n{msg}")