# -------------------------------------------------
# STUDENT GRADE TRACKER PRO X — ULTRA MODERN BLACK
# Midnight Glassmorphism + Neon + Minimalist
# -------------------------------------------------

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import os
from avl_tree import AVLTree


class StudentGradeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Grade Tracker Pro X")
        self.root.geometry("1200x780")
        self.root.configure(bg="#0d0d0d")
        self.root.minsize(1000, 600)

        self.avl = AVLTree()
        self.avl_root = None
        self.node_widgets = {}

        self.setup_styles()
        self.build_ui()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        # Modern Button
        style.configure("Modern.TButton", font=("Inter", 10, "bold"), padding=10)
        style.map("Modern.TButton",
                  background=[('active', '#1a1a1a'), ('!disabled', '#111')],
                  foreground=[('active', '#00ff88')])

        # Tab style
        style.configure("TNotebook", background="#0d0d0d", borderwidth=0)
        style.configure("TNotebook.Tab", padding=[15, 8], font=("Inter", 11))
        style.map("TNotebook.Tab",
                  background=[("selected", "#1a1a1a"), ("active", "#222")],
                  foreground=[("selected", "#00ff88"), ("active", "#ffffff")])

    def build_ui(self):
        # === GLASS HEADER ===
        header = tk.Frame(self.root, bg="#000000", height=70, bd=0)
        header.pack(fill='x', pady=(0, 10))
        header.pack_propagate(False)

        title = tk.Label(header, text="STUDENT GRADE TRACKER PRO X", font=("Inter", 22, "bold"),
                         bg="#000000", fg="#00ff88", anchor='w')
        title.pack(side='left', padx=30, pady=15)

        # === MAIN CONTAINER ===
        main_container = tk.Frame(self.root, bg="#0d0d0d")
        main_container.pack(fill='both', expand=True, padx=20, pady=10)

        # === LEFT PANEL - GLASS CARD ===
        left_card = tk.Frame(main_container, bg="#111111", relief='flat', bd=0)
        left_card.pack(side='left', fill='y', padx=(0, 15))
        left_card.configure(highlightbackground="#333", highlightthickness=1)

        # Title
        tk.Label(left_card, text="Student Record", font=("Inter", 14, "bold"),
                 bg="#111111", fg="#00ff88").pack(pady=(20, 15), anchor='w', padx=25)

        # Form Fields
        self.entries = {}
        fields = [("ID", "id"), ("Name", "name"), ("Grade", "grade")]
        for label_text, key in fields:
            frame = tk.Frame(left_card, bg="#111111")
            frame.pack(fill='x', padx=25, pady=8)

            tk.Label(frame, text=label_text, font=("Inter", 10), bg="#111111", fg="#aaaaaa").pack(anchor='w')
            entry = tk.Entry(frame, font=("Inter", 11), bg="#1a1a1a", fg="white",
                             insertbackground="#00ff88", relief='flat', bd=0, highlightthickness=1,
                             highlightbackground="#333")
            entry.pack(fill='x', pady=(4, 0), ipady=8)
            self.entries[key] = entry

        # Buttons - Neon Glow
        btn_frame = tk.Frame(left_card, bg="#111111")
        btn_frame.pack(pady=20, padx=25, fill='x')

        buttons = [
            ("Add / Update", self.add_student, "#00cc66"),
            ("Search", self.search_student, "#0099ff"),
            ("Delete", self.delete_student, "#ff3366"),
            ("Show All", self.show_all, "#ff9900"),
            ("Export CSV", self.export_csv, "#9966ff")
        ]
        for i, (text, cmd, base_color) in enumerate(buttons):
            btn = tk.Button(btn_frame, text=text, command=cmd,
                            bg=base_color, fg="white", font=("Inter", 10, "bold"),
                            relief='flat', bd=0, cursor="hand2", padx=15, pady=10)
            btn.pack(fill='x', pady=6)
            btn.bind("<Enter>", lambda e, b=btn, c=base_color: b.configure(bg=self.glow(c)))
            btn.bind("<Leave>", lambda e, b=btn, c=base_color: b.configure(bg=c))

        # === RIGHT PANEL - TABS ===
        right_panel = tk.Frame(main_container, bg="#0d0d0d")
        right_panel.pack(side='right', fill='both', expand=True)

        tab_control = ttk.Notebook(right_panel, style="TNotebook")
        tab_control.pack(fill='both', expand=True, padx=5, pady=5)

        # Tab 1: Output Log
        log_tab = tk.Frame(tab_control, bg="#0f0f0f")
        tab_control.add(log_tab, text=" Output Log ")

        self.output = tk.Text(log_tab, bg="#0f0f0f", fg="#00ff88", font=("Consolas", 11),
                              wrap='word', relief='flat', bd=0, insertbackground="#00ff88",
                              selectbackground="#003311")
        scroll = tk.Scrollbar(log_tab, command=self.output.yview, bg="#333", troughcolor="#0f0f0f")
        self.output.configure(yscrollcommand=scroll.set)
        self.output.pack(side='left', fill='both', expand=True, padx=(15, 0), pady=15)
        scroll.pack(side='right', fill='y', padx=(0, 15), pady=15)
        self.log("System initialized. Ready.", "#00ff88")

        # Tab 2: AVL Tree View
        tree_tab = tk.Frame(tab_control, bg="#0f0f0f")
        tab_control.add(tree_tab, text=" AVL Tree ")

        self.canvas = tk.Canvas(tree_tab, bg="#0f0f0f", highlightthickness=0)
        self.canvas.pack(fill='both', expand=True, padx=20, pady=20)
        self.canvas.bind("<Configure>", lambda e: self.draw_tree())

    def glow(self, hex_color):
        rgb = tuple(int(hex_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        glow = tuple(min(255, int(c * 1.4)) for c in rgb)
        return f"#{glow[0]:02x}{glow[1]:02x}{glow[2]:02x}"

    def log(self, text, color="#00ff88"):
        self.output.insert(tk.END, f"» {text}\n", f"tag_{color}")
        self.output.tag_config(f"tag_{color}", foreground=color)
        self.output.see(tk.END)

    def add_student(self):
        try:
            sid = int(self.entries['id'].get().strip())
            name = self.entries['name'].get().strip()
            grade = self.entries['grade'].get().strip()
            if not name or not grade: raise ValueError
            self.avl_root = self.avl.insert(self.avl_root, sid, name, grade)
            self.log(f"Added: {sid} | {name} | {grade}", "#00cc66")
            self.clear_entries()
            self.draw_tree()
        except:
            messagebox.showerror("Invalid", "ID must be number. Name & Grade required.")

    def search_student(self):
        try:
            sid = int(self.entries['id'].get().strip())
            self.log(f"Searching: {sid}...", "#0099ff")
            node = self.avl.search(self.avl_root, sid)
            if node:
                self.log(f"FOUND → {node.student_id} | {node.name} | {node.grade}", "#00ff88")
                self.highlight_node(sid)
            else:
                self.log("Not found.", "#ff6666")
        except:
            messagebox.showerror("Error", "Enter valid ID.")

    def delete_student(self):
        try:
            sid = int(self.entries['id'].get().strip())
            old = self.avl_root
            self.avl_root = self.avl.delete(self.avl_root, sid)
            if old is not self.avl_root:
                self.log(f"Deleted: {sid}", "#ff3366")
            else:
                self.log(f"ID {sid} not found.", "#ff9966")
            self.clear_entries()
            self.draw_tree()
        except:
            pass

    def show_all(self):
        result = []
        self.avl.inorder(self.avl_root, result)
        self.log("ALL STUDENTS (sorted):", "#ff9900")
        for s in result:
            self.log(f"   {s}", "#cccccc")
        self.draw_tree()

    def export_csv(self):
        if not self.avl_root:
            messagebox.showinfo("Empty", "No data.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
        if path:
            result = []
            self.avl.inorder(self.avl_root, result)
            with open(path, 'w', newline='', encoding='utf-8') as f:
                w = csv.writer(f)
                w.writerow(["ID", "Name", "Grade"])
                for line in result:
                    parts = line.replace("ID: ", "").split(" | ")
                    w.writerow(parts)
            self.log(f"Exported: {os.path.basename(path)}", "#9966ff")

    def clear_entries(self):
        for e in self.entries.values(): e.delete(0, tk.END)

    # === TREE VISUALIZATION ===
    def draw_tree(self):
        self.canvas.delete("all")
        self.node_widgets.clear()
        if self.avl_root:
            w = self.canvas.winfo_width()
            self._draw_node(self.avl_root, w // 2, 80, min(w // 4, 280))

    def _draw_node(self, node, x, y, dx):
        if not node: return
        left_x = x - dx
        right_x = x + dx
        next_y = y + 100

        self._draw_node(node.left, left_x, next_y, dx * 0.6)
        self._draw_node(node.right, right_x, next_y, dx * 0.6)

        if node.left:
            self.canvas.create_line(x, y + 20, left_x, next_y - 20, fill="#333", width=2, smooth=True)
        if node.right:
            self.canvas.create_line(x, y + 20, right_x, next_y - 20, fill="#333", width=2, smooth=True)

        # Modern Node
        r = 32
        fill = "#00ff88" if node.student_id == int(self.entries['id'].get() or -1) else "#1a1a1a"
        outline = "#00ff88" if node.student_id in self.node_widgets else "#444"

        oval = self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=fill, outline=outline, width=2)
        self.canvas.create_text(x, y-8, text=str(node.student_id), fill="white", font=("Inter", 13, "bold"))
        self.canvas.create_text(x, y+14, text=node.name[:9], fill="#aaffaa", font=("Inter", 9))

        self.node_widgets[node.student_id] = oval

    def highlight_node(self, sid):
        if sid in self.node_widgets:
            obj = self.node_widgets[sid]
            self.canvas.itemconfig(obj, outline="#00ff88", width=4)
            self.root.after(1800, lambda: self.canvas.itemconfig(obj, outline="#444", width=2))


# ==================== RUN ====================
if __name__ == "__main__":
    root = tk.Tk()
    app = StudentGradeApp(root)
    root.mainloop()