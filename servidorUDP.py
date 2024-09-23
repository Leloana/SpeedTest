import socket
import time

# Configurações do servidor
HOST = '0.0.0.0'  # Endereço IP do servidor
PORT = 12345      # Porta do servidor

pacotes_recebidos = 0

def format_all_speeds(bps):
    gbps = bps / 10**9
    mbps = bps / 10**6
    kbps = bps / 10**3
    return (
        f"{gbps:,.2f} Gbps\n"
        f"{mbps:,.2f} Mbps\n"
        f"{kbps:,.2f} Kbps\n"
        f"{bps:,.2f} bps"
    )

def generate_test_string():
    base_string = "teste de rede *2024*"
    repeated_string = (base_string * (500 // len(base_string)))[:500]
    return repeated_string.encode('utf-8')  # Converter para bytes

def handle_client(server_socket, client_addr):
    global pacotes_recebidos
    print(f"Connected to {client_addr}\n")

    # FASE 1: Receber dados do cliente (Upload)
    start_time = time.time()
    data_received = 0
    packet_count = 0
    while True:
        data, addr = server_socket.recvfrom(500)  # Recebe 500 bytes por vez
        if b'UPLOAD_COMPLETE' in data:
            print("Fim da Fase 1")
            break
        if not data:
            print("Nenhum dado recebido, encerrando")
            break
        data_received += len(data)
        packet_count += 1
    end_time = time.time()

    upload_time = end_time - start_time
    upload_bps = (data_received * 8) / upload_time
    upload_pps = packet_count / upload_time
    print(f"Tempo de download: {upload_time} segundos")
    print(f"Taxa de download: {format_all_speeds(upload_bps)}")
    print(f"Pacotes por segundo: {upload_pps:,.2f}")
    print(f"Pacotes recebidos: {packet_count:,}")
    print(f"Bytes recebidos: {data_received:,} bytes\n")
    pacotes_recebidos = packet_count

def start_udp_server():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((HOST, PORT))
        print(f"Started an UDP server -> port: {PORT}...")

        while True:
            data, client_addr = server_socket.recvfrom(500)  # Recebe qualquer dado para iniciar
            print(f"New connection from {client_addr}")
            handle_client(server_socket, client_addr)
            pacotes_enviados = int(input("Pacotes enviados: "));
            print("Pacotes perdidos = " + str(pacotes_enviados-pacotes_recebidos))
            break

