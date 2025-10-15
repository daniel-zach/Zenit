import json
import os
from datetime import datetime
from util import cores, limpar_terminal

class GerenciadorUsuarios:
    def __init__(self, arquivo='usuarios.json'):
        self.arquivo = arquivo
        self.usuarios = self.carregar_usuarios()
    
    def carregar_usuarios(self):
        """Carrega usuários do arquivo JSON"""
        if os.path.exists(self.arquivo):
            try:
                with open(self.arquivo, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}
    
    def salvar_usuarios(self):
        """Salva usuários no arquivo JSON"""
        with open(self.arquivo, 'w', encoding='utf-8') as f:
            json.dump(self.usuarios, f, ensure_ascii=False, indent=4)
    
    def criar_usuario(self):
        """Cria um novo usuário"""
        print("\n=== CRIAR NOVO USUÁRIO ===")
        
        # Nome de usuário
        while True:
            username = input("Nome de usuário: ").strip()
            if not username:
                print("Nome de usuário não pode ser vazio!")
                continue
            if " " in username:
                print("Nome de usuário não poder conter espaços!")
                continue
            if len(username) <3:
                print("Nome de usuário deve conter pelo menos 3 caracteres!")
                continue
            if username in self.usuarios:
                print("Nome de usuário já existe!")
                continue
            break
        
        # Nome real
        nome_real = input("Insira seu nome: ").strip()
        if not nome_real:
            nome_real = username
        
        # Tempo dedicado
        print("\nQuanto tempo você quer dedicar por dia?")
        print("1. 10 minutos")
        print("2. 15 minutos")
        print("3. 30 minutos")
        print("4. 1 hora")
        print("5. 2 horas ou mais")
        
        opcoes_tempo = {
            '1': 10/60,  # 10 minutos em horas
            '2': 15/60,  # 15 minutos em horas
            '3': 30/60,  # 30 minutos em horas
            '4': 1,    # 1 hora
            '5': 2    # 2 horas
        }
        
        tempo_labels = {
            '1': '10 minutos',
            '2': '15 minutos',
            '3': '30 minutos',
            '4': '1 hora',
            '5': '2 horas ou mais'
        }
        
        while True:
            opcao_tempo = input("Opção: ").strip()
            if opcao_tempo in opcoes_tempo:
                tempo_horas = opcoes_tempo[opcao_tempo]
                tempo_label = tempo_labels[opcao_tempo]
                break
            else:
                print("Opção inválida! Escolha entre 1 e 5.")
        
        # Criar usuário
        self.usuarios[username] = {
            "nome_real": nome_real,
            "tempo_diario": tempo_horas,
            "tempo_label": tempo_label,
            "data_criacao": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }
        
        self.salvar_usuarios()
        print(f"\nUsuário '{username}' criado com sucesso!")
    
    def listar_usuarios(self):
        """Lista todos os usuários"""
        if not self.usuarios:
            print("\nNenhum usuário cadastrado.")
            return
        
        print("\n=== USUÁRIOS CADASTRADOS ===")
        for username, dados in self.usuarios.items():
            print(f"\nUsername: {username}")
            print(f"  Nome: {dados['nome_real']}")
            print(f"  Tempo diário: {dados.get('tempo_label', str(dados['tempo_diario']) + ' horas')}")
            print(f"  Criado em: {dados['data_criacao']}")
    
    def visualizar_usuario(self):
        """Visualiza detalhes de um usuário específico"""
        if not self.usuarios:
            print("\nNenhum usuário cadastrado.")
            return
        
        username = input("\nDigite o nome de usuario: ").strip()
        
        if username not in self.usuarios:
            print(f"Usuário '{username}' não encontrado.")
            return
        
        dados = self.usuarios[username]
        print(f"\n=== PERFIL: {username} ===")
        print(f"Nome: {dados['nome_real']}")
        print(f"Tempo diário: {dados.get('tempo_label', str(dados['tempo_diario']) + ' horas')}")
        print(f"Criado em: {dados['data_criacao']}")
    
    def editar_usuario(self):
        """Edita informações de um usuário"""
        if not self.usuarios:
            print("\nNenhum usuário cadastrado.")
            return
        
        username = input("\nDigite o nome de usuário para editar: ").strip()
        
        if username not in self.usuarios:
            print(f"Usuário '{username}' não encontrado.")
            return
        
        dados = self.usuarios[username]
        print(f"\n=== EDITANDO: {username} ===")
        
        # Editar nome real
        novo_nome = input(f"Nome [{dados['nome_real']}]: ").strip()
        if novo_nome:
            dados['nome_real'] = novo_nome
        
        # Editar tempo diário
        while True:
            novo_tempo = input(f"Tempo diário em horas [{dados['tempo_diario']}]: ").strip()
            if not novo_tempo:
                break
            try:
                tempo_horas = float(novo_tempo)
                if tempo_horas <= 0:
                    print("O tempo deve ser maior que zero!")
                    continue
                dados['tempo_diario'] = tempo_horas
                break
            except ValueError:
                print("Por favor, digite um número válido!")
        
        self.salvar_usuarios()
        print(f"\nUsuário '{username}' atualizado com sucesso!")
    
    def excluir_usuario(self):
        """Exclui um usuário"""
        if not self.usuarios:
            print("\nNenhum usuário cadastrado.")
            return
        
        username = input("\nDigite o nome de usuário para excluir: ").strip()
        
        if username not in self.usuarios:
            print(f"Usuario '{username}' nao encontrado.")
            return
        
        confirma = input(f"Tem certeza que deseja excluir '{username}'? (s/n): ").strip().lower()
        
        if confirma == 's':
            del self.usuarios[username]
            self.salvar_usuarios()
            print(f"Usuário '{username}' excluído com sucesso!")
        else:
            print("Operação cancelada.")
    
    def menu_principal(self):
        """Exibe o menu principal dos usuários"""
        while True:
            print("\n" + "="*40)
            print("  SISTEMA DE GERENCIAMENTO DE USUÁRIOS")
            print("="*40)
            print("1. Criar novo usuário")
            print("2. Listar usuários")
            print("3. Visualizar usuário")
            print("4. Editar usuário")
            print("5. Excluir usuário")
            print("0. Sair")
            print("="*40)
            
            opcao = input("Escolha uma opção: ").strip()
            
            if opcao == '1':
                self.criar_usuario()
            elif opcao == '2':
                self.listar_usuarios()
            elif opcao == '3':
                self.visualizar_usuario()
            elif opcao == '4':
                self.editar_usuario()
            elif opcao == '5':
                self.excluir_usuario()
            elif opcao == '0':
                print("\nAté logo!")
                break
            else:
                print("\nOpcao inválida! Tente novamente.")

if __name__ == "__main__":
    gerenciador = GerenciadorUsuarios()
    gerenciador.menu_principal()