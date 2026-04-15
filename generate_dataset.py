import json
import random

# System prompt for the chatbot
system_prompt = (
    "You are the official KLE Technological University (KLE Tech) Virtual Assistant. "
    "Your purpose is to provide highly accurate, professional, and helpful information about the university. "
    "Always use the verified university context. Answer with the category anchor like [CALENDAR] or [FEE] where relevant."
)

# Template groups for automated query synthesis (Mega-Augmentation Mode)
QUERY_TEMPLATES = {
    "factual": [
        "What is the {label}?", "Tell me about {label}.", "Info on {label}.", "{label}?",
        "Can you explain {label}?", "Details on {label} at KLE Tech.", "{label} information?",
        "I want to know about {label}.", "Give me a summary of {label}.", "What's the data for {label}?",
        "Describe {label}.", "Everything about {label}.", "Brief me on {label}.", "List {label} data."
    ],
    "numeric": [
        "How much is {label}?", "What are the charges for {label}?", "{label} fee structure?", "Cost of {label}?",
        "Price for {label}?", "Total fee for {label}?", "What is the {label} amount?", "Give me the {label} price.",
        "How much to pay for {label}?", "Fees of {label}.", "What's the cost of {label}?", "Tell me about {label} charges.",
        "What is the total for {label}?", "Amount of {label}?"
    ],
    "date": [
        "When is {label}?", "What is the date for {label}?", "Day of {label}?", "Schedule for {label}?",
        "On which date is {label}?", "Tell me {label} date.", "When does {label} happen?",
        "What are the dates for {label}?", "Time for {label}?", "Is {label} coming up?",
        "Give me the timing for {label}.", "Can you provide {label} dates?", "On which day is {label}?"
    ],
    "timetable": [
        "What is the {label} timetable?", "Schedule for {label}?", "Classes for {label}?", "Show me {label} timetable.",
        "Daily courses for {label}?", "{label} weekly schedule?", "What's on for {label}?",
        "Can I see the {label} class list?", "{label} day plan?", "Classes on {label}?",
        "Timetable of {label}?", "What is {label} routine?", "Show me {label} sessions."
    ]
}

def expand_fact(labels, answer, category="factual"):
    entries = []
    templates = QUERY_TEMPLATES.get(category, QUERY_TEMPLATES["factual"])
    for label in labels:
        for template in templates:
            entries.append({"user": template.format(label=label), "assistant": answer})
    return entries

# --- Data Definition ---
# Global University Facts [LOCATION / PLACEMENT / RANKING Anchors]
# We saturate these with keywords so the search engine cannot miss them
UNIVERSITY_FACTS = [
    ("location of kle tech university in hubli hubballi vidyanagar karnataka campus address", "[LOCATION]: KLE Tech is located in Hubballi (Hubli), Karnataka, India. Its main campus is in BVB Campus, Vidyanagar."),
    ("where exactly is kle tech university situated hubli hubballi", "[LOCATION]: KLE Tech is situated in Hubballi (Hubli), Karnataka. The campus address is BVB Campus, Vidyanagar."),
    ("how can i reach the kle tech campus in hubballi airport railway station", "[LOCATION]: Reach KLE Tech by Hubballi Airport (HBX), Hubballi Junction (Rail), or via the Vidyanagar campus main gate."),
    ("placement records statistics companies average highest package google amazon", "[PLACEMENT]: KLE Tech has an exceptional placement record with 90%+ students placed yearly. Top companies include Google, Amazon, AWS, Bosch, and Microsoft."),
    ("highest package at kle tech google microsoft placements stats", "[PLACEMENT]: The highest international and domestic packages at KLE Tech often exceed INR 30-40 Lakhs per annum for top engineering roles."),
    ("university ranking nirf karnataka top engineering colleges best in hubli", "[RANKING]: KLE Tech is consistently ranked among the top engineering colleges in Karnataka and features in the NIRF ranking bands.")
]

HOLIDAYS = [
    ("Chandramana Ugadi", "19th March 2026"),
    ("Compensatory Holiday", "20th March 2026"),
    ("Ramzan (Eid-ul-Fitr)", "21st March 2026"),
    ("Mahavir Jayanti", "31st March 2026"),
    ("Good Friday", "3rd April 2026"),
    ("Ambedkar Jayanti", "14th April 2026"),
    ("Basava Jayanti", "20th April 2026"),
    ("May Day", "1st May 2026"),
    ("Bakrid (Eid-ul-Adha)", "28th May 2026")
]

MONTHS_HOLIDAYS = {
    "March 2026": "Ugadi (19th March), Compensatory (20th March), Ramzan (21st March), and Mahavir Jayanti (31st March).",
    "April 2026": "Good Friday (3rd April), Ambedkar Jayanti (14th April), and Basava Jayanti (20th April).",
    "May 2026": "May Day (1st May) and Bakrid (28th May)."
}

DEPARTMENTS = ['B.E. Computer Science', 'B.E. E&C', 'B.E. Mechanical', 'B.E. Civil']
DIVISIONS = ['A', 'B', 'C', 'D', 'E', 'F']

