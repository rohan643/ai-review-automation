# 🔁 AI Review Automation

Three AI agents that automate multi-step document review workflows. Built for high-volume engineering and legal document processing.

---

```
Document submitted
      │
      ▼
[Agent 1] Parser    — extracts all structured data
      │
      ▼
[Agent 2] Reviewer  — checks against specs, flags issues with references
      │
      ▼
[Agent 3] Reporter  — writes formal review report + disposition
      │
      ▼
Routed to correct reviewer with priority score
```

---

### Stack

```
Python 3.11  ·  LangChain  ·  OpenAI GPT-4o  ·  Pinecone  ·  FastAPI
PyMuPDF  ·  python-docx  ·  pdfplumber
```

### Files

```
ai-review-automation/
├── main.py                  # FastAPI app + orchestrator
├── agents/
│   ├── parser_agent.py      # Document ingestion + extraction
│   ├── review_agent.py      # Compliance check against RAG knowledge base
│   └── report_agent.py      # Formal review report generation
├── rag/
│   └── indexer.py           # Build/update Pinecone vector index
└── requirements.txt
```

### Run

```bash
pip install -r requirements.txt
uvicorn main:app --port 8000
# POST /review with multipart file upload
```

---

### Sample Output

```
DOCUMENT REVIEW — AI FIRST PASS
────────────────────────────────────────
AI Disposition: REVISE AND RESUBMIT
Critical items: 2
Minor items: 3
Estimated engineer review time: 15–20 min
────────────────────────────────────────
[C-01] Column base plate 1" — drawings require 1.5" min (AISC Guide 1)
[C-02] Weld size 5/16" — spec requires 3/8" min (AISC 360-22 J2.4)
```

---

<sub>[@rohan643](https://github.com/rohan643)</sub>
