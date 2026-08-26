# Learning LangChain & LangGraph Through a Real Project

*A structured path from a .NET/backend engineering background to designing real-world agentic workflows.*

---

## What Makes a Project Good for Learning LangChain + LangGraph

Most "LangChain tutorial projects" fail to actually teach the framework. Here's the filter used to evaluate every candidate below:

1. **The workflow has real branching, not just sequential steps.** If step 2 always follows step 1 with no decision point, you don't need a graph — a plain chain (or a Python function) does the job. LangGraph earns its keep when the *next step depends on the outcome of the current one* — that's conditional edges, and it's the single most important LangGraph concept to internalize.

2. **There's a reason for state to persist and evolve, not just get passed through.** A DTO that flows through 3 function calls unchanged isn't "state" in the interesting sense. You want a project where the state accumulates evidence, gets revised, and different nodes read/write different slices of it — closer to an aggregate that accrues events than a stateless request/response payload.

3. **Something can legitimately fail or be uncertain**, so retries, self-correction loops, and human approval have a real job to do — not because you inserted a "confirm?" step for the sake of demonstrating the concept.

4. **There's more than one *kind* of reasoning needed** — e.g., "search the web" is a different competency than "critique this draft for factual accuracy," which is different again from "format this into a report." That's what makes multi-agent decomposition natural instead of cosplay. If one well-prompted agent could do the whole thing, splitting it into 4 agents is just overhead.

5. **Retrieval is answering a real question, not decorating the prompt.** RAG is worth including only if there's a corpus too large/dynamic to stuff in a prompt and where retrieval quality genuinely changes output quality — not "let's add a vector DB because it's on the list."

6. **It produces an artifact or decision with consequences**, so structured output (Pydantic schemas) and evaluation matter — a project that only produces prose has nothing to grade or validate against.

Every candidate below is judged against these six filters, not against "does it technically use the SDK."

---

## Candidate Projects

### 1. AI Code Review & Refactoring Agent

**Real-world problem:** Automate first-pass PR review — catch security issues, style violations, architectural smells, missing tests — before a human reviewer spends time on it.

**Why it's a good learning project:** A diff naturally requires *different kinds* of judgment (security ≠ style ≠ architecture), the codebase is too large to fit in context (real RAG need), review suggestions have real cost if wrong (real need for human approval), and you already have deep domain expertise to judge whether the agent's output is actually good.

**What you'd actually do:** Point it at a local git repo, feed it a diff or PR, get back a structured review with categorized findings, approve/reject/edit each finding, and have it post final comments (or just print them, in v1).

**Where LangChain is used:** Prompt templates, structured output parsing (Pydantic schemas for `ReviewFinding`), tool wrappers (run `git diff`, run a linter, run tests), the retriever interface for the vector store.

**Where LangGraph is used:** The whole orchestration — route to specialist nodes based on which files changed, loop the review through a self-critique node until confidence is high enough, checkpoint before human approval, fan out to parallel specialist agents and fan back in.

