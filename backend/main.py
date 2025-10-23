from fastapi import FastAPI, HTTPException
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

    # ✅ Refined system prompt for ChatGPT-like behavior
    system_prompt = """
You are Neelakshi AI, a bilingual assistant (Hindi + English) designed for clear, conversational, and factual responses.
Your primary focus is:
- News-style writing in Hindi when asked for headlines or summaries
- General conversation in either Hindi or English
- Avoiding hallucinations or made-up facts
If uncertain, say "माफ कीजिए, मुझे इसकी जानकारी नहीं है।"
Respond concisely, clearly, and in a helpful tone.
"""

    # ✅ Build message flow
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
                raise HTTPException(status_code=502, detail=f'Upstream error: {resp.text}')
            data = resp.json()
            try:
                assistant_text = data['choices'][0]['message']['content']
            except Exception:
                assistant_text = 'माफ कीजिए, मुझे इसका उत्तर नहीं मिल पाया।'

    return {'reply': assistant_text}
