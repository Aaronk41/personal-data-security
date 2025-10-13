import tkinter as tk
from tkinter import filedialog, messagebox
from stegano import lsb

#Define variables for functions
steg_input_filepath = None
hidden_material = None
steg_reveal_filepath = None
output_file = None
extracted_file = None

#Functions
##select input png file to hide message in
def select_input_png():
    global steg_input_filepath
    steg_input_filepath = filedialog.askopenfilename(
        title="Select PNG Image",
        filetypes=(
            ("png files", "*.png"),
        )
    )
    #output
    if steg_input_filepath:  #check if a file was actually selected
        messagebox.showinfo("Selected File", f"You selected: {steg_input_filepath}")
    else:
        messagebox.showwarning("No Selection", "No file was selected.")
##select text file with hidden message
def select_hidden_material():
    global hidden_material
    hidden_material_filepath = filedialog.askopenfilename(
        title="Select File to Hide",
        filetypes=(
            ("select text file", "*.txt"),
        )
    )
    if hidden_material_filepath:  #check if a file was actually selected
        messagebox.showinfo("Selected File", f"You selected: {hidden_material_filepath}")
    else:
        messagebox.showwarning("No Selection", "No file was selected.")
    #read contents of hidden material file path
    hidden_material = open(hidden_material_filepath, "r")
##hide using stego lsb steganography
def hide():
    global output_file
    output_file = "steg.png"
    hidden_image = lsb.hide(steg_input_filepath, hidden_material.read())
    hidden_image.save(output_file)
    #output message
    messagebox.showinfo("Success", f"Hidden file saved as {output_file}")
##select stego png file to reveal
def select_reveal_png():
    global steg_reveal_filepath
    steg_reveal_filepath = filedialog.askopenfilename(
        title="Select PNG Image",
        filetypes=(
            ("png files", "*.png"),
        )
    )
    #output
    if steg_reveal_filepath:  #check if a file was actually selected
        messagebox.showinfo("Selected File", f"You selected: {steg_reveal_filepath}")
    else:
        messagebox.showwarning("No Selection", "No file was selected.")
##reveal txt file using stego lsb steganography
def reveal():
    #reveal
    extracted_file="steg-reveal.txt"
    clear_message=lsb.reveal(output_file)
    with open(extracted_file, "w") as f:
        f.write(clear_message)
    #output
    messagebox.showinfo("Success", f"Hidden file saved as {extracted_file}")
#create the window
root = tk.Tk()
root.title("Steganography Example")
root.geometry("400x150")

#buttons
open_PNG_button = tk.Button(root, text="Open PNG Input File", command=select_input_png)
open_PNG_button.grid(row=1, column=1, pady=10, padx=10)

open_Hidden_Material_button = tk.Button(root, text="Open Material to Hide", command=select_hidden_material)
open_Hidden_Material_button.grid(row=1, column=2, pady=10)

Hide_button = tk.Button(root, text="Hide!", command=hide)
Hide_button.grid(row=1, column=3, pady=10, padx=10)

open_to_reveal_button = tk.Button(root, text="Open Material to Reveal", command=select_reveal_png)
open_to_reveal_button.grid(row=2, column=1, pady=10, padx=10)

Reveal_button = tk.Button(root, text="Reveal!", command=reveal)
Reveal_button.grid(row=2, column=2, pady=10, padx=10)

#event loop for tkinter
root.mainloop()