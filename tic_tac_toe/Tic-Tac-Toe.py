import tkinter as tk
current_player = "X"
def button_click(row, col):
    global current_player

    if buttons[row][col]["text"] == " ":
        buttons[row][col]["text"] = current_player
        if check_winner():
            show_winner(f"🎉 Congrats Player {current_player}!")
        elif all(button["text"] != " " for row in buttons for button in row):
            show_winner("🤝 It's a Draw!")
        else:
            current_player = "O" if current_player == "X" else "X"

def check_winner():
    for i in range(3):
        if buttons[i][0]["text"] == buttons[i][1]["text"] == buttons[i][2]["text"] != " ":
            return True
        if buttons[0][i]["text"] == buttons[1][i]["text"] == buttons[2][i]["text"] != " ":
            return True
    if buttons[0][0]["text"] == buttons[1][1]["text"] == buttons[2][2]["text"] != " ":
        return True
    if buttons[0][2]["text"] == buttons[1][1]["text"] == buttons[2][0]["text"] != " ":
        return True
    return False

def show_winner(message):
    popup = tk.Toplevel()
    popup.title("Game Over")
    popup.geometry("350x250")
    popup.configure(bg="lightyellow")
    popup.resizable(False, False)

    label = tk.Label(popup, text=message, font=("Arial", 20, "bold"), fg="green", bg="lightyellow")
    label.pack(pady=30)

    button_frame = tk.Frame(popup, bg="lightyellow")
    button_frame.pack(pady=10)

    exit_btn = tk.Button(button_frame, text="Exit", font=("Arial", 14), bg="red", fg="white", width=10, command=window.quit)
    exit_btn.pack(side="left", padx=10)

    play_again_btn = tk.Button(button_frame, text="Play Again", font=("Arial", 14), bg="blue", fg="white", width=12, command=lambda: [popup.destroy(), reset_board()])
    play_again_btn.pack(side="left", padx=10)

def reset_board():
    global current_player
    current_player = "X"
    for row in buttons:
        for btn in row:
            btn["text"] = " "

window = tk.Tk()
window.title("Tic-Tac-Toe 🎮")
buttons = [[None, None, None] for _ in range(3)]
for row in range(3):
    for col in range(3):
        button = tk.Button(window, text=" ", font=("Arial", 32), width=5, height=2,
                           command=lambda r=row, c=col: button_click(r, c))
        button.grid(row=row, column=col)
        buttons[row][col] = button
window.mainloop()
