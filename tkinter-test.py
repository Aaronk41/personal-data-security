import tkinter as tk
from tkinter import ttk

window = tk.Tk()

#Options
window.geometry('900x600')
window.configure(background="#333232")
window.title("StegCrypt")
window.resizable(0,0)

#Buttons
button_style = ttk.Style()
button_style.map('TButton', background=[('active','green')], foreground=[('active','green')])


Encrypt = ttk.Button(window, text="Encrypt")
Encrypt.place(x=625, y=175)

Decrypt = ttk.Button(window, text="Decrypt")
Decrypt.place(x=625, y=425)

Stego_Input = ttk.Button(window, text="Select Input File")
Stego_Input.place(x=200, y=175)

Stego_HiddenMessage = ttk.Button(window, text="Select File to Hide")
Stego_HiddenMessage.place(x=200, y=200)

Stego_Hide = ttk.Button(window, text="Hide!")
Stego_Hide.place(x=200, y=225)

Reveal = ttk.Button(window, text="Reveal")
Reveal.place(x=200, y=425)

window.mainloop()