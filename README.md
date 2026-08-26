# AI Code Review & Refactoring Agent

> A structured, hands-on project to learn **LangChain** and **LangGraph** by building an AI-powered Code Review & Refactoring Agent.

---

## 📁 Project Structure

```text
personal/
├── docs/
│   ├── roadmap.md     # Learning roadmap & project candidates analysis
│   └── progress.md    # Step-by-step progress tracking checklist
├── src/
│   └── code_review_agent/  # Real production package layout
│       ├── schemas/        # Pydantic DTOs & structured output models
│       ├── chains/         # LCEL pipelines & prompt templates
│       ├── tools/          # Dynamic tool definitions (git diff, linters)
│       ├── graph/          # LangGraph state machine & nodes
│       ├── rag/            # Vector store retrieval engine
│       ├── config.py       # Configuration & LLM provider bindings
│       └── main.py         # Application entry point / CLI
├── .env.example       # Template for required environment variables
├── .gitignore         # Ignores virtualenv, secrets, and caches
└── README.md          # Project overview & navigation
```

---

## 📚 Documentation

* **[Learning Roadmap](docs/roadmap.md)**: Detailed evaluation filters, candidate projects, and stage-by-stage learning objectives tailored for backend/C# engineers.
* **[Progress Tracker](docs/progress.md)**: Interactive checklist tracking completion across all 10 implementation stages.

---

## 🚀 Quick Start

### 1. Create & Activate Virtual Environment

```powershell
# Create venv using direct Python path
& "C:\Users\kulbahadur.thapa\AppData\Local\Python\pythoncore-3.14-64\python.exe" -m venv .venv

# Activate venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install Dependencies

```powershell
pip install langchain langchain-nvidia-ai-endpoints pydantic python-dotenv
```

### 3. Environment Configuration

Copy `.env.example` to `.env` and configure your NVIDIA API key:

```env
NVIDIA_API_KEY=nvapi-your-key-here
```
