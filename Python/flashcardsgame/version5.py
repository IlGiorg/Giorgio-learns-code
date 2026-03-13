"""
CS Flashcard Game - Extended Edition
A gamified flashcard learning app with Endless Mode, Speedrun Mode,
expanded achievements, and enhanced database.
Built with Python 3, Tkinter, SQLite3
"""

import tkinter as tk
from tkinter import ttk
import sqlite3
import random
import math
import time
from datetime import datetime

# ─────────────────────────── ACHIEVEMENT DEFINITIONS ─────────────────────────

ACHIEVEMENTS = [
    # Progress Achievements
    ("First Steps",          "Answer 10 cards",          "🎯"),
    ("Learning Curve",       "Answer 50 cards",          "📘"),
    ("Knowledge Engine",     "Answer 250 cards",         "🧠"),
    ("Data Bank",            "Answer 500 cards",         "💾"),
    # Speed Achievements
    ("Lightning Brain",      "5 answers in 30 seconds",  "⚡"),
    ("Human Cache",          "10 answers no reveal",     "💡"),
    ("CPU Overclocked",      "20 correct streak",        "🔥"),
    # Endless Mode Achievements
    ("Survivor",             "Reach score 15 in Endless","🛡"),
    ("Untouchable",          "Reach score 30 in Endless","💠"),
    ("Legend",               "Reach score 75 in Endless","👑"),
    # Risk Achievements
    ("Gambler",              "Cash out with score 1",    "🎲"),
    ("Risk Taker",           "Cash out with score 20+",  "💰"),
    # Speedrun Achievements
    ("Blitz Master",         "Score 20 in 60s mode",     "⚡"),
    ("Marathon Runner",      "Score 100 in Marathon",    "🏃"),
    ("Reflex God",           "Survive 30 Reflex Qs",     "🎯"),
    # Perfection Achievements
    ("Flawless",             "Win Normal with no mistakes","✨"),
    ("Memory Palace",        "Win Normal without reveal", "🏛"),
    # Fun Achievements
    ("Database Brain",       "See all cards in a session","🗄"),
    ("Night Coder",          "Play after midnight",       "🌙"),
    ("Addicted",             "5 consecutive games",       "🎮"),
    # Bonus Achievements
    ("Stack Overflow",       "Answer 404 questions total","💻"),
    ("Binary Master",        "Reach score 32 in Endless", "🔢"),
    ("Root Access",          "Unlock 10 badges",          "🔑"),
    ("System Administrator", "Unlock 20 badges",          "👨‍💻"),
    # Original badges
    ("First Time",           "Win Normal Mode once",      "🏆"),
    ("Fast Learner",         "Win in under 15 questions", "⚡"),
    ("Endless 10",           "Score 10+ in Endless",      "🔥"),
    ("Endless 25",           "Score 25+ in Endless",      "💎"),
    ("Endless 50",           "Score 50+ in Endless",      "👑"),
    ("Flash Master",         "Answer 100 cards total",    "🎓"),
]

# ─────────────────────────── FLASHCARD DATA ──────────────────────────────────

FLASHCARDS = {
    # ── Original 25 ──────────────────────────────────────────────────────────
    "RAM":   "Random Access Memory – temporary storage used by the CPU",
    "CPU":   "Central Processing Unit – the primary processor of a computer",
    "HTTP":  "HyperText Transfer Protocol – used for web communication",
    "IP":    "Internet Protocol – identifies devices on a network",
    "DNS":   "Domain Name System – translates domain names to IP addresses",
    "GUI":   "Graphical User Interface – visual way to interact with software",
    "API":   "Application Programming Interface – lets programs talk to each other",
    "SQL":   "Structured Query Language – language for managing databases",
    "OS":    "Operating System – manages hardware and software resources",
    "URL":   "Uniform Resource Locator – address for internet resources",
    "HTML":  "HyperText Markup Language – structure language for web pages",
    "CSS":   "Cascading Style Sheets – styling language for web pages",
    "OOP":   "Object-Oriented Programming – design paradigm using objects",
    "IDE":   "Integrated Development Environment – software for coding",
    "LAN":   "Local Area Network – network within a limited area",
    "WAN":   "Wide Area Network – network spanning large geographical areas",
    "SSH":   "Secure Shell – cryptographic network protocol for remote access",
    "VPN":   "Virtual Private Network – encrypted private network over internet",
    "BIOS":  "Basic Input/Output System – firmware initializing hardware at boot",
    "ROM":   "Read-Only Memory – non-volatile permanent storage",
    "HTTPS": "HyperText Transfer Protocol Secure – encrypted HTTP",
    "JSON":  "JavaScript Object Notation – lightweight data-interchange format",
    "XML":   "eXtensible Markup Language – flexible data markup language",
    "SDK":   "Software Development Kit – tools for building applications",
    "EOF":   "End Of File – marker signaling the end of a data stream",

    # ── A ────────────────────────────────────────────────────────────────────
    "ALU":                    "Arithmetic Logic Unit. Does all the maths",
    "ANALOGUE":               "Smooth stream of data that our senses process",
    "ARQ":                    "Automatic Repeat Request. Acknowledgement is sent from the receiver to the sender to signal it has successfully received the packet. If it fails it will send a timeout error",
    "ASYMMETRIC ENCRYPTION":  "A type of encryption that uses two different keys to encrypt and decrypt data",
    "AUTOMATED":              "Processes that are performed by a computer without human intervention",
    "ACTUATOR":               "A device that changes electrical signals into physical actions",
    "ARTIFICIAL INTELLIGENCE":"A part of computer science that looks at creating machines that can think and perform tasks a person would usually perform",
    "AI":                     "A part of computer science that looks at creating machines that can think and perform tasks a person would usually perform",

    # ── B ────────────────────────────────────────────────────────────────────
    "BINARY":      "Base 2. Units increase to the power of 2",
    "BOOLEAN":     "A data type. True or False",
    "PRIMARY KEY": "A unique identifier for a record",

    # ── C ────────────────────────────────────────────────────────────────────
    "CONTROLLER":  "Input device because inputs things and output because vibrates",
    "CAMERA":      "Input. Can also be output if it has a screen on it to view photos",
    "COMPRESSION": "A method that uses an algorithm to reduce the size of a file",
    "CHECK DIGIT": "A method of error checking that adds up all the digits and divides by ten. Remainder is checkdigit",
    "CYPHER":      "The name given to data after transmission",

    # ── D ────────────────────────────────────────────────────────────────────
    "DIGITAL":          "Data represented in the values of 1 and 0 that a computer can understand",
    "DATA":             "Numbers, symbols, raw format characters before processing",
    "DENARY":           "Base 10. Units increase to the power of 10",
    "DICTIONARY":       "A dictionary is a mutable, ordered collection of key valued pairs",
    "DATA PACKET":      "A small unit of data",
    "PACKET":           "A small unit of data",
    "PACKET SWITCHING": "A method of sending packets of information over a network",
    "DATA TRANSMISSION":"Sending and receiving information over a network",
    "DATABASE":         "An example of application software to store and manipulate data",
    "DATA TYPE":        "The characteristics of a piece of data. Common data types are string, integer, real and Boolean",
    "DIV":              "The division operator. It gives the whole number part of a division calculation. E.g. 7 div 2 = 3",

    # ── E ────────────────────────────────────────────────────────────────────
    "ETHERNET":       "Another type of connection that can be used to transmit data within a network",
    "ECHO CHECK":     "A type of error detection method that sends the transmitted data back to the sender to be compared with the original data sent",
    "ENCRYPTION":     "A method of securing data for storage or transmission that scrambles it and makes it meaningless",
    "ENCRYPTION KEY": "A type of algorithm",
    "EXPERT SYSTEM":  "A computer program that uses a set of rules to provide advice or make decisions in a specific area",

    # ── F ────────────────────────────────────────────────────────────────────
    "FIELD": "An individual piece of data, e.g. date of birth",

    # ── G ────────────────────────────────────────────────────────────────────
    "GPU":  "Graphics Processing Unit. Controls the video output",
    "AND":  "Outputs 1 only if all inputs are 1, otherwise 0",
    "OR":   "Output 1 if at least 1 input is 1",
    "NOT":  "Input 1 becomes 0, input 0 becomes 1",
    "NAND": "Inverts inputs from AND",
    "NOR":  "Inverts inputs from OR",
    "XOR":  "If inputs are different outputs 1, otherwise 0",

    # ── H ────────────────────────────────────────────────────────────────────
    "HDD":       "Hard Disk Drive. Non-Volatile. Secondary Memory",
    "HARDWARE":  "Any physical part of a PC that you can touch",
    "HEADPHONES":"Output",

    # ── I ────────────────────────────────────────────────────────────────────
    "INPUT":           "When a user enters information or data into a computer",
    "INFORMATION":     "Data that has a context and can be interpreted with meaning",
    "IF":              "Checks something",
    "LOGICAL OPERATOR":"A symbol that performs a comparison resulting in True or False. Can be equals, not equal to, less than, less than or equal to, greater than, greater than or equal to",
    "INFERENCE ENGINE":"The part of an expert system that applies the rules from the rule base to the facts in the knowledge base to deduce new facts or make decisions",

    # ── K ────────────────────────────────────────────────────────────────────
    "KEYBOARD":      "Input",
    "KNOWLEDGE BASE":"A collection of facts and rules used by an expert system",

    # ── L ────────────────────────────────────────────────────────────────────
    "LIGHT RING": "Output because gives light",
    "LOSSY":      "A compression method that reduces the size of a file by permanently removing data",
    "LOSSLESS":   "A compression method that reduces the size of a file by temporarily altering the data",
    "LIST":       "A list is a mutable, ordered collection of elements. Lists are for ordered, changeable sequences",

    # ── M ────────────────────────────────────────────────────────────────────
    "MOTHERBOARD":   "Main circuit board of a computer",
    "MONITOR":       "Output because shows what's happening",
    "MICROPHONE":    "Input because gets sound",
    "MICROPROCESSOR":"An integrated circuit that is able to perform the functions of a computer's central processing unit (CPU)",
    "MACHINE LEARNING":"A computer program that can adapt its stored rules or processes",
    "MOD":           "The modulus operator. It gives the remainder part of a division calculation. E.g. 7 mod 2 = 1",

    # ── P ────────────────────────────────────────────────────────────────────
    "PAYLOAD":      "The actual data the user is sending to the receiver",
    "TRAILER":      "A section of a packet of data that contains information about any error checking methods that can be used",
    "PARITY CHECK": "A way of checking that the data being sent is correct. if 0100110 we make it 10100110",
    "PCHK ERROR":   "When two bits are reversed which means that the parity check passes but the data received is wrong",

    # ── Q ────────────────────────────────────────────────────────────────────
    "SERIAL":      "A transmission method where data is sent one bit at a time down a single wire",
    "PARALLEL":    "A transmission method where data is sent multiple bits at a time down multiple wires",
    "INTERFERENCE":"Disruption, such as electromagnetism, to data when it is transmitted",
    "SIMPLEX":     "A transmission method where data is transmitted in a single direction only",
    "DUPLEX":      "A transmission method where data is transmitted in both directions, but only one direction at a time",
    "FULL DUPLEX": "A transmission method where data is transmitted in both directions at the same time",

    # ── R ────────────────────────────────────────────────────────────────────
    "RECORD":    "All of the information in a table about one object, e.g. all the personal details about one student",
    "ROBOT":     "A machine that emulates human actions",
    "ROBOTICS":  "The branch of technology that deals with the design, construction, operation, and application of robots",
    "RULE BASE": "A collection of rules used by an expert system",

    # ── S ────────────────────────────────────────────────────────────────────
    "STRING":   "Strings are words, characters or symbols in quotation marks in Python",
    "SSD":      "Solid State Drive. Store everything. Secondary Memory",
    "SOFTWARE": "Any programs, app functions etc. of a computer that you can't touch",
    "SENSOR":   "Detects changes in the environment and sends the data to the computer",
    "SPEAKERS": "Output because makes sound",

    # ── T ────────────────────────────────────────────────────────────────────
    "TUPLE": "A tuple is an immutable, ordered collection of elements",
    "TABLE": "A set of data about one type of objects",

    # ── U ────────────────────────────────────────────────────────────────────
    "USB":            "Universal Serial Bus. An industry standard that is used to transmit data",
    "USB PORT":       "A socket that is part of a device or computer that enables you to insert a USB method",
    "USB CABLE":      "A type of transmission media that uses the USB method to transmit data",
    "USB CONNECTION": "A collective name for using a USB cable plugged into a USB port to transfer data from one device to another",
    "USB DEVICE":     "The name of a device that plugs into a USB port",

    # ── V ────────────────────────────────────────────────────────────────────
    "VR HEADSET": "Output Device for Virtual Reality",
    "VR":         "Virtual Reality",
}

