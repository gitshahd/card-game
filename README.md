# card-game
This repository is to showcase the card flipping game for the advanced topics course

A polished, feature-complete card-matching memory game built entirely in Python using Pygame.
The player flips face-down cards two at a time, trying to find matching pairs before the countdown timer runs out.
The board size and time limit are fully configurable before each game session.

---


## Prerequisites

- **Python 3.8 or higher** — download from https://www.python.org/downloads/
- **pip** — included with any standard Python installation

---

## Installation

Clone or download the repository, then install the single dependency:

```bash
pip install pygame
```

No build step is required. The game runs directly from source.

---

## Running the Game

```bash
python game.py
```

That is the only command needed. The game window will open immediately.

---

## How to Play

**Step 1 — Configure the board**

On the main menu you will see three input fields:

- **Rows** (2 to 8) — the number of card rows on the board
- **Cols** (2 to 8) — the number of card columns on the board
- **Time** (10 to 300 seconds) — how long you have to find all pairs

The total number of cards (rows x cols) must be even so that every card has a matching partner.
If you enter a combination that results in an odd total, the game automatically corrects it by incrementing the column count by one.

**Step 2 — Start the game**

Click the START GAME button. The board will be generated with randomised card positions and the timer will begin immediately.

**Step 3 — Flip cards**

Click any face-down card to reveal its icon. Then click a second face-down card to attempt a match.

- If the two icons match, both cards stay face-up and a particle burst plays as confirmation. Your matched pair count increases by one.
- If the two icons do not match, both cards flip back face-down after a brief pause so you can see what they were.

**Step 4 — Win or lose**

- Match every pair before the timer reaches zero and you win.
- If the timer hits zero with unmatched cards remaining, a Game Over screen is shown.
- Press any key or click anywhere on the win or lose screen to return to the main menu and start a new game.
- Press ESC at any point during gameplay to go back to the menu immediately.

---

## Features

- **18 distinct geometric icons** drawn procedurally with pure math — circles, diamonds, triangles, stars, hearts, moons, lightning bolts, spirals, flowers, and more. No image files required.
- **Smooth card-flip animation** using a cosine-based horizontal squash effect that gives the impression of a physical card turning over.
- **Particle burst celebrations** that fire from each card on a successful match.
- **Colour-coded countdown timer** that transitions from green to yellow to red as time runs low, giving the player a clear urgency signal.
- **Move counter** displayed in the HUD so players can track and improve their efficiency across sessions.
- **Dynamic card layout** that automatically calculates card size based on the chosen board dimensions, ensuring the board always fills the window cleanly regardless of configuration.
- **Odd-size correction** so that entering an odd row x col combination never breaks the game.

---

## Project Structure

```
memory_scramble/
├── game.py        Main source file — all game logic, rendering, animation, and UI
└── README.md      This document
```

The entire implementation lives in a single file for simplicity and portability.
It is structured around five classes and one standalone drawing function:

| Component           | Role                                                                    |
|---------------------|-------------------------------------------------------------------------|
| MemoryScramble      | Top-level game controller and state machine (menu, playing, win, lose)  |
| Card                | Flip animation state, matched/wrong flash state, and self-rendering     |
| Button              | Hover-aware clickable button widget                                     |
| InputField          | Validated integer input field with min/max clamping                     |
| Particle            | Short-lived celebration particle with physics                           |
| draw_shape()        | Renders one of 18 unique icons to any surface at any position           |

---