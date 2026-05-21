"""
Word List Cleaner
=================
One-time cleanup script for the Bee Spoiler word list.
Removes words that can never be valid Spelling Bee answers:
  - Less than 4 letters
  - More than 7 unique letters
  - Contains non-letter characters (hyphens, apostrophes, etc.)

HOW TO RUN:
    python clean_wordlist.py
"""

from pathlib import Path

# Find the word list — adjust this path if needed
script_dir = Path(__file__).parent
wordlist_path = script_dir / "wordlist.txt"

if not wordlist_path.exists():
    print(f"Word list not found at {wordlist_path}")
    print("Make sure wordlist.txt is in the same folder as this script.")
    input("Press Enter to exit...")
    exit()

# Read the word list
with open(wordlist_path, "r") as f:
    word_list = [line.strip().lower() for line in f if line.strip()]

print(f"Loaded {len(word_list)} words")

# Filter
clean_list = []
for word in word_list:
    wordset = set(word)

    if word.isalpha() and len(word) > 3 and len(wordset) < 8:
        clean_list.append(word)

removed = len(word_list) - len(clean_list)
print(f"Removed {removed} words")
print(f"Clean list: {len(clean_list)} words")

# Save
with open(wordlist_path, "w") as f:
    for word in sorted(clean_list):
        f.write(word + "\n")

print(f"Saved to {wordlist_path}")