# ─────────────────────────── BADGE DEPENDENCIES ──────────────────────────────

BADGE_DEPENDENCIES = {
    "Human Cache":          ["First Steps"],
    "CPU Overclocked":      ["Learning Curve"],
    "Legend":               ["Survivor", "Untouchable"],
    "System Administrator": ["Root Access"],
    "Memory Palace":        ["First Time"],
    "Flawless":             ["First Time"],
}

# Speedrun unlock threshold – normal-mode questions answered
SPEEDRUN_UNLOCK_AT = 40
TIMEWARP_UNLOCK_AT = 100

# ─────────────────────────── COLOUR PALETTE ──────────────────────────────────

C = {
    "bg":      "#0f0f1a",
    "panel":   "#1a1a2e",
    "card":    "#16213e",
    "accent":  "#e94560",
    "accent2": "#0f3460",
    "green":   "#00d26a",
    "yellow":  "#ffd700",
    "text":    "#eaeaea",
    "muted":   "#888899",
    "white":   "#ffffff",
    "purple":  "#7b2fff",
    "cyan":    "#00d4ff",
    "orange":  "#ff8c00",
    "pink":    "#ff6b9d",
}

FONT_TITLE = ("Segoe UI", 28, "bold")
FONT_LARGE = ("Segoe UI", 18, "bold")
FONT_MED   = ("Segoe UI", 14)
FONT_SMALL = ("Segoe UI", 11)
FONT_MONO  = ("Consolas", 13)


# ══════════════════════════ DATABASE MANAGER ═════════════════════════════════

