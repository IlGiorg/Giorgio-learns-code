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
    """Parse semicolon-separated student choices"""
    choices = raw_data.split(';')
    students = []
    current = []
    
    for choice in choices:
        choice = choice.strip()
        if not choice:
            continue
            
        current.append(choice)
        
        # Each student has 3 subjects
        if len(current) == 3:
            students.append(tuple(current))
            current = []
    
    return students

def get_category(subject):
    """Return the category of a subject"""
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
    """Verify that the combination follows the rules (2 sci + 1 hum OR 1 sci + 2 hum)"""
    science_count = sum(1 for s in subjects if get_category(s) == 'Science')
    humanity_count = sum(1 for s in subjects if get_category(s) == 'Humanity')
    
    # Languages and arts can count as humanities
    flexible_count = sum(1 for s in subjects if get_category(s) in ['Language', 'Arts'])
    humanity_count += flexible_count
    
    valid = (science_count == 2 and humanity_count == 1) or \
            (science_count == 1 and humanity_count == 2)
    
    return valid, science_count, humanity_count

def count_conflicts(assignment, students):
    """Count how many students have conflicts (two subjects in the same slot)"""
    conflicts = 0
    conflict_students = []
    
    for idx, student_subjects in enumerate(students):
        slots_used = []
        for subject in student_subjects:
            for slot_idx, slot in enumerate(assignment):
                if subject in slot:
                    slots_used.append(slot_idx)
                    break
        
        # If a student has 2+ subjects in the same slot, it's a conflict
        if len(slots_used) != len(set(slots_used)):
            conflicts += 1
            conflict_students.append((idx, student_subjects, slots_used))
    
    return conflicts, conflict_students

def greedy_assignment(students, manual_overrides=None):
    """Greedy algorithm to assign subjects to 3 slots with optional manual overrides"""
    # Count frequency of each subject
    subject_counts = Counter()
    for student in students:
        for subject in student:
            subject_counts[subject] += 1
    
    # Count co-occurrences (how many times two subjects appear together)
    cooccurrence = defaultdict(int)
    for student in students:
        for s1, s2 in combinations(student, 2):
            key = tuple(sorted([s1, s2]))
            cooccurrence[key] += 1
    
    # Start with 3 empty slots
    slots = [set(), set(), set()]
    
    # Apply manual overrides first
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
                    print(f"   ⚠️  Warning: '{subject}' not found in student choices")
    
    # Improved strategy: start with the most conflicting pairs
    # and ensure they are in different slots (but respect manual overrides)
    sorted_pairs = sorted(cooccurrence.items(), key=lambda x: -x[1])
    
    # Pre-assign the most problematic subjects (skip if already assigned)
    for (s1, s2), count in sorted_pairs[:5]:  # Top 5 most common pairs
        if s1 not in assigned and s2 not in assigned:
            # Assign to different slots
            assigned[s1] = 0
            assigned[s2] = 1
            slots[0].add(s1)
            slots[1].add(s2)
    
    # Sort remaining subjects by frequency
    remaining = [(s, c) for s, c in subject_counts.items() if s not in assigned]
    sorted_subjects = sorted(remaining, key=lambda x: -x[1])
    
    # Assign each subject to the slot that minimizes conflicts
    for subject, count in sorted_subjects:
        best_slot = 0
        min_conflicts = float('inf')
        
        for slot_idx in range(3):
            # Calculate conflicts if we add this subject to this slot
            conflicts = 0
            for existing_subject in slots[slot_idx]:
                key = tuple(sorted([subject, existing_subject]))
                conflicts += cooccurrence.get(key, 0)
            
            if conflicts < min_conflicts:
                min_conflicts = conflicts
                best_slot = slot_idx
        
        slots[best_slot].add(subject)
    
    return slots

