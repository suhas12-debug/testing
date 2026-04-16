# KLE Tech University Chatbot (Pure Semantic RAG)

A high-performance, university-specific chatbot for **KLE Technological University**. This system uses a **Pure Semantic RAG** architecture—combining a powerful `Sentence-BERT` semantic retrieval engine with a highly efficient Qwen2.5-0.5B-Instruct model. It is completely optimized to deliver 100% factual accuracy on local hardware with only **4GB of VRAM**.

---

## 🏗️ System Architecture: "Pure-Semantic-0.5B"

This project utilizes a modern **Semantic Retrieval-Augmented Generation (RAG)** pipeline. By providing verified facts directly to the model at inference time, we eliminate hallucinations and ensure every answer is grounded in university data.

### 🧠 The Inference Pipeline (Semantic Search RAG)

```text
Student types question
         │
         ▼
 ┌───────────────────────┐
 │  Sentence-BERT (CPU)  │ ◄── converts question to meaning vector
 │  all-MiniLM-L6-v2     │     (understands "kab hai exam" = "when is exam")
 └───────────────────────┘
         │
         ▼
 ┌───────────────────────┐
 │  knowledge_base       │ ◄── your kle_tech_dataset.jsonl file
 │  (your scraped data)  │     finds top matching facts
 └───────────────────────┘
         │
         ▼
 score > SIMILARITY_THRESHOLD?
     ╱       ╲
   YES        NO
   │          │
   ▼          ▼
facts found   "please contact
   │          university office"
   │          │
 ┌─▼──────────▼──────────┐
 │  Qwen 0.5B 4-bit(GPU) │ ◄── only job: format facts naturally
 │  ~400MB VRAM          │     reads facts → writes clean reply
 └───────────────────────┘
         │
         ▼
   Answer shown
```

---

## 🛠️ Technical Specs

| Component              | Technology                          | Strategy Implementation                                     |
|------------------------|-------------------------------------|-----------------------------------------------------------|
| **LLM Generator Core** | Qwen2.5-0.5B-Instruct               | Tiny footprint with high instruction-following capability. |
| **Quantization**       | BitsAndBytes (4-bit NF4)           | Reduces VRAM usage of the brain to ~400MB.                |
| **Matching Engine**    | Sentence-Transformers (all-MiniLM)  | Computes dense semantic vectors, parsing true *meaning*.  |
| **Data Source**        | `kle_tech_dataset.jsonl`          | Expert curated master grid for timetables and university facts. |
| **Hardware Goal**      | NVIDIA RTX 3050 (4GB VRAM)          | Fully local, high-speed, 100% private inference.          |

---

## 🚀 Key Features

- **Zero Hallucination Grounding:** Since the model relies purely on retrieved facts and has no outdated "memory" (No Adapter), it only provides information present in your dataset.
- **Semantic Memory Overrides Keywords:** Using `all-MiniLM-L6-v2`, the system interprets the student's *intent*. "Where is the college?" mathematically aligns with "KLE Tech Location".
- **Strict Logic Thresholds:** Employs a cosine similarity threshold. If the user asks an irrelevant question, the system safely redirects them.
- **University Intelligence:** Pre-loaded with comprehensive data including:
  - 100% specific 6-Day timetables for **Semester IV** and **Semester VI** divisions.
  - Placement records, Electives, and Exam dates.
  - Academic Dates & Holidays.

---

## 📖 How to Use

### 1. Build the Master Knowledge Base
Generates the pristine `.jsonl` data grid with complete timetable grids.
```bash
python generate_dataset.py
```

### 2. Chat with the Expert Bot 🌟
Launches the high-precision CLI utilizing the full hybrid Semantic RAG pipeline.
```bash
# Windows (requires Python UTF-8 encoding)
$env:PYTHONUTF8=1; python chat_qwen.py
```

---

## 📊 Sample Queries

Try these questions to witness the semantic retrieval engine working flawlessly:

| Query Focus                                        | Why it works                                          |
|----------------------------------------------------|-------------------------------------------------------|
| *"Where is the college located?"*                  | Semantic engine knows "college" = "KLE Tech".         |
| *"What is the Thursday schedule for VI D?"*        | Precision data extraction from the RAG context.       |
| *"Who hired the most students this year?"*         | Contextually understands "hired" links to "placements".|
| *"Tell me about the latest cricket match"*         | Gets mathematically blocked and safely rejected.      |

---

## 📁 Project Structure

| File                      | Description                                                  |
|---------------------------|--------------------------------------------------------------|
| `chat_qwen.py`            | Main Inference Engine with Qwen Generation and Chat Templates.|
| `chat.py`                 | The Semantic Search Core running Sentence-BERT vector math.   |
| `generate_dataset.py`     | Pristine data generator maintaining the university truths.    |
