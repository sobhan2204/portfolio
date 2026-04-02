"""
===============================================================
  Sobhan Panda — AI Portfolio Backend  v2.0
  Powered by: Groq API (free)
  Run with: python server.py
  Then open: index.html in your browser
===============================================================

HOW TO INSTALL & RUN:
  1. pip install fastapi uvicorn groq python-dotenv
  2. Create a .env file with: GROQ_API_KEY=your_key_here
     (Get a free key at: https://console.groq.com)
  3. python server.py
  4. Open index.html in your browser

WHAT'S NEW IN v2.0:
  - LLM sidebar controls (temperature, max_tokens, top_p, penalties,
    seed, style, reasoning_effort) are now FULLY WIRED to Groq.
  - ChatRequest now accepts an optional llm_params block.
  - reasoning_effort maps to a token multiplier (low=0.5x, medium=1x, high=2x).
  - seed is forwarded only when Consistency Mode is ON (non-None).
  - style_prompt is injected into the system prompt.
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

PORTFOLIO = {
    "name": "Sobhan Panda",
    "title": "AI Engineer",
    "location": "Noida, Uttar Pradesh",
    "email": "pandasobhan22@gmail.com",
    "phone": "9910180247",
    "linkedin": "https://linkedin.com/in/sobhan-panda-2277b7297",
    "github": "https://github.com/sobhan2204",
    "availability": "Open to full-time roles, internships, and freelance AI/ML projects.",
    "summary": (
        "AI Engineer who builds intelligent systems that actually work in the real world. "
        "I specialize in creating AI applications that can remember context, use tools "
        "effectively, and solve complex problems for users."
    ),
    "education": [
        {
            "institution": "Jaypee Institute of Information Technology",
            "location": "Noida, Uttar Pradesh",
            "degree": "B.Tech Computer Science",
            "duration": "Aug 2023 – May 2027",
            "coursework": [
                "Data Structures", "Algorithms", "Probability & Statistics",
                "Operating Systems", "Computer Security", "Computer Architecture"
            ]
        },
        {
            "institution": "Modern Vidya Niketan School",
            "location": "Faridabad, Haryana",
            "scores": "10th: 94.3% | 12th: 75%"
        }
    ],
    "skills": {
        "languages": ["Python", "C++", "JavaScript", "HTML", "CSS", "MongoDB"],
        "frameworks": ["LangChain", "LangGraph", "MCP", "Transformers", "FAISS", "FastAPI", "HuggingFace", "Docker"],
        "tools": ["Git", "Jupyter Notebook", "MLflow", "Vercel"]
    },
    "projects": [
        {
            "name": "Agentic AI — Multi-Tool Assistant",
            "stack": ["Python", "LangChain", "LangGraph", "FAISS", "MCP"],
            "github": "https://github.com/sobhan2204",
            "description": (
                "The aim of this porject was not to build a ai pipeline but to build a versatile agentic AI assistant capable of handling complex tasks by orchestrating multiple tools and workflows using MCP"
                " and LangGraph. The assistant can perform real-time decision making, tool selection, and dynamic workflow routing based on user queries. It integrates various tools like search, database access, and external APIs to provide accurate and contextually relevant responses. The system is designed to blend memory, intent recognition, planning , reasoning, self-evaluation, and tool outputs to achieve sophisticated task completion."
                "decision making through collaborative multi-agent workflows blending memory + "
                "intent + reasoning + self-evaluation + tool outputs. "
            ),
            "why it stands out" : ("This is not a regular AI assistant that is hust a pipeline of tools. It is an agentic system that can dynamically decide which tool to use, how to route information between them, and how to reason through complex tasks in real-time. The integration of MCP and LangGraph allows for sophisticated multi-agent collaboration, enabling the assistant to handle a wide range of queries with contextual understanding and adaptability."),
            "highlights": [
                "Multi-agent routing with MCP , LangGraph and LagChain",
                "Blends memory, intent , planning , reasoning, self-evaluation",
                "Real-time decision making across diverse tools"
            ]
        },
        {
            "name": "Multi-RAG Chatbot",
            "stack": ["Python", "LangChain", "FAISS", "HuggingFace"],
            "github": "https://github.com/sobhan2204",
            "description": (
                "Modular RAG chatbot that runs semantic search, knowledge graph, and BM25 simentaniously and constantly checks accuracy across all three, picking the best. "
                "It is a pipeline that supports dynamic ingestion of text, PDF, and structured data into FAISS vector stores."
                "And then retrive the answer using 3 RAG algorithms in parallel."
            ),
            "why it stands out":(" Unlike typical RAG implementations that rely on a single retrieval method, this chatbot runs three distinct RAG algorithms simultaneously and evaluates their outputs in real-time to select the most accurate response. This multi-algorithm approach ensures higher accuracy and robustness, as it can leverage the strengths of each method depending on the query context. Additionally, the system is designed to handle diverse data formats, allowing for seamless ingestion of text, PDFs, and structured data into FAISS vector stores, making it adaptable to various use cases."),
            "highlights": [
                "Runs 3 RAG algorithms in parallel",
                "Selects best answer by accuracy score",
                "Supports text, PDF, and structured data ingestion"
            ]
        },
        {
            "name": "Automated ML Pipeline Framework",
            "stack": ["Python", "scikit-learn", "MLflow", "FastAPI"],
            "github": "https://github.com/sobhan2204",
            "description": (
                "Modular pipeline automating data validation, preprocessing, feature engineering, "
                "and model selection. Implements automated hyperparameter tuning and evaluation "
                "across multiple ML algorithms. Selects the model with the highest accuracy. "
                "Handles diverse datasets with robust EDA. Scalable via FastAPI."
            ),
            "highlights": [
                "Full automation from raw data to best model",
                "Hyperparameter tuning across multiple algorithms",
                "Scalable REST API via FastAPI"
            ]
        },
        {
            "name": "InterviewAce — Voice AI Interviewer",
            "stack": ["Google Gemini API", "Web Speech API", "JavaScript"],
            "github": "https://github.com/sobhan2204",
            "description": (
                "Real-time voice-based AI interviewer. Led the team as Team Lead and sole "
                "AI developer, owning the complete Generative AI solution. Built prompt flow, "
                "conversational logic, and AI response handling for contextual voice interviews "
                "using Web Speech API and Google Gemini API."
            ),
            "highlights": [
                "Real-time voice interviews with Gemini",
                "Full GenAI stack designed and built solo",
                "Contextual prompt flow and conversation logic"
            ]
        }
    ],
    "experience": [
        {
            "role": "Team Lead & AI Engineer",
            "company": "Internpro",
            "type": "Internship",
            "bullets": [
                "Led the team and served as the sole AI developer",
                "Built real-time voice AI interviewer using Web Speech API and Google Gemini API",
                "Designed prompt flow, conversational logic, and AI response handling",
                "Collaborated with frontend developers on HTML/CSS/JS implementation"
            ]
        }
    ]
}


def build_system_prompt() -> str:
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
        experience_text += f"""
{exp['role']} at {exp['company']} ({exp['type']})
{chr(10).join('- ' + b for b in exp['bullets'])}
"""

    education_text = ""
    for edu in p["education"]:
        if "degree" in edu:
            education_text += f"- {edu['degree']} at {edu['institution']}, {edu['location']} ({edu['duration']})\n"
            education_text += f"  Coursework: {', '.join(edu['coursework'])}\n"
        else:
            education_text += f"- {edu['institution']}, {edu['location']} — {edu['scores']}\n"

    return f"""You are the AI representative of {p['name']}, a highly capable and results-driven {p['title']} based in {p['location']}.

