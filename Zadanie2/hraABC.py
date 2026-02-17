import tkinter as tk
import random
import string

TOTAL_ROUNDS = 20
TIME_LIMIT_S = 3

COLORS = [
    "red", "blue", "green", "orange", "purple",
    "pink", "brown", "cyan", "magenta", "gold",
    "darkred", "darkblue", "darkgreen", "gray25"
]


class AlphabetClickGame:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Klikaj písmená - 20 kôl / 3 sekundy")

        self.round_index = 0
        self.score = 0
        self.current_letter = None

        self.awaiting_input = False
        self.timer_ids = []
        self.advance_id = None

        tk.Label(root, text="Stlač správne písmeno (A–Z).", font=("Arial", 16)).pack(pady=(12, 6))

        # Grafické kružky nad písmenom
        self.dots_lbl = tk.Label(root, text="", font=("Arial", 28))
        self.dots_lbl.pack(pady=(0, 2))

        self.letter_lbl = tk.Label(root, text="—", font=("Arial", 72, "bold"))
        self.letter_lbl.pack(pady=(0, 6))

        self.info_lbl = tk.Label(root, text="Kolo: 0/20", font=("Arial", 12))
        self.info_lbl.pack(pady=(0, 6))

        self.status_lbl = tk.Label(root, text="Stlač START", font=("Arial", 12))
        self.status_lbl.pack(pady=(0, 10))

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=(0, 12))

        self.start_btn = tk.Button(btn_frame, text="START", width=12, command=self.start_game)
        self.start_btn.grid(row=0, column=0, padx=6)

        self.retry_btn = tk.Button(btn_frame, text="HRAŤ ZNOVA", width=12, command=self.start_game, state="disabled")
        self.retry_btn.grid(row=0, column=1, padx=6)

        self.quit_btn = tk.Button(btn_frame, text="KONIEC", width=12, command=root.destroy)
        self.quit_btn.grid(row=0, column=2, padx=6)

        root.bind("<KeyPress>", self.on_key_press)

    def cancel_all_timers(self):
        for tid in self.timer_ids:
            try:
                self.root.after_cancel(tid)
            except Exception:
                pass
        self.timer_ids.clear()

        if self.advance_id is not None:
            try:
                self.root.after_cancel(self.advance_id)
            except Exception:
                pass
            self.advance_id = None

    def start_game(self):
        self.cancel_all_timers()

        self.round_index = 0
        self.score = 0
        self.current_letter = None
        self.awaiting_input = False

        self.start_btn.config(state="disabled")
        self.retry_btn.config(state="disabled")

        self.status_lbl.config(text="Hra beží. Máš 3 sekundy na každé písmeno.")
        self.dots_lbl.config(text="")
        self.letter_lbl.config(text="—", fg="black")
        self.info_lbl.config(text=f"Kolo: 0/{TOTAL_ROUNDS}")

        self.next_round()

    def next_round(self):
        self.cancel_all_timers()

        if self.round_index >= TOTAL_ROUNDS:
            self.end_game()
            return

        self.round_index += 1
        self.current_letter = random.choice(string.ascii_uppercase)
        color = random.choice(COLORS)

        self.awaiting_input = True

        self.letter_lbl.config(text=self.current_letter, fg=color)
        self.info_lbl.config(text=f"Kolo: {self.round_index}/{TOTAL_ROUNDS}")
        self.status_lbl.config(text="Stlač správne písmeno...")

        self.start_circle_countdown(TIME_LIMIT_S)

    def start_circle_countdown(self, seconds: int):
        # ●●● -> ●● -> ●
        def tick(remaining: int):
            if not self.awaiting_input:
                return
            if remaining <= 0:
                self.time_out()
                return

            self.dots_lbl.config(text="●" * remaining)
            tid = self.root.after(1000, lambda: tick(remaining - 1))
            self.timer_ids.append(tid)

        tick(seconds)

    def evaluate_round(self, correct: bool, message: str):
        if not self.awaiting_input:
            return

        self.awaiting_input = False
        self.cancel_all_timers()

        if correct:
            self.score += 1

        self.status_lbl.config(text=message)
        self.dots_lbl.config(text="")

        self.advance_id = self.root.after(500, self.next_round)

    def on_key_press(self, event):
        if not self.awaiting_input:
            return

        key = event.keysym.upper()
        if len(key) != 1 or key not in string.ascii_uppercase:
            return

        if key == self.current_letter:
            self.evaluate_round(True, f"Správne! (+1) {key}")
        else:
            self.evaluate_round(False, f"Zle! Stlačil si {key}, správne bolo {self.current_letter}")

    def time_out(self):
        self.evaluate_round(False, f"NESTIHOL SI! Správne bolo {self.current_letter}")

    def end_game(self):
        self.cancel_all_timers()
        self.awaiting_input = False

        if self.score == TOTAL_ROUNDS:
            self.letter_lbl.config(text="🎉", fg="green")
            self.status_lbl.config(text=f"Vyhral si! Skóre: {self.score}/{TOTAL_ROUNDS}")
        else:
            self.letter_lbl.config(text="✗", fg="red")
            self.status_lbl.config(text=f"Koniec hry. Skóre: {self.score}/{TOTAL_ROUNDS}")

        self.dots_lbl.config(text="")
        self.retry_btn.config(state="normal")


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("520x360")
    root.resizable(False, False)
    AlphabetClickGame(root)
    root.mainloop()