**Tools the agents need:** `git diff` reader, file reader, a linter/static analyzer (e.g., `dotnet format`/Roslyn analyzers for C#, or `ruff`/`eslint` for language-agnostic), test runner, vector search over the repo.

**RAG involved:** Yes — retrieving relevant existing code, coding standards docs, and prior review comments to ground suggestions instead of hallucinating conventions.

**Human-in-the-loop:** Yes — approve findings before "posting," edit severity, reject false positives. Natural home for LangGraph's `interrupt`.

**State/persistence:** Yes — a review session is a multi-step, resumable workflow (PR arrives → analysis in progress → awaiting human approval → posted). Perfect fit for a checkpointer.

**Multi-agent architecture:** Yes, and it's earned — Security Reviewer, Style Reviewer, Architecture Reviewer are genuinely different lenses, run in parallel, aggregated by a supervisor.

**Estimated difficulty:** Medium → Medium-High as you add stages. Manageable to MVP fast.

**Concepts you'd learn:** Tool calling, structured output, conditional routing, RAG, parallel execution (map-reduce over specialists), retries (tool failures), self-correction loops, human-in-the-loop interrupts, checkpointing/persistence, multi-agent supervisor pattern, evaluation, observability.

**MVP:** Single agent, single node, takes a diff, returns a structured list of findings using one prompt. No graph yet.

**Path to production-grade:** Caching of repeated file analyses, cost/token budget management, CI integration (GitHub Action), a proper eval suite with regression testing on past PRs, streaming output, async parallel tool calls, feedback loop where rejected findings retrain prompts/few-shot examples.

---

### 2. Autonomous Research & Report Writer ("Deep Research" clone)

**Real-world problem:** Given a topic, produce a structured, cited report.

**Why it's a good learning project:** Naturally decomposes into plan → parallel search → synthesize → critique → revise — the canonical LangGraph shape. Long-running (minutes), so checkpointing/resumability matters for real reasons.

**What you'd actually do:** Give it a research question, review its generated sub-question plan (approve/edit it before burning API calls), watch it search in parallel, get a cited report, send weak sections back for revision.

**Where LangChain is used:** Web search tool wrappers, prompt templates for planning/synthesis/critique, structured output for the research plan and citations.

**Where LangGraph is used:** Plan node → parallel search branches → merge node → draft node → critique node → conditional loop back to research-more-or-finalize.

**Tools the agents need:** Web search API (Tavily/Bing/etc.), a scraper/fetch tool, optionally a calculator or code execution tool.

**RAG involved:** Yes, in a specific form — retrieval over documents *gathered during the run* (dynamic/ephemeral RAG, not a static index).

**Human-in-the-loop:** Yes — approving the research plan before execution is a valuable, cost-saving checkpoint.

**State/persistence:** Yes — long-running jobs, resumable across a crash, checkpointed after each expensive phase.

**Multi-agent architecture:** Optional but natural — a "critic" agent adversarial to the "writer" agent is a clean, teachable pattern.

**Estimated difficulty:** Medium-High. The parallel fan-out/fan-in and iterative critique loop are the trickiest LangGraph patterns in this whole set.

**Concepts you'd learn:** Planning/decomposition, parallel execution, structured output (citations schema), loops with exit conditions, human approval of a plan, persistence for long jobs, critic/writer multi-agent pattern, evaluation of report quality.

**MVP:** No planning, no parallelism — one search call, one synthesis call, return report.

**Path to production-grade:** Source credibility scoring, deduplication across parallel searches, streaming partial results, cost caps per run, citation-verification step.

---

### 3. Multi-Agent Customer Support Ticket System

**Real-world problem:** Triage and resolve support tickets — classify, answer from a knowledge base, or escalate/execute actions (refund, reset, etc.) — with clear human oversight for anything risky.

**Why it's a good learning project:** Textbook "supervisor + specialist agents" architecture, fully self-contained (synthetic tickets, no external system required). Maps cleanly onto DDD/CQRS instincts — a ticket is basically an aggregate moving through states; specialist agents are like command handlers.

**What you'd actually do:** Feed it a synthetic ticket, watch it classify and route, see a specialist agent draft a resolution (RAG-grounded KB answers), approve any action above a risk threshold before it "executes."

**Where LangChain is used:** Classification via structured output, prompt templates per specialist, retriever for the KB.

**Where LangGraph is used:** Supervisor node routes to Billing/Technical/Refunds specialist nodes (conditional edges keyed on classification), escalation path to a human-approval interrupt, state carries the ticket + conversation history across the whole graph.

**Tools the agents need:** Mock "backend" tools you write yourself (`get_order`, `issue_refund`, `reset_password`) — a great place to practice tool calling against your own fake API.

**RAG involved:** Yes — a support KB (write ~30-50 markdown docs) the Technical agent retrieves from.

**Human-in-the-loop:** Yes, meaningfully risk-tiered — great for learning *conditional* human-in-the-loop (only interrupt above a threshold), not just always-interrupt.

**State/persistence:** Yes — tickets are long-lived, multi-turn, need to resume.

**Multi-agent architecture:** Yes — the cleanest "supervisor pattern" of all the candidates.

**Estimated difficulty:** Medium. Slightly less conceptually deep than #1 or #2 — less ambiguity in the domain.

**Concepts you'd learn:** Supervisor/router pattern, conditional edges, tool calling against mock APIs, RAG, risk-tiered human approval, persistence, state accumulation across multi-turn conversation.

**MVP:** One classifier + one generic responder, no routing yet.

**Path to production-grade:** Real ticketing system integration (Zendesk/Intercom API), SLA-aware prioritization, agent handoff to a live human with full context transfer, analytics/eval on resolution accuracy.

---

### 4. Natural-Language SQL Data Analyst Agent

**Real-world problem:** Let a non-technical user ask questions of a database in plain English and get correct answers/charts, safely.

**Why it's a good learning project:** You already deeply understand databases, so you can judge correctness immediately. Self-correction on SQL errors is a genuinely useful, non-contrived loop.

**What you'd actually do:** Stand up a local SQLite/Postgres with realistic sample data, ask questions, watch it generate SQL, execute, self-correct on error, render a chart or table.

**Where LangChain is used:** Schema-aware prompt construction, SQL generation with structured output, retriever for schema/column-description RAG.

**Where LangGraph is used:** Generate query → execute → (on error) retry-with-error-context loop → validate result shape → format output; conditional routing between chart vs. table.

**Tools the agents need:** SQL execution tool, schema introspection tool, charting tool.

**RAG involved:** Mild — retrieving schema descriptions/business glossary when the schema is large. Weakest RAG case of the set for a small DB.

**Human-in-the-loop:** Optional — natural fit for confirming destructive queries before execution.

**State/persistence:** Lighter than the others — mostly useful for multi-turn follow-ups.

**Multi-agent architecture:** Weakest fit — hard to justify more than 1-2 agents without forcing it.

**Estimated difficulty:** Low-Medium. Fastest to a satisfying MVP.

**Concepts you'd learn:** Tool calling, structured output, retry loops (a genuinely great teaching example), conditional routing, light RAG, light human-in-the-loop.

**MVP:** Question in, SQL out, execute, return raw result.

**Path to production-grade:** Query result caching, read-only sandboxing, row-level security awareness, natural-language explanations of results, chart type selection logic.

---

### 5. Resume / Job Application Tailoring Assistant

**Real-world problem:** Tailor a resume and cover letter to a specific job posting, with gap analysis.

**Why it's a good learning project:** Personally motivating, clean iterative-refinement loop with human feedback, structured output for gap analysis.

**Where LangGraph is used:** Extract requirements → compare against resume (structured gap analysis) → draft → human feedback loop → revise.

**RAG involved:** Yes, if you build an "achievement bank" the agent retrieves from — somewhat artificial unless your corpus is large enough.

**Human-in-the-loop:** Yes, central to the project.

**Multi-agent architecture:** Can justify Writer + ATS-Checker + Tone-Critic, but a stretch — one well-designed agent could do most of it.

**Estimated difficulty:** Low.

**Verdict:** Good side-project, weakest of the set for learning LangGraph specifically — too much complexity is prompt-engineering, not graph architecture. Fastest confidence-builder, not the deepest teacher.

---

### 6. Personal Finance Statement Analyzer Agent

**Real-world problem:** Ingest bank/credit card statement exports, categorize spending, flag anomalies, answer questions about your own finances.

**Why it's a good learning project:** Fully self-contained, real utility, decent anomaly-detection branching logic.

**Where LangGraph is used:** Categorize → detect anomalies (conditional branch) → clarify with user on ambiguous transactions (human-in-loop) → generate report.

**RAG involved:** Weak — unless you add a corpus of receipts/statements, which feels bolted-on.

**Multi-agent architecture:** Weak fit — one agent handles this comfortably.

**Estimated difficulty:** Low.

**Verdict:** Fine weekend project, but closest to "chatbot with structured output" — the least naturally graph-shaped. Included for completeness, not recommended.

---

## Ranking for This Learning Goal

| Rank | Project | Why |
|---|---|---|
| **1** | **AI Code Review & Refactoring Agent** | Hits all six filters hardest, and existing domain expertise lets you evaluate output quality while also learning the framework |
| **2** | Multi-Agent Customer Support System | Cleanest supervisor/routing pattern, fully self-contained, maps well to CQRS instincts |
| **3** | Autonomous Research & Report Writer | Best for parallel execution + long-running persistence, but hardest to get right and least tied to existing expertise |
| **4** | Natural-Language SQL Analyst | Fastest MVP, great retry-loop teaching example, but thin on RAG and multi-agent |
| **5** | Resume Tailoring Assistant | Motivating but conceptually shallow for LangGraph specifically |
| **6** | Personal Finance Analyzer | Weakest graph-shape of the set |

---

## Recommendation: AI Code Review & Refactoring Agent

Three reasons this beats the others for this specific background:

1. **Correctness can be judged without learning a new domain first.** With the research writer or support system, you'd be evaluating "is this a good research report / good ticket resolution" *while also* learning LangGraph — two unknowns at once. With code review, you already know what a good review looks like, freeing all cognitive effort for the framework.

2. **Every concept on the list shows up because the domain demands it, not because the project was designed to hit a checklist.** Security review really is a different reasoning task than style review. A diff really is too large for context sometimes, hence real RAG. A false-positive finding really does have a cost, hence real human approval. Nothing here is decorative.

3. **It's directly useful in an actual engineering job**, which means continued iteration past the "tutorial project" finish line — and continued use is where the deepest learning happens, well after the roadmap ends.

---

## Build Roadmap

Each stage should take you from "it runs" to "I understand *why* this is architected this way, and what breaks if I remove this piece." Where a new term is introduced, there's a .NET-side handle to anchor it to.

### Stage 0 — Foundations, no graph yet
**Goal:** Understand LangChain's core abstractions before adding orchestration.

- Set up a Python env, get a working call to an LLM through LangChain's chat model wrapper (think: a typed HTTP client, comparable to a generated OpenAPI client — not magic).
- Learn **prompt templates** (parameterized prompt strings — like a Razor/string template, nothing more).
- Learn **structured output**: define a Pydantic model (`class ReviewFinding(BaseModel): ...`) and have the LLM return validated JSON matching it — the backbone of everything downstream. Think of it as deserializing an HTTP response into a C# record, except the "server" is a language model and its output shape is constrained via schema.
- **LCEL** (LangChain Expression Language) — chaining `prompt | model | parser` with the `|` operator. Just function composition — think middleware pipeline in ASP.NET Core, minus the graph structure (no branching yet).

**Deliverable:** A script that takes a hardcoded diff string and returns one structured `ReviewFinding` list. No files read, no tools, no graph.

### Stage 1 — Tool calling
**Goal:** Let the LLM call functions instead of you hardcoding inputs.

- Write a real tool: `read_git_diff()` that shells out to `git diff`. Learn the `@tool` decorator / tool schemas — this is dependency injection of a *capability* into the model: you're not giving it data, you're giving it a function it can decide to invoke, with arguments it decides on, based on a schema you define (similar to exposing a method via an interface and letting something else decide when to call it).
- Bind the tool to the model, run a simple **ReAct loop** (model decides: call tool → observe result → maybe call another tool → respond). LangChain has helpers for this, but build one manually once so the loop isn't a black box: it's just a `while` loop around "call model, if it requested a tool, run the tool, feed the result back, repeat."

**Deliverable:** Agent that, given a repo path, decides on its own to fetch the diff, then produces findings.

### Stage 2 — Introduce LangGraph: state and nodes
**Goal:** Replace the implicit while-loop with an explicit state machine.

- Core mental model: **a graph is a state machine, where State is a typed object (a Pydantic model or TypedDict) that every node reads and writes to.** If you've built a saga/orchestrator with explicit steps and a shared context object passed through each step — this is that, formalized, with the framework managing the transitions instead of you hand-rolling them.
- **Nodes** = functions that take the current state, do something, return an update to the state (a single step/handler in a pipeline).
- **Edges** = the wiring between nodes (default: linear, A → B → C).
- Rebuild Stage 1's single agent as a 2-3 node graph: `fetch_diff` node → `generate_review` node → `format_output` node. Nothing conditional yet — the point is purely to get comfortable with `StateGraph`, `add_node`, `add_edge`, `compile()`.

**Deliverable:** Same functionality as Stage 1, now expressed as an explicit, inspectable graph.

### Stage 3 — Conditional routing
**Goal:** Make the graph actually branch based on data.

- Add a node that classifies which files changed (security-sensitive? test files only? docs only?), and use a **conditional edge** to route to different downstream nodes based on that classification — a `switch` statement / strategy pattern, but declared as graph structure instead of buried in an `if`.
- Add a "skip" path: docs-only changes route straight to trivial approval, skipping the expensive review nodes entirely. This is the first place you'll feel *why* graphs beat linear chains.

**Deliverable:** The graph takes different paths depending on what changed, visualized as a Mermaid diagram (genuinely useful for debugging — similar to visualizing a state machine diagram).

### Stage 4 — RAG
**Goal:** Ground reviews in real project context instead of the model guessing conventions.

- Index a small local repo into a vector store (Chroma is the easiest local option — no external service needed).
- Add a **retrieval node**: given the diff, pull relevant existing code / coding-standards docs, inject into the review prompt's context. This is where you'll learn embeddings, chunking strategy, and similarity search — treat the vector store as a specialized index (closer to a full-text search index than a database replacement).

**Deliverable:** Review quality visibly improves because the agent references actual project conventions instead of generic best practices.

### Stage 5 — Loops and retries
**Goal:** Let the graph recover from failure and self-improve.

- **Tool retry:** if the linter tool crashes or returns malformed output, route back to a retry node with backoff, capped at N attempts — an edge that points *backward* in the graph, the mechanic that makes loops possible.
- **Self-critique loop:** after generating findings, add a "critic" node that checks them for obvious hallucination/low confidence, conditionally routing back to regenerate — bounded by a max-iteration counter in state (same discipline as a retry policy with max attempts in Polly).

**Deliverable:** The graph recovers from a flaky tool call and iteratively improves a weak first-pass review.

### Stage 6 — Human-in-the-loop
**Goal:** Pause execution for a real human decision, and resume correctly.

- Learn `interrupt()` — pauses the graph mid-execution, returns control to your calling code, waits for external input before resuming from *exactly* that point. Closest .NET analogy: a long-running workflow engine (like Durable Functions' `WaitForExternalEvent`) — execution state is fully suspended and resumable.
- Insert an interrupt before "posting" findings: show them to the user, let them approve/edit/reject each one, resume the graph with that input incorporated into state.

**Deliverable:** A review run that genuinely pauses, waits, and resumes with human input — not a fake `input()` call.

### Stage 7 — Persistence / checkpointing
**Goal:** Make runs durable across process restarts, not just resumable within one process.

- Swap the in-memory checkpointer for a SQLite-backed one. Every state transition is now persisted — your event-store analogy: inspect the full history of a run, replay it, or resume a run interrupted hours ago after a process restart, keyed by a thread/session ID (comparable to an aggregate ID for rehydrating state in event sourcing).

**Deliverable:** Kill the process mid-review, restart it, resume from the human-approval interrupt with full state intact.

### Stage 8 — Multi-agent architecture
**Goal:** Split monolithic review generation into specialist subgraphs coordinated by a supervisor.

- Build Security Reviewer, Style Reviewer, and Architecture Reviewer as separate nodes (or subgraphs) with distinct prompts/tools, run them **in parallel** (fan-out) after routing, then an **aggregation node** merges their findings (fan-in) — map-reduce, and the first place you'll deal with concurrent writes to shared state via reducer functions (similar to merging concurrent event streams in a CQRS projection).

**Deliverable:** Three specialists genuinely running concurrently, results merged into one coherent report.

### Stage 9 — Evaluation & observability
**Goal:** Know whether changes make the agent better or worse, and see *why* it made a given decision.

- Build a small labeled test set (10-20 diffs with known "good" findings), score the agent's output against it (precision/recall on findings, or LLM-as-judge scoring) — your regression test suite, with fuzzier assertions than `Assert.Equal`.
- Add tracing (LangSmith, or structured logging of every node transition) to inspect exactly which retrieved documents, tool calls, and intermediate states led to a given finding — the debugging equivalent of distributed tracing/correlation IDs across a microservice call chain.

**Deliverable:** A repeatable eval run that gives a score, plus full visibility into any single run's execution path.

### Stage 10 — Production hardening
**Goal:** Turn the learning project into something trustworthy to run regularly.

- Async/streaming execution, per-run cost tracking and budget caps, caching of repeated file analyses, package as a CLI tool or GitHub Action, unit tests around individual nodes (each node is just a function — test it like one), formalize the eval suite as CI-gated regression testing before changing prompts.

---

*Start at Stage 0 even though it'll feel almost too simple — the temptation with a strong backend background is to jump straight to the graph. The graph will make far more sense once you've felt, in your hands, what a plain chain can't do.*
