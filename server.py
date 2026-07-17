import json
import os
import time
from typing import List, Optional

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from groq import Groq
from pydantic import BaseModel
from tokenizers import Tokenizer

load_dotenv()

TOKENIZER_PATH = os.path.join(os.path.dirname(__file__), "tokenizer.json")
tokenizer = Tokenizer.from_file(TOKENIZER_PATH)


def tokenize_display(text: str) -> List[dict]:
    """Tokenize text with the real Llama 3 tokenizer for live UI display."""
    if not text:
        return []
    encoding = tokenizer.encode(text, add_special_tokens=False)
    return [
        {"id": token_id, "text": tokenizer.decode([token_id])}
        for token_id in encoding.ids
    ]

GITHUB_USERNAME = os.getenv("GITHUB_USERNAME", "sobhan2204")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN") 
GITHUB_CACHE_TTL = 3600 

github_cache = {"data": None, "ts": 0.0}


def fetch_github_repos() -> List[dict]:
    """Fetch and cache the user's public GitHub repos, newest-active first."""
    now = time.time()
    if github_cache["data"] is not None and (now - github_cache["ts"]) < GITHUB_CACHE_TTL:
        return github_cache["data"]

    headers = {"Accept": "application/vnd.github+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    try:
        resp = requests.get(
            f"https://api.github.com/users/{GITHUB_USERNAME}/repos",
            params={"per_page": 100, "sort": "pushed", "direction": "desc"},
            headers=headers,
            timeout=8,
        )
        resp.raise_for_status()
        repos = resp.json()
    except Exception:
        # Fail soft: keep serving the cached/empty list rather than breaking /chat
        return github_cache["data"] or []

    cleaned = [
        {
            "name": r["name"],
            "description": r.get("description") or "",
            "url": r["html_url"],
            "language": r.get("language") or "",
            "stars": r.get("stargazers_count", 0),
            "topics": r.get("topics", []),
            "updated": r.get("pushed_at", ""),
        }
        for r in repos
        if not r.get("fork") and not r.get("archived")
    ]

    github_cache["data"] = cleaned
    github_cache["ts"] = now
    return cleaned


PORTFOLIO = {
    "name": "Sobhan Panda",
    "title": "Software Engineer",
    "location": "Noida, India",
    "email": "pandasobhan22@gmail.com",
    "phone": "9910180247",
    "linkedin": "https://www.linkedin.com/in/sobhan-panda-2277b7297/",
    "github": "https://github.com/sobhan2204",
    "availability": "Open to full-time roles, internships, and freelance AI/ML projects.",
    "summary": (
        "Software engineer specializing in Generative AI, machine learning pipelines, "
        "and backend systems. Experienced in building end-to-end agentic frameworks "
        "and observability platforms. Seeking to leverage skills in LLMs, RAG "
        "architectures, and scalable API design to deliver impactful technical solutions."
    ),
    "education": [
        {
            "institution": "Jaypee Institute of Information Technology",
            "location": "Noida, India",
            "degree": "B.Tech in Computer Science",
            "duration": "Aug 2023 - May 2027",
        }
    ],
    "skills": {
        "languages": ["Python", "JavaScript", "C++", "SQL"],
        "frameworks": [
            "Machine Learning",
            "Generative AI",
            "RAG",
            "AI Agents",
            "vLLM",
            "DSPy",
            "FAISS",
            "Pinecone",
            "Knowledge Graphs",
            "LangChain",
            "LangGraph",
            "MCP",
            "LLM Evaluation",
            "FastAPI",
            "Flask",
            "PyTorch",
        ],
        "tools": [
            "Docker",
            "Kubernetes",
            "Terraform",
            "Prometheus",
            "Grafana",
            "OpenTelemetry",
            "CI/CD",
            "Git",
            "AWS (ECS, ECR)",
            "PostgreSQL",
            "MySQL",
            "MongoDB",
            "Redis",
        ],
    },
    "projects": [
        {
            "name": "AI Agent Framework with Dynamic MCP Tool Orchestration",
            "stack": ["Python", "LangChain", "ReWOO", "MCP", "FAISS"],
            "github": "https://github.com/sobhan2204/Agentic_AI",
            "description": (
                "Built a modular agentic AI framework implementing the ReWOO architecture "
                "with Planner, Worker, Solver, and Refiner stages. Developed a dynamic "
                "MCP registry for tool orchestration and achieved sub-3 second response "
                "times for multi-step reasoning."
            ),
            "highlights": [
                "Planner, Worker, Solver, and Refiner stages",
                "Dynamic MCP registry for tool orchestration",
                "Sub-3 second response times on multi-step reasoning",
            ],
        },
        {
            "name": "Comparative Study of Multi-RAG Architectures",
            "stack": ["FAISS", "BM25", "Knowledge Graphs", "FastAPI"],
            "github": "https://github.com/sobhan2204/multi-rag-chatbot",
            "description": (
                "Built a multi-retriever RAG system combining vector search, BM25 "
                "retrieval, and knowledge graphs. Indexed and processed 4 comprehensive "
                "medical policies, then used an LLM-as-a-judge validator to measure "
                "cross-model consensus."
            ),
            "highlights": [
                "Vector search, BM25, and knowledge graphs",
                "LLM-as-a-judge validation pipeline",
                "87.6% groundedness and retrieval quality",
            ],
        },
        {
            "name": "Avalanche Susceptibility Mapping",
            "stack": ["PyTorch", "Earth Engine", "Flask"],
            "github": "https://github.com/sobhan2204/Avalanche-Susceptibility-Mapping-for-Vegetation-Restoration",
            "description": (
                "Processed over 3.4 GB of high-resolution Sentinel-2 satellite imagery "
                "to train a MultiSSL + U-KAN segmentation model integrated with DEM-"
                "derived terrain features. Built a geospatial ML system that combines "
                "vegetation suitability and avalanche susceptibility analysis."
            ),
            "highlights": [
                "3.4 GB of high-resolution satellite imagery",
                "MultiSSL plus U-KAN segmentation model",
                "15+ optimal coordinates for vegetation restoration",
            ],
        },
    ],
    "experience": [
        {
            "role": "Software Engineer Intern",
            "company": "LTM",
            "type": "Internship",
            "duration": "June 2026 - Present",
            "bullets": [
                "Building a cloud-ready observability platform using Prometheus and Grafana for monitoring infrastructure, services, and application performance.",
                "Designing dashboards, alerting pipelines, and metrics collection systems for a startup to ensure system reliability.",
            ],
        },
        {
            "role": "AI Engineer Intern (Team Lead)",
            "company": "Internpro",
            "type": "Internship",
            "duration": "June 2025 - July 2025",
            "bullets": [
                "Led a team of interns to develop a voice-enabled AI interview chatbot from scratch.",
                "Built datasets from scraped interview content, applied clustering techniques for different roles, and improved response quality through LLM fine-tuning.",
            ],
        },
    ],
}


def build_system_prompt(github_repos: Optional[List[dict]] = None) -> str:
    p = PORTFOLIO

    projects_text = ""
    for i, proj in enumerate(p["projects"], 1):
        projects_text += f"""
{i}. {proj['name']}
   Stack: {', '.join(proj['stack'])}
   GitHub: {proj['github']}
   Description: {proj['description']}
   Key highlights: {' | '.join(proj['highlights'])}
"""

    experience_text = ""
    for exp in p["experience"]:
        duration = f" ({exp['duration']})" if exp.get("duration") else ""
        experience_text += f"""
{exp['role']} at {exp['company']} ({exp['type']}){duration}
{chr(10).join('- ' + b for b in exp['bullets'])}
"""

    education_text = ""
    for edu in p["education"]:
        education_text += f"- {edu['degree']} at {edu['institution']}, {edu['location']} ({edu['duration']})\n"
        coursework = edu.get("coursework")
        if coursework:
            education_text += f"  Coursework: {', '.join(coursework)}\n"

    other_projects_text = ""
    if github_repos:
        featured_names = {proj["name"].lower() for proj in p["projects"]}
        others = [r for r in github_repos if r["name"].lower() not in featured_names][:8]
        for r in others:
            desc = f" - {r['description']}" if r["description"] else ""
            lang = f" [{r['language']}]" if r["language"] else ""
            other_projects_text += f"- {r['name']}{lang}{desc} ({r['url']})\n"

    return f"""You are the AI representative of {p['name']}, a highly capable and results-driven {p['title']} based in {p['location']}.

Your job: Answer visitor questions clearly while representing {p['name']} well. Prioritize portfolio, hiring, project, skill, and experience questions, but you may also answer broader technical or career questions when helpful.
Always speak as Sobhan. Use "I", "my", and "me".

Tone:
- Confident, sharp, and professional
- Slightly persuasive
- Enthusiastic about work and impact
- A little sarcasm is allowed when appropriate, but do not sound arrogant or cocky
- Never arrogant, but clearly high-value

ABOUT
{p['summary']}
Availability: {p['availability']}

EDUCATION
{education_text}

SKILLS
Languages: {', '.join(p['skills']['languages'])}
Frameworks/Libraries: {', '.join(p['skills']['frameworks'])}
Tools: {', '.join(p['skills']['tools'])}

PROJECTS
{projects_text}
{f'''OTHER GITHUB REPOS (mention only if directly relevant or specifically asked; these are lower priority than the featured projects above)
{other_projects_text}''' if other_projects_text else ''}
EXPERIENCE
{experience_text}

CONTACT
Email: {p['email']}
Phone: {p['phone']}
LinkedIn: {p['linkedin']}
GitHub: {p['github']}

RESPONSE STRATEGY
- Keep answers to 2-5 sentences unless a deep dive is requested
- Always frame responses to highlight impact, problem-solving, or technical strength
- Use strong phrases like "I've built...", "What makes this stand out is...", and "I focused on solving..."
- After answering, invite them to explore: {p['github']}
- If asked about something outside the portfolio, say "I don't have that detail handy - feel free to reach out at {p['email']}"
- Always end with a question about what the recruiter is looking for, such as "what job role are you looking for?" or "what kind of projects are you hiring for?"

EDGE RULES
- Do not invent skills or experience not listed above
- Do not sound generic or like a chatbot
- Avoid weak phrases like "I think" or "I tried"
- Prefer "I built", "I designed", and "I optimized"
- For unrelated general questions, answer briefly if useful, then steer back to how it connects to {p['name']}'s work when possible
- Do not invent personal facts, projects, credentials, employers, metrics, or private details not listed above
"""


TECH_KEYWORDS = {
    "ai": ["AI", "artificial intelligence", "machine learning", "ML", "neural", "deep learning"],
    "llm": ["LLM", "language model", "ChatGPT", "GPT", "Gemini", "Claude", "Groq", "vLLM", "DSPy"],
    "nlp": ["NLP", "text", "language", "sentiment", "named entity"],
    "vision": ["computer vision", "CV", "image", "CNN", "object detection", "Sentinel", "satellite"],
    "rag": ["RAG", "retrieval", "vector", "embedding", "FAISS", "semantic search", "knowledge graph", "BM25"],
    "api": ["API", "REST", "backend", "server", "endpoint", "HTTP", "FastAPI", "Flask"],
    "backend": ["FastAPI","Rate limiting", "micro services", "load balancing"],
    "database": ["database", "SQL", "MongoDB", "Postgres", "PostgreSQL", "MySQL", "Redis", "Pinecone"],
    "agents": ["agent", "multi-agent", "agentic", "workflow", "tool", "routing", "planner", "worker", "solver", "refiner"],
    "langchain": ["LangChain", "LangGraph", "MCP", "ReWOO"],
    "mlops": ["pipeline", "automation", "hyperparameter", "tuning", "scikit-learn", "MLflow", "evaluation"],
    "devops": ["Docker","Prometheus", "Grafana", "OpenTelemetry", "CI/CD", "GitHub Actions"],
    "cloud": ["AWS", "ECS", "ECR", "cloud", "observability", "monitoring", "alerting", "Loki"],
    "voice": ["voice", "speech", "audio", "interviewer"],
    "interview": ["interview", "assessment", "evaluation"],
}

DOMAIN_TO_SKILLS = {
    "ai": ["Python", "Machine Learning", "Generative AI"],
    "llm": ["Python", "LangChain", "LangGraph", "vLLM", "DSPy"],
    "nlp": ["Python", "Generative AI"],
    "vision": ["Python", "C++"],
    "rag": ["Python", "LangChain", "FAISS", "Qdrant", "Knowledge Graphs"],
    "api": ["Python", "FastAPI", "Flask", "JavaScript"],
    "frontend": ["HTML", "CSS", "JavaScript", "Node.js"],
    "database": ["SQL", "PostgreSQL", "MySQL", "MongoDB", "Redis", "Qdrant"],
    "fullstack": ["Python", "JavaScript", "Node.js", "FastAPI", "Flask"],
    "agents": ["Python", "LangChain", "LangGraph", "MCP", "ReWOO"],
    "langchain": ["Python", "LangChain", "LangGraph", "MCP"],
    "devops": ["Docker", "Kubernetes", "Terraform", "Prometheus", "Grafana", "OpenTelemetry"],
    "cloud": ["AWS", "Docker", "Kubernetes", "Terraform"],
    "mlops": ["Python", "PyTorch", "MLflow", "scikit-learn"],
    "voice": ["JavaScript", "Python"],
    "interview": ["Python", "JavaScript"],
}

DOMAIN_TO_PROJECTS = {
    "ai": [0, 1, 2],
    "llm": [0, 1],
    "nlp": [0, 1],
    "vision": [2],
    "rag": [1],
    "api": [1, 2],
    "frontend": [],
    "database": [1],
    "fullstack": [0, 1, 2],
    "agents": [0],
    "langchain": [0, 1],
    "devops": [0, 1, 2],
    "cloud": [2],
    "mlops": [2],
    "voice": [],
    "interview": [],
}


def extract_requirements(message: str) -> dict:
    message_lower = message.lower()
    matched = {}
    for domain, keywords in TECH_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw.lower() in message_lower)
        if score > 0:
            matched[domain] = score
    return dict(sorted(matched.items(), key=lambda x: x[1], reverse=True))


