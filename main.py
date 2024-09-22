from servidorUDP import start_udp_server
from clienteUDP import start_udp_client
from servidor import start_tcp_server
from cliente import start_tcp_client

if __name__ == "__main__":
    tipo = input("UDP ou TCP?")
    formato = input("server ou client?")

    if tipo == "UDP" :
        if formato == "client": start_udp_client
        else: start_tcp_server
    else :
        if formato == "client": start_tcp_client
        else: start_tcp_server