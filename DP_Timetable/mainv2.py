# =======================================================
# SUBJECTS + TEACHERS
# =======================================================

teachers = {
    "Computer Science": ["NMA"],
    "Physics": ["ARS", "JDO"],
    "ESS": ["GMA"],
    "Economics": ["ATR"],
    "Business": ["GEV"],
    "Psychology": ["JJA"],
    "History": ["GST"],
    "Geography": ["AEV"],
    "Global Politics": ["AEV"],
    "Biology": ["IAM"],
    "Chemistry": ["JJO", "GMA"],
    "Visual Arts": ["LGA", "ERO"],
    "French": ["ABE"],
    "Spanish": ["IZO", "CCA"]
}

group3 = ["Economics", "Business", "Psychology", "History", "Geography", "Global Politics", "ESS"]
group4 = ["Computer Science", "Biology", "Chemistry", "Physics"]
group6 = ["Visual Arts", "French", "Spanish"]

# Required student combinations
required_pairs = [
    ("Spanish", "Psychology"),
    ("Spanish", "Computer Science"),
    ("Computer Science", "Psychology"),
    ("Biology", "Chemistry"),
    ("Chemistry", "Global Politics"),
    ("Chemistry", "Psychology"),
    ("Biology", "Psychology")
]


# =======================================================
# VALIDATION HELPERS
# =======================================================

def teacher_conflict(block, subject):
    """Check if adding subject causes teacher double-booking."""
    subject_teachers = set(teachers[subject])
    for s in block:
        if subject_teachers & set(teachers[s]):
            return True
    return False


def pair_conflict(block, subject):
    """Check if required student combinations would be blocked."""
    for a, b in required_pairs:
        if subject == a and b in block: return True
        if subject == b and a in block: return True
    return False


def place(blocks, subject):
    """Try to place a subject in the first valid block."""
    for block in blocks:
        if not teacher_conflict(block, subject) and not pair_conflict(block, subject):
            block.append(subject)
            return True
    return False


# =======================================================
# BLOCK GENERATOR
# =======================================================

def generate_blocks():
    # Three DP blocks
    blocks = [[], [], []]

    # -------------------------
    # Strongest constraints first
    # -------------------------

    # Group 4 must appear in all blocks
    mandatory_g4 = ["Biology", "Chemistry", "Physics", "Computer Science"]
    for i, subject in enumerate(mandatory_g4):
        place(blocks, subject)

    # Psychology must be away from CS + Spanish
    place(blocks, "Psychology")

    # Spanish must be away from Psych + CS
    place(blocks, "Spanish")

    # Add Group 3 subjects
    for subject in group3:
        if subject not in sum(blocks, []):
            place(blocks, subject)

    # Add Group 6 subjects
    for subject in group6:
        if subject not in sum(blocks, []):
            place(blocks, subject)

    # -------------------------
    # Guarantee each block has:
    # - at least 1 Group 3
    # - at least 1 Group 4
    # -------------------------
    for block in blocks:
        if not any(s in group3 for s in block):
            # add a group 3 that fits
            for s in group3:
                if s not in block and place([block], s):
                    break

        if not any(s in group4 for s in block):
            # add a group 4 that fits
            for s in group4:
                if s not in block and place([block], s):
                    break

    return blocks


# =======================================================
# RUN
# =======================================================

blocks = generate_blocks()

print("\nOptimised IB Blocks (Teacher-Safe, Group-3/4 ensured):\n")
for i, block in enumerate(blocks, start=1):
    print(f"Block {i}:")
    for subject in block:
        teacher_list = ", ".join(teachers[subject])
        print(f"  - {subject} ({teacher_list})")
    print()
