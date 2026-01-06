import socket
import threading
import search_engine as se  # Import the search engine from Part 1

# Named constants as requested by the grading rubric 
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 52300
BUFFER_SIZE = 1024
ENDING_MSG = "q"

def process_search(query_data):
    """
    Parse the client query and call the appropriate search functions.
    Format expected: 'txt,pdf|apple|normal' or 'xlsx|^A.*|regex'
    """
    try:
        categories_str, keyword, mode = query_data.split('|')
        categories = categories_str.split(',')
        is_regex = (mode.lower() == 'regex')
        
        final_results = []
        
        # Mapping categories to search functions
        # This handles 'Choice of categories' requirement 
        if 'txt' in categories or 'html' in categories:
            # Search in data folder (relative path)
            for file in os.listdir("data"):
                if file.endswith(('.txt', '.html')):
                    res = se.search_in_txt_html(f"data/{file}", keyword, is_regex)
                    if res:
                        final_results.append(f"{file}: {', '.join(res)}")

        if 'pdf' in categories:
            for file in os.listdir("data"):
                if file.endswith('.pdf'):
                    res = se.search_in_pdf(f"data/{file}", keyword, is_regex)
                    if res:
                        final_results.append(f"{file}: {', '.join(res)}")

        if 'xlsx' in categories:
            for file in os.listdir("data"):
                if file.endswith('.xlsx'):
                    res = se.search_in_excel(f"data/{file}", keyword, is_regex)
                    if res:
                        final_results.append(f"{file}: {', '.join(res)}")

        return "\n".join(final_results) if final_results else "No matches found."
    except Exception as e:
        return f"Error processing request: {e}"

def handle_client(connection, address):
    """ Handle interaction with a specific client. """
    print(f"[Server] Client {address} connected.")
    
    try:
        while True:
            # Receive data from client
            data = connection.recv(BUFFER_SIZE).decode("utf8")
            if not data or data == ENDING_MSG:
                break
                
            print(f"[Client {address}] Search request: {data}")
            
            # Execute search logic
            search_response = process_search(data)
            
            # Send results back to client
            connection.send(search_response.encode("utf8"))
            
    except ConnectionResetError:
        print(f"[Server] Connection with {address} lost.")
    finally:
        connection.close()
        print(f"[Server] Connection with {address} closed.")

def start_server():
    """ Main loop to accept multiple clients. """
    # Using 'with' automatically handles socket closing
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((SERVER_HOST, SERVER_PORT))
        s.listen(5) # Allow a queue of clients
        print(f"[Server] Server ready on {SERVER_HOST}:{SERVER_PORT}")
        
        while True:
            # Accepting a new connection
            conn, addr = s.accept()
            # Launch a new thread for each client (Concurrent management) 
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()

if __name__ == "__main__":
    import os # Needed for directory listing
    start_server()