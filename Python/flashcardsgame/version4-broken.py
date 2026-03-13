"""
CS Flashcard Game — Extended Edition
Extends the original with:
  • Speedrun modes (60s / 10min / Reflex)
  • Cash Out in Endless
  • 30+ new achievements with tier/dependency system
  • Expanded DB schema (auto-migrated)
  • 100+ new flashcards
  • Expanded leaderboard
Python 3 · Tkinter · SQLite3 only
"""

import tkinter as tk
from tkinter import ttk
import sqlite3
import random
import math
import time
import datetime

# ══════════════════════════════════════════════════════════════════════════════
#  FLASHCARD DATA  (original 25 + 100+ new terms)
# ══════════════════════════════════════════════════════════════════════════════

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

    # ── Programming ──────────────────────────────────────────────────────────
    "Recursion":      "A function that calls itself to solve sub-problems",
    "Polymorphism":   "OOP concept where one interface serves multiple types",
    "Inheritance":    "OOP mechanism where a class derives from another class",
    "Abstraction":    "Hiding complex implementation behind a simple interface",
    "Algorithm":      "Step-by-step procedure for solving a problem",
    "Encapsulation":  "Bundling data and methods that operate on the data together",
    "Compiler":       "Translates source code into machine code before execution",
    "Interpreter":    "Executes source code line-by-line at runtime",
    "Variable":       "Named storage location for a value in a program",
    "Function":       "Reusable block of code that performs a specific task",
    "Loop":           "Control structure that repeats code while a condition holds",
    "Condition":      "Boolean expression that controls branching in code",
    "Array":          "Ordered collection of elements of the same type",
    "Stack":          "LIFO data structure – last in, first out",
    "Queue":          "FIFO data structure – first in, first out",
    "Hash Table":     "Data structure mapping keys to values via a hash function",
    "Linked List":    "Linear structure where each element points to the next",
    "Tree":           "Hierarchical data structure with nodes and edges",
    "Graph":          "Collection of nodes connected by edges",
    "Binary Search":  "Efficient search by repeatedly halving the search space",
    "Sorting":        "Arranging elements in a defined order",
    "Debugging":      "Process of identifying and fixing errors in code",
    "Refactoring":    "Restructuring code without changing its external behaviour",
    "Version Control":"System tracking changes to code over time (e.g. Git)",
    "Git":            "Distributed version control system",
    "Commit":         "Snapshot of changes saved to a version control repository",
    "Branch":         "Parallel line of development in a repository",
    "Merge":          "Combining two branches of code into one",
    "Exception":      "Runtime error that interrupts normal program flow",
    "Callback":       "Function passed as an argument to be called later",
    "Closure":        "Function that captures variables from its enclosing scope",
    "Lambda":         "Anonymous function defined inline",
    "Iterator":       "Object that yields elements one at a time",
    "Generator":      "Function that lazily produces a sequence of values",
    "Decorator":      "Python construct that wraps a function to extend behaviour",
    "Thread":         "Lightweight unit of execution within a process",
    "Process":        "Independent program instance with its own memory space",
    "Mutex":          "Mutual exclusion lock preventing concurrent resource access",
    "Semaphore":      "Signalling mechanism controlling access to shared resources",
    "Deadlock":       "State where two processes each wait on the other to release a resource",
    "Race Condition": "Bug where output depends on non-deterministic execution order",
    "Big O":          "Notation describing algorithm time/space complexity",
    "Heap":           "Memory region for dynamic allocation; also a tree-based data structure",

    # ── Networking ───────────────────────────────────────────────────────────
    "TCP":       "Transmission Control Protocol – reliable, ordered data delivery",
    "UDP":       "User Datagram Protocol – fast, connectionless data delivery",
    "Packet":    "Unit of data transmitted over a network",
    "Port":      "Logical endpoint for network communication (0–65535)",
    "Firewall":  "Security system filtering incoming/outgoing network traffic",
    "Router":    "Device forwarding packets between networks",
    "Switch":    "Network device connecting devices within a LAN",
    "MAC Address":"Hardware identifier for a network interface card",
    "Subnet":    "Logical subdivision of an IP network",
    "NAT":       "Network Address Translation – maps private to public IPs",
    "DHCP":      "Dynamic Host Configuration Protocol – auto-assigns IP addresses",
    "FTP":       "File Transfer Protocol – for transferring files over a network",
    "SMTP":      "Simple Mail Transfer Protocol – for sending emails",
    "POP3":      "Post Office Protocol 3 – for receiving emails",
    "IMAP":      "Internet Message Access Protocol – email access on server",
    "WebSocket": "Protocol providing full-duplex communication over TCP",
    "CDN":       "Content Delivery Network – distributes content globally for speed",
    "Proxy":     "Intermediary server between client and destination",
    "Load Balancer":"Distributes network traffic across multiple servers",
    "Latency":   "Delay between sending a request and receiving a response",
    "Bandwidth": "Maximum data transfer rate of a network connection",
    "TLS":       "Transport Layer Security – cryptographic protocol for secure comms",
    "SSL":       "Secure Sockets Layer – predecessor to TLS",
    "OSI Model": "7-layer conceptual model for network communication",

    # ── Databases ────────────────────────────────────────────────────────────
    "Primary Key":  "Unique identifier for each record in a database table",
    "Foreign Key":  "Column referencing the primary key of another table",
    "Index":        "Database structure speeding up data retrieval",
    "Normalization":"Organizing a database to reduce redundancy",
    "Transaction":  "Sequence of DB operations treated as a single unit",
    "ACID":         "Atomicity, Consistency, Isolation, Durability – DB properties",
    "NoSQL":        "Non-relational database (documents, key-value, graph, etc.)",
    "Schema":       "Structure defining tables, columns, and relationships in a DB",
    "Query":        "Request to retrieve or manipulate data in a database",
    "ORM":          "Object-Relational Mapping – maps objects to DB tables",
    "JOIN":         "SQL operation combining rows from two or more tables",
    "View":         "Virtual table defined by a stored SQL query",
    "Stored Procedure":"Precompiled SQL code stored and executed on the DB server",
    "Trigger":      "DB procedure that runs automatically on a specified event",
    "Sharding":     "Splitting a database across multiple machines",
    "Replication":  "Copying data across multiple DB instances for redundancy",
    "Cache":        "Temporary storage for frequently accessed data",

    # ── Operating Systems ────────────────────────────────────────────────────
    "Kernel":     "Core of an OS managing hardware resources",
    "Scheduler":  "OS component deciding which process runs next",
    "Context Switch":"Saving/restoring CPU state when switching processes",
    "Virtual Memory":"Technique using disk space as extra RAM",
    "Page Fault":  "Interrupt when a process accesses a memory page not in RAM",
    "File System": "Method for organizing and storing files on storage media",
    "Interrupt":   "Signal to the CPU requiring immediate attention",
    "Daemon":      "Background process running without user interaction",
    "Shell":       "Command-line interface to the operating system",
    "Syscall":     "System call – interface between user programs and the kernel",
    "I/O":         "Input/Output – communication between CPU and external devices",
    "Driver":      "Software allowing the OS to communicate with hardware",
    "Bootloader":  "Software that loads the OS during startup",
    "Swap":        "Disk space used as overflow when RAM is full",
    "Pipe":        "Mechanism passing output of one process as input to another",

    # ── Security ─────────────────────────────────────────────────────────────
    "Encryption":     "Converting data to unreadable form without the key",
    "Hashing":        "One-way function mapping data to a fixed-size digest",
    "Authentication": "Verifying the identity of a user or system",
    "Authorisation":  "Granting permissions to authenticated users",
    "Public Key":     "Shared cryptographic key used to encrypt data",
    "Private Key":    "Secret cryptographic key used to decrypt data",
    "Digital Signature":"Cryptographic proof of data integrity and authenticity",
    "Certificate":    "Digital document binding a public key to an identity",
    "SQL Injection":  "Attack injecting malicious SQL into a query",
    "XSS":            "Cross-Site Scripting – injecting scripts into web pages",
    "CSRF":           "Cross-Site Request Forgery – tricks users into unwanted actions",
    "2FA":            "Two-Factor Authentication – requires two forms of verification",
    "OAuth":          "Open standard for access delegation (login with Google etc.)",
    "JWT":            "JSON Web Token – compact token for stateless auth",
    "Penetration Test":"Simulated cyberattack to find security vulnerabilities",
    "Zero-Day":       "Vulnerability unknown to the vendor with no patch yet",
    "Malware":        "Malicious software designed to damage or gain access",
    "Phishing":       "Social engineering attack using fake communications",

    # ── Web Development ──────────────────────────────────────────────────────
    "REST":       "Representational State Transfer – stateless HTTP API style",
    "GraphQL":    "Query language for APIs allowing precise data fetching",
    "Session":    "Server-side storage of user state across requests",
    "Cookie":     "Small data stored in the browser by a website",
    "Middleware":  "Software layer between OS/server and applications",
    "Backend":    "Server-side logic, databases, and APIs",
    "Frontend":   "Client-side UI and interactions in the browser",
    "DOM":        "Document Object Model – tree representation of HTML",
    "SPA":        "Single Page Application – loads once, updates dynamically",
    "PWA":        "Progressive Web App – web app with native-like features",
    "Webpack":    "Module bundler for JavaScript applications",
    "MVC":        "Model-View-Controller – architectural pattern",
    "CORS":       "Cross-Origin Resource Sharing – browser security mechanism",
    "CDN":        "Content Delivery Network – speeds up static asset delivery",
    "Microservice":"Independently deployable small service in a larger system",
    "Docker":     "Platform for building and running containerised applications",
    "Container":  "Lightweight isolated runtime environment for applications",
    "Kubernetes": "System for automating container deployment and scaling",
    "CI/CD":      "Continuous Integration/Delivery – automated build and deploy",
    "Serverless": "Cloud execution model where infrastructure is fully managed",
    "WebAssembly":"Binary instruction format running in browsers near-natively",
}