def build_requirement_context(message: str) -> str:
    domains = extract_requirements(message)
    if not domains:
        return ""

    matched_skills = set()
    for d in domains:
        matched_skills.update(DOMAIN_TO_SKILLS.get(d, []))

    matched_indices = set()
    for d in domains:
        matched_indices.update(DOMAIN_TO_PROJECTS.get(d, []))

    matched_projects = [
        PORTFOLIO["projects"][i] for i in sorted(matched_indices)
        if i < len(PORTFOLIO["projects"])
    ]
    skill_text = ", ".join(sorted(matched_skills)) or "None"
    project_text = ", ".join([p["name"] for p in matched_projects[:2]]) or "None"

    return f"""
REQUIREMENT ANALYSIS
Recruiter is asking about: {', '.join([d.upper() for d in list(domains.keys())[:3]])}
Relevant skills: {skill_text}
Most relevant projects: {project_text}
Highlight these naturally. Keep it concise but impressive.
"""


class Message(BaseModel):
    role: str
    text: str


class LLMParams(BaseModel):
    temperature: float = 0.7
    max_completion_tokens: int = 300
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    seed: Optional[int] = None
    style_prompt: str = ""
    reasoning_effort: str = "medium"


class ChatRequest(BaseModel):
    message: str
    history: List[Message] = []
    llm_params: Optional[LLMParams] = None


