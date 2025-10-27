import tkinter as tk
from tkinter import ttk
import os
from PIL import Image, ImageTk

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

# Encryption Section
encrypt_label = tk.Label(window, text="Encryption:", font=("Segoe UI", 12, "bold"))
encrypt_label.place(x=160, y=220)

encrypt_instr = tk.Label(
    window,
    text=(
        "• Select a file (max size: 50–100 MB)\n"
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

encrypt_btn = ttk.Button(window, text="Encrypt")
encrypt_btn.place(x=280, y=420)

selected_encrypt_label = tk.Label(
    window,
    text="Currently selected encryption file: None",
    font=("Segoe UI", 9),
    anchor="w"
)
selected_encrypt_label.place(x=160, y=460)

# Decrypt Section
select_decrypt_file = ttk.Button(window, text="Select File")
select_decrypt_file.place(x=180, y=490)

decrypt_btn = ttk.Button(window, text="Decrypt")
decrypt_btn.place(x=280, y=490)

selected_decrypt_label = tk.Label(
    window,
    text="Currently selected file to decrypt: None",
    font=("Segoe UI", 9),
    anchor="w"
)
selected_decrypt_label.place(x=160, y=530)

# Steganography Section
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

select_stego_image = ttk.Button(window, text="Select Image")
select_stego_image.place(x=560, y=420)

file_to_hide = ttk.Button(window, text="File to Hide")
file_to_hide.place(x=670, y=420)

hide_btn = ttk.Button(window, text="Hide")
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
select_reveal_file = ttk.Button(window, text="Select File")
select_reveal_file.place(x=560, y=520)

reveal_btn = ttk.Button(window, text="Reveal")
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