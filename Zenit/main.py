import json
import os
from util import cores, limpar_terminal, enter_continuar, Tempo
from metas import MenuMetas
from usuario import GerenciadorUsuarios
from loja import Loja

class SistemaMain:
    def __init__(self):
        self.arquivo_config = 'config.json'
        self.gerenciador_usuarios = GerenciadorUsuarios()
        self.usuario_atual = self.carregar_usuario_atual()
        self.menu_metas = None
        self.loja = None
        
        # Verifica streak e reseta missões ao iniciar
        if self.usuario_atual:
            quebrou_streak = self.gerenciador_usuarios.gd.verificar_e_resetar_streak(self.usuario_atual)
            missoes_resetadas = self.gerenciador_usuarios.gd.verificar_e_resetar_missoes(self.usuario_atual)
            
            # Notifica se quebrou o streak
            if quebrou_streak:
                print(f"\n{cores.VERMELHO}❌ Seu streak foi resetado por inatividade.{cores.NORMAL}")
                enter_continuar()
    
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
        # Atualiza o menu de metas e loja com o novo usuário
        self.menu_metas = MenuMetas(username)
        self.loja = Loja(username)
        # Verifica streak e reseta missões
        self.gerenciador_usuarios.gd.verificar_e_resetar_streak(username)
        self.gerenciador_usuarios.gd.verificar_e_resetar_missoes(username)
    
    def limpar_usuario_atual(self):
        """Remove o usuário atual da configuração"""
        if os.path.exists(self.arquivo_config):
            os.remove(self.arquivo_config)
        self.usuario_atual = None
        self.menu_metas = None
        self.loja = None
    
    def selecionar_usuario(self):
        """Permite selecionar um usuário existente"""
        limpar_terminal()
        
        usuarios = self.gerenciador_usuarios.gd.listar_usuarios()
        if not usuarios:
            print(cores.AMARELO + "Nenhum usuário cadastrado ainda." + cores.NORMAL)
            enter_continuar()
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
                enter_continuar()
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
                    enter_continuar()
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
                enter_continuar()
    
    def exibir_cabecalho(self):
        """Exibe informações do usuário atual"""
        limpar_terminal()
        
        if self.usuario_atual:
            dados_usuario = self.gerenciador_usuarios.gd.obter_usuario(self.usuario_atual)
            if dados_usuario:
                stats = self.gerenciador_usuarios.gd.obter_estatisticas(self.usuario_atual)
                streak = stats.get('streak', 0)
                pendentes_hoje = stats.get('missoes_pendentes_hoje', 0)
                completas_hoje = stats.get('missoes_completas_hoje', 0)
                pontos = dados_usuario.get('pontos', 0)
                
                print(cores.AZUL + "="*50)
                print(f"  Usuário: {dados_usuario['nome_real']} (@{self.usuario_atual})")
                print(f"  Meta diária: {dados_usuario.get('tempo_label', str(dados_usuario['tempo_diario']) + ' horas')}")
                
                if pendentes_hoje > 0:
                    print(f"  Metas: {stats['total_metas']} | {cores.AMARELO}Missões para hoje: {completas_hoje}/{pendentes_hoje}{cores.AZUL}")
                else:
                    print(f"  Metas: {stats['total_metas']} | Missões: {stats['total_missoes']}")

                # Exibe streak e pontos
                if streak > 0:
                    print(f"  {cores.VERDE}🔥 Streak: {streak} dia(s){cores.AZUL} | Pontos: {pontos}")
                else:
                    print(f"  Streak: {streak} dia(s) | Pontos: {pontos}")
                
                print("="*50 + cores.NORMAL)
    
    def menu_principal(self):
        """Menu principal do sistema"""
        limpar_terminal()

        # Se não há usuário, exibe menu de seleção/criação
        if not self.usuario_atual:
            self.menu_sem_usuario()
        
        # Inicializa o menu de metas e loja
        if not self.menu_metas:
            self.menu_metas = MenuMetas(self.usuario_atual)
        if not self.loja:
            self.loja = Loja(self.usuario_atual)
        
        # Menu principal com usuário selecionado
        opcao = ''
        while opcao != "0":
            limpar_terminal()
            self.gerenciador_usuarios = GerenciadorUsuarios()
            self.exibir_cabecalho()
            
            print(cores.VERDE + "\nMenu Principal\n" + cores.NORMAL)
            print("[1] Gerenciar Metas")
            print("[2] Monitoramento de Progresso")
            print("[3] Loja de Itens")
            print("[4] Exportar Progresso")
            print("[5] Trocar de usuário")
            print("[0] Sair do Programa")
            
            opcao = input("\nEscolha uma opção: ").strip()
            limpar_terminal()
            
            if opcao == "1":
                self.menu_metas.menu_principal()
            elif opcao == "2":
                self.exibir_monitoramento()
            elif opcao == "3":
                self.loja.menu_principal()
            elif opcao == "4":
                self.exportar_progresso()
            elif opcao == "5":
                if self.selecionar_usuario():
                    # Atualiza o menu de metas e loja com o novo usuário
                    self.menu_metas = MenuMetas(self.usuario_atual)
                    self.loja = Loja(self.usuario_atual)
                else:
                    print(cores.AMARELO + "Usuário não foi alterado." + cores.NORMAL)
                    enter_continuar()
            elif opcao == "adm_usuarios":
                self.gerenciador_usuarios.menu_principal()
            elif opcao == "0":
                print(cores.VERDE+"Esperamos te ver amanhã!"+cores.NORMAL)
                exit()
            else:
                print(cores.VERMELHO + "Opção não reconhecida!" + cores.NORMAL)
                enter_continuar()
    
    def exibir_monitoramento(self):
        """Exibe monitoramento de progresso"""
        limpar_terminal()
        
        if not self.usuario_atual:
            print(cores.VERMELHO + "Nenhum usuário selecionado!" + cores.NORMAL)
            enter_continuar()
            return
        
        dados = self.gerenciador_usuarios.gd.obter_usuario(self.usuario_atual)
        stats = self.gerenciador_usuarios.gd.obter_estatisticas(self.usuario_atual)
        itens = self.gerenciador_usuarios.gd.obter_todos_itens(self.usuario_atual)
        
        print(cores.VERDE + "="*50)
        print("  MONITORAMENTO DE PROGRESSO")
        print("="*50 + cores.NORMAL)
        
        print(f"\nUsuário: {dados['nome_real']} (@{self.usuario_atual})")
        print(f"Criado em: {dados['data_criacao']}")
        print(f"Meta diária: {dados.get('tempo_label', str(dados['tempo_diario']) + ' horas')}")
        # Informações de Pontos
        pontos = dados.get('pontos', 0)
        print(f"Pontos: {cores.VERDE}{pontos}{cores.NORMAL}")
        
        # Informações de Streak
        streak = stats.get('streak', 0)
        ultima_missao = stats.get('ultima_missao')
        
        print(f"\n{cores.AZUL}--- Streak ---{cores.NORMAL}")
        if streak > 0:
            print(f"🔥 {streak} dia(s) consecutivo(s)!")
            if ultima_missao:
                print(f"Última missão completa: {Tempo.formatar_tempo_relativo(ultima_missao)}")
        else:
            print(f"{cores.AMARELO}Nenhum streak ativo.{cores.NORMAL}\nComplete uma missão hoje para começar!")
        
        print(f"\n{cores.AZUL}--- Estatísticas Gerais ---{cores.NORMAL}")
        print(f"Total de metas: {stats['total_metas']}")
        print(f"Total de missões: {stats['total_missoes']}")
        print(f"Missões completas: {cores.VERDE}{stats['missoes_completas_hoje']}{cores.NORMAL}")
        print(f"Missões pendentes: {cores.AMARELO}{stats['missoes_pendentes_hoje']}{cores.NORMAL}")
        
        if stats.get('missoes_pendentes_hoje',0) > 0:
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
                missoes_hoje = self.gerenciador_usuarios.gd.listar_missoes_pendentes_hoje(
                    self.usuario_atual, meta_id
                )
                total = len(missoes)
                
                if total > 0:
                    print(f"\n{meta['nome']}:")
                    print(f"  Missões: {total}")
                    for missao_id, missao in missoes.items():
                        completa = missao.get('completa', False)
                        data_pendente = missao.get('data_pendente', '')     
                        if completa:
                            status = "✓"
                            info = "(Completa)"
                        elif Tempo.e_hoje(data_pendente):
                            status = "○"
                            info = "(Hoje)"
                        elif Tempo.e_antes_de_hoje(data_pendente):
                            status = "●"
                            info = "(Atrasada)"
                        else:
                            status = None
                            info = None
                        if status and info:
                            print(f"   {status} {missao['nome']} {info}")
                else:
                    print(f"\n{meta['nome']}:")
                    print(f"  Sem missões cadastradas")
        
        enter_continuar()
    
    def exportar_progresso(self):
        """Exporta o progresso do usuário para um arquivo .txt"""
        limpar_terminal()
        
        if not self.usuario_atual:
            print(cores.VERMELHO + "Nenhum usuário selecionado!" + cores.NORMAL)
            enter_continuar()
            return
        
        dados = self.gerenciador_usuarios.gd.obter_usuario(self.usuario_atual)
        stats = self.gerenciador_usuarios.gd.obter_estatisticas(self.usuario_atual)
        
        # Nome do arquivo
        timestamp = Tempo.extrair_data(Tempo.agora()).replace("/", "-")
        nome_arquivo = f"progresso_{self.usuario_atual}_{timestamp}.txt"
        
        try:
            with open(nome_arquivo, 'w', encoding='utf-8') as f:
                # Cabeçalho
                f.write("="*60 + "\n")
                f.write(" "*19+"RELATÓRIO DE PROGRESSO\n\n\n")
                
                # Informações do usuário
                f.write(f"Usuário: {dados['nome_real']} (@{self.usuario_atual})\n")
                f.write(f"Criado em: {dados['data_criacao']}\n")
                f.write(f"Meta diária: {dados.get('tempo_label', str(dados['tempo_diario']) + ' horas')}\n")
                f.write(f"Pontos: {dados.get('pontos', 0)}\n")
                f.write(f"Relatório gerado em: {Tempo.agora()}\n")
                
                # Informações de Streak
                f.write("\n" + "-"*60 + "\n")
                f.write(" "*27+"STREAK\n")
                f.write("-"*60 + "\n")
                
                streak = stats.get('streak', 0)
                ultima_missao = stats.get('ultima_missao')
                
                if streak > 0:
                    f.write(f"🔥 {streak} dia(s) consecutivo(s)!\n")
                    if ultima_missao:
                        f.write(f"Última missão completa: {Tempo.formatar_tempo_relativo(ultima_missao)}\n")
                else:
                    f.write("Nenhum streak ativo.\n")
                
                # Estatísticas Gerais
                f.write("\n" + "-"*60 + "\n")
                f.write(" "*20+"ESTATÍSTICAS GERAIS\n")
                f.write("-"*60 + "\n")
                
                f.write(f"Total de metas: {stats['total_metas']}\n")
                f.write(f"Total de missões: {stats['total_missoes']}\n")
                
                # Detalhes por meta
                metas = self.gerenciador_usuarios.gd.listar_metas(self.usuario_atual)
                if metas:
                    f.write("\n" + "-"*60 + "\n")
                    f.write(" "*21+"PROGRESSO POR META\n")
                    f.write("-"*60 + "\n")
                    
                    for meta_id, meta in metas.items():
                        f.write(f"\n{meta['nome']}\n")
                        
                        if meta.get('descricao'):
                            f.write(f"  Descrição: {meta['descricao']}\n")
                        
                        f.write(f"  Criada em: {meta.get('data_criacao', 'Data desconhecida')}\n")
                        
                        missoes = meta.get('missoes', {})
                        missoes_hoje = self.gerenciador_usuarios.gd.listar_missoes_pendentes_hoje(
                            self.usuario_atual, meta_id
                        )
                        total = len(missoes)
                        
                        f.write(f"  Total de missões: {total}\n")
                        
                        # Lista todas as missões desta meta
                        if missoes:
                            f.write("\n  Missões:\n")
                            for missao_id, missao in missoes.items():
                                f.write(f"    {missao['nome']}\n")
                                f.write(f"      Frequência: A cada {missao.get('frequencia', 1)} dia(s)\n")
                
                # Rodapé
                f.write("\n\n"+" "*22+"Fim do relatório\n")
                f.write("="*60 + "\n")
            
            print(cores.VERDE + "="*50)
            print("  ✓ PROGRESSO EXPORTADO COM SUCESSO!")
            print("="*50 + cores.NORMAL)
            print(f"\nArquivo salvo como: {cores.AZUL}{nome_arquivo}{cores.NORMAL}")
            print(f"Localização: {cores.AZUL}{os.path.abspath(nome_arquivo)}{cores.NORMAL}")
            
        except Exception as e:
            print(cores.VERMELHO + f"Erro ao exportar progresso: {e}" + cores.NORMAL)
        
        enter_continuar()

if __name__ == "__main__":
    sistema = SistemaMain()
    sistema.menu_principal()