class ChatResponse(BaseModel):
    reply: str
    history: List[Message]


class TokenizeRequest(BaseModel):
    text: str


REASONING_MULTIPLIERS = {"low": 0.5, "medium": 1.0, "high": 2.0}


def resolve_max_tokens(params: LLMParams) -> int:
    multiplier = REASONING_MULTIPLIERS.get(params.reasoning_effort, 1.0)
    return max(50, min(int(params.max_completion_tokens * multiplier), 8192))


app = FastAPI(title="Sobhan Panda - AI Portfolio", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_groq_client() -> Groq:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="GROQ_API_KEY not set. Add it to your .env file.",
        )
    return Groq(api_key=api_key)


@app.get("/health")
def health():
    return {"status": "ok", "name": PORTFOLIO["name"], "title": PORTFOLIO["title"]}


@app.get("/info")
def info():
    return {
        "name": PORTFOLIO["name"],
        "title": PORTFOLIO["title"],
        "location": PORTFOLIO["location"],
        "email": PORTFOLIO["email"],
        "phone": PORTFOLIO["phone"],
        "linkedin": PORTFOLIO["linkedin"],
        "github": PORTFOLIO["github"],
        "summary": PORTFOLIO["summary"],
        "availability": PORTFOLIO["availability"],
        "skills": PORTFOLIO["skills"],
        "projects": [
            {
                "name": p["name"],
                "stack": p["stack"],
                "github": p["github"],
                "description": p["description"],
                "highlights": p["highlights"],
            }
            for p in PORTFOLIO["projects"]
        ],
        "experience": PORTFOLIO["experience"],
        "education": PORTFOLIO["education"],
    }


