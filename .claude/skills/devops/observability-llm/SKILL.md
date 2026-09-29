---
name: observability-llm
description: "LLM observability with Langfuse/LangSmith"
category: devops
tags: [observability, llm, langfuse, langsmith, tracing, monitoring]
models: [sonnet, opus]
version: 1.0.0
created: 2026-05-14
updated: 2026-09-29
---
# LLM Observability

> Monitor, trace, and debug LLM applications with Langfuse and LangSmith.

## Quick Start
```python
# Langfuse — LLM observability platform
from langfuse import Langfuse
from langfuse.decorators import observe, langfuse_context

langfuse = Langfuse(
    secret_key="sk-lf-...",
    public_key="pk-lf-..."
)

@observe(name="rag-query", as_type="generation")
def rag_query(question: str, context: str) -> str:
    # Automatically traces token usage, latency, and metadata
    langfuse_context.update_current_generation(
        input=question,
        output="generated answer",
        usage={"promptTokens": 150, "completionTokens": 80, "totalTokens": 230},
        metadata={"retrieved_docs": 3, "model": "claude-sonnet-4"}
    )
    return "Generated answer"

# Manual tracing
trace = langfuse.trace(name="document-pipeline")
span = trace.span(name="embedding-generation")
span.end()
trace.update(
    input={"query": "user question"},
    output={"answer": "AI response"}
)
```

```python
# LangSmith — LangChain observability
from langsmith import Client
from langchain.callbacks.tracers import LangSmithTracer

# Environment setup
import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "ls-..."
os.environ["LANGCHAIN_PROJECT"] = "my-llm-app"

# Automatic tracing with callback
tracer = LangSmithTracer()
llm.invoke("Hello", config={"callbacks": [tracer]})
```

## Key Concepts
Trace every LLM call with latency, tokens, cost, and metadata. Track prompt versions, model parameters, and retrieval context. Debug with full trace visualization. Set up monitoring for cost alerts and quality metrics.

## When to Use
- Production LLM applications needing debugging
- Tracking token usage and costs across teams
- A/B testing prompt variations
- Monitoring response quality and latency regressions

## Step-by-Step
1. Install: `pip install langfuse` and set env keys `LANGFUSE_PUBLIC_KEY`/`LANGFUSE_SECRET_KEY`.
2. Add decorators: wrap your generation/RAG functions with `@observe` so the SDK traces latency, tokens, and metadata.
3. Add context: capture input/output, usage dict, and retrieval metadata (doc ids, model name, versions).
4. Build dashboards: use Langfuse/LangSmith views to group by session, project, or prompt version.
5. Set monitoring: alerts for cost spikes, latency regressions, and error rates per prompt/model.
6. Iterate on prompts: use trace comparison and prompt playground to A/B versions and pin winners.

## Examples
```python
# Trace a full RAG pipeline as nested spans
from langfuse.decorators import observe, langfuse_context

@observe(name="retrieve")
def retrieve(query: str) -> list[str]:
    return ["doc-1", "doc-2"]  # from your vector store

@observe(name="generate")
def generate(query: str, docs: list[str]) -> str:
    langfuse_context.update_current_generation(
        input=query,
        output="answer text",
        usage={"promptTokens": 120, "completionTokens": 40, "totalTokens": 160},
        metadata={"docs": docs, "model": "claude-sonnet-4"},
    )
    return "answer text"

@observe(name="rag")
def rag(question: str) -> str:
    docs = retrieve(question)
    return generate(question, docs)
```
```bash
# Export traces for offline analysis
python -m langfuse export-json --project your-project --output ./traces.json
# or use the CLI dashboard
langfuse-compose up    # self-hosted Langfuse stack
```

## Validation
1. Traces appear in Langfuse/LangSmith dashboard
2. Token usage and costs are accurately tracked
3. Latency breakdown shows where time is spent
4. Search and filter by metadata/tags works correctly
