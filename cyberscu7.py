import tkinter as tk
from tkinter import ttk, messagebox
import re
import hashlib
import requests
from PIL import Image, ImageTk
import threading
import random
import string
import secrets

# Password strength checker
def check_password_strength(password):
    length = len(password) >= 8
    has_digit = re.search(r"\d", password)
    has_upper = re.search(r"[A-Z]", password)
    has_lower = re.search(r"[a-z]", password)
    has_symbol = re.search(r"[!@#$%^&*()_+=\-{}\[\]:;\"'<>,.?/]", password)

    errors = []
    if not length: errors.append("Password must be at least 8 characters.")
    if not has_digit: errors.append("Add at least one digit.")
    if not has_upper: errors.append("Add at least one uppercase letter.")
    if not has_lower: errors.append("Add at least one lowercase letter.")
    if not has_symbol: errors.append("Add at least one special character (!@#$ etc.).")

    return errors

# Check password breach using HaveIBeenPwned API
def check_password_pwned(password):
    sha1 = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]
    try:
        response = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}")
        if response.status_code != 200:
            return "⚠️ Error checking breach database."
        hashes = (line.split(':') for line in response.text.splitlines())
        for hash_suffix, count in hashes:
            if hash_suffix == suffix:
                return f"🔒 This password has been found in data breaches {count} times. Please change it."
        return "✅ This password was not found in any known data breaches."
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# Website check
def is_website_safe(url):
    if not url.startswith("http"):
        url = "http://" + url
    try:
        response = requests.get(url, timeout=5)
        return f"✅ Website is reachable. Status: {response.status_code}"
    except Exception as e:
        return f"⚠️ Could not reach the website. Error: {str(e)}"

# Handle password check
def handle_check_password():
    password = password_entry.get()
    result_text_pw.delete(1.0, tk.END)

    if not password:
        messagebox.showwarning("Input Needed", "Please enter a password.")
        return

    errors = check_password_strength(password)
    if not errors:
        result_text_pw.insert(tk.END, "✅ Password is strong!\n")
    else:
        result_text_pw.insert(tk.END, "❌ Weak password:\n")
        for err in errors:
            result_text_pw.insert(tk.END, f"- {err}\n")

    def check_breach():
        msg = check_password_pwned(password)
        result_text_pw.after(0, lambda: result_text_pw.insert(tk.END, f"\n{msg}"))

    threading.Thread(target=check_breach).start()

# Handle website check
def handle_check_website():
    url = website_entry.get()
    result_text_web.delete(1.0, tk.END)

    if not url:
        messagebox.showwarning("Input Needed", "Please enter a website URL.")
        return

    result = is_website_safe(url)
    result_text_web.insert(tk.END, result)

# Show/hide password
def toggle_password():
    if show_var.get():
        password_entry.config(show="")
    else:
        password_entry.config(show="*")

# Recommend password
def generate_password():
    chars = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{}|;:,.<>?"
    new_password = ''.join(secrets.choice(chars) for _ in range(16))
    recommended_pw_label.config(text=f"🔑 {new_password}")

# Toggle Dark Mode
def toggle_dark_mode():
    dark = dark_mode_var.get()
    bg = "#1e1e1e" if dark else "#f0f0f0"
    fg = "white" if dark else "black"
    entry_bg = "#2e2e2e" if dark else "white"

    root.config(bg=bg)
    for widget in root.winfo_children():
        if isinstance(widget, tk.Label) or isinstance(widget, tk.Checkbutton) or isinstance(widget, tk.Button):
            widget.config(bg=bg, fg=fg)

    for frame in [pw_frame, web_frame, guide_frame]:
        frame.config(bg=bg)
    for widget in [guide_text, result_text_pw, result_text_web]:
        widget.config(bg=entry_bg, fg=fg, insertbackground=fg)
    for entry in [password_entry, website_entry]:
        entry.config(bg=entry_bg, fg=fg, insertbackground=fg)
    recommended_pw_label.config(bg=bg, fg="lightblue")
    dark_toggle.config(bg=bg, fg=fg)

# GUI setup
root = tk.Tk()
root.title("	Rassed Cyber Security Tool – Password & Website Checker")
root.geometry("700x530")
root.resizable(False, False)
root.config(bg="#f0f0f0")