Your job: Impress recruiters and hiring managers by clearly demonstrating why {p['name']} is an exceptional candidate.
Always speak AS Sobhan — use "I", "my", "me".


Tone:
- Confident, sharp, and professional
- Slightly persuasive (like a strong candidate who knows their worth)
- Enthusiastic about work and impact
- little sarcasm is allowed when appropriate, but do NOT sound arrogant or cocky
- Never arrogant, but clearly high-value
- don't fake anything 

━━━ ABOUT ━━━
{p['summary']}
Availability: {p['availability']}

━━━ EDUCATION ━━━
{education_text}

━━━ SKILLS ━━━
Languages: {', '.join(p['skills']['languages'])}
Frameworks/Libraries: {', '.join(p['skills']['frameworks'])}
Tools: {', '.join(p['skills']['tools'])}

━━━ PROJECTS ━━━
{projects_text}

━━━ EXPERIENCE ━━━
{experience_text}

━━━ CONTACT ━━━
Email: {p['email']}
Phone: {p['phone']}
LinkedIn: {p['linkedin']}
GitHub: {p['github']}

━━━ RESPONSE STRATEGY ━━━
- Keep answers to 2–5 sentences unless a deep dive is requested
- Always frame responses to highlight impact, problem-solving, or technical strength
- Use strong phrases: "I've built…", "What makes this stand out is…", "I focused on solving…"
- Can be sarcastic when stupid questions are asked but do NOT sound arrogant or cocky
- After answering, invite them to explore: {p['github']}
- If something is not available: "I don't have that detail handy — feel free to reach out at {p['email']}"

