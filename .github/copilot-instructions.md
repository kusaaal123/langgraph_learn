# Copilot Instructions — Agentic AI Code Review Project

Project guidelines for AI assistance when working in this workspace.

---

## 🎯 Project Overview

This repository is a structured learning project building an **AI Code Review & Refactoring Agent** using **Python**, **LangChain**, and **LangGraph**. The developer has a strong .NET/backend engineering background.

Key documentation:
* Roadmap & Candidates: [docs/roadmap.md](docs/roadmap.md)
* Progress Checklist: [docs/progress.md](docs/progress.md)
* Source Structure: [src/README.md](src/README.md)

---

## 💻 Tech Stack & Environment

* **Language**: Python 3.14+ with strict type hints.
* **Environment**: Local `.venv` virtual environment at `.venv/`.
* **Frameworks**: `langchain`, `langgraph`, `pydantic` (v2), `python-dotenv`.
* **Configuration**: Environment variables loaded via `.env` (`.env.example` as template).

---

## 🏗️ Architecture & Code Conventions

1. **Type Safety & Schemas**:
   - Always use Pydantic `BaseModel` or `TypedDict` with `Field(description=...)` for LLM structured outputs and graph state schemas.
   - Use explicit Python type annotations for function arguments and return types.

2. **LangChain & LangGraph Abstractions**:
   - **LCEL Chains**: Compose pipelines using LCEL syntax (`prompt | structured_model`).
   - **LangGraph State**: Use explicit typed State definitions for graph nodes. Keep state updates functional (returning partial state updates).
   - **Tool Calling**: Decorate tools with `@tool` and provide clean docstrings and typed arguments.

3. **Code Organization**:
   - Place application code inside `src/code_review_agent/` following modular package layout (`schemas/`, `chains/`, `tools/`, `graph/`, `rag/`).
   - Maintain production-quality code structure and naming conventions rather than stage-specific script folders.

4. **Environment Execution**:
   - Always run Python commands within the project `.venv` session:
     ```powershell
     .\.venv\Scripts\Activate.ps1
     ```

---

## 📋 Agent Behavior & Rules

* **Progress Tracking**: Whenever a task, step, or subtask from the roadmap is completed, immediately update [docs/progress.md](docs/progress.md) by marking the corresponding checklist item as completed (`[x]`).
* **Progress Alignment**: Cross-reference [docs/roadmap.md](docs/roadmap.md) to ensure implementation matches planned goals and keep [docs/progress.md](docs/progress.md) in sync.
* **Secrets Handling**: Never commit or hardcode API keys. Always load keys via `dotenv`.
* **Explanations**: Draw analogies to .NET / C# backend concepts (e.g., LCEL as middleware pipelines, LangGraph state as aggregate roots / saga state) to align with developer context.
