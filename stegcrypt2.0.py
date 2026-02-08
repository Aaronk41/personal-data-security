import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from PIL import Image, ImageTk
from stegano import lsb
from cryptography.fernet import Fernet


# Theme Colors
LIGHT_THEME = {
    "bg": "#f4f6f8",
    "fg": "#1f2933",
    "accent": "#3b82f6",
    "button": "#2563eb",
    "button_fg": "#ffffff",
    "section": "#111827"
}

DARK_THEME = {
    "bg": "#0f172a",
    "fg": "#e5e7eb",
    "accent": "#60a5fa",
    "button": "#3b82f6",
    "button_fg": "#ffffff",
    "section": "#f9fafb"
}

current_theme = LIGHT_THEME

window = tk.Tk()
window.geometry("900x600")
window.title("StegCrypt")
window.resizable(False, False)
window.configure(bg=current_theme["bg"])


# Styling
style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Accent.TButton",
    background=current_theme["button"],
    foreground=current_theme["button_fg"],
    font=("Segoe UI", 10, "bold"),
    padding=(16, 8),
    borderwidth=0
)

style.map(
    "Accent.TButton",
    background=[("active", current_theme["accent"])]
)


# Theme Toggle
def toggle_theme():
    global current_theme
    current_theme = DARK_THEME if current_theme == LIGHT_THEME else LIGHT_THEME
    apply_theme()


def apply_theme():
    window.configure(bg=current_theme["bg"])

    for widget in window.winfo_children():
        if isinstance(widget, tk.Label):
            widget.configure(
                bg=current_theme["bg"],
                fg=current_theme["fg"]
            )

    title.configure(fg=current_theme["section"])
    style.configure("Accent.TButton", background=current_theme["button"])


# Title and Logo
title = tk.Label(
    window,
    text="StegCrypt",
    font=("Segoe UI", 24, "bold"),
    bg=current_theme["bg"],
    fg=current_theme["section"]
)
title.place(x=360, y=20)

toggle_btn = ttk.Button(
    window,
    text="Toggle Light / Dark",
    command=toggle_theme
)
toggle_btn.place(x=720, y=30)

img_path = os.path.join(os.path.dirname(__file__), "dino.png")
if os.path.exists(img_path):
    img = Image.open(img_path).resize((120, 120))
    logo_img = ImageTk.PhotoImage(img)
    logo = tk.Label(window, image=logo_img, bg=current_theme["bg"])
    logo.place(x=390, y=70)

MAX_FILE_SIZE = 100 * 1024 * 1024

# Encryption Section
encrypt_label = tk.Label(
    window,
    text="Encryption",
    font=("Segoe UI", 13, "bold"),
    bg=current_theme["bg"],
    fg=current_theme["section"]
)
encrypt_label.place(x=160, y=220)

encrypt_instr = tk.Label(
    window,
    text="Select a file and encrypt or decrypt",
    bg=current_theme["bg"],
    fg=current_theme["fg"]
)
encrypt_instr.place(x=160, y=250)

# Encryption and Decryption
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as f:
        f.write(key)
    return key


def load_key():
    try:
        return open("secret.key", "rb").read()
    except FileNotFoundError:
        return generate_key()


def encrypt_file():
    global encrypt_file_path
    encrypt_file_path = filedialog.askopenfilename(
        title='Select file to encrypt'
    )
    selected_encrypt_label.config(text=encrypt_file_path)

    if not encrypt_file_path:
        messagebox.showwarning("No File", "Select a file first.")
        return

    f = Fernet(load_key())
    with open(encrypt_file_path, "rb") as file:
        data = file.read()

    encrypted = f.encrypt(data)
    output = encrypt_file_path.rsplit(".", 1)[0] + "[encrypted].txt"

    with open(output, "wb") as file:
        file.write(encrypted)

        if output:
            messagebox.showinfo("Success", f"Hidden file saved as {output}")
        else:
            messagebox.showwarning("Failure", "No file was saved.")

    os.remove(encrypt_file_path)
    selected_encrypt_label.config(text=f"Encrypted: {output}")


