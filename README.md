https://portfolio-inky-eight-95.vercel.app/

# AI Portfolio Chatbot

A personal portfolio website with a built-in AI recruiter assistant.

This project combines:
- A frontend portfolio page (`index.html`) with a modern chat interface
- A FastAPI backend (`server.py`) that serves portfolio data and routes chat requests to Groq
- Dynamic requirement matching that tailors responses based on recruiter keywords (AI, RAG, agents, frontend, MLOps, etc.)

## What This Project Does

- Presents portfolio information (skills, projects, experience, education)
- Lets visitors chat with an AI representative in real time
- Detects topic keywords in user messages and highlights relevant strengths/projects
- Supports advanced LLM controls from the UI (temperature, top-p, penalties, seed, style prompt, reasoning effort)

## Tech Stack

- Python
- FastAPI
- Uvicorn
- Groq API
- python-dotenv
- HTML, CSS, JavaScript

## Project Structure

- `index.html` - Frontend portfolio site + chat UI + LLM control sidebar
- `server.py` - FastAPI app, portfolio data, prompt building, requirement routing, chat endpoint
- `req.txt` - Python dependency list
- `README.md` - Project documentation

## Prerequisites

- Python 3.10+
- A Groq API key

Get a free key from: https://console.groq.com

## Setup

1. Clone the repository and open the project folder.
2. Create and activate a virtual environment (recommended).
3. Install dependencies:

```bash
pip install -r req.txt
```

If needed, also install missing packages manually:

```bash
pip install uvicorn groq python-dotenv
```

4. Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

## Run the App

1. Start backend server:

```bash
python server.py
```

2. Open `index.html` in your browser.

The frontend expects the API at:
- `http://localhost:8000`

## API Endpoints

- `GET /health`
  - Returns service status and basic profile info
- `GET /info`
  - Returns portfolio metadata (skills, projects, experience, education)
- `POST /chat`
  - Accepts message, chat history, and optional LLM parameters
  - Returns assistant reply and updated conversation history

Interactive API docs:
- `http://localhost:8000/docs`

## Example Chat Request

```json
{
  "message": "Do you have experience with RAG systems?",
  "history": [],
  "llm_params": {
    "temperature": 0.7,
    "max_completion_tokens": 300,
    "top_p": 1.0,
    "frequency_penalty": 0.0,
    "presence_penalty": 0.0,
    "seed": null,
    "style_prompt": "Respond in a concise professional tone.",
    "reasoning_effort": "medium"
  }
}
```

## Key Implementation Highlights

- Domain keyword extraction and scoring (`extract_requirements`)
- Dynamic context injection for matched domains (`build_requirement_context`)
- Prompt builder with structured portfolio context (`build_system_prompt`)
- Groq parameter safety clamping and reasoning-based token scaling
- CORS-enabled FastAPI backend for local frontend usage

## Troubleshooting

- Error: `GROQ_API_KEY not set`
  - Ensure `.env` exists in project root and includes a valid key

- Frontend chat shows server offline
  - Confirm backend is running on port `8000`
  - Check `http://localhost:8000/health`

- Import errors for `dotenv` or `groq`
  - Install required packages using `pip install -r req.txt`

## Roadmap Ideas

- Serve frontend from FastAPI static routes (single command startup)
- Add conversation persistence (database)
- Add analytics for recruiter query categories
- Add deployment guides (Render/Vercel + backend hosting)

## Author

Sobhan Panda

- GitHub: https://github.com/sobhan2204
- LinkedIn: https://linkedin.com/in/sobhan-panda-2277b7297
- Email: pandasobhan22@gmail.com
