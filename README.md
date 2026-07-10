# Meta-Agent

An AI "agent that builds agents" — describe the CX bot you want in plain English, and Meta-Agent generates a complete, structured, deployable configuration for it.

## Overview

Meta-Agent is a meta-level LLM tool: instead of manually designing a customer experience (CX) phone/chat bot — writing its persona, greeting, conversation flow, and tool schemas by hand — you describe what you need in a single sentence (e.g. *"Create a bot for a gym that books personal training sessions"*), and Meta-Agent uses an LLM (via Groq's `llama-3.3-70b-versatile`) to generate a full, validated agent configuration as structured JSON, ready to be plugged into a voice/chat platform.

## Tech Stack

- **Language:** Python
- **LLM Provider:** [Groq](https://groq.com/) (OpenAI-compatible API), model `llama-3.3-70b-versatile`
- **Validation:** Pydantic (schema-enforced structured output)
- **SDK:** `openai` Python client (pointed at Groq's endpoint)

## Features

- **Natural language → agent config** — describe a bot in one sentence, get a full configuration back
- **Strict JSON schema validation** — every generated config is validated against a Pydantic model (`CXAgentConfig`) before being trusted
- **Structured conversation design** — auto-generates:
  - Agent name & detailed persona
  - Recommended voice style
  - Opening greeting line
  - Step-by-step conversation flow
  - Callable tools/functions with full JSON-schema parameters
- **Deployable output** — saves the generated config as `deployed_agent.json`, ready to feed into a CX/voice bot runtime

## Architecture

```
User description (CLI input)
        │
        ▼
 SYSTEM_PROMPT (Meta-Agent Architect role)
        │
        ▼
   Groq API (llama-3.3-70b-versatile)
   — forced JSON response format —
        │
        ▼
 CXAgentConfig (Pydantic model validation)
        │
        ▼
  deployed_agent.json (saved to disk)
```

**Generated config includes:**
```
agent_name   → e.g. "Return Assistant"
persona      → detailed personality & instructions
voice_type   → e.g. "Friendly and Professional"
greeting     → first line the bot speaks
steps        → ordered conversation stages
tools        → [{ name, description, parameters (JSON schema) }]
```


## Setup & Installation

1. Clone this repo:
   ```bash
   git clone https://github.com/Shriya-2701/Meta-Agent.git
   cd Meta-Agent
   ```
2. Install dependencies:
   ```bash
   pip install openai pydantic
   ```
3. Get a free API key from [Groq Console](https://console.groq.com/) and set it as an environment variable (**do not hardcode it in the source**):
   ```bash
   export GROQ_API_KEY="your-key-here"
   ```
4. Update `meta_agent.py` to read the key from the environment instead of a hardcoded string:
   ```python
   import os
   GROQ_API_KEY = os.environ["GROQ_API_KEY"]

   client = OpenAI(
       base_url="https://api.groq.com/openai/v1",
       api_key=GROQ_API_KEY
   )
   ```
5. Run it:
   ```bash
   python main.py
   ```
6. When prompted, describe the agent you want (e.g. `Create a bot for a gym that books personal training sessions`). The generated config prints to console and saves to `deployed_agent.json`.

## Folder Structure

```
Meta-Agent-main/
├── main.py               # CLI entry point — takes user description, runs the pipeline
├── meta_agent.py         # Core logic — system prompt, Groq API call, JSON parsing
├── models.py             # Pydantic schema (CXAgentConfig, ToolDefinition)
└── deployed_agent.json   # Example output — a generated agent config
```

## Key Learnings / Challenges

- Using structured/forced JSON output (`response_format={"type": "json_object"}`) from an open-weight model served via Groq, since Groq doesn't yet support OpenAI's stricter `.parse()`/function-calling schema enforcement — validating the raw JSON string against a Pydantic model afterward as a safety net.
- Designing a system prompt that reliably makes an LLM act as a "meta" architect — generating structured specifications *for another agent* rather than answering directly.
- Modeling a reusable, tool-calling-ready agent schema (persona, conversation steps, callable tools with JSON-schema parameters) that could plug into a real CX/voice bot platform.
- **Security lesson:** learned the hard way not to hardcode API keys in source files — moved to environment-variable based config to keep secrets out of version control.