class DatabaseManager:
    def __init__(self, db_path="flashcard_game.db"):
        self.conn = sqlite3.connect(db_path)
        self._create_tables()
        self._migrate_schema()
        self._seed_badges()

    def _create_tables(self):
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id                INTEGER PRIMARY KEY AUTOINCREMENT,
                username          TEXT UNIQUE NOT NULL,
                code              TEXT NOT NULL,
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

    def _migrate_schema(self):
        cur = self.conn.cursor()
        new_cols = [
            ("total_correct",             "INTEGER DEFAULT 0"),
            ("games_played",              "INTEGER DEFAULT 0"),
            ("current_streak",            "INTEGER DEFAULT 0"),
            ("longest_streak",            "INTEGER DEFAULT 0"),
            ("questions_without_reveal",  "INTEGER DEFAULT 0"),
            ("last_play_time",            "TEXT DEFAULT ''"),
            ("speedrun_highscore",        "INTEGER DEFAULT 0"),
            ("speedrun_unlocked",         "INTEGER DEFAULT 0"),
            ("consecutive_games",         "INTEGER DEFAULT 0"),
            ("normal_questions_answered", "INTEGER DEFAULT 0"),
        ]
        existing = {r[1] for r in cur.execute("PRAGMA table_info(users)").fetchall()}
        for col, typedef in new_cols:
            if col not in existing:
                cur.execute(f"ALTER TABLE users ADD COLUMN {col} {typedef}")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS game_history (
                id                 INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id            INTEGER NOT NULL,
                mode               TEXT NOT NULL,
                score              INTEGER DEFAULT 0,
                questions_answered INTEGER DEFAULT 0,
                timestamp          TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def _seed_badges(self):
        cur = self.conn.cursor()
        for name, desc, icon in ACHIEVEMENTS:
            cur.execute(
                "INSERT OR IGNORE INTO badges (badge_name, description, icon) VALUES (?,?,?)",
                (name, desc, icon))
        self.conn.commit()

    # ── User ─────────────────────────────────────────────────────────────────

    def user_exists(self, username):
        return self.conn.execute(
            "SELECT id FROM users WHERE username=?", (username,)).fetchone() is not None

    def verify_code(self, username, code):
        return self.conn.execute(
            "SELECT id FROM users WHERE username=? AND code=?",
            (username, code)).fetchone() is not None

    def create_user(self, username, code):
        self.conn.execute(
            "INSERT INTO users (username, code, last_play_time) VALUES (?,?,?)",
            (username, code, datetime.now().isoformat()))
        self.conn.commit()

    def get_user(self, username):
        row = self.conn.execute(
            "SELECT * FROM users WHERE username=?", (username,)).fetchone()
        if not row:
            return None
        cols = [r[1] for r in self.conn.execute("PRAGMA table_info(users)").fetchall()]
        return dict(zip(cols, row))

    def update_streak(self, user_id, correct):
        if correct:
            self.conn.execute("""
                UPDATE users SET
                    current_streak = current_streak + 1,
                    longest_streak = MAX(longest_streak, current_streak + 1),
                    total_correct  = total_correct + 1,
                    last_play_time = ?
                WHERE id = ?""", (datetime.now().isoformat(), user_id))
        else:
            self.conn.execute(
                "UPDATE users SET current_streak=0, last_play_time=? WHERE id=?",
                (datetime.now().isoformat(), user_id))
        self.conn.commit()

    def increment_total_answered(self, user_id, count):
        self.conn.execute(
            "UPDATE users SET total_answered=total_answered+? WHERE id=?",
            (count, user_id))
        self.conn.commit()

    def increment_normal_questions(self, user_id, count):
        """Track questions answered in normal mode for speedrun unlock."""
        self.conn.execute(
            "UPDATE users SET normal_questions_answered=normal_questions_answered+? WHERE id=?",
            (count, user_id))
        self.conn.commit()

    def increment_games_played(self, user_id):
        self.conn.execute(
            "UPDATE users SET games_played=games_played+1 WHERE id=?", (user_id,))
        self.conn.commit()

    def update_consecutive_games(self, user_id, n):
        self.conn.execute(
            "UPDATE users SET consecutive_games=? WHERE id=?", (n, user_id))
        self.conn.commit()

    def check_and_unlock_speedrun(self, user_id):
        """Unlock speedrun if normal_questions_answered >= threshold."""
        row = self.conn.execute(
            "SELECT normal_questions_answered, speedrun_unlocked FROM users WHERE id=?",
            (user_id,)).fetchone()
        if row and row[0] >= SPEEDRUN_UNLOCK_AT and not row[1]:
            self.conn.execute(
                "UPDATE users SET speedrun_unlocked=1 WHERE id=?", (user_id,))
            self.conn.commit()
            return True
        return False

    def update_endless_highscore(self, user_id, score):
        self.conn.execute(
            "UPDATE users SET endless_highscore=? WHERE id=? AND endless_highscore<?",
            (score, user_id, score))
        self.conn.commit()

    def update_speedrun_highscore(self, user_id, score):
        self.conn.execute(
            "UPDATE users SET speedrun_highscore=? WHERE id=? AND speedrun_highscore<?",
            (score, user_id, score))
        self.conn.commit()

    def save_game_history(self, user_id, mode, score, questions):
        self.conn.execute(
            "INSERT INTO game_history(user_id,mode,score,questions_answered,timestamp)"
            " VALUES(?,?,?,?,?)",
            (user_id, mode, score, questions, datetime.now().isoformat()))
        self.conn.commit()

    # ── Badges ───────────────────────────────────────────────────────────────

    def award_badge(self, user_id, badge_name):
        cur = self.conn.cursor()
        row = cur.execute(
            "SELECT id FROM badges WHERE badge_name=?", (badge_name,)).fetchone()
        if not row:
            return False
        badge_id = row[0]
        # Dependency check
        if badge_name in BADGE_DEPENDENCIES:
            for dep in BADGE_DEPENDENCIES[badge_name]:
                dep_row = cur.execute(
                    "SELECT id FROM badges WHERE badge_name=?", (dep,)).fetchone()
                if not dep_row:
                    return False
                if not cur.execute(
                        "SELECT 1 FROM user_badges WHERE user_id=? AND badge_id=?",
                        (user_id, dep_row[0])).fetchone():
                    return False
        # Already awarded?
        if cur.execute(
                "SELECT 1 FROM user_badges WHERE user_id=? AND badge_id=?",
                (user_id, badge_id)).fetchone():
            return False
        cur.execute("INSERT INTO user_badges(user_id,badge_id) VALUES(?,?)",
                    (user_id, badge_id))
        self.conn.commit()
        self._check_badge_count(user_id)
        return True

    def _check_badge_count(self, user_id):
        count = self.conn.execute(
            "SELECT COUNT(*) FROM user_badges WHERE user_id=?",
            (user_id,)).fetchone()[0]
        if count >= 10:
            self.award_badge(user_id, "Root Access")
        if count >= 20:
            self.award_badge(user_id, "System Administrator")

    def get_user_badge_names(self, user_id):
        rows = self.conn.execute("""
            SELECT b.badge_name FROM badges b
            JOIN user_badges ub ON b.id=ub.badge_id
            WHERE ub.user_id=?""", (user_id,)).fetchall()
        return {r[0] for r in rows}

    def get_all_badges(self):
        return self.conn.execute(
            "SELECT badge_name, description, icon FROM badges").fetchall()

    def check_progress_achievements(self, user_id):
        total = self.conn.execute(
            "SELECT total_answered FROM users WHERE id=?",
            (user_id,)).fetchone()[0]
        if total >= 10:   self.award_badge(user_id, "First Steps")
        if total >= 50:   self.award_badge(user_id, "Learning Curve")
        if total >= 100:  self.award_badge(user_id, "Flash Master")
        if total >= 250:  self.award_badge(user_id, "Knowledge Engine")
        if total >= 404:  self.award_badge(user_id, "Stack Overflow")
        if total >= 500:  self.award_badge(user_id, "Data Bank")

    # ── Leaderboard ──────────────────────────────────────────────────────────

    def get_leaderboard(self):
        return self.conn.execute("""
            SELECT u.username,
                   u.endless_highscore,
                   u.speedrun_highscore,
                   COUNT(ub.badge_id) AS badge_count,
                   u.total_answered
            FROM users u
            LEFT JOIN user_badges ub ON u.id=ub.user_id
            GROUP BY u.id
            ORDER BY u.endless_highscore DESC, u.total_answered DESC
        """).fetchall()

    def close(self):
        self.conn.close()


# ══════════════════════════ ANIMATION HELPERS ════════════════════════════════

class FloatingText:
    def __init__(self, canvas, x, y, text, color, font=("Segoe UI", 20, "bold")):
        self.canvas = canvas
        self.item   = canvas.create_text(x, y, text=text, fill=color, font=font)
        self.y      = float(y)
        self.life   = 26
        self._step()

    def _step(self):
        self.life -= 1
        if self.life <= 0:
            try: self.canvas.delete(self.item)
            except: pass
            return
        self.y -= 2.2
        cx = (self.canvas.winfo_width() or 430) // 2
        self.canvas.coords(self.item, cx, self.y)
        self.canvas.after(30, self._step)


class ConfettiCanvas:
    COLORS = ["#e94560","#ffd700","#00d4ff","#00d26a","#7b2fff","#ff6b6b"]

    def __init__(self, canvas, w, h):
        self.canvas = canvas; self.w = w; self.h = h
        self.parts  = []
        self._spawn()

    def _spawn(self):
        for _ in range(80):
            x     = random.randint(0, self.w)
            y     = random.randint(-self.h, 0)
            size  = random.randint(6, 14)
            color = random.choice(self.COLORS)
            item  = self.canvas.create_rectangle(
                x, y, x+size, y+size, fill=color, outline="")
            self.parts.append([x, y, size,
                                random.uniform(3, 8),
                                random.uniform(-2, 2),
                                0.0,
                                random.uniform(-5, 5),
                                item])
        self._animate()

    def _animate(self):
        for p in self.parts:
            p[1] += p[3]; p[0] += p[4]; p[5] += p[6]
            if p[1] > self.h:
                p[1] = random.randint(-60, -10)
                p[0] = random.randint(0, self.w)
            rad = math.radians(p[5])
            self.canvas.coords(p[7], p[0], p[1],
                               p[0]+p[2]*math.cos(rad),
                               p[1]+p[2]*math.sin(rad))
        self.canvas.after(30, self._animate)


class GlowEffect:
    """Pulsing highlight border on a Label-button."""
    def __init__(self, widget, color=C["green"]):
        self.widget    = widget
        self.color     = color
        self.direction = 1
        self.thickness = 2
        self._pulse()

    def _pulse(self):
        self.thickness += self.direction
        if self.thickness >= 6 or self.thickness <= 2:
            self.direction *= -1
        try:
            self.widget.config(
                highlightthickness=self.thickness,
                highlightbackground=self.color,
                highlightcolor=self.color)
            self.widget.after(70, self._pulse)
        except: pass


class AchievementPopup(tk.Toplevel):
    """Bottom-right toast for newly unlocked badges."""
    def __init__(self, master, badge_name):
        super().__init__(master)
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.configure(bg=C["panel"])
        icon = next((b[2] for b in ACHIEVEMENTS if b[0] == badge_name), "🏅")
        tk.Label(self, text="🔓 Achievement Unlocked!",
                 font=("Segoe UI", 11, "bold"),
                 fg=C["yellow"], bg=C["panel"]).pack(padx=18, pady=(10, 2))
        tk.Label(self, text=f"{icon}  {badge_name}",
                 font=("Segoe UI", 13, "bold"),
                 fg=C["cyan"], bg=C["panel"]).pack(padx=18, pady=(0, 10))
        self.update_idletasks()
        mw = master.winfo_width();  mx = master.winfo_x()
        mh = master.winfo_height(); my = master.winfo_y()
        pw = self.winfo_width();    ph = self.winfo_height()
        self.geometry(f"+{mx+mw-pw-20}+{my+mh-ph-60}")
        self._alpha = 1.0
        self.after(2400, self._fade)

    def _fade(self):
        self._alpha -= 0.07
        if self._alpha <= 0:
            self.destroy(); return
        try:
            self.attributes("-alpha", max(0, self._alpha))
            self.after(40, self._fade)
        except: pass


def queue_popups(master, badges, delay=0):
    for i, name in enumerate(badges):
        master.after(delay + i * 750, lambda n=name: AchievementPopup(master, n))


# ══════════════════════════ WIDGET HELPERS ════════════════════════════════════

def _lighten(hex_color, amount):
    h = hex_color.lstrip("#")
    r = max(0, min(255, int(h[0:2], 16) + amount))
    g = max(0, min(255, int(h[2:4], 16) + amount))
    b = max(0, min(255, int(h[4:6], 16) + amount))
    return f"#{r:02x}{g:02x}{b:02x}"


def make_button(parent, text, command, bg=C["accent"], fg=C["white"],
                font=FONT_MED, pad=(20, 10), width=None):
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


def make_label(parent, text, font=FONT_MED, fg=C["text"], bg=C["bg"], **kw):
    return tk.Label(parent, text=text, font=font, fg=fg, bg=bg, **kw)


# ══════════════════════════ MAIN APPLICATION ═════════════════════════════════

class FlashcardApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CS Flashcard Game — Extended Edition")
        self.geometry("920x660")
        self.resizable(True, True)
        self.configure(bg=C["bg"])
        self.minsize(720, 540)
        self._fullscreen    = False
        self._current_frame = None
        self.bind("<F11>",    lambda e: self.toggle_fullscreen())
        self.bind("<Escape>", lambda e: self.exit_fullscreen())
        self.db   = DatabaseManager()
        self.user = None
        self.show_login()

    def toggle_fullscreen(self):
        self._fullscreen = not self._fullscreen
        self.attributes("-fullscreen", self._fullscreen)

    def exit_fullscreen(self):
        if self._fullscreen:
            self._fullscreen = False
            self.attributes("-fullscreen", False)

    def show_frame(self, FrameClass, **kwargs):
        if self._current_frame:
            self._current_frame.destroy()
        frame = FrameClass(self, **kwargs)
        frame.pack(fill="both", expand=True)
        self._current_frame = frame

    def show_login(self):        self.show_frame(LoginScreen)
    def show_menu(self):         self.show_frame(MainMenu)
    def show_normal_mode(self):  self.show_frame(NormalModeScreen)
    def show_endless_mode(self): self.show_frame(EndlessModeScreen)
    def show_rewards(self):      self.show_frame(RewardsScreen)
    def show_leaderboard(self):  self.show_frame(LeaderboardScreen)

    def show_speedrun_menu(self):
        if self.user and self.user.get("speedrun_unlocked", 0):
            self.show_frame(SpeedrunMenuScreen)
        else:
            self.show_frame(SpeedrunLockedScreen)

    def show_speedrun_mode(self, mode_type):
        self.show_frame(SpeedrunModeScreen, mode_type=mode_type)

    def on_close(self):
        self.db.close()
        self.destroy()


# ══════════════════════════ LOGIN ════════════════════════════════════════════

class LoginScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=C["bg"])
        self._build()

    def _build(self):
        make_label(self, "🖥  CS Flashcard Game",
                   font=("Segoe UI", 26, "bold"), fg=C["cyan"]).pack(pady=(60, 5))
        make_label(self, "Learn Computer Science — Level Up!",
                   font=FONT_SMALL, fg=C["muted"]).pack(pady=(0, 40))
        panel = tk.Frame(self, bg=C["panel"], padx=40, pady=30)
        panel.pack()
        make_label(panel, "Enter your username",
                   bg=C["panel"], fg=C["text"], font=FONT_MED).pack(anchor="w")
        self._uvar = tk.StringVar()
        e = tk.Entry(panel, textvariable=self._uvar, font=FONT_MED,
                     bg=C["card"], fg=C["text"], insertbackground=C["text"],
                     relief="flat", width=28)
        e.pack(pady=(6, 20), ipady=8)
        e.focus()
        e.bind("<Return>", lambda _: self._proceed())
        make_button(panel, "Continue →", self._proceed,
                    bg=C["accent"], width=26).pack(pady=(0, 6))
        self._msg = tk.StringVar()
        tk.Label(panel, textvariable=self._msg, bg=C["panel"],
                 fg="#ff6b6b", font=FONT_SMALL).pack()

    def _proceed(self):
        username = self._uvar.get().strip()
        if not username:
            self._msg.set("Please enter a username."); return
        CodeDialog(self.master, username,
                   new_user=not self.master.db.user_exists(username))


