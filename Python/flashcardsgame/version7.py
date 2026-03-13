"""
CS Flashcard Game — Extended Edition v2.0
Features: Multiplayer Duel, Daily Challenge, Performance Heatmap,
          Learning Curve Graph, Weak Spots, Power-Ups Shop,
          Daily Quests, Time Warp Mode, 40+ new achievements, bug fixes.
Built with Python 3, Tkinter, SQLite3
"""

import tkinter as tk
from tkinter import ttk
import sqlite3
import random
import math
import time
from datetime import datetime, date, timedelta
import json
import struct
import wave
import io
import threading
import os
import sys

# ─────────────────────────── ACHIEVEMENT DEFINITIONS ─────────────────────────

ACHIEVEMENTS = [
    # Progress
    ("First Steps",          "Answer 10 cards",                    "🎯"),
    ("Learning Curve",       "Answer 50 cards",                    "📘"),
    ("Knowledge Engine",     "Answer 250 cards",                   "🧠"),
    ("Data Bank",            "Answer 500 cards",                   "💾"),
    # Speed
    ("Lightning Brain",      "5 answers in 30 seconds",            "⚡"),
    ("Human Cache",          "10 answers no reveal",               "💡"),
    ("CPU Overclocked",      "20 correct streak",                  "🔥"),
    # Endless
    ("Survivor",             "Reach score 15 in Endless",          "🛡"),
    ("Untouchable",          "Reach score 30 in Endless",          "💠"),
    ("Legend",               "Reach score 75 in Endless",          "👑"),
    # Risk
    ("Gambler",              "Cash out with score 1",              "🎲"),
    ("Risk Taker",           "Cash out with score 20+",            "💰"),
    # Speedrun
    ("Blitz Master",         "Score 20 in 60s mode",               "⚡"),
    ("Marathon Runner",      "Score 100 in Marathon",              "🏃"),
    ("Reflex God",           "Survive 30 Reflex Qs",               "🎯"),
    # Perfection
    ("Flawless",             "Win Normal with no mistakes",        "✨"),
    ("Memory Palace",        "Win Normal without reveal",          "🏛"),
    # Fun
    ("Database Brain",       "See all cards in a session",         "🗄"),
    ("Night Coder",          "Play after midnight",                "🌙"),
    ("Addicted",             "5 consecutive games",               "🎮"),
    # Bonus
    ("Stack Overflow",       "Answer 404 questions total",         "💻"),
    ("Binary Master",        "Reach score 32 in Endless",          "🔢"),
    ("Root Access",          "Unlock 10 badges",                   "🔑"),
    ("System Administrator", "Unlock 20 badges",                   "👨‍💻"),
    # Original
    ("First Time",           "Win Normal Mode once",               "🏆"),
    ("Fast Learner",         "Win in under 15 questions",          "⚡"),
    ("Endless 10",           "Score 10+ in Endless",              "🔥"),
    ("Endless 25",           "Score 25+ in Endless",              "💎"),
    ("Endless 50",           "Score 50+ in Endless",              "👑"),
    ("Flash Master",         "Answer 100 cards total",             "🎓"),
    # ── NEW: Skill-Based ────────────────────────────────────────────────────
    ("Triple Threat",        "Win all 3 modes in one session",     "🔱"),
    ("Bullseye",             "Win Normal with 100% accuracy",      "🎯"),
    ("Puzzle Master",        "30 unique cards in one session",     "🧩"),
    # ── NEW: Progression ────────────────────────────────────────────────────
    ("Diamond Hands",        "Cash out Endless with 100+ points",  "💎"),
    # ── NEW: Fun & Hidden ───────────────────────────────────────────────────
    ("Owl",                  "Play between 3:00–4:00 AM",          "🦉"),
    ("Wizard",               "Complete any mode without Reveal",   "🧙"),
    ("Nostalgia",            "Play any game on a Tuesday",         "📅"),
    ("Tortoise",             "Spend 120s+ on a single card",       "🐢"),
    ("Hare",                 "Answer 3 cards in under 10 seconds", "🐇"),
    # ── NEW: Mode-Specific ──────────────────────────────────────────────────
    ("Lightning Rod",        "Answer 50 Qs in one 60s Speedrun",   "⚡"),
    ("Infinity",             "Score 100+ in Endless mode",         "∞"),
    ("Sharpshooter",         "Reflex mode 20+ answers 100% acc.",  "🎯"),
    ("Ultramarathon",        "Full Marathon + score 150+",         "🏅"),
    ("Omniscient",           "Answer every unique card correctly", "🌟"),
    # ── NEW: Risk/Reward ────────────────────────────────────────────────────
    ("High Roller",          "Cash out Endless with prime score",  "🎰"),
    ("Joker",                "Win after being at 0 points",        "🃏"),
    ("Balance",              "Finish any mode with exactly 21 pts","⚖"),
    # ── NEW: Daily Challenge ────────────────────────────────────────────────
    ("Daily Dedication",     "Complete a daily quest",             "📋"),
    ("Weekly Warrior",       "Complete 3 daily quests",            "🗓"),
    ("Daily Champion",       "Complete a Daily Challenge",         "🌟"),
    # ── NEW: Multiplayer ────────────────────────────────────────────────────
    ("Duelist",              "Win a Multiplayer Duel",             "⚔"),
    ("Dominant",             "Win Duel by 5+ point margin",        "👊"),
    # ── NEW: Power-Ups ──────────────────────────────────────────────────────
    ("Big Spender",          "Spend 50 coins in the shop",        "🛍"),
    ("Coin Collector",       "Earn 100 coins total",              "🪙"),
    # ── NEW: Time Warp ──────────────────────────────────────────────────────
    ("Time Bender",          "Survive 3 minutes in Time Warp",    "🌀"),
    ("Chrono Master",        "Score 30 in Time Warp mode",        "⏰"),
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
    "LOGICAL OPERATOR":"A symbol that performs a comparison resulting in True or False",
    "INFERENCE ENGINE":"The part of an expert system that applies the rules from the rule base to the facts in the knowledge base",
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
    "RECORD":    "All of the information in a table about one object",
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

# ── Card categories for heatmap ───────────────────────────────────────────────
CARD_CATEGORIES = {
    "Hardware":     ["RAM","CPU","GPU","HDD","SSD","ROM","BIOS","MOTHERBOARD","MICROPROCESSOR","ALU","CONTROLLER","CAMERA","HEADPHONES","KEYBOARD","LIGHT RING","MICROPHONE","MONITOR","SPEAKERS","VR HEADSET","USB","USB PORT","USB CABLE","USB CONNECTION","USB DEVICE","ACTUATOR","SENSOR"],
    "Networking":   ["HTTP","HTTPS","IP","DNS","URL","SSH","VPN","LAN","WAN","ETHERNET","SERIAL","PARALLEL","INTERFERENCE","SIMPLEX","DUPLEX","FULL DUPLEX","DATA TRANSMISSION","PACKET","DATA PACKET","PACKET SWITCHING","ARQ","ECHO CHECK","PARITY CHECK","PCHK ERROR"],
    "Software":     ["OS","GUI","API","SQL","HTML","CSS","OOP","IDE","SDK","JSON","XML","EOF","SOFTWARE","DATABASE","ENCRYPTION","ENCRYPTION KEY","ASYMMETRIC ENCRYPTION","CYPHER","COMPRESSION","LOSSY","LOSSLESS"],
    "Data":         ["BINARY","BOOLEAN","DENARY","ANALOGUE","DIGITAL","DATA","DATA TYPE","STRING","LIST","TUPLE","DICTIONARY","RECORD","FIELD","TABLE","PRIMARY KEY","MOD","DIV","IF","LOGICAL OPERATOR"],
    "AI/Robotics":  ["AI","ARTIFICIAL INTELLIGENCE","MACHINE LEARNING","EXPERT SYSTEM","INFERENCE ENGINE","KNOWLEDGE BASE","RULE BASE","ROBOT","ROBOTICS","AUTOMATED"],
    "Logic Gates":  ["AND","OR","NOT","NAND","NOR","XOR"],
    "Misc":         ["VR","PAYLOAD","TRAILER","INFORMATION","INPUT"],
}

# ── Daily challenge seeds (10 cards per day) ──────────────────────────────────
ALL_CARDS = list(FLASHCARDS.keys())

def get_daily_cards():
    """Return a stable list of 10 cards for today."""
    today = date.today()
    seed  = today.year * 10000 + today.month * 100 + today.day
    rng   = random.Random(seed)
    cards = list(FLASHCARDS.keys())
    rng.shuffle(cards)
    return cards[:10]

# ── Daily Quests definition ───────────────────────────────────────────────────
DAILY_QUESTS = [
    ("no_reveal_30",   "Answer 30 cards without revealing",         30, "no_reveal"),
    ("streak_15",      "Get 15 correct in a row",                   15, "streak"),
    ("all_modes",      "Play all 3 game modes in one day",           3, "modes"),
    ("endless_50",     "Score 50+ in Endless mode",                 50, "endless_score"),
    ("normal_12",      "Win Normal mode in under 12 questions",     12, "normal_fast"),
]

# ── Power-up definitions ──────────────────────────────────────────────────────
POWERUPS = [
    ("shield",        "🛡 Shield",       "Protect from 1 wrong answer",     15),
    ("time_freeze",   "❄ Time Freeze",  "Pause timer 10 seconds",           20),
    ("peek",          "👁 Peek",         "Show first letter of answer",       8),
    ("skip",          "⏭ Skip",         "Skip card without penalty",         10),
    ("double_points", "✕2 Double",       "Next answer worth 2 points",       25),
]

# ─────────────────────────── BADGE DEPENDENCIES ──────────────────────────────

BADGE_DEPENDENCIES = {
    "Human Cache":          ["First Steps"],
    "CPU Overclocked":      ["Learning Curve"],
    "Legend":               ["Survivor", "Untouchable"],
    "System Administrator": ["Root Access"],
    "Memory Palace":        ["First Time"],
    "Flawless":             ["First Time"],
    "Dominant":             ["Duelist"],
}

SPEEDRUN_UNLOCK_AT  = 40
TIMEWARP_UNLOCK_AT  = 100

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
    "teal":    "#00b4a0",
    "lime":    "#a8ff3e",
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
            # New columns
            ("coins",                     "INTEGER DEFAULT 0"),
            ("coins_spent",               "INTEGER DEFAULT 0"),
            ("coins_earned_total",        "INTEGER DEFAULT 0"),
            ("daily_challenge_streak",    "INTEGER DEFAULT 0"),
            ("last_daily_date",           "TEXT DEFAULT ''"),
            ("quests_completed",          "INTEGER DEFAULT 0"),
            ("modes_played_today",        "TEXT DEFAULT '[]'"),
            ("session_modes_won",         "TEXT DEFAULT '[]'"),
            ("timewarp_highscore",        "INTEGER DEFAULT 0"),
            ("timewarp_unlocked",         "INTEGER DEFAULT 0"),
            ("total_playtime_seconds",    "INTEGER DEFAULT 0"),
            ("powerup_shield",            "INTEGER DEFAULT 0"),
            ("powerup_time_freeze",       "INTEGER DEFAULT 0"),
            ("powerup_peek",              "INTEGER DEFAULT 0"),
            ("powerup_skip",              "INTEGER DEFAULT 0"),
            ("powerup_double_points",     "INTEGER DEFAULT 0"),
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
                accuracy           REAL DEFAULT 0,
                timestamp          TEXT NOT NULL
            )
        """)
        # Card performance tracking
        cur.execute("""
            CREATE TABLE IF NOT EXISTS card_performance (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id    INTEGER NOT NULL,
                card_term  TEXT NOT NULL,
                correct    INTEGER DEFAULT 0,
                wrong      INTEGER DEFAULT 0,
                last_seen  TEXT DEFAULT '',
                UNIQUE(user_id, card_term)
            )
        """)
        # Daily challenge completions
        cur.execute("""
            CREATE TABLE IF NOT EXISTS daily_challenge_completions (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id   INTEGER NOT NULL,
                date_str  TEXT NOT NULL,
                score     INTEGER DEFAULT 0,
                UNIQUE(user_id, date_str)
            )
        """)
        # Daily quest tracking
        cur.execute("""
            CREATE TABLE IF NOT EXISTS daily_quest_progress (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id    INTEGER NOT NULL,
                quest_id   TEXT NOT NULL,
                date_str   TEXT NOT NULL,
                progress   INTEGER DEFAULT 0,
                completed  INTEGER DEFAULT 0,
                UNIQUE(user_id, quest_id, date_str)
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
        self.conn.execute(
            "UPDATE users SET normal_questions_answered=normal_questions_answered+? WHERE id=?",
            (count, user_id))
        self.conn.commit()

    def increment_games_played(self, user_id):
        self.conn.execute(
            "UPDATE users SET games_played=games_played+1 WHERE id=?", (user_id,))
        self.conn.commit()

    def add_playtime(self, user_id, seconds):
        self.conn.execute(
            "UPDATE users SET total_playtime_seconds=total_playtime_seconds+? WHERE id=?",
            (int(seconds), user_id))
        self.conn.commit()

    def update_consecutive_games(self, user_id, n):
        self.conn.execute(
            "UPDATE users SET consecutive_games=? WHERE id=?", (n, user_id))
        self.conn.commit()

    def check_and_unlock_speedrun(self, user_id):
        row = self.conn.execute(
            "SELECT normal_questions_answered, speedrun_unlocked FROM users WHERE id=?",
            (user_id,)).fetchone()
        if row and row[0] >= SPEEDRUN_UNLOCK_AT and not row[1]:
            self.conn.execute(
                "UPDATE users SET speedrun_unlocked=1 WHERE id=?", (user_id,))
            self.conn.commit()
            return True
        return False

    def check_and_unlock_timewarp(self, user_id):
        row = self.conn.execute(
            "SELECT normal_questions_answered, timewarp_unlocked FROM users WHERE id=?",
            (user_id,)).fetchone()
        if row and row[0] >= TIMEWARP_UNLOCK_AT and not row[1]:
            self.conn.execute(
                "UPDATE users SET timewarp_unlocked=1 WHERE id=?", (user_id,))
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

    def update_timewarp_highscore(self, user_id, score):
        self.conn.execute(
            "UPDATE users SET timewarp_highscore=? WHERE id=? AND timewarp_highscore<?",
            (score, user_id, score))
        self.conn.commit()

    def save_game_history(self, user_id, mode, score, questions, accuracy=0.0):
        self.conn.execute(
            "INSERT INTO game_history(user_id,mode,score,questions_answered,accuracy,timestamp)"
            " VALUES(?,?,?,?,?,?)",
            (user_id, mode, score, questions, accuracy, datetime.now().isoformat()))
        self.conn.commit()

    # ── Coins & Power-Ups ────────────────────────────────────────────────────

    def add_coins(self, user_id, amount):
        self.conn.execute(
            "UPDATE users SET coins=coins+?, coins_earned_total=coins_earned_total+? WHERE id=?",
            (amount, amount, user_id))
        self.conn.commit()

    def spend_coins(self, user_id, amount):
        row = self.conn.execute("SELECT coins FROM users WHERE id=?", (user_id,)).fetchone()
        if row and row[0] >= amount:
            self.conn.execute(
                "UPDATE users SET coins=coins-?, coins_spent=coins_spent+? WHERE id=?",
                (amount, amount, user_id))
            self.conn.commit()
            return True
        return False

    def add_powerup(self, user_id, pup_id, qty=1):
        col = f"powerup_{pup_id}"
        self.conn.execute(f"UPDATE users SET {col}={col}+? WHERE id=?", (qty, user_id))
        self.conn.commit()

    def use_powerup(self, user_id, pup_id):
        col = f"powerup_{pup_id}"
        row = self.conn.execute(f"SELECT {col} FROM users WHERE id=?", (user_id,)).fetchone()
        if row and row[0] > 0:
            self.conn.execute(f"UPDATE users SET {col}={col}-1 WHERE id=?", (user_id,))
            self.conn.commit()
            return True
        return False

    # ── Card Performance ─────────────────────────────────────────────────────

    def record_card_result(self, user_id, card_term, correct):
        now = datetime.now().isoformat()
        self.conn.execute("""
            INSERT INTO card_performance(user_id, card_term, correct, wrong, last_seen)
            VALUES(?,?,?,?,?)
            ON CONFLICT(user_id, card_term) DO UPDATE SET
                correct  = correct  + ?,
                wrong    = wrong    + ?,
                last_seen = ?
        """, (user_id, card_term, 1 if correct else 0, 0 if correct else 1, now,
              1 if correct else 0, 0 if correct else 1, now))
        self.conn.commit()

    def get_weak_spots(self, user_id, n=5):
        """Return top-n cards with highest wrong count."""
        rows = self.conn.execute("""
            SELECT card_term, correct, wrong
            FROM card_performance
            WHERE user_id=? AND wrong > 0
            ORDER BY wrong DESC, correct ASC
            LIMIT ?
        """, (user_id, n)).fetchall()
        return rows

    def get_category_stats(self, user_id):
        """Return dict: category -> (correct, wrong)."""
        rows = self.conn.execute("""
            SELECT card_term, correct, wrong FROM card_performance WHERE user_id=?
        """, (user_id,)).fetchall()
        stats = {cat: [0, 0] for cat in CARD_CATEGORIES}
        stats["Misc"] = [0, 0]
        term_to_cat = {}
        for cat, terms in CARD_CATEGORIES.items():
            for t in terms:
                term_to_cat[t] = cat
        for term, correct, wrong in rows:
            cat = term_to_cat.get(term, "Misc")
            stats[cat][0] += correct
            stats[cat][1] += wrong
        return stats

    def get_accuracy_history(self, user_id, days=7):
        """Return list of (date_str, accuracy) tuples for the last N days."""
        cutoff = (datetime.now() - timedelta(days=days)).isoformat()
        rows = self.conn.execute("""
            SELECT DATE(timestamp), AVG(accuracy)
            FROM game_history
            WHERE user_id=? AND timestamp>=? AND questions_answered>0
            GROUP BY DATE(timestamp)
            ORDER BY DATE(timestamp) ASC
        """, (user_id, cutoff)).fetchall()
        return rows

    # ── Daily Challenge ──────────────────────────────────────────────────────

    def complete_daily_challenge(self, user_id, score):
        today = date.today().isoformat()
        try:
            self.conn.execute(
                "INSERT INTO daily_challenge_completions(user_id,date_str,score) VALUES(?,?,?)",
                (user_id, today, score))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def has_completed_daily(self, user_id):
        today = date.today().isoformat()
        row = self.conn.execute(
            "SELECT id FROM daily_challenge_completions WHERE user_id=? AND date_str=?",
            (user_id, today)).fetchone()
        return row is not None

    def get_completed_dates(self, user_id):
        rows = self.conn.execute(
            "SELECT date_str FROM daily_challenge_completions WHERE user_id=? ORDER BY date_str",
            (user_id,)).fetchall()
        return {r[0] for r in rows}

    # ── Daily Quests ──────────────────────────────────────────────────────────

    def get_quest_progress(self, user_id, quest_id):
        today = date.today().isoformat()
        row = self.conn.execute(
            "SELECT progress, completed FROM daily_quest_progress WHERE user_id=? AND quest_id=? AND date_str=?",
            (user_id, quest_id, today)).fetchone()
        return row if row else (0, 0)

    def update_quest_progress(self, user_id, quest_id, new_progress, target):
        today = date.today().isoformat()
        completed = 1 if new_progress >= target else 0
        self.conn.execute("""
            INSERT INTO daily_quest_progress(user_id, quest_id, date_str, progress, completed)
            VALUES(?,?,?,?,?)
            ON CONFLICT(user_id, quest_id, date_str) DO UPDATE SET
                progress  = MAX(progress, ?),
                completed = MAX(completed, ?)
        """, (user_id, quest_id, today, new_progress, completed, new_progress, completed))
        self.conn.commit()

    def count_quests_completed_today(self, user_id):
        today = date.today().isoformat()
        row = self.conn.execute(
            "SELECT COUNT(*) FROM daily_quest_progress WHERE user_id=? AND date_str=? AND completed=1",
            (user_id, today)).fetchone()
        return row[0] if row else 0

    def increment_quests_completed_total(self, user_id):
        self.conn.execute(
            "UPDATE users SET quests_completed=quests_completed+1 WHERE id=?", (user_id,))
        self.conn.commit()

    # ── Session Mode Tracking ─────────────────────────────────────────────────

    def record_mode_won(self, user_id, mode):
        user = self.get_user_by_id(user_id)
        if not user: return
        modes = json.loads(user.get("session_modes_won") or "[]")
        if mode not in modes:
            modes.append(mode)
        self.conn.execute(
            "UPDATE users SET session_modes_won=? WHERE id=?",
            (json.dumps(modes), user_id))
        self.conn.commit()
        return modes

    def get_user_by_id(self, user_id):
        row = self.conn.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
        if not row: return None
        cols = [r[1] for r in self.conn.execute("PRAGMA table_info(users)").fetchall()]
        return dict(zip(cols, row))

    def reset_session_modes(self, user_id):
        self.conn.execute("UPDATE users SET session_modes_won='[]' WHERE id=?", (user_id,))
        self.conn.commit()

    def record_mode_played_today(self, user_id, mode):
        user = self.get_user_by_id(user_id)
        if not user: return []
        today = date.today().isoformat()
        stored = json.loads(user.get("modes_played_today") or "[]")
        # stored is [[mode, date], ...]
        today_modes = [m for m, d in stored if d == today]
        if mode not in today_modes:
            stored.append([mode, today])
            today_modes.append(mode)
        self.conn.execute(
            "UPDATE users SET modes_played_today=? WHERE id=?",
            (json.dumps(stored), user_id))
        self.conn.commit()
        return today_modes

    # ── Badges ───────────────────────────────────────────────────────────────

    def award_badge(self, user_id, badge_name):
        cur = self.conn.cursor()
        row = cur.execute(
            "SELECT id FROM badges WHERE badge_name=?", (badge_name,)).fetchone()
        if not row:
            return False
        badge_id = row[0]
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
        if count >= 10: self.award_badge(user_id, "Root Access")
        if count >= 20: self.award_badge(user_id, "System Administrator")
        # Check Legendary (all other achievements unlocked)
        total_badges = self.conn.execute("SELECT COUNT(*) FROM badges").fetchone()[0]
        if count >= total_badges - 1:
            self.award_badge(user_id, "Legendary") if self.conn.execute(
                "SELECT id FROM badges WHERE badge_name='Legendary'").fetchone() else None

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

    def check_coin_achievements(self, user_id):
        row = self.conn.execute(
            "SELECT coins_earned_total, coins_spent FROM users WHERE id=?",
            (user_id,)).fetchone()
        if not row: return
        earned, spent = row
        if earned >= 100: self.award_badge(user_id, "Coin Collector")
        if spent >= 50:   self.award_badge(user_id, "Big Spender")

    # ── Leaderboard ──────────────────────────────────────────────────────────

    def get_leaderboard(self):
        return self.conn.execute("""
            SELECT u.username,
                   u.endless_highscore,
                   u.speedrun_highscore,
                   COUNT(ub.badge_id) AS badge_count,
                   u.total_answered,
                   u.coins
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
        def _show(n=name, d=delay + i * 750):
            AchievementPopup(master, n)
            try:
                master.sound.play("achievement")
            except Exception:
                pass
        master.after(delay + i * 750, _show)


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

    def _release(e):
        btn.config(bg=lighter)
        # Fire click SFX if root has a sound manager
        try:
            root = btn.winfo_toplevel()
            if hasattr(root, "sound"):
                root.sound.play("click")
        except Exception:
            pass
        command()

    btn.bind("<ButtonRelease-1>", _release)
    return btn


def make_label(parent, text, font=FONT_MED, fg=C["text"], bg=C["bg"], **kw):
    return tk.Label(parent, text=text, font=font, fg=fg, bg=bg, **kw)


def make_scrollable(parent, bg=C["bg"]):
    """Return (canvas, inner_frame) with proper scroll binding."""
    outer = tk.Frame(parent, bg=bg)
    scv   = tk.Canvas(outer, bg=bg, highlightthickness=0)
    sb    = tk.Scrollbar(outer, orient="vertical", command=scv.yview)
    scv.configure(yscrollcommand=sb.set)
    sb.pack(side="right", fill="y")
    scv.pack(side="left", fill="both", expand=True)
    inner = tk.Frame(scv, bg=bg)
    win   = scv.create_window(0, 0, anchor="nw", window=inner)
    inner.bind("<Configure>", lambda e: scv.configure(scrollregion=scv.bbox("all")))
    scv.bind("<Configure>",   lambda e: scv.itemconfig(win, width=e.width))

    def _on_wheel(e):
        scv.yview_scroll(int(-1*(e.delta/120)), "units")

    scv.bind("<MouseWheel>",  _on_wheel)
    inner.bind("<MouseWheel>", _on_wheel)
    return outer, scv, inner


def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0: return False
    return True


# ══════════════════════════ SOUND MANAGER ════════════════════════════════════

class SoundManager:
    """
    Pure-stdlib audio engine.  Generates PCM tones entirely in Python and
    plays them via:
      • winsound  (Windows)
      • afplay    (macOS)
      • aplay     (Linux / ALSA)
    Music is a gentle lo-fi loop built from layered sine tones.
    All playback is non-blocking (threads) so the UI stays responsive.
    """

    SAMPLE_RATE = 22050
    CHANNELS    = 1
    SAMPWIDTH   = 2   # 16-bit

    # ---------- waveform helpers ----------

    @staticmethod
    def _sine(freq, duration, volume=0.4, sample_rate=22050):
        """Return raw 16-bit PCM bytes for a sine wave."""
        n      = int(sample_rate * duration)
        factor = 2 * math.pi * freq / sample_rate
        data   = bytearray(n * 2)
        for i in range(n):
            # Tiny fade-in/out to kill clicks
            env = min(1.0, min(i, n - i) / max(1, sample_rate * 0.008))
            val = int(volume * env * 32767 * math.sin(i * factor))
            struct.pack_into("<h", data, i * 2, max(-32768, min(32767, val)))
        return bytes(data)

    @staticmethod
    def _mix(*pcm_list):
        """Mix multiple equal-length PCM byte strings by averaging."""
        n = len(pcm_list[0]) // 2
        out = bytearray(len(pcm_list[0]))
        for i in range(n):
            total = sum(struct.unpack_from("<h", p, i * 2)[0] for p in pcm_list)
            val   = max(-32768, min(32767, total // len(pcm_list)))
            struct.pack_into("<h", out, i * 2, val)
        return bytes(out)

    @staticmethod
    def _envelope(pcm, attack=0.02, release=0.05, sample_rate=22050):
        """Apply attack/release envelope to PCM bytes."""
        n        = len(pcm) // 2
        atk_s    = int(sample_rate * attack)
        rel_s    = int(sample_rate * release)
        out      = bytearray(len(pcm))
        for i in range(n):
            if i < atk_s:
                env = i / atk_s
            elif i > n - rel_s:
                env = (n - i) / rel_s
            else:
                env = 1.0
            val = int(struct.unpack_from("<h", pcm, i * 2)[0] * env)
            struct.pack_into("<h", out, i * 2, max(-32768, min(32767, val)))
        return bytes(out)

    @classmethod
    def _make_wav(cls, pcm):
        """Wrap raw PCM in a WAV container and return bytes."""
        buf = io.BytesIO()
        with wave.open(buf, "wb") as wf:
            wf.setnchannels(cls.CHANNELS)
            wf.setsampwidth(cls.SAMPWIDTH)
            wf.setframerate(cls.SAMPLE_RATE)
            wf.writeframes(pcm)
        return buf.getvalue()

    # ---------- sound definitions ----------

    @classmethod
    def _build_sounds(cls):
        sr = cls.SAMPLE_RATE
        s  = cls._sine

        sounds = {}

        # Correct — bright ascending two-tone ding
        t1 = s(880,  0.10, 0.55, sr)
        t2 = s(1320, 0.14, 0.45, sr)
        combined  = t1 + bytes(max(0, len(t2) - len(t1)))
        combined2 = bytes(max(0, len(t1) - len(t2))) + t2
        n = min(len(combined), len(combined2)) // 2
        merged = bytearray(n * 2)
        for i in range(n):
            v1 = struct.unpack_from("<h", combined,  i * 2)[0]
            v2 = struct.unpack_from("<h", combined2, i * 2)[0]
            struct.pack_into("<h", merged, i * 2, max(-32768, min(32767, v1 + v2)))
        sounds["correct"] = cls._make_wav(cls._envelope(bytes(merged)))

        # Wrong — descending dissonant buzz
        b1 = s(220, 0.12, 0.5, sr)
        b2 = s(196, 0.18, 0.4, sr)
        n  = min(len(b1), len(b2)) // 2
        bz = bytearray(n * 2)
        for i in range(n):
            v1 = struct.unpack_from("<h", b1, i * 2)[0]
            v2 = struct.unpack_from("<h", b2, i * 2)[0]
            struct.pack_into("<h", bz, i * 2, max(-32768, min(32767, (v1 + v2) // 2)))
        sounds["wrong"] = cls._make_wav(cls._envelope(bytes(bz), attack=0.005, release=0.1))

        # Achievement — triumphant 4-note fanfare
        notes  = [523, 659, 784, 1047]   # C5 E5 G5 C6
        frames = b""
        for freq in notes:
            frames += cls._envelope(s(freq, 0.13, 0.5, sr), attack=0.01, release=0.04)
        sounds["achievement"] = cls._make_wav(frames)

        # Click — very short tick
        sounds["click"] = cls._make_wav(cls._envelope(s(1200, 0.03, 0.25, sr),
                                                       attack=0.001, release=0.01))

        # Reveal — soft whoosh (detuned saw approximated with 8 harmonics)
        whoosh = bytearray(int(sr * 0.18) * 2)
        for h in range(1, 9):
            tone = s(300 * h, 0.18, 0.08 / h, sr)
            for i in range(len(whoosh) // 2):
                v  = struct.unpack_from("<h", whoosh, i * 2)[0]
                v2 = struct.unpack_from("<h", tone,   i * 2)[0] if i * 2 < len(tone) else 0
                struct.pack_into("<h", whoosh, i * 2, max(-32768, min(32767, v + v2)))
        sounds["reveal"] = cls._make_wav(cls._envelope(bytes(whoosh), attack=0.02, release=0.08))

        # Cashout — coin jingle (three quick pings)
        coin = b""
        for freq in [1047, 1175, 1319]:
            coin += cls._envelope(s(freq, 0.08, 0.45, sr), attack=0.005, release=0.04)
        sounds["cashout"] = cls._make_wav(coin)

        return sounds

    @classmethod
    def _build_music_loop(cls, duration=8.0):
        """
        Generate a ~8 second lo-fi study beat loop:
        - Slow bass note (root)
        - Mid pad chord (root + fifth)
        - Gentle high melody motif
        All soft, blended, loopable.
        """
        sr  = cls.SAMPLE_RATE
        n   = int(sr * duration)
        s   = cls._sine
        buf = bytearray(n * 2)

        def _add(freq, vol, dur, offset_s=0.0):
            tone  = cls._envelope(s(freq, dur, vol, sr), attack=0.15, release=0.2)
            start = int(offset_s * sr)
            for i in range(len(tone) // 2):
                idx = start + i
                if idx >= n: break
                old = struct.unpack_from("<h", buf, idx * 2)[0]
                new = struct.unpack_from("<h", tone, i * 2)[0]
                struct.pack_into("<h", buf, idx * 2,
                                 max(-32768, min(32767, old + new)))

        # Bass pulses every 2 s  (A2 = 110 Hz)
        for t in [0, 2.0, 4.0, 6.0]:
            _add(110, 0.18, 1.4, t)

        # Pad chord (A3 + E4 + A4)
        for freq, vol in [(220, 0.10), (330, 0.08), (440, 0.07)]:
            _add(freq, vol, duration - 0.3, 0.0)

        # Melody motif — gentle 8-note phrase repeated
        melody = [
            (660, 0.30, 0.14, 0.0),
            (587, 0.25, 0.14, 0.5),
            (523, 0.28, 0.18, 1.0),
            (587, 0.22, 0.12, 1.6),
            (660, 0.30, 0.20, 2.2),
            (784, 0.28, 0.16, 3.0),
            (740, 0.25, 0.14, 3.6),
            (660, 0.30, 0.28, 4.2),
            (587, 0.22, 0.16, 5.0),
            (523, 0.28, 0.22, 5.6),
            (440, 0.20, 0.30, 6.4),
            (494, 0.25, 0.24, 7.0),
        ]
        for freq, vol, dur, off in melody:
            _add(freq, vol, dur, off)

        return cls._make_wav(bytes(buf))

    # ---------- playback ----------

    @staticmethod
    def _write_tmp(wav_bytes, suffix=".wav"):
        """Write WAV bytes to a temp file; return path."""
        import tempfile
        fd, path = tempfile.mkstemp(suffix=suffix)
        os.write(fd, wav_bytes)
        os.close(fd)
        return path

    @classmethod
    def _play_wav_bytes(cls, wav_bytes):
        """Play wav_bytes non-blocking. Returns immediately."""
        def _worker():
            path = cls._write_tmp(wav_bytes)
            try:
                if sys.platform == "win32":
                    import winsound
                    winsound.PlaySound(path, winsound.SND_FILENAME)
                elif sys.platform == "darwin":
                    os.system(f'afplay "{path}" 2>/dev/null')
                else:
                    os.system(f'aplay -q "{path}" 2>/dev/null || '
                              f'paplay "{path}" 2>/dev/null || '
                              f'ffplay -nodisp -autoexit -loglevel quiet "{path}" 2>/dev/null')
            finally:
                try: os.unlink(path)
                except: pass
        threading.Thread(target=_worker, daemon=True).start()

    # ---------- public API ----------

    def __init__(self):
        self._sfx_enabled   = True
        self._music_enabled = True
        self._volume        = 0.7       # 0.0 – 1.0 (applied by scaling pcm)
        self._music_thread  = None
        self._music_stop    = threading.Event()
        self._sounds        = {}
        self._music_wav     = None
        # Build in background so startup is instant
        threading.Thread(target=self._preload, daemon=True).start()

    def _preload(self):
        try:
            self._sounds   = self._build_sounds()
            self._music_wav = self._build_music_loop(duration=8.0)
        except Exception:
            pass   # silently degrade if audio generation fails

    # -- SFX --

    def play(self, name):
        """Play a named SFX if enabled. Non-blocking."""
        if not self._sfx_enabled: return
        wav = self._sounds.get(name)
        if wav:
            self._play_wav_bytes(wav)

    # -- Music --

    def start_music(self):
        """Start looping background music in a daemon thread."""
        if not self._music_enabled: return
        if self._music_thread and self._music_thread.is_alive(): return
        self._music_stop.clear()
        self._music_thread = threading.Thread(target=self._music_loop, daemon=True)
        self._music_thread.start()

    def stop_music(self):
        """Signal the music loop to stop after its current iteration."""
        self._music_stop.set()

    def _music_loop(self):
        while not self._music_stop.is_set():
            wav = self._music_wav
            if not wav: time.sleep(0.5); continue
            path = self._write_tmp(wav)
            try:
                if sys.platform == "win32":
                    import winsound
                    winsound.PlaySound(path, winsound.SND_FILENAME)
                elif sys.platform == "darwin":
                    os.system(f'afplay "{path}" 2>/dev/null')
                else:
                    os.system(f'aplay -q "{path}" 2>/dev/null || '
                              f'paplay "{path}" 2>/dev/null || '
                              f'ffplay -nodisp -autoexit -loglevel quiet "{path}" 2>/dev/null')
            finally:
                try: os.unlink(path)
                except: pass
            if self._music_stop.is_set(): break

    # -- Toggles --

    def toggle_sfx(self):
        self._sfx_enabled = not self._sfx_enabled
        return self._sfx_enabled

    def toggle_music(self):
        self._music_enabled = not self._music_enabled
        if self._music_enabled:
            self.start_music()
        else:
            self.stop_music()
        return self._music_enabled


# ══════════════════════════ MAIN APPLICATION ═════════════════════════════════

class FlashcardApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CS Flashcard Game — Extended Edition v2.0")
        self.geometry("960x700")
        self.resizable(True, True)
        self.configure(bg=C["bg"])
        self.minsize(720, 560)
        self._fullscreen    = False
        self._current_frame = None
        # Session tracking across modes for Triple Threat
        self._session_modes_won = set()
        self.bind("<F11>",    lambda e: self.toggle_fullscreen())
        self.bind("<Escape>", lambda e: self.exit_fullscreen())
        self.db    = DatabaseManager()
        self.user  = None
        self.sound = SoundManager()
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
        # Music: play during game modes, stop on menu/lobby screens
        _game_screens = (NormalModeScreen, EndlessModeScreen, SpeedrunModeScreen,
                         TimeWarpModeScreen, MultiplayerDuelScreen, DailyChallengeScreen)
        _menu_screens = (MainMenu, LoginScreen, RewardsScreen, LeaderboardScreen,
                         PowerUpShopScreen, StatsScreen, DailyQuestsScreen,
                         SpeedrunMenuScreen, SpeedrunLockedScreen, TimeWarpLockedScreen,
                         MultiplayerSetupScreen, VictoryScreen, EndlessResultScreen,
                         SpeedrunResultScreen, TimeWarpResultScreen, DuelResultScreen)
        try:
            if isinstance(frame, _game_screens):
                self.sound.start_music()
            elif isinstance(frame, _menu_screens):
                self.sound.stop_music()
        except Exception:
            pass

    def show_login(self):           self.show_frame(LoginScreen)
    def show_menu(self):            self.show_frame(MainMenu)
    def show_normal_mode(self):     self.show_frame(NormalModeScreen)
    def show_endless_mode(self):    self.show_frame(EndlessModeScreen)
    def show_rewards(self):         self.show_frame(RewardsScreen)
    def show_leaderboard(self):     self.show_frame(LeaderboardScreen)
    def show_shop(self):            self.show_frame(PowerUpShopScreen)
    def show_daily_challenge(self): self.show_frame(DailyChallengeScreen)
    def show_heatmap(self):         self.show_frame(HeatmapScreen)
    def show_weak_spots(self):      self.show_frame(WeakSpotsScreen)
    def show_daily_quests(self):    self.show_frame(DailyQuestsScreen)
    def show_multiplayer(self):     self.show_frame(MultiplayerSetupScreen)
    def show_stats(self):           self.show_frame(StatsScreen)

    def show_timewarp_mode(self):
        if self.user and self.user.get("timewarp_unlocked", 0):
            self.show_frame(TimeWarpModeScreen)
        else:
            self.show_frame(TimeWarpLockedScreen)

    def show_speedrun_menu(self):
        if self.user and self.user.get("speedrun_unlocked", 0):
            self.show_frame(SpeedrunMenuScreen)
        else:
            self.show_frame(SpeedrunLockedScreen)

    def show_speedrun_mode(self, mode_type):
        self.show_frame(SpeedrunModeScreen, mode_type=mode_type)

    def on_close(self):
        self.sound.stop_music()
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
        self._err = make_label(self, "", bg=C["panel"], fg="#ff6b6b", font=FONT_SMALL)
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
                   font=FONT_TITLE, fg=C["cyan"]).pack(pady=(20, 2))

        sr_unlocked = user.get("speedrun_unlocked", 0)
        tw_unlocked = user.get("timewarp_unlocked", 0)
        normal_q    = user.get("normal_questions_answered", 0)
        needed_sr   = max(0, SPEEDRUN_UNLOCK_AT - normal_q)
        needed_tw   = max(0, TIMEWARP_UNLOCK_AT - normal_q)
        coins       = user.get("coins", 0)

        if sr_unlocked and tw_unlocked:
            stats = (f"Endless HS: {user['endless_highscore']}  |  "
                     f"Speedrun HS: {user.get('speedrun_highscore',0)}  |  "
                     f"🪙 {coins} coins  |  Total Q: {user['total_answered']}")
        else:
            unlock_info = []
            if not sr_unlocked:
                unlock_info.append(f"Speedrun 🔒 {normal_q}/{SPEEDRUN_UNLOCK_AT}")
            if not tw_unlocked:
                unlock_info.append(f"TimeWarp 🔒 {normal_q}/{TIMEWARP_UNLOCK_AT}")
            stats = (f"Endless HS: {user['endless_highscore']}  |  "
                     f"🪙 {coins} coins  |  " + "  |  ".join(unlock_info))

        make_label(self, stats, font=FONT_SMALL, fg=C["yellow"]).pack(pady=(0, 12))

        sr_text  = "⚡  Speedrun Mode" if sr_unlocked else f"⚡  Speedrun 🔒 ({needed_sr} Qs)"
        sr_color = C["orange"] if sr_unlocked else C["muted"]
        tw_text  = "🌀  Time Warp Mode" if tw_unlocked else f"🌀  Time Warp 🔒 ({needed_tw} Qs)"
        tw_color = C["teal"] if tw_unlocked else C["muted"]

        # Two-column button layout
        cols = tk.Frame(self, bg=C["bg"])
        cols.pack()
        left  = tk.Frame(cols, bg=C["bg"])
        right = tk.Frame(cols, bg=C["bg"])
        left.pack(side="left", padx=10)
        right.pack(side="left", padx=10)

        left_btns = [
            ("▶  Normal Mode",         C["accent"],   self.master.show_normal_mode),
            ("♾  Endless Mode",        C["purple"],   self.master.show_endless_mode),
            (sr_text,                   sr_color,      self.master.show_speedrun_menu),
            (tw_text,                   tw_color,      self.master.show_timewarp_mode),
            ("⚔  Multiplayer Duel",    C["pink"],     self.master.show_multiplayer),
            ("✕  Quit",                "#333344",     self._quit),
        ]
        right_btns = [
            ("📅  Daily Challenge",    C["yellow"],   self.master.show_daily_challenge, C["bg"]),
            ("📋  Daily Quests",       "#2a5a2a",     self.master.show_daily_quests,    C["white"]),
            ("🏅  Badges",            "#1a6b3c",     self.master.show_rewards,         C["white"]),
            ("🛍  Power-Up Shop",     C["accent2"],  self.master.show_shop,            C["white"]),
            ("📊  Stats & Heatmap",   "#2d2d4e",     self.master.show_stats,           C["white"]),
            ("📊  Leaderboard",       "#1a3a6a",     self.master.show_leaderboard,     C["white"]),
        ]

        for text, color, cmd in left_btns:
            make_button(left, text, cmd, bg=color,
                        font=FONT_MED, pad=(24, 10), width=24).pack(pady=4)

        for text, color, cmd, fg in right_btns:
            make_button(right, text, cmd, bg=color, fg=fg,
                        font=FONT_MED, pad=(24, 10), width=24).pack(pady=4)

        fs_row = tk.Frame(self, bg=C["bg"])
        fs_row.pack(pady=(8, 0))
        self._fs_btn = make_button(fs_row, self._fs_label(), self._toggle_fs,
                                   bg="#2a2a3e", font=FONT_SMALL, pad=(16, 7))
        self._fs_btn.pack(side="left", padx=4)

        # ── Audio controls ────────────────────────────────────────────────────
        audio_row = tk.Frame(self, bg=C["bg"])
        audio_row.pack(pady=(4, 0))

        snd = self.master.sound
        self._sfx_btn = make_button(
            audio_row,
            self._sfx_label(),
            self._toggle_sfx,
            bg="#2a2a3e", font=FONT_SMALL, pad=(14, 7))
        self._sfx_btn.pack(side="left", padx=4)

        self._music_btn = make_button(
            audio_row,
            self._music_label(),
            self._toggle_music,
            bg="#2a2a3e", font=FONT_SMALL, pad=(14, 7))
        self._music_btn.pack(side="left", padx=4)

    def _quit(self):     self.master.on_close()
    def _fs_label(self): return "⛶  Exit Fullscreen" if self.master._fullscreen else "⛶  Fullscreen"
    def _toggle_fs(self):
        self.master.toggle_fullscreen()
        self._fs_btn.config(text=self._fs_label())

    def _sfx_label(self):
        return "🔊 SFX: ON" if self.master.sound._sfx_enabled else "🔇 SFX: OFF"

    def _toggle_sfx(self):
        self.master.sound.toggle_sfx()
        self._sfx_btn.config(text=self._sfx_label())

    def _music_label(self):
        return "🎵 Music: ON" if self.master.sound._music_enabled else "🎵 Music: OFF"

    def _toggle_music(self):
        self.master.sound.toggle_music()
        self._music_btn.config(text=self._music_label())


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
        make_label(self, f"Answer {SPEEDRUN_UNLOCK_AT} questions in Normal Mode to unlock.",
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
                 height=14, width=int(400 * ratio)).place(x=0, y=0)
        make_button(self, "▶  Play Normal Mode", self.master.show_normal_mode,
                    bg=C["accent"], font=FONT_LARGE, pad=(30, 12)).pack(pady=24)
        make_button(self, "← Back to Menu", self.master.show_menu,
                    bg=C["accent2"], pad=(20, 8)).pack()


# ══════════════════════════ TIME WARP LOCKED ══════════════════════════════════

class TimeWarpLockedScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=C["bg"])
        self._build()

    def _build(self):
        make_label(self, "🔒  Time Warp Mode Locked",
                   font=FONT_TITLE, fg=C["muted"]).pack(pady=(80, 20))
        user   = self.master.user
        normal = user.get("normal_questions_answered", 0)
        needed = max(0, TIMEWARP_UNLOCK_AT - normal)
        make_label(self, f"Answer {TIMEWARP_UNLOCK_AT} questions in Normal Mode to unlock.",
                   font=FONT_LARGE, fg=C["text"]).pack(pady=10)
        make_label(self, f"Progress:  {normal} / {TIMEWARP_UNLOCK_AT}",
                   font=FONT_MED, fg=C["yellow"]).pack(pady=5)
        make_label(self, f"Still need:  {needed} more questions",
                   font=FONT_MED, fg=C["cyan"] if needed > 0 else C["green"]).pack(pady=5)
        bar_frame = tk.Frame(self, bg=C["card"], height=14, width=400)
        bar_frame.pack(pady=14); bar_frame.pack_propagate(False)
        ratio = min(1.0, normal / TIMEWARP_UNLOCK_AT)
        tk.Frame(bar_frame,
                 bg=C["green"] if ratio >= 1 else C["teal"],
                 height=14, width=int(400 * ratio)).place(x=0, y=0)
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
            make_label(panel, title, font=FONT_LARGE, fg=C["orange"], bg=C["card"]).pack()
            make_label(panel, desc, font=FONT_SMALL, fg=C["muted"], bg=C["card"]).pack()
            m = mid
            make_button(panel, "Select →",
                        lambda m=m: self.master.show_speedrun_mode(m),
                        bg=C["orange"], pad=(20, 5)).pack(pady=(8, 0))
        make_button(self, "← Back to Menu", self.master.show_menu,
                    bg=C["accent2"], pad=(20, 8)).pack(pady=24)


# ══════════════════════════ POWER-UP HUD ════════════════════════════════════

class PowerUpHUD(tk.Frame):
    """Small horizontal bar showing available power-ups with use buttons."""
    def __init__(self, parent, user, db, bg=C["bg"]):
        super().__init__(parent, bg=bg)
        self.user = user
        self.db   = db
        self._active = {}   # pup_id -> bool (whether active this turn)
        self._callbacks = {}
        self._build()

    def _build(self):
        make_label(self, "Power-Ups:", font=("Segoe UI", 10, "bold"),
                   fg=C["muted"], bg=self["bg"]).pack(side="left", padx=(0, 8))
        self._btns = {}
        self._qty_labels = {}
        for pup_id, name, desc, cost in POWERUPS:
            qty = self.user.get(f"powerup_{pup_id}", 0)
            f = tk.Frame(self, bg=self["bg"])
            f.pack(side="left", padx=4)
            icon = name.split()[0]
            btn = tk.Label(f, text=icon, font=("Segoe UI", 14),
                           bg=C["card"] if qty > 0 else C["panel"],
                           fg=C["white"] if qty > 0 else C["muted"],
                           padx=6, pady=2, relief="flat",
                           cursor="hand2" if qty > 0 else "arrow")
            btn.pack()
            ql = tk.Label(f, text=f"×{qty}", font=("Segoe UI", 8),
                          bg=self["bg"], fg=C["yellow"] if qty > 0 else C["muted"])
            ql.pack()
            if qty > 0:
                pid = pup_id
                btn.bind("<ButtonRelease-1>", lambda e, p=pid: self._use(p))
            self._btns[pup_id] = btn
            self._qty_labels[pup_id] = ql

    def register_callback(self, pup_id, cb):
        self._callbacks[pup_id] = cb

    def _use(self, pup_id):
        qty = self.user.get(f"powerup_{pup_id}", 0)
        if qty <= 0: return
        if self.db.use_powerup(self.user["id"], pup_id):
            self.user[f"powerup_{pup_id}"] = qty - 1
            self._refresh(pup_id)
            if pup_id in self._callbacks:
                self._callbacks[pup_id]()

    def _refresh(self, pup_id):
        qty = self.user.get(f"powerup_{pup_id}", 0)
        btn = self._btns[pup_id]
        ql  = self._qty_labels[pup_id]
        ql.config(text=f"×{qty}")
        if qty > 0:
            btn.config(bg=C["card"], fg=C["white"], cursor="hand2")
        else:
            btn.config(bg=C["panel"], fg=C["muted"], cursor="arrow")
            btn.unbind("<ButtonRelease-1>")


# ══════════════════════════ BASE GAME SCREEN ══════════════════════════════════

class BaseGameScreen(tk.Frame):
    def __init__(self, master, mode):
        super().__init__(master, bg=C["bg"])
        self.mode             = mode
        self.score            = 0
        self.questions        = 0
        self.correct_streak   = 0
        self._deck            = list(FLASHCARDS.keys())
        random.shuffle(self._deck)
        self._deck_idx        = 0
        self._revealed        = False
        self._reveal_used     = False
        self._start_time      = time.time()
        self._card_start_time = time.time()
        self._session_cards   = set()
        self._correct_cards   = set()
        self._mistakes        = 0
        self._no_reveal_run   = True
        self._was_at_zero     = False
        self._double_active   = False
        self._shield_active   = False
        self._skip_used       = False
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
        # Coin display
        self.coin_lbl = make_label(top, f"🪙 {self.master.user.get('coins', 0)}",
                                   font=FONT_SMALL, fg=C["yellow"], bg=C["bg"])
        self.coin_lbl.pack(side="right", padx=10)

        if self.mode == "normal":
            self._pb_canvas = tk.Canvas(self, height=22, bg=C["bg"],
                                        highlightthickness=0)
            self._pb_canvas.pack(fill="x", padx=20, pady=(0, 10))
            self._pb_value  = 0.0
            self._pb_target = 0.0
            self._pb_color  = C["green"]
            self._pb_canvas.bind("<Configure>", lambda e: self._pb_draw(self._pb_value))

        self.canvas = tk.Canvas(self, bg=C["bg"], highlightthickness=0,
                                width=860, height=260)
        self.canvas.pack(pady=4)
        self._draw_card_bg()
        self.term_text = self.canvas.create_text(
            430, 90, text="", fill=C["white"],
            font=("Segoe UI", 32, "bold"), width=780)
        self.ans_text = self.canvas.create_text(
            430, 185, text="", fill=C["cyan"],
            font=FONT_MED, width=780)

        btn_row = tk.Frame(self, bg=C["bg"])
        btn_row.pack(pady=4)
        self.reveal_btn = make_button(btn_row, "👁  Reveal Answer", self._reveal,
                                      bg=C["accent2"], font=FONT_LARGE, pad=(30, 10))
        self.reveal_btn.pack(side="left", padx=10)
        self.correct_btn = make_button(btn_row, "✅ Correct  +1",
                                       lambda: self._answer(True),
                                       bg=C["green"], font=FONT_LARGE, pad=(20, 10))
        self.wrong_btn   = make_button(btn_row,
                                       "❌ Wrong  -2" if self.mode == "normal" else "❌ Wrong",
                                       lambda: self._answer(False),
                                       bg=C["accent"], font=FONT_LARGE, pad=(20, 10))
        self.correct_btn.pack_forget()
        self.wrong_btn.pack_forget()

        self.q_lbl = make_label(self, "Questions answered: 0",
                                font=FONT_SMALL, fg=C["muted"])
        self.q_lbl.pack()

        # Power-up HUD
        self._hud = PowerUpHUD(self, self.master.user, self.master.db)
        self._hud.pack(pady=(2, 0))
        self._hud.register_callback("shield",        self._activate_shield)
        self._hud.register_callback("time_freeze",   self._activate_time_freeze)
        self._hud.register_callback("peek",          self._activate_peek)
        self._hud.register_callback("skip",          self._activate_skip)
        self._hud.register_callback("double_points", self._activate_double)

        # Status label for power-ups
        self._status_var = tk.StringVar()
        make_label(self, "", font=FONT_SMALL, fg=C["orange"],
                   bg=C["bg"], textvariable=self._status_var).pack()

        # Cash Out button – Endless only
        if self.mode == "endless":
            co_outer = tk.Frame(self, bg=C["bg"])
            co_outer.pack(pady=4)
            self.cashout_btn = make_button(
                co_outer, "💾  Cash Out", self._cash_out,
                bg=C["green"], fg=C["bg"],
                font=("Segoe UI", 15, "bold"), pad=(28, 10))
            self.cashout_btn.pack()
            GlowEffect(self.cashout_btn, color=C["green"])
            make_label(co_outer, "Save your score — wrong answer loses it",
                       font=("Segoe UI", 9), fg=C["muted"], bg=C["bg"]).pack(pady=(2, 0))

    def _get_title(self):
        if self.mode == "normal":   return "Normal Mode  (reach 11 pts)"
        if self.mode == "endless":  return "Endless Mode"
        if self.mode == "timewarp": return "⏰ Time Warp"
        return "Speedrun"

    def _draw_card_bg(self):
        self.canvas.create_rectangle(10, 10, 850, 250,
                                     fill=C["card"], outline=C["accent2"], width=2)

    # ── Power-Up Activations ─────────────────────────────────────────────────

    def _activate_shield(self):
        self._shield_active = True
        self._status_var.set("🛡 Shield active — next wrong answer protected!")

    def _activate_time_freeze(self):
        # Subclasses that have timers override this
        self._status_var.set("❄ Time Freeze activated!")

    def _activate_peek(self):
        if not self._revealed:
            ans = FLASHCARDS.get(self._current_term, "")
            first = ans[0] if ans else "?"
            self.canvas.itemconfig(self.ans_text, text=f"Starts with: {first}...")
        self._status_var.set("👁 Peek used!")

    def _activate_skip(self):
        self._skip_used = True
        self._status_var.set("⏭ Skipping card…")
        self.after(300, self._next_card)

    def _activate_double(self):
        self._double_active = True
        self._status_var.set("✕2 Double Points active for next answer!")

    # ── Cards ─────────────────────────────────────────────────────────────────

    def _next_card(self):
        self._revealed = self._reveal_used = False
        self._double_active = False
        self._card_start_time = time.time()
        self.reveal_btn.pack(side="left", padx=10)
        self.correct_btn.pack_forget()
        self.wrong_btn.pack_forget()
        self._status_var.set("")
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
        self.master.sound.play("reveal")
        self.reveal_btn.pack_forget()
        self.correct_btn.pack(side="left", padx=10)
        self.wrong_btn.pack(side="left",   padx=10)

    def _answer(self, correct):
        # Tortoise achievement: 120+ seconds on one card
        card_time = time.time() - self._card_start_time
        if card_time >= 120:
            self.master.db.award_badge(self.master.user["id"], "Tortoise")

        self.questions += 1
        self.q_lbl.config(text=f"Questions answered: {self.questions}")
        db  = self.master.db
        uid = self.master.user["id"]
        db.update_streak(uid, correct)
        db.record_card_result(uid, self._current_term, correct)

        # Hare: 3 cards in under 10 seconds total (tracked via session)
        if not hasattr(self, "_hare_times"):
            self._hare_times = []
        self._hare_times.append(time.time())
        if len(self._hare_times) >= 3:
            span = self._hare_times[-1] - self._hare_times[-3]
            if span < 10:
                db.award_badge(uid, "Hare")

        if correct:
            pts = 2 if self._double_active else 1
            self.score += pts
            self.correct_streak += 1
            self._correct_cards.add(self._current_term)
            self._float(f"+{pts}", C["green"])
            self.master.sound.play("correct")
            if self.correct_streak >= 20:
                db.award_badge(uid, "CPU Overclocked")
            # Earn 1 coin per correct answer
            db.add_coins(uid, 1)
            self.master.user["coins"] = self.master.user.get("coins", 0) + 1
            self.coin_lbl.config(text=f"🪙 {self.master.user['coins']}")
            db.check_coin_achievements(uid)
        else:
            if self._shield_active:
                self._shield_active = False
                self._status_var.set("🛡 Shield absorbed the wrong answer!")
                self.master.sound.play("correct")
                self._next_card()
                return
            self.correct_streak = 0
            self._mistakes += 1
            self.master.sound.play("wrong")
            self._on_wrong()
            return

        self._double_active = False
        self._update_score_display()

        if self.score == 0 and self.questions > 1:
            self._was_at_zero = True

        if not self._reveal_used and self.questions == 10:
            db.award_badge(uid, "Human Cache")
        if self.questions >= 5 and (time.time() - self._start_time) < 30:
            db.award_badge(uid, "Lightning Brain")

        # Puzzle Master: 30 unique cards
        if len(self._session_cards) >= 30:
            db.award_badge(uid, "Puzzle Master")

        self._check_win()
        self._next_card()

    def _float(self, text, color):
        cx = (self.canvas.winfo_width() or 430) // 2
        FloatingText(self.canvas, cx, 120, text, color,
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

    # ── Common end-of-game helpers ────────────────────────────────────────────

    def _common_end_checks(self, db, uid, new_badges):
        now   = datetime.now()
        h     = now.hour
        dow   = now.weekday()   # 1 = Tuesday
        # Night Coder (midnight-5am)
        if h < 5 and db.award_badge(uid, "Night Coder"):
            new_badges.append("Night Coder")
        # Owl (3-4am)
        if h == 3 and db.award_badge(uid, "Owl"):
            new_badges.append("Owl")
        # Nostalgia (Tuesday)
        if dow == 1 and db.award_badge(uid, "Nostalgia"):
            new_badges.append("Nostalgia")
        # Wizard: completed mode without ever using reveal
        if self._no_reveal_run and db.award_badge(uid, "Wizard"):
            new_badges.append("Wizard")
        # Joker: won after being at 0
        if self._was_at_zero and db.award_badge(uid, "Joker"):
            new_badges.append("Joker")
        # Balance: exactly 21 points
        if self.score == 21 and db.award_badge(uid, "Balance"):
            new_badges.append("Balance")
        # Omniscient: answered all unique cards correctly
        if self._correct_cards >= set(FLASHCARDS.keys()):
            if db.award_badge(uid, "Omniscient"):
                new_badges.append("Omniscient")
        # Consecutive games
        consec = (self.master.user.get("consecutive_games", 0) or 0) + 1
        db.update_consecutive_games(uid, consec)
        if consec >= 5 and db.award_badge(uid, "Addicted"):
            new_badges.append("Addicted")
        # Triple Threat (session)
        session_modes = self.master._session_modes_won
        if len(session_modes) >= 3:
            if db.award_badge(uid, "Triple Threat"):
                new_badges.append("Triple Threat")
        return new_badges


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
        acc = (self.questions - self._mistakes) / max(1, self.questions) * 100

        db.increment_total_answered(uid, self.questions)
        db.increment_normal_questions(uid, self.questions)
        db.increment_games_played(uid)
        db.add_playtime(uid, time.time() - self._start_time)
        db.save_game_history(uid, "normal", self.score, self.questions, acc)
        db.check_progress_achievements(uid)
        db.check_and_unlock_speedrun(uid)
        db.check_and_unlock_timewarp(uid)

        # Record mode won for Triple Threat
        self.master._session_modes_won.add("normal")
        db.record_mode_won(uid, "normal")

        # Daily quest: all_modes
        today_modes = db.record_mode_played_today(uid, "normal")
        if len(today_modes) >= 3:
            db.update_quest_progress(uid, "all_modes", 3, 3)

        # Daily quest: normal_fast
        if self.questions <= 12:
            db.update_quest_progress(uid, "normal_12", 1, 1)

        self.master.user = db.get_user(self.master.user["username"])

        new_badges = []
        if db.award_badge(uid, "First Time"):        new_badges.append("First Time")
        if self.questions < 15 and db.award_badge(uid, "Fast Learner"):
            new_badges.append("Fast Learner")
        if self._mistakes == 0 and db.award_badge(uid, "Flawless"):
            new_badges.append("Flawless")
        if self._mistakes == 0 and db.award_badge(uid, "Bullseye"):
            new_badges.append("Bullseye")
        if self._no_reveal_run and db.award_badge(uid, "Memory Palace"):
            new_badges.append("Memory Palace")
        if len(self._session_cards) >= len(FLASHCARDS):
            if db.award_badge(uid, "Database Brain"):
                new_badges.append("Database Brain")

        new_badges = self._common_end_checks(db, uid, new_badges)
        queue_popups(self.master, new_badges, delay=400)
        self.after(200, lambda: self.master.show_frame(
            VictoryScreen, score=self.score,
            questions=self.questions, new_badges=new_badges))


# ══════════════════════════ ENDLESS MODE ════════════════════════════════════

class EndlessModeScreen(BaseGameScreen):
    def __init__(self, master):
        super().__init__(master, "endless")
        self._ended = False

    def _on_wrong(self):
        if self._ended: return
        self._ended = True
        db  = self.master.db
        uid = self.master.user["id"]
        acc = (self.questions - self._mistakes) / max(1, self.questions) * 100

        db.increment_total_answered(uid, self.questions)
        db.increment_games_played(uid)
        db.add_playtime(uid, time.time() - self._start_time)
        db.save_game_history(uid, "endless_wrong", self.score, self.questions, acc)
        db.check_progress_achievements(uid)
        self._award_endless_badges(db, uid, [])

        today_modes = db.record_mode_played_today(uid, "endless")
        if len(today_modes) >= 3:
            db.update_quest_progress(uid, "all_modes", 3, 3)

        prev_hs = self.master.user["endless_highscore"]
        self.master.user = db.get_user(self.master.user["username"])
        self.after(120, lambda: self.master.show_frame(
            EndlessResultScreen, score=self.score, prev_hs=prev_hs,
            new_hs=False, cashout=False))

    def _cash_out(self):
        if self._ended: return
        self._ended = True
        self.master.sound.play("cashout")
        db  = self.master.db
        uid = self.master.user["id"]
        acc = (self.questions - self._mistakes) / max(1, self.questions) * 100

        db.increment_total_answered(uid, self.questions)
        db.increment_games_played(uid)
        db.add_playtime(uid, time.time() - self._start_time)
        db.save_game_history(uid, "endless_cashout", self.score, self.questions, acc)
        db.check_progress_achievements(uid)

        new_badges = []
        new_badges = self._award_endless_badges(db, uid, new_badges)

        # Risk achievements
        if self.score == 1   and db.award_badge(uid, "Gambler"):     new_badges.append("Gambler")
        if self.score >= 20  and db.award_badge(uid, "Risk Taker"):  new_badges.append("Risk Taker")
        if self.score >= 100 and db.award_badge(uid, "Diamond Hands"):new_badges.append("Diamond Hands")
        if is_prime(self.score) and db.award_badge(uid, "High Roller"):new_badges.append("High Roller")

        today_modes = db.record_mode_played_today(uid, "endless")
        if len(today_modes) >= 3:
            db.update_quest_progress(uid, "all_modes", 3, 3)

        # Quest: endless_50
        if self.score >= 50:
            db.update_quest_progress(uid, "endless_50", self.score, 50)

        self.master._session_modes_won.add("endless")
        db.record_mode_won(uid, "endless")

        new_badges = self._common_end_checks(db, uid, new_badges)

        prev_hs = self.master.user["endless_highscore"]
        new_hs  = self.score > prev_hs
        if new_hs:
            db.update_endless_highscore(uid, self.score)
        self.master.user = db.get_user(self.master.user["username"])

        queue_popups(self.master, new_badges)
        self.after(120, lambda: self.master.show_frame(
            EndlessResultScreen, score=self.score, prev_hs=prev_hs,
            new_hs=new_hs, cashout=True))

    def _award_endless_badges(self, db, uid, new_badges):
        pairs = [
            (10, "Endless 10"), (15, "Survivor"), (25, "Endless 25"),
            (30, "Untouchable"), (32, "Binary Master"), (50, "Endless 50"),
            (75, "Legend"), (100, "Infinity"),
        ]
        for threshold, badge in pairs:
            if self.score >= threshold and db.award_badge(uid, badge):
                new_badges.append(badge)
        return new_badges


# ══════════════════════════ SPEEDRUN MODE ════════════════════════════════════

class SpeedrunModeScreen(BaseGameScreen):
    def __init__(self, master, mode_type):
        self.speedrun_type  = mode_type
        self.timer_running  = False
        self._reflex_wrong  = 0
        super().__init__(master, "speedrun")
        self.time_left      = self._initial_time()
        self.timer_running  = True
        self._tick()

    def _initial_time(self):
        return {"60s": 60, "marathon": 600, "reflex": 10}[self.speedrun_type]

    def _build_ui(self):
        super()._build_ui()
        self._tb = tk.Canvas(self, height=14, bg=C["bg"], highlightthickness=0)
        self._tb.pack(fill="x", padx=20, pady=(0, 4))
        self._tb.bind("<Configure>", lambda e: self._draw_timer_bar())
        tr = tk.Frame(self, bg=C["bg"]); tr.pack()
        make_label(tr, "⏱  Time:", font=FONT_MED, fg=C["cyan"]).pack(side="left")
        self._timer_lbl = make_label(tr, "0", font=("Segoe UI", 20, "bold"),
                                     fg=C["green"], bg=C["bg"])
        self._timer_lbl.pack(side="left", padx=8)

    def _activate_time_freeze(self):
        self.time_left += 10
        self._status_var.set("❄ Time Freeze! +10 seconds added!")

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
        lbl  = f"{mins}:{secs:02d}" if self.speedrun_type == "marathon" else str(max(0, int(self.time_left)))
        self._timer_lbl.config(text=lbl)
        self._draw_timer_bar()
        if self.time_left < 10:
            clr = C["accent"] if int(self.time_left * 2) % 2 == 0 else C["yellow"]
            self._timer_lbl.config(fg=clr)
        else:
            self._timer_lbl.config(fg=C["green"])
        if self.time_left <= 0:
            self._end_speedrun(); return
        self.after(1000, self._tick)

    def _on_wrong(self):
        if self.speedrun_type == "reflex":
            self._reflex_wrong += 1
        self._next_card()

    def _answer(self, correct):
        super()._answer(correct)
        if correct and self.speedrun_type == "reflex":
            self.time_left = 10

    def _end_speedrun(self):
        self.timer_running = False
        db  = self.master.db
        uid = self.master.user["id"]
        acc = (self.questions - self._mistakes) / max(1, self.questions) * 100

        db.increment_total_answered(uid, self.questions)
        db.increment_games_played(uid)
        db.add_playtime(uid, self._initial_time())
        db.save_game_history(uid, f"speedrun_{self.speedrun_type}",
                             self.score, self.questions, acc)
        db.update_speedrun_highscore(uid, self.score)
        db.check_progress_achievements(uid)

        today_modes = db.record_mode_played_today(uid, f"speedrun_{self.speedrun_type}")
        if len(today_modes) >= 3:
            db.update_quest_progress(uid, "all_modes", 3, 3)

        self.master._session_modes_won.add("speedrun")
        db.record_mode_won(uid, "speedrun")

        new_badges = []
        if   self.speedrun_type == "60s"     and self.score     >= 20:  nb = "Blitz Master"
        elif self.speedrun_type == "60s"     and self.questions >= 50:  nb = "Lightning Rod"
        elif self.speedrun_type == "marathon" and self.score    >= 100:  nb = "Marathon Runner"
        elif self.speedrun_type == "marathon" and self.score    >= 150:  nb = "Ultramarathon"
        elif self.speedrun_type == "reflex"   and self.questions >= 30:  nb = "Reflex God"
        else: nb = None
        if nb and db.award_badge(uid, nb): new_badges.append(nb)

        # Sharpshooter: reflex 20+ answers 100% accuracy
        if (self.speedrun_type == "reflex" and self.questions >= 20
                and self._reflex_wrong == 0 and db.award_badge(uid, "Sharpshooter")):
            new_badges.append("Sharpshooter")

        new_badges = self._common_end_checks(db, uid, new_badges)
        queue_popups(self.master, new_badges)
        self.master.user = db.get_user(self.master.user["username"])
        self.after(100, lambda: self.master.show_frame(
            SpeedrunResultScreen, score=self.score,
            mode_type=self.speedrun_type, questions=self.questions))

    def _back_to_menu(self):
        self.timer_running = False
        super()._back_to_menu()


# ══════════════════════════ TIME WARP MODE ════════════════════════════════════

class TimeWarpModeScreen(BaseGameScreen):
    """Timer starts at 60s, +3 correct, -5 wrong. Survive as long as possible."""
    def __init__(self, master):
        self.timer_running = False
        self._elapsed_total = 0
        super().__init__(master, "timewarp")
        self.time_left     = 60.0
        self.timer_running = True
        self._tick()

    def _build_ui(self):
        super()._build_ui()
        self._tb = tk.Canvas(self, height=18, bg=C["bg"], highlightthickness=0)
        self._tb.pack(fill="x", padx=20, pady=(0, 4))
        self._tb.bind("<Configure>", lambda e: self._draw_timer_bar())
        tr = tk.Frame(self, bg=C["bg"]); tr.pack()
        make_label(tr, "⏰ Time Warp:", font=FONT_MED, fg=C["teal"]).pack(side="left")
        self._timer_lbl = make_label(tr, "60", font=("Segoe UI", 22, "bold"),
                                     fg=C["green"], bg=C["bg"])
        self._timer_lbl.pack(side="left", padx=8)
        make_label(tr, " ✅+3s  ❌-5s", font=FONT_SMALL, fg=C["muted"]).pack(side="left")

    def _activate_time_freeze(self):
        self.time_left += 10
        self._status_var.set("❄ Time Freeze! +10 seconds added!")

    def _draw_timer_bar(self):
        c = self._tb; W = c.winfo_width(); H = c.winfo_height()
        if W < 2: return
        c.delete("all")
        ratio = max(0.0, min(1.0, self.time_left / 60))
        color = C["accent"] if ratio < 0.2 else C["yellow"] if ratio < 0.5 else C["teal"]
        c.create_rectangle(0, 2, W, H-2, fill=C["card"], outline="")
        fw = int(ratio * W)
        if fw > 0:
            c.create_rectangle(0, 2, fw, H-2, fill=color, outline="")

    def _tick(self):
        if not self.timer_running: return
        self.time_left -= 1
        self._elapsed_total += 1
        self._timer_lbl.config(text=str(max(0, int(self.time_left))))
        self._draw_timer_bar()
        if self.time_left < 10:
            clr = C["accent"] if int(self.time_left * 2) % 2 == 0 else C["yellow"]
            self._timer_lbl.config(fg=clr)
        else:
            self._timer_lbl.config(fg=C["teal"])
        if self.time_left <= 0:
            self._end_timewarp(); return
        self.after(1000, self._tick)

    def _on_wrong(self):
        self.time_left = max(0, self.time_left - 5)
        self._float("-5s", C["accent"])
        self._update_score_display(wrong=True if hasattr(self, "_pb_canvas") else False)
        self._next_card()

    def _answer(self, correct):
        super()._answer(correct)
        if correct:
            self.time_left += 3
            self._float("+3s", C["teal"])

    def _check_win(self): pass  # no win condition, survive as long as possible

    def _end_timewarp(self):
        self.timer_running = False
        db  = self.master.db
        uid = self.master.user["id"]
        acc = (self.questions - self._mistakes) / max(1, self.questions) * 100

        db.increment_total_answered(uid, self.questions)
        db.increment_games_played(uid)
        db.add_playtime(uid, self._elapsed_total)
        db.save_game_history(uid, "timewarp", self.score, self.questions, acc)
        db.update_timewarp_highscore(uid, self.score)
        db.check_progress_achievements(uid)

        new_badges = []
        if self._elapsed_total >= 180 and db.award_badge(uid, "Time Bender"):
            new_badges.append("Time Bender")
        if self.score >= 30 and db.award_badge(uid, "Chrono Master"):
            new_badges.append("Chrono Master")

        new_badges = self._common_end_checks(db, uid, new_badges)
        queue_popups(self.master, new_badges)
        self.master.user = db.get_user(self.master.user["username"])
        self.after(100, lambda: self.master.show_frame(
            TimeWarpResultScreen, score=self.score,
            elapsed=self._elapsed_total, questions=self.questions))

    def _back_to_menu(self):
        self.timer_running = False
        super()._back_to_menu()


# ══════════════════════════ MULTIPLAYER DUEL ══════════════════════════════════

class MultiplayerSetupScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=C["bg"])
        self._build()

    def _build(self):
        make_label(self, "⚔  Multiplayer Duel",
                   font=FONT_TITLE, fg=C["pink"]).pack(pady=(40, 10))
        make_label(self, "Two players take turns on the same device.\nFirst to reach 15 points wins!",
                   font=FONT_MED, fg=C["text"], justify="center").pack(pady=(0, 30))

        panel = tk.Frame(self, bg=C["panel"], padx=40, pady=24)
        panel.pack()

        make_label(panel, "Player 1 Name:", bg=C["panel"], fg=C["cyan"],
                   font=FONT_MED).grid(row=0, column=0, sticky="w", pady=6)
        self._p1 = tk.StringVar(value=self.master.user.get("username", "Player 1"))
        tk.Entry(panel, textvariable=self._p1, font=FONT_MED,
                 bg=C["card"], fg=C["text"], insertbackground=C["text"],
                 relief="flat", width=20).grid(row=0, column=1, padx=10)

        make_label(panel, "Player 2 Name:", bg=C["panel"], fg=C["pink"],
                   font=FONT_MED).grid(row=1, column=0, sticky="w", pady=6)
        self._p2 = tk.StringVar(value="Player 2")
        tk.Entry(panel, textvariable=self._p2, font=FONT_MED,
                 bg=C["card"], fg=C["text"], insertbackground=C["text"],
                 relief="flat", width=20).grid(row=1, column=1, padx=10)

        make_label(panel, "Cards per player:", bg=C["panel"], fg=C["text"],
                   font=FONT_MED).grid(row=2, column=0, sticky="w", pady=6)
        self._rounds = tk.IntVar(value=10)
        for i, val in enumerate([5, 10, 15, 20]):
            tk.Radiobutton(panel, text=str(val), variable=self._rounds, value=val,
                           bg=C["panel"], fg=C["text"],
                           selectcolor=C["card"], font=FONT_SMALL
                           ).grid(row=2, column=1+i//2, sticky="w")

        make_button(self, "⚔  Start Duel!", self._start,
                    bg=C["pink"], font=FONT_LARGE, pad=(30, 12)).pack(pady=24)
        make_button(self, "← Back to Menu", self.master.show_menu,
                    bg=C["accent2"], pad=(20, 8)).pack()

    def _start(self):
        p1 = self._p1.get().strip() or "Player 1"
        p2 = self._p2.get().strip() or "Player 2"
        self.master.show_frame(MultiplayerDuelScreen,
                               p1_name=p1, p2_name=p2,
                               cards_per_player=self._rounds.get())


class MultiplayerDuelScreen(tk.Frame):
    def __init__(self, master, p1_name, p2_name, cards_per_player):
        super().__init__(master, bg=C["bg"])
        self.p1_name         = p1_name
        self.p2_name         = p2_name
        self.cards_per       = cards_per_player
        self.p1_score        = 0
        self.p2_score        = 0
        self.p1_cards        = 0
        self.p2_cards        = 0
        self.current_player  = 1
        self._deck           = list(FLASHCARDS.keys())
        random.shuffle(self._deck)
        self._deck_idx       = 0
        self._revealed       = False
        self._build()
        self._next_card()

    def _build(self):
        # Header
        top = tk.Frame(self, bg=C["bg"])
        top.pack(fill="x", padx=20, pady=10)
        make_button(top, "← Menu", self._back, bg=C["accent2"],
                    font=FONT_SMALL, pad=(10, 5)).pack(side="left")
        make_label(top, "⚔  Multiplayer Duel", font=FONT_LARGE,
                   fg=C["pink"], bg=C["bg"]).pack(side="left", padx=20)

        # Score panels
        score_row = tk.Frame(self, bg=C["bg"])
        score_row.pack(fill="x", padx=40, pady=8)
        self._p1_panel = tk.Frame(score_row, bg=C["card"], padx=20, pady=10)
        self._p1_panel.pack(side="left", expand=True, fill="both")
        self._p2_panel = tk.Frame(score_row, bg=C["card"], padx=20, pady=10)
        self._p2_panel.pack(side="right", expand=True, fill="both")

        self._p1_name_lbl = tk.Label(self._p1_panel, text=self.p1_name,
                                      font=("Segoe UI", 14, "bold"),
                                      fg=C["cyan"], bg=C["card"])
        self._p1_name_lbl.pack()
        self._p1_score_lbl = tk.Label(self._p1_panel, text="0",
                                       font=("Segoe UI", 36, "bold"),
                                       fg=C["yellow"], bg=C["card"])
        self._p1_score_lbl.pack()
        self._p1_cards_lbl = tk.Label(self._p1_panel, text="Cards: 0",
                                       font=FONT_SMALL, fg=C["muted"], bg=C["card"])
        self._p1_cards_lbl.pack()

        self._p2_name_lbl = tk.Label(self._p2_panel, text=self.p2_name,
                                      font=("Segoe UI", 14, "bold"),
                                      fg=C["pink"], bg=C["card"])
        self._p2_name_lbl.pack()
        self._p2_score_lbl = tk.Label(self._p2_panel, text="0",
                                       font=("Segoe UI", 36, "bold"),
                                       fg=C["yellow"], bg=C["card"])
        self._p2_score_lbl.pack()
        self._p2_cards_lbl = tk.Label(self._p2_panel, text="Cards: 0",
                                       font=FONT_SMALL, fg=C["muted"], bg=C["card"])
        self._p2_cards_lbl.pack()

        # Turn indicator
        self._turn_lbl = make_label(self, "", font=FONT_LARGE, fg=C["yellow"])
        self._turn_lbl.pack(pady=4)

        # Card canvas
        self.canvas = tk.Canvas(self, bg=C["bg"], highlightthickness=0,
                                width=860, height=240)
        self.canvas.pack(pady=4)
        self.canvas.create_rectangle(10, 10, 850, 230,
                                     fill=C["card"], outline=C["accent2"], width=2)
        self.term_text = self.canvas.create_text(
            430, 85, text="", fill=C["white"],
            font=("Segoe UI", 30, "bold"), width=780)
        self.ans_text = self.canvas.create_text(
            430, 165, text="", fill=C["cyan"],
            font=FONT_MED, width=780)

        # Buttons
        btn_row = tk.Frame(self, bg=C["bg"])
        btn_row.pack(pady=6)
        self.reveal_btn = make_button(btn_row, "👁  Reveal Answer", self._reveal,
                                      bg=C["accent2"], font=FONT_LARGE, pad=(30, 10))
        self.reveal_btn.pack(side="left", padx=10)
        self.correct_btn = make_button(btn_row, "✅ Correct  +1",
                                       lambda: self._answer(True),
                                       bg=C["green"], font=FONT_LARGE, pad=(20, 10))
        self.wrong_btn = make_button(btn_row, "❌ Wrong",
                                     lambda: self._answer(False),
                                     bg=C["accent"], font=FONT_LARGE, pad=(20, 10))
        self.correct_btn.pack_forget()
        self.wrong_btn.pack_forget()

        self.q_lbl = make_label(self, "", font=FONT_SMALL, fg=C["muted"])
        self.q_lbl.pack()

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

        # Highlight active player
        if self.current_player == 1:
            self._p1_panel.config(bg=C["accent2"])
            self._p1_name_lbl.config(bg=C["accent2"])
            self._p1_score_lbl.config(bg=C["accent2"])
            self._p1_cards_lbl.config(bg=C["accent2"])
            self._p2_panel.config(bg=C["card"])
            self._p2_name_lbl.config(bg=C["card"])
            self._p2_score_lbl.config(bg=C["card"])
            self._p2_cards_lbl.config(bg=C["card"])
            self._turn_lbl.config(
                text=f"🎯 {self.p1_name}'s Turn  ({self.cards_per - self.p1_cards} cards left)",
                fg=C["cyan"])
        else:
            self._p2_panel.config(bg=C["accent2"])
            self._p2_name_lbl.config(bg=C["accent2"])
            self._p2_score_lbl.config(bg=C["accent2"])
            self._p2_cards_lbl.config(bg=C["accent2"])
            self._p1_panel.config(bg=C["card"])
            self._p1_name_lbl.config(bg=C["card"])
            self._p1_score_lbl.config(bg=C["card"])
            self._p1_cards_lbl.config(bg=C["card"])
            self._turn_lbl.config(
                text=f"🎯 {self.p2_name}'s Turn  ({self.cards_per - self.p2_cards} cards left)",
                fg=C["pink"])

        total_done = self.p1_cards + self.p2_cards
        self.q_lbl.config(text=f"Round {total_done + 1} of {self.cards_per * 2}")

    def _reveal(self):
        if self._revealed: return
        self._revealed = True
        self.canvas.itemconfig(self.ans_text, text=FLASHCARDS[self._current_term])
        self.reveal_btn.pack_forget()
        self.correct_btn.pack(side="left", padx=10)
        self.wrong_btn.pack(side="left", padx=10)

    def _answer(self, correct):
        if self.current_player == 1:
            if correct:
                self.p1_score += 1
                self._p1_score_lbl.config(text=str(self.p1_score))
            self.p1_cards += 1
            self._p1_cards_lbl.config(text=f"Cards: {self.p1_cards}")
            if self.p1_cards >= self.cards_per and self.p2_cards >= self.cards_per:
                self._end_duel(); return
            # Alternate: switch to p2 after each card
            self.current_player = 2
        else:
            if correct:
                self.p2_score += 1
                self._p2_score_lbl.config(text=str(self.p2_score))
            self.p2_cards += 1
            self._p2_cards_lbl.config(text=f"Cards: {self.p2_cards}")
            if self.p1_cards >= self.cards_per and self.p2_cards >= self.cards_per:
                self._end_duel(); return
            self.current_player = 1

        self._next_card()

    def _end_duel(self):
        db  = self.master.db
        uid = self.master.user["id"]
        p1_won = self.p1_score > self.p2_score
        margin = abs(self.p1_score - self.p2_score)

        if p1_won or self.p1_score == self.p2_score:
            if p1_won and db.award_badge(uid, "Duelist"):
                queue_popups(self.master, ["Duelist"])
            if p1_won and margin >= 5 and db.award_badge(uid, "Dominant"):
                queue_popups(self.master, ["Dominant"], delay=800)

        self.master.show_frame(
            DuelResultScreen,
            p1_name=self.p1_name, p2_name=self.p2_name,
            p1_score=self.p1_score, p2_score=self.p2_score)

    def _back(self):
        self.master.show_menu()


class DuelResultScreen(tk.Frame):
    def __init__(self, master, p1_name, p2_name, p1_score, p2_score):
        super().__init__(master, bg=C["bg"])
        self.p1_name  = p1_name; self.p2_name  = p2_name
        self.p1_score = p1_score; self.p2_score = p2_score
        self._build()

    def _build(self):
        W, H = 960, 700
        c = tk.Canvas(self, width=W, height=H, bg=C["bg"], highlightthickness=0)
        c.pack(fill="both", expand=True)

        if self.p1_score != self.p2_score:
            ConfettiCanvas(c, W, H)

        if self.p1_score > self.p2_score:
            winner = self.p1_name; loser = self.p2_name
            ws = self.p1_score;   ls = self.p2_score
        elif self.p2_score > self.p1_score:
            winner = self.p2_name; loser = self.p1_name
            ws = self.p2_score;   ls = self.p1_score
        else:
            winner = None

        if winner:
            c.create_text(W//2, 160, text=f"⚔  {winner} Wins!",
                          fill=C["yellow"], font=("Segoe UI", 44, "bold"))
            c.create_text(W//2, 240, text=f"{ws}  vs  {ls}",
                          fill=C["text"], font=("Segoe UI", 28))
            c.create_text(W//2, 300, text=f"{loser}: better luck next time!",
                          fill=C["muted"], font=FONT_MED)
        else:
            c.create_text(W//2, 160, text="🤝  It's a Draw!",
                          fill=C["cyan"], font=("Segoe UI", 44, "bold"))
            c.create_text(W//2, 240, text=f"{self.p1_score}  vs  {self.p2_score}",
                          fill=C["text"], font=("Segoe UI", 28))

        bf = tk.Frame(c, bg=C["bg"])
        c.create_window(W//2, 420, window=bf)
        make_button(bf, "⚔ Play Again", self.master.show_multiplayer,
                    bg=C["pink"], pad=(20, 10)).pack(side="left", padx=10)
        make_button(bf, "🏠 Menu", self.master.show_menu,
                    bg=C["accent2"], pad=(20, 10)).pack(side="left", padx=10)


# ══════════════════════════ DAILY CHALLENGE ══════════════════════════════════

class DailyChallengeScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=C["bg"])
        self._cards       = get_daily_cards()
        self._idx         = 0
        self._score       = 0
        self._revealed    = False
        self._done        = False
        self._already     = master.db.has_completed_daily(master.user["id"])
        self._build()
        if not self._already:
            self._show_card()

    def _build(self):
        today = date.today().strftime("%A, %d %B %Y")
        make_label(self, f"📅  Daily Challenge — {today}",
                   font=FONT_TITLE, fg=C["yellow"]).pack(pady=(20, 4))

        if self._already:
            make_label(self, "✅ You've already completed today's challenge!",
                       font=FONT_LARGE, fg=C["green"]).pack(pady=20)
            self._show_calendar()
            make_button(self, "← Back to Menu", self.master.show_menu,
                        bg=C["accent2"], pad=(20, 8)).pack(pady=10)
            return

        make_label(self, "10 cards — complete them all for bonus rewards!",
                   font=FONT_SMALL, fg=C["muted"]).pack(pady=(0, 10))

        self._prog_lbl = make_label(self, "Card 1 of 10", font=FONT_MED, fg=C["cyan"])
        self._prog_lbl.pack()

        self.canvas = tk.Canvas(self, bg=C["bg"], highlightthickness=0,
                                width=860, height=240)
        self.canvas.pack(pady=8)
        self.canvas.create_rectangle(10, 10, 850, 230,
                                     fill=C["card"], outline=C["yellow"], width=2)
        self.term_text = self.canvas.create_text(
            430, 85, text="", fill=C["white"],
            font=("Segoe UI", 30, "bold"), width=780)
        self.ans_text = self.canvas.create_text(
            430, 165, text="", fill=C["cyan"], font=FONT_MED, width=780)

        btn_row = tk.Frame(self, bg=C["bg"])
        btn_row.pack(pady=6)
        self.reveal_btn = make_button(btn_row, "👁  Reveal", self._reveal,
                                      bg=C["accent2"], font=FONT_LARGE, pad=(24, 10))
        self.reveal_btn.pack(side="left", padx=10)
        self.correct_btn = make_button(btn_row, "✅ Got it",
                                       lambda: self._answer(True),
                                       bg=C["green"], font=FONT_LARGE, pad=(20, 10))
        self.wrong_btn = make_button(btn_row, "❌ Missed",
                                     lambda: self._answer(False),
                                     bg=C["accent"], font=FONT_LARGE, pad=(20, 10))
        self.correct_btn.pack_forget()
        self.wrong_btn.pack_forget()

        self._score_lbl = make_label(self, "Score: 0 / 10", font=FONT_MED, fg=C["yellow"])
        self._score_lbl.pack()
        make_button(self, "← Back to Menu", self.master.show_menu,
                    bg=C["accent2"], pad=(16, 6), font=FONT_SMALL).pack(pady=6)

    def _show_card(self):
        if self._idx >= len(self._cards):
            self._finish(); return
        term = self._cards[self._idx]
        self._current_term = term
        self._revealed = False
        self.reveal_btn.pack(side="left", padx=10)
        self.correct_btn.pack_forget()
        self.wrong_btn.pack_forget()
        self.canvas.itemconfig(self.term_text, text=term)
        self.canvas.itemconfig(self.ans_text, text="")
        self._prog_lbl.config(text=f"Card {self._idx+1} of {len(self._cards)}")

    def _reveal(self):
        if self._revealed: return
        self._revealed = True
        self.canvas.itemconfig(self.ans_text, text=FLASHCARDS[self._current_term])
        self.reveal_btn.pack_forget()
        self.correct_btn.pack(side="left", padx=10)
        self.wrong_btn.pack(side="left", padx=10)

    def _answer(self, correct):
        if correct: self._score += 1
        self._score_lbl.config(text=f"Score: {self._score} / {len(self._cards)}")
        self._idx += 1
        self.after(200, self._show_card)

    def _finish(self):
        db  = self.master.db
        uid = self.master.user["id"]
        db.complete_daily_challenge(uid, self._score)
        # Reward: bonus coins
        bonus = self._score * 3
        db.add_coins(uid, bonus)
        db.award_badge(uid, "Daily Champion")
        self.master.user = db.get_user(self.master.user["username"])

        # Clear widgets and show result
        for w in self.winfo_children(): w.destroy()
        make_label(self, "📅  Daily Challenge Complete!",
                   font=FONT_TITLE, fg=C["yellow"]).pack(pady=(40, 10))
        make_label(self, f"Score: {self._score} / {len(self._cards)}",
                   font=("Segoe UI", 36, "bold"), fg=C["green"]).pack(pady=10)
        make_label(self, f"🪙 Bonus: +{bonus} coins",
                   font=FONT_LARGE, fg=C["yellow"]).pack(pady=6)
        self._show_calendar()
        row = tk.Frame(self, bg=C["bg"]); row.pack(pady=16)
        make_button(row, "📅 Play Again Tomorrow", self.master.show_menu,
                    bg=C["accent2"], pad=(16, 8)).pack(side="left", padx=8)
        make_button(row, "🏠 Menu", self.master.show_menu,
                    bg=C["purple"], pad=(16, 8)).pack(side="left", padx=8)

    def _show_calendar(self):
        db  = self.master.db
        uid = self.master.user["id"]
        completed = db.get_completed_dates(uid)

        make_label(self, "📆  Challenge Calendar (last 30 days)",
                   font=FONT_MED, fg=C["cyan"]).pack(pady=(16, 6))

        today = date.today()
        cal_frame = tk.Frame(self, bg=C["panel"], padx=16, pady=12)
        cal_frame.pack(padx=60)

        # Day headers
        days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        for i, d in enumerate(days):
            tk.Label(cal_frame, text=d, font=("Segoe UI", 9, "bold"),
                     fg=C["muted"], bg=C["panel"], width=4).grid(row=0, column=i)

        # Find start of 5-week window
        start = today - timedelta(days=today.weekday() + 28)
        for week in range(5):
            for dow in range(7):
                day = start + timedelta(weeks=week, days=dow)
                if day > today: continue
                ds = day.isoformat()
                done = ds in completed
                is_today = day == today
                bg = C["green"] if done else (C["accent2"] if is_today else C["card"])
                fg = C["white"] if (done or is_today) else C["muted"]
                tk.Label(cal_frame, text=str(day.day),
                         bg=bg, fg=fg, font=("Segoe UI", 9),
                         width=3, pady=4, relief="flat"
                         ).grid(row=week+1, column=dow, padx=1, pady=1)


# ══════════════════════════ DAILY QUESTS ══════════════════════════════════════

class DailyQuestsScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=C["bg"])
        self._build()

    def _build(self):
        make_label(self, "📋  Daily Quests",
                   font=FONT_TITLE, fg=C["lime"]).pack(pady=(20, 6))
        today = date.today().strftime("%A, %d %B")
        make_label(self, f"Today: {today}  — complete quests for achievements!",
                   font=FONT_SMALL, fg=C["muted"]).pack(pady=(0, 16))

        db  = self.master.db
        uid = self.master.user["id"]
        completed_today = db.count_quests_completed_today(uid)

        for qid, label, target, kind in DAILY_QUESTS:
            prog, done = db.get_quest_progress(uid, qid)
            pct = min(1.0, prog / target) if target else 1.0

            row = tk.Frame(self, bg=C["card"] if done else C["panel"],
                           padx=20, pady=12)
            row.pack(fill="x", padx=60, pady=5)

            icon = "✅" if done else "🔲"
            tk.Label(row, text=icon, font=("Segoe UI", 18),
                     bg=row["bg"], fg=C["green"] if done else C["muted"]
                     ).pack(side="left", padx=(0, 12))

            info = tk.Frame(row, bg=row["bg"])
            info.pack(side="left", fill="x", expand=True)
            tk.Label(info, text=label, font=("Segoe UI", 13, "bold"),
                     fg=C["text"] if not done else C["green"],
                     bg=row["bg"], anchor="w").pack(anchor="w")
            # Progress bar
            bar_outer = tk.Frame(info, bg=C["bg"], height=6, width=300)
            bar_outer.pack(anchor="w", pady=3)
            bar_outer.pack_propagate(False)
            bar_fill = tk.Frame(bar_outer,
                                bg=C["green"] if done else C["lime"],
                                height=6)
            bar_fill.place(x=0, y=0, relwidth=pct, relheight=1)

            tk.Label(info, text=f"Progress: {prog} / {target}",
                     font=FONT_SMALL, fg=C["muted"], bg=row["bg"],
                     anchor="w").pack(anchor="w")

        # Summary
        make_label(self, f"Quests completed today: {completed_today} / {len(DAILY_QUESTS)}",
                   font=FONT_MED, fg=C["yellow"]).pack(pady=16)
        total_q = self.master.user.get("quests_completed", 0)
        make_label(self, f"Total quests completed all time: {total_q}",
                   font=FONT_SMALL, fg=C["muted"]).pack()

        make_button(self, "← Back to Menu", self.master.show_menu,
                    bg=C["accent2"], pad=(20, 8)).pack(pady=14)


# ══════════════════════════ POWER-UP SHOP ════════════════════════════════════

class PowerUpShopScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=C["bg"])
        self._build()

    def _build(self):
        make_label(self, "🛍  Power-Up Shop",
                   font=FONT_TITLE, fg=C["orange"]).pack(pady=(20, 4))
        self._coin_var = tk.StringVar(value=f"🪙 Your Coins: {self.master.user.get('coins',0)}")
        make_label(self, "", font=FONT_LARGE, fg=C["yellow"],
                   textvariable=self._coin_var).pack(pady=(0, 16))

        for pup_id, name, desc, cost in POWERUPS:
            qty = self.master.user.get(f"powerup_{pup_id}", 0)
            row = tk.Frame(self, bg=C["card"], padx=24, pady=14)
            row.pack(fill="x", padx=80, pady=6)
            icon = name.split()[0]
            tk.Label(row, text=icon, font=("Segoe UI", 28),
                     bg=C["card"], fg=C["orange"]).pack(side="left", padx=(0, 16))
            info = tk.Frame(row, bg=C["card"])
            info.pack(side="left", fill="x", expand=True)
            tk.Label(info, text=name, font=("Segoe UI", 14, "bold"),
                     fg=C["text"], bg=C["card"], anchor="w").pack(anchor="w")
            tk.Label(info, text=desc, font=FONT_SMALL,
                     fg=C["muted"], bg=C["card"], anchor="w").pack(anchor="w")

            right = tk.Frame(row, bg=C["card"])
            right.pack(side="right")
            self._qty_lbl = tk.Label(right, text=f"Owned: {qty}",
                                     font=FONT_SMALL, fg=C["yellow"], bg=C["card"])
            self._qty_lbl.pack()
            pid = pup_id; pname = name; pcost = cost
            ql = self._qty_lbl

            def _buy(pid=pid, pname=pname, pcost=pcost, ql=ql):
                if self.master.db.spend_coins(self.master.user["id"], pcost):
                    self.master.db.add_powerup(self.master.user["id"], pid)
                    self.master.user = self.master.db.get_user(self.master.user["username"])
                    new_qty = self.master.user.get(f"powerup_{pid}", 0)
                    ql.config(text=f"Owned: {new_qty}")
                    self._coin_var.set(f"🪙 Your Coins: {self.master.user.get('coins',0)}")
                    self.master.db.check_coin_achievements(self.master.user["id"])

            make_button(right, f"Buy — {cost} 🪙", _buy,
                        bg=C["orange"], fg=C["bg"],
                        font=FONT_SMALL, pad=(12, 6)).pack(pady=4)

        make_button(self, "← Back to Menu", self.master.show_menu,
                    bg=C["accent2"], pad=(20, 8)).pack(pady=16)


# ══════════════════════════ STATS / HEATMAP / GRAPH ══════════════════════════

class StatsScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=C["bg"])
        self._build()

    def _build(self):
        make_label(self, "📊  Stats, Heatmap & Learning Curve",
                   font=FONT_TITLE, fg=C["cyan"]).pack(pady=(16, 4))

        db  = self.master.db
        uid = self.master.user["id"]

        tab_bar = tk.Frame(self, bg=C["panel"])
        tab_bar.pack(fill="x", padx=0, pady=0)

        self._content = tk.Frame(self, bg=C["bg"])
        self._content.pack(fill="both", expand=True)

        tabs = [("🗺 Heatmap", self._show_heatmap),
                ("📈 Learning Curve", self._show_curve),
                ("🎯 Weak Spots", self._show_weak_spots)]
        for txt, cmd in tabs:
            make_button(tab_bar, txt, cmd, bg=C["accent2"],
                        font=FONT_SMALL, pad=(18, 8)).pack(side="left", padx=2, pady=4)

        make_button(self, "← Back", self.master.show_menu,
                    bg=C["accent2"], pad=(20, 8)).pack(side="bottom", pady=10)
        self._show_heatmap()

    def _clear_content(self):
        for w in self._content.winfo_children():
            w.destroy()

    def _show_heatmap(self):
        self._clear_content()
        db  = self.master.db
        uid = self.master.user["id"]
        cat_stats = db.get_category_stats(uid)

        make_label(self._content, "📊  Topic Heatmap",
                   font=FONT_LARGE, fg=C["cyan"], bg=C["bg"]).pack(pady=(12, 8))
        make_label(self._content, "Green = strong  |  Yellow = medium  |  Red = struggling",
                   font=FONT_SMALL, fg=C["muted"], bg=C["bg"]).pack(pady=(0, 10))

        grid_frame = tk.Frame(self._content, bg=C["bg"])
        grid_frame.pack(padx=40)

        categories = list(CARD_CATEGORIES.keys())
        for i, cat in enumerate(categories):
            correct, wrong = cat_stats.get(cat, [0, 0])
            total = correct + wrong
            if total == 0:
                ratio = 0.5
                color = C["muted"]
            else:
                ratio = correct / total
                if ratio >= 0.75:
                    color = C["green"]
                elif ratio >= 0.45:
                    color = C["yellow"]
                else:
                    color = C["accent"]

            col = i % 4
            row_i = i // 4

            cell = tk.Frame(grid_frame, bg=color, padx=12, pady=10,
                            width=180, height=90)
            cell.grid(row=row_i, column=col, padx=6, pady=6)
            cell.pack_propagate(False)

            tk.Label(cell, text=cat, font=("Segoe UI", 11, "bold"),
                     fg=C["bg"], bg=color, wraplength=160).pack()
            tk.Label(cell, text=f"✅{correct}  ❌{wrong}",
                     font=("Segoe UI", 10), fg=C["bg"], bg=color).pack()
            pct = f"{ratio*100:.0f}%" if total > 0 else "No data"
            tk.Label(cell, text=pct, font=("Segoe UI", 13, "bold"),
                     fg=C["bg"], bg=color).pack()

    def _show_curve(self):
        self._clear_content()
        db  = self.master.db
        uid = self.master.user["id"]

        make_label(self._content, "📈  Learning Curve (last 30 days)",
                   font=FONT_LARGE, fg=C["cyan"], bg=C["bg"]).pack(pady=(12, 6))

        data = db.get_accuracy_history(uid, days=30)
        if not data:
            make_label(self._content,
                       "No game history yet. Play some games to see your progress!",
                       font=FONT_MED, fg=C["muted"], bg=C["bg"]).pack(pady=40)
            return

        # Draw line chart on canvas
        W, H = 700, 300
        c = tk.Canvas(self._content, width=W, height=H,
                      bg=C["card"], highlightthickness=0)
        c.pack(pady=10, padx=40)

        pad = 60
        dates  = [r[0] for r in data]
        values = [float(r[1]) for r in data]
        n = len(values)

        c.create_line(pad, pad, pad, H-pad, fill=C["muted"], width=1)
        c.create_line(pad, H-pad, W-pad, H-pad, fill=C["muted"], width=1)

        # Grid lines and Y labels
        for pct in [0, 25, 50, 75, 100]:
            y = H - pad - (pct/100) * (H - 2*pad)
            c.create_line(pad, y, W-pad, y, fill=C["panel"], width=1, dash=(4,4))
            c.create_text(pad-8, y, text=f"{pct}%",
                          fill=C["muted"], font=("Segoe UI", 8), anchor="e")

        # Plot
        if n > 1:
            pts = []
            for i, v in enumerate(values):
                x = pad + i * ((W - 2*pad) / (n-1))
                y = H - pad - (v/100) * (H - 2*pad)
                pts.append((x, y))
            for i in range(len(pts)-1):
                c.create_line(pts[i][0], pts[i][1],
                              pts[i+1][0], pts[i+1][1],
                              fill=C["cyan"], width=2)
            for x, y in pts:
                c.create_oval(x-4, y-4, x+4, y+4, fill=C["cyan"], outline="")
        elif n == 1:
            x = (W) // 2
            y = H - pad - (values[0]/100) * (H - 2*pad)
            c.create_oval(x-5, y-5, x+5, y+5, fill=C["cyan"], outline="")

        # X labels (every other date)
        for i, d in enumerate(dates):
            if i % max(1, n//6) == 0:
                x = pad + i * ((W - 2*pad) / max(1, n-1))
                label = d[5:]  # MM-DD
                c.create_text(x, H-pad+14, text=label,
                              fill=C["muted"], font=("Segoe UI", 8), angle=0)

        # Latest value
        if values:
            last_val = values[-1]
            color = C["green"] if last_val >= 75 else C["yellow"] if last_val >= 45 else C["accent"]
            make_label(self._content,
                       f"Latest accuracy: {last_val:.1f}%",
                       font=FONT_MED, fg=color, bg=C["bg"]).pack()

    def _show_weak_spots(self):
        self._clear_content()
        db  = self.master.db
        uid = self.master.user["id"]
        weak = db.get_weak_spots(uid, n=5)

        make_label(self._content, "🎯  Weak Spots — Cards to Practice",
                   font=FONT_LARGE, fg=C["accent"], bg=C["bg"]).pack(pady=(12, 6))

        if not weak:
            make_label(self._content,
                       "No wrong answers recorded yet. Keep playing!",
                       font=FONT_MED, fg=C["muted"], bg=C["bg"]).pack(pady=40)
            return

        for rank, (term, correct, wrong) in enumerate(weak, 1):
            total = correct + wrong
            acc   = correct / total * 100 if total else 0
            panel = tk.Frame(self._content, bg=C["card"], padx=20, pady=12)
            panel.pack(fill="x", padx=80, pady=4)

            heat = C["accent"] if acc < 40 else C["yellow"] if acc < 70 else C["green"]

            left = tk.Frame(panel, bg=heat, width=8)
            left.pack(side="left", fill="y", padx=(0, 14))

            info = tk.Frame(panel, bg=C["card"])
            info.pack(side="left", fill="x", expand=True)
            tk.Label(info, text=f"#{rank}  {term}",
                     font=("Segoe UI", 14, "bold"),
                     fg=C["text"], bg=C["card"], anchor="w").pack(anchor="w")
            tk.Label(info, text=FLASHCARDS.get(term, ""),
                     font=FONT_SMALL, fg=C["muted"], bg=C["card"],
                     anchor="w", wraplength=500).pack(anchor="w")

            right = tk.Frame(panel, bg=C["card"])
            right.pack(side="right")
            tk.Label(right, text=f"❌ {wrong}  ✅ {correct}",
                     font=FONT_SMALL, fg=C["text"], bg=C["card"]).pack()
            tk.Label(right, text=f"{acc:.0f}% acc",
                     font=("Segoe UI", 12, "bold"), fg=heat, bg=C["card"]).pack()


# ══════════════════════════ VICTORY SCREEN ═══════════════════════════════════

class VictoryScreen(tk.Frame):
    def __init__(self, master, score, questions, new_badges):
        super().__init__(master, bg=C["bg"])
        self.score = score; self.questions = questions; self.new_badges = new_badges
        self._build()

    def _build(self):
        W, H = 960, 700
        c = tk.Canvas(self, width=W, height=H, bg=C["bg"], highlightthickness=0)
        c.pack(fill="both", expand=True)
        ConfettiCanvas(c, W, H)
        c.create_text(W//2, 160, text="🎉  YOU WIN! 🎉",
                      fill=C["yellow"], font=("Segoe UI", 44, "bold"))
        c.create_text(W//2, 230,
                      text=f"Score: {self.score}  |  Questions: {self.questions}",
                      fill=C["cyan"], font=FONT_LARGE)
        y = 290
        if self.new_badges:
            c.create_text(W//2, y, text="🏅 Badges Unlocked!",
                          fill=C["green"], font=FONT_LARGE); y += 40
            for b in self.new_badges:
                icon = next((a[2] for a in ACHIEVEMENTS if a[0] == b), "🏅")
                c.create_text(W//2, y, text=f"{icon}  {b}",
                              fill=C["yellow"], font=("Segoe UI", 18, "bold")); y += 36
        bf = tk.Frame(c, bg=C["bg"])
        c.create_window(W//2, 590, window=bf)
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
        W, H = 960, 700
        c = tk.Canvas(self, width=W, height=H, bg=C["bg"], highlightthickness=0)
        c.pack(fill="both", expand=True)
        ConfettiCanvas(c, W, H)
        header = "💾 CASHED OUT — NEW HIGH SCORE! 🔥" if self.cashout else "🔥 NEW HIGH SCORE! 🔥"
        c.create_text(W//2, 175, text=header,
                      fill=C["yellow"], font=("Segoe UI", 36, "bold"))
        self._hs_txt = c.create_text(W//2, 285, text="0",
                                     fill=C["cyan"], font=("Segoe UI", 72, "bold"))
        self._c = c
        self._count_up()
        bf = tk.Frame(c, bg=C["bg"])
        c.create_window(W//2, 430, window=bf)
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
            header = "💾  Cashed Out!";  hfg = C["green"]
            note   = "Your score was saved."
        else:
            header = "❌  Wrong Answer — Score Lost"; hfg = C["accent"]
            note   = "Wrong answer ends the run. Cash out next time to save your score!"
        make_label(self, header, font=("Segoe UI", 36, "bold"), fg=hfg).pack(pady=(70, 10))
        make_label(self, f"Your score: {self.score}", font=FONT_LARGE, fg=C["text"]).pack(pady=6)
        make_label(self, f"High Score: {self.prev_hs}", font=FONT_MED, fg=C["muted"]).pack(pady=6)
        make_label(self, note, font=FONT_SMALL, fg=C["muted"]).pack(pady=4)
        row = tk.Frame(self, bg=C["bg"]); row.pack(pady=24)
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
        make_label(self, f"Score: {self.score}", font=FONT_LARGE, fg=C["yellow"]).pack(pady=6)
        make_label(self, f"Questions answered: {self.questions}",
                   font=FONT_MED, fg=C["text"]).pack(pady=4)
        hs = self.master.user.get("speedrun_highscore", 0)
        if self.score >= hs and self.score > 0:
            make_label(self, "🏆 New Speedrun High Score!",
                       font=FONT_LARGE, fg=C["green"]).pack(pady=6)
        row = tk.Frame(self, bg=C["bg"]); row.pack(pady=24)
        mt = self.mode_type
        make_button(row, "▶ Play Again",
                    lambda: self.master.show_speedrun_mode(mt),
                    bg=C["orange"], pad=(20, 10)).pack(side="left", padx=10)
        make_button(row, "⚡ Other Modes", self.master.show_speedrun_menu,
                    bg=C["accent2"], pad=(20, 10)).pack(side="left", padx=10)
        make_button(row, "🏠 Menu", self.master.show_menu,
                    bg=C["purple"], pad=(20, 10)).pack(side="left", padx=10)


# ══════════════════════════ TIME WARP RESULT ═════════════════════════════════

class TimeWarpResultScreen(tk.Frame):
    def __init__(self, master, score, elapsed, questions):
        super().__init__(master, bg=C["bg"])
        self.score = score; self.elapsed = elapsed; self.questions = questions
        self._build()

    def _build(self):
        make_label(self, "🌀  Time Warp Complete!",
                   font=("Segoe UI", 34, "bold"), fg=C["teal"]).pack(pady=(60, 10))
        mins = self.elapsed // 60; secs = self.elapsed % 60
        make_label(self, f"Survived: {mins}m {secs}s",
                   font=FONT_LARGE, fg=C["cyan"]).pack(pady=6)
        make_label(self, f"Score: {self.score}",
                   font=FONT_LARGE, fg=C["yellow"]).pack(pady=4)
        make_label(self, f"Questions: {self.questions}",
                   font=FONT_MED, fg=C["text"]).pack(pady=4)
        hs = self.master.user.get("timewarp_highscore", 0)
        if self.score >= hs and self.score > 0:
            make_label(self, "🏆 New Time Warp High Score!",
                       font=FONT_LARGE, fg=C["green"]).pack(pady=6)
        row = tk.Frame(self, bg=C["bg"]); row.pack(pady=24)
        make_button(row, "▶ Play Again", self.master.show_timewarp_mode,
                    bg=C["teal"], pad=(20, 10)).pack(side="left", padx=10)
        make_button(row, "🏠 Menu", self.master.show_menu,
                    bg=C["accent2"], pad=(20, 10)).pack(side="left", padx=10)


# ══════════════════════════ REWARDS SCREEN ═══════════════════════════════════

class RewardsScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=C["bg"])
        self._build()

    def _build(self):
        make_label(self, "🏅  Badges & Rewards",
                   font=FONT_TITLE, fg=C["yellow"]).pack(pady=(14, 4))

        db     = self.master.db
        uid    = self.master.user["id"]
        earned = db.get_user_badge_names(uid)
        all_b  = db.get_all_badges()

        sf = tk.Frame(self, bg=C["panel"], pady=8, padx=20)
        sf.pack(fill="x", padx=40, pady=(0, 6))
        make_label(sf, f"Total Questions: {self.master.user['total_answered']}",
                   font=FONT_MED, fg=C["cyan"], bg=C["panel"]).pack(side="left")
        make_label(sf, f"  |  Badges: {len(earned)} / {len(all_b)}",
                   font=FONT_MED, fg=C["yellow"], bg=C["panel"]).pack(side="left")
        make_label(sf, f"  |  🪙 {self.master.user.get('coins',0)} coins",
                   font=FONT_MED, fg=C["orange"], bg=C["panel"]).pack(side="left")

        CATEGORIES = [
            ("🏆 Original",      ["First Time","Fast Learner","Flash Master","Endless 10","Endless 25","Endless 50"]),
            ("📈 Progress",      ["First Steps","Learning Curve","Knowledge Engine","Data Bank"]),
            ("⚡ Speed",         ["Lightning Brain","Human Cache","CPU Overclocked"]),
            ("♾ Endless",       ["Survivor","Untouchable","Legend","Infinity","Diamond Hands"]),
            ("💰 Risk",          ["Gambler","Risk Taker","High Roller","Balance"]),
            ("🏃 Speedrun",      ["Blitz Master","Marathon Runner","Reflex God","Lightning Rod","Sharpshooter","Ultramarathon"]),
            ("✨ Perfection",    ["Flawless","Bullseye","Memory Palace","Wizard"]),
            ("🎮 Fun & Hidden",  ["Database Brain","Night Coder","Addicted","Nostalgia","Tortoise","Hare","Owl","Joker"]),
            ("💻 Bonus",         ["Stack Overflow","Binary Master","Root Access","System Administrator"]),
            ("🔱 Skill",         ["Triple Threat","Puzzle Master","Omniscient"]),
            ("⚔ Multiplayer",   ["Duelist","Dominant"]),
            ("🌀 Time Warp",     ["Time Bender","Chrono Master"]),
            ("🛍 Power-Ups",     ["Coin Collector","Big Spender"]),
            ("📅 Daily",         ["Daily Champion","Daily Dedication","Weekly Warrior"]),
        ]

        badge_lookup = {row[0]: (row[1], row[2]) for row in all_b}

        # Scrollable container — FIXED bidirectional scrolling
        outer, scv, inner = make_scrollable(self)
        outer.pack(fill="both", expand=True, padx=40)

        for cat_name, badge_list in CATEGORIES:
            hf = tk.Frame(inner, bg=C["accent2"])
            hf.pack(fill="x", pady=(10, 3))
            tk.Label(hf, text=cat_name, font=("Segoe UI", 12, "bold"),
                     fg=C["white"], bg=C["accent2"], pady=4
                     ).pack(anchor="w", padx=12)

            for name in badge_list:
                if name not in badge_lookup: continue
                desc, icon = badge_lookup[name]
                unlocked   = name in earned
                row = tk.Frame(inner,
                               bg=C["card"] if unlocked else C["panel"],
                               pady=6, padx=14)
                row.pack(fill="x", pady=2)

                # Bind scroll on every sub-widget too
                def _bind_scroll(w, _scv=scv):
                    def _on_wheel(e, s=_scv):
                        s.yview_scroll(int(-1*(e.delta/120)), "units")
                    w.bind("<MouseWheel>", _on_wheel)
                    for child in w.winfo_children():
                        _bind_scroll(child)

                tk.Label(row, text=icon if unlocked else "🔒",
                         font=("Segoe UI", 18), bg=row["bg"],
                         fg=C["yellow"] if unlocked else C["muted"]
                         ).pack(side="left", padx=(0, 10))
                info = tk.Frame(row, bg=row["bg"])
                info.pack(side="left", fill="x", expand=True)
                tk.Label(info, text=name, font=("Segoe UI", 11, "bold"),
                         bg=row["bg"],
                         fg=C["text"] if unlocked else C["muted"],
                         anchor="w").pack(anchor="w")
                tk.Label(info, text=desc, font=FONT_SMALL, bg=row["bg"],
                         fg=C["muted"], anchor="w").pack(anchor="w")
                tk.Label(row, text="✓ Unlocked" if unlocked else "Locked",
                         font=("Segoe UI", 10, "bold"), bg=row["bg"],
                         fg=C["green"] if unlocked else C["muted"]
                         ).pack(side="right")

                _bind_scroll(row)

        make_button(self, "← Back to Menu", self.master.show_menu,
                    bg=C["accent2"], pad=(20, 8)).pack(pady=10)


# ══════════════════════════ LEADERBOARD ══════════════════════════════════════

class LeaderboardScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=C["bg"])
        self._build()

    def _build(self):
        make_label(self, "📊  Leaderboard",
                   font=FONT_TITLE, fg=C["cyan"]).pack(pady=(20, 14))

        rows = self.master.db.get_leaderboard()
        outer = tk.Frame(self, bg=C["bg"])
        outer.pack(fill="both", expand=True, padx=40)

        COLS = [
            ("Rank",     70,  0),
            ("Username", 180, 1),
            ("Endless",  90,  0),
            ("Speedrun", 90,  0),
            ("Badges",   70,  0),
            ("Total Q",  80,  0),
            ("🪙 Coins", 80,  0),
        ]

        hdr = tk.Frame(outer, bg=C["accent2"])
        hdr.pack(fill="x")
        for col_i, (label, w, flex) in enumerate(COLS):
            hdr.grid_columnconfigure(col_i, weight=flex, minsize=w)
        for col_i, (label, w, flex) in enumerate(COLS):
            tk.Label(hdr, text=label, font=("Segoe UI", 11, "bold"),
                     bg=C["accent2"], fg=C["white"],
                     padx=6, pady=7, anchor="center"
                     ).grid(row=0, column=col_i, sticky="ew")

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

        def _on_wheel(e):
            scv.yview_scroll(int(-1*(e.delta/120)), "units")
        scv.bind("<MouseWheel>", _on_wheel)
        body.bind("<MouseWheel>", _on_wheel)

        def _configure_row_cols(frame):
            for col_i, (_, w, flex) in enumerate(COLS):
                frame.grid_columnconfigure(col_i, weight=flex, minsize=w)

        MEDALS   = {1: "🥇", 2: "🥈", 3: "🥉"}
        MEDAL_FG = {1: C["yellow"], 2: "#c0c0c0", 3: "#cd7f32"}

        for i, row_data in enumerate(rows, 1):
            uname, hs, sp, bc, tq, coins = row_data
            bg_c      = C["card"] if i % 2 == 0 else C["panel"]
            medal     = MEDALS.get(i, f"#{i}")
            medal_clr = MEDAL_FG.get(i, C["text"])
            name_fg   = C["yellow"] if i <= 3 else C["text"]

            drow = tk.Frame(body, bg=bg_c)
            drow.pack(fill="x")
            _configure_row_cols(drow)

            cells = [
                (medal,    "center", medal_clr),
                (uname,    "w",      name_fg),
                (str(hs),  "center", C["green"]  if hs > 0 else C["muted"]),
                (str(sp),  "center", C["orange"] if sp > 0 else C["muted"]),
                (str(bc),  "center", C["yellow"] if bc > 0 else C["muted"]),
                (str(tq),  "center", C["cyan"]   if tq > 0 else C["muted"]),
                (str(coins),"center",C["orange"] if coins > 0 else C["muted"]),
            ]
            for col_i, (val, anc, fg) in enumerate(cells):
                tk.Label(drow, text=val, anchor=anc,
                         font=FONT_SMALL, bg=bg_c, fg=fg,
                         padx=6, pady=7
                         ).grid(row=0, column=col_i, sticky="ew")

        make_button(self, "← Back", self.master.show_menu,
                    bg=C["accent2"], pad=(20, 8)).pack(pady=14)


# ══════════════════════════ WEAK SPOTS (standalone) ══════════════════════════

class WeakSpotsScreen(tk.Frame):
    """Standalone screen navigable from old menu path."""
    def __init__(self, master):
        super().__init__(master, bg=C["bg"])
        self.master.show_stats()  # redirect to unified stats screen


# ══════════════════════════ HEATMAP (standalone) ══════════════════════════════

class HeatmapScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=C["bg"])
        self.master.show_stats()


# ══════════════════════════ ENTRY POINT ══════════════════════════════════════

if __name__ == "__main__":
    app = FlashcardApp()
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()
