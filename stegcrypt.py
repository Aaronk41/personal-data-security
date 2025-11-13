import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from PIL import Image, ImageTk
from stegano import lsb
from cryptography.fernet import Fernet

# --- Encryption & Decryption Logic ---

def generate_key():
    """Generates a new Fernet key and saves it to secret.key"""
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    return key

def load_key():
    """Loads the Fernet key, or generates one if missing."""
    try:
        return open("secret.key", "rb").read()
    except FileNotFoundError:
        return generate_key()

def encrypt_selected_file():
    """Encrypts the file selected for encryption."""
    global encrypt_file_path
    if not encrypt_file_path:
        messagebox.showwarning("No File Selected", "Please select a file to encrypt.")
        return

    try:
        key = load_key()
        f = Fernet(key)

        with open(encrypt_file_path, "rb") as file:
            data = file.read()

        encrypted_data = f.encrypt(data)
        output_file = encrypt_file_path.rsplit(".", 1)[0] + "[encrypted].txt"

        with open(output_file, "wb") as file:
            file.write(encrypted_data)

        os.remove(encrypt_file_path)
        messagebox.showinfo("Success", f"Encrypted and saved as:\n{output_file}")

        selected_encrypt_label.config(text=f"File encrypted: {output_file}")
    except Exception as e:
        messagebox.showerror("Encryption Error", f"An error occurred:\n{e}")

def decrypt_selected_file():
    """Decrypts the file selected for decryption."""
    global decrypt_file_path
    if not decrypt_file_path:
        messagebox.showwarning("No File Selected", "Please select a file to decrypt.")
        return

    try:
        key = load_key()
        f = Fernet(key)

        with open(decrypt_file_path, "rb") as file:
            encrypted_data = file.read()

        decrypted_data = f.decrypt(encrypted_data)
        output_file = decrypt_file_path.rsplit(".", 1)[0] + "[decrypted].txt"

        with open(output_file, "wb") as file:
            file.write(decrypted_data)

        os.remove(decrypt_file_path)
        messagebox.showinfo("Success", f"Decrypted and saved as:\n{output_file}")

        selected_decrypt_label.config(text=f"File decrypted: {output_file}")
    except Exception as e:
        messagebox.showerror("Decryption Error", f"An error occurred:\n{e}")




# Window Specs
window = tk.Tk()
window.geometry('900x600')
window.title("StegCrypt")
window.resizable(0, 0)


# Color
COLOR_THEMES = {
    "dark": {
        "primary_bg": "#1e1e1e",
        "secondary_bg": "#2e2e2e",
        "text_fg": "white",
        "highlight_fg": "#1d9ab9",
        "button_bg": "#2b2b2b",
        "button_fg": "white",
        "button_active_bg": "#1d9ab9",
        "button_active_fg": "black",
        "logo_text_fg": "gray"
    },
    "light": {
        "primary_bg": "#ffffff",
        "secondary_bg": "#f0f0f0",
        "text_fg": "black",
        "highlight_fg": "#9370db",
        "button_bg": "#c0c0c0",
        "button_fg": "black",
        "button_active_bg": "#9370db",
        "button_active_fg": "white",
        "logo_text_fg": "#6a5acd"
    }
}

current_theme = tk.StringVar(value="dark")

def apply_theme(theme_name):
    """Applies the selected color theme to all widgets."""
    theme = COLOR_THEMES[theme_name]
    current_theme.set(theme_name)

    window.configure(background=theme["primary_bg"])

    title.configure(bg=theme["primary_bg"], fg=theme["highlight_fg"])

    if 'logo' in globals():
        logo.configure(bg=theme["primary_bg"])
        if logo.cget("text") == "(logo)":
            logo.configure(fg=theme["logo_text_fg"])

    encrypt_label.configure(bg=theme["primary_bg"], fg=theme["text_fg"])
    stego_label.configure(bg=theme["primary_bg"], fg=theme["text_fg"])

    encrypt_instr.configure(bg=theme["secondary_bg"], fg=theme["text_fg"])
    stego_instr.configure(bg=theme["secondary_bg"], fg=theme["text_fg"])

    selected_encrypt_label.configure(bg=theme["primary_bg"], fg=theme["text_fg"])
    selected_decrypt_label.configure(bg=theme["primary_bg"], fg=theme["text_fg"])
    selected_image_label.configure(bg=theme["primary_bg"], fg=theme["text_fg"])
    selected_hidden_label.configure(bg=theme["primary_bg"], fg=theme["text_fg"])
    selected_reveal_label.configure(bg=theme["primary_bg"], fg=theme["text_fg"])

    style.configure(
        "TButton",
        background=theme["button_bg"],
        foreground=theme["button_fg"],
    )
    style.map(
        "TButton",
        background=[('active', theme["button_active_bg"])],
        foreground=[('active', theme["button_active_fg"])]
    )


    toggle_button.configure(text=f"Switch to {next_theme(theme_name)} Mode")

