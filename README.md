# Neelakshi AI — Ready-to-deploy project

**AI Name:** Neelakshi AI  
**Languages:** English + Hindi  
**Theme:** Auto (light/dark via system preference)  
**Focus:** General Chat + News Writing (Hindi priority)

This package contains:
- `frontend/` — Next.js + React + Tailwind chat UI
- `backend/` — FastAPI backend that proxies to an LLM provider (OpenAI by default)
- `.env.example` files and deploy notes

Follow the included README sections below to configure and deploy.

---

## Quick local run (development)

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate        # on Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# set your OPENAI_API_KEY inside backend/.env
uvicorn main:app --reload --port 8080
```

### Frontend
```bash
cd frontend
npm install
# set NEXT_PUBLIC_API_URL in frontend/.env.local (default: http://localhost:8080)
cp .env.local.example .env.local
npm run dev
# Open: http://localhost:3000
```

## Deploy notes
1. Push repo to GitHub.
2. Deploy backend (Render / Railway / Fly / Heroku). Provide `OPENAI_API_KEY`.
3. Deploy frontend on Vercel. Set `NEXT_PUBLIC_API_URL` to your backend URL.
4. Add custom domain in Vercel and follow DNS instructions.

---

If you want, I can now walk you step-by-step to deploy to GitHub, Render, and Vercel.
