import tkinter as tk
from tkinter import messagebox
import random

MAX_ROUNDS = 10

root = tk.Tk()
root.title("Sten Påse Sax")
root.geometry("480x300")
root.configure(background="#17EEAE")

# --- UI elements ---
label_name = tk.Label(root, text="Ditt namn:", background="#17EEAE")
entry_name = tk.Entry(root)

label_name.pack(pady=(12, 2))
entry_name.pack()


    
    
button_confirm = tk.Button(root, text="Bekräfta namn")
button_confirm.pack(pady=8)


label_choice = tk.Label(root, text=" Välj: Sten, Påse eller Sax", background="#17EEAE")
label_choice.pack(pady=10)
choices_frame = tk.Frame(root, background="#17EEAE")    
choices_frame.pack(pady=5)


btn_sten = tk.Button(choices_frame, text="✊", font=("times", 13), padx=25, pady=3, background="#c9f7d7", fg="black")
btn_sax  = tk.Button(choices_frame, text="✌️", font=("times", 13), padx=25, pady=3, background="#c9f7d7", fg="black")
btn_pase = tk.Button(choices_frame, text="✋", font=("times", 13), padx=25, pady=3, background="#c9f7d7", fg="black")

score_label = tk.Label(root, text="Poäng: Du 0 - Datorn 0")
round_label = tk.Label(root, text=f"Runda: 0/{MAX_ROUNDS}")

# --- Game state ---
player_name = ""
rounds_played = 0
player_score = 0
computer_score = 0
rounds_history = []  # [{'round':n,'player':..., 'computer':..., 'result':...}, ...]

# --- Helper functions ---
def enable_choice_buttons(enable: bool):
    state = tk.NORMAL if enable else tk.DISABLED
    btn_sten.config(state=state)
    btn_pase.config(state=state)
    btn_sax.config(state=state)

def update_labels():
    score_label.config(text=f"Poäng: Du {player_score} - Datorn {computer_score}")
    round_label.config(text=f"Runda: {rounds_played}/{MAX_ROUNDS}")
    round_label.configure(background="#17EEAE")
    score_label.configure(background="#17EEAE") 

def reset_series(keep_player=True):
    """Återställ serien. keep_player=True = samma spelare spelar en ny serie.
       keep_player=False = ny spelare får skriva in namn."""
    global rounds_played, player_score, computer_score, rounds_history
    rounds_played = 0
    player_score = 0
    computer_score = 0
    rounds_history = []
    update_labels()
    enable_choice_buttons(False)

    if not keep_player:
        # Dölj spel-widgets och tillåt ny spelare ange namn
        label_choice.pack_forget()
        choices_frame.pack_forget()
        score_label.pack_forget()
        round_label.pack_forget()
        entry_name.config(state=tk.NORMAL)
        button_confirm.config(state=tk.NORMAL)
    else:
        # Visa widgets och aktivera val-knappar
        if not label_choice.winfo_ismapped():
            label_choice.pack(pady=10)
        if not choices_frame.winfo_ismapped():
            choices_frame.pack(pady=5)
            # Packa knappar (gör detta bara en gång; winfo_ismapped hindrar duplicering)
            btn_sten.pack(side=tk.LEFT, padx=5)
            btn_pase.pack(side=tk.LEFT, padx=5)
            btn_sax.pack(side=tk.LEFT, padx=5)
        if not score_label.winfo_ismapped():
            score_label.pack(pady=5)
        if not round_label.winfo_ismapped():
            round_label.pack(pady=5)
        enable_choice_buttons(True)

def show_round_result_popup(round_no, player_choice, computer_choice, result_text):
    messagebox.showinfo(f"Runda {round_no} resultat",
                        f"Runda {round_no}/{MAX_ROUNDS}\n"
                        f"{player_name} valde {player_choice}.\n"
                        f"Datorn valde {computer_choice}.\n\n"
                        f"{result_text}")

def summarize_and_ask():
    # Resultattext för serien
    if player_score > computer_score:
        winner_text = f"Grattis {player_name}, du vann serien med {player_score}-{computer_score}!"
    elif computer_score > player_score:
        winner_text = f"Datorn vann serien med {computer_score}-{player_score}. Bättre lycka nästa gång!"
    else:
        winner_text = f"Serien slutade oavgjort {player_score}-{computer_score}!"

    # Rundsammanfattning (en rad per runda)
    rounds_summary_lines = [f"{r['round']}: {r['player']} vs {r['computer']} -> {r['result']}"
                             for r in rounds_history]
    rounds_summary = "\n".join(rounds_summary_lines)

    full_msg = f"{winner_text}\n\nRundsammanfattning:\n{rounds_summary}"
    messagebox.showinfo("Slutresultat", full_msg)

    # Fråga om fortsättning
    cont = messagebox.askyesno("Fortsätta?", "Vill du fortsätta spela med samma spelare?\n"
                                 "Klicka Nej för att låta en ny spelare börja.")
    if cont:
        # Starta ny serie med samma spelare
        reset_series(keep_player=True)
    else:
        # Nollställ för ny spelare
        reset_series(keep_player=False)

# --- Game logic ---
def determine_result(player_choice, computer_choice):
    if player_choice == computer_choice:
        return "Oavgjort"
    wins = {"Sten": "Sax", "Påse": "Sten", "Sax": "Påse"}
    if wins[player_choice] == computer_choice:
        return "Spelaren"
    else:
        return "Datorn"

def play_round(player_choice):
    global rounds_played, player_score, computer_score, rounds_history
    if rounds_played >= MAX_ROUNDS:
        return
    computer_choice = random.choice(["Sten", "Påse", "Sax"])
    result = determine_result(player_choice, computer_choice)
    rounds_played += 1

    if result == "Oavgjort":
        result_text = "Oavgjort!😐😐😐😐"
    elif result == "Spelaren":
        player_score += 1
        result_text = f"{player_name}, du vann rundan!😀😀😀😀"
    else:
        computer_score += 1
        result_text = "Datorn vann rundan!😢😢😢😢"

    rounds_history.append({
        'round': rounds_played,
        'player': player_choice,
        'computer': computer_choice,
        'result': result_text
    })

    update_labels()
    show_round_result_popup(rounds_played, player_choice, computer_choice, result_text)
    

    if rounds_played >= MAX_ROUNDS:
        enable_choice_buttons(False)
        summarize_and_ask()

# --- Event bindings ---
def on_confirm_name():
    global player_name
    name = entry_name.get().strip()
    if not name:
        messagebox.showwarning("Fel", "Du måste ange ditt namn!")
        return
    player_name = name
    entry_name.config(state=tk.DISABLED)
    button_confirm.config(state=tk.DISABLED)
    reset_series(keep_player=True)

button_confirm.config(command=on_confirm_name)
button_confirm.configure(background="#c9f7d7")
btn_sten.config(command=lambda: play_round("Sten"))
btn_sax.config(command=lambda: play_round("Sax"))
btn_pase.config(command=lambda: play_round("Påse"))

# Initial state: dolt spel och inaktiverade val-knappar
enable_choice_buttons(False)
label_choice.pack_forget()
choices_frame.pack_forget()
score_label.pack_forget()
round_label.pack_forget()

root.mainloop()
