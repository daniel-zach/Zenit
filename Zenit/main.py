import json
import os
from util import cores, limpar_terminal
from metas import MenuMetas
from usuario import GerenciadorUsuarios

# BUG o terminal não está limpando corretamente
# BUG as missoes depois de carregadas não estão sendo atualizadas, precisa reiniciar o menu

class SistemaMain:
    def __init__(self):
        self.arquivo_config = 'config.json'
        self.gerenciador_usuarios = GerenciadorUsuarios()
        self.usuario_atual = self.carregar_usuario_atual()
        self.menu_metas = None
    
    def carregar_usuario_atual(self):
        """Carrega o usuário atualmente selecionado do arquivo de configuração"""
        if os.path.exists(self.arquivo_config):
            try:
                with open(self.arquivo_config, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    return config.get('usuario_atual', None)
            except json.JSONDecodeError:
                return None
        return None
    
    def salvar_usuario_atual(self, username):
        """Salva o usuário atual no arquivo de configuração"""
        config = {'usuario_atual': username}
        with open(self.arquivo_config, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=4)
        self.usuario_atual = username
        # Atualiza o menu de metas com o novo usuário
        self.menu_metas = MenuMetas(username)
    
    def limpar_usuario_atual(self):
        """Remove o usuário atual da configuração"""
        if os.path.exists(self.arquivo_config):
            os.remove(self.arquivo_config)
        self.usuario_atual = None
        self.menu_metas = None
    
    def selecionar_usuario(self):
        """Permite selecionar um usuário existente"""
        limpar_terminal()
        
        usuarios = self.gerenciador_usuarios.gd.listar_usuarios()
        if not usuarios:
            print(cores.AMARELO + "Nenhum usuário cadastrado ainda." + cores.NORMAL)
            input("\nPressione Enter para continuar...")
            return False
        
        print(cores.VERDE + "=== SELECIONAR USUÁRIO ===" + cores.NORMAL)
        
        while True:
            username = input("\nDigite o nome de usuário (ou '0' para voltar): ").strip().lower()
            
            if username == '0':
                return False
            
            if username in usuarios:
                self.salvar_usuario_atual(username)
                dados = usuarios[username]
                print(cores.VERDE + f"\nUsuário '{dados['nome_real']}' (@{username}) selecionado!" + cores.NORMAL)
                input("\nPressione Enter para continuar...")
                return True
            else:
                print(cores.VERMELHO + f"Usuário '{username}' não encontrado!" + cores.NORMAL)
    
    def menu_sem_usuario(self):
        """Menu exibido quando não há usuário selecionado"""
        while True:
            limpar_terminal()
            print(cores.AMARELO + "="*50)
            print("  BEM-VINDO! NENHUM USUÁRIO SELECIONADO")
            print("="*50 + cores.NORMAL)
            print("\nPara começar, você precisa criar ou selecionar um usuário.\n")
            print("[1] Criar novo usuário")
            print("[2] Selecionar usuário existente")
            print("[3] Configurações avançadas de usuários")
            print("[0] Sair")
            
            opcao = input("\nEscolha uma opção: ").strip()
            
            if opcao == "1":
                username = self.gerenciador_usuarios.criar_usuario()
                if username:
                    self.salvar_usuario_atual(username)
                    print(cores.VERDE + f"\nUsuário '{username}' selecionado automaticamente!" + cores.NORMAL)
                    input("\nPressione Enter para continuar...")
                    return
            elif opcao == "2":
                if self.selecionar_usuario():
                    return
            elif opcao == "3":
                self.gerenciador_usuarios.menu_principal()
            elif opcao == "0":
                print("\nAté logo!")
                exit()
            else:
                print(cores.VERMELHO + "Opção inválida!" + cores.NORMAL)
                input("\nPressione Enter para continuar...")
    
    def exibir_cabecalho(self):
        """Exibe informações do usuário atual"""
        limpar_terminal()
        
        if self.usuario_atual:
            dados_usuario = self.gerenciador_usuarios.gd.obter_usuario(self.usuario_atual)
            if dados_usuario:
                stats = self.gerenciador_usuarios.gd.obter_estatisticas(self.usuario_atual)
                print(cores.AZUL + "="*50)
                print(f"  Usuário: {dados_usuario['nome_real']} (@{self.usuario_atual})")
                print(f"  Meta diária: {dados_usuario.get('tempo_label', str(dados_usuario['tempo_diario']) + ' horas')}")
                print(f"  Metas: {stats['total_metas']} | Missões: {stats['missoes_completas']}/{stats['total_missoes']}")
                print("="*50 + cores.NORMAL)
    
    def menu_principal(self):
        """Menu principal do sistema"""
        limpar_terminal()

        # Se não há usuário, exibe menu de seleção/criação
        if not self.usuario_atual:
            self.menu_sem_usuario()
        
        # Inicializa o menu de metas
        if not self.menu_metas:
            self.menu_metas = MenuMetas(self.usuario_atual)
        
        # Menu principal com usuário selecionado
        opcao = ''
        while opcao != "0":
            limpar_terminal()
            self.exibir_cabecalho()
            
            print(cores.VERDE + "\nMenu Principal\n" + cores.NORMAL)
            print("[1] Gerenciar Metas")
            print("[2] Monitoramento de Progresso")
            print("[3] Trocar de usuário")
            print("[4] Gerenciar usuários")
            print("[0] Sair do Programa")
            
            opcao = input("\nEscolha uma opção: ").strip()
            limpar_terminal()
            
            if opcao == "1":
                self.menu_metas.menu_principal()
            elif opcao == "2":
                self.exibir_monitoramento()
            elif opcao == "3":
                if self.selecionar_usuario():
                    # Atualiza o menu de metas com o novo usuário
                    self.menu_metas = MenuMetas(self.usuario_atual)
                else:
                    print(cores.AMARELO + "Usuário não foi alterado." + cores.NORMAL)
                    input("\nPressione Enter para continuar...")
            elif opcao == "4":
                self.gerenciador_usuarios.menu_principal()
            elif opcao == "0":
                print(cores.VERDE+"Esperamos te ver amanhã!"+cores.NORMAL)
                exit()
            else:
                print(cores.VERMELHO + "Opção não reconhecida!" + cores.NORMAL)
                input("\nPressione Enter para continuar...")
    
    def exibir_monitoramento(self):
        """Exibe monitoramento de progresso"""
        limpar_terminal()
        
        if not self.usuario_atual:
            print(cores.VERMELHO + "Nenhum usuário selecionado!" + cores.NORMAL)
            input("\nPressione Enter para continuar...")
            return
        
        dados = self.gerenciador_usuarios.gd.obter_usuario(self.usuario_atual)
        stats = self.gerenciador_usuarios.gd.obter_estatisticas(self.usuario_atual)
        
        print(cores.VERDE + "="*50)
        print("  MONITORAMENTO DE PROGRESSO")
        print("="*50 + cores.NORMAL)
        
        print(f"\nUsuário: {dados['nome_real']} (@{self.usuario_atual})")
        print(f"Criado em: {dados['data_criacao']}")
        print(f"Meta diária: {dados.get('tempo_label', str(dados['tempo_diario']) + ' horas')}")
        
        print(f"\n{cores.AZUL}--- Estatísticas Gerais ---{cores.NORMAL}")
        print(f"Total de metas: {stats['total_metas']}")
        print(f"Total de missões: {stats['total_missoes']}")
        print(f"Missões completas: {cores.VERDE}{stats['missoes_completas']}{cores.NORMAL}")
        print(f"Missões pendentes: {cores.AMARELO}{stats['missoes_pendentes']}{cores.NORMAL}")
        
        if stats['total_missoes'] > 0:
            taxa = stats['taxa_conclusao']
            cor_taxa = cores.VERDE if taxa >= 70 else cores.AMARELO if taxa >= 40 else cores.VERMELHO
            print(f"Taxa de conclusão: {cor_taxa}{taxa:.1f}%{cores.NORMAL}")
            
            # Barra de progresso
            barra_tamanho = 30
            completo = int((taxa / 100) * barra_tamanho)
            vazio = barra_tamanho - completo
            print(f"\n[{'█' * completo}{'░' * vazio}] {taxa:.1f}%")
        
        # Detalhes por meta
        metas = self.gerenciador_usuarios.gd.listar_metas(self.usuario_atual)
        if metas:
            print(f"\n{cores.AZUL}--- Progresso por Meta ---{cores.NORMAL}")
            for meta_id, meta in metas.items():
                missoes = meta.get('missoes', {})
                total = len(missoes)
                completas = sum(1 for m in missoes.values() if m.get('completa', False))
                
                if total > 0:
                    percentual = (completas / total) * 100
                    print(f"\n{meta['nome']}:")
                    print(f"  Missões: {completas}/{total} ({percentual:.0f}%)")
                else:
                    print(f"\n{meta['nome']}:")
                    print(f"  Sem missões cadastradas")
        
        input("\n\nPressione Enter para continuar...")

if __name__ == "__main__":
    sistema = SistemaMain()
    sistema.menu_principal()