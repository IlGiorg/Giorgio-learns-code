"""
CS Flashcard Game - Extended Edition
A gamified flashcard learning app with Endless Mode improvements,
Speedrun Mode, expanded achievements, and enhanced database.
Built with Python 3, Tkinter, SQLite3
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import random
import math
import time
from datetime import datetime

# ─────────────────────────── ACHIEVEMENT DEFINITIONS ─────────────────────────

ACHIEVEMENTS = [
    # Progress Achievements
    ("First Steps", "Answer 10 cards", "🎯"),
    ("Learning Curve", "Answer 50 cards", "📘"),
    ("Knowledge Engine", "Answer 250 cards", "🧠"),
    ("Data Bank", "Answer 500 cards", "💾"),
    
    # Speed Achievements
    ("Lightning Brain", "5 answers in 30 seconds", "⚡"),
    ("Human Cache", "10 answers no reveal", "🧠"),
    ("CPU Overclocked", "20 streak", "🔥"),
    
    # Endless Mode Achievements
    ("Survivor", "Endless 15", "🛡"),
    ("Untouchable", "Endless 30", "💠"),
    ("Legend", "Endless 75", "👑"),
    
    # Risk Achievements
    ("Gambler", "Cash out with 1", "🎲"),
    ("Risk Taker", "Cash out 20+", "💰"),
    
    # Speedrun Achievements
    ("Blitz Master", "Speedrun 20", "⚡"),
    ("Marathon Runner", "Speedrun 100", "🏃"),
    ("Reflex God", "30 reflex", "⚡"),
    
    # Perfection Achievements
    ("Flawless", "Win no mistakes", "✨"),
    ("Memory Palace", "Win no reveal", "🏛"),
    
    # Fun Achievements
    ("Database Brain", "Learn all cards", "🗄"),
    ("Night Coder", "Play after midnight", "🌙"),
    ("Addicted", "5 games", "🎮"),
    
    # Bonus Achievements
    ("Stack Overflow", "404 answers", "💻"),
    ("Binary Master", "Endless 32", "010"),
    ("Root Access", "Unlock 10 badges", "🔑"),
    ("System Administrator", "Unlock 20 badges", "👑")
]

# ─────────────────────────── FLASHCARD DATA (EXPANDED) ───────────────────────

FLASHCARDS = {
    # Original 25 terms
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
    
    # A - Terms
    "ALU": "Arithmetic Logic Unit. Does all the maths",
    "ANALOGUE": "Smooth stream of data that our senses process",
    "ARQ": "Automatic Repeat Request. Acknowledgement is sent from the receiver to the sender to signal it has successfully received the packet. If it fails it will send a timeout error",
    "ASYMMETRIC ENCRYPTION": "A type of encryption that uses two different keys to encrypt and decrypt data",
    "AUTOMATED": "Processes that are performed by a computer without human intervention",
    "ACTUATOR": "A device that changes electrical signals into physical actions",
    "ARTIFICIAL INTELLIGENCE": "A part of computer science that looks at creating machines that can think and perform tasks a person would usually perform",
    "AI": "A part of computer science that looks at creating machines that can think and perform tasks a person would usually perform",
    
    # B - Terms
    "BINARY": "Base 2. Units increase to the power of 2",
    "BOOLEAN": "A data type. True or False",
    "PRIMARY KEY": "A unique identifier for a record",
    
    # C - Terms
    "CPU": "Central Processing Unit. Brain of the computer",
    "CONTROLLER": "Input device because inputs things and output because vibrates",
    "CAMERA": "Input. Can also be output if it has a screen on it to view photos",
    "COMPRESSION": "A method that uses an algorithm to reduce the size of a file",
    "CHECK DIGIT": "A method of error checking that adds up all the digits and divides by ten. Remainder is checkdigit",
    "CYPHER": "The name given to data after transmission",
    
    # D - Terms
    "DIGITAL": "Data represented in the values of 1 and 0 that a computer can understand",
    "DATA": "Numbers, symbols, raw format characters before processing",
    "DENARY": "Base 10. Units increase to the power of 10",
    "DICTIONARY": "A dictionary is a mutable, ordered collection of key valued pairs",
    "DATA PACKET": "A small unit of data",
    "PACKET": "A small unit of data",
    "PACKET SWITCHING": "A method of sending packets of information over a network",
    "DATA TRANSMISSION": "Sending and receiving information over a network",
    "DATABASE": "An example of application software to store and manipulate data",
    "DATA TYPE": "The characteristics of a piece of data. Common data types are string, integer, real and Boolean",
    "DIV": "The division operator. It gives the whole number part of a division calculation. E.g. 7 div 2 = 3",
    
    # E - Terms
    "ETHERNET": "Another type of connection that can be used to transmit data within a network",
    "ECHO CHECK": "A type of error detection method that sends the transmitted data back to the sender to be compared with the original data sent",
    "ENCRYPTION": "A method of securing data for storage or transmission that scrambles it and makes it meaningless",
    "ENCRYPTION KEY": "A type of algorithm",
    "EXPERT SYSTEM": "A computer program that uses a set of rules to provide advice or make decisions in a specific area",
    
    # F - Terms
    "FIELD": "An individual piece of data, e.g. date of birth",
    
    # G - Terms
    "GPU": "Graphics Processing Unit. Controls the video output",
    "AND": "Outputs 1 only if all inputs are 1, otherwise 0",
    "OR": "Output 1 if at least 1 input is 1",
    "NOT": "Input 1 becomes 0, input 0 becomes 1",
    "NAND": "Inverts inputs from AND",
    "NOR": "Inverts inputs from OR",
    "XOR": "If inputs are different outputs 1, otherwise 0",
    
    # H - Terms
    "HDD": "Hard Disk Drive. Non-Volatile. Secondary Memory",
    "HARDWARE": "Any physical part of a PC that you can touch",
    "HEADPHONES": "Output",
    
    # I - Terms
    "INPUT": "When a user enters information or data into a computer",
    "INFORMATION": "Data that has a context and can be interpreted with meaning",
    "IF": "Checks something",
    "LOGICAL OPERATOR": "A symbol that performs a comparison resulting in True or False. Can be equals, not equal to, less than, less than or equal to, greater than, greater than or equal to",
    "INFERENCE ENGINE": "The part of an expert system that applies the rules from the rule base to the facts in the knowledge base to deduce new facts or make decisions",
    
    # J - Terms
    "SQL": "A standard language used to define and manipulate databases",
    
    # K - Terms
    "KEYBOARD": "Input",
    "KNOWLEDGE BASE": "A collection of facts and rules used by an expert system",
    
    # L - Terms
    "LIGHT RING": "Output because gives light",
    "LOSSY": "A compression method that reduces the size of a file by permanently removing data",
    "LOSSLESS": "A compression method that reduces the size of a file by temporarily altering the data",
    "LIST": "A list is a mutable, ordered collection of elements. Lists are for ordered, changeable sequences",
    
    # M - Terms
    "MOTHERBOARD": "Main circuit board of a computer",
    "MONITOR": "Output because shows what's happening",
    "MICROPHONE": "Input because gets sound",
    "MICROPROCESSOR": "An integrated circuit that is able to perform the functions of a computer's central processing unit (CPU)",
    "MACHINE LEARNING": "A computer program that can adapt its stored rules or processes",
    "MOD": "The modulus operator. It gives the remainder part of a division calculation. E.g. 7 mod 2 = 1",
    
    # P - Terms
    "PAYLOAD": "The actual data the user is sending to the receiver",
    "TRAILER": "A section of a packet of data that contains information about any error checking methods that can be used",
    "PARITY CHECK": "A way of checking that the data being sent is correct. if 0100110 we make it 10100110",
    "PCHK ERROR": "When two bits are reversed which means that the parity check passes but the data received is wrong",
    
    # Q - Terms
    "SERIAL": "A transmission method where data is sent one bit at a time down a single wire",
    "PARALLEL": "A transmission method where data is sent multiple bits at a time down multiple wires",
    "INTERFERENCE": "Disruption, such as electromagnetism, to data when it is transmitted",
    "SIMPLEX": "A transmission method where data is transmitted in a single direction only",
    "DUPLEX": "A transmission method where data is transmitted in both directions, but only one direction at a time",
    "FULL DUPLEX": "A transmission method where data is transmitted in both directions at the same time",
    
    # R - Terms
    "RAM": "Random Access Memory. Volatile. Primary Memory",
    "ROM": "Read Only Memory. Non-Volatile. Primary Memory",
    "RECORD": "All of the information in a table about one object, e.g. all the personal details about one student",
    "ROBOT": "A machine that emulates human actions",
    "ROBOTICS": "The branch of technology that deals with the design, construction, operation, and application of robots",
    "RULE BASE": "A collection of rules used by an expert system",
    
    # S - Terms
    "STRING": "Strings are words, characters or symbols in quotation marks in Python",
    "SSD": "Solid State Drive. Store everything. Secondary Memory",
    "SOFTWARE": "Any programs, app functions etc. of a computer that you can't touch",
    "SENSOR": "Detects changes in the environment and sends the data to the computer",
    "SPEAKERS": "Output because makes sound",
    
    # T - Terms
    "TUPLE": "A tuple is an immutable, ordered collection of elements",
    "TABLE": "A set of data about one type of objects",
    
    # U - Terms
    "USB": "Universal Serial Bus. An industry standard that is used to transmit data",
    "USB PORT": "A socket that is part of a device or computer that enables you to insert a USB method",
    "USB CABLE": "A type of transmission media that uses the USB method to transmit data",
    "USB CONNECTION": "A collective name for using a USB cable plugged into a USB port to transfer data from one device to another",
    "USB DEVICE": "The name of a device that plugs into a USB port",
    
    # V - Terms
    "VR HEADSET": "Output Device for Virtual Reality",
    "VR": "Virtual Reality",
}

# ─────────────────────────── BADGE DEFINITIONS ───────────────────────────────

# Map achievements to badge definitions (keeping compatibility)
BADGE_DEFS = ACHIEVEMENTS.copy()

# Badge unlock dependencies
BADGE_DEPENDENCIES = {
    "Human Cache": ["First Steps"],
    "CPU Overclocked": ["Learning Curve"],
    "Legend": ["Survivor", "Untouchable"],
    "System Administrator": ["Root Access"],
    "Memory Palace": ["First Time"],
    "Flawless": ["First Time"],
}

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
    "orange":    "#ff8c00",
    "pink":      "#ff6b9d",
}

FONT_TITLE  = ("Segoe UI", 28, "bold")
FONT_LARGE  = ("Segoe UI", 18, "bold")
FONT_MED    = ("Segoe UI", 14)
FONT_SMALL  = ("Segoe UI", 11)
FONT_MONO   = ("Consolas", 13)

# ══════════════════════════ DATABASE MANAGER ═════════════════════════════════

class DatabaseManager:
    """Handles all SQLite operations with automatic schema migration."""

    def __init__(self, db_path="flashcard_game.db"):
        self.conn = sqlite3.connect(db_path)
        self._create_tables()
        self._migrate_schema()
        self._seed_badges()

    # ── Schema creation and migration ───────────────────────────────────────

    def _create_tables(self):
        """Create initial tables if they don't exist."""
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

    def _migrate_schema(self):
        """Add new columns and tables for extended features."""
        cur = self.conn.cursor()
        
        # Add new columns to users table if they don't exist
        new_columns = [
            ("total_correct", "INTEGER DEFAULT 0"),
            ("games_played", "INTEGER DEFAULT 0"),
            ("current_streak", "INTEGER DEFAULT 0"),
            ("longest_streak", "INTEGER DEFAULT 0"),
            ("questions_without_reveal", "INTEGER DEFAULT 0"),
            ("last_play_time", "TEXT"),
            ("speedrun_highscore", "INTEGER DEFAULT 0"),
            ("speedrun_unlocked", "INTEGER DEFAULT 0"),  # 0 = locked, 1 = unlocked
        ]
        
        # Get existing columns
        cur.execute("PRAGMA table_info(users)")
        existing_cols = [col[1] for col in cur.fetchall()]
        
        # Add missing columns
        for col_name, col_def in new_columns:
            if col_name not in existing_cols:
                try:
                    cur.execute(f"ALTER TABLE users ADD COLUMN {col_name} {col_def}")
                except sqlite3.OperationalError:
                    pass  # Column might already exist
        
        # Create game_history table if it doesn't exist
        cur.execute("""
            CREATE TABLE IF NOT EXISTS game_history (
                id                INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id           INTEGER NOT NULL,
                mode              TEXT NOT NULL,
                score             INTEGER DEFAULT 0,
                questions_answered INTEGER DEFAULT 0,
                timestamp         TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        
        self.conn.commit()

    def _seed_badges(self):
        """Insert all badge definitions."""
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
        cur.execute("""
            INSERT INTO users 
            (username, code, last_play_time) 
            VALUES (?,?,?)
        """, (username, code, datetime.now().isoformat()))
        self.conn.commit()

    def get_user(self, username):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=?", (username,))
        row = cur.fetchone()
        if row:
            # Get column names
            cur.execute("PRAGMA table_info(users)")
            columns = [col[1] for col in cur.fetchall()]
            return dict(zip(columns, row))
        return None

    def update_user_stats(self, user_id, correct=False, reveal_used=False):
        """Update user statistics after a question."""
        cur = self.conn.cursor()
        
        # Get current user data
        cur.execute("SELECT * FROM users WHERE id=?", (user_id,))
        user = cur.fetchone()
        if not user:
            return
        
        # Update stats
        updates = []
        params = []
        
        if correct:
            updates.append("total_correct = total_correct + 1")
            updates.append("current_streak = current_streak + 1")
            updates.append("longest_streak = MAX(longest_streak, current_streak)")
        else:
            updates.append("current_streak = 0")
        
        if not reveal_used:
            updates.append("questions_without_reveal = questions_without_reveal + 1")
        else:
            updates.append("questions_without_reveal = 0")
        
        updates.append("last_play_time = ?")
        params.append(datetime.now().isoformat())
        
        if updates:
            query = f"UPDATE users SET {', '.join(updates)} WHERE id=?"
            params.append(user_id)
            cur.execute(query, params)
        
        self.conn.commit()

    def increment_games_played(self, user_id):
        """Increment games played counter."""
        self.conn.execute(
            "UPDATE users SET games_played = games_played + 1 WHERE id=?",
            (user_id,)
        )
        self.conn.commit()

    def check_speedrun_unlock(self, user_id):
        """Check if speedrun mode should be unlocked (50 questions answered)."""
        cur = self.conn.cursor()
        cur.execute("SELECT total_answered, speedrun_unlocked FROM users WHERE id=?", (user_id,))
        row = cur.fetchone()
        if row:
            total_answered, unlocked = row
            if total_answered >= 50 and not unlocked:
                cur.execute("UPDATE users SET speedrun_unlocked = 1 WHERE id=?", (user_id,))
                self.conn.commit()
                return True
        return False

    def update_endless_highscore(self, user_id, score):
        self.conn.execute(
            "UPDATE users SET endless_highscore=? WHERE id=? AND endless_highscore<?",
            (score, user_id, score)
        )
        self.conn.commit()

    def update_speedrun_highscore(self, user_id, score):
        self.conn.execute(
            "UPDATE users SET speedrun_highscore=? WHERE id=? AND speedrun_highscore<?",
            (score, user_id, score)
        )
        self.conn.commit()

    def increment_total_answered(self, user_id, count=1):
        self.conn.execute(
            "UPDATE users SET total_answered = total_answered + ? WHERE id=?",
            (count, user_id)
        )
        self.conn.commit()

    def save_game_history(self, user_id, mode, score, questions_answered):
        """Save game result to history."""
        cur = self.conn.cursor()
        cur.execute("""
            INSERT INTO game_history (user_id, mode, score, questions_answered, timestamp)
            VALUES (?,?,?,?,?)
        """, (user_id, mode, score, questions_answered, datetime.now().isoformat()))
        self.conn.commit()

    # ── Badge helpers ────────────────────────────────────────────────────────

    def award_badge(self, user_id, badge_name):
        """Award a badge if dependencies are met."""
        cur = self.conn.cursor()
        
        # Check if badge exists
        cur.execute("SELECT id FROM badges WHERE badge_name=?", (badge_name,))
        row = cur.fetchone()
        if not row:
            return False
        badge_id = row[0]
        
        # Check dependencies
        if badge_name in BADGE_DEPENDENCIES:
            deps = BADGE_DEPENDENCIES[badge_name]
            for dep in deps:
                cur.execute("""
                    SELECT 1 FROM user_badges ub
                    JOIN badges b ON ub.badge_id = b.id
                    WHERE ub.user_id=? AND b.badge_name=?
                """, (user_id, dep))
                if not cur.fetchone():
                    return False  # Missing dependency
        
        # Check if already has it
        cur.execute("SELECT 1 FROM user_badges WHERE user_id=? AND badge_id=?",
                    (user_id, badge_id))
        if cur.fetchone():
            return False
        
        # Award badge
        cur.execute("INSERT INTO user_badges (user_id, badge_id) VALUES (?,?)",
                    (user_id, badge_id))
        self.conn.commit()
        
        # Check for Root Access and System Administrator
        self._check_badge_count_achievements(user_id)
        
        return True

    def _check_badge_count_achievements(self, user_id):
        """Check and award badge count achievements."""
        cur = self.conn.cursor()
        cur.execute("SELECT COUNT(*) FROM user_badges WHERE user_id=?", (user_id,))
        count = cur.fetchone()[0]
        
        if count >= 10:
            self.award_badge(user_id, "Root Access")
        if count >= 20:
            self.award_badge(user_id, "System Administrator")

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

    def check_progress_achievements(self, user_id):
        """Check and award progress-based achievements."""
        cur = self.conn.cursor()
        cur.execute("SELECT total_answered FROM users WHERE id=?", (user_id,))
        total = cur.fetchone()[0]
        
        if total >= 10:
            self.award_badge(user_id, "First Steps")
        if total >= 50:
            self.award_badge(user_id, "Learning Curve")
        if total >= 250:
            self.award_badge(user_id, "Knowledge Engine")
        if total >= 500:
            self.award_badge(user_id, "Data Bank")
        if total >= 404:
            self.award_badge(user_id, "Stack Overflow")

    # ── Leaderboard ──────────────────────────────────────────────────────────

    def get_leaderboard(self):
        """Get enhanced leaderboard with all stats."""
        cur = self.conn.cursor()
        cur.execute("""
            SELECT u.username, 
                   u.endless_highscore,
                   u.speedrun_highscore,
                   COUNT(ub.badge_id) AS badge_count,
                   u.total_answered
            FROM users u
            LEFT JOIN user_badges ub ON u.id = ub.user_id
            GROUP BY u.id
            ORDER BY u.endless_highscore DESC, u.total_answered DESC
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


class GlowEffect:
    """Creates a pulsing glow effect around a widget."""
    
    def __init__(self, widget, color=C["green"], size=10):
        self.widget = widget
        self.color = color
        self.size = size
        self.direction = 1
        self.current = size
        self._pulse()

    def _pulse(self):
        self.current += self.direction * 2
        if self.current > self.size * 2 or self.current < self.size:
            self.direction *= -1
        self.widget.config(bd=self.current, relief="solid", highlightbackground=self.color)
        self.widget.after(50, self._pulse)


# ══════════════════════════ MAIN APPLICATION ═════════════════════════════════

class FlashcardApp(tk.Tk):
    """Root window – acts as the screen manager."""

    def __init__(self):
        super().__init__()
        self.title("CS Flashcard Game - Extended Edition")
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
        self._consecutive_games = 0  # Track for Addicted achievement

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

    def show_speedrun_menu(self):
        # Check if speedrun is unlocked
        if self.user and self.user.get("speedrun_unlocked", 0):
            self.show_frame(SpeedrunMenuScreen)
        else:
            self.show_frame(SpeedrunLockedScreen)

    def show_speedrun_mode(self, mode_type):
        """Show speedrun mode with specific variant."""
        self.show_frame(SpeedrunModeScreen, mode_type=mode_type)

    def show_rewards(self):
        self.show_frame(RewardsScreen)

    def show_leaderboard(self):
        self.show_frame(LeaderboardScreen)

    def check_night_coder(self):
        """Check if playing after midnight."""
        now = datetime.now()
        if now.hour >= 0 and now.hour < 5:  # After midnight
            self.db.award_badge(self.user["id"], "Night Coder")

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
        
        stats_text = f"Endless: {user['endless_highscore']}  |  Speedrun: {user.get('speedrun_highscore', 0)}  |  Total Q: {user['total_answered']}"
        make_label(self, stats_text,
                   font=FONT_SMALL, fg=C["yellow"]).pack(pady=(0, 30))

        # Check if speedrun is unlocked
        speedrun_unlocked = user.get("speedrun_unlocked", 0)
        speedrun_text = "⚡  Speedrun Mode" if speedrun_unlocked else "⚡  Speedrun Mode [LOCKED]"
        speedrun_color = C["orange"] if speedrun_unlocked else C["muted"]
        speedrun_cmd = self.master.show_speedrun_menu if speedrun_unlocked else lambda: None

        btn_cfg = [
            ("▶  Play Normal Mode",  C["accent"],  self.master.show_normal_mode),
            ("♾  Endless Mode",      C["purple"],  self.master.show_endless_mode),
            (speedrun_text,          speedrun_color, speedrun_cmd),
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


# ══════════════════════════ SPEEDRUN LOCKED SCREEN ═══════════════════════════

class SpeedrunLockedScreen(tk.Frame):

    def __init__(self, master):
        super().__init__(master, bg=C["bg"])
        self._build()

    def _build(self):
        make_label(self, "🔒  Speedrun Mode Locked",
                   font=FONT_TITLE, fg=C["muted"]).pack(pady=(100, 20))
        
        user = self.master.user
        total = user['total_answered']
        needed = max(0, 50 - total)
        
        make_label(self, f"You need to answer 50 questions to unlock Speedrun Mode.",
                   font=FONT_LARGE, fg=C["text"]).pack(pady=10)
        make_label(self, f"You've answered: {total} questions",
                   font=FONT_MED, fg=C["yellow"]).pack(pady=5)
        make_label(self, f"Questions remaining: {needed}",
                   font=FONT_MED, fg=C["cyan"] if needed > 0 else C["green"]).pack(pady=5)
        
        make_button(self, "▶  Play Normal Mode", self.master.show_normal_mode,
                    bg=C["accent"], font=FONT_LARGE, pad=(30, 12)).pack(pady=30)
        make_button(self, "← Back to Menu", self.master.show_menu,
                    bg=C["accent2"], pad=(20, 8)).pack()


# ══════════════════════════ SPEEDRUN MENU SCREEN ════════════════════════════

class SpeedrunMenuScreen(tk.Frame):

    def __init__(self, master):
        super().__init__(master, bg=C["bg"])
        self._build()

    def _build(self):
        make_label(self, "⚡  Speedrun Mode",
                   font=FONT_TITLE, fg=C["orange"]).pack(pady=(40, 20))

        make_label(self, "Choose your challenge:",
                   font=FONT_LARGE, fg=C["text"]).pack(pady=(0, 30))

        modes = [
            ("⏱️  60 Seconds Chaos", "60s", "Answer as many as possible in 60 seconds"),
            ("🏃  Marathon (10 min)", "marathon", "Long challenge – 10 minutes"),
            ("🎯  Reflex Mode", "reflex", "10 seconds per question – timer resets"),
        ]

        for title, mode_id, desc in modes:
            panel = tk.Frame(self, bg=C["card"], padx=30, pady=15)
            panel.pack(pady=10, fill="x", padx=100)

            make_label(panel, title, font=FONT_LARGE, 
                       fg=C["orange"], bg=C["card"]).pack()
            make_label(panel, desc, font=FONT_SMALL,
                       fg=C["muted"], bg=C["card"]).pack()

            make_button(panel, "Select →", 
                       lambda m=mode_id: self.master.show_speedrun_mode(m),
                       bg=C["orange"], pad=(20, 5)).pack(pady=(10, 0))

        make_button(self, "← Back to Menu", self.master.show_menu,
                    bg=C["accent2"], pad=(20, 8)).pack(pady=30)


# ══════════════════════════ BASE GAME SCREEN ════════════════════════════════

class BaseGameScreen(tk.Frame):
    """Shared logic for all game modes."""

    def __init__(self, master, mode):
        super().__init__(master, bg=C["bg"])
        self.mode      = mode          # "normal", "endless", "speedrun"
        self.score     = 0
        self.questions = 0             # cards answered
        self.correct_streak = 0
        self._anim_score = 0           # displayed score (animated)
        self._deck  = list(FLASHCARDS.keys())
        random.shuffle(self._deck)
        self._deck_idx  = 0
        self._revealed  = False
        self._reveal_used = False
        self._start_time = time.time()
        self._build_ui()
        self._next_card()

    # ── UI construction ──────────────────────────────────────────────────────

    def _build_ui(self):
        top = tk.Frame(self, bg=C["bg"])
        top.pack(fill="x", padx=20, pady=10)

        make_button(top, "← Menu", self._back_to_menu,
                    bg=C["accent2"], font=FONT_SMALL, pad=(10, 5)).pack(side="left")

        title = self._get_title()
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
        self.wrong_btn   = make_button(btn_row, self._wrong_text(),
                                       lambda: self._answer(False),
                                       bg=C["accent"], font=FONT_LARGE,
                                       pad=(20, 12))
        self.correct_btn.pack_forget()
        self.wrong_btn.pack_forget()

        # Question counter
        self.q_lbl = make_label(self, "Questions answered: 0",
                                font=FONT_SMALL, fg=C["muted"])
        self.q_lbl.pack()

        # Endless mode cash out button
        if self.mode == "endless":
            self.cashout_btn = make_button(self, "💾 Cash Out", self._cash_out,
                                          bg=C["green"], font=FONT_LARGE,
                                          pad=(20, 8))
            self.cashout_btn.pack(pady=5)
            # Add glow effect
            self._glow = GlowEffect(self.cashout_btn, color=C["green"])

    def _get_title(self):
        if self.mode == "normal":
            return "Normal Mode  (reach 11 pts)"
        elif self.mode == "endless":
            return "Endless Mode  (Cash out anytime)"
        return "Speedrun Mode"

    def _wrong_text(self):
        if self.mode == "normal":
            return "❌ Wrong  -2"
        return "❌ Wrong"

    def _draw_card_bg(self):
        self.canvas.create_rectangle(10, 10, 850, 290,
                                     fill=C["card"], outline=C["accent2"],
                                     width=2)

    # ── Card logic ───────────────────────────────────────────────────────────

    def _next_card(self):
        self._revealed = False
        self._reveal_used = False
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
        self._reveal_used = True
        ans = FLASHCARDS[self._current_term]
        self.canvas.itemconfig(self.ans_text, text=ans)
        self.reveal_btn.pack_forget()
        self.correct_btn.pack(side="left", padx=10)
        self.wrong_btn.pack(side="left", padx=10)

    def _answer(self, correct):
        self.questions += 1
        self.q_lbl.config(text=f"Questions answered: {self.questions}")
        
        # Update user stats in database
        db = self.master.db
        uid = self.master.user["id"]
        
        if correct:
            self.score += 1
            self.correct_streak += 1
            self._animate_score_change("+1", C["green"])
            db.update_user_stats(uid, correct=True, reveal_used=self._reveal_used)
            
            # Check for streak achievements
            if self.correct_streak >= 20:
                db.award_badge(uid, "CPU Overclocked")
        else:
            self.correct_streak = 0
            self._on_wrong()
            db.update_user_stats(uid, correct=False, reveal_used=self._reveal_used)
            return
            
        self._update_score_display()
        
        # Check for achievements
        if not self._reveal_used and self.questions == 10:
            db.award_badge(uid, "Human Cache")
        
        if self.questions == 5 and (time.time() - self._start_time) < 30:
            db.award_badge(uid, "Lightning Brain")
        
        self._check_win()
        self._next_card()

    def _on_wrong(self):
        """Override in subclasses."""
        pass

    def _cash_out(self):
        """Cash out in endless mode."""
        if self.mode != "endless":
            return
        
        db = self.master.db
        uid = self.master.user["id"]
        prev = self.master.user["endless_highscore"]
        
        # Check for risk achievements
        if self.score == 1:
            db.award_badge(uid, "Gambler")
        if self.score >= 20:
            db.award_badge(uid, "Risk Taker")
        
        # Save game history
        db.save_game_history(uid, "endless_cashout", self.score, self.questions)
        db.increment_total_answered(uid, self.questions)
        db.increment_games_played(uid)
        
        # Check high score
        new_hs = self.score > prev
        if new_hs:
            db.update_endless_highscore(uid, self.score)
            self.master.user["endless_highscore"] = self.score
        
        self.master._consecutive_games += 1
        if self.master._consecutive_games >= 5:
            db.award_badge(uid, "Addicted")
        
        self.after(100, lambda: self.master.show_frame(
            EndlessResultScreen, score=self.score,
            prev_hs=prev, new_hs=new_hs, cashout=True
        ))

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
        # Update consecutive games counter
        self.master._consecutive_games = 0
        self.master.show_menu()


# ══════════════════════════ NORMAL MODE ═════════════════════════════════════

class NormalModeScreen(BaseGameScreen):

    def __init__(self, master):
        super().__init__(master, "normal")
        self._mistakes = 0
        self._no_reveal = True

    def _on_wrong(self):
        self.score = max(0, self.score - 2)
        self._mistakes += 1
        self._animate_score_change("−2", C["accent"])
        self._update_score_display(wrong=True)
        self.after(400, self._next_card)   # small delay so animation is visible

    def _reveal(self):
        super()._reveal()
        self._no_reveal = False

    def _check_win(self):
        if self.score >= 11:
            db  = self.master.db
            uid = self.master.user["id"]
            db.increment_total_answered(uid, self.questions)
            db.increment_games_played(uid)
            
            # Save game history
            db.save_game_history(uid, "normal", self.score, self.questions)
            
            # Award badges
            new_badges = []
            if db.award_badge(uid, "First Time"):
                new_badges.append("First Time")
            if self.questions < 15 and db.award_badge(uid, "Fast Learner"):
                new_badges.append("Fast Learner")
            if self._mistakes == 0 and db.award_badge(uid, "Flawless"):
                new_badges.append("Flawless")
            if self._no_reveal and db.award_badge(uid, "Memory Palace"):
                new_badges.append("Memory Palace")
            
            self._check_flash_master()
            db.check_progress_achievements(uid)
            
            # Check for speedrun unlock
            unlocked = db.check_speedrun_unlock(uid)
            if unlocked:
                self.master.user["speedrun_unlocked"] = 1
            
            # Check for Database Brain (learn all flashcards in one session)
            if self.questions >= len(FLASHCARDS):
                db.award_badge(uid, "Database Brain")
            
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
        # Wrong answer ends the game
        self._end_game()

    def _end_game(self):
        """End the endless run (from wrong answer or cash out)."""
        db   = self.master.db
        uid  = self.master.user["id"]
        prev = self.master.user["endless_highscore"]
        
        db.increment_total_answered(uid, self.questions)
        db.increment_games_played(uid)
        db.save_game_history(uid, "endless", self.score, self.questions)
        
        self._check_endless_badges()
        
        new_hs = self.score > prev
        if new_hs:
            db.update_endless_highscore(uid, self.score)
            self.master.user["endless_highscore"] = self.score
        
        self.master._consecutive_games += 1
        if self.master._consecutive_games >= 5:
            db.award_badge(uid, "Addicted")
        
        self.after(100, lambda: self.master.show_frame(
            EndlessResultScreen, score=self.score,
            prev_hs=prev, new_hs=new_hs, cashout=False
        ))

    def _cash_out(self):
        """Override cash out to end game properly."""
        self._end_game()

    def _check_endless_badges(self):
        db  = self.master.db
        uid = self.master.user["id"]
        
        # Score-based badges
        if self.score >= 10:
            db.award_badge(uid, "Endless 10")
        if self.score >= 15:
            db.award_badge(uid, "Survivor")
        if self.score >= 25:
            db.award_badge(uid, "Endless 25")
        if self.score >= 30:
            db.award_badge(uid, "Untouchable")
        if self.score >= 32:
            db.award_badge(uid, "Binary Master")
        if self.score >= 50:
            db.award_badge(uid, "Endless 50")
        if self.score >= 75:
            db.award_badge(uid, "Legend")
        
        user = db.get_user(self.master.user["username"])
        if user["total_answered"] >= 100:
            db.award_badge(uid, "Flash Master")


# ══════════════════════════ SPEEDRUN MODE ═══════════════════════════════════

class SpeedrunModeScreen(BaseGameScreen):

    def __init__(self, master, mode_type):
        self.speedrun_type = mode_type  # "60s", "marathon", "reflex"
        super().__init__(master, "speedrun")
        
        # Timer setup
        self.timer_running = True
        self.time_left = self._get_initial_time()
        self._timer_update()

    def _get_initial_time(self):
        if self.speedrun_type == "60s":
            return 60
        elif self.speedrun_type == "marathon":
            return 600
        else:  # reflex
            return 10

    def _build_ui(self):
        super()._build_ui()
        
        # Add timer display
        timer_frame = tk.Frame(self, bg=C["bg"])
        timer_frame.pack(pady=5)
        
        make_label(timer_frame, "⏱️  Time Left:", 
                  font=FONT_MED, fg=C["cyan"], bg=C["bg"]).pack(side="left")
        
        self.timer_lbl = make_label(timer_frame, self._format_time(self.time_left),
                                   font=("Digital", 24, "bold"), fg=C["green"], bg=C["bg"])
        self.timer_lbl.pack(side="left", padx=10)
        
        # Store original color for flashing
        self.timer_original_color = C["green"]

    def _format_time(self, seconds):
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins:02d}:{secs:02d}"

    def _timer_update(self):
        if not self.timer_running:
            return
            
        self.time_left -= 1
        
        # Flash when low on time
        if self.time_left < 10:
            color = C["accent"] if int(time.time() * 2) % 2 == 0 else C["green"]
            self.timer_lbl.config(fg=color)
        else:
            self.timer_lbl.config(fg=C["green"])
        
        self.timer_lbl.config(text=self._format_time(max(0, self.time_left)))
        
        if self.time_left <= 0:
            self._end_game()
        else:
            self.after(1000, self._timer_update)

    def _answer(self, correct):
        super()._answer(correct)
        
        # Reset timer for reflex mode
        if self.speedrun_type == "reflex" and correct:
            self.time_left = 10

    def _on_wrong(self):
        # No penalty for wrong answers in speedrun, just move on
        self._next_card()

    def _end_game(self):
        self.timer_running = False
        
        db = self.master.db
        uid = self.master.user["id"]
        
        # Save game history
        db.save_game_history(uid, f"speedrun_{self.speedrun_type}", self.score, self.questions)
        db.increment_total_answered(uid, self.questions)
        db.increment_games_played(uid)
        
        # Update high score
        prev = self.master.user.get("speedrun_highscore", 0)
        if self.score > prev:
            db.update_speedrun_highscore(uid, self.score)
            self.master.user["speedrun_highscore"] = self.score
        
        # Check for speedrun achievements
        if self.speedrun_type == "60s" and self.score >= 20:
            db.award_badge(uid, "Blitz Master")
        elif self.speedrun_type == "marathon" and self.score >= 100:
            db.award_badge(uid, "Marathon Runner")
        elif self.speedrun_type == "reflex" and self.questions >= 30:
            db.award_badge(uid, "Reflex God")
        
        # Check progress achievements
        db.check_progress_achievements(uid)
        
        self.master._consecutive_games += 1
        if self.master._consecutive_games >= 5:
            db.award_badge(uid, "Addicted")
        
        self.after(100, lambda: self.master.show_frame(
            SpeedrunResultScreen, score=self.score,
            mode_type=self.speedrun_type, questions=self.questions
        ))

    def _back_to_menu(self):
        self.timer_running = False
        super()._back_to_menu()


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
                # Find icon for badge
                icon = "🏅"
                for name, _, ico in BADGE_DEFS:
                    if name == b:
                        icon = ico
                        break
                badge_item = self.canvas.create_text(450, y,
                                                    text=f"{icon}  {b}",
                                                    fill=C["yellow"],
                                                    font=("Segoe UI", 18, "bold"))
                y += 36
                
                # Pop animation for badge
                self._pop_animation(badge_item, y-36)

        # Buttons
        btn_frame = tk.Frame(self.canvas, bg=C["bg"])
        self.canvas.create_window(450, 580, window=btn_frame)
        make_button(btn_frame, "▶ Play Again", self.master.show_normal_mode,
                    bg=C["green"], pad=(20, 10)).pack(side="left", padx=10)
        make_button(btn_frame, "🏠 Main Menu", self.master.show_menu,
                    bg=C["accent2"], pad=(20, 10)).pack(side="left", padx=10)

    def _pop_animation(self, item, y, scale=1.0):
        """Pop animation for badge."""
        if scale > 1.2:
            self.canvas.itemconfig(item, font=("Segoe UI", 18, "bold"))
            return
        self.canvas.itemconfig(item, font=("Segoe UI", int(18 * scale), "bold"))
        self.after(30, lambda: self._pop_animation(item, y, scale + 0.1))


# ══════════════════════════ ENDLESS RESULT SCREEN ═══════════════════════════

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
        W, H = 900, 650
        self.canvas = tk.Canvas(self, width=W, height=H,
                                bg=C["bg"], highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self._confetti = ConfettiCanvas(self.canvas, W, H)

        msg = "💰 CASH OUT SUCCESS!" if self.cashout else "🔥 NEW HIGH SCORE! 🔥"
        self.canvas.create_text(450, 180, text=msg,
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
        make_button(btn_frame, "⚡ Speedrun", self.master.show_speedrun_menu,
                    bg=C["orange"], pad=(20, 10)).pack(side="left", padx=10)
        make_button(btn_frame, "🏠 Menu", self.master.show_menu,
                    bg=C["accent2"], pad=(20, 10)).pack(side="left", padx=10)

    def _count_up(self):
        if self._displayed < self.score:
            step = max(1, (self.score - self._displayed) // 8)
            self._displayed = min(self._displayed + step, self.score)
            self.canvas.itemconfig(self._hs_text, text=str(self._displayed))
            self.after(40, self._count_up)

    def _build_normal(self):
        cashout_msg = "Cash Out Complete!" if self.cashout else "Game Over"
        make_label(self, cashout_msg, font=("Segoe UI", 36, "bold"),
                   fg=C["accent"] if not self.cashout else C["green"]).pack(pady=(80, 10))
        make_label(self, f"Your score: {self.score}",
                   font=FONT_LARGE, fg=C["text"]).pack(pady=6)
        make_label(self, f"High Score: {self.prev_hs}",
                   font=FONT_MED, fg=C["muted"]).pack(pady=6)

        row = tk.Frame(self, bg=C["bg"])
        row.pack(pady=30)
        make_button(row, "▶ Play Again", self.master.show_endless_mode,
                    bg=C["purple"], pad=(20, 10)).pack(side="left", padx=10)
        make_button(row, "⚡ Speedrun", self.master.show_speedrun_menu,
                    bg=C["orange"], pad=(20, 10)).pack(side="left", padx=10)
        make_button(row, "🏠 Menu", self.master.show_menu,
                    bg=C["accent2"], pad=(20, 10)).pack(side="left", padx=10)


# ══════════════════════════ SPEEDRUN RESULT SCREEN ══════════════════════════

class SpeedrunResultScreen(tk.Frame):

    def __init__(self, master, score, mode_type, questions):
        super().__init__(master, bg=C["bg"])
        self.score = score
        self.mode_type = mode_type
        self.questions = questions
        
        mode_names = {
            "60s": "60 Seconds Chaos",
            "marathon": "Marathon",
            "reflex": "Reflex Mode"
        }
        self.mode_name = mode_names.get(mode_type, "Speedrun")
        self._build()

    def _build(self):
        make_label(self, f"⚡ {self.mode_name} Complete!",
                   font=("Segoe UI", 36, "bold"),
                   fg=C["orange"]).pack(pady=(80, 10))
        make_label(self, f"Score: {self.score}",
                   font=FONT_LARGE, fg=C["yellow"]).pack(pady=6)
        make_label(self, f"Questions: {self.questions}",
                   font=FONT_MED, fg=C["text"]).pack(pady=6)

        # Get high score
        hs = self.master.user.get("speedrun_highscore", 0)
        if self.score > hs:
            make_label(self, "🏆 NEW HIGH SCORE! 🏆",
                       font=FONT_LARGE, fg=C["green"]).pack(pady=6)

        row = tk.Frame(self, bg=C["bg"])
        row.pack(pady=30)
        make_button(row, "▶ Play Again", 
                   lambda: self.master.show_speedrun_mode(self.mode_type),
                   bg=C["orange"], pad=(20, 10)).pack(side="left", padx=10)
        make_button(row, "⚡ Other Modes", self.master.show_speedrun_menu,
                    bg=C["accent2"], pad=(20, 10)).pack(side="left", padx=10)
        make_button(row, "🏠 Menu", self.master.show_menu,
                    bg=C["purple"], pad=(20, 10)).pack(side="left", padx=10)


# ══════════════════════════ REWARDS SCREEN ══════════════════════════════════

class RewardsScreen(tk.Frame):

    def __init__(self, master):
        super().__init__(master, bg=C["bg"])
        self._build()

    def _build(self):
        # Title
        title_frame = tk.Frame(self, bg=C["bg"])
        title_frame.pack(pady=(30, 10))
        
        make_label(title_frame, "🏅  Badges & Rewards",
                   font=FONT_TITLE, fg=C["yellow"]).pack()

        db       = self.master.db
        uid      = self.master.user["id"]
        earned   = db.get_user_badge_names(uid)
        all_b    = db.get_all_badges()
        
        # Stats bar
        stats_frame = tk.Frame(self, bg=C["panel"], pady=10, padx=20)
        stats_frame.pack(pady=(0, 20), padx=40, fill="x")
        
        # Total questions answered counter
        total_q = self.master.user["total_answered"]
        badge_count = len(earned)
        
        stats_left = tk.Frame(stats_frame, bg=C["panel"])
        stats_left.pack(side="left", expand=True)
        make_label(stats_left, f"Total Questions: {total_q}",
                  font=FONT_LARGE, fg=C["cyan"], bg=C["panel"]).pack()
        
        stats_right = tk.Frame(stats_frame, bg=C["panel"])
        stats_right.pack(side="right", expand=True)
        make_label(stats_right, f"Badges: {badge_count} / {len(all_b)}",
                  font=FONT_LARGE, fg=C["yellow"], bg=C["panel"]).pack()

        # Create main container with scrollbar
        main_container = tk.Frame(self, bg=C["bg"])
        main_container.pack(fill="both", expand=True, padx=40)

        # Canvas for scrolling
        canvas = tk.Canvas(main_container, bg=C["bg"], highlightthickness=0)
        scrollbar = tk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        
        # Frame inside canvas for content
        scrollable_frame = tk.Frame(canvas, bg=C["bg"])
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=canvas.winfo_width())
        canvas.configure(yscrollcommand=scrollbar.set)

        # Group badges by category using achievement list
        categories = {
            "Progress": ["First Steps", "Learning Curve", "Knowledge Engine", "Data Bank"],
            "Speed": ["Lightning Brain", "Human Cache", "CPU Overclocked"],
            "Endless": ["Survivor", "Untouchable", "Legend", "Endless 10", "Endless 25", "Endless 50"],
            "Risk": ["Gambler", "Risk Taker"],
            "Speedrun": ["Blitz Master", "Marathon Runner", "Reflex God"],
            "Perfection": ["Flawless", "Memory Palace"],
            "Fun": ["Database Brain", "Night Coder", "Addicted"],
            "Bonus": ["Stack Overflow", "Binary Master", "Root Access", "System Administrator"],
            "Original": ["First Time", "Fast Learner", "Flash Master"]
        }

        # Create grid layout (3 columns)
        for category, badge_list in categories.items():
            # Category header spanning all columns
            cat_header = tk.Frame(scrollable_frame, bg=C["accent2"], height=30)
            cat_header.pack(fill="x", pady=(15, 5))
            cat_header.pack_propagate(False)
            
            make_label(cat_header, f"📁 {category}", 
                      font=("Segoe UI", 14, "bold"), 
                      fg=C["white"], bg=C["accent2"]).pack(expand=True)

            # Create frame for badges in this category (grid)
            badges_frame = tk.Frame(scrollable_frame, bg=C["bg"])
            badges_frame.pack(fill="x", pady=5)

            # Filter badges in this category
            category_badges = [(name, desc, icon) for name, desc, icon in all_b if name in badge_list]
            
            # Display in grid (3 columns)
            for i, (name, desc, icon) in enumerate(category_badges):
                unlocked = name in earned
                
                # Create badge card
                card = tk.Frame(badges_frame, bg=C["card"] if unlocked else "#2a2a3a", 
                               relief="flat", bd=1, padx=10, pady=8)
                card.grid(row=i//3, column=i%3, padx=5, pady=5, sticky="nsew")
                
                # Configure grid weights
                badges_frame.grid_columnconfigure(0, weight=1)
                badges_frame.grid_columnconfigure(1, weight=1)
                badges_frame.grid_columnconfigure(2, weight=1)
                
                # Icon
                icon_label = tk.Label(card,
                                     text=icon if unlocked else "🔒",
                                     font=("Segoe UI", 24),
                                     bg=card["bg"],
                                     fg=C["yellow"] if unlocked else C["muted"])
                icon_label.pack(pady=(0, 2))
                
                # Name
                name_label = tk.Label(card, text=name,
                                     font=("Segoe UI", 10, "bold"),
                                     bg=card["bg"],
                                     fg=C["text"] if unlocked else C["muted"],
                                     wraplength=120)
                name_label.pack()
                
                # Description
                desc_label = tk.Label(card, text=desc,
                                     font=FONT_SMALL,
                                     bg=card["bg"],
                                     fg=C["muted"],
                                     wraplength=120)
                desc_label.pack()
                
                # Status
                status = "✓" if unlocked else "🔒"
                status_label = tk.Label(card, text=status,
                                       font=("Segoe UI", 12),
                                       bg=card["bg"],
                                       fg=C["green"] if unlocked else C["muted"])
                status_label.pack(pady=(2, 0))

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Back button
        make_button(self, "← Back to Menu", self.master.show_menu,
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

        # Create main container
        main_container = tk.Frame(self, bg=C["bg"])
        main_container.pack(fill="both", expand=True, padx=40)

        # Canvas for scrolling
        canvas = tk.Canvas(main_container, bg=C["bg"], highlightthickness=0)
        scrollbar = tk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        
        # Frame inside canvas for content
        scrollable_frame = tk.Frame(canvas, bg=C["bg"])
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=canvas.winfo_width())
        canvas.configure(yscrollcommand=scrollbar.set)

        # Header
        headers = ["Rank", "Username", "Endless", "Speedrun", "Badges", "Total Q"]
        widths  = [6, 16, 8, 8, 8, 10]
        
        hrow = tk.Frame(scrollable_frame, bg=C["accent2"])
        hrow.pack(fill="x", pady=(0, 5))
        for h, w in zip(headers, widths):
            tk.Label(hrow, text=h, width=w, font=("Segoe UI", 11, "bold"),
                     bg=C["accent2"], fg=C["white"], pady=8).pack(side="left", padx=2)

        # Data rows
        for i, (uname, hs, sp, bc, tq) in enumerate(rows, 1):
            # Medal icons for top 3
            if i == 1:
                medal = "🥇"
                medal_color = C["yellow"]
            elif i == 2:
                medal = "🥈"
                medal_color = C["muted"]
            elif i == 3:
                medal = "🥉"
                medal_color = "#cd7f32"  # bronze
            else:
                medal = f"#{i}"
                medal_color = C["text"]
            
            bg_c  = C["card"] if i % 2 == 0 else C["panel"]
            drow  = tk.Frame(scrollable_frame, bg=bg_c)
            drow.pack(fill="x", pady=1)
            
            # Rank with medal
            rank_label = tk.Label(drow, text=medal, width=widths[0],
                                 font=FONT_SMALL, bg=bg_c,
                                 fg=medal_color, pady=6)
            rank_label.pack(side="left", padx=2)
            
            # Username
            tk.Label(drow, text=uname, width=widths[1],
                     font=FONT_SMALL, bg=bg_c,
                     fg=C["yellow"] if i <= 3 else C["text"],
                     pady=6).pack(side="left", padx=2)
            
            # Endless high score
            tk.Label(drow, text=str(hs), width=widths[2],
                     font=FONT_SMALL, bg=bg_c,
                     fg=C["green"] if hs > 0 else C["muted"],
                     pady=6).pack(side="left", padx=2)
            
            # Speedrun high score
            tk.Label(drow, text=str(sp), width=widths[3],
                     font=FONT_SMALL, bg=bg_c,
                     fg=C["orange"] if sp > 0 else C["muted"],
                     pady=6).pack(side="left", padx=2)
            
            # Badge count
            tk.Label(drow, text=str(bc), width=widths[4],
                     font=FONT_SMALL, bg=bg_c,
                     fg=C["yellow"] if bc > 0 else C["muted"],
                     pady=6).pack(side="left", padx=2)
            
            # Total questions
            tk.Label(drow, text=str(tq), width=widths[5],
                     font=FONT_SMALL, bg=bg_c,
                     fg=C["cyan"] if tq > 0 else C["muted"],
                     pady=6).pack(side="left", padx=2)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        make_button(self, "← Back", self.master.show_menu,
                    bg=C["accent2"], pad=(20, 8)).pack(pady=20)


# ══════════════════════════ ENTRY POINT ═════════════════════════════════════

if __name__ == "__main__":
    app = FlashcardApp()
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()