<div align="center">

# 🎨 AiToon  
### *AI-Powered Comic Story Generation Platform*

<p align="center">
  <img src="https://img.shields.io/badge/Frontend-Next.js-black?style=for-the-badge&logo=next.js" />
  <img src="https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi" />
  <img src="https://img.shields.io/badge/AI-LLM%20Orchestrator-blueviolet?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Image%20Generation-Pixazo-orange?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Database-MongoDB-green?style=for-the-badge&logo=mongodb" />
</p>

<p align="center">
  <b>Transform stories into fully illustrated comic panels using AI</b>
</p>

<br>

<img src="./assets/readme/landing-ui.png" width="100%" alt="AiToon Landing Page UI"/>

<br><br>

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-tech-stack">Tech Stack</a> •
  <a href="#-setup">Setup</a>
</p>

</div>

---

# ✨ About AiToon

AiToon is a **full-stack AI comic generation platform** that converts a simple story idea into a **structured multi-panel comic strip** with:

- 🎭 Story scenes
- 👤 consistent characters
- 💬 dialogues
- 🖼️ AI-generated comic panels

The platform follows a **3-layer intelligent architecture**:

```text
Client (Next.js)
    ↓
FastAPI + LLM Orchestrator
    ↓
AI Image Generation Engine
```

---

# 🚀 Features

- 🎨 Theme-based comic generation
- 🧠 AI story orchestration pipeline
- 👤 character consistency memory
- 💬 automatic dialogue generation
- 🖼️ AI panel image generation
- 🔁 retry + fallback image models
- ⚡ parallel batch rendering
- 🛠️ single panel regeneration

---

# 🎨 Main Dashboard / Editor UI

<p align="center">
  <img src="./assets/readme/editor-dashboard.png" width="100%" alt="AiToon Editor Dashboard"/>
</p>

---

# 🏗️ Architecture

```text
User Input
   ↓
Story Setup UI
   ↓
FastAPI Backend
   ↓
LLM Orchestrator Graph
   ↓
Structured Comic JSON
   ↓
Prompt Builder
   ↓
Model Router + Retry Engine
   ↓
Image Generation
   ↓
Comic Editor UI
```

---

# 💻 Tech Stack

| Layer | Technologies |
|---|---|
| Frontend | Next.js, React.js |
| Backend | FastAPI, Python |
| AI | Groq, Gemini, OpenRouter |
| Image Engine | Pixazo, Flux, SDXL |
| Database | MongoDB |

---

# 📂 Project Structure

```text
AiToon/
│
├── client/
├── server/
├── image_gen/
├── outputs/
└── assets/readme/
```

---

# ⚙️ Setup

## Backend

```bash
cd server
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

## Frontend

```bash
cd client
npm install
npm run dev
```

---

<div align="center">

## 🌟 Built with AI + Full Stack Engineering

⭐ Star this repo if you like the project

</div>