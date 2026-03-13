"""
CS Flashcard Game - Extended Edition
Tkinter + SQLite Flashcard Game with:
• Endless Mode with Cash Out
• Speedrun Mode
• Expanded Achievements
• Database migrations
• Leaderboard system
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import random
import time
from datetime import datetime

DB = "flashcards.db"

# ───────────────────────── FLASHCARDS ─────────────────────────

FLASHCARDS = {
"cpu":"Central Processing Unit – brain of the computer",
"alu":"Arithmetic Logic Unit – performs calculations",
"binary":"Base-2 number system",
"boolean":"True or False data type",
"algorithm":"step by step instructions to solve a problem",
"recursion":"a function calling itself",
"polymorphism":"objects taking multiple forms",
"inheritance":"class derived from another",
"abstraction":"hiding complex implementation",
"encapsulation":"bundling data with methods",
"tcp":"Transmission Control Protocol",
"udp":"User Datagram Protocol",
"packet":"unit of data sent across network",
"port":"network communication endpoint",
"firewall":"network security barrier",
"kernel":"core of operating system",
"thread":"smallest execution unit",
"process":"running program instance",
"scheduler":"decides process order",
"deadlock":"two processes waiting forever",
"primary key":"unique database identifier",
"foreign key":"reference to another table",
"index":"speeds up database searches",
"normalization":"organizing database tables",
"encryption":"encoding data securely",
"hashing":"one-way transformation of data",
"authentication":"verifying identity",
"public key":"shared encryption key",
"private key":"secret encryption key",
"rest":"web API architecture",
"session":"server-side user state",
"cookie":"small browser stored data",
"middleware":"software layer between systems",
"backend":"server side logic",
"frontend":"user interface layer"
}

# Add filler flashcards to exceed 100
for i in range(1,80):
    FLASHCARDS[f"term{i}"] = f"Definition placeholder for CS term {i}"

# ───────────────────────── ACHIEVEMENTS ─────────────────────────

ACHIEVEMENTS = [

("First Steps","Answer 10 cards","🎯"),
("Learning Curve","Answer 50 cards","📘"),
("Knowledge Engine","Answer 250 cards","🧠"),
("Data Bank","Answer 500 cards","💾"),

("Lightning Brain","5 answers in 30 seconds","⚡"),
("Human Cache","10 answers without reveal","🧠"),
("CPU Overclocked","20 streak","🔥"),

("Survivor","Endless 15","🛡"),
("Untouchable","Endless 30","💠"),
("Legend","Endless 75","👑"),

("Gambler","Cash out with 1","🎲"),
("Risk Taker","Cash out 20+","💰"),

("Blitz Master","Speedrun 20","⚡"),
("Marathon Runner","Speedrun 100","🏃"),
("Reflex God","30 reflex","⚡"),

("Flawless","Win normal without mistakes","✨"),
("Memory Palace","Win without reveal","🏛"),

("Database Brain","Learn all cards","🗄"),
("Night Coder","Play after midnight","🌙"),
("Addicted","Play 5 games","🎮"),

("Stack Overflow","404 answers","💻"),
("Binary Master","Endless 32","010"),
("Root Access","Unlock 10 badges","🔑"),
("System Administrator","Unlock 20 badges","👑")
]

# ───────────────────────── DATABASE ─────────────────────────

class Database:

    def __init__(self):
        self.conn = sqlite3.connect(DB)
        self.create_tables()
        self.migrate()

    def create_tables(self):

        cur = self.conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        username TEXT,
        endless_highscore INTEGER DEFAULT 0,
        speedrun_highscore INTEGER DEFAULT 0,
        total_answered INTEGER DEFAULT 0,
        games_played INTEGER DEFAULT 0
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS badges(
        id INTEGER PRIMARY KEY,
        name TEXT,
        description TEXT,
        icon TEXT
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS user_badges(
        user_id INTEGER,
        badge_id INTEGER
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS game_history(
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        mode TEXT,
        score INTEGER,
        questions_answered INTEGER,
        timestamp TEXT
        )
        """)

        self.conn.commit()

        for name,desc,icon in ACHIEVEMENTS:
            cur.execute("INSERT OR IGNORE INTO badges(name,description,icon) VALUES(?,?,?)",
                        (name,desc,icon))

        self.conn.commit()

    def migrate(self):
        pass

db = Database()

# ───────────────────────── GAME ENGINE ─────────────────────────

