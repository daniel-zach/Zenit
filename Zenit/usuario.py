from util import cores, limpar_terminal
from gerenciador_dados import GerenciadorDados

class GerenciadorUsuarios:
    def __init__(self):
        self.gd = GerenciadorDados()
    
    def criar_usuario(self):
        """Cria um novo usuário"""
        limpar_terminal()
        print("\n=== CRIAR NOVO USUÁRIO ===")
        
        # Nome de usuário
        while True:
            username = input("Nome de usuário: ").strip().lower()
            if not username:
                print("Nome de usuário não pode ser vazio!")
                continue
            if " " in username:
                print("Nome de usuário não pode conter espaços!")
                continue
            if len(username) < 3:
                print("Nome de usuário deve conter pelo menos 3 caracteres!")
                continue
            if self.gd.obter_usuario(username):
                print("Nome de usuário já existe!")
                continue
            break
        
        # Nome real
        nome_real = input("Insira seu nome: ").strip()
        if not nome_real:
            nome_real = username
        
        # Tempo dedicado
        print("\nQuanto tempo você quer dedicar por dia?")
        print("[1] 10 minutos")
        print("[2] 15 minutos")
        print("[3] 30 minutos")
        print("[4] 1 hora")
        print("[5] 2 horas ou mais")
        
        opcoes_tempo = {
            '1': 10/60,
            '2': 15/60,
            '3': 30/60,
            '4': 1,
            '5': 2
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
        
        # Criar usuário usando o GerenciadorDados
        sucesso, msg = self.gd.criar_usuario(username, nome_real, tempo_horas, tempo_label)
        print(f"\n{cores.VERDE if sucesso else cores.VERMELHO}{msg}{cores.NORMAL}")
        
        return username if sucesso else None
    
    def listar_usuarios(self):
        """Lista todos os usuários"""
        limpar_terminal()
        usuarios = self.gd.listar_usuarios()
        
        if not usuarios:
            print("\nNenhum usuário cadastrado.")
            return
        
        print("\n=== USUÁRIOS CADASTRADOS ===")
        for username, dados in usuarios.items():
            print(f"\nUsername: {username}")
            print(f"  Nome: {dados['nome_real']}")
            print(f"  Tempo diário: {dados.get('tempo_label', str(dados['tempo_diario']) + ' horas')}")
            print(f"  Criado em: {dados['data_criacao']}")
            print(f"  Metas cadastradas: {len(dados.get('metas', {}))}")
    
    def visualizar_usuario(self):
        """Visualiza detalhes de um usuário específico"""
        limpar_terminal()
        usuarios = self.gd.listar_usuarios()
        
        if not usuarios:
            print("\nNenhum usuário cadastrado.")
            return
        
        username = input("\nDigite o nome de usuário: ").strip().lower()
        dados = self.gd.obter_usuario(username)
        
        if not dados:
            print(f"{cores.VERMELHO}Usuário '{username}' não encontrado.{cores.NORMAL}")
            return
        
        # Obter estatísticas
        stats = self.gd.obter_estatisticas(username)
        
        print(f"\n=== PERFIL: {username} ===")
        print(f"Nome: {dados['nome_real']}")
        print(f"Tempo diário: {dados.get('tempo_label', str(dados['tempo_diario']) + ' horas')}")
        print(f"Criado em: {dados['data_criacao']}")
        print(f"\n--- Estatísticas ---")
        print(f"Metas: {stats['total_metas']}")
        print(f"Missões totais: {stats['total_missoes']}")
        print(f"Missões completas: {stats['missoes_completas']}")
        print(f"Missões pendentes: {stats['missoes_pendentes']}")
        if stats['total_missoes'] > 0:
            print(f"Taxa de conclusão: {stats['taxa_conclusao']:.1f}%")
    
    def editar_usuario(self):
        """Edita informações de um usuário"""
        limpar_terminal()
        usuarios = self.gd.listar_usuarios()
        
        if not usuarios:
            print("\nNenhum usuário cadastrado.")
            return
        
        username = input("\nDigite o nome de usuário para editar: ").strip().lower()
        dados = self.gd.obter_usuario(username)
        
        if not dados:
            print(f"{cores.VERMELHO}Usuário '{username}' não encontrado.{cores.NORMAL}")
            return
        
        print(f"\n=== EDITANDO: {username} ===")
        
        # Editar nome real
        novo_nome = input(f"Nome [{dados['nome_real']}]: ").strip()
        nome_final = novo_nome if novo_nome else None
        
        # Editar tempo diário
        tempo_final = None
        tempo_label_final = None
        
        print("\nDeseja alterar o tempo diário? (s/n): ", end="")
        if input().strip().lower() == 's':
            print("\nQuanto tempo você quer dedicar por dia?")
            print("[1] 10 minutos")
            print("[2] 15 minutos")
            print("[3] 30 minutos")
            print("[4] 1 hora")
            print("[5] 2 horas ou mais")
            
            opcoes_tempo = {
                '1': (10/60, '10 minutos'),
                '2': (15/60, '15 minutos'),
                '3': (30/60, '30 minutos'),
                '4': (1, '1 hora'),
                '5': (2, '2 horas ou mais')
            }
            
            opcao = input("Opção: ").strip()
            if opcao in opcoes_tempo:
                tempo_final, tempo_label_final = opcoes_tempo[opcao]
        
        # Atualizar no GerenciadorDados
        sucesso, msg = self.gd.atualizar_usuario(
            username, 
            nome_real=nome_final,
            tempo_diario=tempo_final,
            tempo_label=tempo_label_final
        )
        
        print(f"\n{cores.VERDE if sucesso else cores.VERMELHO}{msg}{cores.NORMAL}")
    
    def excluir_usuario(self):
        """Exclui um usuário"""
        limpar_terminal()
        usuarios = self.gd.listar_usuarios()
        
        if not usuarios:
            print("\nNenhum usuário cadastrado.")
            return
        
        username = input("\nDigite o nome de usuário para excluir: ").strip().lower()
        
        if not self.gd.obter_usuario(username):
            print(f"{cores.VERMELHO}Usuário '{username}' não encontrado.{cores.NORMAL}")
            return
        
        # Mostrar quantas metas/missões serão perdidas
        stats = self.gd.obter_estatisticas(username)
        print(f"\n{cores.AMARELO}ATENÇÃO: Isso excluirá:{cores.NORMAL}")
        print(f"  - {stats['total_metas']} meta(s)")
        print(f"  - {stats['total_missoes']} missão(ões)")
        
        confirma = input(f"\nTem certeza que deseja excluir '{username}'? (s/n): ").strip().lower()
        
        if confirma == 's':
            sucesso, msg = self.gd.excluir_usuario(username)
            print(f"\n{cores.VERDE if sucesso else cores.VERMELHO}{msg}{cores.NORMAL}")
        else:
            print(f"{cores.AMARELO}Operação cancelada.{cores.NORMAL}")
    
    def menu_principal(self, limpar_proxima=True):
        """Exibe o menu principal dos usuários"""
        while True:
            if limpar_proxima:
                limpar_terminal()
            print("\n" + "="*40)
            print("  SISTEMA DE GERENCIAMENTO DE USUÁRIOS")
            print("="*40)
            print("[1] Criar novo usuário")
            print("[2] Listar usuários")
            print("[3] Visualizar usuário")
            print("[4] Editar usuário")
            print("[5] Excluir usuário")
            print("[0] Sair")
            print("="*40)
            
            opcao = input("Escolha uma opção: ").strip()
            
            if opcao == '1':
                limpar_terminal()
                self.criar_usuario()
                limpar_proxima = True
            elif opcao == '2':
                limpar_terminal()
                self.listar_usuarios()
                limpar_proxima = False
            elif opcao == '3':
                limpar_terminal()
                self.visualizar_usuario()
                limpar_proxima = False
            elif opcao == '4':
                limpar_terminal()
                self.editar_usuario()
                limpar_proxima = False
            elif opcao == '5':
                limpar_terminal()
                self.excluir_usuario()
                limpar_proxima = False
            elif opcao == '0':
                print("\nAté logo!")
                break
            else:
                limpar_terminal()
                print("\nOpção inválida! Tente novamente.")
                limpar_proxima = False

if __name__ == "__main__":
    gerenciador = GerenciadorUsuarios()
    gerenciador.menu_principal()