# AI Support Desk

A learning project for a small support platform. The planned stack is React + TypeScript, FastAPI, and MySQL.

## MVP plan

1. **Project setup and API health check** — create the backend environment and confirm FastAPI runs.
2. **Support chat UI** — build a responsive React screen and connect it to a temporary chat endpoint.
3. **MySQL persistence** — add users, conversations, and messages, with migrations.
4. **Accounts and chat history** — add password hashing, login, protected history, and ownership checks.
5. **AI replies** — call a provider from the backend using a key loaded from `.env`; keep provider secrets out of the browser.
6. **Finish and publish** — run the app locally, document GitHub workflow, and outline deployment.

### MVP data model (planned for milestone 3)

- `users`: `id`, `email` (unique), `password_hash`, `created_at`
- `conversations`: `id`, `user_id` (owner), `title`, `created_at`, `updated_at`
- `messages`: `id`, `conversation_id`, `role` (`user` or `assistant`), `content`, `created_at`

Each conversation belongs to one user; each message belongs to one conversation. This keeps chat history private and gives us a small, relational schema to start with.

We are starting with milestone 1. The first API route is only a health check; chat, accounts, database, and AI arrive in later checkpoints.

### Checkpoint 1 acceptance checks

- The API starts locally without an import error.
- `GET /health` responds with HTTP 200 and `{"status":"ok"}`.
- The health check passes in pytest.

## Milestone 1: run the API

### Requirements

- Python 3.11 or newer
- VS Code
- macOS Command Line Tools (`xcode-select --install`) if Terminal reports that developer tools are missing

Check Python and Git in Terminal:

```bash
python3 --version
git --version
```

If Python is missing or older than 3.11, install a current Python 3 release from [python.org](https://www.python.org/downloads/macos/) and reopen Terminal. If Git prompts for Command Line Tools, install them with `xcode-select --install` and follow the macOS dialog.

From the project folder, create and activate a virtual environment, then install the API dependencies:

```bash
cd "/Users/bhavan/Documents/Codex/2026-11-11/referenced-chatgpt-conversation-this-is-an"
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r backend/requirements.txt
```

`venv` keeps this project's Python packages separate from the rest of the Mac. `source` activates it for the current Terminal window. The final commands install FastAPI and its development server.

Start the API:

```bash
uvicorn app.main:app --reload --app-dir backend
```

Open <http://127.0.0.1:8000/health> and expect `{"status":"ok"}`. Interactive API docs are at <http://127.0.0.1:8000/docs>. Stop the server with Control-C.

Run the milestone check from another Terminal window with the virtual environment activated:

```bash
python -m pytest backend/tests
```

## Configuration and secrets

Copy `.env.example` to `.env` when we add database and AI configuration. Real credentials belong only in `.env`, which Git ignores. The sample file contains placeholders, never usable keys. The future AI key will be read by the FastAPI server and must never be added to React or committed.

## Later: React, MySQL, and GitHub

Once the API health check works, the next checkpoint is a Vite React + TypeScript frontend. We will then add MySQL and schema migrations, followed by authentication, persistent chat history, and server-side AI integration. Before pushing to GitHub, initialize the repository with `git init`, check `git status`, and commit only source and `.env.example`; never commit `.env` or credentials. Deployment instructions will be added after the local MVP runs end to end.
