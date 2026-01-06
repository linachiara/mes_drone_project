import socket

# CONFIGURATION
LISTEN_IP = "127.0.0.1"
LISTEN_PORT = 5600
TARGET_IP = "10.42.0.93"  # Your Pi's IP
TARGET_PORT = 5600
BUFFER_SIZE = 65535

def main():
    # Create listening socket (From Gazebo)
    sock_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_in.bind((LISTEN_IP, LISTEN_PORT))

    # Create sending socket (To Pi)
    sock_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print(f"--- VIDEO BRIDGE STARTED ---")
    print(f"Listening on {LISTEN_IP}:{LISTEN_PORT}")
    print(f"Forwarding to {TARGET_IP}:{TARGET_PORT}")
    print(f"Press Ctrl+C to stop.")

    count = 0
    try:
        while True:
            data, addr = sock_in.recvfrom(BUFFER_SIZE)
            sock_out.sendto(data, (TARGET_IP, TARGET_PORT))
            
            # Print status every 100 packets so you know it's working
            count += 1
            if count % 500 == 0:
                print(f"Forwarded {count} packets...", end='\r')
    except KeyboardInterrupt:
        print("\nStopping bridge.")

if __name__ == "__main__":
    main()