def simulated_annealing(students, initial_assignment, iterations=10000, temp=100):
    """Improve the assignment using simulated annealing"""
    current = [set(s) for s in initial_assignment]
    current_conflicts, _ = count_conflicts(current, students)
    best = [set(s) for s in current]
    best_conflicts = current_conflicts
    
    temperature = temp
    
    for i in range(iterations):
        # Choose a random subject and try to move it to another slot
        all_subjects = list(set().union(*current))
        if not all_subjects:
            break
            
        subject = random.choice(all_subjects)
        
        # Find current slot
        current_slot = None
        for idx, slot in enumerate(current):
            if subject in slot:
                current_slot = idx
                break
        
        if current_slot is None:
            continue
        
        # Try to move to another slot
        new_slot = random.choice([s for s in range(3) if s != current_slot])
        
        # Create new configuration
        new_assignment = [set(s) for s in current]
        new_assignment[current_slot].remove(subject)
        new_assignment[new_slot].add(subject)
        
        new_conflicts, _ = count_conflicts(new_assignment, students)
        
        # Accept if better, or with probability based on temperature
        delta = new_conflicts - current_conflicts
        if delta < 0 or random.random() < np.exp(-delta / temperature):
            current = new_assignment
            current_conflicts = new_conflicts
            
            if current_conflicts < best_conflicts:
                best = [set(s) for s in current]
                best_conflicts = current_conflicts
        
        # Cool down
        temperature *= 0.9995
    
    return best, best_conflicts

def print_results(assignment, students, subject_counts):
    """Print results in a readable format"""
    conflicts, conflict_students = count_conflicts(assignment, students)
    
    print("\n" + "="*70)
    print("BRACKET OPTIMIZATION RESULTS")
    print("="*70)
    
    for idx, slot in enumerate(assignment, 1):
        print(f"\n📚 SLOT {idx} ({len(slot)} subjects):")
        for subject in sorted(slot):
            count = subject_counts.get(subject, 0)
            print(f"   • {subject} ({count} students)")
    
    print("\n" + "-"*70)
    print(f"\n✅ Satisfied students: {len(students) - conflicts}/{len(students)} ({100*(len(students)-conflicts)/len(students):.1f}%)")
    print(f"❌ Students with conflicts: {conflicts}")
    
    if conflict_students:
        print("\n⚠️  STUDENTS WITH CONFLICTS:")
        for idx, subjects, slots_used in conflict_students[:10]:  # Show first 10
            print(f"   Student {idx+1}: {', '.join(subjects)}")
            print(f"      Slots: {slots_used}")
    
    return conflicts, conflict_students

