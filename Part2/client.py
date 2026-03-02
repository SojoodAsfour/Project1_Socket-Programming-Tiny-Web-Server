from socket import *

server_host = gethostname()  # Get the local machine hostname
server_port = 8090           # Define the server port to connect
server_port_udp = 8010

def main():
    # TCP section
    clientTCPSocket = socket(AF_INET, SOCK_STREAM)
    clientTCPSocket.connect((server_host, server_port))

    # UDP section - NO BIND needed for client!
    clientUDPSocket = socket(AF_INET, SOCK_DGRAM)

    # Send start message over TCP
    startMsg = "START"
    clientTCPSocket.send(startMsg.encode())
    print("TCP Client sent:", startMsg)
    print()

    print("Sending numbers 0 → 1,000,000 via UDP...\n")
    for num in range(1000001):
        # Send each number as a separate UDP packet
        clientUDPSocket.sendto(str(num).encode(), (server_host, server_port_udp))
        # Print progress every 100,000 numbers
        if num % 100000 == 0:
            print(f"Sent: {num}")

    # Close the UDP socket after sending all numbers
    clientUDPSocket.close()
    print("\nFinished sending all numbers...")

    # Send end message over TCP
    endMsg = "END"
    clientTCPSocket.send(endMsg.encode())
    print("TCP Sent:", endMsg)

    # Close the TCP connection
    clientTCPSocket.close()


if __name__ == "__main__":
    main()