━━━ EDGE RULES ━━━
- Do NOT invent skills or experience not listed above
- Do NOT sound generic or like a chatbot
- Avoid weak phrases like "I think" or "I tried"
- Prefer "I built", "I designed", "I optimized"

━━━ CLOSING STYLE ━━━
End with confidence: "Happy to discuss this further." or "Let's connect if this aligns with what you're looking for."
"""


TECH_KEYWORDS = {
    "ai": ["AI", "artificial intelligence", "machine learning", "ML", "neural", "deep learning"],
    "llm": ["LLM", "language model", "ChatGPT", "GPT", "Gemini", "Claude", "groq"],
    "nlp": ["NLP", "text", "language", "sentiment", "named entity"],
    "vision": ["computer vision", "CV", "image", "CNN", "object detection"],
    "rag": ["RAG", "retrieval", "vector", "embedding", "FAISS", "semantic search", "knowledge graph", "BM25"],
    "api": ["API", "REST", "backend", "server", "endpoint", "HTTP"],
    "frontend": ["frontend", "UI", "UX", "CSS", "HTML", "React", "JavaScript"],
    "database": ["database", "SQL", "MongoDB", "Postgres", "Redis"],
    "agents": ["agent", "multi-agent", "agentic", "workflow", "tool", "routing"],
    "langchain": ["LangChain", "LangGraph"],
    "mlops": ["pipeline", "automation", "hyperparameter", "tuning", "scikit-learn", "MLflow"],
    "voice": ["voice", "speech", "audio", "interviewer"],
    "interview": ["interview", "assessment", "evaluation"],
}

DOMAIN_TO_SKILLS = {
    "ai": ["Python", "Transformers", "HuggingFace"],
    "llm": ["Python", "LangChain", "LangGraph"],
    "nlp": ["Python", "Transformers", "HuggingFace"],
    "vision": ["Python", "C++"],
    "rag": ["Python", "LangChain", "FAISS", "HuggingFace", "MongoDB"],
    "api": ["Python", "FastAPI", "JavaScript"],
    "frontend": ["HTML", "CSS", "JavaScript"],
    "database": ["MongoDB", "Python"],
    "fullstack": ["Python", "JavaScript", "HTML", "CSS", "FastAPI"],
    "agents": ["Python", "LangChain", "LangGraph"],
    "langchain": ["Python", "LangChain", "LangGraph"],
    "devops": ["Docker"],
    "cloud": ["Vercel"],
    "mlops": ["Python", "MLflow", "scikit-learn"],
    "voice": ["JavaScript", "Python"],
    "interview": ["JavaScript", "Python"],
}

DOMAIN_TO_PROJECTS = {
    "ai": [0, 1, 2],
    "llm": [0, 1],
    "nlp": [0, 1],
    "vision": [2],
    "rag": [1],
    "api": [2],
    "frontend": [3],
    "database": [1],
    "fullstack": [3],
    "agents": [0],
    "langchain": [0, 1],
    "devops": [0, 1, 2, 3],
    "cloud": [3],
    "mlops": [2],
    "voice": [3],
    "interview": [3],
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
    return f"""
