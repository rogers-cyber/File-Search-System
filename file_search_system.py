import os
import sys
import re
import fnmatch
import threading
import time
import pandas as pd
import PyPDF2
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as tb
from ttkbootstrap.constants import *

# =================== APP CONFIG ===================
APP_NAME = "File Search System"
APP_VERSION = "1.0.1"

# =================== APP ===================
app = tk.Tk()
style = tb.Style(theme="superhero")
app.title(f"{APP_NAME} {APP_VERSION}")
app.geometry("1230x680")

# =================== Utility ===================
def resource_path(file_name):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, file_name)

def show_about():
    messagebox.showinfo(
        f"About {APP_NAME} v{APP_VERSION}",

        f"{APP_NAME} v{APP_VERSION}\n"
        "Production Edition\n\n"

        "File Search System is a high-performance desktop utility designed to "
        "search large directory trees and inspect file contents with speed, accuracy, "
        "and clarity.\n\n"

        "Key Features\n"
        "────────────\n"
        "✔ Recursive Folder Search\n"
        "✔ Content Search (TXT, CSV, XLSX, PDF, XML)\n"
        "✔ Regex & Multi-Keyword Matching\n"
        "✔ Real-Time Progress, Speed & ETA\n"
        "✔ Match Preview (Line / Page / Cell / Tag)\n"
        "✔ Folder Exclusion Rules\n"
        "✔ File Type Filters (Glob Patterns)\n"
        "✔ Threaded Search (Non-Blocking UI)\n"
        "✔ One-Click Path Copy\n"
        "✔ Double-Click to Open Files\n"
        "✔ CSV Export of Results\n"
        "✔ Cross-Platform Support\n\n"

        "Built with Python, Tkinter & ttkbootstrap\n\n"

        "© 2026 Mate Technologies\n"
        "All rights reserved."
    )
    
try:
    app.iconbitmap(resource_path("logo.ico"))
except Exception:
    pass

# 👇 ADD MENU HERE
menubar = tk.Menu(app)
help_menu = tk.Menu(menubar, tearoff=0)
help_menu.add_command(label="About", command=show_about)
menubar.add_cascade(label="Help", menu=help_menu)
app.config(menu=menubar)

stop_flag = False

# ================= SEARCH SETTINGS =================
frame1 = tb.Labelframe(app, text="Search Settings", padding=10)
frame1.pack(fill="x", padx=10, pady=6)

root_path = tk.StringVar()
tb.Label(frame1, text="Root Folder:", width=12).pack(side="left")
tb.Entry(frame1, textvariable=root_path, width=50).pack(side="left", padx=6)
tb.Button(frame1, text="Browse", command=lambda: root_path.set(filedialog.askdirectory())).pack(side="left", padx=6)

search_var = tk.StringVar()
tb.Label(frame1, text="Search Term:", width=12).pack(side="left", padx=(12,0))
tb.Entry(frame1, textvariable=search_var, width=40).pack(side="left", padx=6)

regex_var = tk.BooleanVar()
tb.Checkbutton(frame1, text="Regex", variable=regex_var, bootstyle="info-round-toggle").pack(side="left", padx=12)

# ================= FILTERS =================
frame2 = tb.Labelframe(app, text="Filters", padding=10)
frame2.pack(fill="x", padx=10, pady=6)

file_filter = tk.StringVar(value="*")
exclude_folders = tk.StringVar(value="node_modules .git __pycache__")

tb.Label(frame2, text="File Types:", width=12).pack(side="left")
tb.Entry(frame2, textvariable=file_filter, width=30).pack(side="left", padx=6)
tb.Label(frame2, text="Example: *.txt *.csv *.xlsx *.pdf *.xml", foreground="#9ca3af").pack(side="left", padx=10)

tb.Label(frame2, text="Exclude Folders:", width=16).pack(side="left", padx=(12,2))
tb.Entry(frame2, textvariable=exclude_folders, width=40).pack(side="left", padx=6)

search_btn = tb.Button(frame2, text="🔍 SEARCH", bootstyle="success")
search_btn.pack(side="left", padx=6)

stop_btn = tb.Button(frame2, text="🛑 STOP", bootstyle="danger-outline", state="disabled")
stop_btn.pack(side="left", padx=6)

export_btn = tb.Button(frame2, text="📤 Export Results", bootstyle="primary-outline")
export_btn.pack(side="right", padx=6)

# ================= PROGRESS =================
frame3 = tb.Labelframe(app, text="Progress", padding=8)
frame3.pack(fill="x", padx=10)

progress_var = tk.IntVar()
tb.Progressbar(frame3, variable=progress_var, maximum=100, length=500).pack(side="left", padx=10)

eta_lbl = tb.Label(frame3, text="ETA: --")
eta_lbl.pack(side="left", padx=10)

spd_lbl = tb.Label(frame3, text="Speed: -- files/s")
spd_lbl.pack(side="left", padx=10)

counter_lbl = tb.Label(frame3, text="Matches: 0")
counter_lbl.pack(side="right", padx=10)

# ================= RESULTS TREEVIEW =================
frame4 = tb.Labelframe(app, text="Search Results (Click=Copy | Double-Click=Open)", padding=10)
frame4.pack(fill="both", expand=True, padx=10, pady=6)

cols = ("path", "preview")
tree = tb.Treeview(frame4, columns=cols, show="headings")
tree.heading("path", text="File Path")
tree.column("path", width=550, anchor="w")
tree.heading("preview", text="Match Preview")
tree.column("preview", width=500, anchor="w")
tree.pack(side="left", fill="both", expand=True)

scroll = tb.Scrollbar(frame4, orient="vertical", command=tree.yview)
scroll.pack(side="right", fill="y")
tree.configure(yscrollcommand=scroll.set)

