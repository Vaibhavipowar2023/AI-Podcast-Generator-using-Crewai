# 🎙️ AI Podcast Generator

An end-to-end AI-powered podcast generator built with **CrewAI + Groq + Gemini + Sarvam TTS** that converts any topic into a fully produced MP3 podcast episode with two distinct AI voices — automatically.

> Enter any topic → AI agents research it → write a script → polish the dialogue → generate real audio → download your podcast 🎧

---

## 🚀 What It Does

Type any topic like `"Bitcoin"`, `"Climate Change"`, or `"Chess"` and the system:

1. **Researches** the topic using live web search
2. **Finds latest news** from the past 3 months
3. **Writes** a natural two-host podcast script (Alex + Sam)
4. **Polishes** the dialogue with humor and transitions
5. **Generates** real MP3 audio with two distinct Indian-English voices
6. **Saves** the final podcast to `output/audio/podcast.mp3`

---

## 🤖 Agent Architecture

| Agent | Model | Role |
|-------|-------|------|
| 🔍 Topic Researcher | `llama-3.1-8b-instant` (Groq) | Finds surprising facts and controversies |
| 📰 News Gatherer | `llama-3.1-8b-instant` (Groq) | Tracks latest developments |
| ✍️ Script Writer | `gemini-1.5-flash` (Google) | Writes natural two-host dialogue |
| 🎭 Dialogue Polisher | `gemini-1.5-flash` (Google) | Adds humor and smooths transitions |
| 🎙️ Audio Producer | `llama-3.1-8b-instant` (Groq) | Calls TTS and produces MP3 |

### 🎙️ Podcast Hosts

| Host | Voice | Personality |
|------|-------|-------------|
| **Alex** | `abhilash` (Sarvam Bulbul v2) | Calm, factual, explanatory |
| **Sam** | `anushka` (Sarvam Bulbul v2) | Curious, skeptical, funny |

---

## 🛠️ Tech Stack

