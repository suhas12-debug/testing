import json
import os

# --- Data Definition (Manual Variations) ---

UNIVERSITY_FACTS = [
    (
        ["Where is KLE Tech located?", "Campus location?", "Give me the university address."],
        "[LOCATION]: KLE Tech is located in Hubballi (Hubli), Karnataka, India. Its main campus is in BVB Campus, Vidyanagar."
    ),
    (
        ["How to reach the campus?", "Nearest airport or railway station?", "Travel info for KLE Tech."],
        "[LOCATION]: You can reach the campus via Hubballi Airport (HBX) or Hubballi Junction Railway Station. It is situated in Vidyanagar."
    ),
    (
        ["Tell me about placement records.", "How are the placements at KLE Tech?", "Placement statistics and companies."],
        "[PLACEMENT]: KLE Tech has an exceptional placement record with 90%+ students placed yearly. Top companies include Google, Amazon, AWS, Bosch, and Microsoft."
    ),
    (
        ["What is the highest package?", "Google placement package?", "Highest domestic and international package."],
        "[PLACEMENT]: The highest international and domestic packages at KLE Tech often exceed INR 30-40 Lakhs per annum for top engineering roles."
    ),
    (
        ["University ranking info?", "NIRF ranking of KLE Tech?", "Is it a top engineering college?"],
        "[RANKING]: KLE Tech is consistently ranked among the top engineering colleges in Karnataka and features in the NIRF ranking bands."
    )
]

FEES = [
    (
        ["What is the KCET fee?", "Government quota fee for B.E.?", "CET quota charges."],
        "[FEE]: The KCET / Government Quota fee for B.E. is approximately INR 1,25,000 per annum."
    ),
    (
        ["COMEDK fee structure?", "Management quota fee for B.E.?", "How much is COMEDK entry?"],
        "[FEE]: The COMEDK quota fee for B.E. is approximately INR 2,25,000 per annum."
    )
]

HOLIDAYS = [
    ("Chandramana Ugadi", "19th March 2026", ["When is Ugadi?", "Ugadi holiday date?", "Is 19th March a holiday?"]),
    ("Compensatory Holiday", "20th March 2026", ["Is 20th March a holiday?", "When is the compensatory holiday?", "Next holiday after Ugadi?"]),
    ("Ramzan (Eid-ul-Fitr)", "21st March 2026", ["Ramzan date?", "Eid-ul-Fitr holiday?", "When is Eid?"]),
    ("Mahavir Jayanti", "31st March 2026", ["Mahavir Jayanti date?", "Is 31st March a holiday?", "When is Mahavir Jayanti?"]),
    ("Good Friday", "3rd April 2026", ["Good Friday date?", "Is Good Friday a holiday?"]),
    ("Ambedkar Jayanti", "14th April 2026", ["Ambedkar Jayanti date?", "When is Ambedkar Jayanti?"]),
    ("Basava Jayanti", "20th April 2026", ["Basava Jayanti date?", "Basava Jayanti holiday?"]),
    ("May Day", "1st May 2026", ["When is May Day?", "Is 1st May a holiday?"]),
    ("Bakrid", "28th May 2026", ["Bakrid date?", "Bakrid holiday?"])
]

# --- Timetable Data Construction (Manual + Placeholder) ---
# We will generate a complete 6-day x 6-division grid for both IV and VI semesters

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
DIVISIONS = ["A", "B", "C", "D", "E", "F"]

def generate_placeholder_day(semester, div, day):
    # Just a placeholder generator to fill the requested grid
    # Format: 'SubjectCode-TeacherInitials (time, room)'
    if semester == "VI" and div == "D":
        # Keep real data for VI D as requested (from original source)
        real_data = {
            'Monday': 'EIS (8-10, CLH304), Elective (10:15-12:15), Minor Project (1:30-5:30)',
            'Tuesday': 'CCN-SHS (8-10, SEE302), Electives (10:15-1:30), AE LAB D1 & CCN LAB D2 (1:30-3:30)',
            'Wednesday': 'GEN AI-SSC+SVK (8-10, SEE209), CCN-SHS (10:15-12:15, SEE204), AE-BP (1:30-2:30, SEE110)',
            'Thursday': 'PALR (8-10, SEE303), GEN AI-SSC+SVK (10:15-12:15, SEE208)',
            'Friday': 'AE-BP (9-10, SEE204), AE LAB D2 & CCN LAB D1 (10:15-12:15), PALR (1:30-3:30, SEE303)',
            'Saturday': 'Self-Study / Project Work (9-1)'
        }
        return real_data.get(day, "Self-Study (9-1)")
    
    # Generic placeholder for others
    code = f"CS{semester}{div}"
    return f"{code}-T1 (9-11, RM401), Lab-{div} (11:15-1:15)"

# --- Final Assembly ---
final_pairs = []

# 1. Identity
final_pairs.append({"user": "Who are you?", "assistant": "[PERSONA]: I am the official Virtual Assistant for KLE Technological University (KLE Tech)."})
final_pairs.append({"user": "Tell me your role.", "assistant": "[PERSONA]: I am an AI assistant designed to provide accurate information about KLE Tech university."})

# 2. Add University Facts
for questions, answer in UNIVERSITY_FACTS:
    for q in questions:
        final_pairs.append({"user": q, "assistant": answer})

# 3. Add Fees
for questions, answer in FEES:
    for q in questions:
        final_pairs.append({"user": q, "assistant": answer})

# 4. Add Holidays
for name, date, questions in HOLIDAYS:
    ans = f"[CALENDAR]: {name} is a university holiday on {date}."
    for q in questions:
        final_pairs.append({"user": q, "assistant": ans})

# 5. Add Timetables (VI and IV Semester)
for sem in ["IV", "VI"]:
    for div in DIVISIONS:
        for day in DAYS:
            schedule = generate_placeholder_day(sem, div, day)
            ans = f"[ACADEMIC]: {day} schedule for {sem} {div} is: {schedule}."
            
            # Manual question variations as requested
            final_pairs.append({"user": f"What is the {day} timetable for {sem} {div}?", "assistant": ans})
            final_pairs.append({"user": f"Classes for division {div} semester {sem} on {day}?", "assistant": ans})
            final_pairs.append({"user": f"{sem} {div} {day} schedule.", "assistant": ans})

# 6. Academic Dates
final_pairs.append({"user": "When are Minor 1 exams?", "assistant": "[ACADEMIC]: Minor 1 (26-28 March)."})
final_pairs.append({"user": "ESA theory exam dates?", "assistant": "[ACADEMIC]: ESA Exams start from 19th June 2026."})

# --- Write to Output ---
# No shuffle, No system prompt, format: {"user": q, "assistant": a}
with open('kle_tech_dataset.jsonl', 'w', encoding='utf-8') as f:
    for pair in final_pairs:
        f.write(json.dumps(pair) + '\n')

print(f"Dataset Refactor Complete! Generated {len(final_pairs)} manual/placeholder samples.")