TIMETABLE_DATA = {
    'VI D': {
        'Monday': 'EIS (8-10, CLH304), Elective (10:15-12:15), Minor Project (1:30-5:30)',
        'Tuesday': 'CCN-SHS (8-10, SEE302), Electives (10:15-1:30), AE LAB D1 & CCN LAB D2 (1:30-3:30)',
        'Wednesday': 'GEN AI-SSC+SVK (8-10, SEE209), CCN-SHS (10:15-12:15, SEE204), AE-BP (1:30-2:30, SEE110)',
        'Thursday': 'PALR (8-10, SEE303), GEN AI-SSC+SVK (10:15-12:15, SEE208)',
        'Friday': 'AE-BP (9-10, SEE204), AE LAB D2 & CCN LAB D1 (10:15-12:15), PALR (1:30-3:30, SEE303)'
    },
    'VI A': {'Monday': 'PALR (8-10, SEE303), Elective (10:15-12:15), Minor Project (1:30-4:30)'},
    'VI B': {'Monday': 'EIS (8-10), Elective (10:15-12:15), CCN-SKG (1:30-2:30), Minor Project (2:30-5:30)'},
    'VI C': {'Monday': 'AE-GHM (8-10, SEE210), Minor Project (10:15-1:30)', 'Thursday': 'PALR (10:15-12:15), EIS (1:30-3:30)'},
    'VI E': {'Tuesday': 'CCN-SHS (8-10), Electives (10:15-1:30)', 'Friday': 'Project Lab (1:30-5:30)'},
    'VI F': {'Monday': 'EIS (8-10), PALR (10:15-12:15)', 'Wednesday': 'Full Day Project Work (9-5)'}
}

# --- Generation Logic ---
final_pairs = []

# 1. Identity & Purpose [PERSONA Anchor]
final_pairs.extend(expand_fact(
    ["who you are", "your role", "KLE Tech Assistant", "are you a person"], 
    "[PERSONA]: I am the official Virtual Assistant for KLE Technological University (KLE Tech). I am an AI designed to help with university-related information."
))

# 1b. Global Facts [LOCATION / PLACEMENT / RANKING Anchors]
for query_label, fact_ans in UNIVERSITY_FACTS:
    final_pairs.extend(expand_fact(
        [query_label, f"Tell me about {query_label}", f"Info on {query_label}"],
        fact_ans,
        "factual"
    ))

# 2. Fees [FEE Anchor]
final_pairs.extend(expand_fact(
    ["KCET fee B.E.", "Government quota fee", "CET quota charges"], 
    "[FEE]: The KCET / Government Quota fee for B.E. is approximately INR 1,25,000 per annum.", 
    "numeric"
))
final_pairs.extend(expand_fact(
    ["COMEDK fee B.E.", "Management quota fee", "COMEDK entry price"], 
    "[FEE]: The COMEDK quota fee for B.E. is approximately INR 2,25,000 per annum.", 
    "numeric"
))

# 3. Holidays [CALENDAR Anchor]
for name, date in HOLIDAYS:
    final_pairs.extend(expand_fact(
        [f"{name} holiday", f"{name} date", f"Is {date} a holiday"], 
        f"[CALENDAR]: {name} is a university holiday on {date}.", 
        "date"
    ))

# 4. Monthly Summaries [CALENDAR Anchor]
for month, summary in MONTHS_HOLIDAYS.items():
    final_pairs.extend(expand_fact(
        [f"holidays in {month}", f"list {month} holidays", f"all {month} holidays"], 
        f"[CALENDAR]: The holidays in {month} are: {summary}", 
        "factual"
    ))

# 5. Full 2026 Summary [CALENDAR Anchor]
all_hols = ", ".join([f"{n} ({d})" for n, d in HOLIDAYS])
final_pairs.extend(expand_fact(
    ["all holidays in 2026", "2026 holiday calendar", "list every holiday"], 
    f"[CALENDAR]: The university holidays for 2026 are: {all_hols}", 
    "factual"
))

# 6. Timetables [ACADEMIC Anchor]
for div_key, days in TIMETABLE_DATA.items():
    for day, schedule in days.items():
        final_pairs.extend(expand_fact(
            [f"{day} timetable for {div_key}", f"classes for {div_key} on {day}", f"{div_key} {day} schedule"], 
            f"[ACADEMIC]: {day} schedule for {div_key} is: {schedule}.", 
            "timetable"
        ))

# 7. Academic Dates [ACADEMIC Anchor]
final_pairs.extend(expand_fact(
    ["Minor 1 exam", "ISA-1 dates", "Minor 2", "ISA-2", "ESA Theory Exams", "final exams"], 
    "[ACADEMIC]: Minor 1 (26-28 March), Minor 2 (18-20 May), and ESA Exams (start from 19th June 2026).", 
    "date"
))

# Shuffle and Write to JSONL
random.shuffle(final_pairs)
with open('kle_tech_dataset.jsonl', 'w', encoding='utf-8') as f:
    for pair in final_pairs:
        line = {"system": system_prompt, "user": pair["user"], "assistant": pair["assistant"]}
        f.write(json.dumps(line) + '\n')

print(f"Brute Force Augmentation Complete! Generated {len(final_pairs)} samples.")
