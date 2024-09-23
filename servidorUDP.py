import socket
import time

# Configurações do servidor
HOST = '0.0.0.0'  # Endereço IP do servidor
PORT = 12345      # Porta do servidor

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

    # FASE 2: Enviar dados ao cliente (Download)
    try:
        data_to_send = generate_test_string()  # Gera uma string de 500 bytes
        packet_size = 500
        total_bytes_sent = 0
        packet_count = 0
        start_time = time.time()

        while time.time() - start_time < 20:  # Envia pacotes por 20 segundos
            try:
                server_socket.sendto(data_to_send, client_addr)
                total_bytes_sent += packet_size
                packet_count += 1
            except socket.error as e:
                print(f"Erro ao enviar dados: {e}")
                break
        end_time = time.time()

        download_time = end_time - start_time
        if download_time == 0:
            download_time = 1e-9  # Prevenir divisão por zero

        download_bps = (total_bytes_sent * 8) / download_time  # bits por segundo
        download_pps = packet_count / download_time
        print(f"Tempo de upload: {download_time} segundos")
        print(f"Taxa de upload: {format_all_speeds(download_bps)}")
        print(f"Pacotes por segundo: {download_pps:,.2f}")
        print(f"Pacotes enviados: {packet_count:,}")
        print(f"Bytes enviados: {total_bytes_sent:,} bytes")

        # Enviar mensagem especial para indicar o fim dos dados
        server_socket.sendto(b'UPLOAD_COMPLETE', client_addr)

    except socket.error as e:
        print(f"Error to sent client data: {e}\n")
    finally:
        print("Ending client connection.\n")

def start_udp_server():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((HOST, PORT))
        print(f"Started an UDP server -> port: {PORT}...")

        while True:
            data, client_addr = server_socket.recvfrom(500)  # Recebe qualquer dado para iniciar
            print(f"New connection from {client_addr}")
            handle_client(server_socket, client_addr)
            input("Finalizar")
            break

