# SAE 3.02 - Communicating Search Applications

## Overview
This repository provides a simple client-server search application written in Python. A client connects to the server and submits keyword queries; the server searches files stored under `storage/` and returns matching results (file names and locations).

## Features
- Search across multiple file formats: `.txt`, `.pdf`, and `.xlsx`.
- Returns filename and contextual locations (lines for text, page numbers for PDFs, sheet/cell ranges for Excel).
- Simple TCP-based client-server communication suitable for learning and extension.

## Repository layout
- `server/`
  - `main_server.py` — server entry point
  - `search_engine.py` — search logic and file parsers
  - `utils.py` — helper functions
- `client/`
  - `main_client.py` — client entry point
- `storage/` — sample files and documents to search
- `R302_files/` — course assets and example resources (CSS, JS, MathJax, PHP snippets)
- `requirements.txt` — Python dependencies

## Requirements
- Python 3.10+ (or compatible)
- See `requirements.txt` for required Python packages (for example: `pandas`, `openpyxl`, `PyPDF2`).

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Matrocco/SA-302.git
   cd SA-302
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Start the server (default host `127.0.0.1`, port `5000` unless changed):
   ```bash
   python server/main_server.py
   ```
2. In another terminal, run the client and enter queries:
   ```bash
   python client/main_client.py
   ```
3. Type a keyword and press Enter. The client will display matches returned by the server.

Notes:
- Put files you want indexed/searched in the `storage/` directory.
- Adjust host/port settings in the scripts if your environment requires it.

## Development notes
- The main search logic lives in `server/search_engine.py`. Extend or improve parsers there to add more file formats or richer context extraction.
- Communication is currently implemented with plain TCP sockets; consider using HTTP or WebSocket for production scenarios.

## License & Contact
This repository is intended for educational use. Add an appropriate license before publishing.

If you'd like, I can also:
- add a minimal `requirements.txt` example,
- provide simple run scripts (`./run-server.sh`, `./run-client.sh`),
- or run a quick lint and smoke test.
