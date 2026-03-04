"""
Multi-threaded TCP Server module for the SAE32 application.

This module handles incoming client connections, parses search requests 
formatted as JSON, and dispatches them to the search_engine logic.
Each client is served in a dedicated background thread.
"""

from __future__ import annotations

import json
import socket
import threading
from typing import Tuple

# Importing our custom search logic module
import search_engine

# --- Network Configuration ---
SERVER_HOST: str = "127.0.0.1"  # Localhost
SERVER_PORT: int = 52300        # Arbitrary non-privileged port
BUFFER_SIZE: int = 4096         # Maximum data size per receive call (4KB)
MAX_LISTEN: int = 5             # Maximum number of queued connections


def handle_client_connection(connection: socket.socket, address: Tuple[str, int]) -> None:
    """
    Main loop to handle a single client session until they disconnect.

    Args:
        connection: The socket object for the connected client.
        address: A tuple containing the client's IP and port.
    """
    print(f"[NEW CONNECTION] Client connected from {address}")

    try:
        while True:
            # Receive incoming data from the client
            data = connection.recv(BUFFER_SIZE)
            
            # Empty data indicates the client has closed the connection
            if not data:
                break

            try:
                # Expecting a JSON payload: {"query": str, "extensions": list, "regex": bool}
                request = json.loads(data.decode("utf-8"))
                
                query = request.get("query", "")
                exts = request.get("extensions", [])
                regex = request.get("regex", False)

                print(f"[{address}] Processing query: {query!r} | Filter: {exts} | Regex: {regex}")

                # Execute search via the engine module
                results = search_engine.process_search(query, exts, regex)

                # Ensure we always return a valid list to the client
                if results is None:
                    results = []

                # Serialize results back to JSON and send to client
                response_json = json.dumps(results)
                connection.sendall(response_json.encode("utf-8"))

            except json.JSONDecodeError:
                print(f"[ERROR] [{address}] Sent invalid JSON payload.")
                break

            except Exception as error:
                print(f"[ERROR] [{address}] Unexpected error during processing: {error}")
                break

    finally:
        # Clean up the connection resources
        connection.close()
        print(f"[DISCONNECTED] Connection with {address} closed.")


def start_server() -> None:
    """
    Initializes and starts the TCP server.
    
    Listens for incoming connections and spawns a new daemon thread 
    for every client to allow concurrent search requests.
    """
    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Allow the server to restart immediately without waiting for timeout
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server_socket.bind((SERVER_HOST, SERVER_PORT))
        server_socket.listen(MAX_LISTEN)

        print(f"[STARTING] TCP Server listening on {SERVER_HOST}:{SERVER_PORT}")
        print("[INFO] Waiting for client connections...")

        while True:
            # Accept new connection
            conn, addr = server_socket.accept()
            
            # Create a daemon thread: it will exit automatically when the main program stops
            thread = threading.Thread(
                target=handle_client_connection,
                args=(conn, addr),
                daemon=True,
            )
            thread.start()
            print(f"[ACTIVE THREADS] Total clients connected: {threading.active_count() - 1}")

    except Exception as error:
        print(f"[CRITICAL ERROR] Server startup failed: {error}")

    finally:
        server_socket.close()
        print("[SHUTDOWN] Server socket has been closed.")


if __name__ == "__main__":
    start_server()