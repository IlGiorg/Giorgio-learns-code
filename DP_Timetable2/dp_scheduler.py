#!/usr/bin/env python3
"""
DP Subject Scheduler - Ottimizzazione dei bracket per minimizzare conflitti
"""

from collections import defaultdict, Counter
from itertools import combinations
import random

# Categorie di materie
SCIENCES = {'Computer Science', 'Physics', 'Biology', 'Chemistry', 'Environmental Sciences Studies (ESS)'}
HUMANITIES = {'Economics', 'Business', 'Global Politics', 'History', 'Geography', 'Politics', 'GeoPolitics'}
ARTS = {'Arts', 'Music', 'Visual Arts'}
LANGUAGES = {'Spanish', 'French'}
ONLINE = {'Psychology (Timetabled Online)'}

def parse_student_choices(raw_data):
    """Parse il formato semicolon-separated delle scelte studenti"""
    choices = raw_data.split(';')
    students = []
    current = []
    
    for choice in choices:
        choice = choice.strip()
        if not choice:
            continue
            
        current.append(choice)
        
        # Ogni studente ha 3 materie
        if len(current) == 3:
            students.append(tuple(current))
            current = []
    
    return students

def get_category(subject):
    """Ritorna la categoria di una materia"""
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
    """Verifica che la combinazione rispetti le regole (2 sci + 1 hum O 1 sci + 2 hum)"""
    science_count = sum(1 for s in subjects if get_category(s) == 'Science')
    humanity_count = sum(1 for s in subjects if get_category(s) == 'Humanity')
    
    # Le lingue e arts possono contare come humanities
    flexible_count = sum(1 for s in subjects if get_category(s) in ['Language', 'Arts'])
    humanity_count += flexible_count
    
    valid = (science_count == 2 and humanity_count == 1) or \
            (science_count == 1 and humanity_count == 2)
    
    return valid, science_count, humanity_count

def count_conflicts(assignment, students):
    """Conta quanti studenti hanno conflitti (due materie nello stesso slot)"""
    conflicts = 0
    conflict_students = []
    
    for idx, student_subjects in enumerate(students):
        slots_used = []
        for subject in student_subjects:
            for slot_idx, slot in enumerate(assignment):
                if subject in slot:
                    slots_used.append(slot_idx)
                    break
        
        # Se uno studente ha 2+ materie nello stesso slot, è un conflitto
        if len(slots_used) != len(set(slots_used)):
            conflicts += 1
            conflict_students.append((idx, student_subjects, slots_used))
    
    return conflicts, conflict_students

def greedy_assignment(students):
    """Algoritmo greedy per assegnare materie a 3 slot"""
    # Conta frequenza di ogni materia
    subject_counts = Counter()
    for student in students:
        for subject in student:
            subject_counts[subject] += 1
    
    # Conta co-occorrenze (quante volte due materie appaiono insieme)
    cooccurrence = defaultdict(int)
    for student in students:
        for s1, s2 in combinations(student, 2):
            key = tuple(sorted([s1, s2]))
            cooccurrence[key] += 1
    
    # Inizia con 3 slot vuoti
    slots = [set(), set(), set()]
    
    # Strategia migliorata: inizia con le coppie più conflittuali
    # e assicurati che siano in slot diversi
    sorted_pairs = sorted(cooccurrence.items(), key=lambda x: -x[1])
    
    # Pre-assegna le materie più problematiche
    assigned = {}
    for (s1, s2), count in sorted_pairs[:5]:  # Top 5 coppie più comuni
        if s1 not in assigned and s2 not in assigned:
            # Assegna a slot diversi
            assigned[s1] = 0
            assigned[s2] = 1
            slots[0].add(s1)
            slots[1].add(s2)
    
    # Ordina materie rimanenti per frequenza
    remaining = [(s, c) for s, c in subject_counts.items() if s not in assigned]
    sorted_subjects = sorted(remaining, key=lambda x: -x[1])
    
    # Assegna ogni materia allo slot che minimizza i conflitti
    for subject, count in sorted_subjects:
        best_slot = 0
        min_conflicts = float('inf')
        
        for slot_idx in range(3):
            # Calcola conflitti se aggiungiamo questa materia a questo slot
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
    """Migliora l'assegnamento usando simulated annealing"""
    current = [set(s) for s in initial_assignment]
    current_conflicts, _ = count_conflicts(current, students)
    best = [set(s) for s in current]
    best_conflicts = current_conflicts
    
    temperature = temp
    
    for i in range(iterations):
        # Scegli una materia random e prova a spostarla in un altro slot
        all_subjects = list(set().union(*current))
        if not all_subjects:
            break
            
        subject = random.choice(all_subjects)
        
        # Trova slot corrente
        current_slot = None
        for idx, slot in enumerate(current):
            if subject in slot:
                current_slot = idx
                break
        
        if current_slot is None:
            continue
        
        # Prova a spostare in un altro slot
        new_slot = random.choice([s for s in range(3) if s != current_slot])
        
        # Crea nuova configurazione
        new_assignment = [set(s) for s in current]
        new_assignment[current_slot].remove(subject)
        new_assignment[new_slot].add(subject)
        
        new_conflicts, _ = count_conflicts(new_assignment, students)
        
        # Accetta se migliore, o con probabilità basata su temperatura
        delta = new_conflicts - current_conflicts
        if delta < 0 or random.random() < np.exp(-delta / temperature):
            current = new_assignment
            current_conflicts = new_conflicts
            
            if current_conflicts < best_conflicts:
                best = [set(s) for s in current]
                best_conflicts = current_conflicts
        
        # Raffredda
        temperature *= 0.9995
    
    return best, best_conflicts