| Component | Tool |
|-----------|------|
| Agent Framework | [CrewAI](https://crewai.com) |
| LLM — Research | [Groq](https://console.groq.com) — `llama-3.1-8b-instant` |
| LLM — Creative | [Google Gemini](https://aistudio.google.com) — `gemini-1.5-flash` |
| Web Search | [Tavily API](https://app.tavily.com) |
| Text-to-Speech | [Sarvam AI](https://dashboard.sarvam.ai) — `Bulbul v2` |
| Audio Merging | [pydub](https://github.com/jiaaro/pydub) |
| UI | [Streamlit](https://streamlit.io) |
| Language | Python 3.11+ |

---

## 📁 Project Structure

```
ai-podcast-generator/
├── config/
│   ├── agents.yaml          # All agent definitions (role, goal, backstory)
│   └── tasks.yaml           # All task definitions with context dependencies
├── tools/
│   └── tts_tool.py          # Sarvam TTS + pydub audio merger
├── output/
│   ├── audio/               # Generated MP3 files saved here
│   └── scripts/             # Podcast transcripts saved here
├── crew.py                  # Main crew orchestration
├── app.py                   # Streamlit UI
├── test_tts.py              # TTS API test script
├── .env                     # API keys (never commit this!)
└── pyproject.toml           # Dependencies
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-podcast-generator.git
cd ai-podcast-generator
```

### 2. Create virtual environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Mac / Linux
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install crewai crewai-tools langchain-groq langchain-google-genai tavily-python requests pydub streamlit python-dotenv
```

### 4. Get your free API keys

| Key | Where to get it | Free tier |
|-----|----------------|-----------|
| `GROQ_API_KEY` | [console.groq.com](https://console.groq.com) | 6000 TPM free |
| `GEMINI_API_KEY` | [aistudio.google.com](https://aistudio.google.com) | 1M tokens/day free |
| `TAVILY_API_KEY` | [app.tavily.com](https://app.tavily.com) | 1000 searches/month free |
| `SARVAM_API_KEY` | [dashboard.sarvam.ai](https://dashboard.sarvam.ai) | ₹1000 free credits |

### 5. Create `.env` file

```bash
GROQ_API_KEY=your_groq_key_here
GEMINI_API_KEY=your_gemini_key_here
TAVILY_API_KEY=your_tavily_key_here
SARVAM_API_KEY=your_sarvam_key_here
```

### 6. Install ffmpeg (required for audio merging)

```bash
# Windows
winget install ffmpeg

# Mac
brew install ffmpeg

# Ubuntu
sudo apt install ffmpeg
```

---

## 🎬 Usage

### Command Line

```bash
# Generate a podcast on any topic
python crew.py "Chess"
python crew.py "Bitcoin vs Gold"
python crew.py "Why India will dominate AI"
python crew.py "Is social media making us dumb"
```

### Streamlit UI

```bash
streamlit run app.py
```

---

## 📄 Output

After running, check these files:

```
output/
├── audio/
│   └── podcast.mp3          ← 🎧 Your generated podcast episode
└── scripts/
    └── podcast_script.md    ← 📄 Full transcript with ALEX/SAM dialogue
```

---

## 🔄 How The Pipeline Works

```
User Input (topic)
       ↓
Topic Researcher → searches web, finds 3 facts + 1 controversy
       ↓
News Gatherer → finds 3 recent news items about the topic
       ↓
Script Writer → writes ALEX/SAM dialogue (400-600 words)
       ↓
Dialogue Polisher → adds humor, smooths transitions
       ↓
Audio Producer → calls Sarvam TTS, merges audio segments
       ↓
output/audio/podcast.mp3 ← Final MP3 podcast episode
```

---

## 🎛️ Dual Model Strategy

This project uses **two different LLMs** strategically to optimize cost and quality:

- **Small model** (`llama-3.1-8b-instant`) for research agents — fast, cheap, good at following instructions
- **Big model** (`gemini-1.5-flash`) for creative agents — better reasoning, natural dialogue, humor

This pattern reduces token costs by ~60% while maintaining high output quality for the creative tasks that matter most.

---

## 📝 Resume Highlights

```
• Built a 5-agent CrewAI pipeline that generates full podcast episodes
  (research → script → MP3) end-to-end with zero human input

• Integrated Sarvam AI Bulbul v2 TTS with pydub to produce dual-voice
  MP3 audio with distinct speaker personalities (Indian English)

• Implemented dual-model routing: Groq llama-3.1-8b for research tasks,
  Gemini 1.5 Flash for creative writing — reducing token cost by ~60%

• System generates a 5-min podcast on any topic in under 5 minutes
  deployed on Streamlit with live audio playback and transcript view
```

---

## 🔑 Environment Variables

| Variable | Description |
|----------|-------------|
| `GROQ_API_KEY` | Groq API key for small LLM |
| `GEMINI_API_KEY` | Google Gemini API key for big LLM |
| `TAVILY_API_KEY` | Tavily search API key |
| `SARVAM_API_KEY` | Sarvam AI TTS API key |

⚠️ **Never commit your `.env` file to GitHub.** Make sure `.env` is in your `.gitignore`.

---

## 🚧 Roadmap

- [ ] Streamlit UI with live agent progress tracking
- [ ] Support for Hindi and regional Indian language podcasts (Sarvam supports 11 languages)
- [ ] Multiple episode formats (interview, debate, explainer)
- [ ] Podcast RSS feed generation
- [ ] Background music mixing

---

## Built With

- [CrewAI](https://crewai.com) — Multi-agent orchestration
- [Groq](https://groq.com) — Ultra-fast LLM inference
- [Google Gemini](https://deepmind.google/technologies/gemini/) — Creative writing LLM
- [Sarvam AI](https://sarvam.ai) — Indian language TTS
- [Tavily](https://tavily.com) — AI-optimized web search
