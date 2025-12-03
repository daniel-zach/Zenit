from util import cores, limpar_terminal, enter_continuar
from gerenciador_dados import GerenciadorDados

class Loja:
    """Sistema dos menus da loja para compra de itens"""
    
    def __init__(self, username):
        self.username = username
        self.gd = GerenciadorDados()
        
        # Catálogo de itens disponíveis
        self.catalogo = {
            "1": {
                "nome": "Defesa de Ofensiva",
                "descricao": "Protege seu streak de quebrar durante 1 dia",
                "preco": 50,
                "item_id": "defesa_ofensiva",
                "limite_maximo": 2
            }
        }
    
    def menu_principal(self):
        """Menu principal da loja"""
        opcao = ''
        while opcao != "0":
            limpar_terminal()
            
            # Carrega pontos e itens do usuário
            pontos = self.gd.obter_pontos(self.username)
            itens = self.gd.obter_todos_itens(self.username)
            
            print(cores.VERDE + "="*50)
            print("  LOJA DE ITENS")
            print("="*50 + cores.NORMAL)
            
            print(f"\n{cores.AZUL}Seus pontos: {pontos}{cores.NORMAL}")
            
            # Exibe inventário
            print(f"\n{cores.AZUL}Seu Inventário:{cores.NORMAL}")
            if itens:
                for item_nome, quantidade in itens.items():
                    nome_formatado = item_nome.replace('_', ' ').title()
                    print(f"  • {nome_formatado}: {quantidade}")
            else:
                print("  (vazio)")
            
            # Exibe catálogo
            print(f"\n{cores.VERDE}🛒 Itens Disponíveis:{cores.NORMAL}")
            for item_id, item in self.catalogo.items():
                quantidade_atual = itens.get(item["item_id"], 0)
                limite = item.get("limite_maximo", float('inf'))
                
                # Verifica se pode comprar
                if quantidade_atual >= limite:
                    status = f"{cores.VERMELHO}[LIMITE ATINGIDO]{cores.NORMAL}"
                elif pontos < item["preco"]:
                    status = f"{cores.AMARELO}[PONTOS INSUFICIENTES]{cores.NORMAL}"
                else:
                    status = f"{cores.VERDE}[DISPONÍVEL]{cores.NORMAL}"
                
                print(f"\n[{item_id}] {item['nome']} - {item['preco']} pontos {status}")
                print(f"    {item['descricao']}")
                
                if quantidade_atual > 0:
                    print(f"    {cores.AZUL}Você possui: {quantidade_atual}/{limite}{cores.NORMAL}")
            
            print(f"\n{cores.AMARELO}[0] Voltar ao Menu Principal{cores.NORMAL}")
            
            opcao = input("\nEscolha um item para comprar: ").strip()
            
            if opcao == "0":
                return
            elif opcao in self.catalogo:
                self.comprar_item(opcao)
            else:
                limpar_terminal()
                print(cores.VERMELHO + "Opção inválida!" + cores.NORMAL)
                enter_continuar()
    
    def comprar_item(self, item_id):
        """Processa a compra de um item"""
        limpar_terminal()
        
        item = self.catalogo[item_id]
        pontos = self.gd.obter_pontos(self.username)
        quantidade_atual = self.gd.obter_quantidade_item(self.username, item["item_id"])
        limite = item.get("limite_maximo", float('inf'))
        
        print(cores.VERDE + "="*50)
        print(f"  COMPRAR: {item['nome']}")
        print("="*50 + cores.NORMAL)
        
        print(f"\nPreço: {cores.AZUL}{item['preco']} pontos{cores.NORMAL}")
        print(f"Seus pontos: {cores.AZUL}{pontos} pontos{cores.NORMAL}")
        print(f"\nDescrição: {item['descricao']}")
        
        # Verificações
        if quantidade_atual >= limite:
            print(f"\n{cores.VERMELHO}❌ Você já atingiu o limite máximo deste item ({limite})!{cores.NORMAL}")
            enter_continuar()
            return
        
        if pontos < item["preco"]:
            faltam = item["preco"] - pontos
            print(f"\n{cores.VERMELHO}❌ Pontos insuficientes! Faltam {faltam} pontos.{cores.NORMAL}")
            enter_continuar()
            return
        
        # Confirmação
        print(f"\n{cores.AMARELO}Você possui: {quantidade_atual}/{limite}{cores.NORMAL}")
        confirma = input(f"\nConfirmar compra? (s/n): ").strip().lower()
        
        if confirma == 's':
            # Remove pontos
            sucesso_pontos, msg_pontos = self.gd.remover_pontos(self.username, item["preco"])
            
            if sucesso_pontos:
                # Adiciona item
                sucesso_item, msg_item = self.gd.adicionar_item(self.username, item["item_id"], 1)
                
                if sucesso_item:
                    limpar_terminal()
                    print(cores.VERDE + "="*50)
                    print("  ✅ COMPRA REALIZADA!")
                    print("="*50 + cores.NORMAL)
                    print(f"\n{cores.VERDE}Você comprou: {item['nome']}!{cores.NORMAL}")
                    print(f"{cores.AZUL}Pontos restantes: {self.gd.obter_pontos(self.username)}{cores.NORMAL}")
                    print(f"{cores.AZUL}Você agora possui: {quantidade_atual + 1}/{limite} {item['nome']}{cores.NORMAL}")
                else:
                    print(cores.VERMELHO + f"Erro ao adicionar item: {msg_item}" + cores.NORMAL)
                    # Devolve os pontos
                    self.gd.adicionar_pontos(self.username, item["preco"])
            else:
                print(cores.VERMELHO + f"Erro: {msg_pontos}" + cores.NORMAL)
        else:
            limpar_terminal()
            print(cores.AMARELO + "Compra cancelada." + cores.NORMAL)
        
        enter_continuar()