def print_results(assignment, students):
    """Stampa i risultati in modo leggibile"""
    conflicts, conflict_students = count_conflicts(assignment, students)
    
    print("\n" + "="*70)
    print("RISULTATI OTTIMIZZAZIONE BRACKET")
    print("="*70)
    
    for idx, slot in enumerate(assignment, 1):
        print(f"\n📚 SLOT {idx} ({len(slot)} materie):")
        for subject in sorted(slot):
            print(f"   • {subject}")
    
    print("\n" + "-"*70)
    print(f"\n✅ Studenti soddisfatti: {len(students) - conflicts}/{len(students)} ({100*(len(students)-conflicts)/len(students):.1f}%)")
    print(f"❌ Studenti con conflitti: {conflicts}")
    
    if conflict_students:
        print("\n⚠️  STUDENTI CON CONFLITTI:")
        for idx, subjects, slots_used in conflict_students[:10]:  # Mostra primi 10
            print(f"   Studente {idx+1}: {', '.join(subjects)}")
            print(f"      Slots: {slots_used}")
    
    return conflicts

# Importa numpy se disponibile per simulated annealing
try:
    import numpy as np
    USE_SA = True
except ImportError:
    USE_SA = False
    print("NumPy non disponibile - usando solo greedy algorithm")

if __name__ == "__main__":
    # Dati raw
    raw_data = """Computer Science;Physics;Business;Computer Science;Spanish;Business;Biology;Computer Science;Business;Computer Science;Environmental Sciences Studies (ESS);Business;Computer Science;Biology;Business;Visual Arts;Biology;History;Business;Biology;Politics;Business;Chemistry;Physics;Business;Physics;Computer Science;Business;Biology;Politics;French;Environmental Sciences Studies (ESS);Spanish;Business;Computer Science;Spanish;Psychology (Timetabled Online);Biology;Business;Psychology (Timetabled Online);Physics;Computer Science;Business;Biology;Chemistry;Spanish;Physics;Computer Science;Business;Chemistry;Physics;Psychology (Timetabled Online);Biology;GeoPolitics;Psychology (Timetabled Online);Biology;Psychology (Timetabled Online);Politics;Chemistry;Computer Science;History;Computer Science;Business;Spanish;Biology;Psychology (Timetabled Online);Visual Arts;Biology;History;GeoPolitics;Biology;French;Business;Biology;Chemistry;Spanish;Physics;Computer Science;Business"""
    
    print("🔍 Parsing scelte studenti...")
    students = parse_student_choices(raw_data)
    
    print(f"📊 Trovati {len(students)} studenti")
    
    # Valida studenti
    print("\n🔎 Validazione combinazioni...")
    invalid = []
    for idx, student in enumerate(students):
        valid, sci, hum = validate_student(student)
        if not valid:
            invalid.append((idx, student, sci, hum))
    
    if invalid:
        print(f"⚠️  {len(invalid)} studenti con combinazioni non valide:")
        for idx, subjects, sci, hum in invalid[:5]:
            print(f"   Studente {idx+1}: {subjects} (Sci: {sci}, Hum: {hum})")
    
    # Statistiche materie
    subject_counts = Counter()
    for student in students:
        for subject in student:
            subject_counts[subject] += 1
    
    print(f"\n📈 Materie più popolari:")
    for subject, count in subject_counts.most_common(10):
        print(f"   {subject}: {count} studenti")
    
    print("\n🎯 Ottimizzazione in corso...")
    
    # Greedy assignment
    assignment = greedy_assignment(students)
    conflicts = print_results(assignment, students)
    
    # Prova simulated annealing se numpy è disponibile
    if USE_SA and conflicts > 0:
        print("\n🔥 Applicazione Simulated Annealing per migliorare...")
        improved, new_conflicts = simulated_annealing(students, assignment, iterations=5000)
        if new_conflicts < conflicts:
            print(f"\n✨ Miglioramento trovato! Conflitti: {conflicts} → {new_conflicts}")
            print_results(improved, students)
        else:
            print("\nℹ️  Nessun miglioramento trovato con SA")
