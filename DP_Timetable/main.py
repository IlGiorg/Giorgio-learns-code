# ============================================
# SUBJECTS + TEACHERS
# ============================================

teachers = {
    "Computer Science": ["NMA"],
    "Physics": ["ARS", "JDO"],
    "ESS": ["GMA"],
    "Italian A": ["SDI", "GIA", "MBO"],
    "Italian B": ["EGA"],
    "Economics": ["ATR"],
    "Business": ["GEV"],
    "Spanish": ["IZO", "CCA"],
    "Mathematics": ["SZI", "LSI", "ARS"],
    "Psychology": ["JJA"],
    "Chemistry": ["JJO", "GMA"],
    "History": ["GST"],
    "Geography": ["AEV"],
    "Global Politics": ["AEV"],
    "Biology": ["IAM"],
    "Visual Arts": ["LGA", "ERO"],
    "French": ["ABE"]
}

group3 = ["Economics", "Business", "Psychology", "History", "Geography", "Global Politics", "ESS"]
group4 = ["Computer Science", "Biology", "Chemistry", "Physics"]
group6 = ["Visual Arts", "French", "Spanish"]

required_pairs = [
    ("Spanish", "Psychology"),
    ("Spanish", "Computer Science"),
    ("Computer Science", "Psychology"),
    ("Biology", "Chemistry"),
    ("Chemistry", "Global Politics"),
    ("Chemistry", "Psychology"),
    ("Computer Science", "Business"),
    ("Biology", "Psychology")
]

# ============================================
# BLOCK CHECK FUNCTIONS
# ============================================

def teacher_conflict(block, subject):
    """Return True if adding this subject causes teacher double-booking."""
    new_teachers = set(teachers[subject])
    for existing in block:
        existing_teachers = set(teachers[existing])
        if new_teachers & existing_teachers:  # intersection
            return True
    return False


def pair_conflict(block, subject):
    """Return True if putting subject in block violates student combinations."""
    for (a, b) in required_pairs:
        if subject == a and b in block:
            return True
        if subject == b and a in block:
            return True
    return False


# ============================================
# BLOCK BUILDER
# ============================================

def place_subject(blocks, subject):
    """Place a subject in the first legal block."""
    for block in blocks:
        if not teacher_conflict(block, subject) and not pair_conflict(block, subject):
            block.append(subject)
            return True
    return False  # no legal placement found


def build_blocks():
    blocks = [[], [], []]  # 3 DP blocks

    # Pre-seed based on strongest constraints:
    place_subject(blocks, "Biology")
    place_subject(blocks, "Chemistry")
    place_subject(blocks, "Physics")
    place_subject(blocks, "Computer Science")
    place_subject(blocks, "Psychology")
    place_subject(blocks, "Spanish")

    # Fill Group 3 subjects
    for s in group3:
        if s not in sum(blocks, []):
            place_subject(blocks, s)

    # Fill Group 6 subjects
    for s in group6:
        if s not in sum(blocks, []):
            place_subject(blocks, s)

    return blocks


# ============================================
# RUN
# ============================================

blocks = build_blocks()

print("Teacher-Safe IB Blocks:\n")
for i, block in enumerate(blocks, start=1):
    print(f"Block {i}: {', '.join(block)}")
