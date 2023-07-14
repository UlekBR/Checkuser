#!/bin/bash

# Função para exibir a mensagem de ajuda
function exibir_ajuda() {
    echo "Uso: ./install_checkuser.sh"
    echo "Instala e executa o script checkuser.py em segundo plano."
    echo ""
    echo "Opções:"
    echo "  -h, --help      Exibe esta mensagem de ajuda"
}

# Verifica se o usuário pediu ajuda
if [[ $1 == "-h" || $1 == "--help" ]]; then
    exibir_ajuda
    exit 0
fi

# Verifica se o script está sendo executado como root
if [[ $EUID -ne 0 ]]; then
   echo "Este script precisa ser executado como root"
   exit 1
fi

# Verifica se o Python 3 está instalado
if ! command -v python3 &> /dev/null; then
    echo "O Python 3 não está instalado. Por favor, instale-o antes de prosseguir."
    exit 1
fi

# Instalação das dependências do Python
pip3 install flask

# Solicita ao usuário para digitar a porta
read -p "Digite a porta desejada: " porta

# Criação do arquivo de serviço systemd
servico="[Unit]
Description=Script CheckUser
After=network.target

[Service]
ExecStart=/usr/bin/python3 checkuser.py -port $porta
WorkingDirectory=$(pwd)
StandardOutput=null

[Install]
WantedBy=multi-user.target"

echo "$servico" > /etc/systemd/system/checkuser.service

# Recarrega os serviços do systemd
systemctl daemon-reload

# Inicia o serviço
systemctl start checkuser

# Habilita o serviço para iniciar automaticamente na inicialização do sistema
systemctl enable checkuser

# Exibe a mensagem de conclusão
echo "O serviço CheckUser foi instalado e está sendo executado na porta $porta."
echo "Para verificar o status do serviço:"
echo "  systemctl status checkuser"