# ================= TREEVIEW ACTIONS =================
def copy_path(event):
    item = tree.identify_row(event.y)
    if item:
        path = tree.item(item, "values")[0]
        app.clipboard_clear()
        app.clipboard_append(path)

def open_file(event):
    item = tree.identify_row(event.y)
    if item:
        path = tree.item(item, "values")[0]
        if os.path.exists(path):
            if sys.platform.startswith("win"):
                os.startfile(path)
            elif sys.platform == "darwin":
                os.system(f'open "{path}"')
            else:
                os.system(f'xdg-open "{path}"')

tree.bind("<Button-1>", copy_path)
tree.bind("<Double-Button-1>", open_file)

# ================= SEARCH LOGIC =================
def allowed_file(name):
    pats = file_filter.get().lower().split()
    return "*" in pats or any(fnmatch.fnmatch(name, p) for p in pats)

def excluded_dir(path):
    parts = set(path.lower().split(os.sep))
    return any(ex in parts for ex in exclude_folders.get().lower().split())

def read_file_content_with_preview(path, query, use_regex=False):
    """
    Returns (found, preview) for a file.
    Preview shows exact line/cell/page/tag context.
    """
    preview = ""
    found = False
    try:
        if path.lower().endswith((".txt", ".csv")):
            with open(path, "r", errors="ignore") as f:
                for i, line in enumerate(f, 1):
                    text_line = line.strip()
                    if use_regex:
                        if re.search(query, text_line, re.IGNORECASE):
                            found = True
                            preview = f"Line {i}: {text_line[:100]}"
                            break
                    else:
                        if all(t.lower() in text_line.lower() for t in query.split()):
                            found = True
                            preview = f"Line {i}: {text_line[:100]}"
                            break

        elif path.lower().endswith(".xlsx"):
            sheets = pd.read_excel(path, sheet_name=None)
            for sheet_name, sheet in sheets.items():
                for r_idx, row in sheet.iterrows():
                    for c_idx, value in row.items():
                        if pd.notna(value):
                            text = str(value)
                            if use_regex:
                                if re.search(query, text, re.IGNORECASE):
                                    found = True
                                    preview = f"Sheet '{sheet_name}' Row {r_idx+1} Col {c_idx+1}: {text[:50]}"
                                    return found, preview
                            else:
                                if all(t.lower() in text.lower() for t in query.split()):
                                    found = True
                                    preview = f"Sheet '{sheet_name}' Row {r_idx+1} Col {c_idx+1}: {text[:50]}"
                                    return found, preview

        elif path.lower().endswith(".pdf"):
            with open(path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for i, page in enumerate(reader.pages):
                    text = page.extract_text()
                    if text:
                        for line in text.splitlines():
                            if use_regex:
                                if re.search(query, line, re.IGNORECASE):
                                    found = True
                                    preview = f"Page {i+1}: {line[:100]}"
                                    return found, preview
                            else:
                                if all(t.lower() in line.lower() for t in query.split()):
                                    found = True
                                    preview = f"Page {i+1}: {line[:100]}"
                                    return found, preview

        elif path.lower().endswith(".xml"):
            tree_xml = ET.parse(path)
            root_xml = tree_xml.getroot()
            for elem in root_xml.iter():
                if elem.text:
                    text = elem.text.strip()
                    if use_regex:
                        if re.search(query, text, re.IGNORECASE):
                            found = True
                            preview = f"Tag <{elem.tag}>: {text[:100]}"
                            return found, preview
                    else:
                        if all(t.lower() in text.lower() for t in query.split()):
                            found = True
                            preview = f"Tag <{elem.tag}>: {text[:100]}"
                            return found, preview
    except Exception:
        return False, ""
    return found, preview

results_list = []

def run_search():
    global stop_flag, results_list
    stop_flag = False
    results_list = []
    for i in tree.get_children():
        tree.delete(i)
    counter_lbl.config(text="Matches: 0")
    progress_var.set(0)

    root = root_path.get()
    query = search_var.get()
    start = time.time()

    search_btn.config(state="disabled")
    stop_btn.config(state="normal")

    files = []
    for r, d, f in os.walk(root):
        if excluded_dir(r):
            d[:] = []
            continue
        for file in f:
            if allowed_file(file.lower()):
                files.append(os.path.join(r, file))

    total = max(len(files),1)
    done = matches = 0

    for path in files:
        if stop_flag:
            break
        found, preview = read_file_content_with_preview(path, query, regex_var.get())

        done +=1
        progress_var.set(int(done/total*100))
        elapsed = time.time()-start
        spd = done/elapsed if elapsed else 0
        eta = int((total-done)/spd) if spd else 0
        eta_lbl.config(text=f"ETA: {eta}s")
        spd_lbl.config(text=f"Speed: {spd:.1f} files/s")

        if found:
            tree.insert("", "end", values=(path, preview))
            results_list.append((path, preview))
            matches +=1
            counter_lbl.config(text=f"Matches: {matches}")

        app.update_idletasks()

    search_btn.config(state="normal")
    stop_btn.config(state="disabled")

def stop_search():
    global stop_flag
    stop_flag = True

def export_results():
    if not results_list:
        messagebox.showinfo("Info","No results to export")
        return
    file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files","*.csv")])
    if not file:
        return
    import csv
    with open(file,"w",newline="",encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["File Path","Preview"])
        writer.writerows(results_list)
    messagebox.showinfo("Success", f"Results exported to {file}")

search_btn.config(command=lambda: threading.Thread(target=run_search, daemon=True).start())
stop_btn.config(command=stop_search)
export_btn.config(command=export_results)

app.mainloop()