@app.get("/github")
def github_repos():
    return {"username": GITHUB_USERNAME, "repos": fetch_github_repos()}


def build_groq_kwargs(req: ChatRequest) -> dict:
    params = req.llm_params if req.llm_params is not None else LLMParams()

    system_content = build_system_prompt(github_repos=fetch_github_repos())

    if params.style_prompt.strip():
        system_content += f"\n\nSTYLE INSTRUCTION\n{params.style_prompt}\n"

    req_context = build_requirement_context(req.message)
    if req_context:
        system_content += req_context

    messages = [{"role": "system", "content": system_content}]
    for msg in req.history:
        role = "assistant" if msg.role == "model" else msg.role
        messages.append({"role": role, "content": msg.text})
    messages.append({"role": "user", "content": req.message})

    temperature = max(0.0, min(2.0, params.temperature))
    top_p = max(0.0, min(1.0, params.top_p))
    frequency_penalty = max(-2.0, min(2.0, params.frequency_penalty))
    presence_penalty = max(-2.0, min(2.0, params.presence_penalty))
    max_tokens = resolve_max_tokens(params)

    groq_kwargs = dict(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
    )
    if params.seed is not None:
        groq_kwargs["seed"] = params.seed

    return groq_kwargs


def build_updated_history(req: ChatRequest, reply: str) -> List[Message]:
    updated_history = req.history + [
        Message(role="user", text=req.message),
        Message(role="model", text=reply),
    ]
    if len(updated_history) > 40:
        updated_history = updated_history[-40:]
    return updated_history


