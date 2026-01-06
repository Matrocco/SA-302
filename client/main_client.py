import socket
import tkinter as tk
from tkinter import messagebox, scrolledtext

# Constants for server connection
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 52300
BUFFER_SIZE = 4096

class SearchClientIHM:
    def __init__(self, root):
        self.root = root
        self.root.title("Communicating Search Application - SAE3.02")
        self.root.geometry("600x500")

        # --- 1. Category Selection ---
        tk.Label(root, text="Step 1: Select document types", font=('Arial', 10, 'bold')).pack(pady=5)
        self.cat_vars = {
            "txt": tk.BooleanVar(value=True),
            "pdf": tk.BooleanVar(value=True),
            "xlsx": tk.BooleanVar(value=True)
        }
        cat_frame = tk.Frame(root)
        cat_frame.pack()
        for cat, var in self.cat_vars.items():
            tk.Checkbutton(cat_frame, text=cat.upper(), variable=var).pack(side=tk.LEFT, padx=10)

        # --- 2. Keyword and Mode ---
        tk.Label(root, text="Step 2: Enter keyword or Regex", font=('Arial', 10, 'bold')).pack(pady=5)
        self.keyword_entry = tk.Entry(root, width=50)
        self.keyword_entry.pack(pady=5)

        self.mode_var = tk.StringVar(value="normal")
        mode_frame = tk.Frame(root)
        mode_frame.pack()
        tk.Radiobutton(mode_frame, text="Normal Search", variable=self.mode_var, value="normal").pack(side=tk.LEFT)
        tk.Radiobutton(mode_frame, text="Regex Search", variable=self.mode_var, value="regex").pack(side=tk.LEFT)

        # --- 3. Action Button ---
        self.search_btn = tk.Button(root, text="Search on Server", command=self.send_request, bg="blue", fg="white")
        self.search_btn.pack(pady=10)

        # --- 4. Results Area ---
        tk.Label(root, text="Results:", font=('Arial', 10, 'bold')).pack()
        self.result_area = scrolledtext.ScrolledText(root, width=70, height=15)
        self.result_area.pack(pady=5)

    def send_request(self):
        """ Connects to the server and sends the search query. """
        keyword = self.keyword_entry.get()
        if not keyword:
            messagebox.showwarning("Warning", "Please enter a keyword.")
            return

        # Prepare the query string: "categories|keyword|mode"
        selected_cats = [cat for cat, var in self.cat_vars.items() if var.get()]
        if not selected_cats:
            messagebox.showwarning("Warning", "Please select at least one category.")
            return

        query = f"{','.join(selected_cats)}|{keyword}|{self.mode_var.get()}"

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((SERVER_HOST, SERVER_PORT)) #
                s.send(query.encode("utf8")) #
                
                # Receive multi-line response from server
                response = s.recv(BUFFER_SIZE).decode("utf8")
                
                self.result_area.delete(1.0, tk.END)
                self.result_area.insert(tk.END, response)
        except Exception as e:
            messagebox.showerror("Connection Error", f"Could not connect to server: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SearchClientIHM(root)
    root.mainloop()