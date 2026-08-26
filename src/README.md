# Source Code Directory

Source code is organized as a production Python package inside `src/code_review_agent/`:

```text
code_review_agent/
├── __init__.py
├── config.py           # Model initialization & environment setup
├── schemas/            # Pydantic schemas (ReviewFinding, ReviewReport, State)
├── chains/             # Single-pass LCEL review pipelines
├── tools/              # Custom LangChain tools (git diff, static analyzers)
├── graph/              # LangGraph nodes, state definitions, conditional edges
├── rag/                # Vector store indexer & retriever logic
└── main.py             # CLI / execution entry point
```

This clean modular layout mirrors production architecture standards rather than stage-specific playground folders.
