# KLE Tech University Chatbot (Custom Seq2Seq Transformer)

A robust, custom-built Seq2Seq Transformer chatbot designed for **KLE Technological University**. This bot is built entirely from scratch using PyTorch — no pre-trained LLMs, no external APIs. It ensures high precision and factual accuracy for university-specific queries.

---

## 🏗️ System Architecture

This project uses a **Hybrid Retrieval-Augmented Generation (RAG)** approach. Instead of relying on a multi-billion parameter model, it combines a high-precision **TF-IDF Retrieval Matcher** with a custom-trained **Seq2Seq Transformer** to ensure zero hallucinations.

### High-Level System Workflow

```
┌─────────────────────────────────────────────────────────────────────┐
│                        TRAINING PIPELINE                            │
│                                                                     │
│  University Knowledge ──► generate_dataset.py ──► dataset.jsonl     │
│        (Calendar, Timetable,       │                                │
│         Placements, etc.)          ▼                                │
│                            vocab_builder.py ──► Custom Vocabulary   │
│                                    │                                │
│                                    ▼                                │
│                               train.py ──► kle_tech_bot.pth         │
│                          (Teacher Forcing,       (Trained Weights)  │
│                           CUDA/GPU Accel.)                          │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                        INFERENCE PIPELINE                           │
│                                                                     │
│  User Query ──► TF-IDF Bi-gram Matcher ──► Best Matching Question   │
│                  (Cosine Similarity)              │                 │
│                                                   ▼                 │
│                                        Seq2Seq Transformer          │
│                                        (Encoder → Decoder)          │
│                                                   │                 │
│                                                   ▼                 │
│                                        Response Formatter           │
│                                        (Capitalization, Punctuation)│
│                                                   │                 │
│                                                   ▼                 │
│                                           Final Answer              │
└─────────────────────────────────────────────────────────────────────┘
```

### Custom Transformer Architecture (Encoder-Decoder)

```
┌──────────────────────────────────────────────────────────────────┐
│                    Seq2Seq Transformer Model                     │
│                                                                  │
│  ┌─────────────────────┐          ┌─────────────────────────┐    │
│  │      ENCODER         │         │        DECODER          │    │
│  │                      │         │                         │    │
│  │  Input Embedding     │         │  Output Embedding       │    │
│  │        │             │         │        │                │    │
│  │        ▼             │         │        ▼                │    │
│  │  Positional Encoding │         │  Positional Encoding    │    │
│  │        │             │         │        │                │    │
│  │        ▼             │         │        ▼                │    │
│  │  Multi-Head          │         │  Masked Multi-Head      │    │
│  │  Self-Attention      │         │  Self-Attention         │    │
│  │        │             │         │        │                │    │
│  │        ▼             │         │        ▼                │    │
│  │  Feed Forward        │────────►│  Cross-Attention        │    │
│  │  Network             │ Context │  (Encoder-Decoder Attn) │    │
│  │                      │         │        │                │    │
│  └─────────────────────┘          │        ▼                │    │
│                                   │  Feed Forward Network   │    │
│                                   │        │                │    │
│                                   └────────┼────────────────┘    │
│                                            ▼                     │
│                                   Linear → Softmax → Output      │
└──────────────────────────────────────────────────────────────────┘
```

### Data Augmentation Pipeline

```
  Original Q&A Pair
        │
        ▼
  Synonym Replacement ──► "when is" → "at what time is"
        │                  "tell me" → "explain"
        ▼                  "what are" → "list the"
  Augmented Dataset
  (3x more training pairs)
```

---

## 🛠️ Technical Implementation Details

| Component              | Technology                          | Purpose                                                   |
|------------------------|-------------------------------------|-----------------------------------------------------------|
| **Tokenization**       | Custom Word-Level Vocab             | Splits text into words with `<SOS>`, `<EOS>`, `<PAD>`, `<UNK>` tokens |
| **Data Augmentation**  | Synonym-based expansion             | Generates 3x training pairs to improve robustness         |
| **Matching Engine**    | TF-IDF with Bi-grams (1,2)         | Prevents "6th sem" vs "4th sem" confusion                 |
| **Model**              | PyTorch `nn.Transformer`            | Custom Encoder-Decoder with Positional Encoding           |
| **Training**           | Teacher Forcing + CUDA              | GPU-accelerated for fast convergence                      |
| **Response Formatting**| Regex-based post-processor          | Proper capitalization, punctuation, and number formatting  |

