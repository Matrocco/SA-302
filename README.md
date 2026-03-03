# SAE 3.02 - Communicating Search Applications

## Project Overview
This project is a client-server application developed in Python. It allows clients to connect to a server and search for specific keywords across multiple file formats (Text, PDF, and Excel) stored on the server.

## Features
- **Multi-format search**: Supports `.txt`, `.pdf`, and `.xlsx` files.
- **Detailed feedback**: Returns filenames and specific locations (lines or pages) where matches were found.
- **Robust Connection**: The server automatically detects client disconnection when the application is closed.
- **Clean Code**: Follows PEP 8 guidelines with English naming conventions and internal documentation.

## Installation
1. Clone this repository.
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Linux/macOS
   
SAE3.02-Network-Search/
├── server/
│   ├── main_server.py    # Point d'entrée du serveur
│   ├── file_parser.py    # Fonctions de recherche (PDF, Excel, etc.)
│   └── storage/          # Dossier contenant les fichiers .txt, .pdf... (Chemin relatif !)
├── client/
│   └── main_client.py    # Interface client
├── requirements.txt      # Dépendances (pandas, openpyxl, PyPDF2)
└── README.md             # Documentation en anglais