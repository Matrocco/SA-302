import socket
import os
from file_parser import search_in_pdf, search_in_excel # Importing our tools

# --- CONSTANTS ---
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 52300
BUFFER_SIZE = 1024
FILES_DIRECTORY = "storage"

class SearchServer:
    """
    A robust server that disconnects only when the client closes the application.
    """
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen(5)
            print(f"[SERVER] Monitoring {FILES_DIRECTORY}. Waiting for connections...")

            while True:
                conn, addr = s.accept()
                print(f"[SERVER] New connection: {addr}")
                self.handle_client(conn)

    def handle_client(self, connection):
        """
        Handles data receipt until the socket is closed by the client.
        """
        with connection:
            try:
                while True:
                    data = connection.recv(BUFFER_SIZE)
                    if not data:
                        # This happens when the client closes the window/app
                        print("[SERVER] Client disconnected (Connection closed).")
                        break
                    
                    keyword = data.decode("utf-8").strip()
                    print(f"[QUERY] Searching for: '{keyword}'")
                    
                    results = self.scan_storage(keyword)
                    connection.sendall(results.encode("utf-8"))
            except ConnectionResetError:
                print("[SERVER] Client forcibly closed the page.")

    def scan_storage(self, keyword):
        """
        Iterates through the storage folder and calls appropriate parsers.
        """
        output = []
        if not os.path.exists(FILES_DIRECTORY):
            return "Server storage folder missing."

        for filename in os.listdir(FILES_DIRECTORY):
            path = os.path.join(FILES_DIRECTORY, filename)
            res = ""
            
            if filename.endswith(".txt"):
                res = self.parse_txt(path, keyword)
            elif filename.endswith(".pdf"):
                res = search_in_pdf(path, keyword)
            elif filename.endswith(".xlsx"):
                res = search_in_excel(path, keyword)

            if res:
                output.append(f"[{filename}] Matches found at: {res}")

        return "\n".join(output) if output else "No matches found."

    def parse_txt(self, path, keyword):
        """Simple text parser for .txt files."""
        matches = []
        with open(path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f, 1):
                if keyword.lower() in line.lower():
                    matches.append(str(i))
        return "Lines " + ", ".join(matches) if matches else ""

if __name__ == "__main__":
    SearchServer(SERVER_HOST, SERVER_PORT).start()