class CodeDialog(tk.Toplevel):
    def __init__(self, master, username, new_user):
        super().__init__(master)
        self.master = master; self.username = username; self.new_user = new_user
        self.title("Set Code" if new_user else "Enter Code")
        self.geometry("380x260"); self.resizable(False, False)
        self.configure(bg=C["panel"]); self.grab_set()
        self._build()

    def _build(self):
        msg = (f"Welcome, {self.username}!\nSet a 4-digit code:"
               if self.new_user else
               f"Welcome back, {self.username}!\nEnter your code:")
        make_label(self, msg, bg=C["panel"], fg=C["text"],
                   font=FONT_MED, justify="center").pack(pady=(30, 14))
        self._cv = tk.StringVar()
        e = tk.Entry(self, textvariable=self._cv, show="●",
                     font=("Consolas", 22, "bold"), bg=C["card"],
                     fg=C["cyan"], insertbackground=C["cyan"],
                     relief="flat", width=8, justify="center")
        e.pack(ipady=8); e.focus()
        e.bind("<Return>", lambda _: self._submit())
        make_button(self, "Confirm", self._submit,
                    bg=C["accent"], pad=(30, 8)).pack(pady=14)
        self._err = make_label(self, "", bg=C["panel"], fg="#ff6b6b",
                               font=FONT_SMALL)
        self._err.pack()

    def _submit(self):
        code = self._cv.get().strip()
        if len(code) != 4 or not code.isdigit():
            self._err.config(text="Code must be exactly 4 digits."); return
        db = self.master.db
        if self.new_user:
            db.create_user(self.username, code)
        elif not db.verify_code(self.username, code):
            self._err.config(text="Wrong code. Try again."); return
        self.master.user = db.get_user(self.username)
        self.destroy()
        self.master.show_menu()


# ══════════════════════════ MAIN MENU ════════════════════════════════════════

class MainMenu(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=C["bg"])
        self._build()

    def _build(self):
        user = self.master.user
        make_label(self, f"Welcome, {user['username']}  👋",
                   font=FONT_TITLE, fg=C["cyan"]).pack(pady=(30, 2))

        sr_unlocked = user.get("speedrun_unlocked", 0)
        normal_q    = user.get("normal_questions_answered", 0)
        needed      = max(0, SPEEDRUN_UNLOCK_AT - normal_q)

        if sr_unlocked:
            stats = (f"Endless HS: {user['endless_highscore']}  |  "
                     f"Speedrun HS: {user.get('speedrun_highscore', 0)}  |  "
                     f"Total Q: {user['total_answered']}")
        else:
            stats = (f"Endless HS: {user['endless_highscore']}  |  "
                     f"Normal Q: {normal_q}/{SPEEDRUN_UNLOCK_AT}  "
                     f"(Speedrun unlocks at {SPEEDRUN_UNLOCK_AT})")

        make_label(self, stats, font=FONT_SMALL, fg=C["yellow"]).pack(pady=(0, 20))

        sr_text  = "⚡  Speedrun Mode" if sr_unlocked else f"⚡  Speedrun Mode 🔒 ({needed} more Qs)"
        sr_color = C["orange"] if sr_unlocked else C["muted"]

        btns = [
            ("▶  Play Normal Mode",  C["accent"],   self.master.show_normal_mode),
            ("♾  Endless Mode",      C["purple"],   self.master.show_endless_mode),
            (sr_text,                sr_color,      self.master.show_speedrun_menu),
            ("🏅  Rewards / Badges", "#1a6b3c",     self.master.show_rewards),
            ("📊  Leaderboard",      C["accent2"],  self.master.show_leaderboard),
            ("✕  Quit Game",         "#333344",     self._quit),
        ]
        for text, color, cmd in btns:
            make_button(self, text, cmd, bg=color,
                        font=FONT_LARGE, pad=(40, 12), width=30).pack(pady=5)

        fs_row = tk.Frame(self, bg=C["bg"])
        fs_row.pack(pady=(8, 0))
        self._fs_btn = make_button(fs_row, self._fs_label(), self._toggle_fs,
                                   bg="#2a2a3e", font=FONT_SMALL, pad=(16, 7))
        self._fs_btn.pack()
        make_label(fs_row, "  F11 to toggle  ",
                   font=("Segoe UI", 9), fg=C["muted"]).pack()

    def _quit(self):     self.master.on_close()
    def _fs_label(self): return "⛶  Exit Fullscreen" if self.master._fullscreen else "⛶  Fullscreen"
    def _toggle_fs(self):
        self.master.toggle_fullscreen()
        self._fs_btn.config(text=self._fs_label())


# ══════════════════════════ SPEEDRUN LOCKED ══════════════════════════════════

class SpeedrunLockedScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=C["bg"])
        self._build()

    def _build(self):
        make_label(self, "🔒  Speedrun Mode Locked",
                   font=FONT_TITLE, fg=C["muted"]).pack(pady=(80, 20))
        user   = self.master.user
        normal = user.get("normal_questions_answered", 0)
        needed = max(0, SPEEDRUN_UNLOCK_AT - normal)
        make_label(self,
                   f"Answer {SPEEDRUN_UNLOCK_AT} questions in Normal Mode to unlock.",
                   font=FONT_LARGE, fg=C["text"]).pack(pady=10)
        make_label(self, f"Progress:  {normal} / {SPEEDRUN_UNLOCK_AT}",
                   font=FONT_MED, fg=C["yellow"]).pack(pady=5)
        make_label(self, f"Still need:  {needed} more questions",
                   font=FONT_MED, fg=C["cyan"] if needed > 0 else C["green"]).pack(pady=5)

        bar_frame = tk.Frame(self, bg=C["card"], height=14, width=400)
        bar_frame.pack(pady=14); bar_frame.pack_propagate(False)
        ratio = min(1.0, normal / SPEEDRUN_UNLOCK_AT)
        tk.Frame(bar_frame,
                 bg=C["green"] if ratio >= 1 else C["cyan"],
                 height=14,
                 width=int(400 * ratio)).place(x=0, y=0)

        make_button(self, "▶  Play Normal Mode", self.master.show_normal_mode,
                    bg=C["accent"], font=FONT_LARGE, pad=(30, 12)).pack(pady=24)
        make_button(self, "← Back to Menu", self.master.show_menu,
                    bg=C["accent2"], pad=(20, 8)).pack()


# ══════════════════════════ SPEEDRUN MENU ════════════════════════════════════

class SpeedrunMenuScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=C["bg"])
        self._build()

    def _build(self):
        make_label(self, "⚡  Speedrun Mode",
                   font=FONT_TITLE, fg=C["orange"]).pack(pady=(40, 20))
        make_label(self, "Choose your challenge:",
                   font=FONT_LARGE, fg=C["text"]).pack(pady=(0, 20))
        modes = [
            ("⏱  60 Seconds Chaos",  "60s",      "Answer as many cards as possible in 60 seconds"),
            ("🏃  Marathon (10 min)", "marathon",  "Endurance challenge – 10 full minutes"),
            ("🎯  Reflex Mode",       "reflex",    "10 seconds per question – timer resets on correct"),
        ]
        for title, mid, desc in modes:
            panel = tk.Frame(self, bg=C["card"], padx=30, pady=12)
            panel.pack(pady=8, fill="x", padx=100)
            make_label(panel, title, font=FONT_LARGE,
                       fg=C["orange"], bg=C["card"]).pack()
            make_label(panel, desc, font=FONT_SMALL,
                       fg=C["muted"], bg=C["card"]).pack()
            m = mid
            make_button(panel, "Select →",
                        lambda m=m: self.master.show_speedrun_mode(m),
                        bg=C["orange"], pad=(20, 5)).pack(pady=(8, 0))
        make_button(self, "← Back to Menu", self.master.show_menu,
                    bg=C["accent2"], pad=(20, 8)).pack(pady=24)


# ══════════════════════════ BASE GAME SCREEN ══════════════════════════════════

class BaseGameScreen(tk.Frame):
    """Shared scaffolding – subclasses override _on_wrong / _cash_out / _check_win."""

    def __init__(self, master, mode):
        super().__init__(master, bg=C["bg"])
        self.mode           = mode
        self.score          = 0
        self.questions      = 0
        self.correct_streak = 0
        self._deck          = list(FLASHCARDS.keys())
        random.shuffle(self._deck)
        self._deck_idx    = 0
        self._revealed    = False
        self._reveal_used = False
        self._start_time  = time.time()
        self._session_cards = set()
        self._mistakes    = 0
        self._no_reveal_run = True
        self._build_ui()
        self._next_card()

    # ── UI ────────────────────────────────────────────────────────────────────

    def _build_ui(self):
        top = tk.Frame(self, bg=C["bg"])
        top.pack(fill="x", padx=20, pady=10)
        make_button(top, "← Menu", self._back_to_menu,
                    bg=C["accent2"], font=FONT_SMALL, pad=(10, 5)).pack(side="left")
        make_label(top, self._get_title(),
                   font=FONT_LARGE, fg=C["cyan"], bg=C["bg"]).pack(side="left", padx=20)
        self.score_lbl = make_label(top, "Score: 0",
                                    font=FONT_LARGE, fg=C["yellow"], bg=C["bg"])
        self.score_lbl.pack(side="right")

        if self.mode == "normal":
            self._pb_canvas = tk.Canvas(self, height=22, bg=C["bg"],
                                        highlightthickness=0)
            self._pb_canvas.pack(fill="x", padx=20, pady=(0, 10))
            self._pb_value  = 0.0
            self._pb_target = 0.0
            self._pb_color  = C["green"]
            self._pb_canvas.bind("<Configure>", lambda e: self._pb_draw(self._pb_value))

        self.canvas = tk.Canvas(self, bg=C["bg"], highlightthickness=0,
                                width=860, height=280)
        self.canvas.pack(pady=6)
        self._draw_card_bg()
        self.term_text = self.canvas.create_text(
            430, 95, text="", fill=C["white"],
            font=("Segoe UI", 32, "bold"), width=780)
        self.ans_text = self.canvas.create_text(
            430, 195, text="", fill=C["cyan"],
            font=FONT_MED, width=780)

        btn_row = tk.Frame(self, bg=C["bg"])
        btn_row.pack(pady=6)
        self.reveal_btn = make_button(btn_row, "👁  Reveal Answer", self._reveal,
                                      bg=C["accent2"], font=FONT_LARGE, pad=(30, 12))
        self.reveal_btn.pack(side="left", padx=10)
        self.correct_btn = make_button(btn_row, "✅ Correct  +1",
                                       lambda: self._answer(True),
                                       bg=C["green"], font=FONT_LARGE, pad=(20, 12))
        self.wrong_btn   = make_button(btn_row,
                                       "❌ Wrong  -2" if self.mode == "normal" else "❌ Wrong",
                                       lambda: self._answer(False),
                                       bg=C["accent"], font=FONT_LARGE, pad=(20, 12))
        self.correct_btn.pack_forget()
        self.wrong_btn.pack_forget()

        self.q_lbl = make_label(self, "Questions answered: 0",
                                font=FONT_SMALL, fg=C["muted"])
        self.q_lbl.pack()

        # Cash Out button – Endless only
        if self.mode == "endless":
            co_outer = tk.Frame(self, bg=C["bg"])
            co_outer.pack(pady=6)
            self.cashout_btn = make_button(
                co_outer, "💾  Cash Out", self._cash_out,
                bg=C["green"], fg=C["bg"],
                font=("Segoe UI", 15, "bold"), pad=(28, 10))
            self.cashout_btn.pack()
            GlowEffect(self.cashout_btn, color=C["green"])
            make_label(co_outer, "Save your score — wrong answer loses it",
                       font=("Segoe UI", 9), fg=C["muted"], bg=C["bg"]).pack(pady=(2, 0))

    def _get_title(self):
        if self.mode == "normal":  return "Normal Mode  (reach 11 pts)"
        if self.mode == "endless": return "Endless Mode"
        return "Speedrun"

    def _draw_card_bg(self):
        self.canvas.create_rectangle(10, 10, 850, 270,
                                     fill=C["card"], outline=C["accent2"], width=2)

    # ── Cards ─────────────────────────────────────────────────────────────────

    def _next_card(self):
        self._revealed = self._reveal_used = False
        self.reveal_btn.pack(side="left", padx=10)
        self.correct_btn.pack_forget()
        self.wrong_btn.pack_forget()
        if self._deck_idx >= len(self._deck):
            random.shuffle(self._deck)
            self._deck_idx = 0
        term = self._deck[self._deck_idx]
        self._deck_idx += 1
        self._current_term = term
        self._session_cards.add(term)
        self.canvas.itemconfig(self.term_text, text=term)
        self.canvas.itemconfig(self.ans_text,  text="")

    def _reveal(self):
        if self._revealed: return
        self._revealed = self._reveal_used = True
        self._no_reveal_run = False
        self.canvas.itemconfig(self.ans_text, text=FLASHCARDS[self._current_term])
        self.reveal_btn.pack_forget()
        self.correct_btn.pack(side="left", padx=10)
        self.wrong_btn.pack(side="left",   padx=10)

    def _answer(self, correct):
        self.questions += 1
        self.q_lbl.config(text=f"Questions answered: {self.questions}")
        db  = self.master.db
        uid = self.master.user["id"]
        db.update_streak(uid, correct)
        if correct:
            self.score += 1
            self.correct_streak += 1
            self._float("+1", C["green"])
            if self.correct_streak >= 20:
                db.award_badge(uid, "CPU Overclocked")
        else:
            self.correct_streak = 0
            self._on_wrong()
            return
        self._update_score_display()
        if not self._reveal_used and self.questions == 10:
            db.award_badge(uid, "Human Cache")
        if self.questions >= 5 and (time.time() - self._start_time) < 30:
            db.award_badge(uid, "Lightning Brain")
        self._check_win()
        self._next_card()

    def _float(self, text, color):
        cx = (self.canvas.winfo_width() or 430) // 2
        FloatingText(self.canvas, cx, 135, text, color,
                     font=("Segoe UI", 26, "bold"))

    def _on_wrong(self):  pass
    def _cash_out(self):  pass
    def _check_win(self): pass

    def _update_score_display(self, wrong=False):
        self.score_lbl.config(text=f"Score: {self.score}")
        if self.mode == "normal":
            self._pb_target = max(0.0, float(self.score))
            if wrong:
                self._pb_color = C["accent"]
                self._pb_animate_fill()
                self._pb_shake(6, 0)
                self.after(2000, self._pb_restore_green)
            else:
                self._pb_color = C["green"]
                self._pb_animate_fill()

    def _back_to_menu(self):
        self.master.user = self.master.db.get_user(self.master.user["username"])
        self.master.show_menu()

    # ── Progress bar ──────────────────────────────────────────────────────────

    def _pb_draw(self, val, offset=0):
        c = self._pb_canvas; W = c.winfo_width(); H = c.winfo_height()
        if W < 2: return
        c.delete("all")
        c.create_rectangle(0, 3, W, H-3, fill=C["card"], outline="")
        fw = int((val/11)*W)
        if fw > 0:
            x0 = max(0, offset); x1 = min(W, fw+offset)
            if x1 > x0:
                c.create_rectangle(x0, 3, x1, H-3, fill=self._pb_color, outline="")
        for i in range(1, 11):
            x = int((i/11)*W)+offset
            c.create_line(x, 3, x, H-3, fill=C["bg"], width=2)

    def _pb_animate_fill(self):
        diff = self._pb_target - self._pb_value
        if abs(diff) < 0.01:
            self._pb_value = self._pb_target
            self._pb_draw(self._pb_value); return
        self._pb_value += diff * 0.18
        self._pb_draw(self._pb_value)
        self.after(16, self._pb_animate_fill)

    def _pb_shake(self, remaining, direction):
        if remaining <= 0:
            self._pb_draw(self._pb_value); return
        self._pb_draw(self._pb_value, 7*(1 if direction%2==0 else -1))
        self.after(40, lambda: self._pb_shake(remaining-1, direction+1))

    def _pb_restore_green(self):
        self._pb_color = C["green"]
        self._pb_draw(self._pb_value)


