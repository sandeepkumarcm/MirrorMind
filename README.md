# 🎯 MirrorMind — AI-Powered Interview Coach with RAG-Grounded Feedback

[![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit)](https://streamlit.io)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker)](https://www.docker.com)
[![RAG](https://img.shields.io/badge/RAG-FAISS%20%2B%20Sentence--BERT-6C63FF?style=for-the-badge)](https://github.com/facebookresearch/faiss)

> **Watches you through the webcam, listens to your answer, and gives you real, grounded interview feedback — like a real interviewer would.**
>
> 🐳 Fully containerized and verified working end-to-end via Docker. Cloud deployment in progress — see [How to Run](#-quick-start) below to try it locally in the meantime.

---

## 🎬 Demo Video


▶️ **[Watch Full Demo on YouTube](https://youtu.be/LGOjw2AxfDY)**

---

## 🎯 The Problem

Most interview prep tools only check *what* you say — a keyword match against a model answer, nothing more. They miss how you actually come across: whether you're making eye contact, how fast you're talking, whether you're rambling or hesitating. **MirrorMind goes further** — it analyzes your face, your voice, and your words together, then grounds its feedback in a real knowledge base instead of generic AI platitudes.

---




---

# 🏗️ System Architecture

```text
                              MirrorMind Architecture

                                   👤 User
                                      │
                                      ▼
                         🖥️ Streamlit Frontend (UI)
                                      │
                                      ▼
                           ⚡ FastAPI Backend API
                                      │
                  ┌───────────────────┴───────────────────┐
                  │                                       │
                  ▼                                       ▼
        🎥 Video Processing                      🎙️ Audio Processing
     OpenCV + MediaPipe Face Mesh           Whisper Speech-to-Text
                  │                                       │
                  │                                       ▼
                  │                           Transcript + Word Timestamps
        ┌─────────┼─────────┐                          │
        │         │         │                          │
        ▼         ▼         ▼                          │
 Emotion      Eye Contact   Head Pose                 │
 DeepFace     Iris Tracking solvePnP                  │
        │         │         │                          │
        └─────────┴─────────┘                          │
                  │                                   │
                  ▼                                   ▼
        📈 Communication Analysis        📝 Transcript Analysis
     • WPM                              • Sentence-BERT
     • Pause Detection                  • Cosine Similarity
     • Filler Detection                 • Keyword Coverage
     • Answer Timer                     • Technical Score
                  │                                   │
                  └───────────────────┬───────────────┘
                                      ▼
                         🔎 RAG Retrieval Pipeline
               Sentence-BERT Embeddings + FAISS Index
                Retrieve Top-3 Relevant Knowledge Chunks
                                      │
                                      ▼
                      🤖 Llama 3 (Groq API)
            Grounded Feedback • STAR Evaluation
             Follow-up Questions • JSON Output
                                      │
                    ┌─────────────────┴──────────────────┐
                    ▼                                    ▼
         📊 Streamlit Dashboard                📄 PDF Report
     • Communication Metrics               • Transcript
     • Technical Evaluation                • Scores
     • Final AI Feedback                   • STAR Evaluation
     • Emotion Timeline                    • AI Feedback
```

## 📖 Architecture Overview

MirrorMind follows a modular AI pipeline where the Streamlit frontend communicates with a FastAPI backend. The backend processes webcam video and microphone audio independently before combining their outputs for interview evaluation.

- **Video Processing:** OpenCV captures webcam frames, MediaPipe Face Mesh extracts facial landmarks once per frame, and those landmarks are reused for emotion detection (DeepFace), eye-contact estimation, and head-pose tracking.

- **Audio Processing:** Whisper converts speech into text with word-level timestamps. The transcript is analyzed for speaking pace (WPM), pauses, filler words, and answer duration.

- **Technical Evaluation:** Sentence-BERT computes semantic similarity between the candidate's answer and the ideal answer, while keyword coverage contributes to the technical score.

- **RAG Pipeline:** The interview transcript is embedded using Sentence-BERT and queried against a FAISS vector index built from the 50-question knowledge base. The top-3 most relevant concepts are retrieved and injected into the Llama 3 prompt as grounding context.

- **LLM Feedback:** Llama 3 (via Groq API) generates structured interview feedback, STAR evaluation, strengths, weaknesses, suggestions, and follow-up questions using the retrieved context.

- **Final Output:** The frontend displays communication metrics, technical evaluation, emotion timeline, and grounded AI feedback. A complete interview report is generated as a PDF using ReportLab.

## 🏗️ System Architecture

<p align="center">
  <img src="docs/images/architecture.png" alt="MirrorMind Architecture" width="1000"/>
</p>

## 🖥️ App Screenshots

### Homepage
<img width="1872" height="842" alt="MirrorMind Homepage" src=<img width="1747" height="895" alt="Screenshot 2026-07-15 165802" src="https://github.com/user-attachments/assets/a1360d32-5cee-4703-81c0-e07f24f22a7e" />
 />

### Setup | Live Session
| Question Setup | Live Camera + Real-Time Metrics |
|---|---|
| <img alt="Setup tab" src="PASTE_YOUR_SCREENSHOT_URL_HERE" /> | <img alt="Live Session tab" src="<img width="1786" height="877" alt="Screenshot 2026-07-15 165539" src="https://github.com/user-attachments/assets/6548b1f6-9555-4d10-ba2f-4ef72c436b73" />
 /> |

| **Setup** — pick a category, pull a random question from a 50-question bank, start the session | **Live Session** — real-time webcam feed with live emotion, eye contact, and head pose tracking |

### Results — Communication | Results — Final
| Communication Metrics + Emotion Timeline | Overall Score + Grounded AI Feedback |
|---|---|
| <img alt="Communication results" src="<img width="1851" height="907" alt="Screenshot 2026-07-15 164707" src="https://github.com/user-attachments/assets/82fd25d1-d5ef-4ad8-9735-717e0fac547a" />
 /> | <img alt="Final results" src="PASTE_YOUR_SCREENSHOT_URL_HERE /> |

| **Communication** — WPM, filler words, pauses, and a full emotion timeline across the session | **Final** — radial overall score plus RAG-grounded strengths, weaknesses, and suggestions |

### Results — Technical Evaluation
<img alt="Technical results" src="<img width="1791" height="647" alt="Screenshot 2026-07-15 164742" src="https://github.com/user-attachments/assets/ddf8c67f-0db4-4eba-ad95-d11f9788223c" />
 />

*Similarity score, keyword coverage, and matched/missing keywords — computed via Sentence-BERT cosine similarity, not simple string matching.*

---

## ✨ Features

| Feature | Description |
|---|---|
| 🎥 **Real-Time Face Analysis** | MediaPipe Face Mesh (468 landmarks) + DeepFace emotion detection, smoothed over a rolling window to avoid frame-to-frame flicker |
| 👁️ **Eye Contact Tracking** | Iris landmark tracking against eye-region geometry, reported as a live percentage |
| 🧭 **Head Pose Estimation** | `solvePnP`-based yaw/pitch/roll classification (Forward/Left/Right/Up/Down) |
| 🎙️ **Speech-to-Text** | OpenAI Whisper transcribes answers with word-level timestamps |
| 📈 **Communication Scoring** | WPM, filler word detection, pause/hesitation detection, answer-length classification — all against defined ideal ranges |
| 🧠 **RAG-Grounded Feedback** | Sentence-BERT + FAISS retrieve the most relevant concepts from a 50-question knowledge base; Llama 3 generates feedback grounded in that retrieved context — not just its own parametric knowledge |
| 🔍 **Semantic Technical Scoring** | Cosine similarity between the candidate's answer and an ideal answer, blended with keyword coverage |
| ⭐ **STAR Framework Evaluation** | For behavioral questions, an LLM pass checks for Situation/Task/Action/Result and flags what's missing |
| 💬 **AI Follow-Up Questions** | Llama 3 generates a relevant follow-up question based on the candidate's actual answer |
| 📊 **Live Evaluation Dashboard** | Communication, Technical, and Final tabs with Plotly charts, a radial score gauge, and structured AI feedback |
| 📄 **PDF Interview Report** | ReportLab-generated report with transcript, metrics, STAR evaluation, and final score |

---

## ⚙️ How It Works

```
Webcam + Microphone
   │
   ▼
🎥  Video Pipeline (OpenCV → MediaPipe Face Mesh)
   │   Landmarks extracted ONCE per frame, reused for:
   │   → DeepFace emotion detection (smoothed)
   │   → Eye contact % (iris vs eye-region geometry)
   │   → Head pose (solvePnP: Forward/Left/Right/Up/Down)
   ▼
🎙️  Audio Pipeline (sounddevice → Whisper)
   │   Transcript + word-level timestamps
   │   → WPM, pause detection, filler word count, answer timer
   ▼
🧠  Technical Evaluation (Sentence-BERT)
   │   Cosine similarity vs ideal answer + keyword coverage
   │   → Technical Score
   ▼
🔎  RAG Retrieval (FAISS)
   │   Embeds the transcript, retrieves top-3 most similar
   │   concepts from across the full 50-question knowledge base
   ▼
🤖  Grounded Feedback Generation (Llama 3 via Groq)
   │   Retrieved concepts injected into the prompt as context
   │   → Strengths, Weaknesses, Suggestions, Summary (JSON mode)
   ▼
📊  Streamlit Dashboard — Communication / Technical / Final tabs
   │
   ▼
📄  PDF Report (ReportLab)
```

---

## 🧠 RAG Pipeline — How It Actually Works

This isn't a "RAG" label slapped on a normal LLM call — it's a real retrieval loop:

1. **Index build (once, at startup):** every `ideal_answer` in the 50-question bank is embedded with `all-MiniLM-L6-v2` (Sentence-BERT) and loaded into a FAISS `IndexFlatL2` vector index.
2. **Retrieval:** when a candidate finishes answering, their transcript is embedded and used to query the index for the **top-3 most semantically similar concepts across the entire question bank** — not just the question they were asked.
3. **Augmentation:** the retrieved concepts (question + reference explanation) are formatted and injected directly into the feedback-generation prompt.
4. **Generation:** Llama 3 (via Groq, in JSON mode for guaranteed valid structured output) writes feedback grounded in that retrieved context.

**Example from a real run:** a candidate answering "What is the difference between `==` and `is` in Python?" got feedback that connected their answer to **list/tuple mutability** — a completely different question in the bank — because the retrieval step correctly surfaced it as conceptually related. That's genuine retrieval-augmented grounding, not the model just improvising.

---

## 🎚️ Scoring Formulas

```
communication_score = (
    0.35 × eye_contact_component +
    0.35 × wpm_component +
    0.15 × filler_penalty_component +
    0.15 × pause_penalty_component
) × 100

overall_score = 0.5 × technical_score + 0.5 × communication_score
```

- `wpm_component` peaks at the ideal 110–150 WPM midpoint (130) and decays linearly the further actual WPM drifts from it
- `filler_penalty_component` / `pause_penalty_component` decay linearly up to a cap of 10 occurrences
- `technical_score = 0.6 × similarity_pct + 0.4 × keyword_coverage_pct`

All weights are configurable constants in `charts.py` — not hardcoded magic numbers buried in logic.

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Backend | FastAPI, Uvicorn | REST API + WebSocket-style state polling |
| Computer Vision | OpenCV, MediaPipe, DeepFace | Webcam capture, face landmarks, emotion detection |
| Speech | OpenAI Whisper | Speech-to-text with word-level timestamps |
| NLP / RAG | Sentence-BERT (`all-MiniLM-L6-v2`), FAISS | Semantic similarity scoring + retrieval-augmented generation |
| LLM | Groq API, Llama 3.3 (70B) | Feedback generation, STAR evaluation, follow-up questions |
| Frontend | Streamlit | Interactive web dashboard |
| Visualization | Plotly | Emotion timeline, communication metric charts |
| PDF | ReportLab | Structured interview report export |
| Deployment | Docker | Containerized, verified working locally |
| Config | python-dotenv, Pydantic Settings | Environment variable + settings management |

---

## 📂 Project Structure

```
MirrorMind/
│
├── backend/
│   ├── main.py                      # FastAPI entrypoint
│   ├── routes/                      # video, audio, interview, evaluation, report routes
│   ├── core/                        # config.py, state_manager.py
│   ├── schemas/                     # Pydantic request/response models
│   ├── video/                       # webcam, face detection/landmarks, emotion,
│   │                                 # eye contact, head pose, emotion smoothing
│   ├── audio/                       # recorder, Whisper transcription, WPM,
│   │                                 # pause detection, filler words, answer timer
│   ├── nlp/                         # embeddings.py, similarity_score.py, vector_store.py (FAISS)
│   ├── llm/                         # groq_client, followup_question, feedback_generator
│   │                                 # (RAG-enhanced), star_evaluator
│   ├── data/                        # questions.json — 50 questions, 10 per category
│   ├── reports/                     # pdf_generator.py (ReportLab)
│   └── utils/
│
├── frontend/
│   ├── app.py                       # Streamlit entrypoint
│   └── components/                  # dashboard.py, charts.py, styles.py
│
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── tests/
├── docs/
├── .env.example
├── .gitignore
└── requirements.txt
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10
- FFmpeg (system install, required by Whisper)
- Groq API key

### Setup (Windows)

```powershell
# Clone the repo
git clone https://github.com/YOUR_USERNAME/MirrorMind.git
cd MirrorMind

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
copy .env.example .env
# then edit .env and add your GROQ_API_KEY

# Run the backend (terminal 1)
uvicorn backend.main:app --reload

# Run the frontend (terminal 2)
cd frontend
streamlit run app.py
```

Backend runs at `http://127.0.0.1:8000` · Frontend opens at `http://localhost:8501`

### Run with Docker

```powershell
docker compose -f docker/docker-compose.yml build
docker compose -f docker/docker-compose.yml up
```

Both the FastAPI backend and Streamlit frontend start inside a single container, built and verified working from a clean image on Docker Desktop.

---

## 🔧 Engineering Highlights

- **Single landmark extraction per frame** — MediaPipe Face Mesh runs once per frame; emotion detection, eye contact, and head pose all reuse the same 478 landmarks instead of triggering three separate face detections, keeping the live loop fast
- **Emotion smoothing** — a bounded `deque(maxlen=20)` sliding window returns the mode emotion label, preventing frame-to-frame flicker without unbounded memory growth over long sessions
- **JSON-mode LLM calls** — feedback and STAR evaluation use Groq's `response_format={"type": "json_object"}` rather than parsing free-text output, eliminating a class of malformed-JSON failures caused by unescaped characters inside generated text
- **Real RAG, not a relabeled prompt** — retrieval genuinely queries a FAISS index built from the *entire* question bank, not just the current question, so feedback can surface relevant concepts the candidate never directly addressed
- **Decoupled audio pipeline** — recording runs on its own thread so a 60-second answer capture never blocks the live video polling loop
- **Snapshot-on-evaluation** — video/audio state is frozen into `st.session_state` at the moment an answer is scored, so the Results dashboard doesn't silently drift as the live webcam continues running afterward

---

## ⚠️ Current Limitations

- English only — no multilingual speech recognition or evaluation
- Question bank covers 50 questions across 5 categories (10 each); broader coverage would need a larger bank
- Whisper's `base` model occasionally mis-transcribes near-homophones (e.g., "is" → "ease") in fast speech, which can surface as an odd point in AI feedback
- Communication scoring weights are fixed defaults — not personalized per interview type (technical vs. behavioral)
- No persistent user accounts — session data resets on refresh
- Not yet deployed to a public cloud host — currently run via local Python or Docker

---

## 🔮 Future Roadmap

- Deploy to a persistent cloud host with a public live demo link
- Expand the question bank beyond 50 questions and add difficulty-adaptive selection
- Multi-turn interviews using the AI follow-up question feature end-to-end
- Persistent session history across visits (currently in-memory only)
- Swap Whisper `base` for `small`/`medium` to reduce transcription errors
- True WebRTC-based video streaming to replace the current HTTP-polling camera feed

---

## 📄 Resume Line

```
Built MirrorMind, an AI interview coach combining real-time computer vision
(MediaPipe, DeepFace), speech recognition (Whisper), and a retrieval-augmented
generation pipeline (Sentence-BERT, FAISS, Llama 3) to deliver grounded,
concept-aware interview feedback — containerized with Docker.
```

---

## 🔗 Links

| | Link |
|---|---|
| 🎬 Demo Video | [youtube.com/watch?v=YOUR_VIDEO_ID](https://www.youtube.com/watch?v=YOUR_VIDEO_ID) |
| 🐙 GitHub | [github.com/YOUR_USERNAME](https://github.com/YOUR_USERNAME) |

---

## 👤 Author

**Sandeepkumar**
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/sandeepkumarcm/)
[![GitHub](https://img.shields.io/badge/GitHub-YOUR_USERNAME-black?style=flat&logo=github)](https://github.com/sandeepkumarcm)

---
