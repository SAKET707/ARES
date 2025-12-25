# **ARES : Agent for Repository Exploration & Structured Analysis**

ARES is a deterministic, tool-driven GitHub repository intelligence system.  
It enables structured exploration and inspection of software repositories through a clean chat interface, without hallucination, hidden memory, or speculative reasoning.

ARES prioritizes **correctness, transparency, and reproducibility** over generative creativity.

---
## **STREAMLIT DEMO**
- https://ares-by-saket.streamlit.app/
---

## What ARES Does

ARES allows you to:

- Explore repository structure (tree view)
- Read and inspect source files
- Explain code strictly from actual source content
- Analyze code metrics (Python)
- Inspect imports and dependencies
- View repository metadata and owner information
- Generate repository summaries based on README and structure

If something is not present in the repository, ARES explicitly states that.

---

## Design Principles

- No hallucination  
- No long-term or hidden memory  
- Deterministic intent routing  
- Explicit tool usage  
- Clear separation of responsibilities    

ARES is intentionally conservative by design.

---

##  Architecture

ARES follows a **dual-agent architecture**:

### Agent A - Leader / Router
- Classifies user intent
- Extracts entities (file names, line ranges)
- Routes requests deterministically
- Does **not** read or reason about code

### Agent B - Code / Technical Agent
- Reads file content
- Explains code strictly from source
- Computes metrics and dependencies
- Makes no assumptions beyond visible code

This separation enforces clean reasoning boundaries and prevents hallucination.

---

##  Project Structure

```text
ARES/
├── .gitignore
├── LICENSE
├── README.md
├── agents/
│   ├── __init__.py
│   ├── agent_a.py
│   └── agent_b.py
├── app.py
├── assets/
│   ├── __init__.py
│   ├── agent.png
│   └── user.png
├── config/
│   ├── __init__.py
│   ├── prompts.py
│   └── settings.py
├── intents/
│   ├── __init__.py
│   └── classifier.py
├── requirements.txt
├── storage/
│   ├── __init__.py
│   ├── file_cache.py
│   └── session_cache.py
├── tools/
│   ├── __init__.py
│   ├── code_tools.py
│   ├── dependency_tools.py
│   ├── file_tools.py
│   └── repo_tools.py
└── utils/
    ├── __init__.py
    ├── formatting.py
    ├── github_client.py
    └── language_utils.py
```

---
## User Interface

ARES uses **Streamlit** to provide:

- Chat-style interaction (user ↔ agent)
- Scrollable conversation history
- No persistent memory between sessions
- Repository selection via GitHub username
- Session reset functionality
- Visual avatars for user and agent

---

##  Demo Walkthrough

<div align="center">

  <div style="display: flex; justify-content: center; gap: 40px; flex-wrap: wrap;">
    <img src="https://github.com/user-attachments/assets/0ea4d555-953a-450f-b3b8-9d87f893393d" alt="ARES demo 1" width="400" />
    <img src="https://github.com/user-attachments/assets/c796d734-7bb0-4696-a4b0-a8b69e6c42fa" alt="ARES demo 2" width="400" />
  </div>

  <br/><br/>

  <div style="display: flex; justify-content: center; gap: 40px; flex-wrap: wrap;">
    <img src="https://github.com/user-attachments/assets/9ad490ce-edf5-4379-b1c9-48351b109aff" alt="ARES demo 3" width="400" />
    <img src="https://github.com/user-attachments/assets/6ce8c326-af47-46ff-b42a-e754f0cec9c0" alt="ARES demo 4" width="400" />
  </div>

</div>

> **Credit & Attribution**  
> The repositories showcased in the above demonstration belong to their respective original owners.  
>  
> Repositories referenced:  
> - https://github.com/SAKET707/RETRIEVIST  
> - https://github.com/SAKET707/ARES  
>  
> This project analyzes only publicly available information and is intended strictly for educational and demonstration purposes.

---

## Tech Stack
- Python 3.11.9
- Streamlit 
- Groq
- Agno
- PyGitHub
- Pydantic
- Tree-sitter
- FAISS (optional / future use)

---
## Future Improvements

- Multi-language static analysis support beyond Python  
- Fine-grained diff analysis between repository versions and commits  
- Pluggable tool system for custom analyzers and organization-specific rules  
- Optional local indexing for faster repeated repository inspection  
