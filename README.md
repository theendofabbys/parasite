│ O uso inadequado destas ferramentas é ILEGAL e pode │
│ resultar em: │
│ • Penas de prisão │
│ • Multas pesadas │
│ • Processos criminais │
│ • Danos irreparáveis │
│ │
│ Use apenas em: │
│ ✅ Seus próprios servidores │
│ ✅ Laboratórios autorizados │
│ ✅ Ambientes controlados com permissão explícita │
│ ✅ Pesquisas acadêmicas éticas │
│ │
└────────────────────────────────────────────────────────────┘
Este repositório contém uma coleção de ferramentas educacionais para estudo de ataques de negação de serviço (DoS/DDoS). Desenvolvido para:

- 🔬 Entender vulnerabilidades de rede
- 📚 Praticar técnicas de segurança ofensiva
- 🛡️ Desenvolver contramedidas e defesas
- 🧪 Testar em ambientes controlados

## 🎯 **Ferramentas Incluídas**

| Ferramenta | Descrição | Protocolo | Porta Padrão |
|------------|-----------|-----------|--------------|
| **HTTP Flood** | Ataque de camada 7 (aplicação) | HTTP/HTTPS | 80/443 |
| **SYN Flood** | Ataque de camada 4 (transporte) | TCP | 80 |
| **UDP Flood** | Ataque de amplificação | UDP | 53 |
| **Slowloris** | Ataque de conexões lentas | HTTP | 80 |

## 📁 **Estrutura do Projeto**
dos-attack-tools/
├── main.py # Menu interativo (recomendado)
├── dos.py # Versão linha de comando
├── requirements.txt # Dependências do projeto
├── README.md # Este arquivo
├── tools/ # Módulos de ataque
│ ├── init.py
│ ├── http_flood.py
│ ├── syn_flood.py
│ ├── udp_flood.py
│ └── slowloris.py
└── venv/ # Ambiente virtual (opcional)
linha de comando... 
# HTTP Flood
python3 dos.py --type http --target http://exemplo.com --threads 50 --time 30

# SYN Flood (requer root)
sudo python3 dos.py --type syn --target 192.168.1.100 --port 80 --threads 20 --time 30

# UDP Flood
python3 dos.py --type udp --target 192.168.1.100 --port 53 --threads 10 --time 20

# Slowloris
python3 dos.py --type slowloris --target exemplo.com --port 80 --threads 100 --time 60


TTP Flood (http_flood.py)

    Envia requisições HTTP/HTTPS massivas

    Headers aleatórios para parecer legítimo

    Suporta GET, POST e HEAD

SYN Flood (syn_flood.py)

    Ataque de camada de transporte

    Requer privilégios de root

    Suporta IP spoofing

UDP Flood (udp_flood.py)

    Envia pacotes UDP aleatórios

    Eficaz para amplificação

    Bom para testar serviços DNS

Slowloris (slowloris.py)

    Mantém conexões HTTP abertas

    Consome recursos do servidor

    Baixo consumo de banda

⚠️ Requisitos

    Python 3.8 ou superior

    Linux/Unix (recomendado) ou Windows

    Root/admin para SYN Flood

    Conexão com internet

autor:azrael
