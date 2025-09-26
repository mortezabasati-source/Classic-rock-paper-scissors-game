import tkinter as tk
from tkinter import messagebox

import random


# Huvudfönster
root = tk.Tk()
root.title("Sten Påse Sax")
root.geometry("400x400")


# Namninmatning
lable_name = tk.Label(root,text="Ditt namn")
lable_name.pack(pady=5)

entry = tk.Entry(root)
entry.pack()


# Steg 1: Ange namn och bekräfta
def confirm_name():
    name = entry.get()
    if not name:
        messagebox.showwarning("Fel", "Du måste ange ditt namn!")
        return
    messagebox.showinfo("Välkommen", f"Hej {name}! Välj ett av alternativen för att börja spela.")
    # Visa val-alternativen och startknappen
    lable_choice.pack(pady=10)
    radio_sten.pack(pady=10)
    radio_påse.pack(pady=10)
    radio_sax.pack(pady=10)
    button_play.pack(pady=10)


# Steg 2: Välj och spela
def play_game():
    name = entry.get()
    choice = choice_var.get()

    # Datorns val
    options = ["Sten", "Påse", "Sax"]
    computer_choice = random.choice(options)

    # Bestäm vinnare
    if choice == computer_choice:
        result = "Oavgjort!"
    elif ((choice == "Sten" and computer_choice == "Sax") or
        (choice == "Påse" and computer_choice == "Sten") or
        (choice == "Sax" and computer_choice == "Påse")):
        result = f"Grattis {name}, du vann!"
    else:
        result = f"Datorn vann!"

    messagebox.showinfo("Resultat", f"Hej {name}, du valde {choice}.\nDatorn valde {computer_choice}.\n{result}")

lable_choice = tk.Label(root, text="Välj: Sten, Påse eller Sax")
choice_var = tk.StringVar(value="Sten")
radio_sten = tk.Radiobutton(root, text="    Sten", variable=choice_var, value="Sten")
radio_påse = tk.Radiobutton(root, text="    Påse", variable=choice_var, value="Påse")
radio_sax = tk.Radiobutton(root, text="      Sax", variable=choice_var, value="Sax")

# Knapp för att bekräfta namn
button_confirm = tk.Button(root, text="Bekräfta namn", command=confirm_name)
button_confirm.pack(pady=10)

# Knapp för att spela
button_play = tk.Button(root, text="Spela", command=play_game)



root.mainloop()