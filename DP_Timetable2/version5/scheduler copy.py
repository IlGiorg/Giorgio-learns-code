#!/usr/bin/env python3
"""
DP Subject Scheduler – FIXED VERSION
Accurate conflict detection + success rate
"""

from collections import defaultdict, Counter
from itertools import combinations

# =========================
# SUBJECT DEFINITIONS
# =========================

SCIENCES = {
    'Computer Science',
    'Physics',
    'Biology',
    'Chemistry',
    'Environmental Sciences Studies (ESS)'
}

HUMANITIES = {
    'Business',
    'Economics',
    'Geography',
    'History',
    'Politics',
    'Global Politics',
    'GeoPolitics'
}

ARTS = {
    'Visual Arts'
}

LANGUAGES = {
    'Spanish',
    'French'
}

ONLINE = {
    'Psychology (Timetabled Online)'
}

# =========================
# PARSING
# =========================

def parse_student_choices(raw):
    parts = [p.strip() for p in raw.split(';') if p.strip()]
    if len(parts) % 3 != 0:
        raise ValueError("Student choices are not divisible by 3")

    return [tuple(parts[i:i+3]) for i in range(0, len(parts), 3)]

# =========================
# VALIDATION
# =========================

def get_category(subject):
    if subject in SCIENCES:
        return 'Science'
    if subject in HUMANITIES:
        return 'Humanity'
    if subject in ARTS:
        return 'Arts'
    if subject in LANGUAGES:
        return 'Language'
    if subject in ONLINE:
        return 'Online'
    return 'Unknown'

def validate_student(subjects):
    sci = sum(get_category(s) == 'Science' for s in subjects)
    hum = sum(get_category(s) == 'Humanity' for s in subjects)
    flex = sum(get_category(s) in ('Arts', 'Language') for s in subjects)
    hum += flex

    valid = (sci == 2 and hum == 1) or (sci == 1 and hum == 2)
    return valid

# =========================
# CONFLICT DETECTION
# =========================

def count_conflicts(slots, students):
    conflicts = []
    for i, student in enumerate(students):
        used = []
        for subj in student:
            for s_idx, slot in enumerate(slots):
                if subj in slot:
                    used.append(s_idx)
                    break
        if len(used) != len(set(used)):
            conflicts.append((i, student, [u+1 for u in used]))

    return len(conflicts), conflicts

# =========================
# ASSIGNMENT
# =========================

def greedy_assignment(students, manual_overrides):
    subject_counts = Counter(s for stu in students for s in stu)

    co = defaultdict(int)
    for stu in students:
        for a, b in combinations(stu, 2):
            co[tuple(sorted((a, b)))] += 1

    slots = [set(), set(), set()]
    locked = {}

    # Apply manual overrides (LOCKED)
    for slot_idx, subjects in manual_overrides.items():
        for s in subjects:
            if s in subject_counts:
                slots[slot_idx].add(s)
                locked[s] = slot_idx

    # Remaining subjects
    remaining = [s for s in subject_counts if s not in locked]

    remaining.sort(key=lambda s: -subject_counts[s])

    for subject in remaining:
        best = min(
            range(3),
            key=lambda i: sum(
                co.get(tuple(sorted((subject, other))), 0)
                for other in slots[i]
            )
        )
        slots[best].add(subject)

    return slots, subject_counts

# =========================
# HTML OUTPUT
# =========================

def generate_html(slots, students, counts, conflicts, conflict_students):
    total = len(students)
    success = total - conflicts
    rate = success / total * 100 if total else 0

    def slot_block(i, slot):
        rows = ""
        for s in sorted(slot):
            rows += f"<li>{s} <b>({counts[s]})</b></li>"
        return f"""
        <div class="slot">
            <h3>SLOT {i+1}</h3>
            <ul>{rows}</ul>
        </div>
        """

    conflict_rows = ""
    for i, subs, used in conflict_students:
        conflict_rows += f"<li>Student {i+1}: {', '.join(subs)} → slots {used}</li>"

    return f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>DP Scheduler</title>
<style>
body {{ font-family: Arial; background:#f5f7fa; padding:20px; }}
.slot {{ background:white; padding:15px; border-radius:10px; margin:10px; }}
.stats {{ display:flex; gap:20px; }}
.card {{ background:white; padding:15px; border-radius:10px; }}
</style>
</head>
<body>

<h1>📚 DP Subject Scheduler</h1>

<div class="stats">
<div class="card"><h2>{success}</h2>Satisfied</div>
<div class="card"><h2>{conflicts}</h2>Conflicts</div>
<div class="card"><h2>{rate:.1f}%</h2>Success</div>
</div>

<h2>Schedule</h2>
{''.join(slot_block(i, s) for i, s in enumerate(slots))}

<h2>Conflicts</h2>
<ul>{conflict_rows}</ul>

</body>
</html>
"""

# =========================
# YOUR BRACKETS (FIXED)
# =========================

MANUAL_OVERRIDES = {
    0: ['Business', 'Economics', 'Geography', 'History', 'Politics', 'GeoPolitics'],
    1: ['Biology', 'Chemistry', 'Physics', 'Environmental Sciences Studies (ESS)'],
    2: ['Computer Science', 'Visual Arts', 'Spanish', 'French']
}

# =========================
# DATA
# =========================

raw_data = """Computer Science;Physics;Business;Computer Science;Spanish;Business;Biology;Computer Science;Business;Computer Science;Environmental Sciences Studies (ESS);Business;Computer Science;Biology;Business;Visual Arts;Biology;History;Business;Chemistry;Physics;Business;Biology;Politics;French;Physics;Computer Science;Business;Biology;Chemistry;Spanish;Biology;GeoPolitics;Psychology (Timetabled Online);Biology;Psychology (Timetabled Online);Politics;Chemistry;Computer Science;History;Biology;Psychology (Timetabled Online);Visual Arts;Biology;History;GeoPolitics;Biology;French;Business;Biology;Chemistry;Spanish;Physics;Computer Science;Business"""

# =========================
# RUN
# =========================

students = parse_student_choices(raw_data)
slots, counts = greedy_assignment(students, MANUAL_OVERRIDES)
conflict_count, conflict_students = count_conflicts(slots, students)

html = generate_html(slots, students, counts, conflict_count, conflict_students)

with open("dp_schedule_results.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ DONE")
print(f"Students: {len(students)}")
print(f"Conflicts: {conflict_count}")
print(f"Success rate: {(len(students)-conflict_count)/len(students)*100:.1f}%")