# ══════════════════════════ NORMAL MODE ══════════════════════════════════════

class NormalModeScreen(BaseGameScreen):
    def __init__(self, master):
        super().__init__(master, "normal")

    def _on_wrong(self):
        self.score = max(0, self.score - 2)
        self._mistakes += 1
        self._float("−2", C["accent"])
        self._update_score_display(wrong=True)
        self.after(400, self._next_card)

    def _check_win(self):
        if self.score < 11: return
        db  = self.master.db
        uid = self.master.user["id"]

        db.increment_total_answered(uid, self.questions)
        db.increment_normal_questions(uid, self.questions)
        db.increment_games_played(uid)
        db.save_game_history(uid, "normal", self.score, self.questions)
        db.check_progress_achievements(uid)

        if datetime.now().hour < 5:
            db.award_badge(uid, "Night Coder")

        consec = (self.master.user.get("consecutive_games", 0) or 0) + 1
        db.update_consecutive_games(uid, consec)
        if consec >= 5: db.award_badge(uid, "Addicted")

        # Unlock speedrun if threshold met
        db.check_and_unlock_speedrun(uid)
        self.master.user = db.get_user(self.master.user["username"])

        new_badges = []
        if db.award_badge(uid, "First Time"):    new_badges.append("First Time")
        if self.questions < 15 and db.award_badge(uid, "Fast Learner"):
            new_badges.append("Fast Learner")
        if self._mistakes == 0 and db.award_badge(uid, "Flawless"):
            new_badges.append("Flawless")
        if self._no_reveal_run and db.award_badge(uid, "Memory Palace"):
            new_badges.append("Memory Palace")
        if len(self._session_cards) >= len(FLASHCARDS):
            if db.award_badge(uid, "Database Brain"):
                new_badges.append("Database Brain")

        queue_popups(self.master, new_badges, delay=400)
        self.after(200, lambda: self.master.show_frame(
            VictoryScreen, score=self.score,
            questions=self.questions, new_badges=new_badges))


# ══════════════════════════ ENDLESS MODE ════════════════════════════════════

class EndlessModeScreen(BaseGameScreen):
    """
    Cash Out rule:
      • Cash Out  → score SAVED, high score updated if beaten
      • Wrong ans → run ends, score LOST, high score NOT updated
    """

    def __init__(self, master):
        super().__init__(master, "endless")
        self._ended = False   # guard against double-trigger

    def _on_wrong(self):
        """Wrong answer: run ends immediately, score is lost, HS not updated."""
        if self._ended: return
        self._ended = True
        db  = self.master.db
        uid = self.master.user["id"]

        db.increment_total_answered(uid, self.questions)
        db.increment_games_played(uid)
        db.save_game_history(uid, "endless_wrong", self.score, self.questions)
        db.check_progress_achievements(uid)
        self._award_endless_badges(db, uid)

        if datetime.now().hour < 5:
            db.award_badge(uid, "Night Coder")

        consec = (self.master.user.get("consecutive_games", 0) or 0) + 1
        db.update_consecutive_games(uid, consec)
        if consec >= 5: db.award_badge(uid, "Addicted")

        # !! HIGH SCORE IS NOT UPDATED on wrong answer !!
        prev_hs = self.master.user["endless_highscore"]
        self.master.user = db.get_user(self.master.user["username"])

        self.after(120, lambda: self.master.show_frame(
            EndlessResultScreen,
            score=self.score, prev_hs=prev_hs,
            new_hs=False, cashout=False))

    def _cash_out(self):
        """Player voluntarily cashes out: score saved, HS updated if beaten."""
        if self._ended: return
        self._ended = True
        db  = self.master.db
        uid = self.master.user["id"]

        db.increment_total_answered(uid, self.questions)
        db.increment_games_played(uid)
        db.save_game_history(uid, "endless_cashout", self.score, self.questions)
        db.check_progress_achievements(uid)
        self._award_endless_badges(db, uid)

        # Risk achievements
        if self.score == 1: db.award_badge(uid, "Gambler")
        if self.score >= 20: db.award_badge(uid, "Risk Taker")

        if datetime.now().hour < 5:
            db.award_badge(uid, "Night Coder")

        consec = (self.master.user.get("consecutive_games", 0) or 0) + 1
        db.update_consecutive_games(uid, consec)
        if consec >= 5: db.award_badge(uid, "Addicted")

        prev_hs = self.master.user["endless_highscore"]
        new_hs  = self.score > prev_hs
        if new_hs:
            db.update_endless_highscore(uid, self.score)
        self.master.user = db.get_user(self.master.user["username"])

        new_badges = []
        queue_popups(self.master, new_badges)

        self.after(120, lambda: self.master.show_frame(
            EndlessResultScreen,
            score=self.score, prev_hs=prev_hs,
            new_hs=new_hs, cashout=True))

    def _award_endless_badges(self, db, uid):
        if self.score >= 10:  db.award_badge(uid, "Endless 10")
        if self.score >= 15:  db.award_badge(uid, "Survivor")
        if self.score >= 25:  db.award_badge(uid, "Endless 25")
        if self.score >= 30:  db.award_badge(uid, "Untouchable")
        if self.score >= 32:  db.award_badge(uid, "Binary Master")
        if self.score >= 50:  db.award_badge(uid, "Endless 50")
        if self.score >= 75:  db.award_badge(uid, "Legend")


# ══════════════════════════ SPEEDRUN MODE ════════════════════════════════════