# ══════════════════════════════════════════════════════════════════════════════
#  BADGE / ACHIEVEMENT DEFINITIONS
# ══════════════════════════════════════════════════════════════════════════════

# Each entry: (name, description, icon, unlock_condition_hint, depends_on_names)
# depends_on_names: list of badge names that must be earned first (empty = always available)
BADGE_DEFS = [
    # ── Original badges ───────────────────────────────────────────────────────
    ("First Time",    "Win Normal Mode once",                   "🏆", "", []),
    ("Fast Learner",  "Win Normal Mode in under 15 questions",  "⚡", "", []),
    ("Endless 10",    "Score 10+ in Endless Mode",              "🔥", "", []),
    ("Endless 25",    "Score 25+ in Endless Mode",              "💎", "", []),
    ("Endless 50",    "Score 50+ in Endless Mode",              "👑", "", []),
    ("Flash Master",  "Answer 100 cards total",                 "🎓", "", []),

    # ── Progress achievements ─────────────────────────────────────────────────
    ("First Steps",      "Answer 10 cards",      "👣", "Answer 10 cards total",  []),
    ("Learning Curve",   "Answer 50 cards",      "📈", "Answer 50 cards total",  ["First Steps"]),
    ("Knowledge Engine", "Answer 250 cards",     "🧠", "Answer 250 cards total", ["Learning Curve"]),
    ("Data Bank",        "Answer 500 cards",     "🗄️", "Answer 500 cards total", ["Knowledge Engine"]),

    # ── Speed achievements ────────────────────────────────────────────────────
    ("Lightning Brain",  "Answer 5 questions in under 30 seconds", "🌩️", "5 answers in 30s",    []),
    ("Human Cache",      "Answer 10 in a row without revealing",   "💡", "10 no-reveal streak", ["First Steps"]),
    ("CPU Overclocked",  "20 correct answers in a row",            "🖥️", "20-answer streak",    ["Learning Curve"]),

    # ── Endless achievements ──────────────────────────────────────────────────
    ("Survivor",     "Reach score 15 in Endless",  "🛡️", "Score 15 in Endless",  []),
    ("Untouchable",  "Reach score 30 in Endless",  "🔒", "Score 30 in Endless",  ["Survivor"]),
    ("Legend",       "Reach score 75 in Endless",  "🌟", "Score 75 in Endless",  ["Survivor", "Untouchable"]),

    # ── Risk achievements ─────────────────────────────────────────────────────
    ("Gambler",    "Cash out Endless with exactly 1 point",   "🎰", "Cash out at score 1", []),
    ("Risk Taker", "Cash out Endless with 20+ points",        "🎲", "Cash out at 20+",    []),

    # ── Speedrun achievements ─────────────────────────────────────────────────
    ("Blitz Master",    "Score 20+ in 60-second mode",        "⚡", "20 pts in 60s",       []),
    ("Marathon Runner", "Score 100+ in 10-minute mode",       "🏃", "100 pts in 10min",    []),
    ("Reflex God",      "Survive 30 questions in Reflex mode","🎯", "30 Qs in Reflex",     []),

    # ── Perfection achievements ───────────────────────────────────────────────
    ("Flawless",       "Win Normal Mode without any mistakes",        "✨", "Zero wrong in Normal",       []),
    ("Memory Palace",  "Win Normal Mode without revealing answers",   "🏛️", "Win without reveals",       []),

    # ── Fun achievements ──────────────────────────────────────────────────────
    ("Database Brain", "See every flashcard in one session",   "🔮", "All cards in one session", []),
    ("Night Coder",    "Play after midnight",                  "🦉", "Play after 00:00",         []),
    ("Addicted",       "Play 5 games in a row",                "🎮", "5 consecutive games",      []),

    # ── Bonus achievements ────────────────────────────────────────────────────
    ("Stack Overflow",       "Answer 404 questions total",    "🌊", "404 total answers",   ["Flash Master"]),
    ("Binary Master",        "Reach score 32 in Endless",     "01", "Score 32 in Endless", ["Endless 25"]),
    ("Root Access",          "Unlock 10 badges",              "🔑", "Earn 10 badges",      []),
    ("System Administrator", "Unlock 20 badges",              "👨‍💻","Earn 20 badges",     ["Root Access"]),
]

# ══════════════════════════════════════════════════════════════════════════════
#  COLOUR PALETTE  (original palette preserved)
# ══════════════════════════════════════════════════════════════════════════════

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
}

FONT_TITLE = ("Segoe UI", 28, "bold")
FONT_LARGE = ("Segoe UI", 18, "bold")
FONT_MED   = ("Segoe UI", 14)
FONT_SMALL = ("Segoe UI", 11)
FONT_MONO  = ("Consolas", 13)

# ══════════════════════════════════════════════════════════════════════════════
#  DATABASE MANAGER
# ══════════════════════════════════════════════════════════════════════════════

