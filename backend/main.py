from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import httpx
from dotenv import load_dotenv
from aiolimiter import AsyncLimiter

load_dotenv()
OPENAI_KEY = os.getenv('OPENAI_API_KEY')
MODEL_ENDPOINT = os.getenv('MODEL_ENDPOINT', 'https://api.openai.com/v1/chat/completions')
MODEL_NAME = os.getenv('MODEL_NAME', 'gpt-35-turbo')

if not OPENAI_KEY:
    print('WARNING: OPENAI_API_KEY not set; backend will fail to call model provider')

app = FastAPI(title='Neelakshi AI Backend')

# ✅ Homepage route to avoid 404 on "/"
@app.get("/")
def read_root():
    return {"message": "Neelakshi AI backend is live and ready to chat!"}

# small rate limiter: 30 requests per minute
limiter = AsyncLimiter(30, 60)

class ChatRequest(BaseModel):
    messages: list

@app.post('/chat')
async def chat(req: ChatRequest):
    if not isinstance(req.messages, list) or len(req.messages) == 0:
        raise HTTPException(status_code=400, detail='messages required')

    # Build messages payload for model
    system_prompt = "You are Neelakshi AI, a helpful bilingual assistant (Hindi + English). Primary focus: producing clear news-style writing in Hindi when asked, and general chat otherwise. Be concise, factual, and avoid hallucinations. If uncertain, say you do not know."
    model_messages = [
        {"role": "system", "content": system_prompt}
    ]
    for m in req.messages:
        role = m.get('role', 'user')
        content = m.get('text', '')
        if role == 'system':
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
                raise HTTPException(status_code=502, detail=f'Upstream error: {resp.text}')
            data = resp.json()
            try:
                assistant_text = data['choices'][0]['message']['content']
            except Exception:
                assistant_text = 'Sorry — upstream returned unexpected response.'
    return {'reply': assistant_text}