class SpeedrunModeScreen(BaseGameScreen):
    def __init__(self, master, mode_type):
        self.speedrun_type  = mode_type
        self.timer_running  = False
        super().__init__(master, "speedrun")
        self.time_left      = self._initial_time()
        self.timer_running  = True
        self._tick()

    def _initial_time(self):
        return {"60s": 60, "marathon": 600, "reflex": 10}[self.speedrun_type]

    # Build extra timer UI on top of base UI
    def _build_ui(self):
        super()._build_ui()
        # Timer bar
        self._tb = tk.Canvas(self, height=14, bg=C["bg"], highlightthickness=0)
        self._tb.pack(fill="x", padx=20, pady=(0, 4))
        self._tb.bind("<Configure>", lambda e: self._draw_timer_bar())
        # Timer label row
        tr = tk.Frame(self, bg=C["bg"]); tr.pack()
        make_label(tr, "⏱  Time:", font=FONT_MED, fg=C["cyan"]).pack(side="left")
        self._timer_lbl = make_label(tr, "0",
                                     font=("Segoe UI", 20, "bold"),
                                     fg=C["green"], bg=C["bg"])
        self._timer_lbl.pack(side="left", padx=8)

    def _draw_timer_bar(self):
        c = self._tb; W = c.winfo_width(); H = c.winfo_height()
        if W < 2: return
        c.delete("all")
        total = self._initial_time()
        ratio = max(0.0, getattr(self, "time_left", total) / total)
        color = C["accent"] if ratio < 0.25 else C["yellow"] if ratio < 0.5 else C["green"]
        c.create_rectangle(0, 2, W, H-2, fill=C["card"], outline="")
        fw = int(ratio * W)
        if fw > 0:
            c.create_rectangle(0, 2, fw, H-2, fill=color, outline="")

    def _tick(self):
        if not self.timer_running: return
        self.time_left -= 1
        mins = int(self.time_left) // 60
        secs = int(self.time_left) % 60
        if self.speedrun_type == "marathon":
            lbl = f"{mins}:{secs:02d}"
        else:
            lbl = str(max(0, int(self.time_left)))
        self._timer_lbl.config(text=lbl)
        self._draw_timer_bar()
        # Flash red < 10s
        if self.time_left < 10:
            clr = C["accent"] if int(self.time_left * 2) % 2 == 0 else C["yellow"]
            self._timer_lbl.config(fg=clr)
        else:
            self._timer_lbl.config(fg=C["green"])
        if self.time_left <= 0:
            self._end_speedrun(); return
        self.after(1000, self._tick)

    def _on_wrong(self):
        # Wrong = just advance (no penalty in speedrun)
        self._next_card()

    def _answer(self, correct):
        super()._answer(correct)
        if correct and self.speedrun_type == "reflex":
            self.time_left = 10   # reset reflex timer

    def _end_speedrun(self):
        self.timer_running = False
        db  = self.master.db
        uid = self.master.user["id"]
        db.increment_total_answered(uid, self.questions)
        db.increment_games_played(uid)
        db.save_game_history(uid, f"speedrun_{self.speedrun_type}",
                             self.score, self.questions)
        db.update_speedrun_highscore(uid, self.score)
        db.check_progress_achievements(uid)

        new_badges = []
        if   self.speedrun_type == "60s"     and self.score    >= 20: nb = "Blitz Master"
        elif self.speedrun_type == "marathon" and self.score   >= 100: nb = "Marathon Runner"
        elif self.speedrun_type == "reflex"   and self.questions >= 30: nb = "Reflex God"
        else: nb = None
        if nb and db.award_badge(uid, nb): new_badges.append(nb)

        if datetime.now().hour < 5 and db.award_badge(uid, "Night Coder"):
            new_badges.append("Night Coder")

        queue_popups(self.master, new_badges)
        self.master.user = db.get_user(self.master.user["username"])
        self.after(100, lambda: self.master.show_frame(
            SpeedrunResultScreen, score=self.score,
            mode_type=self.speedrun_type, questions=self.questions))

    def _back_to_menu(self):
        self.timer_running = False
        super()._back_to_menu()


# ══════════════════════════ VICTORY SCREEN ═══════════════════════════════════

class VictoryScreen(tk.Frame):
    def __init__(self, master, score, questions, new_badges):
        super().__init__(master, bg=C["bg"])
        self.score = score; self.questions = questions; self.new_badges = new_badges
        self._build()

    def _build(self):
        W, H = 920, 660
        c = tk.Canvas(self, width=W, height=H, bg=C["bg"], highlightthickness=0)
        c.pack(fill="both", expand=True)
        ConfettiCanvas(c, W, H)
        c.create_text(460, 160, text="🎉  YOU WIN! 🎉",
                      fill=C["yellow"], font=("Segoe UI", 44, "bold"))
        c.create_text(460, 230,
                      text=f"Score: {self.score}  |  Questions: {self.questions}",
                      fill=C["cyan"], font=FONT_LARGE)
        y = 290
        if self.new_badges:
            c.create_text(460, y, text="🏅 Badges Unlocked!",
                          fill=C["green"], font=FONT_LARGE); y += 40
            for b in self.new_badges:
                icon = next((a[2] for a in ACHIEVEMENTS if a[0] == b), "🏅")
                c.create_text(460, y, text=f"{icon}  {b}",
                              fill=C["yellow"], font=("Segoe UI", 18, "bold")); y += 36
        bf = tk.Frame(c, bg=C["bg"])
        c.create_window(460, 590, window=bf)
        make_button(bf, "▶ Play Again", self.master.show_normal_mode,
                    bg=C["green"], pad=(20, 10)).pack(side="left", padx=10)
        make_button(bf, "🏠 Menu", self.master.show_menu,
                    bg=C["accent2"], pad=(20, 10)).pack(side="left", padx=10)


# ══════════════════════════ ENDLESS RESULT ════════════════════════════════════

