import socket
import threading

# Use named constants and relative paths
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 52300

def handle_client(connection, address):
    """ Handle individual client connection """
    print(f"[Server] New connection: {address}")
    # Logic to receive keywords and call search_engine.py goes here
    connection.close()

def start_server():
    """ Initialize and run the multi-threaded server  """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((SERVER_HOST, SERVER_PORT))
        s.listen()
        print(f"[Server] Listening on {SERVER_HOST}:{SERVER_PORT}")
        while True:
            conn, addr = s.accept()
            # Threading allows simultaneous clients 
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

if __name__ == "__main__":
    start_server()