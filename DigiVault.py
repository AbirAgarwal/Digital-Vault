import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

FILE = "vault_data.json"
MASTER_FILE = "master.txt"

entries = []

# ---------------------------------------------------------
# Master Password
# ---------------------------------------------------------
def check_master_password():
    password = password_entry.get()
    if os.path.exists(MASTER_FILE):
        with open(MASTER_FILE, "r") as file:
            saved_password = file.read()
        if password == saved_password:
            login_window.destroy()
            open_vault()
        else:
            messagebox.showerror("Error", "Incorrect password!")
    else:
        if password == "":
            messagebox.showwarning("Warning", "Enter a password.")
            return
        with open(MASTER_FILE, "w") as file:
            file.write(password)
        login_window.destroy()
        open_vault()

# ---------------------------------------------------------
# Load / Save
# ---------------------------------------------------------
def load_data():
    global entries
    if os.path.exists(FILE):
        try:
            with open(FILE, "r") as file:
                entries = json.load(file)
        except:
            entries = []

def save_data():
    with open(FILE, "w") as file:
        json.dump(entries, file, indent=4)

# ---------------------------------------------------------
# Add Entry
# ---------------------------------------------------------
def add_entry():
    service = service_entry.get().strip()
    username = username_entry.get().strip()
    password = vault_password_entry.get().strip()
    notes = notes_entry.get("1.0", tk.END).strip()

    if service == "" or username == "" or password == "":
        messagebox.showwarning("Warning", "Please fill Service, Username and Password.")
        return

    data = {"service": service, "username": username, "password": password, "notes": notes}
    entries.append(data)
    save_data()
    refresh_table()
    clear_fields()
    messagebox.showinfo("Success", "Entry saved successfully!")

# ---------------------------------------------------------
# Edit Entry
# ---------------------------------------------------------
def edit_entry():
    selected = vault_table.selection()
    if not selected:
        messagebox.showwarning("Warning", "Select an entry first.")
        return
    index = int(selected[0])
    entry = entries[index]

    service_entry.delete(0, tk.END)
    service_entry.insert(0, entry["service"])
    username_entry.delete(0, tk.END)
    username_entry.insert(0, entry["username"])
    vault_password_entry.delete(0, tk.END)
    vault_password_entry.insert(0, entry["password"])
    notes_entry.delete("1.0", tk.END)
    notes_entry.insert(tk.END, entry["notes"])

    del entries[index]
    save_data()
    refresh_table()
    messagebox.showinfo("Edit Mode", "Fields loaded. Click 'Save Entry' to update.")

# ---------------------------------------------------------
# Delete Entry
# ---------------------------------------------------------
def delete_entry():
    selected = vault_table.selection()
    if not selected:
        messagebox.showwarning("Warning", "Select an entry first.")
        return
    index = int(selected[0])
    del entries[index]
    save_data()
    refresh_table()

# ---------------------------------------------------------
# Search
# ---------------------------------------------------------
def search_entry():
    search = search_entry_box.get().lower()
    for item in vault_table.get_children():
        vault_table.delete(item)
    for index, entry in enumerate(entries):
        if search in entry["service"].lower() or search in entry["username"].lower():
            vault_table.insert("", tk.END, iid=index, values=(entry["service"], entry["username"], "********"))

def refresh_table():
    for item in vault_table.get_children():
        vault_table.delete(item)
    for index, entry in enumerate(entries):
        vault_table.insert("", tk.END, iid=index, values=(entry["service"], entry["username"], "********"))

def clear_fields():
    service_entry.delete(0, tk.END)
    username_entry.delete(0, tk.END)
    vault_password_entry.delete(0, tk.END)
    notes_entry.delete("1.0", tk.END)

def copy_password():
    selected = vault_table.selection()
    if not selected:
        messagebox.showwarning("Warning", "Select an entry first.")
        return
    index = int(selected[0])
    password = entries[index]["password"]
    root.clipboard_clear()
    root.clipboard_append(password)
    messagebox.showinfo("Copied", "Password copied to clipboard!")