def next_theme(current):
    """Returns the name of the next theme."""
    return "Dark" if current == "light" else "Light"

def toggle_theme():
    """Switches the theme between dark and light."""
    new_theme = "light" if current_theme.get() == "dark" else "dark"
    apply_theme(new_theme)

style = ttk.Style()
style.theme_use("clam")
style.configure(
    "TButton",
    font=("Segoe UI", 10, "bold"),
    padding=5
)


# Title
title = tk.Label(
    window,
    text="StegCrypt",
    font=("Helvetica", 22, "bold"),
)
title.place(x=380, y=20)

# Logo
img_path = os.path.join(os.path.dirname(__file__), "dino.png")
if os.path.exists(img_path):
    img = Image.open(img_path)
    img_display = img.resize((120, 120))
    logo_img = ImageTk.PhotoImage(img_display)


    img_icon = img.resize((32, 32))
    logo_icon_img = ImageTk.PhotoImage(img_icon)
    window.iconphoto(False, logo_icon_img)

    logo = tk.Label(window, image=logo_img)
    logo.place(x=390, y=70)
else:
    logo_img = None
    logo = tk.Label(
        window,
        text="(logo)",
        font=("Helvetica", 12, "italic"),
    )
    logo.place(x=430, y=120)
# file size

MAX_FILE_SIZE = 100 * 1024 * 1024

# Encryption Section
encrypt_file_path = None
encrypt_label = tk.Label(window, text="Encryption:", font=("Segoe UI", 12, "bold"))
encrypt_label.place(x=160, y=220)

encrypt_instr = tk.Label(
    window,
    text=(
        "• Select a file (max size: 100 MB)\n"
        "• Click Encrypt to fully encrypt it\n"
        "• Click Decrypt to reverse encryption"
    ),
    font=("Segoe UI", 9),
    justify="left",
    padx=10,
    pady=10,
    wraplength=250
)
encrypt_instr.place(x=160, y=250)

select_encrypt_file = ttk.Button(window, text="Select File")
select_encrypt_file.place(x=180, y=420)

encrypt_btn = ttk.Button(window, text="Encrypt", command=encrypt_selected_file)
encrypt_btn.place(x=280, y=420)

selected_encrypt_label = tk.Label(
    window,
    text="Currently selected encryption file: None",
    font=("Segoe UI", 9),
    anchor="w"
)
selected_encrypt_label.place(x=160, y=460)
# Encrypt file section
def select_encrypt_file_func():
    global encrypt_file_path
    file_path = filedialog.askopenfilename(title="Select File to Encrypt")
    if file_path:
        size = os.path.getsize(file_path)
        if size <= MAX_FILE_SIZE:
            encrypt_file_path = file_path
            selected_encrypt_label.config(text=f"Currently selected encryption file: {file_path}")
        else:
            messagebox.showerror("File Size Error", "File must be 100 MB or less.")
            encrypt_file_path = None
            selected_encrypt_label.config(text="Currently selected encryption file: None")

select_encrypt_file.config(command=select_encrypt_file_func)

# Decrypt Section
decrypt_file_path = None
select_decrypt_file = ttk.Button(window, text="Select File")
select_decrypt_file.place(x=180, y=490)

decrypt_btn = ttk.Button(window, text="Decrypt", command=decrypt_selected_file)
decrypt_btn.place(x=280, y=490)

selected_decrypt_label = tk.Label(
    window,
    text="Currently selected file to decrypt: None",
    font=("Segoe UI", 9),
    anchor="w"
)
selected_decrypt_label.place(x=160, y=530)
# Decrypt File Selection
def select_decrypt_file_func():
    global decrypt_file_path
    file_path = filedialog.askopenfilename(title="Select File to Decrypt")
    if file_path:
        size = os.path.getsize(file_path)
        if size <= MAX_FILE_SIZE:
            decrypt_file_path = file_path
            selected_decrypt_label.config(text=f"Currently selected file to decrypt: {file_path}")
        else:
            messagebox.showerror("File Size Error", "File must be 100 MB or less.")
            decrypt_file_path = None
            selected_decrypt_label.config(text="Currently selected file to decrypt: None")

select_decrypt_file.config(command=select_decrypt_file_func)


# Steganography Section
# Define Global Varibles
steg_input_filepath = None
hidden_material = None
output_file = None
steg_reveal_filepath = None

# Steganography Functions
# Select input png file to hide message in
def select_input_png():
    # Make steg_file_path variable global for hide section
    global steg_input_filepath
    # Prompt user to select a PNG file
    steg_input_filepath = filedialog.askopenfilename(
        title="Select PNG Image",
        filetypes=(
            ("png files", "*.png"),
        )
    )
    # Check if a file was selected and output message
    if steg_input_filepath:
        messagebox.showinfo("Selected File", f"File selected: {steg_input_filepath}")
    else:
        messagebox.showwarning("No File Selected", "No file was selected.")
    # update label
    selected_image_label.config(text=f"Currently selected image: {steg_input_filepath}")
