from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import httpx
from dotenv import load_dotenv
from aiolimiter import AsyncLimiter

load_dotenv()
OPENAI_KEY = os.getenv('OPENAI_API_KEY')
MODEL_ENDPOINT = os.getenv('MODEL_ENDPOINT', 'https://api.openai.com/v1/chat/completions')
MODEL_NAME = os.getenv('MODEL_NAME', 'gpt-3.5-turbo')

if not OPENAI_KEY:
    print('WARNING: OPENAI_API_KEY not set; backend will fail to call model provider')

app = FastAPI(title='Neelakshi AI Backend')

# ✅ CORS middleware added to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace "*" with your Vercel domain for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Status"])
def read_root():
    return {"message": "Neelakshi AI backend is live and ready to chat!"}

limiter = AsyncLimiter(30, 60)

class ChatRequest(BaseModel):
    messages: list

@app.post("/chat", tags=["Chat"])
async def chat(req: ChatRequest):
    if not isinstance(req.messages, list) or len(req.messages) == 0:
        raise HTTPException(status_code=400, detail='messages required')

    system_prompt = """
You are Neelakshi AI, a bilingual assistant (Hindi + English) designed for clear, conversational, and factual responses.
Your primary focus is:
- News-style writing in Hindi when asked for headlines or summaries
- General conversation in either Hindi or English
- Avoiding hallucinations or made-up facts
If uncertain, say "माफ कीजिए, मुझे इसकी जानकारी नहीं है।"
Respond concisely, clearly, and in a helpful tone.
"""

    model_messages = [{"role": "system", "content": system_prompt}]
    for m in req.messages:
        role = m.get('role', 'user')
        content = m.get('text', '')
        if role not in ['user', 'assistant']:
            continue
        model_messages.append({"role": role, "content": content})

    payload = {
        "model": MODEL_NAME,
        "messages": model_messages,
        "max_tokens": 512,
        "temperature": 0.6
    }

    async with limiter:
        headers = {'Authorization': f'Bearer {OPENAI_KEY}', 'Content-Type': 'application/json'}
        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(MODEL_ENDPOINT, headers=headers, json=payload)
            if resp.status_code != 200:
                print("OpenAI error:", resp.status_code, resp.text)
                raise HTTPException(status_code=502, detail=f'Upstream error: {resp.text}')
            data = resp.json()
            try:
                assistant_text = data.get('choices', [{}])[0].get('message', {}).get('content', '').strip()
                if not assistant_text:
                    assistant_text = 'माफ कीजिए, मुझे इसका उत्तर नहीं मिल पाया।'
            except Exception as e:
                print("Error parsing OpenAI response:", e)
                assistant_text = 'माफ कीजिए, मुझे इसका उत्तर नहीं मिल पाया।'

    return {'reply': assistant_text}