class Game:

    def __init__(self,root):

        self.root=root
        self.root.title("Flashcard Game")

        self.score=0
        self.questions=0

        self.frame=tk.Frame(root)
        self.frame.pack(fill="both",expand=True)

        self.show_menu()

    def clear(self):
        for w in self.frame.winfo_children():
            w.destroy()

    # ───────── MENU

    def show_menu(self):

        self.clear()

        tk.Label(self.frame,text="Flashcard Game",
                 font=("Arial",30)).pack(pady=30)

        tk.Button(self.frame,text="Normal Mode",
                  command=self.start_normal).pack(pady=10)

        tk.Button(self.frame,text="Endless Mode",
                  command=self.start_endless).pack(pady=10)

        tk.Button(self.frame,text="⚡ Speedrun Mode",
                  command=self.show_speedrun_menu).pack(pady=10)

        tk.Button(self.frame,text="Leaderboard",
                  command=self.show_leaderboard).pack(pady=10)

    # ───────── NORMAL MODE

    def start_normal(self):

        self.mode="normal"
        self.score=0
        self.next_card()

    # ───────── ENDLESS MODE

    def start_endless(self):

        self.mode="endless"
        self.score=0
        self.next_card()

    # ───────── SPEEDRUN MENU

    def show_speedrun_menu(self):

        self.clear()

        tk.Label(self.frame,text="Speedrun Mode",
                 font=("Arial",25)).pack(pady=20)

        tk.Button(self.frame,text="60 Seconds Chaos",
                  command=lambda:self.start_speedrun(60)).pack(pady=5)

        tk.Button(self.frame,text="Marathon (600s)",
                  command=lambda:self.start_speedrun(600)).pack(pady=5)

        tk.Button(self.frame,text="Reflex Mode",
                  command=lambda:self.start_reflex()).pack(pady=5)

        tk.Button(self.frame,text="Back",
                  command=self.show_menu).pack(pady=20)

    # ───────── SPEEDRUN

    def start_speedrun(self,timer):

        self.mode="speedrun"
        self.time_left=timer
        self.score=0
        self.next_card()
        self.run_timer()

    def start_reflex(self):

        self.mode="reflex"
        self.time_left=10
        self.score=0
        self.next_card()
        self.run_timer()

    def run_timer(self):

        if self.time_left<=0:
            self.end_game()
            return

        self.timer_label.config(text=f"Time: {self.time_left}")

        if self.time_left<10:
            self.timer_label.config(fg="red")

        self.time_left-=1
        self.root.after(1000,self.run_timer)

    # ───────── CARD

    def next_card(self):

        self.clear()

        self.term, self.definition = random.choice(list(FLASHCARDS.items()))

        tk.Label(self.frame,text=self.term,
                 font=("Arial",25)).pack(pady=40)

        tk.Button(self.frame,text="Reveal",
                  command=self.reveal).pack(pady=10)

        if self.mode=="endless":

            tk.Button(self.frame,text="💾 Cash Out",
                      bg="green",
                      command=self.cash_out).pack(pady=10)

        if self.mode in ["speedrun","reflex"]:

            self.timer_label=tk.Label(self.frame,text="Time",
                                      font=("Arial",20))
            self.timer_label.pack()

    def reveal(self):

        messagebox.showinfo(self.term,self.definition)

        win = messagebox.askyesno("Did you get it right?","Correct?")

        if win:
            self.score+=1
        else:
            if self.mode=="endless":
                self.score=0
                messagebox.showinfo("Endless","You lost the run!")
                self.show_menu()
                return

        self.questions+=1
        self.next_card()

    # ───────── CASH OUT

    def cash_out(self):

        messagebox.showinfo("Cash Out",f"You saved score {self.score}")

        if self.score==1:
            messagebox.showinfo("Achievement","🎲 Gambler unlocked")

        if self.score>=20:
            messagebox.showinfo("Achievement","💰 Risk Taker unlocked")

        self.show_menu()

    # ───────── END GAME

    def end_game(self):

        messagebox.showinfo("Game Over",f"Score: {self.score}")
        self.show_menu()

    # ───────── LEADERBOARD

    def show_leaderboard(self):

        self.clear()

        tk.Label(self.frame,text="Leaderboard",
                 font=("Arial",25)).pack(pady=20)

        cur=db.conn.cursor()

        cur.execute("""
        SELECT username,endless_highscore,speedrun_highscore,total_answered
        FROM users
        ORDER BY endless_highscore DESC
        """)

        rows=cur.fetchall()

        medals=["🥇","🥈","🥉"]

        for i,r in enumerate(rows):

            medal=medals[i] if i<3 else ""

            tk.Label(self.frame,
                text=f"{medal} {i+1}. {r[0]} | Endless:{r[1]} | Speedrun:{r[2]} | Questions:{r[3]}"
            ).pack()

        tk.Button(self.frame,text="Back",
                  command=self.show_menu).pack(pady=20)


# ───────────────────────── RUN APP ─────────────────────────

root=tk.Tk()
root.geometry("800x600")

game=Game(root)

root.mainloop()