# Select material to hide
def select_hidden_material():
    # Define hidden_material variable global for hide section
    global hidden_material
    # Prompt user to select hidden material text file
    hidden_material_filepath = filedialog.askopenfilename(
        title="Select File to Hide",
        filetypes=(
            ("text file", "*.txt"),
        )
    )
    # Check if the file was selected and output message
    if hidden_material_filepath:
        messagebox.showinfo("Selected File", f"You selected: {hidden_material_filepath}")
    else:
        messagebox.showwarning("No Selection", "No file was selected.")
    # Read contents of hidden material file path
    hidden_material = open(hidden_material_filepath, "r")
    # update the label
    selected_hidden_label.config(text=f"File selected to hide: {hidden_material_filepath}")

# Hide hidden material in the PNG file
# Hide using stego lsb steganography
def hide(steg_input_filepath, hidden_material):
    global output_file

    # Open the image using PIL
    image = Image.open(steg_input_filepath)

    if image.mode != "RGB":
        image = image.convert("RGB")

    output_file = filedialog.asksaveasfilename(
        title="Save File As",
        defaultextension=".png",
        filetypes=[("png files", "*.png")]
    )
    
    hidden_image = lsb.hide(image, hidden_material.read())
    hidden_image.save(output_file)

    if output_file:
        messagebox.showinfo("Success", f"Hidden file saved as {output_file}")
    else:
        messagebox.showwarning("File Not Saved", "No file was saved")

#select stego png file to reveal
def select_reveal_png():
    # Define steg_reveal_filepath as global for reveal button
    global steg_reveal_filepath
    # Prompt user to select PNG file to reveal
    steg_reveal_filepath = filedialog.askopenfilename(
        title="Select PNG Image",
        filetypes=(
            ("png files", "*.png"),
        )
    )
    # Check if a file was selected and output message
    if steg_reveal_filepath:
        messagebox.showinfo("Selected File", f"You selected: {steg_reveal_filepath}")
    else:
        messagebox.showwarning("No File Selected", "No file was selected.")
    #update label
    selected_reveal_label.config(text=f"File selected to reveal: {steg_reveal_filepath}")

# Reveal txt file using stego lsb steganography
def reveal():
    #reveal
    extracted_file = filedialog.asksaveasfilename(
        title="Save File As",
        defaultextension=".txt",
        filetypes=[("text file", "*.txt")]
    )
    clear_message=lsb.reveal(steg_reveal_filepath)
    with open(extracted_file, "w") as f:
        f.write(clear_message)
    # Check if a file was saved and output message
    if extracted_file:
        messagebox.showinfo("Success", f"Hidden file saved as {extracted_file}")
    else:
        messagebox.showwarning("No File Saved", "No file was saved.")

# Steganography User Interface
stego_label = tk.Label(window, text="Steganography:", font=("Segoe UI", 12, "bold"))
stego_label.place(x=540, y=220)

stego_instr = tk.Label(
    window,
    text=(
        "• Only PNG images are supported\n"
        "• Select an image and a file to hide\n"
        "• Click Hide to embed the file\n"
        "• Click Reveal to extract hidden data"
    ),
    font=("Segoe UI", 9),
    justify="left",
    padx=10,
    pady=10,
    wraplength=250
)
stego_instr.place(x=540, y=250)

select_stego_image = ttk.Button(window, text="Select Image", command=select_input_png)
select_stego_image.place(x=560, y=420)

file_to_hide = ttk.Button(window, text="File to Hide", command=select_hidden_material)
file_to_hide.place(x=670, y=420)

hide_btn = ttk.Button(window, text="Hide", command=lambda: hide(steg_input_filepath, hidden_material))
hide_btn.place(x=780, y=420)

selected_image_label = tk.Label(
    window,
    text="Currently selected image: None",
    font=("Segoe UI", 9),
    anchor="w"
)
selected_image_label.place(x=540, y=460)

selected_hidden_label = tk.Label(
    window,
    text="Currently selected file to hide: None",
    font=("Segoe UI", 9),
    anchor="w"
)
selected_hidden_label.place(x=540, y=480)

# Reveal File Section
select_reveal_file = ttk.Button(window, text="Select File", command=select_reveal_png)
select_reveal_file.place(x=560, y=520)

reveal_btn = ttk.Button(window, text="Reveal", command=reveal)
reveal_btn.place(x=660, y=520)

selected_reveal_label = tk.Label(
    window,
    text="Currently selected file to reveal: None",
    font=("Segoe UI", 9),
    anchor="w"
)
selected_reveal_label.place(x=540, y=560)

toggle_button = ttk.Button(
    window,
    text=f"Switch to {next_theme(current_theme.get())} Mode",
    command=toggle_theme
)
toggle_button.place(x=750, y=20)

apply_theme("dark")


window.mainloop()



