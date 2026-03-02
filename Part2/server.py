from socket import *
import time

server_port_tcp = 8090
server_port_udp = 8010

# ---------------- TCP ----------------
serverTCPSocket = socket(AF_INET, SOCK_STREAM)
serverTCPSocket.bind(("", server_port_tcp))
serverTCPSocket.listen(1)

print("TCP Server running on port", server_port_tcp)
print("UDP Server will run on port", server_port_udp)
print("============================================\n")

while True:
    print("Waiting for a TCP client...")

    connectionSocket, addr = serverTCPSocket.accept()
    print("TCP connection from:", addr)

    startMsg = connectionSocket.recv(1024).decode()
    if startMsg != "START":
        print("Invalid START message:", startMsg)
        connectionSocket.close()
        continue

    print("Received START - Beginning to receive UDP packets...")

    # ---------------- UDP ----------------
    serverUDPSocket = socket(AF_INET, SOCK_DGRAM)
    serverUDPSocket.bind(("", server_port_udp))
    serverUDPSocket.settimeout(0.001)  # 1ms timeout for non-blocking
    print(f"UDP Server listening on port {server_port_udp}\n")

    expected = 0
    received_count = 0
    out_of_order = 0

    connectionSocket.setblocking(False)

    finished = False
    end_time = None

    while not finished:
        # ---- UDP receive ----
        try:
            data, _ = serverUDPSocket.recvfrom(2048)
            num = int(data.decode())
            received_count += 1
            if num != expected:
                out_of_order += 1
            expected = num + 1
            
            # Progress indicator
            if received_count % 100000 == 0:
                print(f"Received: {received_count} packets")
                
        except timeout:
            pass  # normal timeout, continue
        except:
            pass  # other errors

        # ---- TCP check for END ----
        if not finished:
            try:
                msg = connectionSocket.recv(1024).decode()
                if msg == "END":
                    print("\nReceived END via TCP")
                    finished = True
            except:
                pass

    # ---------------- Results ----------------
    print("\n===== UDP SUMMARY =====")
    print(f"Total packets received: {received_count}")
    print(f"Expected packets: 1,000,001")
    print(f"Lost packets: {1000001 - received_count}")
    print(f"Out of order packets: {out_of_order}")
    print("========================\n")

    connectionSocket.close()
    serverUDPSocket.close()
    print("Server ready for next client.\n")