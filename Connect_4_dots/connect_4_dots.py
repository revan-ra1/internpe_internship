import tkinter as tk
from tkinter import messagebox

ROWS = 6
COLS = 7

class Connect4:
    def __init__(self, root):
        self.root = root
        self.root.title("Connect 4")

        self.turn = 1  # 1 = Red, 2 = Yellow
        self.board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.buttons = [[None for _ in range(COLS)] for _ in range(ROWS)]

        self.hover_col = None  # Track which column is hovered

        # Main frame
        self.frame = tk.Frame(self.root, bg="#1E1E1E")
        self.frame.pack(padx=10, pady=10)

        # Status label
        self.status_label = tk.Label(self.root, text="Red's Turn", font=("Arial", 16, "bold"))
        self.status_label.pack(pady=5)

        # Play again button (hidden initially)
        self.play_again_btn = tk.Button(self.root, text="Play Again", font=("Arial", 14, "bold"),
                                        bg="#0078D7", fg="white", command=self.reset_game)
        self.play_again_btn.pack(pady=5)
        self.play_again_btn.pack_forget()  # hide until game ends

        self.create_board()

    def create_board(self):
        for r in range(ROWS):
            for c in range(COLS):
                btn = tk.Button(self.frame, text=" ", width=6, height=3,
                                command=lambda col=c: self.drop_disc(col),
                                bg="#ECECEC", relief="raised")
                btn.grid(row=r, column=c, padx=2, pady=2)
                btn.bind("<Enter>", lambda e, col=c: self.highlight_column(col))
                btn.bind("<Leave>", lambda e, col=c: self.unhighlight_column(col))
                self.buttons[r][c] = btn

    def highlight_column(self, col):
        if self.hover_col is not None:
            self.unhighlight_column(self.hover_col)
        for r in range(ROWS):
            if self.board[r][col] == 0:  # only highlight empty slots
                self.buttons[r][col].config(bg="#D0E6FF")
        self.hover_col = col

    def unhighlight_column(self, col):
        for r in range(ROWS):
            if self.board[r][col] == 0:
                self.buttons[r][col].config(bg="#ECECEC")

    def drop_disc(self, col):
        for row in range(ROWS - 1, -1, -1):
            if self.board[row][col] == 0:
                self.board[row][col] = self.turn
                color = "red" if self.turn == 1 else "yellow"
                self.buttons[row][col].config(bg=color)

                if self.check_winner(row, col):
                    winner = "Red" if self.turn == 1 else "Yellow"
                    self.show_winner_popup(winner)
                    return
                elif all(self.board[0][c] != 0 for c in range(COLS)):
                    self.show_winner_popup("Draw")
                    return
                else:
                    self.turn = 2 if self.turn == 1 else 1
                    self.status_label.config(text=f"{'Red' if self.turn == 1 else 'Yellow'}'s Turn")
                return
        messagebox.showwarning("Invalid Move", "Column is full!")

    def check_winner(self, r, c):
        def count_dir(dr, dc):
            count = 0
            row, col = r + dr, c + dc
            while 0 <= row < ROWS and 0 <= col < COLS and self.board[row][col] == self.turn:
                count += 1
                row += dr
                col += dc
            return count

        directions = [(0,1), (1,0), (1,1), (1,-1)]
        for dr, dc in directions:
            count = 1 + count_dir(dr, dc) + count_dir(-dr, -dc)
            if count >= 4:
                return True
        return False

    def show_winner_popup(self, winner):
        popup = tk.Toplevel(self.root)
        popup.title("🎉 Game Over 🎉")
        popup.geometry("300x200")
        popup.configure(bg="#222")

        if winner == "Draw":
            msg = "It's a Draw!"
            color = "white"
        else:
            msg = f"{winner} Wins!"
            color = "red" if winner == "Red" else "gold"

        label = tk.Label(popup, text=msg, font=("Arial", 28, "bold"),
                         fg=color, bg="#222")
        label.pack(expand=True)

        tk.Button(popup, text="Play Again", font=("Arial", 14, "bold"),
                  bg="#0078D7", fg="white", command=lambda: [popup.destroy(), self.reset_game()]).pack(pady=10)
        tk.Button(popup, text="Exit", font=("Arial", 12),
                  command=self.root.destroy).pack()

    def reset_game(self):
        self.board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        for r in range(ROWS):
            for c in range(COLS):
                self.buttons[r][c].config(bg="#ECECEC")
        self.turn = 1
        self.status_label.config(text="Red's Turn")
        self.play_again_btn.pack_forget()

if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="#1E1E1E")
    game = Connect4(root)
    root.mainloop()
