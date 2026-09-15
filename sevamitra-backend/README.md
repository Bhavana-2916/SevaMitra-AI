# SevaMitra Backend - RAG + Supabase + Groq

This bundle is the corrected backend base for the SevaMitra RAG setup.

Important:
- Keep your existing working `venv`. Do not replace it with this ZIP.
- Keep your working `.env` private. Create it from `.env.example`.
- Keep the working Groq configuration; the model defaults to `openai/gpt-oss-120b`.
- Supabase credentials are backend-only. Never put the service-role key in Next.js.

## 1. Install/upgrade dependencies

From `C:\sevamitra-backend` with `(venv)` active:

```powershell
python -m pip install -r requirements.txt
```

## 2. Create `.env`

Copy `.env.example` to `.env` and fill in:

```env
GROQ_API_KEY=...
SUPABASE_URL=https://YOUR_PROJECT_REF.supabase.co
SUPABASE_SERVICE_ROLE_KEY=...
```

Never commit `.env`.

## 3. Supabase SQL

Open `app/rag/supabase_schema.sql` and run it once in Supabase SQL Editor.

## 4. Add official PDFs

Put verified official government PDFs under:

`data/government_documents/`

## 5. Ingest

```powershell
python -m app.rag.ingest
```

## 6. Run backend

```powershell
uvicorn app.main:app --reload --port 8000
```

The existing frontend can continue calling `POST /api/chat`.
