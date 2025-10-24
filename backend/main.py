# backend/app.py
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import openai

# OpenAI API key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI(title="Neelakshi AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Deploy के बाद इसे अपने frontend URL से बदलें
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "Neelakshi AI backend is running."}

@app.post("/chat")
async def chat_endpoint(request: Request):
    body = await request.json()
    user_message = body.get("message", "")
    if not user_message:
        return {"reply": "Koi message bhejein."}

    # OpenAI Chat API call
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # या "gpt-4" / "gpt-3.5-turbo" — आपके account की availability के हिसाब से बदलें
            messages=[
                {"role": "system", "content": "You are Neelakshi AI — helpful assistant speaking Hindi and English."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=600,
            temperature=0.2
        )
        reply = response.choices[0].message.get("content", "").strip()
    except Exception as e:
        # सरल error message
        reply = f"Server error: {str(e)}"
    return {"reply": reply}
