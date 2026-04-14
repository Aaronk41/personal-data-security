import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from PIL import Image, ImageTk
from stegano import lsb
from cryptography.fernet import Fernet
import sys


# Theme Colors
LIGHT_THEME = {
    "bg": "#f4f6f8",
    "fg": "#1f2933",
    "accent": "#f35353",
    "button": "#d91d1d",
    "button_fg": "#ffffff",
    "section": "#111827"
}

DARK_THEME = {
    "bg": "#160b0c",
    "fg": "#e5e7eb",
    "accent": "#f35353",
    "button": "#d91d1d",
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

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


img_path = resource_path("dino2.png")

if os.path.exists(img_path):
    img = Image.open(img_path).resize((200, 120))
    logo_img = ImageTk.PhotoImage(img)
    logo = tk.Label(window, image=logo_img, bg=current_theme["bg"])
    logo.place(x=340, y=70)

MAX_FILE_SIZE = 100 * 1024 * 1024

# Encryption Section
encrypt_label = tk.Label(
    window,
    text="Encryption",
    font=("Segoe UI", 13, "bold"),
    bg=current_theme["bg"],
    fg=current_theme["section"]
)
encrypt_label.place(x=190, y=180)

encrypt_instr = tk.Label(
    window,
   text="Click the encryption button to select a .txt or .csv\nThen rename the file to whatever you want and it will save as a .txt\n\n\nClick the decryption button to select an encrypted .txt or .csv\nChoose the file name to save decrypted file",
    bg=current_theme["bg"],
    fg=current_theme["fg"]
)
encrypt_instr.place(x=60, y=215)


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
        title='Select a .txt or .csv file to encrypt'
    )

    if not encrypt_file_path:
        messagebox.showwarning("No File", "Select a file first.")
        return

    f = Fernet(load_key())
    with open(encrypt_file_path, "rb") as file:
        data = file.read()

    encrypted = f.encrypt(data)
    output = filedialog.asksaveasfilename(
        title="Save Encrypted File As",
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("CSV Files", "*.csv")]
    )

    with open(output, "wb") as file:
        file.write(encrypted)
        if output:
            messagebox.showinfo("Success", f"Hidden file saved as {output}")
        else:
            messagebox.showwarning("Failure", "No file was saved.")

    os.remove(encrypt_file_path)



def decrypt_file():
    global decrypt_file_path
    decrypt_file_path = filedialog.askopenfilename(
        title="Select a .txt or .csv file to decrypt"
    )


    if not decrypt_file_path:
        messagebox.showwarning("No File", "Select a file first.")
        return

    f = Fernet(load_key())
    with open(decrypt_file_path, "rb") as file:
        data = file.read()

    decrypted = f.decrypt(data)
    output = filedialog.asksaveasfilename(
        title="Save Decrypted File As",
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("CSV Files", "*.csv")]
    )

    with open(output, "wb") as file:
        file.write(decrypted)

        if output:
            messagebox.showinfo("Success", f"Hidden file saved as {output}")
        else:
            messagebox.showwarning("Failure", "No file was saved.")
    os.remove(decrypt_file_path)



ttk.Button(window, text="Encrypt", command=encrypt_file, style="Accent.TButton", width=15).place(x=170, y=350)

ttk.Button(window, text="Decrypt", command=decrypt_file, style="Accent.TButton", width=15).place(x=170, y=450)




# Steganography Section
stego_label = tk.Label(
    window,
    text="Steganography",
    font=("Segoe UI", 13, "bold"),
    bg=current_theme["bg"],
    fg=current_theme["section"]
)
stego_label.place(x=590, y=180)

stego_instr = tk.Label(
    window,
   text="Select the .png file you wish to carry the hidden material\nFinally choose the file name of the hidden .png file\nNo transparent .png files\nClick the hide button and select a .txt or .csv file that you wish to hide\n\n\nClick the reveal button and select your hidden material .png\nName the revealed file and save",
    bg=current_theme["bg"],
    fg=current_theme["fg"]
)
stego_instr.place(x=475, y=215)


def hide_file():
    #prompt user to input PNG image
    steg_input_filepath = filedialog.askopenfilename(
        title="Select Image File",
        filetypes=[("PNG Files", "*.png")]
    )
    if not steg_input_filepath:
        messagebox.showwarning("No PNG File", "Select a PNG file first.")
        return


    #prompt user to input text/csv file
    path = filedialog.askopenfilename(
        title="Select Text/CSV File",
        filetypes=[("Text Files", "*.txt"), ("CSV Files", "*.csv")]
    )
    if not path:
        messagebox.showwarning("No Text/CSV File", "Select a txt or csv file after PNG image file")
        return
    hidden_material = open(path, "r")


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
    # error handling

    if output:
        messagebox.showinfo("Success", f"Hidden file saved as {output}")
    else:
        messagebox.showwarning("Failure", "No file was saved.")

#Steganography buttons
ttk.Button(window, text="Hide", command=hide_file, style="Accent.TButton", width=15).place(x=590, y=350)
ttk.Button(window, text="Reveal", command=reveal_file, style="Accent.TButton", width=15).place(x=590, y=450)



# App Launch

window.mainloop()