---

## 🚀 Key Features

- **Custom Transformer Architecture:** Full Encoder-Decoder Transformer with Multi-Head Attention and Positional Encoding — no pre-trained models used.
- **Hybrid RAG Matching:** TF-IDF Vectorizer with Bi-gram matching retrieves the best context before generation, preventing hallucinations.
- **University Intelligence:** Pre-loaded with comprehensive data including:
  - Placement records (highest packages, top recruiters).
  - Full Academic Calendar (Even Semester 2025-26).
  - Weekly Master Timetables for 4th & 6th Sem (Divisions A-F).
  - Elective-specific schedules (ADIC, MCAP, OOPS, AICD, AL).
  - ESA (End Semester Assessment) Practical & Theory dates.
- **100% Offline:** No external APIs, no internet required. Works entirely on your local hardware.

---

## 🛠️ Technology Stack

| Layer           | Tool                                |
|-----------------|-------------------------------------|
| Language        | Python 3.x                          |
| Deep Learning   | PyTorch                             |
| NLP Matching    | Scikit-Learn (TfidfVectorizer)      |
| Hardware        | NVIDIA GPU (CUDA)                   |
| Tokenization    | Custom word-level vocabulary        |

---

## 📖 How to Use

### 1. Generate Dataset
Compiles the university knowledge into a structured JSONL format.
```bash
python generate_dataset.py
```

### 2. Train the Model
Trains the custom Transformer on the generated dataset (uses GPU if available).
```bash
python train.py
```

### 3. Chat with the Bot (Default Mode)
Launches the interactive CLI using your custom-trained 0.6M parameter Transformer.
```bash
python chat.py
```

### 4. Chat with the Bot (Hybrid LLM Mode) 🌟
Launches the CLI using **Qwen2.5-1.5B-Instruct**. This mode uses your local 4GB GPU to run a massive 1.5 Billion parameter model in 4-bit mode. It uses the university dataset as context to provide much smarter and more natural answers.
```bash
python chat_qwen.py
```

---

## 🏗️ Hybrid LLM Architecture (Advanced)

When running in **Qwen Mode**, the system follows a modern **Retrieval-Augmented Generation (RAG)** pipeline:

```
┌─────────────────────────────────────────────────────────┐
│              HYBRID RAG INFERENCE PIPELINE              │
│                                                         │
│  User Query ──► TF-IDF Matcher ──► Best Fact Retrieval  │
│                                           │             │
│                                           ▼             │
│  System Prompt ◄── [University Data] + [User Question]  │
│                                           │             │
│                                           ▼             │
│                                  Qwen2.5-1.5B (4-bit)   │
│                                    (Local Inference)    │
│                                           │             │
│                                           ▼             │
│                                    Natural Response     │
└─────────────────────────────────────────────────────────┘
```

---

## 📊 Sample Queries

| Query                                              | Category          |
|----------------------------------------------------|-------------------|
| *"When are the practical exam dates?"*             | ESA Calendar      |
| *"What is the Monday schedule for IV A?"*          | 4th Sem Timetable |
| *"I have picked the OOPS elective. When is my class?"* | 6th Sem Electives |
| *"Who hired 249 students in 2023?"*                | Placements        |
| *"When is Pleiades fest?"*                         | Events            |
| *"List all holidays this semester"*                | Holidays          |

---

## 📁 Project Structure

| File                    | Description                                              |
|-------------------------|----------------------------------------------------------|
| `transformer_model.py`  | Custom PyTorch Seq2Seq Transformer architecture          |
| `vocab_builder.py`      | Word-level tokenization with synonym augmentation        |
| `train.py`              | GPU-accelerated training pipeline with Teacher Forcing   |
| `chat.py`               | Interactive CLI with TF-IDF context retrieval            |
| `generate_dataset.py`   | Source of all university knowledge (Calendar, Timetables)|
| `kle_tech_bot.pth`      | Trained model weights (~6 MB)                            |

---

## 📈 Training Summary

- **Dataset Size:** 292 distinct Q&A pairs (804 with augmentations)
- **Vocabulary Size:** 764 unique words
- **Training Epochs:** 200
- **Best Loss:** 0.0042
- **Hardware:** NVIDIA CUDA GPU
