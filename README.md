# 🐝 Bee Spoiler

A desktop app that solves the NYT Spelling Bee puzzle and helps maintain a curated word list.

## The story

This was my first "home grown" Python project. I wanted to practice what I was learning, so I built a script to find words for the [Spelling Bee](https://www.nytimes.com/puzzles/spelling-bee) game.

My first attempt involved regex. A few hours of frustration later, I went with **sets** instead — and it turns out `issubset()` is all you need. Sometimes the simplest tool is the right one.

The original version was a script running inside R Markdown (yes, really). It's now a full GUI app with a curated word list I've been pruning for years.

**Fun fact:** I tested this against an AI chatbot by giving it the puzzle letters. It struggled and missed words that the solver finds instantly. Turns out 20 lines of Python with a `for` loop beats a large language model at this particular task.

## Important caveat

The solver logic is solid, but the results are only as good as the word list. In practice this means:

- **It will miss some valid words** that NYT accepts but aren't in the list yet
- **It will suggest some words** that NYT doesn't accept

The word list is a perpetual work in progress. I've been pruning it for years and it gets better every day, but it'll never be perfect since NYT's accepted word list is a closely guarded secret.

## Features

- **Solve any puzzle** — enter the center letter and 6 outer letters, get all valid words instantly
- **Pangram detection** — pangrams are highlighted at the top with a ⭐
- **Stats panel** — word counts by first letter and by length, similar to the NYT hints grid
- **Word list management** — add or remove words right from the app, changes save automatically
- **Curated word list** — years of pruning to match what NYT actually accepts

## How to run

No extra installs needed — just Python 3 and tkinter (included with Python).

```
python bee_spoiler.py
```

Place your `wordlist.txt` in the same folder as the script.

## The word list

I started with a public English word list and have been refining it for years — removing words NYT rejects and adding ones it accepts.

Contributions welcome! If you find words that should be added or removed, open a pull request.

## How it works

The solver uses Python sets to check each word against the puzzle rules:

- Must be at least 4 letters
- Must contain the center letter
- Can only use the 7 provided letters (repeats allowed)
- If a word uses all 7 letters, it's a pangram

That's it. No regex, no AI, no magic. Just `issubset()`.

DISCLAIMER:

GUI developed with assistance from Claude (Anthropic). 
Solver logic and curated word list are original work.