# Load and display logos
try:
    logo_left_img = Image.open("eco.png").resize((70, 80), Image.Resampling.LANCZOS)
    logo_left = ImageTk.PhotoImage(logo_left_img)
    logo_left_label = tk.Label(root, image=logo_left, bg="#f0f0f0")
    logo_left_label.place(x=10, y=5)

    logo_right_img = Image.open("qstss.png").resize((65, 65), Image.Resampling.LANCZOS)
    logo_right = ImageTk.PhotoImage(logo_right_img)
    logo_right_label = tk.Label(root, image=logo_right, bg="#f0f0f0")
    logo_right_label.place(x=600, y=5)

    center_logo_img = Image.open("ag.png").resize((150, 100), Image.Resampling.LANCZOS)
    center_logo = ImageTk.PhotoImage(center_logo_img)
    center_logo_label = tk.Label(root, image=center_logo, bg="#f0f0f0")
    center_logo_label.image = center_logo
    center_logo_label.place(x=300, y=8)
except Exception as e:
    print("Logo load error:", e)

dark_mode_var = tk.BooleanVar()
dark_toggle = tk.Checkbutton(root, text="🌙 Dark Mode", variable=dark_mode_var, command=toggle_dark_mode, bg="#f0f0f0")
dark_toggle.place(x=80, y=60)

notebook = ttk.Notebook(root)
notebook.pack(pady=100, expand=True, fill='both')

# Password Checker Tab
pw_frame = tk.Frame(notebook)
notebook.add(pw_frame, text="🔐 Password Checker")

tk.Label(pw_frame, text="Enter Password:", font=('Arial', 12)).pack(pady=5)
password_entry = tk.Entry(pw_frame, width=30, show="*", font=('Arial', 12))
password_entry.pack()

show_var = tk.BooleanVar()
tk.Checkbutton(pw_frame, text="👁 Show Password", variable=show_var, command=toggle_password).pack()

tk.Button(pw_frame, text="Check Password", command=handle_check_password).pack(pady=10)

tk.Button(pw_frame, text="Recommend Strong Password", command=generate_password).pack(pady=5)
recommended_pw_label = tk.Label(pw_frame, text="", fg="blue", font=('Arial', 10, 'bold'))
recommended_pw_label.pack()

result_text_pw = tk.Text(pw_frame, height=10, width=70, wrap=tk.WORD)
result_text_pw.pack(pady=10)

# Website Checker Tab
web_frame = tk.Frame(notebook)
notebook.add(web_frame, text="🌐 Website Checker")

tk.Label(web_frame, text="Enter Website URL:", font=('Arial', 12)).pack(pady=5)
website_entry = tk.Entry(web_frame, width=40, font=('Arial', 12))
website_entry.pack()

tk.Button(web_frame, text="Check Website", command=handle_check_website).pack(pady=10)

result_text_web = tk.Text(web_frame, height=10, width=70, wrap=tk.WORD)
result_text_web.pack()

# Password Guide Tab
guide_frame = tk.Frame(notebook)
notebook.add(guide_frame, text="📘 Password Guide")

guide_text = tk.Text(guide_frame, wrap=tk.WORD, font=('Arial', 11), bg="#f0f0f0")
guide_text.pack(padx=10, pady=10, expand=True, fill='both')

guide_content = """
🔐 How to Manage and Store Your Passwords

1. Use Strong Passwords:
   - At least 12 characters long
   - A mix of uppercase, lowercase, digits, and special characters
   - Avoid dictionary words and common phrases

2. Never Reuse Passwords:
   - Each account should have a unique password

3. Use a Password Manager:
   - Tools like Bitwarden, LastPass, or 1Password can generate and store strong passwords

4. Enable Two-Factor Authentication (2FA):
   - Adds a second layer of protection using your phone or email

5. Avoid Storing Passwords in Browsers:
   - Use secure password managers instead

6. Never Share Passwords via Email or Text:
   - Use secure platforms or password-sharing features in managers

7. Update Passwords Regularly:
   - Especially if there’s a breach or suspected compromise

8. Backup Your Password Manager:
   - Keep a secure backup of your password vault in case of emergencies
"""

guide_text.insert(tk.END, guide_content)
guide_text.config(state=tk.DISABLED)

root.mainloop()