def decrypt_file():
    global decrypt_file_path
    decrypt_file_path = filedialog.askopenfilename(
        title="Select file to decrypt"
    )
    selected_decrypt_label.config(text=decrypt_file_path)

    if not decrypt_file_path:
        messagebox.showwarning("No File", "Select a file first.")
        return

    f = Fernet(load_key())
    with open(decrypt_file_path, "rb") as file:
        data = file.read()

    decrypted = f.decrypt(data)
    output = decrypt_file_path.rsplit(".", 1)[0] + "[decrypted].txt"

    with open(output, "wb") as file:
        file.write(decrypted)

        if output:
            messagebox.showinfo("Success", f"Hidden file saved as {output}")
        else:
            messagebox.showwarning("Failure", "No file was saved.")
    os.remove(decrypt_file_path)
    selected_decrypt_label.config(text=f"Decrypted: {output}")


ttk.Button(window, text="Encrypt", command=encrypt_file, style="Accent.TButton").place(x=260, y=420)

ttk.Button(window, text="Decrypt", command=decrypt_file, style="Accent.TButton").place(x=260, y=490)

selected_encrypt_label = tk.Label(window, text="No file selected", bg=current_theme["bg"], fg=current_theme["fg"])
selected_encrypt_label.place(x=160, y=460)

selected_decrypt_label = tk.Label(window, text="No file selected", bg=current_theme["bg"], fg=current_theme["fg"])
selected_decrypt_label.place(x=160, y=530)


# Steganography Section
stego_label = tk.Label(
    window,
    text="Steganography",
    font=("Segoe UI", 13, "bold"),
    bg=current_theme["bg"],
    fg=current_theme["section"]
)
stego_label.place(x=540, y=220)

stego_instr = tk.Label(
    window,
    text="Hide or reveal text in PNG images",
    bg=current_theme["bg"],
    fg=current_theme["fg"]
)
stego_instr.place(x=540, y=250)


def hide_file():
    #prompt user to input PNG image
    steg_input_filepath = filedialog.askopenfilename(
        title="Select Image File",
        filetypes=[("PNG Files", "*.png")]
    )
    if not steg_input_filepath:
        messagebox.showwarning("No PNG File", "Select a PNG file first.")
        return
    selected_image_label.config(text=steg_input_filepath)

    #prompt user to input text/csv file
    path = filedialog.askopenfilename(
        title="Select Text/CSV File",
        filetypes=[("Text Files", "*.txt"), ("CSV Files", "*.csv")]
    )
    if not path:
        messagebox.showwarning("No Text/CSV File", "Select a txt or csv file after PNG image file")
        return
    hidden_material = open(path, "r")
    selected_hidden_label.config(text=path)

    #hide the text/csv in PNG image
    if steg_input_filepath and hidden_material:
        #prompt user to save output file
        output_file = filedialog.asksaveasfilename(
            title="Save Hidden Image As",
            defaultextension=".png",
            filetypes=[("png files", "*.png")]
        )
        #open the PNG file and hide the hidden material in the image
        img = Image.open(steg_input_filepath).convert("RGB")
        lsb.hide(img, hidden_material.read()).save(output_file)
        #error handling
        if output_file:
            messagebox.showinfo("Success", f"Hidden file saved as {output_file}")
        else:
            messagebox.showwarning("Failure", "No file was saved.")


def reveal_file():
    path = filedialog.askopenfilename(
        title="Open Hidden Image To Reveal",
        filetypes=[("PNG Files", "*.png")]
    )
    if not path:
        messagebox.showwarning("No PNG File", "Select a PNG file first.")
        return
    output = filedialog.asksaveasfilename(
        title = "Save Revealed File As",
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("CSV Files", "*.csv")]
        )
    with open(output, "w") as f:
        f.write(lsb.reveal(path))
    #error handling
    if output:
        messagebox.showinfo("Success", f"Hidden file saved as {output}")
    else:
        messagebox.showwarning("Failure", "No file was saved.")

#Steganography buttons
ttk.Button(window, text="Hide", command=hide_file, style="Accent.TButton").place(x=600, y=420)
ttk.Button(window, text="Reveal", command=reveal_file, style="Accent.TButton").place(x=600, y=520)

#Steganography file labels
selected_image_label = tk.Label(window, text="No image selected", bg=current_theme["bg"], fg=current_theme["fg"])
selected_image_label.place(x=540, y=460)

selected_hidden_label = tk.Label(window, text="No file selected", bg=current_theme["bg"], fg=current_theme["fg"])
selected_hidden_label.place(x=540, y=480)

# App Launch
window.mainloop()