class EndlessResultScreen(tk.Frame):
    def __init__(self, master, score, prev_hs, new_hs, cashout=False):
        super().__init__(master, bg=C["bg"])
        self.score   = score
        self.prev_hs = prev_hs
        self.new_hs  = new_hs
        self.cashout = cashout
        self._displayed = 0
        self._build()

    def _build(self):
        if self.new_hs:
            self._build_new_hs()
        else:
            self._build_normal()

    def _build_new_hs(self):
        W, H = 920, 660
        c = tk.Canvas(self, width=W, height=H, bg=C["bg"], highlightthickness=0)
        c.pack(fill="both", expand=True)
        ConfettiCanvas(c, W, H)
        header = "💾 CASHED OUT — NEW HIGH SCORE! 🔥" if self.cashout else "🔥 NEW HIGH SCORE! 🔥"
        c.create_text(460, 175, text=header,
                      fill=C["yellow"], font=("Segoe UI", 36, "bold"))
        self._hs_txt = c.create_text(460, 285, text="0",
                                     fill=C["cyan"], font=("Segoe UI", 72, "bold"))
        self._c = c
        self._count_up()
        bf = tk.Frame(c, bg=C["bg"])
        c.create_window(460, 430, window=bf)
        make_button(bf, "▶ Play Again", self.master.show_endless_mode,
                    bg=C["purple"], pad=(20, 10)).pack(side="left", padx=10)
        make_button(bf, "🏠 Menu", self.master.show_menu,
                    bg=C["accent2"], pad=(20, 10)).pack(side="left", padx=10)

    def _count_up(self):
        if self._displayed < self.score:
            step = max(1, (self.score - self._displayed) // 8)
            self._displayed = min(self._displayed + step, self.score)
            self._c.itemconfig(self._hs_txt, text=str(self._displayed))
            self.after(40, self._count_up)

    def _build_normal(self):
        if self.cashout:
            header = "💾  Cashed Out!"
            hfg    = C["green"]
            note   = "Your score was saved."
        else:
            header = "❌  Wrong Answer — Score Lost"
            hfg    = C["accent"]
            note   = "Wrong answer ends the run. Cash out next time to save your score!"

        make_label(self, header, font=("Segoe UI", 36, "bold"), fg=hfg).pack(pady=(70, 10))
        make_label(self, f"Your score: {self.score}",
                   font=FONT_LARGE, fg=C["text"]).pack(pady=6)
        make_label(self, f"High Score: {self.prev_hs}",
                   font=FONT_MED, fg=C["muted"]).pack(pady=6)
        make_label(self, note, font=FONT_SMALL, fg=C["muted"]).pack(pady=4)

        row = tk.Frame(self, bg=C["bg"])
        row.pack(pady=24)
        make_button(row, "▶ Play Again", self.master.show_endless_mode,
                    bg=C["purple"], pad=(20, 10)).pack(side="left", padx=10)
        make_button(row, "🏠 Menu", self.master.show_menu,
                    bg=C["accent2"], pad=(20, 10)).pack(side="left", padx=10)


# ══════════════════════════ SPEEDRUN RESULT ══════════════════════════════════

class SpeedrunResultScreen(tk.Frame):
    def __init__(self, master, score, mode_type, questions):
        super().__init__(master, bg=C["bg"])
        self.score = score; self.mode_type = mode_type; self.questions = questions
        self._build()

    def _build(self):
        names = {"60s": "60 Seconds Chaos", "marathon": "Marathon", "reflex": "Reflex Mode"}
        make_label(self, f"⚡ {names.get(self.mode_type,'Speedrun')} Complete!",
                   font=("Segoe UI", 34, "bold"), fg=C["orange"]).pack(pady=(60, 10))
        make_label(self, f"Score: {self.score}",
                   font=FONT_LARGE, fg=C["yellow"]).pack(pady=6)
        make_label(self, f"Questions answered: {self.questions}",
                   font=FONT_MED, fg=C["text"]).pack(pady=4)
        hs = self.master.user.get("speedrun_highscore", 0)
        if self.score >= hs and self.score > 0:
            make_label(self, "🏆 New Speedrun High Score!",
                       font=FONT_LARGE, fg=C["green"]).pack(pady=6)
        row = tk.Frame(self, bg=C["bg"])
        row.pack(pady=24)
        mt = self.mode_type
        make_button(row, "▶ Play Again",
                    lambda: self.master.show_speedrun_mode(mt),
                    bg=C["orange"], pad=(20, 10)).pack(side="left", padx=10)
        make_button(row, "⚡ Other Modes", self.master.show_speedrun_menu,
                    bg=C["accent2"], pad=(20, 10)).pack(side="left", padx=10)
        make_button(row, "🏠 Menu", self.master.show_menu,
                    bg=C["purple"], pad=(20, 10)).pack(side="left", padx=10)


# ══════════════════════════ REWARDS SCREEN ═══════════════════════════════════

class RewardsScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=C["bg"])
        self._build()

    def _build(self):
        make_label(self, "🏅  Badges & Rewards",
                   font=FONT_TITLE, fg=C["yellow"]).pack(pady=(20, 4))

        db     = self.master.db
        uid    = self.master.user["id"]
        earned = db.get_user_badge_names(uid)
        all_b  = db.get_all_badges()

        # Stats bar
        sf = tk.Frame(self, bg=C["panel"], pady=8, padx=20)
        sf.pack(fill="x", padx=40, pady=(0, 8))
        make_label(sf, f"Total Questions: {self.master.user['total_answered']}",
                   font=FONT_MED, fg=C["cyan"], bg=C["panel"]).pack(side="left")
        make_label(sf, f"  |  Badges: {len(earned)} / {len(all_b)}",
                   font=FONT_MED, fg=C["yellow"], bg=C["panel"]).pack(side="left")

        # Category layout
        CATEGORIES = [
            ("🏆 Original",   ["First Time","Fast Learner","Flash Master","Endless 10","Endless 25","Endless 50"]),
            ("📈 Progress",   ["First Steps","Learning Curve","Knowledge Engine","Data Bank"]),
            ("⚡ Speed",      ["Lightning Brain","Human Cache","CPU Overclocked"]),
            ("♾ Endless",    ["Survivor","Untouchable","Legend"]),
            ("💰 Risk",       ["Gambler","Risk Taker"]),
            ("🏃 Speedrun",   ["Blitz Master","Marathon Runner","Reflex God"]),
            ("✨ Perfection", ["Flawless","Memory Palace"]),
            ("🎮 Fun",        ["Database Brain","Night Coder","Addicted"]),
            ("💻 Bonus",      ["Stack Overflow","Binary Master","Root Access","System Administrator"]),
        ]

        badge_lookup = {row[0]: (row[1], row[2]) for row in all_b}

        # Scrollable container
        outer = tk.Frame(self, bg=C["bg"])
        outer.pack(fill="both", expand=True, padx=40)
        scv = tk.Canvas(outer, bg=C["bg"], highlightthickness=0)
        sb  = tk.Scrollbar(outer, orient="vertical", command=scv.yview)
        scv.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        scv.pack(side="left", fill="both", expand=True)

        inner = tk.Frame(scv, bg=C["bg"])
        win   = scv.create_window(0, 0, anchor="nw", window=inner)
        inner.bind("<Configure>", lambda e: scv.configure(scrollregion=scv.bbox("all")))
        scv.bind("<Configure>",   lambda e: scv.itemconfig(win, width=e.width))
        scv.bind_all("<MouseWheel>",
                     lambda e: scv.yview_scroll(-1*(e.delta//120), "units"))

        for cat_name, badge_list in CATEGORIES:
            # Category header
            hf = tk.Frame(inner, bg=C["accent2"])
            hf.pack(fill="x", pady=(12, 4))
            tk.Label(hf, text=cat_name, font=("Segoe UI", 13, "bold"),
                     fg=C["white"], bg=C["accent2"], pady=4
                     ).pack(anchor="w", padx=12)

            for name in badge_list:
                if name not in badge_lookup: continue
                desc, icon = badge_lookup[name]
                unlocked   = name in earned

                row = tk.Frame(inner,
                               bg=C["card"] if unlocked else C["panel"],
                               pady=7, padx=14)
                row.pack(fill="x", pady=2)

                # Icon
                tk.Label(row,
                         text=icon if unlocked else "🔒",
                         font=("Segoe UI", 20),
                         bg=row["bg"],
                         fg=C["yellow"] if unlocked else C["muted"]
                         ).pack(side="left", padx=(0, 12))

                # Name + desc
                info = tk.Frame(row, bg=row["bg"])
                info.pack(side="left", fill="x", expand=True)
                tk.Label(info, text=name,
                         font=("Segoe UI", 12, "bold"),
                         bg=row["bg"],
                         fg=C["text"] if unlocked else C["muted"],
                         anchor="w").pack(anchor="w")
                tk.Label(info, text=desc,
                         font=FONT_SMALL, bg=row["bg"],
                         fg=C["muted"], anchor="w").pack(anchor="w")

                # Status
                tk.Label(row,
                         text="✓ Unlocked" if unlocked else "Locked",
                         font=("Segoe UI", 10, "bold"),
                         bg=row["bg"],
                         fg=C["green"] if unlocked else C["muted"]
                         ).pack(side="right")

        make_button(self, "← Back to Menu", self.master.show_menu,
                    bg=C["accent2"], pad=(20, 8)).pack(pady=10)


# ══════════════════════════ LEADERBOARD ══════════════════════════════════════

class LeaderboardScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=C["bg"])
        self._build()

    def _build(self):
        make_label(self, "📊  Leaderboard",
                   font=FONT_TITLE, fg=C["cyan"]).pack(pady=(24, 16))

        rows = self.master.db.get_leaderboard()

        outer = tk.Frame(self, bg=C["bg"])
        outer.pack(fill="both", expand=True, padx=40)

        # ── Column spec: (header, min_width_px, flex_weight) ─────────────────
        # Using a grid-based approach so headers and data cells share identical
        # column geometry — the only reliable way to keep them aligned.
        COLS = [
            ("Rank",     70,  0),
            ("Username", 180, 1),   # flex so it grows with window
            ("Endless",  90,  0),
            ("Speedrun", 90,  0),
            ("Badges",   70,  0),
            ("Total Q",  80,  0),
        ]

        # ── Header row ───────────────────────────────────────────────────────
        hdr = tk.Frame(outer, bg=C["accent2"])
        hdr.pack(fill="x")
        for col_i, (label, w, flex) in enumerate(COLS):
            hdr.grid_columnconfigure(col_i, weight=flex, minsize=w)
        for col_i, (label, w, flex) in enumerate(COLS):
            tk.Label(hdr, text=label,
                     font=("Segoe UI", 11, "bold"),
                     bg=C["accent2"], fg=C["white"],
                     padx=6, pady=7, anchor="center"
                     ).grid(row=0, column=col_i, sticky="ew")

        # ── Scrollable body ──────────────────────────────────────────────────
        body_wrap = tk.Frame(outer, bg=C["bg"])
        body_wrap.pack(fill="both", expand=True)
        scv = tk.Canvas(body_wrap, bg=C["bg"], highlightthickness=0)
        sb  = tk.Scrollbar(body_wrap, orient="vertical", command=scv.yview)
        scv.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        scv.pack(side="left", fill="both", expand=True)

        body = tk.Frame(scv, bg=C["bg"])
        win  = scv.create_window(0, 0, anchor="nw", window=body)
        body.bind("<Configure>", lambda e: scv.configure(scrollregion=scv.bbox("all")))
        scv.bind("<Configure>",  lambda e: scv.itemconfig(win, width=e.width))

        # Mirror the same column config on every data row frame
        def _configure_row_cols(frame):
            for col_i, (_, w, flex) in enumerate(COLS):
                frame.grid_columnconfigure(col_i, weight=flex, minsize=w)

        MEDALS    = {1: "🥇", 2: "🥈", 3: "🥉"}
        MEDAL_FG  = {1: C["yellow"], 2: "#c0c0c0", 3: "#cd7f32"}

        for i, (uname, hs, sp, bc, tq) in enumerate(rows, 1):
            bg_c      = C["card"] if i % 2 == 0 else C["panel"]
            medal     = MEDALS.get(i, f"#{i}")
            medal_clr = MEDAL_FG.get(i, C["text"])
            name_fg   = C["yellow"] if i <= 3 else C["text"]

            drow = tk.Frame(body, bg=bg_c)
            drow.pack(fill="x")
            _configure_row_cols(drow)

            cells = [
                (medal,   "center", medal_clr),
                (uname,   "w",      name_fg),
                (str(hs), "center", C["green"]  if hs > 0 else C["muted"]),
                (str(sp), "center", C["orange"] if sp > 0 else C["muted"]),
                (str(bc), "center", C["yellow"] if bc > 0 else C["muted"]),
                (str(tq), "center", C["cyan"]   if tq > 0 else C["muted"]),
            ]
            for col_i, (val, anc, fg) in enumerate(cells):
                tk.Label(drow, text=val, anchor=anc,
                         font=FONT_SMALL, bg=bg_c, fg=fg,
                         padx=6, pady=7
                         ).grid(row=0, column=col_i, sticky="ew")

        make_button(self, "← Back", self.master.show_menu,
                    bg=C["accent2"], pad=(20, 8)).pack(pady=16)


# ══════════════════════════ ENTRY POINT ══════════════════════════════════════

if __name__ == "__main__":
    app = FlashcardApp()
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()