"""
CS Flashcard Game - A gamified flashcard learning app
Built with Python 3, Tkinter, SQLite3
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import random
import math
import time

# ─────────────────────────── FLASHCARD DATA ──────────────────────────────────

FLASHCARDS = {
    "RAM": "Random Access Memory – temporary storage used by the CPU",
    "CPU": "Central Processing Unit – the primary processor of a computer",
    "HTTP": "HyperText Transfer Protocol – used for web communication",
    "IP": "Internet Protocol – identifies devices on a network",
    "DNS": "Domain Name System – translates domain names to IP addresses",
    "GUI": "Graphical User Interface – visual way to interact with software",
    "API": "Application Programming Interface – lets programs talk to each other",
    "SQL": "Structured Query Language – language for managing databases",
    "OS": "Operating System – manages hardware and software resources",
    "URL": "Uniform Resource Locator – address for internet resources",
    "HTML": "HyperText Markup Language – structure language for web pages",
    "CSS": "Cascading Style Sheets – styling language for web pages",
    "OOP": "Object-Oriented Programming – design paradigm using objects",
    "IDE": "Integrated Development Environment – software for coding",
    "LAN": "Local Area Network – network within a limited area",
    "WAN": "Wide Area Network – network spanning large geographical areas",
    "SSH": "Secure Shell – cryptographic network protocol for remote access",
    "VPN": "Virtual Private Network – encrypted private network over internet",
    "BIOS": "Basic Input/Output System – firmware initializing hardware at boot",
    "ROM": "Read-Only Memory – non-volatile permanent storage",
    "HTTPS": "HyperText Transfer Protocol Secure – encrypted HTTP",
    "JSON": "JavaScript Object Notation – lightweight data-interchange format",
    "XML": "eXtensible Markup Language – flexible data markup language",
    "SDK": "Software Development Kit – tools for building applications",
    "EOF": "End Of File – marker signaling the end of a data stream",
}

# ─────────────────────────── BADGE DEFINITIONS ───────────────────────────────

BADGE_DEFS = [
    ("First Time",    "Win Normal Mode once",                   "🏆"),
    ("Fast Learner",  "Win Normal Mode in under 15 questions",  "⚡"),
    ("Endless 10",    "Score 10+ in Endless Mode",              "🔥"),
    ("Endless 25",    "Score 25+ in Endless Mode",              "💎"),
    ("Endless 50",    "Score 50+ in Endless Mode",              "👑"),
    ("Flash Master",  "Answer 100 cards total",                 "🎓"),
]

# ─────────────────────────── COLOUR PALETTE ──────────────────────────────────

C = {
    "bg":        "#0f0f1a",
    "panel":     "#1a1a2e",
    "card":      "#16213e",
    "accent":    "#e94560",
    "accent2":   "#0f3460",
    "green":     "#00d26a",
    "yellow":    "#ffd700",
    "text":      "#eaeaea",
    "muted":     "#888899",
    "white":     "#ffffff",
    "purple":    "#7b2fff",
    "cyan":      "#00d4ff",
}

FONT_TITLE  = ("Segoe UI", 28, "bold")
FONT_LARGE  = ("Segoe UI", 18, "bold")
FONT_MED    = ("Segoe UI", 14)
FONT_SMALL  = ("Segoe UI", 11)
FONT_MONO   = ("Consolas", 13)

# ══════════════════════════ DATABASE MANAGER ═════════════════════════════════

class DatabaseManager:
    """Handles all SQLite operations."""

    def __init__(self, db_path="flashcard_game.db"):
        self.conn = sqlite3.connect(db_path)
        self._create_tables()
        self._seed_badges()

    # ── Schema ──────────────────────────────────────────────────────────────

    def _create_tables(self):
        cur = self.conn.cursor()
        cur.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id                INTEGER PRIMARY KEY AUTOINCREMENT,
                username          TEXT    UNIQUE NOT NULL,
                code              TEXT    NOT NULL,
                endless_highscore INTEGER DEFAULT 0,
                total_answered    INTEGER DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS badges (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                badge_name  TEXT UNIQUE,
                description TEXT,
                icon        TEXT
            );

            CREATE TABLE IF NOT EXISTS user_badges (
                user_id  INTEGER,
                badge_id INTEGER,
                PRIMARY KEY (user_id, badge_id)
            );
        """)
        self.conn.commit()

    def _seed_badges(self):
        cur = self.conn.cursor()
        for name, desc, icon in BADGE_DEFS:
            cur.execute(
                "INSERT OR IGNORE INTO badges (badge_name, description, icon) VALUES (?,?,?)",
                (name, desc, icon)
            )
        self.conn.commit()

    # ── User helpers ─────────────────────────────────────────────────────────

    def user_exists(self, username):
        cur = self.conn.cursor()
        cur.execute("SELECT id FROM users WHERE username=?", (username,))
        return cur.fetchone() is not None

    def verify_code(self, username, code):
        cur = self.conn.cursor()
        cur.execute("SELECT id FROM users WHERE username=? AND code=?", (username, code))
        return cur.fetchone() is not None

    def create_user(self, username, code):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO users (username, code) VALUES (?,?)", (username, code))
        self.conn.commit()

    def get_user(self, username):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=?", (username,))
        row = cur.fetchone()
        if row:
            return {"id": row[0], "username": row[1], "code": row[2],
                    "endless_highscore": row[3], "total_answered": row[4]}
        return None

    def update_endless_highscore(self, user_id, score):
        self.conn.execute(
            "UPDATE users SET endless_highscore=? WHERE id=? AND endless_highscore<?",
            (score, user_id, score)
        )
        self.conn.commit()

    def increment_total_answered(self, user_id, count):
        self.conn.execute(
            "UPDATE users SET total_answered = total_answered + ? WHERE id=?",
            (count, user_id)
        )
        self.conn.commit()

    # ── Badge helpers ────────────────────────────────────────────────────────

    def award_badge(self, user_id, badge_name):
        cur = self.conn.cursor()
        cur.execute("SELECT id FROM badges WHERE badge_name=?", (badge_name,))
        row = cur.fetchone()
        if not row:
            return False
        badge_id = row[0]
        cur.execute("SELECT 1 FROM user_badges WHERE user_id=? AND badge_id=?",
                    (user_id, badge_id))
        if cur.fetchone():
            return False  # already has it
        cur.execute("INSERT INTO user_badges (user_id, badge_id) VALUES (?,?)",
                    (user_id, badge_id))
        self.conn.commit()
        return True

    def get_user_badge_names(self, user_id):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT b.badge_name FROM badges b
            JOIN user_badges ub ON b.id = ub.badge_id
            WHERE ub.user_id=?
        """, (user_id,))
        return {row[0] for row in cur.fetchall()}

    def get_all_badges(self):
        cur = self.conn.cursor()
        cur.execute("SELECT badge_name, description, icon FROM badges")
        return cur.fetchall()

    # ── Leaderboard ──────────────────────────────────────────────────────────

    def get_leaderboard(self):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT u.username, u.endless_highscore,
                   COUNT(ub.badge_id) AS badge_count
            FROM users u
            LEFT JOIN user_badges ub ON u.id = ub.user_id
            GROUP BY u.id
            ORDER BY u.endless_highscore DESC
        """)
        return cur.fetchall()

    def close(self):
        self.conn.close()