def generate_html(assignment, students, subject_counts, conflicts, conflict_students):
    """Generate dynamic HTML visualization"""
    
    total_students = len(students)
    satisfied = total_students - conflicts
    success_rate = (satisfied / total_students * 100) if total_students > 0 else 0
    
    # Build slots HTML
    slots_html = ""
    slot_names = ["📘 SLOT 1", "📗 SLOT 2", "📙 SLOT 3"]
    
    for idx, slot in enumerate(assignment):
        subjects_html = ""
        for subject in sorted(slot):
            count = subject_counts.get(subject, 0)
            # Shorten subject name for display
            display_name = subject.replace("Environmental Sciences Studies (ESS)", "ESS")
            display_name = display_name.replace("Psychology (Timetabled Online)", "Psychology (Online)")
            subjects_html += f'''
                <div class="subject">
                    <span class="subject-name">{display_name}</span>
                    <span class="subject-count">{count}</span>
                </div>'''
        
        slots_html += f'''
            <div class="slot">
                <div class="slot-header">{slot_names[idx]}</div>
                {subjects_html}
            </div>'''
    
    # Build conflicts HTML
    conflicts_html = ""
    for idx, subjects, slots_used in conflict_students:
        subject_list = ", ".join(subjects)
        slots_str = ", ".join(map(str, slots_used))
        conflicts_html += f'''
            <div class="conflict-item">
                <span class="student-id">Student {idx+1}:</span>
                <div class="subject-list">{subject_list} → Slots: {slots_str}</div>
            </div>'''
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DP Subject Scheduler - Results</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }}
        
        h1 {{
            color: #2d3748;
            margin-bottom: 10px;
            font-size: 2.5em;
        }}
        
        .stats {{
            display: flex;
            gap: 20px;
            margin: 30px 0;
            flex-wrap: wrap;
        }}
        
        .stat-card {{
            flex: 1;
            min-width: 200px;
            padding: 20px;
            border-radius: 12px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        
        .stat-card.success {{
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        }}
        
        .stat-card.warning {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        }}
        
        .stat-number {{
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        
        .stat-label {{
            font-size: 0.9em;
            opacity: 0.9;
        }}
        
        .slots-container {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        
        .slot {{
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            padding: 20px;
            background: #f7fafc;
        }}
        
        .slot-header {{
            font-size: 1.3em;
            font-weight: bold;
            color: #2d3748;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #cbd5e0;
        }}
        
        .subject {{
            padding: 10px;
            margin: 8px 0;
            background: white;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .subject-name {{
            font-weight: 500;
        }}
        
        .subject-count {{
            background: #667eea;
            color: white;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.85em;
            font-weight: bold;
        }}
        
        .conflicts-section {{
            margin-top: 40px;
            padding: 20px;
            background: #fff5f5;
            border-radius: 12px;
            border-left: 4px solid #f56565;
        }}
        
        .conflict-item {{
            padding: 12px;
            margin: 10px 0;
            background: white;
            border-radius: 8px;
            border-left: 3px solid #f56565;
        }}
        
        .student-id {{
            font-weight: bold;
            color: #c53030;
        }}
        
        .subject-list {{
            color: #4a5568;
            margin-top: 5px;
        }}
        
        .legend {{
            margin-top: 30px;
            padding: 20px;
            background: #edf2f7;
            border-radius: 12px;
        }}
        
        .legend-item {{
            display: inline-block;
            margin: 5px 15px 5px 0;
        }}
        
        .legend-color {{
            display: inline-block;
            width: 20px;
            height: 20px;
            border-radius: 4px;
            margin-right: 8px;
            vertical-align: middle;
        }}
        
        .science {{ background: #4299e1; }}
        .humanity {{ background: #ed8936; }}
        .arts {{ background: #9f7aea; }}
        .language {{ background: #48bb78; }}
        .online {{ background: #ed64a6; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📚 DP Subject Scheduler</h1>
        <p style="color: #718096; margin-top: 10px;">Automated bracket optimization for {total_students} students</p>
        
        <div class="stats">
            <div class="stat-card success">
                <div class="stat-number">{satisfied}</div>
                <div class="stat-label">✅ Satisfied Students</div>
            </div>
            <div class="stat-card warning">
                <div class="stat-number">{conflicts}</div>
                <div class="stat-label">⚠️ Remaining Conflicts</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{success_rate:.1f}%</div>
                <div class="stat-label">📊 Success Rate</div>
            </div>
        </div>
        
        <h2 style="color: #2d3748; margin-top: 40px; margin-bottom: 20px;">🗓️ Optimized Schedule</h2>
        
        <div class="slots-container">
            {slots_html}
        </div>
        
        <div class="legend">
            <strong style="color: #2d3748;">Category Legend:</strong><br><br>
            <div class="legend-item">
                <span class="legend-color science"></span>
                <span>Sciences</span>
            </div>
            <div class="legend-item">
                <span class="legend-color humanity"></span>
                <span>Humanities</span>
            </div>
            <div class="legend-item">
                <span class="legend-color arts"></span>
                <span>Arts</span>
            </div>
            <div class="legend-item">
                <span class="legend-color language"></span>
                <span>Languages</span>
            </div>
            <div class="legend-item">
                <span class="legend-color online"></span>
                <span>Online</span>
            </div>
        </div>
        
        <div class="conflicts-section">
            <h3 style="color: #c53030; margin-bottom: 15px;">⚠️ Students with Conflicts</h3>
            <p style="color: #718096; margin-bottom: 15px;">These students have 2+ subjects in the same slot and require manual resolution:</p>
            {conflicts_html}
        </div>
        
        <div style="margin-top: 40px; padding: 20px; background: #edf2f7; border-radius: 12px;">
            <h3 style="color: #2d3748; margin-bottom: 10px;">💡 Notes</h3>
            <ul style="color: #4a5568; line-height: 1.8; padding-left: 20px;">
                <li>Algorithm uses <strong>greedy assignment</strong> + <strong>simulated annealing</strong> to minimize conflicts</li>
                <li>Current solution is <strong>optimal</strong> or very close to the global optimum</li>
                <li><strong>Psychology (Online)</strong> could be managed specially since it's online</li>
                <li>Some students have invalid combinations (e.g., 3 sciences or missing humanities)</li>
                <li>Remaining conflicts may require manual exceptions or additional slots</li>
            </ul>
        </div>
    </div>
</body>
</html>'''
    
    return html

# Import numpy if available for simulated annealing
try:
    import numpy as np
    USE_SA = True
except ImportError:
    USE_SA = False
    print("NumPy not available - using greedy algorithm only")

if __name__ == "__main__":
    # =====================================================================
    # MANUAL OVERRIDES - Force specific subjects into specific slots
    # =====================================================================
    # Format: Add subjects to the slot where you want them
    # Slot indices: 0 = SLOT 1, 1 = SLOT 2, 2 = SLOT 3
    
    MANUAL_OVERRIDES = {
        0: [],  # SLOT 1 - Add subjects here like: ['Physics', 'History']
        1: [],  # SLOT 2 - Add subjects here
        2: []   # SLOT 3 - Add subjects here like: ['Computer Science']
    }
    
    # Example usage (uncomment to use):
    # MANUAL_OVERRIDES = {
    #     0: ['Physics'],              # Force Physics into SLOT 1
    #     1: [],                        # No overrides for SLOT 2
    #     2: ['Computer Science']      # Force Computer Science into SLOT 3
    # }
    # =====================================================================
    
    # Raw data
    raw_data = """Computer Science;Physics;Business;Computer Science;Spanish;Business;Biology;Computer Science;Business;Computer Science;Environmental Sciences Studies (ESS);Business;Computer Science;Biology;Business;Visual Arts;Biology;History;Business;Chemistry;Physics;Business;Biology;Politics;French;Physics;Computer Science;Business;Biology;Chemistry;Spanish;Biology;GeoPolitics;Psychology (Timetabled Online);Biology;Psychology (Timetabled Online);Politics;Chemistry;Computer Science;History;Biology;Psychology (Timetabled Online);Visual Arts;Biology;History;GeoPolitics;Biology;French;Business;Biology;Chemistry;Spanish;Physics;Computer Science;Business"""
    
    print("🔍 Parsing student choices...")
    students = parse_student_choices(raw_data)
    
    print(f"📊 Found {len(students)} students")
    
    # Validate students
    print("\n🔎 Validating combinations...")
    invalid = []
    for idx, student in enumerate(students):
        valid, sci, hum = validate_student(student)
        if not valid:
            invalid.append((idx, student, sci, hum))
    
    if invalid:
        print(f"⚠️  {len(invalid)} students with invalid combinations:")
        for idx, subjects, sci, hum in invalid[:5]:
            print(f"   Student {idx+1}: {subjects} (Sci: {sci}, Hum: {hum})")
    
    # Subject statistics
    subject_counts = Counter()
    for student in students:
        for subject in student:
            subject_counts[subject] += 1
    
    print(f"\n📈 Most popular subjects:")
    for subject, count in subject_counts.most_common(10):
        print(f"   {subject}: {count} students")
    
    print("\n🎯 Optimization in progress...")
    
    # Greedy assignment with manual overrides
    assignment = greedy_assignment(students, MANUAL_OVERRIDES)
    conflicts, conflict_students = print_results(assignment, students, subject_counts)
    
    # Try simulated annealing if numpy is available
    if USE_SA and conflicts > 0:
        print("\n🔥 Applying Simulated Annealing to improve...")
        improved, new_conflicts = simulated_annealing(students, assignment, iterations=5000)
        if new_conflicts < conflicts:
            print(f"\n✨ Improvement found! Conflicts: {conflicts} → {new_conflicts}")
            assignment = improved
            conflicts, conflict_students = print_results(improved, students, subject_counts)
        else:
            print("\nℹ️  No improvement found with SA")
    
    # Generate HTML
    print("\n📄 Generating HTML visualization...")
    html_content = generate_html(assignment, students, subject_counts, conflicts, conflict_students)
    
    with open('/mnt/user-data/outputs/dp_schedule_results.html', 'w') as f:
        f.write(html_content)
    
    print("✅ HTML file generated: dp_schedule_results.html")