def show_selected():
    selected = vault_table.selection()
    if not selected:
        messagebox.showwarning("Warning", "Select an entry.")
        return
    index = int(selected[0])
    entry = entries[index]
    messagebox.showinfo("Entry Details",
        f"Service: {entry['service']}\nUsername: {entry['username']}\nPassword: {entry['password']}\nNotes: {entry['notes']}")

# ---------------------------------------------------------
# Vault Window
# ---------------------------------------------------------
def open_vault():
    global service_entry, username_entry, vault_password_entry, notes_entry, vault_table, search_entry_box, root
    load_data()
    root = tk.Tk()
    root.title("Personal Digital Vault")
    root.geometry("850x650")
    root.resizable(False, False)

    tk.Label(root, text="PERSONAL DIGITAL VAULT", font=("Arial", 22, "bold")).pack(pady=15)

    frame = tk.LabelFrame(root, text="Add Secure Entry", padx=10, pady=10)
    frame.pack(fill="x", padx=30)

    tk.Label(frame, text="Service:").grid(row=0, column=0, padx=5, pady=5)
    service_entry = tk.Entry(frame, width=25)
    service_entry.grid(row=0, column=1)

    tk.Label(frame, text="Username:").grid(row=1, column=0, padx=5, pady=5)
    username_entry = tk.Entry(frame, width=25)
    username_entry.grid(row=1, column=1)

    tk.Label(frame, text="Password:").grid(row=2, column=0, padx=5, pady=5)
    vault_password_entry = tk.Entry(frame, width=25, show="*")
    vault_password_entry.grid(row=2, column=1)

    tk.Label(frame, text="Notes:").grid(row=3, column=0)
    notes_entry = tk.Text(frame, width=30, height=4)
    notes_entry.grid(row=3, column=1)

    tk.Button(frame, text="Save Entry", command=add_entry, width=15).grid(row=4, column=1, pady=10)

    search_frame = tk.Frame(root)
    search_frame.pack(pady=15)
    tk.Label(search_frame, text="Search:").pack(side="left")
    search_entry_box = tk.Entry(search_frame, width=30)
    search_entry_box.pack(side="left", padx=5)
    tk.Button(search_frame, text="Search", command=search_entry).pack(side="left")
    tk.Button(search_frame, text="Show All", command=refresh_table).pack(side="left", padx=5)

    columns = ("Service", "Username", "Password")
    vault_table = ttk.Treeview(root, columns=columns, show="headings", height=10)
    for column in columns:
        vault_table.heading(column, text=column)
    vault_table.column("Service", width=200)
    vault_table.column("Username", width=250)
    vault_table.column("Password", width=200)
    vault_table.pack(pady=10)

    button_frame = tk.Frame(root)
    button_frame.pack()
    tk.Button(button_frame, text="View Details", command=show_selected, width=15).grid(row=0, column=0, padx=5)
    tk.Button(button_frame, text="Edit Entry", command=edit_entry, width=15).grid(row=0, column=1, padx=5)
    tk.Button(button_frame, text="Copy Password", command=copy_password, width=15).grid(row=0, column=2, padx=5)
    tk.Button(button_frame, text="Delete", command=delete_entry, width=15).grid(row=0, column=3, padx=5)

    refresh_table()
    root.mainloop()

# ---------------------------------------------------------
# Login Window
# ---------------------------------------------------------
login_window = tk.Tk()
login_window.title("Digital Vault Login")
login_window.geometry("400x250")
login_window.resizable(False, False)

tk.Label(login_window, text="🔐 DIGITAL VAULT", font=("Arial", 22, "bold")).pack(pady=25)
tk.Label(login_window, text="Enter Master Password").pack()
password_entry = tk.Entry(login_window, show="*", width=30)
password_entry.pack(pady=10)
tk.Button(login_window, text="Unlock Vault", command=check_master_password, width=20).pack(pady=10)
tk.Label(login_window, text="First login creates the master password.", font=("Arial", 9)).pack()

login_window.mainloop()