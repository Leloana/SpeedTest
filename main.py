from servidorUDP import start_udp_server
from clienteUDP import start_udp_client
from servidor import start_tcp_server
from cliente import start_tcp_client
import socket

def get_local_ip():
    # Conecta a um endereço externo para determinar o IP local, sem enviar dados reais
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # O endereço de destino e a porta não importam
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception as e:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

if __name__ == "__main__":
    tipo = input("UDP ou TCP?")
    formato = input("server ou client?")
    
    if formato == "server": print(get_local_ip())
    else : 
        ipServer = input("Insira ip do servidor: ")

    if tipo == "UDP" :
        if formato == "client": start_udp_client()
        else: start_tcp_server()
    else :
        if formato == "client": start_tcp_client()
        else: start_tcp_server()