#!/usr/bin/env python3
"""
DP Subject Scheduler - Optimization of brackets to minimize conflicts
"""

from collections import defaultdict, Counter
from itertools import combinations
import random
import json

# Subject categories
SCIENCES = {'Computer Science', 'Physics', 'Biology', 'Chemistry', 'Environmental Sciences Studies (ESS)'}
HUMANITIES = {'Economics', 'Business', 'Global Politics', 'History', 'Geography', 'Politics', 'GeoPolitics'}
ARTS = {'Arts', 'Music', 'Visual Arts'}
LANGUAGES = {'Spanish', 'French'}
ONLINE = {'Psychology (Timetabled Online)'}

def parse_student_choices(raw_data):
    choices = raw_data.split(';')
    students = []
    current = []

    for choice in choices:
        choice = choice.strip()
        if not choice:
            continue

        current.append(choice)
        if len(current) == 3:
            students.append(tuple(current))
            current = []

    return students

def get_category(subject):
    if subject in SCIENCES:
        return 'Science'
    elif subject in HUMANITIES:
        return 'Humanity'
    elif subject in ARTS:
        return 'Arts'
    elif subject in LANGUAGES:
        return 'Language'
    elif subject in ONLINE:
        return 'Online'
    return 'Unknown'

def validate_student(subjects):
    science_count = sum(1 for s in subjects if get_category(s) == 'Science')
    humanity_count = sum(1 for s in subjects if get_category(s) == 'Humanity')
    flexible = sum(1 for s in subjects if get_category(s) in ['Language', 'Arts'])
    humanity_count += flexible

    valid = (science_count == 2 and humanity_count == 1) or \
            (science_count == 1 and humanity_count == 2)

    return valid, science_count, humanity_count

def count_conflicts(assignment, students):
    conflicts = 0
    conflict_students = []

    for idx, student in enumerate(students):
        slots_used = []
        for subject in student:
            for slot_idx, slot in enumerate(assignment):
                if subject in slot:
                    slots_used.append(slot_idx)
                    break

        if len(slots_used) != len(set(slots_used)):
            conflicts += 1
            conflict_students.append((idx, student, slots_used))

    return conflicts, conflict_students

def greedy_assignment(students, manual_overrides=None):
    subject_counts = Counter()
    for student in students:
        for subject in student:
            subject_counts[subject] += 1

    cooccurrence = defaultdict(int)
    for student in students:
        for s1, s2 in combinations(student, 2):
            cooccurrence[tuple(sorted([s1, s2]))] += 1

    slots = [set(), set(), set()]
    assigned = {}

    if manual_overrides:
        print("\n🔧 Applying manual overrides...")
        for slot_idx, subjects in manual_overrides.items():
            for subject in subjects:
                if subject in subject_counts:
                    slots[slot_idx].add(subject)
                    assigned[subject] = slot_idx
                    print(f"   ✓ {subject} → SLOT {slot_idx + 1}")
                else:
                    print(f"   ⚠️  '{subject}' not found in data")

    remaining = [(s, c) for s, c in subject_counts.items() if s not in assigned]
    remaining.sort(key=lambda x: -x[1])

    for subject, _ in remaining:
        best_slot = min(
            range(3),
            key=lambda s: sum(
                cooccurrence.get(tuple(sorted([subject, e])), 0)
                for e in slots[s]
            )
        )
        slots[best_slot].add(subject)

    return slots

# =========================
# MANUAL OVERRIDES (YOUR BRACKETS)
# =========================

MANUAL_OVERRIDES = {
    0: [  # SLOT 1 – Humanities
        'Business',
        'Economics',
        'Geography',
        'GeoPolitics',
        'History',
        'Politics'
    ],
    1: [  # SLOT 2 – Sciences
        'Biology',
        'Chemistry',
        'Environmental Sciences Studies (ESS)',
        'Physics'
    ],
    2: [  # SLOT 3 – Mixed
        'Computer Science',
        'Visual Arts',
        'Spanish',
        'French'
    ]
}

# =========================

raw_data = """Computer Science;Physics;Business;Computer Science;Spanish;Business;Biology;Computer Science;Business;Computer Science;Environmental Sciences Studies (ESS);Business;Computer Science;Biology;Business;Visual Arts;Biology;History;Business;Chemistry;Physics;Business;Biology;Politics;French;Physics;Computer Science;Business;Biology;Chemistry;Spanish;Biology;GeoPolitics;Psychology (Timetabled Online);Biology;Psychology (Timetabled Online);Politics;Chemistry;Computer Science;History;Biology;Psychology (Timetabled Online);Visual Arts;Biology;History;GeoPolitics;Biology;French;Business;Biology;Chemistry;Spanish;Physics;Computer Science;Business"""

print("🔍 Parsing student choices...")
students = parse_student_choices(raw_data)
print(f"📊 Found {len(students)} students")

invalid = []
for i, s in enumerate(students):
    v, sci, hum = validate_student(s)
    if not v:
        invalid.append((i, s, sci, hum))

if invalid:
    print(f"\n⚠️ {len(invalid)} invalid combinations")

subject_counts = Counter()
for s in students:
    for sub in s:
        subject_counts[sub] += 1

print("\n🎯 Running optimization...")
assignment = greedy_assignment(students, MANUAL_OVERRIDES)
conflicts, conflict_students = count_conflicts(assignment, students)

print("\n" + "="*60)
for i, slot in enumerate(assignment, 1):
    print(f"\n📚 SLOT {i}")
    for s in sorted(slot):
        print(f"   • {s} ({subject_counts[s]})")

print("\n" + "-"*60)
print(f"✅ Satisfied students: {len(students)-conflicts}/{len(students)}")
print(f"❌ Conflicts: {conflicts}")
print(f"📊 Success rate: {(len(students)-conflicts)/len(students)*100:.1f}%")

if conflict_students:
    print("\n⚠️ Students with conflicts:")
    for i, subs, slots in conflict_students:
        print(f"   Student {i+1}: {subs} → slots {slots}")