class DatabaseManager:
    """Handles all SQLite operations and auto-migrates the schema."""

    def __init__(self, db_path="flashcard_game.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()
        self._migrate()
        self._seed_badges()

    # ── Schema creation ───────────────────────────────────────────────────────

    def _create_tables(self):
        self.conn.executescript("""
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

    def _migrate(self):
        """Safely add new columns / tables if they don't exist yet."""
        cur = self.conn.cursor()

        # New columns on users
        new_user_cols = [
            ("total_correct",           "INTEGER DEFAULT 0"),
            ("games_played",            "INTEGER DEFAULT 0"),
            ("current_streak",          "INTEGER DEFAULT 0"),
            ("longest_streak",          "INTEGER DEFAULT 0"),
            ("questions_without_reveal","INTEGER DEFAULT 0"),
            ("last_play_time",          "TEXT DEFAULT ''"),
            ("speedrun_highscore",      "INTEGER DEFAULT 0"),
            ("consecutive_games",       "INTEGER DEFAULT 0"),
        ]
        existing = {row[1] for row in
                    cur.execute("PRAGMA table_info(users)").fetchall()}
        for col, typedef in new_user_cols:
            if col not in existing:
                cur.execute(f"ALTER TABLE users ADD COLUMN {col} {typedef}")

        # New columns on badges
        badge_cols = [
            ("depends_on", "TEXT DEFAULT ''"),
            ("condition_hint", "TEXT DEFAULT ''"),
        ]
        existing_b = {row[1] for row in
                      cur.execute("PRAGMA table_info(badges)").fetchall()}
        for col, typedef in badge_cols:
            if col not in existing_b:
                cur.execute(f"ALTER TABLE badges ADD COLUMN {col} {typedef}")

        # game_history table
        cur.executescript("""
            CREATE TABLE IF NOT EXISTS game_history (
                id                INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id           INTEGER,
                mode              TEXT,
                score             INTEGER,
                questions_answered INTEGER,
                timestamp         TEXT
            );
        """)
        self.conn.commit()

    def _seed_badges(self):
        cur = self.conn.cursor()
        for name, desc, icon, hint, deps in BADGE_DEFS:
            cur.execute("""
                INSERT OR IGNORE INTO badges
                    (badge_name, description, icon, condition_hint, depends_on)
                VALUES (?,?,?,?,?)
            """, (name, desc, icon, hint, ",".join(deps)))
            # Update depends_on / hint for existing rows (schema may have been empty)
            cur.execute("""
                UPDATE badges SET condition_hint=?, depends_on=?
                WHERE badge_name=? AND (condition_hint='' OR condition_hint IS NULL)
            """, (hint, ",".join(deps), name))
        self.conn.commit()

    # ── User helpers ──────────────────────────────────────────────────────────

    def user_exists(self, username):
        return self.conn.execute(
            "SELECT id FROM users WHERE username=?", (username,)
        ).fetchone() is not None

    def verify_code(self, username, code):
        return self.conn.execute(
            "SELECT id FROM users WHERE username=? AND code=?", (username, code)
        ).fetchone() is not None

    def create_user(self, username, code):
        self.conn.execute(
            "INSERT INTO users (username, code) VALUES (?,?)", (username, code))
        self.conn.commit()

    def get_user(self, username):
        row = self.conn.execute(
            "SELECT * FROM users WHERE username=?", (username,)).fetchone()
        return dict(row) if row else None

    def get_user_by_id(self, uid):
        row = self.conn.execute(
            "SELECT * FROM users WHERE id=?", (uid,)).fetchone()
        return dict(row) if row else None

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

    def increment_total_answered(self, user_id, count):
        self.conn.execute(
            "UPDATE users SET total_answered=total_answered+? WHERE id=?",
            (count, user_id))
        self.conn.commit()

    def increment_total_correct(self, user_id, count):
        self.conn.execute(
            "UPDATE users SET total_correct=total_correct+? WHERE id=?",
            (count, user_id))
        self.conn.commit()

    def update_streak(self, user_id, streak):
        self.conn.execute("""
            UPDATE users SET current_streak=?,
                longest_streak=MAX(longest_streak,?)
            WHERE id=?""", (streak, streak, user_id))
        self.conn.commit()

    def increment_games_played(self, user_id):
        self.conn.execute(
            "UPDATE users SET games_played=games_played+1 WHERE id=?", (user_id,))
        self.conn.commit()

    def update_consecutive_games(self, user_id, n):
        self.conn.execute(
            "UPDATE users SET consecutive_games=? WHERE id=?", (n, user_id))
        self.conn.commit()

    def set_last_play_time(self, user_id):
        now = datetime.datetime.now().isoformat()
        self.conn.execute(
            "UPDATE users SET last_play_time=? WHERE id=?", (now, user_id))
        self.conn.commit()

    # ── Badge helpers ─────────────────────────────────────────────────────────

    def award_badge(self, user_id, badge_name):
        row = self.conn.execute(
            "SELECT id FROM badges WHERE badge_name=?", (badge_name,)).fetchone()
        if not row:
            return False
        bid = row["id"]
        if self.conn.execute(
                "SELECT 1 FROM user_badges WHERE user_id=? AND badge_id=?",
                (user_id, bid)).fetchone():
            return False
        self.conn.execute(
            "INSERT INTO user_badges (user_id, badge_id) VALUES (?,?)",
            (user_id, bid))
        self.conn.commit()
        return True

    def get_user_badge_names(self, user_id):
        rows = self.conn.execute("""
            SELECT b.badge_name FROM badges b
            JOIN user_badges ub ON b.id=ub.badge_id
            WHERE ub.user_id=?""", (user_id,)).fetchall()
        return {r["badge_name"] for r in rows}

    def get_all_badges(self):
        return self.conn.execute(
            "SELECT badge_name, description, icon, condition_hint, depends_on "
            "FROM badges").fetchall()

    def count_user_badges(self, user_id):
        row = self.conn.execute(
            "SELECT COUNT(*) as n FROM user_badges WHERE user_id=?",
            (user_id,)).fetchone()
        return row["n"] if row else 0

    # ── Game history ──────────────────────────────────────────────────────────

    def log_game(self, user_id, mode, score, questions):
        now = datetime.datetime.now().isoformat()
        self.conn.execute(
            "INSERT INTO game_history(user_id,mode,score,questions_answered,timestamp)"
            " VALUES(?,?,?,?,?)",
            (user_id, mode, score, questions, now))
        self.conn.commit()

    # ── Leaderboard ───────────────────────────────────────────────────────────

    def get_leaderboard(self):
        return self.conn.execute("""
            SELECT u.username,
                   u.endless_highscore,
                   u.speedrun_highscore,
                   u.total_answered,
                   COUNT(ub.badge_id) AS badge_count
            FROM users u
            LEFT JOIN user_badges ub ON u.id=ub.user_id
            GROUP BY u.id
            ORDER BY u.endless_highscore DESC
        """).fetchall()

    def close(self):
        self.conn.close()


# ══════════════════════════════════════════════════════════════════════════════
#  ACHIEVEMENT ENGINE
# ══════════════════════════════════════════════════════════════════════════════

class AchievementEngine:
    """
    Checks and awards badges. All badge logic is centralised here.
    Returns a list of newly-awarded badge names.
    """

    def __init__(self, db: DatabaseManager):
        self.db = db

    def check_all(self, user_id, context: dict) -> list:
        """
        context keys (all optional):
          mode, score, questions, correct_streak, no_reveal_streak,
          time_elapsed, cashed_out, speedrun_variant,
          cards_seen_this_session, wrongs_this_game, reveals_this_game
        """
        db      = self.db
        user    = db.get_user_by_id(user_id)
        earned  = db.get_user_badge_names(user_id)
        awarded = []

        def _try(name):
            # Check dependency gates
            for bd in BADGE_DEFS:
                if bd[0] == name:
                    deps = bd[4]
                    if any(d not in earned for d in deps):
                        return False
                    break
            if db.award_badge(user_id, name):
                earned.add(name)
                awarded.append(name)
                return True
            return False

        total  = user.get("total_answered", 0)
        mode   = context.get("mode", "")
        score  = context.get("score", 0)
        qs     = context.get("questions", 0)

        # ── Progress ──────────────────────────────────────────────────────────
        if total >= 10:  _try("First Steps")
        if total >= 50:  _try("Learning Curve")
        if total >= 100: _try("Flash Master")
        if total >= 250: _try("Knowledge Engine")
        if total >= 404: _try("Stack Overflow")
        if total >= 500: _try("Data Bank")

        # ── Normal mode ───────────────────────────────────────────────────────
        if mode == "normal" and score >= 11:
            _try("First Time")
            if qs < 15:
                _try("Fast Learner")
            if context.get("wrongs_this_game", 1) == 0:
                _try("Flawless")
            if context.get("reveals_this_game", 1) == 0:
                _try("Memory Palace")

        # ── Endless ───────────────────────────────────────────────────────────
        if mode in ("endless", "endless_cashout"):
            if score >= 10: _try("Endless 10")
            if score >= 15: _try("Survivor")
            if score >= 25: _try("Endless 25")
            if score >= 30: _try("Untouchable")
            if score >= 32: _try("Binary Master")
            if score >= 50: _try("Endless 50")
            if score >= 75: _try("Legend")
            if mode == "endless_cashout":
                if score == 1: _try("Gambler")
                if score >= 20: _try("Risk Taker")

        # ── Speedrun ──────────────────────────────────────────────────────────
        variant = context.get("speedrun_variant", "")
        if mode == "speedrun":
            if variant == "60s"  and score >= 20:  _try("Blitz Master")
            if variant == "10min" and score >= 100: _try("Marathon Runner")
            if variant == "reflex" and qs >= 30:   _try("Reflex God")

        # ── Speed / streak ────────────────────────────────────────────────────
        if context.get("time_elapsed", 999) < 30 and qs >= 5:
            _try("Lightning Brain")
        if context.get("no_reveal_streak", 0) >= 10:
            _try("Human Cache")
        if context.get("correct_streak", 0) >= 20:
            _try("CPU Overclocked")

        # ── Session ───────────────────────────────────────────────────────────
        if context.get("cards_seen_this_session", 0) >= len(FLASHCARDS):
            _try("Database Brain")

        # ── Night coder ───────────────────────────────────────────────────────
        hour = datetime.datetime.now().hour
        if hour == 0 or hour < 4:
            _try("Night Coder")

        # ── Consecutive games ─────────────────────────────────────────────────
        consec = user.get("consecutive_games", 0) + 1
        db.update_consecutive_games(user_id, consec)
        if consec >= 5:
            _try("Addicted")

        # ── Badge count milestones ────────────────────────────────────────────
        badge_count = db.count_user_badges(user_id)
        if badge_count >= 10: _try("Root Access")
        if badge_count >= 20: _try("System Administrator")

        return awarded


# ══════════════════════════════════════════════════════════════════════════════
#  ANIMATION HELPERS
# ══════════════════════════════════════════════════════════════════════════════

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
    COLORS = ["#e94560", "#ffd700", "#00d4ff", "#00d26a", "#7b2fff", "#ff6b6b"]

    def __init__(self, canvas, width, height):
        self.canvas = canvas
        self.w = width; self.h = height
        self.particles = []
        self._spawn()

    def _spawn(self):
        for _ in range(80):
            x     = random.randint(0, self.w)
            y     = random.randint(-self.h, 0)
            size  = random.randint(6, 14)
            color = random.choice(self.COLORS)
            speed = random.uniform(3, 8)
            drift = random.uniform(-2, 2)
            spin  = random.uniform(-5, 5)
            item  = self.canvas.create_rectangle(
                x, y, x+size, y+size, fill=color, outline="")
            self.particles.append([x, y, size, speed, drift, 0.0, spin, item])
        self._animate()

    def _animate(self):
        for p in self.particles:
            p[1] += p[3]; p[0] += p[4]; p[5] += p[6]
            if p[1] > self.h:
                p[1] = random.randint(-60, -10)
                p[0] = random.randint(0, self.w)
            rad = math.radians(p[5])
            x1  = p[0] + p[2]*math.cos(rad)
            y1  = p[1] + p[2]*math.sin(rad)
            self.canvas.coords(p[7], p[0], p[1], x1, y1)
        self.canvas.after(30, self._animate)


# ══════════════════════════════════════════════════════════════════════════════
#  WIDGET HELPERS  (original API preserved)
# ══════════════════════════════════════════════════════════════════════════════

def _lighten(hex_color, amount):
    h = hex_color.lstrip("#")
    r = max(0, min(255, int(h[0:2], 16) + amount))
    g = max(0, min(255, int(h[2:4], 16) + amount))
    b = max(0, min(255, int(h[4:6], 16) + amount))
    return f"#{r:02x}{g:02x}{b:02x}"


def make_button(parent, text, command, bg=C["accent"], fg=C["white"],
                font=FONT_MED, pad=(20, 10), width=None):
    """Label-based button — macOS / Windows / Linux safe."""
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


# ══════════════════════════════════════════════════════════════════════════════
#  ACHIEVEMENT POPUP  — floats over any screen
# ══════════════════════════════════════════════════════════════════════════════

class AchievementPopup(tk.Toplevel):
    """
    Small animated popup shown when a badge is awarded.
    Auto-closes after 3 seconds.
    """
    def __init__(self, master, badge_name):
        super().__init__(master)
        self.overrideredirect(True)          # no window chrome
        self.attributes("-topmost", True)
        self.configure(bg=C["panel"])

        icon = next((b[2] for b in BADGE_DEFS if b[0] == badge_name), "🏅")
        tk.Label(self, text="🔓 Achievement Unlocked!",
                 font=("Segoe UI", 11, "bold"),
                 fg=C["yellow"], bg=C["panel"]).pack(padx=18, pady=(10, 2))
        tk.Label(self, text=f"{icon}  {badge_name}",
                 font=("Segoe UI", 13, "bold"),
                 fg=C["cyan"], bg=C["panel"]).pack(padx=18, pady=(0, 10))

        # Position bottom-right of master
        self.update_idletasks()
        mw = master.winfo_width();  mx = master.winfo_x()
        mh = master.winfo_height(); my = master.winfo_y()
        pw = self.winfo_width();    ph = self.winfo_height()
        self.geometry(f"+{mx+mw-pw-20}+{my+mh-ph-60}")

        self._alpha = 1.0
        self.after(2200, self._fade)

    def _fade(self):
        self._alpha -= 0.08
        if self._alpha <= 0:
            self.destroy(); return
        try:
            self.attributes("-alpha", max(0, self._alpha))
            self.after(40, self._fade)
        except: pass


def show_achievements(master, new_badges, delay=0):
    """Queue popups for each newly awarded badge."""
    for i, name in enumerate(new_badges):
        master.after(delay + i * 700, lambda n=name: AchievementPopup(master, n))


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN APPLICATION
# ══════════════════════════════════════════════════════════════════════════════

class FlashcardApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("CS Flashcard Game — Extended")
        self.geometry("960x680")
        self.resizable(True, True)
        self.configure(bg=C["bg"])
        self.minsize(720, 540)

        self._fullscreen    = False
        self._current_frame = None

        self.bind("<F11>",    lambda e: self.toggle_fullscreen())
        self.bind("<Escape>", lambda e: self.exit_fullscreen())

        self.db      = DatabaseManager()
        self.achieve = AchievementEngine(self.db)
        self.user    = None

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
    def show_speedrun_menu(self):self.show_frame(SpeedrunMenuScreen)
    def show_rewards(self):      self.show_frame(RewardsScreen)
    def show_leaderboard(self):  self.show_frame(LeaderboardScreen)

    def on_close(self):
        self.db.close()
        self.destroy()


# ══════════════════════════════════════════════════════════════════════════════
#  LOGIN SCREEN
# ══════════════════════════════════════════════════════════════════════════════

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
        tk.Label(panel, textvariable=self._msg,
                 bg=C["panel"], fg="#ff6b6b", font=FONT_SMALL).pack()

    def _proceed(self):
        username = self._uvar.get().strip()
        if not username:
            self._msg.set("Please enter a username."); return
        db = self.master.db
        CodeDialog(self.master, username, new_user=not db.user_exists(username))


# ── Code dialog ───────────────────────────────────────────────────────────────

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
               f"Welcome back, {self.username}!\nEnter your 4-digit code:")
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


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN MENU
# ══════════════════════════════════════════════════════════════════════════════

class MainMenu(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=C["bg"])
        self._build()

    def _build(self):
        user = self.master.user
        make_label(self, f"Welcome, {user['username']}  👋",
                   font=FONT_TITLE, fg=C["cyan"]).pack(pady=(30, 2))
        make_label(self, f"Endless High Score: {user['endless_highscore']}",
                   font=FONT_SMALL, fg=C["yellow"]).pack(pady=(0, 20))

        btns = [
            ("▶  Play Normal Mode",   C["accent"],   self.master.show_normal_mode),
            ("♾  Endless Mode",       C["purple"],   self.master.show_endless_mode),
            ("⚡  Speedrun Mode",      C["orange"],   self.master.show_speedrun_menu),
            ("🏅  Rewards / Badges",  "#1a6b3c",     self.master.show_rewards),
            ("📊  Leaderboard",       C["accent2"],  self.master.show_leaderboard),
            ("✕  Quit Game",          "#333344",     self._quit),
        ]
        for text, color, cmd in btns:
            make_button(self, text, cmd, bg=color,
                        font=FONT_LARGE, pad=(40, 12), width=28).pack(pady=5)

        fs_row = tk.Frame(self, bg=C["bg"])
        fs_row.pack(pady=(8, 0))
        self._fs_btn = make_button(
            fs_row, self._fs_label(), self._toggle_fs,
            bg="#2a2a3e", font=FONT_SMALL, pad=(16, 7))
        self._fs_btn.pack()
        make_label(fs_row, "  F11 to toggle  ",
                   font=("Segoe UI", 9), fg=C["muted"]).pack()

    def _quit(self): self.master.on_close()

    def _fs_label(self):
        return "⛶  Exit Fullscreen" if self.master._fullscreen else "⛶  Fullscreen"

    def _toggle_fs(self):
        self.master.toggle_fullscreen()
        self._fs_btn.config(text=self._fs_label())


# ══════════════════════════════════════════════════════════════════════════════
#  BASE GAME SCREEN
# ══════════════════════════════════════════════════════════════════════════════

class BaseGameScreen(tk.Frame):
    """
    Shared UI and logic for Normal and Endless modes.
    Tracks: correct streak, no-reveal streak, session card set,
            time per batch (for Lightning Brain), reveals and wrongs.
    """

    def __init__(self, master, mode):
        super().__init__(master, bg=C["bg"])
        self.mode      = mode
        self.score     = 0
        self.questions = 0
        self._deck     = list(FLASHCARDS.keys())
        random.shuffle(self._deck)
        self._deck_idx = 0
        self._revealed = False

        # Tracking for achievements
        self._correct_streak    = 0
        self._no_reveal_streak  = 0
        self._wrongs_this_game  = 0
        self._reveals_this_game = 0
        self._session_cards     = set()
        self._batch_start_time  = time.time()
        self._batch_count       = 0   # answers since last batch timer reset

        self._build_ui()
        self._next_card()

    def _build_ui(self):
        top = tk.Frame(self, bg=C["bg"])
        top.pack(fill="x", padx=20, pady=10)

        make_button(top, "← Menu", self._back_to_menu,
                    bg=C["accent2"], font=FONT_SMALL, pad=(10, 5)).pack(side="left")

        title = ("Normal Mode  (reach 11 pts)"
                 if self.mode == "normal" else "Endless Mode")
        make_label(top, title, font=FONT_LARGE,
                   fg=C["cyan"], bg=C["bg"]).pack(side="left", padx=20)

        self.score_lbl = make_label(top, "Score: 0",
                                    font=FONT_LARGE, fg=C["yellow"], bg=C["bg"])
        self.score_lbl.pack(side="right")

        # Progress bar (Normal) or Cash Out button (Endless)
        if self.mode == "normal":
            self._pb_canvas = tk.Canvas(self, height=22, bg=C["bg"],
                                        highlightthickness=0)
            self._pb_canvas.pack(fill="x", padx=20, pady=(0, 10))
            self._pb_value  = 0.0
            self._pb_target = 0.0
            self._pb_color  = C["green"]
            self._pb_canvas.bind(
                "<Configure>", lambda e: self._pb_draw(self._pb_value))
        elif self.mode == "endless":
            co_row = tk.Frame(self, bg=C["bg"])
            co_row.pack(fill="x", padx=20, pady=(0, 4))
            self._cashout_btn = make_button(
                co_row, "💾  Cash Out",
                self._cash_out,
                bg="#1a4a1a", fg=C["green"],
                font=FONT_SMALL, pad=(14, 5))
            self._cashout_btn.pack(side="left")
            make_label(co_row, "  save your score and end the run",
                       font=("Segoe UI", 9), fg=C["muted"], bg=C["bg"]).pack(
                           side="left", padx=6)

        # Card canvas
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

        # Buttons
        btn_row = tk.Frame(self, bg=C["bg"])
        btn_row.pack(pady=8)

        self.reveal_btn = make_button(
            btn_row, "👁  Reveal Answer", self._reveal,
            bg=C["accent2"], font=FONT_LARGE, pad=(30, 12))
        self.reveal_btn.pack(side="left", padx=10)

        self.correct_btn = make_button(
            btn_row, "✅ Correct  +1",
            lambda: self._answer(True),
            bg=C["green"], font=FONT_LARGE, pad=(20, 12))
        self.wrong_btn = make_button(
            btn_row,
            "❌ Wrong  -2" if self.mode == "normal" else "❌ Wrong",
            lambda: self._answer(False),
            bg=C["accent"], font=FONT_LARGE, pad=(20, 12))
        self.correct_btn.pack_forget()
        self.wrong_btn.pack_forget()

        self.q_lbl = make_label(self, "Questions answered: 0",
                                font=FONT_SMALL, fg=C["muted"])
        self.q_lbl.pack()

    def _draw_card_bg(self):
        self.canvas.create_rectangle(
            10, 10, 850, 270,
            fill=C["card"], outline=C["accent2"], width=2)

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
        self._session_cards.add(term)
        self.canvas.itemconfig(self.term_text, text=term)
        self.canvas.itemconfig(self.ans_text, text="")

    def _reveal(self):
        if self._revealed: return
        self._revealed = True
        self._reveals_this_game += 1
        self._no_reveal_streak   = 0
        self.canvas.itemconfig(self.ans_text, text=FLASHCARDS[self._current_term])
        self.reveal_btn.pack_forget()
        self.correct_btn.pack(side="left", padx=10)
        self.wrong_btn.pack(side="left", padx=10)

    def _answer(self, correct):
        self.questions += 1
        self.q_lbl.config(text=f"Questions answered: {self.questions}")
        if not self._revealed:
            self._no_reveal_streak += 1
        if correct:
            self.score += 1
            self._correct_streak += 1
            self._batch_count    += 1
            self._float("+1", C["green"])
        else:
            self._correct_streak = 0
            self._wrongs_this_game += 1
            self._on_wrong()
            return
        self._update_score_display()
        self._check_win()
        self._next_card()

    def _float(self, text, color):
        cx = (self.canvas.winfo_width() or 430) // 2
        FloatingText(self.canvas, cx, 140, text, color,
                     font=("Segoe UI", 26, "bold"))

    def _on_wrong(self):
        """Override in subclasses."""
        pass

    def _cash_out(self):
        """Override in Endless subclass."""
        pass

    def _update_score_display(self, wrong=False):
        self.score_lbl.config(text=f"Score: {self.score}")
        if self.mode == "normal":
            self._pb_target = max(0.0, float(self.score))
            if wrong:
                self._pb_flash_red()
            else:
                self._pb_color = C["green"]
                self._pb_animate_fill()

    def _check_win(self):
        pass

    def _back_to_menu(self):
        self.master.show_menu()

    def _build_context(self):
        """Build the context dict for AchievementEngine."""
        elapsed = time.time() - self._batch_start_time
        return {
            "mode":                 self.mode,
            "score":                self.score,
            "questions":            self.questions,
            "correct_streak":       self._correct_streak,
            "no_reveal_streak":     self._no_reveal_streak,
            "time_elapsed":         elapsed if self._batch_count >= 5 else 999,
            "cards_seen_this_session": len(self._session_cards),
            "wrongs_this_game":     self._wrongs_this_game,
            "reveals_this_game":    self._reveals_this_game,
        }

    # ── Progress bar ──────────────────────────────────────────────────────────

    def _pb_draw(self, val, offset=0):
        c = self._pb_canvas
        W = c.winfo_width(); H = c.winfo_height()
        if W < 2: return
        c.delete("all")
        c.create_rectangle(0, 3, W, H-3, fill=C["card"], outline="")
        fw = int((val / 11) * W)
        if fw > 0:
            x0 = max(0, offset); x1 = min(W, fw+offset)
            if x1 > x0:
                c.create_rectangle(x0, 3, x1, H-3,
                                   fill=self._pb_color, outline="")
        for i in range(1, 11):
            x = int((i/11)*W)+offset
            c.create_line(x, 3, x, H-3, fill=C["bg"], width=2)

    def _pb_animate_fill(self):
        diff = self._pb_target - self._pb_value
        if abs(diff) < 0.01:
            self._pb_value = self._pb_target
            self._pb_draw(self._pb_value)
            return
        self._pb_value += diff * 0.18
        self._pb_draw(self._pb_value)
        self.after(16, self._pb_animate_fill)

    def _pb_flash_red(self):
        self._pb_color = C["accent"]
        self._pb_animate_fill()
        self._pb_shake(6, 0)
        self.after(2000, self._pb_restore_green)

    def _pb_shake(self, remaining, direction):
        if remaining <= 0:
            self._pb_draw(self._pb_value); return
        offset = 7 * (1 if direction % 2 == 0 else -1)
        self._pb_draw(self._pb_value, offset)
        self.after(40, lambda: self._pb_shake(remaining-1, direction+1))

    def _pb_restore_green(self):
        self._pb_color = C["green"]
        self._pb_draw(self._pb_value)


# ══════════════════════════════════════════════════════════════════════════════
#  NORMAL MODE
# ══════════════════════════════════════════════════════════════════════════════

class NormalModeScreen(BaseGameScreen):
    def __init__(self, master):
        super().__init__(master, "normal")

    def _on_wrong(self):
        self.score = max(0, self.score - 2)
        self._float("−2", C["accent"])
        self._update_score_display(wrong=True)
        self.after(400, self._next_card)

    def _check_win(self):
        if self.score >= 11:
            db  = self.master.db
            uid = self.master.user["id"]
            db.increment_total_answered(uid, self.questions)
            db.increment_total_correct(uid, self.score)
            db.increment_games_played(uid)
            db.set_last_play_time(uid)
            db.log_game(uid, "normal", self.score, self.questions)
            ctx = self._build_context()
            new_badges = self.master.achieve.check_all(uid, ctx)
            self.after(200, lambda: self.master.show_frame(
                VictoryScreen, score=self.score,
                questions=self.questions, new_badges=new_badges))


# ══════════════════════════════════════════════════════════════════════════════
#  ENDLESS MODE
# ══════════════════════════════════════════════════════════════════════════════

class EndlessModeScreen(BaseGameScreen):
    def __init__(self, master):
        super().__init__(master, "endless")

    def _on_wrong(self):
        self._end_run(cashed_out=False)

    def _cash_out(self):
        """Player voluntarily ends the run."""
        self._end_run(cashed_out=True)

    def _end_run(self, cashed_out=False):
        db   = self.master.db
        uid  = self.master.user["id"]
        prev = self.master.user["endless_highscore"]

        db.increment_total_answered(uid, self.questions)
        db.increment_total_correct(uid, self.score)
        db.increment_games_played(uid)
        db.set_last_play_time(uid)
        db.log_game(uid, "endless_cashout" if cashed_out else "endless",
                    self.score, self.questions)

        ctx = self._build_context()
        ctx["mode"] = "endless_cashout" if cashed_out else "endless"
        ctx["cashed_out"] = cashed_out
        new_badges = self.master.achieve.check_all(uid, ctx)

        new_hs = self.score > prev
        if new_hs:
            db.update_endless_highscore(uid, self.score)
            self.master.user["endless_highscore"] = self.score

        show_achievements(self.master, new_badges)
        self.after(120, lambda: self.master.show_frame(
            EndlessResultScreen, score=self.score,
            prev_hs=prev, new_hs=new_hs, cashed_out=cashed_out))


# ══════════════════════════════════════════════════════════════════════════════
#  SPEEDRUN MODE
# ══════════════════════════════════════════════════════════════════════════════

class SpeedrunMenuScreen(tk.Frame):
    """Choose a speedrun variant."""

    def __init__(self, master):
        super().__init__(master, bg=C["bg"])
        self._build()

    def _build(self):
        make_label(self, "⚡  Speedrun Mode",
                   font=FONT_TITLE, fg=C["orange"]).pack(pady=(40, 6))
        make_label(self, "Choose your challenge:",
                   font=FONT_MED, fg=C["muted"]).pack(pady=(0, 30))

        variants = [
            ("1️⃣  60 Seconds Chaos",
             "Answer as many as you can in 60 seconds",
             C["accent"], "60s"),
            ("2️⃣  Marathon  (10 minutes)",
             "Long haul — score as high as possible in 10 minutes",
             C["purple"], "10min"),
            ("3️⃣  Reflex Mode",
             "10 seconds per question — don't let the timer hit zero!",
             C["orange"], "reflex"),
        ]
        for title, desc, color, variant in variants:
            panel = tk.Frame(self, bg=C["panel"], padx=20, pady=14)
            panel.pack(fill="x", padx=120, pady=6)
            make_label(panel, title, font=FONT_LARGE,
                       fg=color, bg=C["panel"]).pack(anchor="w")
            make_label(panel, desc, font=FONT_SMALL,
                       fg=C["muted"], bg=C["panel"]).pack(anchor="w", pady=(2, 6))
            v = variant
            make_button(panel, "▶ Start", lambda v=v: self._start(v),
                        bg=color, pad=(20, 6)).pack(anchor="e")

        make_button(self, "← Back", self.master.show_menu,
                    bg=C["accent2"], pad=(20, 8)).pack(pady=20)

    def _start(self, variant):
        self.master.show_frame(SpeedrunScreen, variant=variant)


class SpeedrunScreen(tk.Frame):
    """
    Unified screen for all three speedrun variants.
    variant: "60s" | "10min" | "reflex"
    """

    VARIANT_CFG = {
        "60s":    {"label": "60 Second Chaos",  "total": 60,   "per_q": None},
        "10min":  {"label": "Marathon (10 min)", "total": 600,  "per_q": None},
        "reflex": {"label": "Reflex Mode",       "total": None, "per_q": 10},
    }

    def __init__(self, master, variant):
        super().__init__(master, bg=C["bg"])
        self.variant  = variant
        self.cfg      = self.VARIANT_CFG[variant]
        self.score    = 0
        self.questions= 0
        self._revealed= False
        self._running = True
        self._deck    = list(FLASHCARDS.keys())
        random.shuffle(self._deck)
        self._deck_idx= 0

        # Timer tracking
        if variant == "reflex":
            self._time_left = self.cfg["per_q"]
        else:
            self._time_left = self.cfg["total"]

        self._start_wall = time.time()
        self._build()
        self._next_card()
        self._tick()

    def _build(self):
        # Top bar
        top = tk.Frame(self, bg=C["bg"])
        top.pack(fill="x", padx=20, pady=10)

        make_button(top, "← Menu", self._abort,
                    bg=C["accent2"], font=FONT_SMALL, pad=(10, 5)).pack(side="left")
        make_label(top, f"⚡ {self.cfg['label']}",
                   font=FONT_LARGE, fg=C["orange"], bg=C["bg"]).pack(
                       side="left", padx=20)

        self._score_lbl = make_label(top, "Score: 0",
                                     font=FONT_LARGE, fg=C["yellow"], bg=C["bg"])
        self._score_lbl.pack(side="right")

        # Timer bar / display
        timer_frame = tk.Frame(self, bg=C["bg"])
        timer_frame.pack(fill="x", padx=20, pady=(0, 6))

        self._timer_lbl = tk.Label(timer_frame, text="60",
                                   font=("Segoe UI", 22, "bold"),
                                   fg=C["cyan"], bg=C["bg"])
        self._timer_lbl.pack(side="left")
        make_label(timer_frame, "  seconds remaining",
                   font=FONT_SMALL, fg=C["muted"], bg=C["bg"]).pack(side="left")

        # Timer canvas bar
        self._tb_canvas = tk.Canvas(self, height=14, bg=C["bg"],
                                    highlightthickness=0)
        self._tb_canvas.pack(fill="x", padx=20, pady=(0, 8))
        self._tb_canvas.bind("<Configure>",
                             lambda e: self._draw_timer_bar(self._time_left))

        # Card area
        self.canvas = tk.Canvas(self, bg=C["bg"], highlightthickness=0,
                                width=860, height=260)
        self.canvas.pack(pady=6)
        self.canvas.create_rectangle(10, 10, 850, 250,
                                     fill=C["card"], outline=C["accent2"], width=2)
        self._term_id = self.canvas.create_text(
            430, 90, text="", fill=C["white"],
            font=("Segoe UI", 32, "bold"), width=780)
        self._ans_id  = self.canvas.create_text(
            430, 185, text="", fill=C["cyan"],
            font=FONT_MED, width=780)

        # Buttons
        btn_row = tk.Frame(self, bg=C["bg"])
        btn_row.pack(pady=8)

        self._reveal_btn = make_button(
            btn_row, "👁  Reveal Answer", self._reveal,
            bg=C["accent2"], font=FONT_LARGE, pad=(30, 12))
        self._reveal_btn.pack(side="left", padx=10)

        self._correct_btn = make_button(
            btn_row, "✅ Correct  +1",
            lambda: self._answer(True),
            bg=C["green"], font=FONT_LARGE, pad=(20, 12))
        self._wrong_btn = make_button(
            btn_row, "❌ Wrong",
            lambda: self._answer(False),
            bg=C["accent"], font=FONT_LARGE, pad=(20, 12))
        self._correct_btn.pack_forget()
        self._wrong_btn.pack_forget()

        self._q_lbl = make_label(self, "Questions: 0",
                                 font=FONT_SMALL, fg=C["muted"])
        self._q_lbl.pack()

    # ── Timer drawing ─────────────────────────────────────────────────────────

    def _draw_timer_bar(self, time_left):
        c = self._tb_canvas
        W = c.winfo_width(); H = c.winfo_height()
        if W < 2: return
        c.delete("all")
        total = (self.cfg["per_q"] if self.variant == "reflex"
                 else self.cfg["total"])
        ratio = max(0.0, time_left / total)
        color = (C["accent"] if ratio < 0.25
                 else C["yellow"] if ratio < 0.5
                 else C["green"])
        fw = int(ratio * W)
        c.create_rectangle(0, 2, W, H-2, fill=C["card"], outline="")
        if fw > 0:
            c.create_rectangle(0, 2, fw, H-2, fill=color, outline="")

    def _tick(self):
        if not self._running: return
        self._time_left -= 1
        mins = int(self._time_left) // 60
        secs = int(self._time_left) % 60
        if self.variant == "reflex":
            lbl = f"{secs}"
        elif self.variant == "10min":
            lbl = f"{mins}:{secs:02d}"
        else:
            lbl = str(max(0, int(self._time_left)))

        self._timer_lbl.config(text=lbl)
        self._draw_timer_bar(self._time_left)

        # Flash red when < 10 seconds
        if self._time_left <= 10:
            clr = C["accent"] if int(self._time_left * 2) % 2 == 0 else C["yellow"]
            self._timer_lbl.config(fg=clr)
        else:
            self._timer_lbl.config(fg=C["cyan"])

        if self._time_left <= 0:
            self._end_game()
            return

        self.after(1000, self._tick)

    # ── Card logic ────────────────────────────────────────────────────────────

    def _next_card(self):
        self._revealed = False
        self._reveal_btn.pack(side="left", padx=10)
        self._correct_btn.pack_forget()
        self._wrong_btn.pack_forget()

        if self._deck_idx >= len(self._deck):
            random.shuffle(self._deck)
            self._deck_idx = 0

        term = self._deck[self._deck_idx]
        self._deck_idx += 1
        self._current_term = term
        self.canvas.itemconfig(self._term_id, text=term)
        self.canvas.itemconfig(self._ans_id, text="")

        # Reflex: reset per-question timer
        if self.variant == "reflex":
            self._time_left = self.cfg["per_q"]
            self._draw_timer_bar(self._time_left)

    def _reveal(self):
        if self._revealed: return
        self._revealed = True
        self.canvas.itemconfig(self._ans_id, text=FLASHCARDS[self._current_term])
        self._reveal_btn.pack_forget()
        self._correct_btn.pack(side="left", padx=10)
        self._wrong_btn.pack(side="left", padx=10)

    def _answer(self, correct):
        self.questions += 1
        self._q_lbl.config(text=f"Questions: {self.questions}")
        if correct:
            self.score += 1
            cx = (self.canvas.winfo_width() or 430) // 2
            FloatingText(self.canvas, cx, 130, "+1", C["green"],
                         font=("Segoe UI", 26, "bold"))
            self._score_lbl.config(text=f"Score: {self.score}")
        # Wrong answers don't penalise but waste time
        self._next_card()

    def _abort(self):
        self._running = False
        self.master.show_menu()

    def _end_game(self):
        if not self._running: return
        self._running = False
        db  = self.master.db
        uid = self.master.user["id"]
        db.increment_total_answered(uid, self.questions)
        db.increment_total_correct(uid, self.score)
        db.increment_games_played(uid)
        db.set_last_play_time(uid)
        db.update_speedrun_highscore(uid, self.score)
        db.log_game(uid, f"speedrun_{self.variant}", self.score, self.questions)

        ctx = {
            "mode": "speedrun",
            "speedrun_variant": self.variant,
            "score": self.score,
            "questions": self.questions,
            "time_elapsed": time.time() - self._start_wall,
        }
        new_badges = self.master.achieve.check_all(uid, ctx)
        show_achievements(self.master, new_badges)

        self.after(100, lambda: self.master.show_frame(
            SpeedrunResultScreen,
            variant=self.variant,
            score=self.score,
            questions=self.questions,
            new_badges=new_badges))


# ── Speedrun result ───────────────────────────────────────────────────────────

class SpeedrunResultScreen(tk.Frame):
    def __init__(self, master, variant, score, questions, new_badges):
        super().__init__(master, bg=C["bg"])
        self.variant = variant; self.score = score
        self.questions = questions; self.new_badges = new_badges
        self._build()

    def _build(self):
        variant_names = {"60s": "60 Seconds Chaos",
                         "10min": "Marathon",
                         "reflex": "Reflex Mode"}
        make_label(self, f"⚡  {variant_names[self.variant]} — Complete!",
                   font=FONT_TITLE, fg=C["orange"]).pack(pady=(50, 10))
        make_label(self, f"Score: {self.score}  |  Questions: {self.questions}",
                   font=FONT_LARGE, fg=C["cyan"]).pack(pady=8)

        if self.new_badges:
            make_label(self, "🏅 Achievements Unlocked!",
                       font=FONT_MED, fg=C["yellow"]).pack(pady=(10, 4))
            for b in self.new_badges:
                icon = next((d[2] for d in BADGE_DEFS if d[0] == b), "🏅")
                make_label(self, f"{icon}  {b}",
                           font=("Segoe UI", 14, "bold"),
                           fg=C["yellow"]).pack(pady=2)

        row = tk.Frame(self, bg=C["bg"])
        row.pack(pady=24)
        make_button(row, "▶ Play Again",
                    lambda: self.master.show_frame(SpeedrunScreen, variant=self.variant),
                    bg=C["orange"], pad=(20, 10)).pack(side="left", padx=10)
        make_button(row, "⚡ Other Modes",
                    self.master.show_speedrun_menu,
                    bg=C["purple"], pad=(20, 10)).pack(side="left", padx=10)
        make_button(row, "🏠 Main Menu",
                    self.master.show_menu,
                    bg=C["accent2"], pad=(20, 10)).pack(side="left", padx=10)


# ══════════════════════════════════════════════════════════════════════════════
#  VICTORY SCREEN  (Normal Mode)
# ══════════════════════════════════════════════════════════════════════════════

class VictoryScreen(tk.Frame):
    def __init__(self, master, score, questions, new_badges):
        super().__init__(master, bg=C["bg"])
        self.score = score; self.questions = questions
        self.new_badges = new_badges
        self._build()
        show_achievements(master, new_badges, delay=500)

    def _build(self):
        W, H = 960, 680
        self.canvas = tk.Canvas(self, width=W, height=H,
                                bg=C["bg"], highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self._confetti = ConfettiCanvas(self.canvas, W, H)

        self.canvas.create_text(480, 160, text="🎉  YOU WIN! 🎉",
                                fill=C["yellow"],
                                font=("Segoe UI", 44, "bold"))
        self.canvas.create_text(
            480, 230,
            text=f"Score: {self.score}  |  Questions: {self.questions}",
            fill=C["cyan"], font=FONT_LARGE)

        y = 290
        if self.new_badges:
            self.canvas.create_text(480, y, text="🏅 Badges Unlocked!",
                                    fill=C["green"], font=FONT_LARGE)
            y += 40
            for b in self.new_badges:
                icon = next((d[2] for d in BADGE_DEFS if d[0] == b), "🏅")
                self.canvas.create_text(
                    480, y, text=f"{icon}  {b}",
                    fill=C["yellow"], font=("Segoe UI", 18, "bold"))
                y += 36

        # Pulsing glow
        self._glow_r = 60; self._glow_dir = 1
        if self.new_badges:
            self._glow = self.canvas.create_oval(
                480-60, y-10, 480+60, y+50,
                outline=C["yellow"], width=3, fill="")
            self._pulse_glow(y)

        btn_frame = tk.Frame(self.canvas, bg=C["bg"])
        self.canvas.create_window(480, 590, window=btn_frame)
        make_button(btn_frame, "▶ Play Again",
                    self.master.show_normal_mode,
                    bg=C["green"], pad=(20, 10)).pack(side="left", padx=10)
        make_button(btn_frame, "🏠 Main Menu",
                    self.master.show_menu,
                    bg=C["accent2"], pad=(20, 10)).pack(side="left", padx=10)

    def _pulse_glow(self, cy):
        self._glow_r += self._glow_dir * 1.5
        if self._glow_r > 75 or self._glow_r < 50:
            self._glow_dir *= -1
        r = self._glow_r
        self.canvas.coords(self._glow, 480-r, cy-10, 480+r, cy+50)
        self.after(40, lambda: self._pulse_glow(cy))


# ══════════════════════════════════════════════════════════════════════════════
#  ENDLESS RESULT SCREEN
# ══════════════════════════════════════════════════════════════════════════════

class EndlessResultScreen(tk.Frame):
    def __init__(self, master, score, prev_hs, new_hs, cashed_out=False):
        super().__init__(master, bg=C["bg"])
        self.score = score; self.prev_hs = prev_hs
        self.new_hs = new_hs; self.cashed_out = cashed_out
        self._displayed = 0
        self._build()

    def _build(self):
        if self.new_hs:
            self._build_new_hs()
        else:
            self._build_normal()

    def _build_new_hs(self):
        W, H = 960, 680
        self.canvas = tk.Canvas(self, width=W, height=H,
                                bg=C["bg"], highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self._confetti = ConfettiCanvas(self.canvas, W, H)

        header = ("💾 CASHED OUT — NEW HIGH SCORE! 🔥"
                  if self.cashed_out else "🔥 NEW HIGH SCORE! 🔥")
        self.canvas.create_text(480, 175, text=header,
                                fill=C["yellow"],
                                font=("Segoe UI", 36, "bold"))
        self._hs_txt = self.canvas.create_text(
            480, 285, text="0",
            fill=C["cyan"], font=("Segoe UI", 72, "bold"))
        self._count_up()

        btn_frame = tk.Frame(self.canvas, bg=C["bg"])
        self.canvas.create_window(480, 430, window=btn_frame)
        make_button(btn_frame, "▶ Play Again",
                    self.master.show_endless_mode,
                    bg=C["purple"], pad=(20, 10)).pack(side="left", padx=10)
        make_button(btn_frame, "🏠 Menu",
                    self.master.show_menu,
                    bg=C["accent2"], pad=(20, 10)).pack(side="left", padx=10)

    def _count_up(self):
        if self._displayed < self.score:
            step = max(1, (self.score - self._displayed) // 8)
            self._displayed = min(self._displayed + step, self.score)
            self.canvas.itemconfig(self._hs_txt, text=str(self._displayed))
            self.after(40, self._count_up)

    def _build_normal(self):
        header = ("💾 Cashed Out!" if self.cashed_out else "Game Over")
        make_label(self, header,
                   font=("Segoe UI", 36, "bold"),
                   fg=C["green"] if self.cashed_out else C["accent"]
                   ).pack(pady=(80, 10))
        make_label(self, f"Your score: {self.score}",
                   font=FONT_LARGE, fg=C["text"]).pack(pady=6)
        make_label(self, f"High Score: {self.prev_hs}",
                   font=FONT_MED, fg=C["muted"]).pack(pady=6)

        row = tk.Frame(self, bg=C["bg"])
        row.pack(pady=30)
        make_button(row, "▶ Play Again",
                    self.master.show_endless_mode,
                    bg=C["purple"], pad=(20, 10)).pack(side="left", padx=10)
        make_button(row, "🏠 Menu",
                    self.master.show_menu,
                    bg=C["accent2"], pad=(20, 10)).pack(side="left", padx=10)


# ══════════════════════════════════════════════════════════════════════════════
#  REWARDS / ACHIEVEMENTS SCREEN
# ══════════════════════════════════════════════════════════════════════════════

class RewardsScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=C["bg"])
        self._build()

    def _build(self):
        make_label(self, "🏅  Badges & Rewards",
                   font=FONT_TITLE, fg=C["yellow"]).pack(pady=(20, 6))

        db     = self.master.db
        uid    = self.master.user["id"]
        earned = db.get_user_badge_names(uid)
        all_b  = db.get_all_badges()

        # Scrollable area via Canvas
        outer = tk.Frame(self, bg=C["bg"])
        outer.pack(fill="both", expand=True, padx=40)

        scv = tk.Canvas(outer, bg=C["bg"], highlightthickness=0)
        scv.pack(side="left", fill="both", expand=True)
        sb  = tk.Scrollbar(outer, orient="vertical", command=scv.yview)
        sb.pack(side="right", fill="y")
        scv.configure(yscrollcommand=sb.set)

        inner = tk.Frame(scv, bg=C["bg"])
        scv_win = scv.create_window(0, 0, anchor="nw", window=inner)

        def _resize(e):
            scv.itemconfig(scv_win, width=e.width)
        scv.bind("<Configure>", _resize)
        inner.bind("<Configure>",
                   lambda e: scv.configure(scrollregion=scv.bbox("all")))
        scv.bind_all("<MouseWheel>",
                     lambda e: scv.yview_scroll(-1*(e.delta//120), "units"))

        for row_data in all_b:
            name, desc, icon = (row_data["badge_name"],
                                row_data["description"],
                                row_data["icon"])
            deps_str = row_data["depends_on"] if row_data["depends_on"] else ""
            deps     = [d for d in deps_str.split(",") if d]
            locked_by_dep = any(d not in earned for d in deps)
            unlocked = name in earned

            if locked_by_dep:
                row_bg  = C["bg"]
                txt_col = C["muted"]
                display_icon = "🔒"
            elif unlocked:
                row_bg  = C["card"]
                txt_col = C["text"]
                display_icon = icon
            else:
                row_bg  = C["panel"]
                txt_col = C["muted"]
                display_icon = "🔒"

            row = tk.Frame(inner, bg=row_bg, pady=10, padx=18)
            row.pack(fill="x", pady=3)

            tk.Label(row, text=display_icon,
                     font=("Segoe UI", 24), bg=row_bg,
                     fg=C["yellow"] if unlocked else C["muted"]
                     ).pack(side="left", padx=(0, 12))

            info = tk.Frame(row, bg=row_bg)
            info.pack(side="left")
            tk.Label(info, text=name,
                     font=("Segoe UI", 13, "bold"),
                     bg=row_bg, fg=txt_col).pack(anchor="w")
            tk.Label(info, text=desc,
                     font=FONT_SMALL, bg=row_bg,
                     fg=C["muted"]).pack(anchor="w")
            if locked_by_dep:
                tk.Label(info,
                         text=f"  Requires: {', '.join(deps)}",
                         font=("Segoe UI", 9, "italic"),
                         bg=row_bg, fg=C["muted"]).pack(anchor="w")

            status_text = ("✓ Unlocked" if unlocked
                           else "🔒 Locked (missing prereq)" if locked_by_dep
                           else "Locked")
            tk.Label(row, text=status_text,
                     font=("Segoe UI", 11, "bold"),
                     bg=row_bg,
                     fg=C["green"] if unlocked else C["muted"]
                     ).pack(side="right")

        make_button(self, "← Back", self.master.show_menu,
                    bg=C["accent2"], pad=(20, 8)).pack(pady=12)


# ══════════════════════════════════════════════════════════════════════════════
#  LEADERBOARD SCREEN
# ══════════════════════════════════════════════════════════════════════════════

class LeaderboardScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=C["bg"])
        self._build()

    def _build(self):
        make_label(self, "📊  Leaderboard",
                   font=FONT_TITLE, fg=C["cyan"]).pack(pady=(30, 20))

        rows    = self.master.db.get_leaderboard()
        frame   = tk.Frame(self, bg=C["bg"])
        frame.pack(fill="both", expand=True, padx=40)

        headers = ["Rank", "Username", "Endless HS", "Speedrun HS",
                   "Total Q's", "Badges"]
        widths  = [6, 18, 12, 12, 10, 8]

        hrow = tk.Frame(frame, bg=C["accent2"])
        hrow.pack(fill="x")
        for h, w in zip(headers, widths):
            tk.Label(hrow, text=h, width=w,
                     font=("Segoe UI", 12, "bold"),
                     bg=C["accent2"], fg=C["white"], pady=8
                     ).pack(side="left")

        for i, row in enumerate(rows, 1):
            medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(i, f"#{i}")
            bg_c  = C["card"] if i % 2 == 0 else C["panel"]
            fg_c  = C["yellow"] if i <= 3 else C["text"]
            drow  = tk.Frame(frame, bg=bg_c)
            drow.pack(fill="x")
            vals = [medal,
                    row["username"],
                    row["endless_highscore"],
                    row["speedrun_highscore"],
                    row["total_answered"],
                    row["badge_count"]]
            for val, w in zip(vals, widths):
                tk.Label(drow, text=str(val), width=w,
                         font=FONT_SMALL, bg=bg_c, fg=fg_c,
                         pady=8).pack(side="left")

        make_button(self, "← Back", self.master.show_menu,
                    bg=C["accent2"], pad=(20, 8)).pack(pady=20)


# ══════════════════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    app = FlashcardApp()
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()
