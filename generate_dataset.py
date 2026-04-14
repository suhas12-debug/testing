import json
import random

# System prompt for all entries
system_prompt = "You are an intelligent, helpful virtual assistant for KLE Technological University (KLE Tech), Hubballi. Provide accurate information about courses, fees, placements, and campus details to prospective and current students."

data_pairs = [
    # ---------------- 1. General Info ----------------
    {
        "questions": [
            "Tell me about KLE Tech.",
            "What is the history of KLE Technological University?",
            "When was KLE Tech established?",
            "Where is KLE Tech located?"
        ],
        "answer": "KLE Technological University (KLE Tech), located in Vidyanagar, Hubballi, Karnataka, is a state private university. It was originally established in 1947 as B.V. Bhoomaraddi College of Engineering and Technology (BVBCET) and gained University status in 2015. It has a lush 64-acre campus and operates with the motto 'Technology for Human Welfare'."
    },
    {
        "questions": [
            "How big is the Hubballi campus?",
            "What is the campus size of KLE Tech?",
            "Where is the campus situated?"
        ],
        "answer": "The KLE Tech main campus is situated in Vidyanagar, Hubballi, Karnataka, and spans across a lush 64-acre area known for its state-of-the-art infrastructure and research-driven environment."
    },
    
    # ---------------- 2. UG Programs ----------------
    {
        "questions": [
            "What undergraduate programs are offered at KLE Tech?",
            "List all the UG courses available.",
            "Does KLE Tech offer architecture or management degrees?"
        ],
        "answer": "At KLE Tech, Hubballi, we offer a diverse range of undergraduate programs. \nEngineering (B.E.): Computer Science & Engineering, Computer Science (AI), Electronics & Communication, Electronics Engineering (VLSI Design), Mechanical, Civil, Biotechnology, Automation & Robotics, and Electrical & Electronics Engineering.\nArchitecture: Bachelor of Architecture (B.Arch).\nManagement & Others: BBA, BCA, and B.Sc. in Fashion and Apparel Design."
    },
    
    # ---------------- 3. ECE Curriculum ----------------
    {
        "questions": [
            "What is the curriculum for the 3rd semester of ECE?",
            "Which subjects are taught in the 2nd year, 3rd sem of Electronics & Communication?",
            "ECE 3rd sem subjects?"
        ],
        "answer": "In the 3rd Semester of B.E. Electronics & Communication at KLE Tech, the subjects include: Integral Transforms and Statistics, Corporate Communication, Circuit Analysis, Analog Electronic Circuits, Digital Circuits, Signals & Systems, Digital Circuits Lab, Analog Electronic Circuits Lab, Microcontroller Architecture & Programming, and C Programming (for Diploma students)."
    },
    {
        "questions": [
            "Tell me the subjects in the 4th semester of ECE.",
            "What will I study in Sem 4 ECE?",
            "Syllabus for ECE 4th sem"
        ],
        "answer": "The 4th Semester ECE curriculum includes: Linear Algebra & Partial Differential Equations, Problem Solving & Analysis, Electromagnetic Fields and Waves, Linear Integrated Circuits, Control Systems, ARM Processor & Applications, Digital System Design Using Verilog, and various labs including Data Acquisition, ARM Microcontroller, and Data Structure Applications."
    },
    {
        "questions": [
            "What are the 5th semester subjects for ECE?",
            "ECE Sem 5 syllabus",
            "What do 3rd year ECE students study in their first sem?"
        ],
        "answer": "For Semester 5 in ECE, students study Arithmetical Thinking & Analytical Reasoning, CMOS VLSI Circuits, Communication System, Digital Signal Processing, Operating System & Embedded Systems Design, Machine Learning, along with RTOS Lab, CMOS VLSI Circuits Lab, and a Mini Project."
    },
    {
        "questions": [
            "What is the curriculum for 6th semester ECE?",
            "6th Sem ECE subjects?"
        ],
        "answer": "Semester 6 of ECE includes: Professional Aptitude and Logical Reasoning, Industry Readiness & Leadership Skills, Automotive Electronics, Computer Communication Networks I, PSE Elective 1, associated labs, and Minor Project I & II."
    },
    {
        "questions": [
            "What subjects are in the final year 7th semester of ECE?",
            "What do 4th year ECE students study?"
        ],
        "answer": "The 7th Semester of ECE focuses heavily on electives and projects. It includes: Advanced Communication Networks, PSE Electives 2, 3, 4, and 5, Senior Design Project, and Constitution of India & Professional Ethics (CIPE)."
    },
    {
        "questions": [
            "What is the syllabus for the 8th semester ECE?",
            "Do we have an internship in the final semester of ECE?"
        ],
        "answer": "Yes, the 8th Semester of ECE is highly practical. It includes PSE Elective 6, Open Elective 1, a comprehensive Internship (Training & Project), and the Final Project Work."
    },

    # ---------------- 4. Placements ----------------
    {
        "questions": [
            "What is the highest placement package of all time at KLE Tech?",
            "Highest package ever recorded?",
            "Who gave the highest placement and for how much?"
        ],
        "answer": "The highest package ever recorded at KLE Technological University is an impressive INR 46.38 LPA, which was offered to a student of the 2024 batch by Amazon."
    },
    {
        "questions": [
            "What is the average package at KLE Tech?",
            "What is the median salary for graduates?"
        ],
        "answer": "The average placement package at KLE Tech is approximately INR 5.3 LPA, with the median package for undergraduate programs sitting around INR 7.00 LPA in recent years."
    },
    {
        "questions": [
            "Tell me about the placements in 2024.",
            "What were the placement highlights for the 2024 batch?",
            "How were the 2024 placements?"
        ],
        "answer": "For the 2024 batch, the highest package was INR 46.38 LPA by Amazon. Other significant offers included Texas Instruments (9 students selected at INR 28 LPA), AWS (INR 26 LPA), Applied Materials (11 students selected at INR 13.75 LPA), and Mercedes-Benz (INR 10 LPA). Key recruiters included TCS, Deloitte, and Tata Elxsi."
    },
    {
        "questions": [
            "What were the placement statistics for 2023?",
            "How was the hiring in 2023?",
            "Tell me about MBA placements."
        ],
        "answer": "In 2023, the highest package was approximately INR 33.00 LPA. A historic milestone was Bosch Global Software Technologies (BGSW) hiring 249 students in a single go. Notably, the MBA 2023-2024 batch achieved 100% placement."
    },
    {
        "questions": [
            "Can you give details about the 2022 placements?",
            "Who were the top recruiters in 2022 and what was the highest package?"
        ],
        "answer": "In 2022, the highest package reached INR 43.00 LPA, offered by Twilio. Other major recruiters included Cognizant (272 students), Accenture (115), and Capgemini (91). Amazon AWS also hired 40 students."
    },
    {
        "questions": [
            "Who are the top recruiters at KLE Tech?",
            "Which companies visit KLE Tech for placements?",
            "List some leading recruiters."
        ],
        "answer": "Major recruiters include Amazon, Google India, AWS, Twilio, Texas Instruments, Applied Materials, Mercedes-Benz, Bosch, Deloitte, TCS, Siemens, and Tata Elxsi. Many of these companies offer high-value roles and long-term internships."
    },
    {
        "questions": [
            "Who is the Placement Officer at KLE Tech?",
            "Who manages placements at KLE Tech Hubballi?",
            "Contact info for placement cell?"
        ],
        "answer": "The Training and Placement Cell in Hubballi is headed by Prof. C. D. Kerure (Placement Officer). Other key members include Prof. Bhargavi Pandurangi (Management Coordinator), Dr. Alok Gaddi (Industry Interaction), and Dr. Suvarna Nimbagal (BBA Head)."
    },
    {
        "questions": [
            "What does the Placement Cell do?",
            "How does the placement office help students?",
            "Does the college provide resume building help?"
        ],
        "answer": "The Placement Cell facilitates internships, Pre-Placement Offers (PPOs), and skill-development. It organizes technical workshops, resume-building sessions, and mock interviews. It also acts as a bridge between industry and academia, ensuring students are industry-ready."
    },

    # ---------------- 5. Fees Structure ----------------
    {
        "questions": [
            "What is the fee structure for B.E. through KCET?",
            "How much are the tuition fees if I come through the KCET quota?",
            "Fees for CET students?"
        ],
        "answer": "For the Academic Year 2024-25, the fee for students entering through the KCET (Government Quota) is approximately INR 1,25,000 per annum in total (including tuition and other university fees)."
    },
    {
        "questions": [
            "What is the COMEDK fee structure for undergraduate programs?",
            "How much is the fee if I apply via COMEDK?",
            "COMEDK fees for 2024?"
        ],
        "answer": "For the Academic Year 2024-25, the total fee for students entering through the COMEDK Quota is approximately INR 2,25,000 per annum. This includes a tuition fee of INR 2,05,000 and other university fees of around INR 20,000."
    },
    {
        "questions": [
            "Are the tuition fees the same for all engineering branches?",
            "Does CSE have a different fee than Mechanical in KCET?"
        ],
        "answer": "For KCET and COMEDK quotas, the designated fee structures (approx. ₹1.25L for KCET and ₹2.25L for COMEDK) apply uniformly across major B.E. branches like Computer Science (CSE), ECE, AI & DS, Mechanical, Civil, and Biotechnology. Management quota fees, however, vary significantly based on the demand for specific branches."
    },
    
    # ---------------- 6. Campus Life & Facilities ----------------
    {
        "questions": [
            "What are the hostel facilities?",
            "Is there a hostel for boys and girls?",
            "Tell me about the hostel accommodation."
        ],
        "answer": "KLE Tech provides excellent, secure hostel facilities for both boys and girls within the campus. The hostels are equipped with Wi-Fi, 24/7 security, hygienic mess food, reading rooms, and indoor sports facilities."
    },
    {
        "questions": [
            "How is the library at KLE Tech?",
            "Tell me about library facilities.",
            "Are there good reading rooms?"
        ],
        "answer": "The central library at KLE Tech is a vast, state-of-the-art resource center. It houses thousands of physical volumes, digital journals, e-books, and features air-conditioned reading halls that foster a great learning environment."
    },
    {
        "questions": [
            "What student clubs and extracurriculars are there?",
            "Are there any clubs for robotics or aero at KLE?",
            "Tell me about campus activities."
        ],
        "answer": "KLE Tech boasts a vibrant campus life with numerous student clubs! Popular ones include the Aero Club, Robotics Center, SAE Baja racing teams, coding clubs, and cultural committees. It encourages students to participate in national-level technical competitions."
    },
    
    # ---------------- 7. Admissions & Contact ----------------
    {
        "questions": [
            "How to apply for admission?",
            "What is the admission process?",
            "How can I join KLE Tech?"
        ],
        "answer": "Admissions to B.E. programs are primarily done through KCET (Karnataka CET), COMEDK, and Management quota. Aspiring students must meet the required cutoff ranks during the official counseling rounds of these exams."
    },
    {
        "questions": [
            "How do I contact KLE Tech?",
            "What is the university helpline?",
            "Give me the contact details for the university."
        ],
        "answer": "You can contact KLE Technological University via their official website (kletech.ac.in). For direct inquiries, you may reach out to the university administration located in Vidyanagar, Hubballi."
    },

    # ---------------- 8. Academic Calendar - Even Semester 2025-26 ----------------
    {
        "questions": [
            "When does the even semester start?",
            "What is the term commencement date?",
            "When does college begin for even semester 2025-26?"
        ],
        "answer": "The Even Semester 2025-26 commenced on 16th February 2026 for all programs — B.E. (2nd, 4th, 6th Sem), B.Arch (2nd, 4th, 6th, 8th Sem), BBA, BCA, B.Com (4th Sem), and B.Sc. FAD (2nd & 4th Sem)."
    },
    {
        "questions": [
            "When does the even semester end?",
            "What is the end of term date?",
            "When does the semester close?"
        ],
        "answer": "The Even Semester 2025-26 ends on 9th June 2026 for all programs."
    },
    {
        "questions": [
            "When is Registration Day?",
            "When did registration happen this semester?"
        ],
        "answer": "Registration Day for the Even Semester 2025-26 is 16th February 2026."
    },
    {
        "questions": [
            "When is the last date for registration?",
            "Deadline for registration this semester?"
        ],
        "answer": "The last date for registration in the Even Semester 2025-26 is 23rd February 2026."
    },
    {
        "questions": [
            "When is Minor 1?",
            "What are the dates of Minor 1 exam?",
            "When is minor exam 1 scheduled?"
        ],
        "answer": "Minor 1 (ISA-1) is scheduled on 26th, 27th, and 28th March 2026 (Week 5, Wednesday to Friday)."
    },
    {
        "questions": [
            "When is Minor 1 marks display?",
            "When are Minor 1 results announced?",
            "When will Minor 1 marks be shown?"
        ],
        "answer": "Minor 1 Marks Display is on 10th April 2026."
    },
    {
        "questions": [
            "When is Make-Up Minor 1?",
            "When is the re-exam for Minor 1?",
            "Makeup exam date for Minor 1?"
        ],
        "answer": "The Make-Up Minor 1 exam is scheduled from 2nd to 7th April 2026."
    },
    {
        "questions": [
            "When is Minor 2?",
            "What are the dates of Minor 2 exam?",
            "When is minor exam 2 scheduled?"
        ],
        "answer": "Minor 2 (ISA-2) is scheduled on 18th, 19th, and 20th May 2026 (Week 14, Monday to Wednesday)."
    },
    {
        "questions": [
            "When is Minor 2 marks display?",
            "When are Minor 2 results out?",
            "When can I see my Minor 2 marks?"
        ],
        "answer": "Minor 2 Marks Display is on 26th May 2026."
    },
    {
        "questions": [
            "When is Make-Up Minor 2?",
            "When is the re-exam for Minor 2?",
            "Makeup exam date for Minor 2?"
        ],
        "answer": "The Make-Up Minor 2 exam is scheduled from 23rd to 27th May 2026."
    },
    {
        "questions": [
            "When is Pleiades?",
            "What are the dates of the Pleiades festival?",
            "When is the annual fest?"
        ],
        "answer": "Pleiades, the annual cultural and technical fest of KLE Tech, is scheduled from 8th May to 10th May 2026 (Week 12)."
    },
    {
        "questions": [
            "When is Formative Feedback?",
            "What are the formative feedback dates?",
            "When is the feedback week?"
        ],
        "answer": "Formative Feedback is scheduled from 16th to 19th March 2026 (Week 4)."
    },
    {
        "questions": [
            "When is Summative Feedback?",
            "What are the summative feedback dates?"
        ],
        "answer": "Summative Feedback is scheduled from 4th to 6th May 2026 (Week 11)."
    },
    {
        "questions": [
            "When is the first monthly attendance report?",
            "When is the attendance report for March?"
        ],
        "answer": "The first Monthly Attendance Report is on 2nd March 2026 (Week 3)."
    },
    {
        "questions": [
            "When is the second monthly attendance report?",
            "When is the CCM 2 meeting?",
            "CCM-2 date?"
        ],
        "answer": "The second Class Committee Meeting (CCM-2) is on 10th and 11th April 2026."
    },
    {
        "questions": [
            "When is the third monthly attendance report?",
            "When is CCM-3?",
            "When is the last committee meeting?"
        ],
        "answer": "The third Class Committee Meeting (CCM-3) is on 11th and 12th May 2026 (Week 13)."
    },
    {
        "questions": [
            "When is the final attendance or marks display?",
            "When is the final marks display this semester?"
        ],
        "answer": "The Final Attendance / Marks Display is on 9th June 2026."
    },
    {
        "questions": [
            "When is student counselling?",
            "What are the student counselling dates?",
            "When does counselling happen?"
        ],
        "answer": "Student Counselling - 1 is from 30th March to 7th April 2026. Student Counselling - 2 is from 25th to 30th May 2026."
    },
    {
        "questions": [
            "When is the last date to drop a course?",
            "Deadline to drop a subject this semester?"
        ],
        "answer": "The last date for course(s) dropping is 10th April 2026."
    },
    {
        "questions": [
            "When is the last date to withdraw from a course?",
            "Deadline for course withdrawal?"
        ],
        "answer": "The last date for course(s) withdrawal is 1st June 2026."
    },
    {
        "questions": [
            "When is last date to apply for Make-Up Minor 1?",
            "Deadline to apply for Minor 1 makeup?"
        ],
        "answer": "The last date for applying for Make-Up Minor 1 is 1st April 2026."
    },
    {
        "questions": [
            "When is last date to apply for Make-Up Minor 2?",
            "Deadline to apply for Minor 2 makeup?"
        ],
        "answer": "The last date for applying for Make-Up Minor 2 is 22nd May 2026."
    },
    {
        "questions": [
            "When is Ramzan holiday?",
            "Is there a Ramzan holiday this semester?"
        ],
        "answer": "Ramzan (Eid-ul-Fitr) is observed as a holiday on 21st March 2026."
    },
    {
        "questions": [
            "When is Ugadi holiday?",
            "What is the date of Ugadi?"
        ],
        "answer": "Chandramana Ugadi is on 19th March 2026, and it is a holiday."
    },
    {
        "questions": [
            "When is the compensatory holiday?",
            "When is the compensatory off?"
        ],
        "answer": "The Compensatory Holiday is on 20th March 2026."
    },
    {
        "questions": [
            "When is Mahavir Jayanti?",
            "Is Mahavir Jayanti a holiday?"
        ],
        "answer": "Mahavir Jayanti is on 31st March 2026, and it is a holiday."
    },
    {
        "questions": [
            "When is Good Friday?",
            "Is Good Friday a holiday this semester?"
        ],
        "answer": "Good Friday is on 3rd April 2026, and it is a holiday."
    },
    {
        "questions": [
            "When is Ambedkar Jayanti?",
            "Is Ambedkar Jayanti a holiday?"
        ],
        "answer": "Ambedkar Jayanti is on 14th April 2026, and it is a holiday."
    },
    {
        "questions": [
            "When is Basava Jayanti?",
            "Is Basava Jayanti a holiday?"
        ],
        "answer": "Basava Jayanti is on 20th April 2026, and it is a holiday."
    },
    {
        "questions": [
            "When is May Day?",
            "Is May Day a holiday?"
        ],
        "answer": "May Day (International Labour Day) is on 1st May 2026, and it is a holiday."
    },
    {
        "questions": [
            "When is Bakrid?",
            "Is Bakrid a holiday this semester?"
        ],
        "answer": "Bakrid (Eid-ul-Adha) is on 28th May 2026, and it is a holiday."
    },
    {
        "questions": [
            "What are all the holidays this semester?",
            "List all holidays in even semester 2025-26.",
            "Which days are off this semester?"
        ],
        "answer": "The holidays in Even Semester 2025-26 are: Chandramana Ugadi (19th March), Compensatory Holiday (20th March), Ramzan (21st March), Mahavir Jayanti (31st March), Good Friday (3rd April), Ambedkar Jayanti (14th April), Basava Jayanti (20th April), May Day (1st May), Bakrid (28th May)."
    },
    {
        "questions": [
            "When is the Working with Friday Time Table?",
            "When does the college follow Friday timetable?"
        ],
        "answer": "The college follows the Friday Time Table on 14th March 2026 (Week 4)."
    },
    {
        "questions": [
            "When is the Working with Saturday Time Table?",
            "When is the Saturday timetable applied?"
        ],
        "answer": "The college follows the Saturday Time Table on 15th March 2026 (Week 4)."
    },

    # ---------------- 9. ESA (End Semester Assessment) Dates ----------------
    {
        "questions": [
            "When are the practical exams?",
            "When is ESA practical exam?",
            "What are the ESA practical dates?",
            "When do practical exams start?"
        ],
        "answer": "The ESA (End Semester Assessment) Practical Exams are scheduled from 12th June to 16th June 2026, for all programs — B.E., B.Arch, BBA, BCA, B.Com, and B.Sc. FAD."
    },
    {
        "questions": [
            "When are the theory exams?",
            "When is ESA theory exam?",
            "What are the ESA theory exam dates?",
            "When do theory exams start?"
        ],
        "answer": "The ESA (End Semester Assessment) Theory Exams begin from 19th June 2026 onwards, for all programs — B.E., B.Arch, BBA, BCA, B.Com, and B.Sc. FAD."
    },
    {
        "questions": [
            "What are the end semester exam dates?",
            "Tell me about ESA schedule.",
            "When are the final exams this semester?"
        ],
        "answer": "The End Semester Assessment (ESA) dates for Even Semester 2025-26 are: Practical Exams from 12th June to 16th June 2026, and Theory Exams starting from 19th June 2026. These dates apply uniformly across all programs including B.E., B.Arch, BBA, BCA, B.Com, and B.Sc. FAD."
    },
    {
        "questions": [
            "When is the end semester assessment for B.E.?",
            "What are ESA dates for engineering students?"
        ],
        "answer": "For B.E. students (2nd, 4th, and 6th Semester), the ESA Practical Exams are from 12th June to 16th June 2026, and Theory Exams start from 19th June 2026."
    },
    {
        "questions": [
            "When is the end semester assessment for B.Arch?",
            "ESA dates for architecture students?"
        ],
        "answer": "For B.Arch students (2nd, 4th, 6th, and 8th Semester), the ESA Practical Exams are from 12th June to 16th June 2026, and Theory Exams start from 19th June 2026."
    },
    {
        "questions": [
            "When is the end semester assessment for BBA, BCA, and B.Com?",
            "ESA dates for management students?"
        ],
        "answer": "For 4th Semester BBA, BCA, and B.Com students, the ESA Practical Exams are from 12th June to 16th June 2026, and Theory Exams start from 19th June 2026."
    },

    # ---------------- 10. 4th Semester Weekly Timetable (Full Grid) ----------------
    {
        "questions": ["Monday timetable for 4th Sem Div A", "IV A Monday schedule"],
        "answer": "Monday (IV A): CS-SAR (8-10, SEE104), LA-NSS (10:15-11:15, SEE104), IT-PC (11:15-12:15, SEE104), S&S-ART (1:30-2:30, SEE208)."
    },
    {
        "questions": ["Monday timetable for 4th Sem Div B", "IV B Monday schedule"],
        "answer": "Monday (IV B): LA-BMS (9-10, SEE114), S&S-RMB+SMG (10:15-12:15, SEE114), LIC-SBH+LRD+KSS (1:30-3:30, SEE108), ARM LAB (3:30-5:30, SEE109)."
    },
    {
        "questions": ["Monday timetable for 4th Sem Div C", "IV C Monday schedule"],
        "answer": "Monday (IV C): S&S-PSP+ART (8-10, SEE112), CS-RVH (10:15-11:15, SEE204), LA-BMS+SAH+SMG (1:30-3:30, SEE112)."
    },
    {
        "questions": ["Monday timetable for 4th Sem Div D", "IV D Monday schedule"],
        "answer": "Monday (IV D): CS-SA (8-10, SEE209), S&S-NSR (10:15-11:15, SEE209), ARM-NS (1:30-2:30, SEE104), LIC-JP+KSS+RVB (3:30-5:30, SEE108)."
    },
    {
        "questions": ["Monday timetable for 4th Sem Div E", "IV E Monday schedule"],
        "answer": "Monday (IV E): CS-SA (10:15-11:15, SEE110), DSA-HS+SBN (1:30-3:30, SEE114), CS LAB E2-SA+CSS (3:30-5:30, SEE206)."
    },
    {
        "questions": ["Monday timetable for 4th Sem Div F", "IV F Monday schedule"],
        "answer": "Monday (IV F): DSA-HS+SMK (8-10, SEE110), LIC-JP+CJ+LRD (10:15-12:15, SEE108), ARM-PSP (1:30-2:30, SEE109)."
    },
    {
        "questions": ["Tuesday timetable for 4th Sem Div A", "IV A Tuesday schedule"],
        "answer": "Tuesday (IV A): PSC LAB-RMB+SMG (10:15-12:15, SEE110), LA-NSS (1:30-2:30, SEE112), IT-PC (2:30-3:30, SEE112)."
    },
    {
        "questions": ["Tuesday timetable for 4th Sem Div B", "IV B Tuesday schedule"],
        "answer": "Tuesday (IV B): S&S-RMB (9-10, SEE104), ARM-SVK (10:15-12:15, SEE104), LA-BMS+SAH+SMG (1:30-3:30, SEE104), CS LAB B2-SAR+VKK (3:30-5:30, SEE206)."
    },
    {
        "questions": ["Tuesday timetable for 4th Sem Div C", "IV C Tuesday schedule"],
        "answer": "Tuesday (IV C): ARM-BRK (9-10, SEE109), LA-BMS (10:15-11:15, SEE114), S&S-PSP (11:15-12:15, SEE114), LIC-SBH+RVB+CJ (1:30-3:30, SEE108)."
    },
    {
        "questions": ["Tuesday timetable for 4th Sem Div D", "IV D Tuesday schedule"],
        "answer": "Tuesday (IV D): LA-PC (9-10, SEE112), LIC-JP+KSS+RVB (10:15-12:15, SEE108), DSA-SBN+HS (1:30-3:30, SEE110)."
    },
    {
        "questions": ["Tuesday timetable for 4th Sem Div E", "IV E Tuesday schedule"],
        "answer": "Tuesday (IV E): LIC-MC+SHH+GK (8-10, SEE108), DSA-HS+SBN (10:15-12:15, SEE111), CS LAB E1-SA+VKK (1:30-3:30, SEE206)."
    },
    {
        "questions": ["Tuesday timetable for 4th Sem Div F", "IV F Tuesday schedule"],
        "answer": "Tuesday (IV F): LA-AB (9-10, SEE114), CS-RVH (10:15-11:15, SEE204), S&S-NSR+PSP (1:30-3:30, SEE114), LIC-JP+CJ+LRD (3:30-5:30, SEE108)."
    },
    {
        "questions": ["Wednesday timetable for 4th Sem Div A", "IV A Wednesday schedule"],
        "answer": "Wednesday (IV A): CS-SAR (8-10, SEE114), ARM LAB-VKK+RA+NS (10:15-12:15, SEE109), S&S-ART (1:30-2:30, SEE109), ARM-VKK (2:30-3:30, SEE109)."
    },
    {
        "questions": ["Wednesday timetable for 4th Sem Div B", "IV B Wednesday schedule"],
        "answer": "Wednesday (IV B): LIC-SBH+LRD+KSS (10:15-12:15, SEE108), S&S-RMB (1:30-2:30, SEE104)."
    },
    {
        "questions": ["Wednesday timetable for 4th Sem Div C", "IV C Wednesday schedule"],
        "answer": "Wednesday (IV C): ARM-BRK (10:15-11:15, SEE112), LA-BMS (11:15-12:15, SEE112), S&S-PSP (1:30-2:30, SEE112), LIC-SBH+RVB+CJ (3:30-5:30, SEE108)."
    },
    {
        "questions": ["Wednesday timetable for 4th Sem Div D", "IV D Wednesday schedule"],
        "answer": "Wednesday (IV D): CS LAB D1-SA+CSS (8-10, SEE206), LA-PC+SAH+SMG (10:15-12:15, SEE114), ARM-NS (1:30-2:30, SEE208), CS LAB D2-SA+CSS (3:30-5:30, SEE206)."
    },
    {
        "questions": ["Wednesday timetable for 4th Sem Div E", "IV E Wednesday schedule"],
        "answer": "Wednesday (IV E): LA-PC (9-10, SEE112), CS-SA (10:15-11:15, SEE104), LIC-MC+SHH+GK (1:30-3:30, SEE108)."
    },
    {
        "questions": ["Wednesday timetable for 4th Sem Div F", "IV F Wednesday schedule"],
        "answer": "Wednesday (IV F): DSA-HS+SMK (8-10, SEE110), CS LAB F1-SAR+CSS (10:15-12:15, SEE206), LA-AB+SAH+SMG (1:30-3:30, SEE114)."
    },
    {
        "questions": ["Thursday timetable for 4th Sem Div A", "IV A Thursday schedule"],
        "answer": "Thursday (IV A): LIC-MC+RVB (8-10, SEE108), PSC LAB-RMB+SMG (10:15-12:15, SEE110), ARM-VKK (1:30-2:30, SEE112), LA-NSS+SAH+SMG (2:30-4:30, SEE112)."
    },
    {
        "questions": ["Thursday timetable for 4th Sem Div B", "IV B Thursday schedule"],
        "answer": "Thursday (IV B): CS-SAR (8-10, SEE114), DSA-SBN+HS (10:15-12:15, SEE114), LA-BMS (1:30-3:30, SEE114)."
    },
    {
        "questions": ["Thursday timetable for 4th Sem Div C", "IV C Thursday schedule"],
        "answer": "Thursday (IV C): CS-RVH (8-10, SEE204), LIC-SBH+RVB+CJ (10:15-12:15, SEE108), ARM LAB-BRK+RA+NS (1:30-3:30, SEE109), CS LAB C2-SA+VKK (3:30-5:30, SEE206)."
    },
    {
        "questions": ["Thursday timetable for 4th Sem Div D", "IV D Thursday schedule"],
        "answer": "Thursday (IV D): CS-SA (10:15-11:15, SEE104), LA-PC (1:30-2:30, SEE104), S&S-NSR (2:30-4:30, SEE104)."
    },
    {
        "questions": ["Thursday timetable for 4th Sem Div E", "IV E Thursday schedule"],
        "answer": "Thursday (IV E): LA-PC (9-10, SEE104), ARM-RA (10:15-11:15, SEE109), LIC-MC+SHH+GK (1:30-3:30, SEE108), S&S-UBP (3:30-5:30, SEE104)."
    },
    {
        "questions": ["Thursday timetable for 4th Sem Div F", "IV F Thursday schedule"],
        "answer": "Thursday (IV F): S&S-NSR (8-10, SEE112), LA-AB (10:15-11:15, SEE112), ARM-PSP (11:15-12:15, SEE112), CS LAB F2-SAR+CSS (1:30-3:30, SEE206)."
    },
    {
        "questions": ["Friday timetable for 4th Sem Div A", "IV A Friday schedule"],
        "answer": "Friday (IV A): S&S-ART+PSP (8-10, SEE112), ARM-VKK (10:15-11:15, SEE112), LA-NSS (11:15-12:15, SEE112), LIC-MC+RVB (1:30-3:30, SEE108)."
    },
    {
        "questions": ["Friday timetable for 4th Sem Div B", "IV B Friday schedule"],
        "answer": "Friday (IV B): CS-SAR (8-10, SEE104), LIC-SBH+LRD+KSS (10:15-12:15, SEE108), DSA-SBN+HS (1:30-3:30, SEE110), CS LAB B1-SAR+VKK (3:30-5:30, SEE206)."
    },
    {
        "questions": ["Friday timetable for 4th Sem Div C", "IV C Friday schedule"],
        "answer": "Friday (IV C): DSA-SBN+MK (8-10, SEE110), LA-BMS (10:15-11:15, SEE104), ARM-BRK (11:15-12:15, SEE104)."
    },
    {
        "questions": ["Friday timetable for 4th Sem Div D", "IV D Friday schedule"],
        "answer": "Friday (IV D): LA-PC (9-10, SEE114), S&S-NSR+ART (10:15-12:15, SEE109), ARM LAB-NS+VKK+RA (1:30-3:30, SEE109), LIC-JP+KSS+RVB (3:30-5:30, SEE108)."
    },
    {
        "questions": ["Friday timetable for 4th Sem Div E", "IV E Friday schedule"],
        "answer": "Friday (IV E): ARM LAB-RA+NS+VKK (8-10, SEE109), S&S-UBP+PSP (10:15-12:15, SEE209), LA-PC+SAH+SMG (1:30-3:30, SEE104)."
    },
    {
        "questions": ["Friday timetable for 4th Sem Div F", "IV F Friday schedule"],
        "answer": "Friday (IV F): LIC-JP+CJ+LRD (8-10, SEE108), CS-RVH (10:15-11:15, SEE204), LA-AB (1:30-2:30, SEE112), S&S-NSR (2:30-3:30, SEE112)."
    },

    # ---------------- 11. 6th Semester Weekly Timetable (Full Grid) ----------------
    {
        "questions": ["Monday timetable for 6th Sem Div A", "VI A Monday schedule"],
        "answer": "Monday (VI A): PALR (8-10, SEE303), Elective (10:15-12:15), Minor Project (1:30-4:30)."
    },
    {
        "questions": ["Monday timetable for 6th Sem Div B", "VI B Monday schedule"],
        "answer": "Monday (VI B): EIS (8-10, CLH304), Elective (10:15-12:15), CCN-SKG (1:30-2:30, SEE302), Minor Project (2:30-5:30)."
    },
    {
        "questions": ["Monday timetable for 6th Sem Div C", "VI C Monday schedule"],
        "answer": "Monday (VI C): EIS (8-10, CLH304), Elective (10:15-12:15), PALR (1:30-2:30, SEE303), CCN LAB C2 (2:30-5:30, SEE111)."
    },
    {
        "questions": ["Monday timetable for 6th Sem Div D", "VI D Monday schedule"],
        "answer": "Monday (VI D): EIS (8-10, CLH304), Elective (10:15-12:15), Minor Project (1:30-5:30)."
    },
    {
        "questions": ["Monday timetable for 6th Sem Div E", "VI E Monday schedule"],
        "answer": "Monday (VI E): EIS (8-10, CLH304), Elective (10:15-12:15), AE LAB E1 (1:30-3:30, SEE305), CCN LAB E2 (3:30-5:30, SEE111)."
    },
    {
        "questions": ["Monday timetable for 6th Sem Div F", "VI F Monday schedule"],
        "answer": "Monday (VI F): EIS (8-10, CLH304), Elective (10:15-12:15), GEN AI-SP+SSC (1:30-2:30, SEE209)."
    },
    {
        "questions": ["Tuesday timetable for 6th Sem Div A", "VI A Tuesday schedule"],
        "answer": "Tuesday (VI A): CCN LAB-SKG+MA (8-10, SEE111), Electives (10:15-1:30), Minor Project (1:30-3:30)."
    },
    {
        "questions": ["Tuesday timetable for 6th Sem Div B", "VI B Tuesday schedule"],
        "answer": "Tuesday (VI B): Minor Project (8-10), Electives (10:15-1:30), GEN AI-RT+ART (1:30-3:30, SEE209)."
    },
    {
        "questions": ["Tuesday timetable for 6th Sem Div C", "VI C Tuesday schedule"],
        "answer": "Tuesday (VI C): Minor Project (8-10), Electives (10:15-1:30), CCN-MA (1:30-3:30, SEE302)."
    },
    {
        "questions": ["Tuesday timetable for 6th Sem Div D", "VI D Tuesday schedule"],
        "answer": "Tuesday (VI D): CCN-SHS (8-10, SEE302), Electives (10:15-1:30), AE LAB D1 & CCN LAB D2 (1:30-3:30)."
    },
    {
        "questions": ["Tuesday timetable for 6th Sem Div E", "VI E Tuesday schedule"],
        "answer": "Tuesday (VI E): Minor Project (8-10), Electives (10:15-1:30), PALR (1:30-3:30, SEE303)."
    },
    {
        "questions": ["Tuesday timetable for 6th Sem Div F", "VI F Tuesday schedule"],
        "answer": "Tuesday (VI F): AE LAB F1-CJ+SM (8-10, SEE305), Electives (10:15-1:30), GEN AI-SP+SSC (1:30-3:30, SEE109), PALR (3:30-5:30, SEE303)."
    },
    {
        "questions": ["Wednesday timetable for 6th Sem Div A", "VI A Wednesday schedule"],
        "answer": "Wednesday (VI A): AE LAB-KSS+SM (8-10, SEE305), CCN-SKG (10:15-12:15, SEE303), Minor Project (1:30-3:30)."
    },
    {
        "questions": ["Wednesday timetable for 6th Sem Div B", "VI B Wednesday schedule"],
        "answer": "Wednesday (VI B): GEN AI-RT+ART (8-10, SEE302), AE-RSJ (10:15-12:15, SEE302), PALR (1:30-2:30, SEE303)."
    },
    {
        "questions": ["Wednesday timetable for 6th Sem Div C", "VI C Wednesday schedule"],
        "answer": "Wednesday (VI C): AE LAB C2 & CCN LAB C1 (10:15-12:15), GEN AI-SSC+SVK (1:30-3:30, SEE209)."
    },
    {
        "questions": ["Wednesday timetable for 6th Sem Div D", "VI D Wednesday schedule", "what is d divison 6th sem timetable on wednesday"],
        "answer": "Wednesday (VI D): GEN AI-SSC+SVK (8-10, SEE209), CCN-SHS (10:15-12:15, SEE204), AE-BP (1:30-2:30, SEE110)."
    },
    {
        "questions": ["Wednesday timetable for 6th Sem Div E", "VI E Wednesday schedule"],
        "answer": "Wednesday (VI E): CCN-GK (8-10, SEE204), GEN AI-ART+RT (10:15-12:15, SEE110), AE-PCN (1:30-2:30, SEE302)."
    },
    {
        "questions": ["Wednesday timetable for 6th Sem Div F", "VI F Wednesday schedule"],
        "answer": "Wednesday (VI F): CCN LAB F2-CA+SHS (8-10, SEE111), AE-CJ (10:15-12:15, SEE208), AE LAB F2 & CCN LAB F1 (1:30-3:30)."
    },
    {
        "questions": ["Thursday timetable for 6th Sem Div A", "VI A Thursday schedule"],
        "answer": "Thursday (VI A): AE-KSS (8-10, SEE209), GEN AI-RT+SP (10:15-12:15, SEE209), PALR (1:30-3:30, SEE302)."
    },
    {
        "questions": ["Thursday timetable for 6th Sem Div B", "VI B Thursday schedule"],
        "answer": "Thursday (VI B): CCN-SKG (10:15-12:15, SEE302), AE LAB B2 & CCN LAB B1 (1:30-3:30)."
    },
    {
        "questions": ["Thursday timetable for 6th Sem Div C", "VI C Thursday schedule"],
        "answer": "Thursday (VI C): AE LAB C1-GHM+KMR (8-10, SEE305), CCN-MA (10:15-12:15, SEE303), GEN AI-SSC+SVK (1:30-3:30, SEE209)."
    },
    {
        "questions": ["Thursday timetable for 6th Sem Div D", "VI D Thursday schedule"],
        "answer": "Thursday (VI D): PALR (8-10, SEE303), GEN AI-SSC+SVK (10:15-12:15, SEE208)."
    },
    {
        "questions": ["Thursday timetable for 6th Sem Div E", "VI E Thursday schedule"],
        "answer": "Thursday (VI E): CCN-GK (8-10, SEE302), AE LAB E2 & CCN LAB E1 (10:15-12:15), AE-PCN (1:30-3:30, SEE303)."
    },
    {
        "questions": ["Thursday timetable for 6th Sem Div F", "VI F Thursday schedule"],
        "answer": "Thursday (VI F): AE-CJ (9-10, SEE109), CCN-CA (10:15-11:15, SEE204), Minor Project (1:30-4:30)."
    },
    {
        "questions": ["Friday timetable for 6th Sem Div A", "VI A Friday schedule"],
        "answer": "Friday (VI A): GEN AI-RT+SP (8-10, SEE209), CCN-SKG (10:15-11:15, SEE114), AE-KSS (1:30-2:30, SEE302)."
    },
    {
        "questions": ["Friday timetable for 6th Sem Div B", "VI B Friday schedule"],
        "answer": "Friday (VI B): CCN-SKG (9-10, SEE302), AE-RSJ (10:15-12:15, SEE110), AE LAB B1 & CCN LAB B2 (1:30-4:30)."
    },
    {
        "questions": ["Friday timetable for 6th Sem Div C", "VI C Friday schedule"],
        "answer": "Friday (VI C): PALR (8-10, SEE303), AE-GHM (10:15-11:15, SEE210), Minor Project (1:30-3:30)."
    },
    {
        "questions": ["Friday timetable for 6th Sem Div D", "VI D Friday schedule"],
        "answer": "Friday (VI D): AE-BP (9-10, SEE204), AE LAB D2 & CCN LAB D1 (10:15-12:15), PALR (1:30-3:30, SEE303)."
    },
    {
        "questions": ["Friday timetable for 6th Sem Div E", "VI E Friday schedule"],
        "answer": "Friday (VI E): Minor Project (8-10), PALR (10:15-11:15, SEE303), GEN AI-ART+RT (1:30-3:30, SEE204)."
    },
    {
        "questions": ["Friday timetable for 6th Sem Div F", "VI F Friday schedule"],
        "answer": "Friday (VI F): Minor Project (8-10), PALR (10:15-11:15, SEE302), CCN-CA (1:30-2:30, SEE114)."
    },
    {
        "questions": ["When is the ADIC elective class?"],
        "answer": "ADIC-RM: Monday and Tuesday (10:15-12:15) in Classroom SEE207 (Mon) and SEE305 (Tue)."
    },
    {
        "questions": ["When is the AL elective class?"],
        "answer": "AL elective: Div A,B,C on Monday/Wednesday (SEE302/207); Div D,E,F on Monday/Tuesday/Thursday (SEE302/207)."
    }
]

# Write to JSONL
output_file = 'kle_tech_dataset.jsonl'
with open(output_file, 'w', encoding='utf-8') as f:
    count = 0
    for block in data_pairs:
        answer = block['answer']
        for question in block['questions']:
            entry = {
                "system": system_prompt,
                "user": question,
                "assistant": answer
            }
            f.write(json.dumps(entry) + '\n')
            count += 1

print(f"Dataset generation complete! Created {count} distinct Q&A pairs in '{output_file}'.")
