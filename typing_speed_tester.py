"""
================================================================================
                    COLLEGE PYTHON MINI PROJECT: TYPING SPEED TESTER
================================================================================
Title: Typing Speed Tester
Subtitle: Test Your Typing Speed and Accuracy
File: typing_speed_tester.py
Description: A standalone offline desktop application built using Python 3 and
             Tkinter to evaluate typing speed (Words Per Minute - WPM) and accuracy.

Demonstrates Core Python Concepts:
  1. Strings: Text slicing, character iteration, length checks, comparison.
  2. Lists: Curated collections of Easy, Medium, and Hard test paragraphs.
  3. Functions: Modular logic for GUI creation, timer, calculations, and flow.
  4. Conditional Statements: Performance rating, input validation, timer state.
  5. Loops: Character-by-character comparison and tag indexing.
  6. Tkinter GUI: Frames, Labels, Text, Entry, Combobox, Buttons, Canvas.

Dependencies: Python 3 Standard Library only (tkinter, random, time).
Run Command:
  python typing_speed_tester.py
================================================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
import time

# ==============================================================================
# SECTION 1: PARAGRAPH COLLECTIONS (LISTS & STRINGS)
# ==============================================================================
EASY_PARAGRAPHS = [
    "The quick brown fox jumps over the lazy dog. A warm breeze blew through the tall green trees on a sunny afternoon.",
    "Learning to code is fun and rewarding. Practice every single day to build great software and solve real problems.",
    "The morning sun shone brightly across the calm lake. Birds were singing sweet songs as fishermen set up their small boats.",
    "Reading books every day opens your mind to wonderful ideas. It helps you speak better and understand the world around you.",
    "A journey of a thousand miles begins with a single step. Stay patient and keep moving forward toward your biggest goals."
]

MEDIUM_PARAGRAPHS = [
    "Python is known for its clear syntax and readability. Programmers love using it for web development, automation, and data analysis tasks.",
    "Consistent daily typing practice trains muscle memory in your fingers. Over time, you will type effortlessly without looking at the keyboard keys.",
    "In computer science, algorithms are step-by-step instructions designed to solve complex challenges efficiently with minimal computational resources.",
    "Modern operating systems manage memory, CPU scheduling, and input devices seamlessly so users can run multiple applications simultaneously.",
    "Creativity combined with logical thinking allows software engineers to build applications that change how billions of people communicate and work."
]

HARD_PARAGRAPHS = [
    "Object-oriented programming encompasses encapsulation, inheritance, and polymorphism; each principle ensures robust, scalable software architectures.",
    "According to research in cognitive psychology (circa 2021), rapid touch-typing requires synchronized motor reflexes, achieving 80+ WPM with 98% accuracy!",
    "Syntactic simplicity in Python 3.10+ enables rapid prototyping: list comprehensions [x**2 for x in data], lambda expressions, and pattern matching.",
    "Distributed database systems must balance consistency, availability, and partition tolerance—famously formalized by Eric Brewer as the CAP theorem.",
    "Cryptographic hash algorithms like SHA-256 produce deterministic, fixed-length digests (256 bits) virtually impossible to invert or counterfeit."
]


# ==============================================================================
# SECTION 2: CORE CALCULATION & STRING PROCESSING FUNCTIONS
# ==============================================================================

def compare_text(original: str, typed: str):
    """
    Compares the original paragraph with user typed text character-by-character.
    Handles different text lengths, empty inputs, and extra characters safely.
    """
    total_typed = len(typed)
    correct_count = 0
    incorrect_count = 0
    
    for i in range(total_typed):
        if i < len(original):
            if typed[i] == original[i]:
                correct_count += 1
            else:
                incorrect_count += 1
        else:
            incorrect_count += 1
            
    return correct_count, incorrect_count, total_typed


def calculate_wpm(characters_typed: int, elapsed_seconds: float) -> int:
    """
    Calculates Words Per Minute (WPM) using:
      WPM = (Characters Typed / 5) / Time in Minutes
    """
    if elapsed_seconds <= 0 or characters_typed <= 0:
        return 0
    time_in_minutes = elapsed_seconds / 60.0
    wpm = (characters_typed / 5.0) / time_in_minutes
    return max(0, int(round(wpm)))


def calculate_accuracy(correct_chars: int, total_chars: int) -> float:
    """
    Calculates typing accuracy percentage:
      Accuracy = (Correct Characters / Total Typed Characters) * 100
    """
    if total_chars <= 0:
        return 0.0
    accuracy = (correct_chars / total_chars) * 100.0
    return max(0.0, min(100.0, round(accuracy, 1)))


def get_performance_rating(wpm: int, accuracy: float) -> tuple:
    """Returns (headline, feedback_message, color_hex) based on WPM and accuracy."""
    if wpm >= 50 and accuracy >= 90.0:
        return "Excellent!", "Outstanding typing speed and superb accuracy! Keep it up!", "#2e7d32"
    elif wpm >= 35 and accuracy >= 85.0:
        return "Great Job!", "Very solid typing speed with good control over accuracy.", "#1565c0"
    elif wpm >= 20 and accuracy >= 75.0:
        return "Good Work!", "Decent performance! A bit more daily practice will push you higher.", "#e65100"
    else:
        return "Keep Practicing!", "Focus on accuracy first, and your typing speed will naturally follow.", "#c2185b"


# ==============================================================================
# SECTION 3: APPLICATION GUI CLASS (TKINTER)
# ==============================================================================

class TypingSpeedTesterApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Typing Speed Tester")
        self.root.geometry("860x680")
        self.root.minsize(780, 600)
        self.root.configure(bg="#f4f6f9")
        self.center_window(860, 680)

        # State Variables
        self.duration_var = tk.StringVar(value="30")
        self.difficulty_var = tk.StringVar(value="Medium")
        
        self.target_text = ""
        self.time_limit = 30
        self.time_remaining = 30
        self.test_started = False
        self.test_finished = False
        self.timer_job = None
        self.start_timestamp = None
        
        self.current_wpm = 0
        self.current_accuracy = 0.0
        self.current_total_typed = 0
        self.current_correct = 0
        self.current_incorrect = 0

        self.container = tk.Frame(self.root, bg="#f4f6f9")
        self.container.pack(fill=tk.BOTH, expand=True)

        self.setup_styles()
        self.create_home_screen()

    def center_window(self, width: int, height: int):
        self.root.update_idletasks()
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        pos_x = max(0, (screen_w // 2) - (width // 2))
        pos_y = max(0, (screen_h // 2) - (height // 2))
        self.root.geometry(f"{width}x{height}+{pos_x}+{pos_y}")

    def setup_styles(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

    def clear_container(self):
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None
        for widget in self.container.winfo_children():
            widget.destroy()

    def create_home_screen(self):
        self.clear_container()
        card = tk.Frame(self.container, bg="#ffffff", bd=1, relief=tk.SOLID, padx=40, pady=30)
        card.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=740, height=580)

        tk.Label(card, text="Typing Speed Tester", font=("Helvetica", 26, "bold"), fg="#1e293b", bg="#ffffff").pack(pady=(10, 4))
        tk.Label(card, text="Test Your Typing Speed and Accuracy", font=("Helvetica", 13), fg="#64748b", bg="#ffffff").pack(pady=(0, 25))

        tk.Frame(card, height=2, bg="#e2e8f0").pack(fill=tk.X, padx=20, pady=(0, 20))

        controls_frame = tk.Frame(card, bg="#ffffff")
        controls_frame.pack(fill=tk.X, pady=10)

        tk.Label(controls_frame, text="Select Duration:", font=("Helvetica", 11, "bold"), fg="#334155", bg="#ffffff").grid(row=0, column=0, sticky="w", padx=(30, 15), pady=8)
        dur_cb = ttk.Combobox(controls_frame, textvariable=self.duration_var, values=["30", "60"], state="readonly", width=15, font=("Helvetica", 11))
        dur_cb.grid(row=0, column=1, sticky="w", pady=8)
        tk.Label(controls_frame, text="Seconds", font=("Helvetica", 11), fg="#64748b", bg="#ffffff").grid(row=0, column=2, sticky="w", padx=(8, 0), pady=8)

        tk.Label(controls_frame, text="Select Difficulty:", font=("Helvetica", 11, "bold"), fg="#334155", bg="#ffffff").grid(row=1, column=0, sticky="w", padx=(30, 15), pady=8)
        diff_cb = ttk.Combobox(controls_frame, textvariable=self.difficulty_var, values=["Easy", "Medium", "Hard"], state="readonly", width=15, font=("Helvetica", 11))
        diff_cb.grid(row=1, column=1, sticky="w", pady=8)

        info_frame = tk.Frame(card, bg="#f8fafc", bd=1, relief=tk.GROOVE, padx=15, pady=10)
        info_frame.pack(fill=tk.X, padx=30, pady=18)
        tk.Label(info_frame, text="Quick Guide:", font=("Helvetica", 10, "bold"), fg="#0f172a", bg="#f8fafc").pack(anchor="w")
        info_text = (
            "1. Choose duration (30 or 60 seconds) and difficulty.\n"
            "2. Click 'START TEST' and type the text as fast and accurately as you can.\n"
            "3. Live stats (WPM, Accuracy, Characters) update in real-time.\n"
            "4. When time expires, your complete performance report appears."
        )
        tk.Label(info_frame, text=info_text, font=("Helvetica", 9), fg="#475569", bg="#f8fafc", justify=tk.LEFT).pack(anchor="w", pady=(3, 0))

        btn_frame = tk.Frame(card, bg="#ffffff")
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="START TEST", font=("Helvetica", 12, "bold"), bg="#2563eb", fg="#ffffff", activebackground="#1d4ed8", activeforeground="#ffffff", padx=25, pady=10, bd=0, cursor="hand2", command=self.start_test).grid(row=0, column=0, padx=8)
        tk.Button(btn_frame, text="Instructions", font=("Helvetica", 11), bg="#e2e8f0", fg="#1e293b", padx=18, pady=10, bd=0, cursor="hand2", command=self.show_instructions).grid(row=0, column=1, padx=8)
        tk.Button(btn_frame, text="Exit", font=("Helvetica", 11), bg="#f1f5f9", fg="#dc2626", padx=18, pady=10, bd=0, cursor="hand2", command=self.exit_app).grid(row=0, column=2, padx=8)

    def start_test(self):
        self.clear_container()
        try:
            self.time_limit = int(self.duration_var.get())
        except ValueError:
            self.time_limit = 30
        self.time_remaining = self.time_limit

        diff = self.difficulty_var.get()
        if diff == "Easy":
            self.target_text = random.choice(EASY_PARAGRAPHS)
        elif diff == "Hard":
            self.target_text = random.choice(HARD_PARAGRAPHS)
        else:
            self.target_text = random.choice(MEDIUM_PARAGRAPHS)

        self.test_started = False
        self.test_finished = False
        self.start_timestamp = None
        self.current_wpm = 0
        self.current_accuracy = 0.0
        self.current_total_typed = 0
        self.current_correct = 0
        self.current_incorrect = 0

        self.build_test_ui()

    def build_test_ui(self):
        header_frame = tk.Frame(self.container, bg="#ffffff", bd=1, relief=tk.SOLID)
        header_frame.pack(fill=tk.X, padx=20, pady=(15, 10))
        tk.Label(header_frame, text="TYPING SPEED TEST", font=("Helvetica", 16, "bold"), fg="#1e293b", bg="#ffffff").pack(side=tk.LEFT, padx=15, pady=10)
        tk.Label(header_frame, text=f"Difficulty: {self.difficulty_var.get()}  |  Duration: {self.time_limit}s", font=("Helvetica", 10, "bold"), fg="#2563eb", bg="#eff6ff", padx=10, pady=4).pack(side=tk.RIGHT, padx=15, pady=10)

        stats_frame = tk.Frame(self.container, bg="#f4f6f9")
        stats_frame.pack(fill=tk.X, padx=20, pady=5)
        card_w = 175

        # 4 Stats: Time, WPM, Accuracy, Characters
        card_time = tk.Frame(stats_frame, bg="#ffffff", bd=1, relief=tk.SOLID, width=card_w, height=75)
        card_time.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5)
        tk.Label(card_time, text="TIME REMAINING", font=("Helvetica", 9, "bold"), fg="#64748b", bg="#ffffff").pack(pady=(8, 2))
        self.stat_time_lbl = tk.Label(card_time, text=f"{self.time_remaining}s", font=("Helvetica", 18, "bold"), fg="#dc2626", bg="#ffffff")
        self.stat_time_lbl.pack()

        card_wpm = tk.Frame(stats_frame, bg="#ffffff", bd=1, relief=tk.SOLID, width=card_w, height=75)
        card_wpm.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5)
        tk.Label(card_wpm, text="SPEED (WPM)", font=("Helvetica", 9, "bold"), fg="#64748b", bg="#ffffff").pack(pady=(8, 2))
        self.stat_wpm_lbl = tk.Label(card_wpm, text="0", font=("Helvetica", 18, "bold"), fg="#2563eb", bg="#ffffff")
        self.stat_wpm_lbl.pack()

        card_acc = tk.Frame(stats_frame, bg="#ffffff", bd=1, relief=tk.SOLID, width=card_w, height=75)
        card_acc.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5)
        tk.Label(card_acc, text="ACCURACY", font=("Helvetica", 9, "bold"), fg="#64748b", bg="#ffffff").pack(pady=(8, 2))
        self.stat_acc_lbl = tk.Label(card_acc, text="0%", font=("Helvetica", 18, "bold"), fg="#16a34a", bg="#ffffff")
        self.stat_acc_lbl.pack()

        card_chars = tk.Frame(stats_frame, bg="#ffffff", bd=1, relief=tk.SOLID, width=card_w, height=75)
        card_chars.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5)
        tk.Label(card_chars, text="CHARACTERS", font=("Helvetica", 9, "bold"), fg="#64748b", bg="#ffffff").pack(pady=(8, 2))
        self.stat_chars_lbl = tk.Label(card_chars, text="0", font=("Helvetica", 18, "bold"), fg="#7c3aed", bg="#ffffff")
        self.stat_chars_lbl.pack()

        target_frame = tk.LabelFrame(self.container, text=" Paragraph to Type ", font=("Helvetica", 10, "bold"), fg="#475569", bg="#f8fafc", padx=12, pady=8)
        target_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=(10, 8))

        self.target_text_widget = tk.Text(target_frame, wrap=tk.WORD, font=("Consolas", 13), bg="#f8fafc", fg="#334155", bd=0, highlightthickness=0, height=4, padx=6, pady=6)
        self.target_text_widget.pack(fill=tk.BOTH, expand=True)
        self.target_text_widget.insert("1.0", self.target_text)
        self.target_text_widget.configure(state=tk.DISABLED)

        self.target_text_widget.tag_configure("correct", foreground="#16a34a", background="#dcfce7")
        self.target_text_widget.tag_configure("incorrect", foreground="#dc2626", background="#fee2e2")
        self.target_text_widget.tag_configure("current", background="#fef08a")

        input_frame = tk.LabelFrame(self.container, text=" Your Typing Area (Start typing here to trigger timer) ", font=("Helvetica", 10, "bold"), fg="#2563eb", bg="#ffffff", padx=12, pady=8)
        input_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=(0, 10))

        self.input_text_widget = tk.Text(input_frame, wrap=tk.WORD, font=("Consolas", 13), bg="#ffffff", fg="#0f172a", bd=1, relief=tk.SOLID, height=4, padx=6, pady=6, insertbackground="#2563eb")
        self.input_text_widget.pack(fill=tk.BOTH, expand=True)
        self.input_text_widget.focus_set()
        self.input_text_widget.bind("<KeyRelease>", self.handle_typing)

        bottom_bar = tk.Frame(self.container, bg="#f4f6f9")
        bottom_bar.pack(fill=tk.X, padx=25, pady=(0, 12))
        tk.Button(bottom_bar, text="Restart Test", font=("Helvetica", 10, "bold"), bg="#e2e8f0", fg="#1e293b", padx=14, pady=6, bd=0, cursor="hand2", command=self.reset_test).pack(side=tk.LEFT)
        tk.Button(bottom_bar, text="Back to Home", font=("Helvetica", 10), bg="#f1f5f9", fg="#475569", padx=14, pady=6, bd=0, cursor="hand2", command=self.back_to_home).pack(side=tk.LEFT, padx=10)
        self.tip_lbl = tk.Label(bottom_bar, text="Hint: Timer starts on your first keystroke!", font=("Helvetica", 9, "italic"), fg="#64748b", bg="#f4f6f9")
        self.tip_lbl.pack(side=tk.RIGHT)

    def start_timer(self):
        if not self.test_started and not self.test_finished:
            self.test_started = True
            self.start_timestamp = time.time()
            self.tip_lbl.config(text="Test in progress... Keep typing!")
            self.update_timer()

    def update_timer(self):
        if self.test_finished:
            return
        if self.time_remaining > 0:
            self.stat_time_lbl.config(text=f"{self.time_remaining}s")
            self.time_remaining -= 1
            self.timer_job = self.root.after(1000, self.update_timer)
        else:
            self.stat_time_lbl.config(text="0s")
            self.finish_test()

    def handle_typing(self, event=None):
        if self.test_finished:
            return
        if not self.test_started:
            self.start_timer()

        typed_content = self.input_text_widget.get("1.0", "end-1c")
        correct_count, incorrect_count, total_typed = compare_text(self.target_text, typed_content)
        
        self.current_correct = correct_count
        self.current_incorrect = incorrect_count
        self.current_total_typed = total_typed

        elapsed = 0.0
        if self.start_timestamp:
            elapsed = max(0.1, time.time() - self.start_timestamp)

        self.current_wpm = calculate_wpm(total_typed, elapsed)
        self.current_accuracy = calculate_accuracy(correct_count, total_typed)
        self.update_statistics()
        self.highlight_target_paragraph(typed_content)

        if len(typed_content) >= len(self.target_text):
            self.finish_test()

    def highlight_target_paragraph(self, typed: str):
        self.target_text_widget.configure(state=tk.NORMAL)
        self.target_text_widget.tag_remove("correct", "1.0", tk.END)
        self.target_text_widget.tag_remove("incorrect", "1.0", tk.END)
        self.target_text_widget.tag_remove("current", "1.0", tk.END)

        for i, ch in enumerate(typed):
            if i >= len(self.target_text):
                break
            start_idx = f"1.0 + {i} chars"
            end_idx = f"1.0 + {i + 1} chars"
            if ch == self.target_text[i]:
                self.target_text_widget.tag_add("correct", start_idx, end_idx)
            else:
                self.target_text_widget.tag_add("incorrect", start_idx, end_idx)

        curr_len = len(typed)
        if curr_len < len(self.target_text):
            c_start = f"1.0 + {curr_len} chars"
            c_end = f"1.0 + {curr_len + 1} chars"
            self.target_text_widget.tag_add("current", c_start, c_end)

        self.target_text_widget.configure(state=tk.DISABLED)

    def update_statistics(self):
        self.stat_wpm_lbl.config(text=str(self.current_wpm))
        self.stat_acc_lbl.config(text=f"{self.current_accuracy}%")
        self.stat_chars_lbl.config(text=str(self.current_total_typed))

    def finish_test(self):
        if self.test_finished:
            return
        self.test_finished = True
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None

        if hasattr(self, "input_text_widget"):
            self.input_text_widget.configure(state=tk.DISABLED)

        total_time_used = self.time_limit - max(0, self.time_remaining)
        if total_time_used <= 0:
            total_time_used = self.time_limit

        final_wpm = calculate_wpm(self.current_total_typed, total_time_used)
        final_accuracy = calculate_accuracy(self.current_correct, self.current_total_typed)
        self.root.after(400, lambda: self.show_results(final_wpm, final_accuracy, total_time_used))

    def show_results(self, final_wpm: int, final_accuracy: float, time_used: int):
        self.clear_container()
        headline, feedback, rating_color = get_performance_rating(final_wpm, final_accuracy)

        card = tk.Frame(self.container, bg="#ffffff", bd=1, relief=tk.SOLID, padx=35, pady=25)
        card.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=740, height=580)

        tk.Label(card, text="TEST COMPLETED", font=("Helvetica", 22, "bold"), fg="#1e293b", bg="#ffffff").pack(pady=(5, 2))
        tk.Label(card, text=f"★  {headline}  ★", font=("Helvetica", 14, "bold"), fg=rating_color, bg="#ffffff").pack(pady=(2, 6))
        tk.Label(card, text=feedback, font=("Helvetica", 10), fg="#475569", bg="#ffffff").pack(pady=(0, 15))

        score_box = tk.Frame(card, bg="#f8fafc", bd=1, relief=tk.GROOVE, padx=20, pady=12)
        score_box.pack(fill=tk.X, padx=25, pady=5)

        wpm_col = tk.Frame(score_box, bg="#f8fafc")
        wpm_col.pack(side=tk.LEFT, expand=True)
        tk.Label(wpm_col, text="SPEED", font=("Helvetica", 10, "bold"), fg="#64748b", bg="#f8fafc").pack()
        tk.Label(wpm_col, text=f"{final_wpm}", font=("Helvetica", 32, "bold"), fg="#2563eb", bg="#f8fafc").pack()
        tk.Label(wpm_col, text="Words Per Minute", font=("Helvetica", 9), fg="#94a3b8", bg="#f8fafc").pack()

        acc_col = tk.Frame(score_box, bg="#f8fafc")
        acc_col.pack(side=tk.RIGHT, expand=True)
        tk.Label(acc_col, text="ACCURACY", font=("Helvetica", 10, "bold"), fg="#64748b", bg="#f8fafc").pack()
        tk.Label(acc_col, text=f"{final_accuracy}%", font=("Helvetica", 32, "bold"), fg="#16a34a", bg="#f8fafc").pack()
        tk.Label(acc_col, text="Correct keystrokes", font=("Helvetica", 9), fg="#94a3b8", bg="#f8fafc").pack()

        breakdown_frame = tk.Frame(card, bg="#ffffff")
        breakdown_frame.pack(fill=tk.X, padx=40, pady=15)

        def add_stat_row(parent, row_idx, label_text, value_text, val_color="#1e293b"):
            lbl = tk.Label(parent, text=label_text, font=("Helvetica", 11), fg="#475569", bg="#ffffff")
            lbl.grid(row=row_idx, column=0, sticky="w", pady=3)
            val = tk.Label(parent, text=value_text, font=("Helvetica", 11, "bold"), fg=val_color, bg="#ffffff")
            val.grid(row=row_idx, column=1, sticky="e", pady=3)
            parent.grid_columnconfigure(0, weight=1)
            parent.grid_columnconfigure(1, weight=1)

        add_stat_row(breakdown_frame, 0, "Correct Characters:", f"{self.current_correct}", "#16a34a")
        add_stat_row(breakdown_frame, 1, "Incorrect Characters:", f"{self.current_incorrect}", "#dc2626")
        add_stat_row(breakdown_frame, 2, "Total Characters Typed:", f"{self.current_total_typed}", "#0f172a")
        add_stat_row(breakdown_frame, 3, "Duration Selected:", f"{self.time_limit} seconds", "#475569")
        add_stat_row(breakdown_frame, 4, "Difficulty Level:", f"{self.difficulty_var.get()}", "#2563eb")

        btn_box = tk.Frame(card, bg="#ffffff")
        btn_box.pack(pady=15)
        tk.Button(btn_box, text="Try Again", font=("Helvetica", 11, "bold"), bg="#2563eb", fg="#ffffff", padx=20, pady=8, bd=0, cursor="hand2", command=self.start_test).grid(row=0, column=0, padx=8)
        tk.Button(btn_box, text="Home", font=("Helvetica", 11), bg="#e2e8f0", fg="#1e293b", padx=18, pady=8, bd=0, cursor="hand2", command=self.back_to_home).grid(row=0, column=1, padx=8)
        tk.Button(btn_box, text="Exit", font=("Helvetica", 11), bg="#f1f5f9", fg="#dc2626", padx=18, pady=8, bd=0, cursor="hand2", command=self.exit_app).grid(row=0, column=2, padx=8)

    def reset_test(self):
        self.start_test()

    def back_to_home(self):
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None
        self.create_home_screen()

    def show_instructions(self):
        instructions_text = (
            "TYPING SPEED TESTER - INSTRUCTIONS\n\n"
            "1. Select Duration: Choose 30 or 60 Seconds.\n"
            "2. Select Difficulty: Easy, Medium, or Hard.\n"
            "3. Start Typing: Timer begins on first keystroke.\n"
            "4. Formula:\n"
            "   WPM = (Characters / 5) / Time (min)\n"
            "   Accuracy = (Correct / Total) * 100"
        )
        messagebox.showinfo("Typing Speed Tester - Instructions", instructions_text)

    def exit_app(self):
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None
        self.root.destroy()


def main():
    root = tk.Tk()
    app = TypingSpeedTesterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
