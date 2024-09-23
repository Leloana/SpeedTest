import socket
import time

HOST = '0.0.0.0'  
PORT = 65432 

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

def handle_client(conn):
    with conn:
        print(f"Connected to {conn.getpeername()}\n")

        start_time = time.time()
        data_received = 0
        packet_count = 0
        while True:
            data = conn.recv(500)  # Recebe 500 bytes por vez
            if b'UPLOAD_COMPLETE' in data:
                break
            if not data:
                break
            data_received += len(data)
            packet_count += 1
        end_time = time.time()

        upload_time = end_time - start_time 
        upload_bps = (data_received * 8) / upload_time
        upload_pps = packet_count / upload_time 
        print(f"Tempo de download: {upload_time} segundos")
        print(f"Taxa de Download:{format_all_speeds(upload_bps)}")
        print(f"Pacotes por segundo: {upload_pps:,.2f}")
        print(f"Pacotes recebidos: {packet_count:,}")
        print(f"Bytes recebidos: {data_received:,} bytes\n")

        # FASE 2: Enviar dados ao cliente
        try:
            data_to_send = generate_test_string()  # String de 500 bytes
            packet_size = 500
            total_bytes_sent = 0
            packet_count = 0
            start_time = time.time()

            while time.time() - start_time < 20:
                try:
                    conn.sendall(data_to_send)
                    total_bytes_sent += packet_size
                    packet_count += 1
                except socket.error as e:
                    print(f"Upload concluido")
                    break
            end_time = time.time()

            download_time = end_time - start_time 
            print(f"Tempo de upload: {download_time} segundos")
            if download_time == 0:
                download_time = 1e-9  # Prevenir divisão por zero

            download_bps = (total_bytes_sent * 8) / download_time  # bits por segundo   
            download_pps = packet_count / download_time 
            print(f"Taxa de Upload:\n{format_all_speeds(download_bps)}")
            print(f"Pacotes por segundo: {download_pps:,.2f}")
            print(f"Pacotes enviados: {packet_count:,}")
            print(f"Bytes enviados: {total_bytes_sent:,} bytes")

            try:
                conn.sendall(b'UPLOAD_COMPLETE')
            except socket.error:
                print("Connection is not possible.")

        except socket.error as e:
            print(f"Error to sent client data: {e}\n")
        finally:
            print("Ending client connection.\n")

def start_tcp_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Started an TCP server -> port:{PORT}...")

        while True:
            conn, addr = s.accept() 
            print(f"New connection from {addr}")
            handle_client(conn) 
            input("Finalizar")
            break