# ══════════════════════════ ANIMATION HELPERS ════════════════════════════════

class FloatingText:
    """Creates a temporary floating label that rises and fades."""

    def __init__(self, canvas, x, y, text, color, font=("Segoe UI", 20, "bold")):
        self.canvas = canvas
        self.item = canvas.create_text(x, y, text=text, fill=color, font=font)
        self.y = y
        self.alpha = 1.0
        self._step()

    def _step(self):
        self.y -= 2
        self.alpha -= 0.04
        if self.alpha <= 0:
            self.canvas.delete(self.item)
            return
        # Simulate fade via colour blending toward background
        a = max(0, self.alpha)
        r = int(0x0f + (int(self.canvas.itemcget(self.item, "fill")[1:3], 16) - 0x0f) * a)
        self.canvas.coords(self.item, self.canvas.winfo_width() // 2, self.y)
        self.canvas.after(30, self._step)


class ConfettiCanvas:
    """Draws animated confetti particles on a canvas."""

    COLORS = ["#e94560", "#ffd700", "#00d4ff", "#00d26a", "#7b2fff", "#ff6b6b"]

    def __init__(self, canvas, width, height):
        self.canvas = canvas
        self.width  = width
        self.height = height
        self.particles = []
        self._spawn()

    def _spawn(self):
        for _ in range(80):
            x = random.randint(0, self.width)
            y = random.randint(-self.height, 0)
            size = random.randint(6, 14)
            color = random.choice(self.COLORS)
            speed = random.uniform(3, 8)
            drift = random.uniform(-2, 2)
            angle = random.uniform(0, 360)
            spin  = random.uniform(-5, 5)
            item  = self.canvas.create_rectangle(
                x, y, x + size, y + size, fill=color, outline=""
            )
            self.particles.append([x, y, size, speed, drift, angle, spin, item])
        self._animate()

    def _animate(self):
        for p in self.particles:
            p[1] += p[3]   # fall
            p[0] += p[4]   # drift
            p[5] += p[6]   # spin
            if p[1] > self.height:
                p[1] = random.randint(-60, -10)
                p[0] = random.randint(0, self.width)
            rad = math.radians(p[5])
            x1 = p[0] + p[2] * math.cos(rad)
            y1 = p[1] + p[2] * math.sin(rad)
            self.canvas.coords(p[7], p[0], p[1], x1, y1)
        self.canvas.after(30, self._animate)


# ══════════════════════════ MAIN APPLICATION ═════════════════════════════════

class FlashcardApp(tk.Tk):
    """Root window – acts as the screen manager."""

    def __init__(self):
        super().__init__()
        self.title("CS Flashcard Game")
        self.geometry("900x650")
        self.resizable(True, True)
        self.configure(bg=C["bg"])
        self.minsize(700, 520)

        self._fullscreen = False
        self.bind("<F11>",     lambda e: self.toggle_fullscreen())
        self.bind("<Escape>",  lambda e: self.exit_fullscreen())

        self.db   = DatabaseManager()
        self.user = None          # dict set after login
        self._current_frame = None

        self.show_login()

    def toggle_fullscreen(self):
        self._fullscreen = not self._fullscreen
        self.attributes("-fullscreen", self._fullscreen)

    def exit_fullscreen(self):
        if self._fullscreen:
            self._fullscreen = False
            self.attributes("-fullscreen", False)

    # ── Screen switching ─────────────────────────────────────────────────────

    def show_frame(self, FrameClass, **kwargs):
        if self._current_frame:
            self._current_frame.destroy()
        frame = FrameClass(self, **kwargs)
        frame.pack(fill="both", expand=True)
        self._current_frame = frame

    def show_login(self):
        self.show_frame(LoginScreen)

    def show_menu(self):
        self.show_frame(MainMenu)

    def show_normal_mode(self):
        self.show_frame(NormalModeScreen)

    def show_endless_mode(self):
        self.show_frame(EndlessModeScreen)

    def show_rewards(self):
        self.show_frame(RewardsScreen)

    def show_leaderboard(self):
        self.show_frame(LeaderboardScreen)

    def on_close(self):
        self.db.close()
        self.destroy()


# ══════════════════════════ SHARED WIDGET HELPERS ════════════════════════════

def make_button(parent, text, command, bg=C["accent"], fg=C["white"],
                font=FONT_MED, pad=(20, 10), width=None):
    """
    Label-based button — works on macOS, Windows, and Linux.
    tk.Button ignores bg/fg on macOS native theme; tk.Label always respects them.
    """
    lighter = _lighten(bg, 35)
    darker  = _lighten(bg, -20)
    kw = dict(text=text, bg=bg, fg=fg, font=font,
               cursor="hand2", padx=pad[0], pady=pad[1], relief="flat")
    if width:
        kw["width"] = width
    btn = tk.Label(parent, **kw)
    btn.bind("<Enter>",           lambda e: btn.config(bg=lighter))
    btn.bind("<Leave>",           lambda e: btn.config(bg=bg))
    btn.bind("<ButtonPress-1>",   lambda e: btn.config(bg=darker))
    btn.bind("<ButtonRelease-1>", lambda e: (btn.config(bg=lighter), command()))
    return btn


def _lighten(hex_color, amount):
    """Lighten (positive) or darken (negative) a hex colour."""
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    r = max(0, min(255, r + amount))
    g = max(0, min(255, g + amount))
    b = max(0, min(255, b + amount))
    return f"#{r:02x}{g:02x}{b:02x}"


def make_label(parent, text, font=FONT_MED, fg=C["text"], bg=C["bg"], **kw):
    return tk.Label(parent, text=text, font=font, fg=fg, bg=bg, **kw)


# ══════════════════════════ LOGIN SCREEN ════════════════════════════════════

class LoginScreen(tk.Frame):

    def __init__(self, master):
        super().__init__(master, bg=C["bg"])
        self._build()

    def _build(self):
        # Title
        make_label(self, "🖥  CS Flashcard Game", font=("Segoe UI", 26, "bold"),
                   fg=C["cyan"]).pack(pady=(60, 5))
        make_label(self, "Learn Computer Science — Level Up!", font=FONT_SMALL,
                   fg=C["muted"]).pack(pady=(0, 40))

        panel = tk.Frame(self, bg=C["panel"], padx=40, pady=30)
        panel.pack()

        make_label(panel, "Enter your username", bg=C["panel"],
                   fg=C["text"], font=FONT_MED).pack(anchor="w")

        self.username_var = tk.StringVar()
        entry = tk.Entry(panel, textvariable=self.username_var,
                         font=FONT_MED, bg=C["card"], fg=C["text"],
                         insertbackground=C["text"], relief="flat",
                         width=28)
        entry.pack(pady=(6, 20), ipady=8)
        entry.focus()
        entry.bind("<Return>", lambda e: self._proceed())

        make_button(panel, "Continue →", self._proceed,
                    bg=C["accent"], width=26).pack(pady=(0, 6))

        self.msg_var = tk.StringVar()
        tk.Label(panel, textvariable=self.msg_var, bg=C["panel"],
                 fg="#ff6b6b", font=FONT_SMALL).pack()

    def _proceed(self):
        username = self.username_var.get().strip()
        if not username:
            self.msg_var.set("Please enter a username.")
            return
        db = self.master.db
        if db.user_exists(username):
            # Ask for code
            CodeDialog(self.master, username, new_user=False)
        else:
            CodeDialog(self.master, username, new_user=True)


# ── Code dialog (used for login & registration) ──────────────────────────────

class CodeDialog(tk.Toplevel):

    def __init__(self, master, username, new_user):
        super().__init__(master)
        self.master   = master
        self.username = username
        self.new_user = new_user
        self.title("Set Code" if new_user else "Enter Code")
        self.geometry("380x260")
        self.resizable(False, False)
        self.configure(bg=C["panel"])
        self.grab_set()
        self._build()

    def _build(self):
        if self.new_user:
            msg = f"Welcome, {self.username}!\nSet a 4-digit code for your account:"
        else:
            msg = f"Welcome back, {self.username}!\nEnter your 4-digit code:"

        make_label(self, msg, bg=C["panel"], fg=C["text"],
                   font=FONT_MED, justify="center").pack(pady=(30, 14))

        self.code_var = tk.StringVar()
        e = tk.Entry(self, textvariable=self.code_var, show="●",
                     font=("Consolas", 22, "bold"), bg=C["card"],
                     fg=C["cyan"], insertbackground=C["cyan"],
                     relief="flat", width=8, justify="center")
        e.pack(ipady=8)
        e.focus()
        e.bind("<Return>", lambda ev: self._submit())

        make_button(self, "Confirm", self._submit,
                    bg=C["accent"], pad=(30, 8)).pack(pady=14)

        self.err = make_label(self, "", bg=C["panel"], fg="#ff6b6b",
                              font=FONT_SMALL)
        self.err.pack()

    def _submit(self):
        code = self.code_var.get().strip()
        if len(code) != 4 or not code.isdigit():
            self.err.config(text="Code must be exactly 4 digits.")
            return
        db = self.master.db
        if self.new_user:
            db.create_user(self.username, code)
        else:
            if not db.verify_code(self.username, code):
                self.err.config(text="Wrong code. Try again.")
                return
        self.master.user = db.get_user(self.username)
        self.destroy()
        self.master.show_menu()


# ══════════════════════════ MAIN MENU ═══════════════════════════════════════

class MainMenu(tk.Frame):

    def __init__(self, master):
        super().__init__(master, bg=C["bg"])
        self._build()

    def _build(self):
        user = self.master.user
        # Header
        make_label(self, f"Welcome, {user['username']}  👋",
                   font=FONT_TITLE, fg=C["cyan"]).pack(pady=(40, 4))
        make_label(self, f"Endless High Score: {user['endless_highscore']}",
                   font=FONT_SMALL, fg=C["yellow"]).pack(pady=(0, 30))

        btn_cfg = [
            ("▶  Play Normal Mode",  C["accent"],  self.master.show_normal_mode),
            ("♾  Endless Mode",      C["purple"],  self.master.show_endless_mode),
            ("🏅  Rewards / Badges", "#1a6b3c",    self.master.show_rewards),
            ("📊  Leaderboard",      C["accent2"], self.master.show_leaderboard),
            ("✕  Quit Game",         "#333344",    self._quit),
        ]
        for text, color, cmd in btn_cfg:
            make_button(self, text, cmd, bg=color,
                        font=FONT_LARGE, pad=(40, 14), width=28).pack(pady=7)

        # Fullscreen toggle button + F11 hint
        fs_row = tk.Frame(self, bg=C["bg"])
        fs_row.pack(pady=(10, 0))
        self._fs_btn = make_button(fs_row, self._fs_label(),
                                   self._toggle_fs, bg="#2a2a3e",
                                   font=FONT_SMALL, pad=(16, 7))
        self._fs_btn.pack()
        make_label(fs_row, "  F11 to toggle  ", font=("Segoe UI", 9),
                   fg=C["muted"], bg=C["bg"]).pack()

    def _quit(self):
        self.master.on_close()

    def _fs_label(self):
        return "⛶  Exit Fullscreen" if self.master._fullscreen else "⛶  Fullscreen"

    def _toggle_fs(self):
        self.master.toggle_fullscreen()
        # Refresh label after toggle
        self._fs_btn.config(text=self._fs_label())


# ══════════════════════════ BASE GAME SCREEN ════════════════════════════════

class BaseGameScreen(tk.Frame):
    """Shared logic for Normal and Endless mode."""

    def __init__(self, master, mode):
        super().__init__(master, bg=C["bg"])
        self.mode      = mode          # "normal" or "endless"
        self.score     = 0
        self.questions = 0             # cards answered
        self._anim_score = 0           # displayed score (animated)
        self._deck  = list(FLASHCARDS.keys())
        random.shuffle(self._deck)
        self._deck_idx  = 0
        self._revealed  = False
        self._build_ui()
        self._next_card()

    # ── UI construction ──────────────────────────────────────────────────────

    def _build_ui(self):
        top = tk.Frame(self, bg=C["bg"])
        top.pack(fill="x", padx=20, pady=10)

        make_button(top, "← Menu", self._back_to_menu,
                    bg=C["accent2"], font=FONT_SMALL, pad=(10, 5)).pack(side="left")

        title = "Normal Mode  (reach 11 pts)" if self.mode == "normal" else "Endless Mode"
        make_label(top, title, font=FONT_LARGE, fg=C["cyan"],
                   bg=C["bg"]).pack(side="left", padx=20)

        self.score_lbl = make_label(top, "Score: 0", font=FONT_LARGE,
                                    fg=C["yellow"], bg=C["bg"])
        self.score_lbl.pack(side="right")

        if self.mode == "normal":
            # Custom canvas progress bar (smooth + animatable on all platforms)
            self._pb_canvas = tk.Canvas(self, height=22, bg=C["bg"],
                                        highlightthickness=0)
            self._pb_canvas.pack(fill="x", padx=20, pady=(0, 10))
            self._pb_trough = None   # drawn once canvas has width
            self._pb_fill   = None
            self._pb_value  = 0.0   # current displayed value (0-11)
            self._pb_target = 0.0   # target value we're animating toward
            self._pb_color  = C["green"]
            self._pb_canvas.bind("<Configure>", self._pb_on_resize)

        # Card area (canvas for animations)
        self.canvas = tk.Canvas(self, bg=C["bg"], highlightthickness=0,
                                width=860, height=300)
        self.canvas.pack(pady=10)
        self._draw_card_bg()

        # Term text (large)
        self.term_text = self.canvas.create_text(
            430, 100, text="", fill=C["white"],
            font=("Segoe UI", 32, "bold"), width=780
        )
        # Answer text (revealed)
        self.ans_text = self.canvas.create_text(
            430, 200, text="", fill=C["cyan"],
            font=FONT_MED, width=780
        )

        # Button row
        btn_row = tk.Frame(self, bg=C["bg"])
        btn_row.pack(pady=8)

        self.reveal_btn = make_button(btn_row, "👁  Reveal Answer",
                                      self._reveal, bg=C["accent2"],
                                      font=FONT_LARGE, pad=(30, 12))
        self.reveal_btn.pack(side="left", padx=10)

        self.correct_btn = make_button(btn_row, "✅ Correct  +1",
                                       lambda: self._answer(True),
                                       bg=C["green"], font=FONT_LARGE,
                                       pad=(20, 12))
        self.wrong_btn   = make_button(btn_row, "❌ Wrong  -2" if self.mode == "normal"
                                       else "❌ Wrong",
                                       lambda: self._answer(False),
                                       bg=C["accent"], font=FONT_LARGE,
                                       pad=(20, 12))
        self.correct_btn.pack_forget()
        self.wrong_btn.pack_forget()

        # Question counter
        self.q_lbl = make_label(self, "Questions answered: 0",
                                font=FONT_SMALL, fg=C["muted"])
        self.q_lbl.pack()

    def _draw_card_bg(self):
        self.canvas.create_rectangle(10, 10, 850, 290,
                                     fill=C["card"], outline=C["accent2"],
                                     width=2)

    # ── Card logic ───────────────────────────────────────────────────────────

    def _next_card(self):
        self._revealed = False
        self.reveal_btn.pack(side="left", padx=10)
        self.correct_btn.pack_forget()
        self.wrong_btn.pack_forget()

        if self._deck_idx >= len(self._deck):
            random.shuffle(self._deck)
            self._deck_idx = 0

        term = self._deck[self._deck_idx]
        self._deck_idx += 1
        self._current_term = term
        self.canvas.itemconfig(self.term_text, text=term)
        self.canvas.itemconfig(self.ans_text, text="")

    def _reveal(self):
        if self._revealed:
            return
        self._revealed = True
        ans = FLASHCARDS[self._current_term]
        self.canvas.itemconfig(self.ans_text, text=ans)
        self.reveal_btn.pack_forget()
        self.correct_btn.pack(side="left", padx=10)
        self.wrong_btn.pack(side="left", padx=10)

    def _answer(self, correct):
        self.questions += 1
        self.q_lbl.config(text=f"Questions answered: {self.questions}")
        if correct:
            self.score += 1
            self._animate_score_change("+1", C["green"])
        else:
            self._on_wrong()
            return
        self._update_score_display()
        self._check_win()
        self._next_card()

    def _on_wrong(self):
        """Override in subclasses."""
        pass

    def _animate_score_change(self, text, color):
        """Float a label over the card."""
        cx = self.canvas.winfo_width() // 2 or 430
        FloatingText(self.canvas, cx, 150, text, color,
                     font=("Segoe UI", 26, "bold"))

    def _update_score_display(self, wrong=False):
        self.score_lbl.config(text=f"Score: {self.score}")
        if self.mode == "normal":
            self._pb_target = max(0.0, float(self.score))
            if wrong:
                self._pb_flash_red()
            else:
                self._pb_color = C["green"]
                self._pb_animate_fill()

    # ── Progress bar helpers ─────────────────────────────────────────────────

    def _pb_on_resize(self, event=None):
        """Draw or redraw the trough once the canvas has a real width."""
        self._pb_draw(self._pb_value)

    def _pb_draw(self, value):
        """Render trough + fill for `value` out of 11."""
        c = self._pb_canvas
        W = c.winfo_width()
        H = c.winfo_height()
        if W < 2:
            return
        c.delete("all")
        # Trough
        c.create_rectangle(0, 3, W, H - 3, fill=C["card"], outline="", tags="trough")
        # Fill
        fill_w = int((value / 11) * W)
        if fill_w > 0:
            c.create_rectangle(0, 3, fill_w, H - 3,
                               fill=self._pb_color, outline="", tags="fill")
        # Segment ticks
        for i in range(1, 11):
            x = int((i / 11) * W)
            c.create_line(x, 3, x, H - 3, fill=C["bg"], width=2)

    def _pb_animate_fill(self):
        """Smoothly tween _pb_value toward _pb_target."""
        diff = self._pb_target - self._pb_value
        if abs(diff) < 0.01:
            self._pb_value = self._pb_target
            self._pb_draw(self._pb_value)
            return
        self._pb_value += diff * 0.18   # easing factor
        self._pb_draw(self._pb_value)
        self.after(16, self._pb_animate_fill)

    def _pb_flash_red(self):
        """Turn bar red, shake it, then fade back to green."""
        self._pb_color = C["accent"]   # red
        self._pb_animate_fill()        # animate down to new value in red
        self._pb_shake(6, 0)           # start shake
        # After 2 s restore green
        self.after(2000, self._pb_restore_green)

    def _pb_shake(self, remaining, direction):
        """Shake by drawing the bar contents offset inside the canvas itself."""
        if remaining <= 0:
            self._pb_draw(self._pb_value)   # final clean redraw at offset 0
            return
        offset = 7 * (1 if direction % 2 == 0 else -1)
        self._pb_draw_offset(self._pb_value, offset)
        self.after(40, lambda: self._pb_shake(remaining - 1, direction + 1))

    def _pb_draw_offset(self, value, offset):
        """Like _pb_draw but shifts fill/ticks horizontally by offset pixels."""
        c = self._pb_canvas
        W = c.winfo_width()
        H = c.winfo_height()
        if W < 2:
            return
        c.delete("all")
        c.create_rectangle(0, 3, W, H - 3, fill=C["card"], outline="")
        fill_w = int((value / 11) * W)
        if fill_w > 0:
            x0 = max(0, offset)
            x1 = min(W, fill_w + offset)
            if x1 > x0:
                c.create_rectangle(x0, 3, x1, H - 3,
                                   fill=self._pb_color, outline="")
        for i in range(1, 11):
            x = int((i / 11) * W) + offset
            c.create_line(x, 3, x, H - 3, fill=C["bg"], width=2)

    def _pb_restore_green(self):
        self._pb_color = C["green"]
        self._pb_draw(self._pb_value)

    def _check_win(self):
        pass  # override

    def _back_to_menu(self):
        self.master.show_menu()


# ══════════════════════════ NORMAL MODE ═════════════════════════════════════

class NormalModeScreen(BaseGameScreen):

    def __init__(self, master):
        super().__init__(master, "normal")

    def _on_wrong(self):
        self.score = max(0, self.score - 2)
        self._animate_score_change("−2", C["accent"])
        self._update_score_display(wrong=True)
        self.after(400, self._next_card)   # small delay so animation is visible

    def _check_win(self):
        if self.score >= 11:
            db  = self.master.db
            uid = self.master.user["id"]
            db.increment_total_answered(uid, self.questions)
            # Award badges
            new_badges = []
            if db.award_badge(uid, "First Time"):
                new_badges.append("First Time")
            if self.questions < 15 and db.award_badge(uid, "Fast Learner"):
                new_badges.append("Fast Learner")
            self._check_flash_master()
            self.after(200, lambda: self.master.show_frame(
                VictoryScreen, score=self.score,
                questions=self.questions, new_badges=new_badges
            ))

    def _check_flash_master(self):
        db  = self.master.db
        uid = self.master.user["id"]
        # re-fetch total
        user = db.get_user(self.master.user["username"])
        if user["total_answered"] >= 100:
            db.award_badge(uid, "Flash Master")


# ══════════════════════════ ENDLESS MODE ════════════════════════════════════

class EndlessModeScreen(BaseGameScreen):

    def __init__(self, master):
        super().__init__(master, "endless")

    def _on_wrong(self):
        # Game over – check high score then show result
        db   = self.master.db
        uid  = self.master.user["id"]
        prev = self.master.user["endless_highscore"]
        db.increment_total_answered(uid, self.questions)
        self._check_endless_badges()
        new_hs = self.score > prev
        if new_hs:
            db.update_endless_highscore(uid, self.score)
            self.master.user["endless_highscore"] = self.score
        self.after(100, lambda: self.master.show_frame(
            EndlessResultScreen, score=self.score,
            prev_hs=prev, new_hs=new_hs
        ))

    def _check_endless_badges(self):
        db  = self.master.db
        uid = self.master.user["id"]
        if self.score >= 10:
            db.award_badge(uid, "Endless 10")
        if self.score >= 25:
            db.award_badge(uid, "Endless 25")
        if self.score >= 50:
            db.award_badge(uid, "Endless 50")
        user = db.get_user(self.master.user["username"])
        if user["total_answered"] >= 100:
            db.award_badge(uid, "Flash Master")


# ══════════════════════════ VICTORY SCREEN ══════════════════════════════════

class VictoryScreen(tk.Frame):

    def __init__(self, master, score, questions, new_badges):
        super().__init__(master, bg=C["bg"])
        self.score       = score
        self.questions   = questions
        self.new_badges  = new_badges
        self._build()

    def _build(self):
        W, H = 900, 650
        self.canvas = tk.Canvas(self, width=W, height=H,
                                bg=C["bg"], highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self._confetti = ConfettiCanvas(self.canvas, W, H)

        # YOU WIN text
        self.canvas.create_text(450, 160, text="🎉  YOU WIN! 🎉",
                                fill=C["yellow"],
                                font=("Segoe UI", 44, "bold"))
        self.canvas.create_text(450, 230,
                                text=f"Score: {self.score}  |  Questions: {self.questions}",
                                fill=C["cyan"], font=FONT_LARGE)

        # Badges unlocked
        y = 290
        if self.new_badges:
            self.canvas.create_text(450, y, text="🏅 Badge Unlocked!",
                                    fill=C["green"], font=FONT_LARGE)
            y += 40
            for b in self.new_badges:
                icon = next((d[2] for d in BADGE_DEFS if d[0] == b), "🏅")
                self.canvas.create_text(450, y,
                                        text=f"{icon}  {b}",
                                        fill=C["yellow"],
                                        font=("Segoe UI", 18, "bold"))
                y += 36

        # Pulsing badge glow animation
        self._glow_r = 60
        self._glow_dir = 1
        if self.new_badges:
            self._glow_item = self.canvas.create_oval(
                450 - 60, y - 10, 450 + 60, y + 50,
                outline=C["yellow"], width=3, fill=""
            )
            self._pulse_glow(y)

        # Buttons
        btn_frame = tk.Frame(self.canvas, bg=C["bg"])
        self.canvas.create_window(450, 580, window=btn_frame)
        make_button(btn_frame, "▶ Play Again", self.master.show_normal_mode,
                    bg=C["green"], pad=(20, 10)).pack(side="left", padx=10)
        make_button(btn_frame, "🏠 Main Menu", self.master.show_menu,
                    bg=C["accent2"], pad=(20, 10)).pack(side="left", padx=10)

    def _pulse_glow(self, cy):
        self._glow_r += self._glow_dir * 1.5
        if self._glow_r > 75 or self._glow_r < 50:
            self._glow_dir *= -1
        r = self._glow_r
        self.canvas.coords(self._glow_item,
                           450 - r, cy - 10, 450 + r, cy + 50)
        self.after(40, lambda: self._pulse_glow(cy))


# ══════════════════════════ ENDLESS RESULT SCREEN ═══════════════════════════

class EndlessResultScreen(tk.Frame):

    def __init__(self, master, score, prev_hs, new_hs):
        super().__init__(master, bg=C["bg"])
        self.score   = score
        self.prev_hs = prev_hs
        self.new_hs  = new_hs
        self._displayed = 0
        self._build()

    def _build(self):
        if self.new_hs:
            self._build_new_hs()
        else:
            self._build_normal()

    def _build_new_hs(self):
        W, H = 900, 650
        self.canvas = tk.Canvas(self, width=W, height=H,
                                bg=C["bg"], highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self._confetti = ConfettiCanvas(self.canvas, W, H)

        self.canvas.create_text(450, 180, text="🔥 NEW HIGH SCORE! 🔥",
                                fill=C["yellow"],
                                font=("Segoe UI", 40, "bold"))
        self._hs_text = self.canvas.create_text(
            450, 280, text="0",
            fill=C["cyan"], font=("Segoe UI", 72, "bold")
        )
        self._count_up()

        btn_frame = tk.Frame(self.canvas, bg=C["bg"])
        self.canvas.create_window(450, 430, window=btn_frame)
        make_button(btn_frame, "▶ Play Again", self.master.show_endless_mode,
                    bg=C["purple"], pad=(20, 10)).pack(side="left", padx=10)
        make_button(btn_frame, "🏠 Menu", self.master.show_menu,
                    bg=C["accent2"], pad=(20, 10)).pack(side="left", padx=10)

    def _count_up(self):
        if self._displayed < self.score:
            step = max(1, (self.score - self._displayed) // 8)
            self._displayed = min(self._displayed + step, self.score)
            self.canvas.itemconfig(self._hs_text, text=str(self._displayed))
            self.after(40, self._count_up)

    def _build_normal(self):
        make_label(self, "Game Over", font=("Segoe UI", 36, "bold"),
                   fg=C["accent"]).pack(pady=(80, 10))
        make_label(self, f"Your score: {self.score}",
                   font=FONT_LARGE, fg=C["text"]).pack(pady=6)
        make_label(self, f"High Score: {self.prev_hs}",
                   font=FONT_MED, fg=C["muted"]).pack(pady=6)

        row = tk.Frame(self, bg=C["bg"])
        row.pack(pady=30)
        make_button(row, "▶ Play Again", self.master.show_endless_mode,
                    bg=C["purple"], pad=(20, 10)).pack(side="left", padx=10)
        make_button(row, "🏠 Menu", self.master.show_menu,
                    bg=C["accent2"], pad=(20, 10)).pack(side="left", padx=10)


# ══════════════════════════ REWARDS SCREEN ══════════════════════════════════

class RewardsScreen(tk.Frame):

    def __init__(self, master):
        super().__init__(master, bg=C["bg"])
        self._build()

    def _build(self):
        make_label(self, "🏅  Badges & Rewards",
                   font=FONT_TITLE, fg=C["yellow"]).pack(pady=(30, 20))

        db       = self.master.db
        uid      = self.master.user["id"]
        earned   = db.get_user_badge_names(uid)
        all_b    = db.get_all_badges()

        frame = tk.Frame(self, bg=C["bg"])
        frame.pack(fill="both", expand=True, padx=60)

        for name, desc, icon in all_b:
            unlocked = name in earned
            row = tk.Frame(frame, bg=C["card" if unlocked else "panel"],
                           pady=12, padx=20)
            row.pack(fill="x", pady=5)

            left = tk.Frame(row, bg=row["bg"])
            left.pack(side="left")

            icon_label = tk.Label(left,
                                  text=icon if unlocked else "🔒",
                                  font=("Segoe UI", 28),
                                  bg=row["bg"],
                                  fg=C["yellow"] if unlocked else C["muted"])
            icon_label.pack(side="left", padx=(0, 14))

            info = tk.Frame(left, bg=row["bg"])
            info.pack(side="left")
            tk.Label(info, text=name,
                     font=("Segoe UI", 14, "bold"),
                     bg=row["bg"],
                     fg=C["text"] if unlocked else C["muted"]).pack(anchor="w")
            tk.Label(info, text=desc,
                     font=FONT_SMALL,
                     bg=row["bg"],
                     fg=C["muted"]).pack(anchor="w")

            status = tk.Label(row,
                              text="✓ Unlocked" if unlocked else "Locked",
                              font=("Segoe UI", 12, "bold"),
                              bg=row["bg"],
                              fg=C["green"] if unlocked else C["muted"])
            status.pack(side="right")

        make_button(self, "← Back", self.master.show_menu,
                    bg=C["accent2"], pad=(20, 8)).pack(pady=20)


# ══════════════════════════ LEADERBOARD SCREEN ══════════════════════════════

class LeaderboardScreen(tk.Frame):

    def __init__(self, master):
        super().__init__(master, bg=C["bg"])
        self._build()

    def _build(self):
        make_label(self, "📊  Leaderboard",
                   font=FONT_TITLE, fg=C["cyan"]).pack(pady=(30, 20))

        rows = self.master.db.get_leaderboard()

        frame = tk.Frame(self, bg=C["bg"])
        frame.pack(fill="both", expand=True, padx=60)

        # Header
        headers = ["Rank", "Username", "Endless High Score", "Badges Unlocked"]
        widths  = [6, 22, 22, 18]
        hrow = tk.Frame(frame, bg=C["accent2"])
        hrow.pack(fill="x")
        for h, w in zip(headers, widths):
            tk.Label(hrow, text=h, width=w, font=("Segoe UI", 12, "bold"),
                     bg=C["accent2"], fg=C["white"], pady=8).pack(side="left")

        for i, (uname, hs, bc) in enumerate(rows, 1):
            medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(i, f"#{i}")
            bg_c  = C["card"] if i % 2 == 0 else C["panel"]
            drow  = tk.Frame(frame, bg=bg_c)
            drow.pack(fill="x")
            for val, w in zip([medal, uname, hs, bc], widths):
                tk.Label(drow, text=str(val), width=w,
                         font=FONT_SMALL, bg=bg_c,
                         fg=C["yellow"] if i <= 3 else C["text"],
                         pady=8).pack(side="left")

        make_button(self, "← Back", self.master.show_menu,
                    bg=C["accent2"], pad=(20, 8)).pack(pady=20)


# ══════════════════════════ ENTRY POINT ═════════════════════════════════════

if __name__ == "__main__":
    app = FlashcardApp()
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()