@app.post("/tokenize")
def tokenize(req: TokenizeRequest):
    return {"tokens": tokenize_display(req.text)}


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    groq_client = get_groq_client()
    groq_kwargs = build_groq_kwargs(req)

    try:
        response = groq_client.chat.completions.create(**groq_kwargs)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    reply = response.choices[0].message.content
    updated_history = build_updated_history(req, reply)

    return ChatResponse(reply=reply, history=updated_history)


@app.post("/chat/stream")
async def chat_stream(req: ChatRequest):
    groq_client = get_groq_client()
    groq_kwargs = build_groq_kwargs(req)

    def event_stream():
        accumulated = ""
        try:
            stream = groq_client.chat.completions.create(stream=True, **groq_kwargs)
            for chunk in stream:
                delta = chunk.choices[0].delta.content or ""
                if not delta:
                    continue
                accumulated += delta
                payload = {"tokens": tokenize_display(accumulated)}
                yield f"data: {json.dumps(payload)}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
            return

        history = [m.model_dump() for m in build_updated_history(req, accumulated)]
        yield f"data: {json.dumps({'done': True, 'reply': accumulated, 'history': history})}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")


if __name__ == "__main__":
    import uvicorn

    print("\nSobhan Panda AI Portfolio Server v2.0")
    print("Docs:   http://localhost:8000/docs")
    print("Health: http://localhost:8000/health")
    print("Chat:   POST http://localhost:8000/chat")
    print("\nAll sidebar controls are wired:")
    print("temperature | max_tokens | top_p | freq/pres penalty")
    print("seed (consistency mode) | style_prompt | reasoning_effort\n")
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