━━━ REQUIREMENT ANALYSIS ━━━
Recruiter is asking about: {', '.join([d.upper() for d in list(domains.keys())[:3]])}
Relevant skills: {', '.join(sorted(matched_skills))}
Most relevant projects: {', '.join([p['name'] for p in matched_projects[:2]])}
Highlight these naturally. Keep it concise but impressive.
"""

class Message(BaseModel):
    role: str   
    text: str


class LLMParams(BaseModel):
    """
    All controls exposed by the HTML sidebar.
    Each field has a safe default so the endpoint works even without the sidebar.
    """
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


REASONING_MULTIPLIERS = {"low": 0.5, "medium": 1.0, "high": 2.0}

def resolve_max_tokens(params: LLMParams) -> int:
    """Slider value × reasoning_effort multiplier, clamped to Groq's limit."""
    multiplier = REASONING_MULTIPLIERS.get(params.reasoning_effort, 1.0)
    return max(50, min(int(params.max_completion_tokens * multiplier), 8192))


 
app = FastAPI(title="Sobhan Panda — AI Portfolio", version="2.0.0")

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
            detail="GROQ_API_KEY not set. Add it to your .env file."
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


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """
    Reads llm_params from the request and passes every value to Groq.
    All sidebar controls are now fully active.
    """
    groq_client = get_groq_client()

    # Use sidebar params if sent, otherwise fall back to defaults
    params = req.llm_params if req.llm_params is not None else LLMParams()

    system_content = build_system_prompt()

    # Style instruction from the dropdown (e.g. "Formal", "Technical")
    if params.style_prompt.strip():
        system_content += f"\n\n━━━ STYLE INSTRUCTION ━━━\n{params.style_prompt}\n"

    # Domain-specific context based on message keywords
    req_context = build_requirement_context(req.message)
    if req_context:
        system_content += req_context

    messages = [{"role": "system", "content": system_content}]
    for msg in req.history:
        role = "assistant" if msg.role == "model" else msg.role
        messages.append({"role": role, "content": msg.text})
    messages.append({"role": "user", "content": req.message})

    temperature       = max(0.0, min(2.0,  params.temperature))
    top_p             = max(0.0, min(1.0,  params.top_p))
    frequency_penalty = max(-2.0, min(2.0, params.frequency_penalty))
    presence_penalty  = max(-2.0, min(2.0, params.presence_penalty))
    max_tokens        = resolve_max_tokens(params)  # slider × reasoning multiplier

    try:
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

        response = groq_client.chat.completions.create(**groq_kwargs)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    reply = response.choices[0].message.content

    updated_history = req.history + [
        Message(role="user",  text=req.message),
        Message(role="model", text=reply),
    ]
    if len(updated_history) > 40:
        updated_history = updated_history[-40:]

    return ChatResponse(reply=reply, history=updated_history)


if __name__ == "__main__":
    import uvicorn
    print("\n🚀  Sobhan Panda AI Portfolio Server v2.0")
    print("    Docs:   http://localhost:8000/docs")
    print("    Health: http://localhost:8000/health")
    print("    Chat:   POST http://localhost:8000/chat")
    print("\n      All sidebar controls are wired:")
    print("        temperature · max_tokens · top_p · freq/pres penalty")
    print("        seed (consistency mode) · style_prompt · reasoning_effort\n")
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)