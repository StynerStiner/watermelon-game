# 🍉 Sol's Watermelon Game

Throw watermelons at the people walking by! Hit them for points before the 60-second timer runs out.

## ▶️ Play online

**[Play it here!](https://stynerdev225.github.io/watermelon-game/)** — works in any browser, desktop or phone.

## 🎮 How to play

- People (🧍) walk across the screen from both sides.
- **Click / tap anywhere** to throw a watermelon 🍉 from the basket at the bottom toward where you clicked.
- Hit a person → **SPLAT! 💥** +10 points.
- You have **60 seconds** — score as high as you can, then click to play again.

## 🖥️ Two versions in this repo

| File | What it is | How to run |
|------|------------|------------|
| `index.html` | Web version (HTML5 canvas) | Open in any browser, or serve locally |
| `watermelon_game.py` | Desktop version (Python + tkinter) | `python3 watermelon_game.py` |

### Run the web version locally

```bash
python3 -m http.server 8000
# then open http://localhost:8000
```

### Run the desktop version

```bash
python3 watermelon_game.py
```

> Note: the desktop version needs Python with **tkinter**. On macOS the built-in `/usr/bin/python3` includes it.

---

Made with 🍉 by Sol.
