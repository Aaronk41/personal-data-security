import tkinter as tk
from tkinter import ttk
import os
from PIL import Image, ImageTk

# styles
window = tk.Tk()
window.geometry('900x600')
window.configure(background="#1e1e1e")
window.title("StegCrypt")
window.resizable(0, 0)

style = ttk.Style()
style.theme_use("clam")
style.configure(
    "TButton",
        background="#2b2b2b",
        foreground="white",
        font=("Segoe UI", 10, "bold"),
        padding=5
    )
style.map(
    "TButton",
        background=[('active', "#1d9ab9")],
        foreground=[('active', 'black')]
)


title = tk.Label(
    window,
        text="StegCrypt",
        font=("Helvetica", 22, "bold"),
        bg="#1e1e1e",
        fg="#1d9ab9"
    )
title.place(x=380, y=20)

# Logo 
img_path = os.path.join(os.path.dirname(__file__), "dino.png")
if os.path.exists(img_path):
    img = Image.open(img_path)
    img = img.resize((120, 120))
    logo_img = ImageTk.PhotoImage(img)
    logo = tk.Label(window, image=logo_img, bg="#1e1e1e")
    logo.place(x=390, y=70)
else:
    logo = tk.Label(
        window,
        text="(logo)",
        font=("Helvetica", 12, "italic"),
        bg="#1e1e1e",
        fg="gray"
    )
    logo.place(x=430, y=120)

# Encryption Section
encrypt_label = tk.Label(
    window,
        text="Encryption:",
        font=("Segoe UI", 12, "bold"),
        bg="#1e1e1e",
        fg="white"
)
encrypt_label.place(x=160, y=220)

encrypt_instr = tk.Label(
    window,
        text=(
            "• Select a file (max size: 50–100 MB)\n"
            "• Click Encrypt to fully encrypt it\n"
            "• Click Decrypt to reverse encryption"
        ),
        font=("Segoe UI", 9),
        bg="#2e2e2e",
        fg="white",
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
        bg="#1e1e1e",
        fg="white",
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
        bg="#1e1e1e",
        fg="white",
        anchor="w"
)
selected_decrypt_label.place(x=160, y=530)

# Steganography Section
stego_label = tk.Label(
    window,
        text="Steganography:",
        font=("Segoe UI", 12, "bold"),
        bg="#1e1e1e",
        fg="white"
    )
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
        bg="#2e2e2e",
        fg="white",
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
        bg="#1e1e1e",
        fg="white",
        anchor="w"
)
selected_image_label.place(x=540, y=460)

selected_hidden_label = tk.Label(
    window,
        text="Currently selected file to hide: None",
        font=("Segoe UI", 9),
        bg="#1e1e1e",
        fg="white",
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
        bg="#1e1e1e",
        fg="white",
        anchor="w"
)
selected_reveal_label.place(x=540, y=560)

window.mainloop()

