#!/usr/bin/env python3
"""
🍉 WATERMELON GAME 🍉
Throw watermelons at the people walking by!

HOW TO PLAY:
  - People (🧍) walk across the screen.
  - Click anywhere to throw a watermelon from the launcher at the bottom.
  - Hit a person for points. SPLAT! 💥
  - You have 60 seconds. Get the highest score you can!

RUN IT:
  /usr/bin/python3 watermelon_game.py
"""

import random
import tkinter as tk

WIDTH = 800
HEIGHT = 600
GAME_SECONDS = 60
FPS = 60
FRAME_MS = int(1000 / FPS)


class WatermelonGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🍉 Watermelon Game 🍉")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#87CEEB",
                                highlightthickness=0)
        self.canvas.pack()

        # Ground
        self.canvas.create_rectangle(0, HEIGHT - 60, WIDTH, HEIGHT,
                                     fill="#6ab150", outline="")

        # Launcher at the bottom center
        self.launcher_x = WIDTH // 2
        self.launcher_y = HEIGHT - 60
        self.canvas.create_text(self.launcher_x, self.launcher_y - 10,
                                text="🧺", font=("Arial", 34))

        self.people = []       # list of dicts: {id, x, y, vx, size}
        self.melons = []       # list of dicts: {id, x, y, vx, vy}
        self.splats = []       # list of dicts: {id, life}

        self.score = 0
        self.thrown = 0
        self.hits = 0
        self.time_left = GAME_SECONDS
        self.running = True

        # HUD
        self.score_text = self.canvas.create_text(
            16, 16, anchor="nw", font=("Helvetica", 20, "bold"),
            fill="#1a1a1a", text="Score: 0")
        self.time_text = self.canvas.create_text(
            WIDTH - 16, 16, anchor="ne", font=("Helvetica", 20, "bold"),
            fill="#1a1a1a", text=f"Time: {GAME_SECONDS}")
        self.hint_text = self.canvas.create_text(
            WIDTH // 2, HEIGHT - 20, font=("Helvetica", 13),
            fill="#0d3b0d", text="Click anywhere to throw a watermelon!")

        self.canvas.bind("<Button-1>", self.throw_melon)

        self.spawn_person()
        self.tick_clock()
        self.game_loop()

    # ---------- People ----------
    def spawn_person(self):
        if not self.running:
            return
        from_left = random.random() < 0.5
        y = random.randint(120, HEIGHT - 120)
        size = random.randint(30, 46)
        speed = random.uniform(1.2, 3.2)
        if from_left:
            x = -30
            vx = speed
        else:
            x = WIDTH + 30
            vx = -speed
        pid = self.canvas.create_text(x, y, text="🧍", font=("Arial", size))
        self.people.append({"id": pid, "x": x, "y": y, "vx": vx, "size": size})

        # schedule the next spawn
        delay = random.randint(500, 1400)
        self.root.after(delay, self.spawn_person)

    # ---------- Throwing ----------
    def throw_melon(self, event):
        if not self.running:
            return
        sx, sy = self.launcher_x, self.launcher_y - 20
        dx = event.x - sx
        dy = event.y - sy
        dist = max((dx * dx + dy * dy) ** 0.5, 1)
        speed = 14.0
        vx = speed * dx / dist
        vy = speed * dy / dist
        mid = self.canvas.create_text(sx, sy, text="🍉", font=("Arial", 26))
        self.melons.append({"id": mid, "x": sx, "y": sy, "vx": vx, "vy": vy})
        self.thrown += 1

    # ---------- Effects ----------
    def make_splat(self, x, y):
        sid = self.canvas.create_text(x, y, text="💥", font=("Arial", 40))
        self.splats.append({"id": sid, "life": 18})

    # ---------- Main loop ----------
    def game_loop(self):
        if not self.running:
            return

        # Move people
        for p in self.people[:]:
            p["x"] += p["vx"]
            self.canvas.coords(p["id"], p["x"], p["y"])
            if p["x"] < -60 or p["x"] > WIDTH + 60:
                self.canvas.delete(p["id"])
                self.people.remove(p)

        # Move melons + collision
        for m in self.melons[:]:
            m["x"] += m["vx"]
            m["y"] += m["vy"]
            self.canvas.coords(m["id"], m["x"], m["y"])

            hit = False
            for p in self.people[:]:
                r = p["size"] * 0.7
                if abs(m["x"] - p["x"]) < r and abs(m["y"] - p["y"]) < r:
                    self.make_splat(p["x"], p["y"])
                    self.canvas.delete(p["id"])
                    self.people.remove(p)
                    self.score += 10
                    self.hits += 1
                    hit = True
                    break

            off = (m["x"] < -40 or m["x"] > WIDTH + 40 or
                   m["y"] < -40 or m["y"] > HEIGHT + 40)
            if hit or off:
                self.canvas.delete(m["id"])
                self.melons.remove(m)

        # Fade splats
        for s in self.splats[:]:
            s["life"] -= 1
            if s["life"] <= 0:
                self.canvas.delete(s["id"])
                self.splats.remove(s)

        self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")
        self.root.after(FRAME_MS, self.game_loop)

    def tick_clock(self):
        if not self.running:
            return
        self.time_left -= 1
        self.canvas.itemconfig(self.time_text, text=f"Time: {self.time_left}")
        if self.time_left <= 0:
            self.end_game()
        else:
            self.root.after(1000, self.tick_clock)

    def end_game(self):
        self.running = False
        for p in self.people:
            self.canvas.delete(p["id"])
        for m in self.melons:
            self.canvas.delete(m["id"])
        self.people.clear()
        self.melons.clear()

        accuracy = (self.hits / self.thrown * 100) if self.thrown else 0
        self.canvas.create_rectangle(150, 180, WIDTH - 150, HEIGHT - 180,
                                     fill="#ffffff", outline="#6ab150", width=4)
        self.canvas.create_text(WIDTH // 2, 240, text="⏰ TIME'S UP! ⏰",
                                font=("Helvetica", 28, "bold"), fill="#1a1a1a")
        self.canvas.create_text(WIDTH // 2, 300,
                                text=f"Final Score: {self.score}",
                                font=("Helvetica", 24), fill="#c0392b")
        self.canvas.create_text(WIDTH // 2, 340,
                                text=f"Hits: {self.hits}   Thrown: {self.thrown}"
                                     f"   Accuracy: {accuracy:.0f}%",
                                font=("Helvetica", 16), fill="#333333")

        btn = tk.Button(self.root, text="Play Again", font=("Helvetica", 16, "bold"),
                        bg="#6ab150", fg="black", command=self.restart)
        self.btn_window = self.canvas.create_window(WIDTH // 2, 400, window=btn)

    def restart(self):
        self.canvas.delete("all")
        self.__init__(self.root)


def main():
    root = tk.Tk()
    WatermelonGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
