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
            "data_criacao": Tempo.agora(),
            "streak": 0,
            "pontos": 0,
            "ultima_missao_completa": None,
            "metas": {},
            "itens": {'defesa_ofensiva': 0}
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
    
    # ============= SISTEMA DE PONTOS ===============
    
    def adicionar_pontos(self, username, pontos):
        """Adiciona pontos ao usuário"""
        if username not in self.dados:
            return False, "Usuário não encontrado!"
        
        self.dados[username]["pontos"] = self.dados[username].get("pontos", 0) + pontos
        self.salvar_dados()
        return True, f"+{pontos} pontos!"
    
    def remover_pontos(self, username, pontos):
        """Remove pontos do usuário"""
        if username not in self.dados:
            return False, "Usuário não encontrado!"
        
        pontos_atuais = self.dados[username].get("pontos", 0)
        if pontos_atuais < pontos:
            return False, "Pontos insuficientes!"
        
        self.dados[username]["pontos"] = pontos_atuais - pontos
        self.salvar_dados()
        return True, f"-{pontos} pontos!"
    
    def obter_pontos(self, username):
        """Retorna pontos do usuário"""
        if username not in self.dados:
            return 0
        return self.dados[username].get("pontos", 0)
    
    # ============= SISTEMA DE ITENS ================
    
    def adicionar_item(self, username, item, quantidade=1):
        """Adiciona um item ao inventário do usuário"""
        if username not in self.dados:
            return False, "Usuário não encontrado!"
        
        if "itens" not in self.dados[username]:
            self.dados[username]["itens"] = {}
        
        itens = self.dados[username]["itens"]
        itens[item] = itens.get(item, 0) + quantidade
        
        self.salvar_dados()
        return True, f"+{quantidade} {item}!"
    
    def remover_item(self, username, item, quantidade=1):
        """Remove um item do inventário do usuário"""
        if username not in self.dados:
            return False, "Usuário não encontrado!"
        
        if "itens" not in self.dados[username]:
            return False, "Item não encontrado!"
        
        itens = self.dados[username]["itens"]
        quantidade_atual = itens.get(item, 0)
        
        if quantidade_atual < quantidade:
            return False, "Quantidade insuficiente!"
        
        itens[item] = quantidade_atual - quantidade
        self.salvar_dados()
        return True, f"-{quantidade} {item}!"
    
    def obter_quantidade_item(self, username, item):
        """Retorna quantidade de um item específico"""
        if username not in self.dados:
            return 0
        
        itens = self.dados[username].get("itens", {})
        return itens.get(item, 0)
    
    def obter_todos_itens(self, username):
        """Retorna todos os itens do usuário"""
        if username not in self.dados:
            return {}
        
        return self.dados[username].get("itens", {})
    
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
            "data_criacao": Tempo.agora(),
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
        
        missoes[index] = {
            "nome": nome,
            "index": index,
            "completa": False,
            "frequencia": int(dias_repeticao),
            "data_criacao": Tempo.agora(),
            "data_pendente": Tempo.agora()
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
    
    def listar_missoes_pendentes_hoje(self, username, meta_index):
        """Retorna apenas missões pendentes para hoje"""
        todas_missoes = self.listar_missoes(username, meta_index)
        
        missoes_hoje = {}
        for missao_id, missao in todas_missoes.items():
            data_pendente = missao.get('data_pendente')
            if not missao.get('completa', False) and data_pendente:
                if Tempo.e_hoje(data_pendente) or Tempo.e_antes_de_hoje(data_pendente):
                    missoes_hoje[missao_id] = missao
        
        return missoes_hoje
    
    def atualizar_missao(self, username, meta_index, missao_index, nome=None, completa=None, frequencia=None):
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
        
        if completa is not None:
            status_anterior = missao.get("completa", False)
            missao["completa"] = completa
            
            if completa and not status_anterior:
                # Missão foi marcada como completa
                missao["data_conclusao"] = Tempo.agora()
                
                # Atualiza data_pendente para próxima ocorrência
                frequencia = missao.get("frequencia", 1)
                missao["data_pendente"] = Tempo.adicionar_dias(frequencia)
                
                # Calcula pontos: 10 + (5 * horas da meta)
                tempo_diario = self.dados[username].get("tempo_diario", 1)
                pontos_ganhos = 10 + int(5 * tempo_diario)
                self.adicionar_pontos(username, pontos_ganhos)
                
                # Atualiza streak
                self._atualizar_streak(username)
                
            elif not completa and status_anterior:
                # Missão foi desmarcada
                if "data_conclusao" in missao:
                    del missao["data_conclusao"]
        
        if frequencia is not None:
            missao["frequencia"] = int(frequencia)
        
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
    
    # ============ SISTEMA DE STREAKS ===============
    
    def _atualizar_streak(self, username):
        """Atualiza o streak quando uma missão é concluída"""
        if username not in self.dados:
            return
        
        usuario = self.dados[username]
        ultima_conclusao = usuario.get("ultima_missao_completa")
        
        if ultima_conclusao is None:
            usuario["streak"] = 1
            usuario["ultima_missao_completa"] = Tempo.hoje()
        elif Tempo.e_hoje(ultima_conclusao):
            pass
        elif Tempo.foi_ontem(ultima_conclusao):
            usuario["streak"] += 1
            usuario["ultima_missao_completa"] = Tempo.hoje()
        else:
            usuario["streak"] = 1
            usuario["ultima_missao_completa"] = Tempo.hoje()
        
        self.salvar_dados()
    
    def verificar_e_resetar_streak(self, username):
        """Verifica se o streak deve ser resetado"""
        if username not in self.dados:
            return False
        
        usuario = self.dados[username]
        ultima_conclusao = usuario.get("ultima_missao_completa")
        
        if ultima_conclusao is None:
            return False
        
        if Tempo.e_hoje(ultima_conclusao) or Tempo.foi_ontem(ultima_conclusao):
            return False
        
        # Verifica se tem defesa ofensiva
        defesas = self.obter_quantidade_item(username, 'defesa_ofensiva')
        if defesas > 0:
            # Usa uma defesa
            self.remover_item(username, 'defesa_ofensiva', 1)
            print(f"\n{cores.AZUL}🛡️ Defesa de Ofensiva usada! Seu streak foi protegido.{cores.NORMAL}")
            print(f"{cores.AMARELO}Defesas restantes: {defesas - 1}{cores.NORMAL}")
            return False
        
        # Quebrou o streak
        usuario["streak"] = 0
        self.salvar_dados()
        return True
    
    def verificar_e_resetar_missoes(self, username):
        """Verifica e reseta missões que chegaram na data de repetição"""
        if username not in self.dados:
            return 0
        
        contador_resetadas = 0
        
        for meta_id in self.dados[username]["metas"]:
            for missao_id in self.dados[username]["metas"][meta_id]["missoes"]:
                missao = self.dados[username]["metas"][meta_id]["missoes"][missao_id]
                
                if not missao.get("completa", False):
                    continue
                
                data_pendente = missao.get("data_pendente")
                if data_pendente and (Tempo.e_hoje(data_pendente) or Tempo.e_antes_de_hoje(data_pendente)):
                    missao["completa"] = False
                    frequencia = missao.get("frequencia", 1)
                    missao["data_pendente"] = Tempo.adicionar_dias(frequencia)
                    
                    if "data_conclusao" in missao:
                        del missao["data_conclusao"]
                    
                    contador_resetadas += 1
        
        if contador_resetadas > 0:
            self.salvar_dados()
        
        return contador_resetadas
    
    # ============ UTILITÁRIOS ===============
    
    def obter_estatisticas(self, username):
        """Retorna estatísticas de um usuário"""
        if username not in self.dados:
            return None
        
        usuario = self.dados[username]
        total_metas = len(usuario["metas"])
        total_missoes = 0
        missoes_completas = 0
        missoes_pendentes_hoje = 0
        missoes_completas_hoje = 0
        total_missoes_hoje = 0
        
        for meta in usuario["metas"].values():
            total_missoes += len(meta["missoes"])
            for missao in meta["missoes"].values():
                data_pendente = missao.get('data_pendente')
                
                if missao["completa"]:
                    missoes_completas += 1
                
                if data_pendente and (Tempo.e_hoje(data_pendente) or Tempo.e_antes_de_hoje(data_pendente)):
                    total_missoes_hoje += 1
                    
                    if missao["completa"]:
                        missoes_completas_hoje += 1
                    else:
                        missoes_pendentes_hoje += 1
        
        return {
            "total_metas": total_metas,
            "total_missoes": total_missoes,
            "missoes_completas": missoes_completas,
            "missoes_pendentes": total_missoes - missoes_completas,
            "missoes_pendentes_hoje": missoes_pendentes_hoje,
            "missoes_completas_hoje": missoes_completas_hoje,
            "total_missoes_hoje": total_missoes_hoje,
            "taxa_conclusao": (missoes_completas_hoje / total_missoes_hoje * 100) if total_missoes_hoje > 0 else 0,
            "streak": usuario.get("streak", 0),
            "ultima_missao": usuario.get("ultima_missao_completa")
        }