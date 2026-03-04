"""
Steampunk Desktop Client for the SAE32 Search Engine.
Theme: Brass, Copper, and Victorian Engineering.
"""

from __future__ import annotations

import json
import socket
import threading
import tkinter as tk
from tkinter import messagebox, ttk

# --- Network Configuration ---
SERVER_HOST: str = "127.0.0.1"
SERVER_PORT: int = 65432
BUFFER_SIZE: int = 65536 # Increased buffer for large search transmissions


class SteampunkSearchApp:
    """
    Main client with a Victorian Industrial / Steampunk aesthetic.
    """

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("⚙️ VICTORIAN DATA RETRIEVAL ENGINE")
        self.root.geometry("1100x750")

        # --- Steampunk Color Palette ---
        self.color_iron = "#1a1613"      # Background (Dark Iron)
        self.color_leather = "#2d241e"   # Surface (Old Leather)
        self.color_copper = "#b87333"    # Main Accents (Copper)
        self.color_brass = "#d4af37"     # Secondary Accents (Brass)
        self.color_ink = "#eaddca"       # Text (Vintage Paper/Ink)
        self.color_rust = "#8b4513"      # Warning/Border (Rust)

        self.root.configure(bg=self.color_iron)
        self._setup_steampunk_styles()

        self.client_socket: socket.socket | None = None
        self.is_connected: bool = False

        self._build_ui()
        self.start_connection_thread()

    def _setup_steampunk_styles(self) -> None:
        """Configures the UI to look like a brass-mounted machine."""
        style = ttk.Style()
        style.theme_use("clam")

        # Main Containers
        style.configure("TFrame", background=self.color_iron)
        style.configure(
            "TLabelframe",
            background=self.color_leather,
            foreground=self.color_brass,
            bordercolor=self.color_rust,
            thickness=2,
            relief="ridge"
        )
        style.configure(
            "TLabelframe.Label",
            background=self.color_leather,
            foreground=self.color_copper,
            font=("Georgia", 11, "bold", "italic")
        )

        # Labels & Buttons
        style.configure(
            "TLabel", 
            background=self.color_leather, 
            foreground=self.color_ink, 
            font=("Georgia", 10)
        )
        
        # Brass Button Style
        style.configure(
            "Brass.TButton",
            background=self.color_rust,
            foreground=self.color_brass,
            font=("Georgia", 10, "bold"),
            borderwidth=3,
            relief="raised"
        )
        style.map(
            "Brass.TButton",
            background=[("active", self.color_copper)],
            foreground=[("active", self.color_iron)]
        )

        # Treeview (The Archive List)
        style.configure(
            "Treeview",
            background="#251f1a",
            foreground=self.color_ink,
            fieldbackground="#251f1a",
            rowheight=30,
            font=("Courier New", 10)
        )
        style.configure(
            "Treeview.Heading",
            background=self.color_leather,
            foreground=self.color_brass,
            font=("Georgia", 10, "bold")
        )

    def _build_ui(self) -> None:
        """Constructs the mechanical-looking interface."""
        
        # --- Top Header ---
        header = tk.Frame(self.root, bg=self.color_iron, pady=20)
        header.pack(fill="x")
        
        title_label = tk.Label(
            header, 
            text="⚙ ARCHIVAL INDEXING APPARATUS ⚙", 
            font=("Times New Roman", 22, "bold"),
            bg=self.color_iron, 
            fg=self.color_copper
        )
        title_label.pack()

        # --- Control Panel (Search) ---
        panel_frame = ttk.LabelFrame(self.root, text=" INPUT MECHANISM ", padding=20)
        panel_frame.pack(fill="x", padx=30, pady=10)

        # Pattern Input
        input_sub = ttk.Frame(panel_frame)
        input_sub.pack(fill="x", pady=(0, 15))

        ttk.Label(input_sub, text="KEYWORD PATTERN:").pack(side="left")
        self.entry_query = tk.Entry(
            input_sub, 
            bg="#120f0d", 
            fg=self.color_brass, 
            insertbackground=self.color_brass,
            font=("Courier New", 12),
            bd=2,
            relief="sunken"
        )
        self.entry_query.pack(side="left", fill="x", expand=True, padx=10)
        self.entry_query.bind("<Return>", lambda _: self.on_search())

        self.btn_search = ttk.Button(
            input_sub, 
            text="ENGAGE ENGINE", 
            style="Brass.TButton", 
            command=self.on_search
        )
        self.btn_search.pack(side="right")

        # Options
        options_sub = ttk.Frame(panel_frame)
        options_sub.pack(fill="x")

        self.var_regex = tk.BooleanVar()
        ttk.Checkbutton(options_sub, text="Advanced Regex Calculus", variable=self.var_regex).pack(side="left", padx=(0, 20))

        ttk.Label(options_sub, text="DOCUMENT TYPES:").pack(side="left", padx=(10, 5))
        self.ext_vars = {ext: tk.BooleanVar(value=True) for ext in [".txt", ".html", ".pdf", ".xlsx"]}
        for ext, var in self.ext_vars.items():
            ttk.Checkbutton(options_sub, text=ext.upper(), variable=var).pack(side="left", padx=10)

        # --- Results Feed ---
        archive_frame = ttk.LabelFrame(self.root, text=" RETRIEVED MANUSCRIPTS ", padding=10)
        archive_frame.pack(fill="both", expand=True, padx=30, pady=10)

        cols = ("file", "type", "loc", "ctx")
        self.tree = ttk.Treeview(archive_frame, columns=cols, show="headings")
        
        headings = {"file": "SOURCE FILENAME", "type": "FORMAT", "loc": "COORDINATES", "ctx": "TEXT EXCERPT"}
        for col, text in headings.items():
            self.tree.heading(col, text=text)
            self.tree.column(col, width=150 if col != "ctx" else 550)

        scroll = ttk.Scrollbar(archive_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        # --- Status Gauge (Footer) ---
        self.status_var = tk.StringVar(value="MACHINE STATUS: IDLE")
        status_bar = tk.Label(
            self.root, 
            textvariable=self.status_var, 
            bg="#000000", 
            fg=self.color_brass,
            anchor="w",
            font=("Courier New", 9, "italic"),
            padx=15,
            pady=5
        )
        status_bar.pack(side="bottom", fill="x")

    # --- Communication Methods ---

    def start_connection_thread(self) -> None:
        threading.Thread(target=self._connect, daemon=True).start()

    def _connect(self) -> None:
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((SERVER_HOST, SERVER_PORT))
            self.is_connected = True
            self.status_var.set(f"MACHINE STATUS: LINKED TO CORE @ {SERVER_HOST}")
        except Exception as e:
            self.is_connected = False
            self.status_var.set(f"MACHINE STATUS: CONNECTION SEVERED - {e}")

    def on_search(self) -> None:
        if not self.is_connected:
            messagebox.showwarning("MECHANICAL FAILURE", "The telegraph line is down. Check the server.")
            return

        query = self.entry_query.get().strip()
        if not query: return

        selected_exts = [ext for ext, var in self.ext_vars.items() if var.get()]
        payload = {"query": query, "extensions": selected_exts, "regex": self.var_regex.get()}

        for i in self.tree.get_children(): self.tree.delete(i)
        self.status_var.set(f"MACHINE STATUS: CALIBRATING FOR '{query}'...")

        threading.Thread(target=self._send_request, args=(payload,), daemon=True).start()

    def _send_request(self, payload: dict) -> None:
        try:
            self.client_socket.sendall(json.dumps(payload).encode("utf-8"))
            self.client_socket.settimeout(5.0)
            data = self.client_socket.recv(BUFFER_SIZE)
            self.client_socket.settimeout(None)

            if data:
                results = json.loads(data.decode("utf-8"))
                self.root.after(0, self._display_results, results)
        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f"MACHINE STATUS: ERROR - {e}"))

    def _display_results(self, results: list[dict]) -> None:
        self.status_var.set(f"MACHINE STATUS: {len(results)} RECORDS RETRIEVED SUCCESSFULLY.")
        for res in results:
            self.tree.insert("", "end", values=(
                res.get("file", "Unknown"),
                res.get("type", "N/A"),
                res.get("location", "N/A"),
                res.get("context", "N/A")
            ))

if __name__ == "__main__":
    root = tk.Tk()
    app = SteampunkSearchApp(root)
    root.mainloop()