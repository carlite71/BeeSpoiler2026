"""
Bee Spoiler — NYT Spelling Bee Solver
======================================
A desktop app that solves the NYT Spelling Bee puzzle
and helps maintain a curated word list.

SETUP:
    No extra installs needed — uses tkinter (built into Python).

HOW TO RUN:
    python bee_spoiler.py

WORD LIST:
    Place your 'wordlist.txt' file in the same folder as this script.
    The app will load it automatically. If not found, it creates an empty one.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
import string


# =========================================================================
# SOLVER LOGIC
# =========================================================================

def solve_bee(word_list, center_letter, outer_letters):
    """
    Find all valid Spelling Bee words.
    Rules:
        - Words must be at least 4 letters long
        - Must contain the center letter
        - Can only use the 7 provided letters (repeats allowed)
    Returns (words, pangrams) — both sorted.
    """
    center = center_letter.lower()
    all_letters = set(outer_letters.lower()) | {center}

    words = []
    pangrams = []

    for word in word_list:
        w = word.lower().strip()
        if len(w) < 4:
            continue
        word_letters = set(w)

        if center not in word_letters:
            continue
        if not word_letters.issubset(all_letters):
            continue

        if word_letters == all_letters:
            pangrams.append(w)
        else:
            words.append(w)

    return sorted(words), sorted(pangrams)


def get_word_stats(words, pangrams):
    """Build statistics: words by starting letter and by length."""
    all_words = sorted(words + pangrams)

    by_letter = {}
    by_length = {}

    for w in all_words:
        # Count by starting letter
        first = w[0].upper()
        by_letter[first] = by_letter.get(first, 0) + 1

        # Count by word length
        length = len(w)
        by_length[length] = by_length.get(length, 0) + 1

    return by_letter, by_length


# =========================================================================
# WORD LIST MANAGEMENT
# =========================================================================

class WordList:
    def __init__(self, filepath="wordlist.txt"):
        self.filepath = Path(filepath)
        self.words = set()
        self.load()

    def load(self):
        if self.filepath.exists():
            with open(self.filepath, "r") as f:
                self.words = {line.strip().lower() for line in f if line.strip()}
            print(f"Loaded {len(self.words)} words from {self.filepath}")
        else:
            print(f"Word list not found at {self.filepath} — starting empty.")
            self.words = set()

    def save(self):
        with open(self.filepath, "w") as f:
            for word in sorted(self.words):
                f.write(word + "\n")
        print(f"Saved {len(self.words)} words to {self.filepath}")

    def add_word(self, word):
        w = word.lower().strip()
        if w and w not in self.words:
            self.words.add(w)
            return True
        return False

    def remove_word(self, word):
        w = word.lower().strip()
        if w in self.words:
            self.words.discard(w)
            return True
        return False


# =========================================================================
# GUI
# =========================================================================

class BeeSpoilerApp:
    # Colors — cool lavender theme
    BG = "#1a1a2e"
    BG_LIGHT = "#16213e"
    CARD_BG = "#0f3460"
    ACCENT = "#a78bfa"        # lavender
    ACCENT_LIGHT = "#c4b5fd"
    TEXT = "#eaeaea"
    TEXT_DIM = "#8899aa"
    PANGRAM_BG = "#a78bfa"
    PANGRAM_FG = "#1a1a2e"
    REMOVE_BG = "#c0392b"
    ADD_BG = "#27ae60"
    CENTER_BG = "#a78bfa"
    PETAL_BG = "#16213e"

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🐝 Bee Spoiler")
        self.root.configure(bg=self.BG)
        self.root.geometry("820x700")
        self.root.minsize(750, 600)

        # Find word list — check same folder as script first
        script_dir = Path(__file__).parent
        wordlist_path = script_dir / "wordlist.txt"
        if not wordlist_path.exists():
            # Also check for common variations
            for name in ["wordlist6.txt", "wordlist.txt", "words.txt"]:
                alt = script_dir / name
                if alt.exists():
                    wordlist_path = alt
                    break

        self.word_list = WordList(wordlist_path)
        self.current_results = []
        self.current_pangrams = []

        self._build_styles()
        self._build_ui()

    def _build_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Gold.TButton",
                        background=self.ACCENT,
                        foreground=self.BG,
                        font=("Segoe UI", 11, "bold"),
                        padding=(16, 8))
        style.map("Gold.TButton",
                  background=[("active", self.ACCENT_LIGHT)])

        style.configure("Remove.TButton",
                        background=self.REMOVE_BG,
                        foreground="white",
                        font=("Segoe UI", 9),
                        padding=(8, 4))
        style.map("Remove.TButton",
                  background=[("active", "#e74c3c")])

        style.configure("Add.TButton",
                        background=self.ADD_BG,
                        foreground="white",
                        font=("Segoe UI", 9),
                        padding=(8, 4))
        style.map("Add.TButton",
                  background=[("active", "#2ecc71")])

    def _build_ui(self):
        # Main container
        main = tk.Frame(self.root, bg=self.BG, padx=20, pady=15)
        main.pack(fill="both", expand=True)

        # Title
        title_frame = tk.Frame(main, bg=self.BG)
        title_frame.pack(fill="x", pady=(0, 15))

        tk.Label(title_frame, text="🐝", font=("Segoe UI", 28),
                 bg=self.BG, fg=self.ACCENT).pack(side="left")
        tk.Label(title_frame, text=" Bee Spoiler",
                 font=("Georgia", 24, "bold"),
                 bg=self.BG, fg=self.TEXT).pack(side="left")
        tk.Label(title_frame, text=f"   {len(self.word_list.words):,} words loaded",
                 font=("Segoe UI", 10),
                 bg=self.BG, fg=self.TEXT_DIM).pack(side="left", padx=(10, 0))

        # Input section
        input_card = tk.Frame(main, bg=self.CARD_BG, padx=20, pady=15,
                              highlightbackground=self.ACCENT,
                              highlightthickness=1)
        input_card.pack(fill="x", pady=(0, 15))

        # Center letter
        row1 = tk.Frame(input_card, bg=self.CARD_BG)
        row1.pack(fill="x", pady=(0, 8))

        tk.Label(row1, text="Center letter:",
                 font=("Segoe UI", 11),
                 bg=self.CARD_BG, fg=self.TEXT).pack(side="left")

        self.center_entry = tk.Entry(row1, width=3,
                                     font=("Consolas", 18, "bold"),
                                     bg=self.CENTER_BG, fg=self.BG,
                                     justify="center",
                                     insertbackground=self.BG)
        self.center_entry.pack(side="left", padx=(10, 0))

        # Outer letters
        tk.Label(row1, text="Outer letters:",
                 font=("Segoe UI", 11),
                 bg=self.CARD_BG, fg=self.TEXT).pack(side="left", padx=(25, 0))

        self.outer_entry = tk.Entry(row1, width=10,
                                    font=("Consolas", 18),
                                    bg=self.PETAL_BG, fg=self.ACCENT_LIGHT,
                                    justify="center",
                                    insertbackground=self.TEXT)
        self.outer_entry.pack(side="left", padx=(10, 0))

        # Solve button
        solve_btn = ttk.Button(row1, text="🔍  Solve!",
                               style="Gold.TButton",
                               command=self.solve)
        solve_btn.pack(side="right")

        # Bind Enter key
        self.root.bind("<Return>", lambda e: self.solve())

        # Results section — split into left (words) and right (stats)
        results_frame = tk.Frame(main, bg=self.BG)
        results_frame.pack(fill="both", expand=True)

        # Left panel — word list
        left = tk.Frame(results_frame, bg=self.BG)
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self.results_label = tk.Label(left, text="Enter letters and click Solve",
                                      font=("Segoe UI", 11),
                                      bg=self.BG, fg=self.TEXT_DIM,
                                      anchor="w")
        self.results_label.pack(fill="x", pady=(0, 5))

        # Word list with scrollbar
        list_frame = tk.Frame(left, bg=self.CARD_BG)
        list_frame.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        self.word_listbox = tk.Listbox(list_frame,
                                        font=("Consolas", 12),
                                        bg=self.BG_LIGHT,
                                        fg=self.TEXT,
                                        selectbackground=self.ACCENT,
                                        selectforeground=self.BG,
                                        activestyle="none",
                                        borderwidth=0,
                                        highlightthickness=0,
                                        yscrollcommand=scrollbar.set)
        self.word_listbox.pack(fill="both", expand=True)
        scrollbar.config(command=self.word_listbox.yview)

        # Word management buttons
        btn_frame = tk.Frame(left, bg=self.BG)
        btn_frame.pack(fill="x", pady=(8, 0))

        ttk.Button(btn_frame, text="❌ Remove selected from word list",
                   style="Remove.TButton",
                   command=self.remove_selected).pack(side="left")

        # Add word section
        self.add_entry = tk.Entry(btn_frame, width=15,
                                  font=("Consolas", 11),
                                  bg=self.BG_LIGHT, fg=self.TEXT,
                                  insertbackground=self.TEXT)
        self.add_entry.pack(side="right", padx=(5, 0))
        self.add_entry.bind("<Return>", lambda e: self.add_word())

        ttk.Button(btn_frame, text="➕ Add word:",
                   style="Add.TButton",
                   command=self.add_word).pack(side="right")

        # Right panel — stats
        right = tk.Frame(results_frame, bg=self.CARD_BG, padx=15, pady=10,
                         width=220,
                         highlightbackground=self.ACCENT,
                         highlightthickness=1)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        tk.Label(right, text="📊 Stats",
                 font=("Georgia", 14, "bold"),
                 bg=self.CARD_BG, fg=self.ACCENT).pack(anchor="w", pady=(0, 10))

        self.stats_text = tk.Text(right,
                                  font=("Consolas", 10),
                                  bg=self.CARD_BG, fg=self.TEXT,
                                  borderwidth=0,
                                  highlightthickness=0,
                                  wrap="word")
        self.stats_text.pack(fill="both", expand=True)
        self.stats_text.config(state="disabled")

        # Status bar
        self.status = tk.Label(main, text="Ready",
                               font=("Segoe UI", 9),
                               bg=self.BG, fg=self.TEXT_DIM,
                               anchor="w")
        self.status.pack(fill="x", pady=(8, 0))

    def solve(self):
        center = self.center_entry.get().strip().lower()
        outer = self.outer_entry.get().strip().lower()

        # Validate
        if not center or len(center) != 1 or center not in string.ascii_lowercase:
            messagebox.showwarning("Oops", "Enter a single letter as the center letter.")
            return

        if not outer or len(outer) != 6:
            messagebox.showwarning("Oops", "Enter exactly 6 outer letters.")
            return

        for ch in outer:
            if ch not in string.ascii_lowercase:
                messagebox.showwarning("Oops", f"'{ch}' is not a valid letter.")
                return

        if center in outer:
            messagebox.showwarning("Oops", "Center letter shouldn't be in the outer letters.")
            return

        # Solve
        words, pangrams = solve_bee(self.word_list.words, center, outer)
        self.current_results = words
        self.current_pangrams = pangrams

        # Display results
        self.word_listbox.delete(0, tk.END)

        # Pangrams first, highlighted
        for p in pangrams:
            self.word_listbox.insert(tk.END, f"⭐ {p.upper()}  (pangram)")

        # Then regular words
        for w in words:
            self.word_listbox.insert(tk.END, f"   {w}")

        # Color the pangrams
        for i in range(len(pangrams)):
            self.word_listbox.itemconfig(i, fg=self.PANGRAM_BG,
                                         selectforeground=self.PANGRAM_BG)

        total = len(words) + len(pangrams)
        self.results_label.config(
            text=f"Found {total} words  ({len(pangrams)} pangram{'s' if len(pangrams) != 1 else ''})",
            fg=self.ACCENT if total > 0 else self.TEXT_DIM
        )

        # Stats
        by_letter, by_length = get_word_stats(words, pangrams)
        self._show_stats(by_letter, by_length, total)

        self.status.config(text=f"Solved: {center.upper()} + {outer.upper()} → {total} words")

    def _show_stats(self, by_letter, by_length, total):
        self.stats_text.config(state="normal")
        self.stats_text.delete("1.0", tk.END)

        self.stats_text.insert(tk.END, f"Total: {total}\n\n")

        self.stats_text.insert(tk.END, "By first letter:\n")
        self.stats_text.insert(tk.END, "─" * 18 + "\n")
        for letter in sorted(by_letter):
            count = by_letter[letter]
            bar = "█" * count
            self.stats_text.insert(tk.END, f"  {letter}  {count:>2}  {bar}\n")

        self.stats_text.insert(tk.END, f"\nBy word length:\n")
        self.stats_text.insert(tk.END, "─" * 18 + "\n")
        for length in sorted(by_length):
            count = by_length[length]
            bar = "█" * count
            self.stats_text.insert(tk.END, f" {length:>2}  {count:>2}  {bar}\n")

        self.stats_text.config(state="disabled")

    def remove_selected(self):
        selection = self.word_listbox.curselection()
        if not selection:
            messagebox.showinfo("Select a word", "Click on a word in the list first.")
            return

        words_to_remove = []
        for idx in selection:
            text = self.word_listbox.get(idx).strip()
            # Clean up the display format
            text = text.replace("⭐", "").replace("(pangram)", "").strip().lower()
            words_to_remove.append(text)

        confirm = messagebox.askyesno(
            "Remove words",
            f"Remove {len(words_to_remove)} word(s) from your word list?\n\n"
            + ", ".join(words_to_remove)
        )

        if confirm:
            for w in words_to_remove:
                self.word_list.remove_word(w)
            self.word_list.save()
            self.status.config(text=f"Removed: {', '.join(words_to_remove)} — list saved ({len(self.word_list.words):,} words)")
            # Re-solve to refresh
            self.solve()

    def add_word(self):
        word = self.add_entry.get().strip().lower()
        if not word:
            return

        if not all(c in string.ascii_lowercase for c in word):
            messagebox.showwarning("Invalid", "Words can only contain letters.")
            return

        if self.word_list.add_word(word):
            self.word_list.save()
            self.add_entry.delete(0, tk.END)
            self.status.config(text=f"Added '{word}' — list saved ({len(self.word_list.words):,} words)")
            # Re-solve if we have letters entered
            if self.center_entry.get() and self.outer_entry.get():
                self.solve()
        else:
            self.status.config(text=f"'{word}' is already in the word list")

    def run(self):
        self.root.mainloop()


# =========================================================================
# MAIN
# =========================================================================

if __name__ == "__main__":
    app = BeeSpoilerApp()
    app.run()
