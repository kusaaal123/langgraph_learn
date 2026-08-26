# LangChain & LangGraph Learning Progress

Tracking progress for the **AI Code Review & Refactoring Agent** project roadmap.

---

## 📌 Progress Overview

- [x] Stage 0: Foundations (No graph yet)
- [x] Stage 1: Tool Calling
- [ ] Stage 2: LangGraph Basics (State & Nodes)
- [ ] Stage 3: Conditional Routing
- [ ] Stage 4: RAG (Retrieval-Augmented Generation)
- [ ] Stage 5: Loops & Retries
- [ ] Stage 6: Human-in-the-Loop
- [ ] Stage 7: Persistence & Checkpointing
- [ ] Stage 8: Multi-Agent Architecture
- [ ] Stage 9: Evaluation & Observability
- [ ] Stage 10: Production Hardening

---

## 🟢 Stage 0 — Foundations (No graph yet)
**Goal:** Understand LangChain's core abstractions before adding orchestration.

- [x] **0.1 Environment Setup:** Virtual environment (`.venv`) created and core packages installed (`langchain`, `langchain-nvidia-ai-endpoints`, `pydantic`, `python-dotenv`).
- [x] **0.2 Environment Config:** `.env` file configured with API keys (`NVIDIA_API_KEY`).
- [x] **0.3 Pydantic Schemas:** Defined `ReviewFinding` and `ReviewReport` structured output models.
- [x] **0.4 Prompt & Model Binding:** Built `ChatPromptTemplate` and applied `model.with_structured_output()`.
- [x] **0.5 LCEL Execution:** Constructed `prompt | model` pipeline and verified output on a hardcoded diff string.

---

## 🔵 Stage 1 — Tool Calling
**Goal:** Let the LLM call functions instead of hardcoding inputs.

- [x] **1.1 Tool Wrapper:** Created `@tool` function `read_git_diff()` that shells out to `git diff`.
- [x] **1.2 ReAct Loop:** Bound tool to model and implemented manual `while` loop to execute tool calls.
- [x] **1.3 Deliverable:** Agent fetches diff dynamically from repo path and produces findings.

---

## 🔵 Stage 2 — Introduce LangGraph: State and Nodes
**Goal:** Replace the implicit while-loop with an explicit state machine.

- [ ] **2.1 State Definition:** Defined typed `State` schema (`TypedDict` or Pydantic).
- [ ] **2.2 Graph Nodes:** Created `fetch_diff`, `generate_review`, and `format_output` node functions.
- [ ] **2.3 StateGraph Construction:** Wired nodes with linear edges in `StateGraph` and compiled workflow.

---

## 🔵 Stage 3 — Conditional Routing
**Goal:** Make the graph branch based on data.

- [ ] **3.1 File Classification:** Created node to classify modified files (security-sensitive, tests, docs).
- [ ] **3.2 Conditional Edges:** Added `add_conditional_edges()` logic for dynamic routing.
- [ ] **3.3 Fast Path:** Routed docs-only changes around heavy review nodes.

---

## 🔵 Stage 4 — RAG (Retrieval-Augmented Generation)
**Goal:** Ground reviews in project context using vector search.

- [ ] **4.1 Vector Store Setup:** Indexed local codebase/guidelines in ChromaDB with embeddings.
- [ ] **4.2 Retrieval Node:** Retrieved relevant code/standards and injected them into the review prompt context.

---

## 🔵 Stage 5 — Loops and Retries
**Goal:** Let the graph recover from failure and self-improve.

- [ ] **5.1 Tool Retry Edge:** Handled tool failures with backward edge and retry limit.
- [ ] **5.2 Self-Critique Loop:** Added critic node that checks findings and conditionally triggers revision.

---

## 🔵 Stage 6 — Human-in-the-Loop
**Goal:** Pause execution for human approval and resume.

- [ ] **6.1 Interrupts:** Added `interrupt()` call before posting findings to pause execution.
- [ ] **6.2 State Resume:** Updated state with user edits/approvals and resumed graph execution.

---

## 🔵 Stage 7 — Persistence & Checkpointing
**Goal:** Make runs durable across process restarts.

- [ ] **7.1 Checkpointer Setup:** Replaced in-memory checkpointer with SQLite checkpointer.
- [ ] **7.2 Workflow Resumption:** Tested process restart and state rehydration via thread ID.

---

## 🔵 Stage 8 — Multi-Agent Architecture
**Goal:** Split review generation into specialist subgraphs coordinated by a supervisor.

- [ ] **8.1 Specialist Nodes:** Created Security, Style, and Architecture reviewer specialists.
- [ ] **8.2 Map-Reduce Pattern:** Fanned out parallel specialist runs and aggregated results in a fan-in node.

---

## 🔵 Stage 9 — Evaluation & Observability
**Goal:** Measure quality and inspect execution traces.

- [ ] **9.1 Benchmark Dataset:** Created ground-truth dataset of diffs and expected findings.
- [ ] **9.2 Automated Eval:** Ran LLM-as-judge scoring for review precision and recall.
- [ ] **9.3 Tracing:** Integrated LangSmith or structured logging for full node transition visibility.

---

## 🔵 Stage 10 — Production Hardening
**Goal:** Prepare for regular production usage.

- [ ] **10.1 Streaming & Budgeting:** Added streaming outputs, token tracking, and cost caps.
- [ ] **10.2 CI / CLI Packaging:** Packaged workflow as CLI tool / GitHub Action with automated CI testing.
