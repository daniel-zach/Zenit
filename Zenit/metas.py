import json
import os
from util import cores, limpar_terminal, enter_continuar, Tempo
from gerenciador_dados import GerenciadorDados

class MenuMetas:
    """Menus para metas e missões"""
    
    def __init__(self, username):
        self.username = username
        self.gd = GerenciadorDados()
        self.arquivo_presets = 'metas_predefinidas.json'
        self.presets = self.carregar_presets()
    
    def carregar_presets(self):
        """Carrega as metas predefinidas do arquivo JSON"""
        if os.path.exists(self.arquivo_presets):
            try:
                with open(self.arquivo_presets, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"{cores.AMARELO}Aviso: Erro ao carregar metas predefinidas.{cores.NORMAL}")
                return {"categorias": {}}
        return {"categorias": {}}
    
    def menu_principal(self):
        """Menu principal de gerenciamento de metas"""
        opcao = ''
        while opcao != "0":
            limpar_terminal()
            print(cores.VERDE + "Gerenciar Metas\n" + cores.NORMAL)
            print("[C] Criar uma nova meta")
            print("[P] Criar meta a partir de predefinição")
            
            # Lista todas as metas do usuário
            metas = self.gd.listar_metas(self.username)
            if metas:
                print("\nMetas cadastradas:")
                for meta_id, meta in metas.items():
                    # Conta missões completas e pendentes hoje
                    missoes_hoje = self.gd.listar_missoes_pendentes_hoje(self.username, meta_id)
                    missoes_todas = meta.get('missoes', {})
                    completas = sum(1 for m in missoes_todas.values() if m.get('completa', False))
                    pendentes_hoje = len(missoes_hoje)
                    
                    status = f"({completas}/{pendentes_hoje})"
                    if pendentes_hoje > 0:
                        status += f" {cores.AMARELO}[{pendentes_hoje} hoje]{cores.NORMAL}"
                    print(f"[{meta_id}] {meta['nome']} {cores.AZUL}{status}{cores.NORMAL}")
            else:
                print(f"\n{cores.AMARELO}Nenhuma meta cadastrada ainda.{cores.NORMAL}")
            
            print("\n[0] Voltar ao Menu Principal")
            opcao = input("\nEscolha uma opção: ").strip().lower()
            limpar_terminal()
            
            if opcao == "c":
                self.criar_meta()
            elif opcao == "p":
                self.criar_meta_preset()
            elif opcao == "0":
                return
            else:
                # Verifica se é um ID de meta válido
                if opcao in metas:
                    self.menu_visualizar_meta(opcao)
                else:
                    print(cores.VERMELHO + "Opção não reconhecida!" + cores.NORMAL)
                    enter_continuar()
    
    def criar_meta_preset(self):
        """Cria uma meta a partir de uma predefinição"""
        limpar_terminal()
        
        categorias = self.presets.get("categorias", {})
        
        if not categorias:
            print(cores.AMARELO + "Nenhuma predefinição disponível!" + cores.NORMAL)
            enter_continuar()
            return
        
        print(cores.VERDE + "=== CRIAR META A PARTIR DE PREDEFINIÇÃO ===" + cores.NORMAL)
        print("\nCategorias disponíveis:\n")
        
        # Lista categorias
        cat_lista = list(categorias.items())
        for i, (cat_id, cat_data) in enumerate(cat_lista, 1):
            print(f"[{i}] {cat_data['nome']}")
        
        print("\n[0] Cancelar")
        
        # Escolher categoria
        while True:
            escolha_cat = input("\nEscolha uma categoria: ").strip()
            
            if escolha_cat == "0":
                return
            
            if escolha_cat.isdigit() and 1 <= int(escolha_cat) <= len(cat_lista):
                cat_id, cat_data = cat_lista[int(escolha_cat) - 1]
                break
            else:
                print(cores.VERMELHO + "Opção inválida!" + cores.NORMAL)
        
        # Lista metas da categoria
        limpar_terminal()
        print(cores.VERDE + f"=== {cat_data['nome'].upper()} ===" + cores.NORMAL)
        print("\nMetas disponíveis:\n")
        
        metas_lista = list(cat_data['metas'].items())
        for idx, (meta_id, meta_data) in enumerate(metas_lista, 1):
            print(f"[{idx}] {meta_data['nome']}")
            print(f"    {cores.AZUL}{meta_data['descricao']}{cores.NORMAL}")
            print(f"    {len(meta_data['missoes'])} missão(ões) incluída(s)\n")
        
        print("[0] Voltar")
        
        # Escolher meta
        while True:
            escolha_meta = input("\nEscolha uma meta: ").strip()
            
            if escolha_meta == "0":
                return
            
            if escolha_meta.isdigit() and 1 <= int(escolha_meta) <= len(metas_lista):
                meta_id, meta_preset = metas_lista[int(escolha_meta) - 1]
                break
            else:
                print(cores.VERMELHO + "Opção inválida!" + cores.NORMAL)
        
        # Confirmar criação
        limpar_terminal()
        print(cores.VERDE + "=== CONFIRMAR CRIAÇÃO ===" + cores.NORMAL)
        print(f"\nMeta: {meta_preset['nome']}")
        print(f"Descrição: {meta_preset['descricao']}")
        print(f"\nMissões que serão criadas:")
        
        for missao in meta_preset['missoes']:
            freq_texto = "diariamente" if missao['frequencia'] == 1 else f"a cada {missao['frequencia']} dias"
            print(f"  • {missao['nome']} ({freq_texto})")
        
        confirma = input(f"\n{cores.AMARELO}Deseja criar esta meta? (s/n): {cores.NORMAL}").strip().lower()
        
        if confirma != 's':
            limpar_terminal()
            print(cores.AMARELO + "Operação cancelada." + cores.NORMAL)
            enter_continuar()
            return
        
        # Criar a meta
        sucesso, msg = self.gd.criar_meta(
            self.username, 
            meta_preset['nome'], 
            meta_preset['descricao']
        )
        
        if not sucesso:
            limpar_terminal()
            print(cores.VERMELHO + msg + cores.NORMAL)
            enter_continuar()
            return
        
        # Obter o ID da meta recém-criada
        metas = self.gd.listar_metas(self.username)
        meta_id = str(len(metas))
        
        # Criar todas as missões
        missoes_criadas = 0
        for missao_preset in meta_preset['missoes']:
            sucesso_missao, msg_missao = self.gd.criar_missao(
                self.username,
                meta_id,
                missao_preset['nome'],
                missao_preset['frequencia']
            )
            if sucesso_missao:
                missoes_criadas += 1
        
        # Exibir resultado
        limpar_terminal()
        print(cores.VERDE + "="*50)
        print("  ✓ META CRIADA COM SUCESSO!")
        print("="*50 + cores.NORMAL)
        print(f"\nMeta: {meta_preset['nome']}")
        print(f"Missões criadas: {cores.VERDE}{missoes_criadas}{cores.NORMAL}")
        enter_continuar()
    
    def criar_meta(self):
        """Cria uma nova meta"""
        limpar_terminal()
        print(cores.VERDE + "=== CRIAR NOVA META ===" + cores.NORMAL)
        
        # Nome da meta
        while True:
            nome = input("\nDefina o nome da meta: ").strip()
            if not nome:
                print(cores.VERMELHO + "A meta precisa de um nome!" + cores.NORMAL)
                continue
            break
        
        # Descrição da meta
        descricao = input("Defina a descrição da meta (opcional): ").strip()
        
        # Criar meta usando GerenciadorDados
        sucesso, msg = self.gd.criar_meta(self.username, nome, descricao)
        
        limpar_terminal()
        if sucesso:
            print(cores.VERDE + msg + cores.NORMAL)
        else:
            print(cores.VERMELHO + msg + cores.NORMAL)
        enter_continuar()
    
    def menu_visualizar_meta(self, meta_id):
        """Menu de visualização e edição de uma meta específica"""
        opcao = ''
        while opcao != "0":
            limpar_terminal()
            
            # Carrega dados da meta
            meta = self.gd.obter_meta(self.username, meta_id)
            if not meta:
                print(cores.VERMELHO + "Meta não encontrada!" + cores.NORMAL)
                enter_continuar()
                return
            
            # Exibe informações da meta
            print(cores.VERDE + "="*50)
            print(f"  {meta['nome'].upper()}")
            print("="*50 + cores.NORMAL)
            
            if meta.get('descricao'):
                print(f"\nDescrição: {meta['descricao']}")
            
            # Estatísticas da meta
            missoes = meta.get('missoes', {})
            missoes_hoje = self.gd.listar_missoes_pendentes_hoje(self.username, meta_id)
            total_missoes = len(missoes)
            completas = sum(1 for m in missoes.values() if m.get('completa', False))
            pendentes_hoje = len(missoes_hoje)
            
            print(f"\nMissões: {total_missoes}")
            if pendentes_hoje > 0:
                print(f"{cores.AMARELO}Missões para hoje: {pendentes_hoje}{cores.NORMAL}")
                percentual = (completas / pendentes_hoje) * 100
                print(f"{cores.VERDE}Progresso: {percentual:.0f}%{cores.NORMAL}")
            
            print(f"\nCriada em: {meta.get('data_criacao', 'Data desconhecida')}")
            
            # Menu de opções
            print(f"\n{cores.AZUL}--- OPÇÕES ---{cores.NORMAL}")
            print("[1] Gerenciar Missões")
            print("[2] Editar meta")
            print("[3] Excluir meta")
            print("[0] Voltar ao menu de metas")
            
            opcao = input("\nEscolha uma opção: ").strip()
            limpar_terminal()
            
            if opcao == "1":
                self.menu_missoes(meta_id)
            elif opcao == "2":
                self.editar_meta(meta_id)
            elif opcao == "3":
                if self.excluir_meta(meta_id):
                    return  # Volta ao menu anterior após exclusão
            elif opcao == "0":
                return
            else:
                print(cores.VERMELHO + "Opção não reconhecida!" + cores.NORMAL)
                enter_continuar()
    
    def editar_meta(self, meta_id):
        """Edita uma meta existente"""
        limpar_terminal()
        meta = self.gd.obter_meta(self.username, meta_id)
        
        print(cores.VERDE + "=== EDITAR META ===" + cores.NORMAL)
        print(f"\nMeta atual: {meta['nome']}")
        print(f"Descrição atual: {meta.get('descricao', '(sem descrição)')}")
        
        print("\nO que deseja editar?")
        print("[1] Nome")
        print("[2] Descrição")
        print("[3] Ambos")
        print("[0] Cancelar")
        
        opcao = input("\nOpção: ").strip()
        
        novo_nome = None
        nova_descricao = None
        
        if opcao in ["1", "3"]:
            novo_nome = input("\nNovo nome da meta: ").strip()
            if not novo_nome:
                print(cores.AMARELO + "Nome não pode ser vazio!" + cores.NORMAL)
                enter_continuar()
                return
        
        if opcao in ["2", "3"]:
            nova_descricao = input("Nova descrição da meta: ").strip()
        
        if opcao in ["1", "2", "3"]:
            sucesso, msg = self.gd.atualizar_meta(
                self.username, 
                meta_id, 
                nome=novo_nome, 
                descricao=nova_descricao
            )
            limpar_terminal()
            if sucesso:
                print(cores.VERDE + msg + cores.NORMAL)
            else:
                print(cores.VERMELHO + msg + cores.NORMAL)
        else:
            limpar_terminal()
            print(cores.AMARELO + "Operação cancelada." + cores.NORMAL)
        
        enter_continuar()
    
    def excluir_meta(self, meta_id):
        """Exclui uma meta e todas suas missões"""
        limpar_terminal()
        meta = self.gd.obter_meta(self.username, meta_id)
        
        print(cores.VERMELHO + "=== EXCLUIR META ===" + cores.NORMAL)
        print(f"\nMeta: {meta['nome']}")
        
        total_missoes = len(meta.get('missoes', {}))
        print(f"\n{cores.AMARELO}ATENÇÃO: Isso excluirá também {total_missoes} missão(ões)!{cores.NORMAL}")
        
        confirma = input("\nTem certeza? (s/n): ").strip().lower()
        
        if confirma == 's':
            sucesso, msg = self.gd.excluir_meta(self.username, meta_id)
            limpar_terminal()
            if sucesso:
                print(cores.VERDE + msg + cores.NORMAL)
            else:
                print(cores.VERMELHO + msg + cores.NORMAL)
            enter_continuar()
            return True
        else:
            limpar_terminal()
            print(cores.AMARELO + "Operação cancelada." + cores.NORMAL)
            enter_continuar()
            return False
    
    def menu_missoes(self, meta_id):
        """Menu de gerenciamento de missões de uma meta"""
        opcao = ''
        while opcao != "0":
            limpar_terminal()
            
            # Carrega dados da meta
            meta = self.gd.obter_meta(self.username, meta_id)
            if not meta:
                print(cores.VERMELHO + "Meta não encontrada!" + cores.NORMAL)
                enter_continuar()
                return
            
            print(cores.VERDE + f"Missões de {meta['nome']}\n" + cores.NORMAL)
            print("[C] Criar uma nova missão")
            print("[T] Ver TODAS as missões")
            
            # Lista apenas missões pendentes para hoje
            missoes_hoje = self.gd.listar_missoes_pendentes_hoje(self.username, meta_id)
            
            if missoes_hoje:
                print(f"\n{cores.AMARELO}Missões pendentes para hoje:{cores.NORMAL}")
                for missao_id, missao in missoes_hoje.items():
                    data_pendente = missao.get('data_pendente', '')
                    tempo_relativo = Tempo.formatar_tempo_relativo(data_pendente)
                    
                    if Tempo.e_antes_de_hoje(data_pendente):
                        # Missão atrasada
                        print(f"[{missao_id}] {cores.VERMELHO}● {missao['nome']} (ATRASADA){cores.NORMAL}")
                    else:
                        # Missão de hoje
                        print(f"[{missao_id}] {cores.AMARELO}○ {missao['nome']}{cores.NORMAL}")
            else:
                print(f"\n{cores.VERDE}✓ Nenhuma missão pendente para hoje!{cores.NORMAL}")
            
            print(f"\n[0] Voltar ao menu da meta")
            opcao = input("\nEscolha uma opção: ").strip().lower()
            limpar_terminal()
            
            if opcao == "c":
                self.criar_missao(meta_id)
            elif opcao == "t":
                self.menu_todas_missoes(meta_id)
            elif opcao == "0":
                return
            else:
                # Verifica se é um ID de missão válido
                if opcao in missoes_hoje:
                    self.menu_visualizar_missao(meta_id, opcao)
                else:
                    print(cores.VERMELHO + "Opção não reconhecida!" + cores.NORMAL)
                    enter_continuar()
    
    def menu_todas_missoes(self, meta_id):
        """Mostra todas as missões (completas e futuras)"""
        opcao = ''
        while opcao != "0":
            limpar_terminal()
            
            meta = self.gd.obter_meta(self.username, meta_id)
            if not meta:
                print(cores.VERMELHO + "Meta não encontrada!" + cores.NORMAL)
                enter_continuar()
                return
            
            print(cores.VERDE + f"Todas as Missões de {meta['nome']}\n" + cores.NORMAL)
            
            # Lista todas as missões
            missoes = meta.get('missoes', {})
            if missoes:
                print("Missões cadastradas:")
                for missao_id, missao in missoes.items():
                    completa = missao.get('completa', False)
                    data_pendente = missao.get('data_pendente', '')
                    tempo_relativo = Tempo.formatar_tempo_relativo(data_pendente)
                    
                    if completa:
                        status = f"{cores.VERDE}✓{cores.NORMAL}"
                        info = f"(Completa)"
                    elif Tempo.e_hoje(data_pendente):
                        status = f"{cores.AMARELO}○{cores.NORMAL}"
                        info = f"(Hoje)"
                    elif Tempo.e_antes_de_hoje(data_pendente):
                        status = f"{cores.VERMELHO}●{cores.NORMAL}"
                        info = f"(Atrasada)"
                    else:
                        status = "◌"
                        info = f"({tempo_relativo})"
                    
                    print(f"[{missao_id}] {status} {missao['nome']} {cores.AZUL}{info}{cores.NORMAL}")
            else:
                print(f"{cores.AMARELO}Nenhuma missão cadastrada ainda.{cores.NORMAL}")
            
            print(f"\n[0] Voltar")
            opcao = input("\nEscolha uma opção: ").strip().lower()
            limpar_terminal()
            
            if opcao == "0":
                return
            else:
                # Verifica se é um ID de missão válido
                if opcao in missoes:
                    self.menu_visualizar_missao(meta_id, opcao)
                else:
                    print(cores.VERMELHO + "Opção não reconhecida!" + cores.NORMAL)
                    enter_continuar()
    
    def criar_missao(self, meta_id):
        """Cria uma nova missão"""
        limpar_terminal()
        meta = self.gd.obter_meta(self.username, meta_id)
        
        print(cores.VERDE + f"=== CRIAR NOVA MISSÃO ===" + cores.NORMAL)
        print(f"Meta: {meta['nome']}\n")
        
        # Nome da missão
        while True:
            nome = input("Defina o nome da missão: ").strip()
            if not nome:
                print(cores.VERMELHO + "A missão precisa de um nome!" + cores.NORMAL)
                continue
            break

        # Tempo em dias em que a missão irá se repetir
        while True:
            tempo_repetir = input("Com que frequência gostaria de repetir esta missão (dias): ").strip()
            if not tempo_repetir:
                print(cores.VERMELHO + "Por favor defina um tempo." + cores.NORMAL)
                continue
            if tempo_repetir.isdigit() and 1 <= int(tempo_repetir) <= 365:
                dias_repeticao = tempo_repetir
                break
            else:
                print(cores.VERMELHO + "Valor inserido é inválido! (1-365 dias)" + cores.NORMAL)
        
        # Criar missão usando GerenciadorDados
        sucesso, msg = self.gd.criar_missao(self.username, meta_id, nome, dias_repeticao)
        
        limpar_terminal()
        if sucesso:
            print(cores.VERDE + msg + cores.NORMAL)
        else:
            print(cores.VERMELHO + msg + cores.NORMAL)
        enter_continuar()
    
    def menu_visualizar_missao(self, meta_id, missao_id):
        """Menu de visualização e edição de uma missão específica"""
        opcao = ''
        while opcao != "0":
            limpar_terminal()
            
            # Carrega dados da missão
            missao = self.gd.obter_missao(self.username, meta_id, missao_id)
            if not missao:
                print(cores.VERMELHO + "Missão não encontrada!" + cores.NORMAL)
                enter_continuar()
                return
            
            # Exibe informações da missão
            print(cores.VERDE + "="*50)
            print(f"  {missao['nome'].upper()}")
            print("="*50 + cores.NORMAL)
            
            completa = missao.get('completa', False)
            status_texto = f"{cores.VERDE}COMPLETA ✓{cores.NORMAL}" if completa else f"{cores.AMARELO}PENDENTE ○{cores.NORMAL}"
            print(f"\nStatus: {status_texto}")
            
            data_pendente = missao.get('data_pendente', '')
            if data_pendente:
                tempo_relativo = Tempo.formatar_tempo_relativo(data_pendente)
                if Tempo.e_antes_de_hoje(data_pendente) and not completa:
                    print(f"{cores.VERMELHO}Próxima: {tempo_relativo} (ATRASADA){cores.NORMAL}")
                else:
                    print(f"Próxima: {tempo_relativo}")
            
            print(f"Frequência: A cada {missao.get('frequencia', 1)} dia(s)")
            print(f"Criada em: {missao.get('data_criacao', 'Data desconhecida')}")
            
            if completa and 'data_conclusao' in missao:
                print(f"Concluída em: {missao['data_conclusao']}")
            
            # Menu de opções
            print(f"\n{cores.AZUL}--- OPÇÕES ---{cores.NORMAL}")
            
            if not completa:
                print("[1] Marcar como completa")
            else:
                print("[1] Marcar como pendente")
            
            print("[2] Editar missão")
            print("[3] Excluir missão")
            print("[0] Voltar ao menu de missões")
            
            opcao = input("\nEscolha uma opção: ").strip()
            limpar_terminal()
            
            if opcao == "1":
                self.alternar_status_missao(meta_id, missao_id, completa)
            elif opcao == "2":
                self.editar_missao(meta_id, missao_id)
            elif opcao == "3":
                if self.excluir_missao(meta_id, missao_id):
                    return  # Volta ao menu anterior após exclusão
            elif opcao == "0":
                return
            else:
                print(cores.VERMELHO + "Opção não reconhecida!" + cores.NORMAL)
                enter_continuar()
    
    def alternar_status_missao(self, meta_id, missao_id, status_atual):
        """Alterna o status de conclusão de uma missão"""
        novo_status = not status_atual
        sucesso, msg = self.gd.atualizar_missao(
            self.username, 
            meta_id, 
            missao_id, 
            completa=novo_status
        )
        
        if sucesso:
            texto_status = "completa" if novo_status else "pendente"
            mensagem = f"Missão marcada como {texto_status}!"
            
            if novo_status:
                # Mostra informação sobre streak
                stats = self.gd.obter_estatisticas(self.username)
                streak = stats.get('streak', 0)
                mensagem += f"\n{cores.VERDE}🔥 Streak: {streak} dia(s)!{cores.NORMAL}"
            
            print(cores.VERDE + mensagem + cores.NORMAL)
        else:
            print(cores.VERMELHO + msg + cores.NORMAL)
        
        enter_continuar()
    
    def editar_missao(self, meta_id, missao_id):
        """Edita uma missão existente"""
        limpar_terminal()
        missao = self.gd.obter_missao(self.username, meta_id, missao_id)
        
        print(cores.VERDE + "=== EDITAR MISSÃO ===" + cores.NORMAL)
        print(f"\nNome atual: {missao['nome']}")
        print(f"Frequência atual: {missao['frequencia']} dias")

        print("\nO que deseja editar?")
        print("[1] Nome")
        print("[2] Frequência")
        print("[3] Ambos")
        print("[0] Cancelar")
        
        opcao = input("\nOpção: ").strip()

        novo_nome = None
        nova_frequencia = None
        
        if opcao in ["1","3"]:
            novo_nome = input("\nNovo nome da missão: ").strip()
            if not novo_nome:
                print(cores.AMARELO + "Nome não pode ser vazio. Operação cancelada." + cores.NORMAL)
                enter_continuar()
                return
        
        if opcao in ["2","3"]:
            nova_frequencia = input("Nova frequência (dias): ").strip()
            if not nova_frequencia.isdigit() or not (1 <= int(nova_frequencia) <= 365):
                print(cores.AMARELO + "Valor inválido. Operação cancelada." + cores.NORMAL)
                enter_continuar()
                return
        
        if opcao in ["1","2","3"]:
            sucesso, msg = self.gd.atualizar_missao(
                self.username, 
                meta_id, 
                missao_id, 
                nome=novo_nome,
                frequencia=nova_frequencia
            )
            limpar_terminal()
            if sucesso:
                print(cores.VERDE + msg + cores.NORMAL)
            else:
                print(cores.VERMELHO + msg + cores.NORMAL)
        else:
            limpar_terminal()
            print(cores.AMARELO + "Operação cancelada." + cores.NORMAL)
        enter_continuar()
    
    def excluir_missao(self, meta_id, missao_id):
        """Exclui uma missão"""
        limpar_terminal()
        missao = self.gd.obter_missao(self.username, meta_id, missao_id)
        
        print(cores.VERMELHO + "=== EXCLUIR MISSÃO ===" + cores.NORMAL)
        print(f"\nMissão: {missao['nome']}")
        
        confirma = input("\nTem certeza? (s/n): ").strip().lower()
        
        if confirma == 's':
            sucesso, msg = self.gd.excluir_missao(self.username, meta_id, missao_id)
            limpar_terminal()
            if sucesso:
                print(cores.VERDE + msg + cores.NORMAL)
            else:
                print(cores.VERMELHO + msg + cores.NORMAL)
            enter_continuar()
            return True
        else:
            limpar_terminal()
            print(cores.AMARELO + "Operação cancelada." + cores.NORMAL)
            enter_continuar()
            return False