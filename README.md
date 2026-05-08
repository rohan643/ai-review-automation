<div align="center">

# 🔁 AI Review Automation

**AI agents that automate document review workflows for engineering firms — built for Walter P Moore ($600M+ revenue).**

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com)
[![LangChain](https://img.shields.io/badge/LangChain-Agents-1C3C3C?style=for-the-badge)](https://langchain.com)
[![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)

</div>

---

## Background

Walter P Moore is a global engineering firm with $600M+ in revenue. Their internal review process for engineering documents — submittals, RFIs, design packages — required senior engineers to manually read, annotate, and route hundreds of documents per week.

This system deploys AI agents to handle the first pass of every document: parsing content, flagging issues, generating annotations, and routing to the right reviewer based on document type and discipline. Senior engineers spend time on judgment calls, not document wrangling.

---

## What the System Does

```
Document Submitted (PDF, DOCX, or via SharePoint)
         │
         ▼
┌──────────────────────────────┐
│  Document Ingestion          │  ← Extracts text, tables, drawings metadata
│  & Classification            │    Identifies document type:
│                              │    Submittal / RFI / Drawing / Spec / Report
└─────────────┬────────────────┘
              │
              ▼
┌──────────────────────────────┐
│  AI Review Agent             │  ← GPT-4o reads the document against:
│  (First Pass)                │    • Project specifications
│                              │    • Engineering standards (IBC, ACI, AISC)
│                              │    • Prior approved submittals
│                              │    • Client-specific requirements
└─────────────┬────────────────┘
              │
              ▼
┌──────────────────────────────┐
│  Issue Flagging              │  ← Agent outputs structured list of:
│  & Annotation                │    • Non-compliances (with code reference)
│                              │    • Missing information
│                              │    • Discrepancies vs. contract documents
│                              │    • Items needing engineer judgment
└─────────────┬────────────────┘
              │
              ▼
┌──────────────────────────────┐
│  Smart Routing               │  ← Routes to correct discipline lead
│                              │    (structural, MEP, civil, etc.)
│                              │    with priority score and estimated review time
└─────────────┬────────────────┘
              │
              ▼
┌──────────────────────────────┐
│  Review Report Generation    │  ← Produces draft review letter/stamp
│                              │    for engineer to finalize and sign off
│                              │    (Approve / Revise & Resubmit / Rejected)
└──────────────────────────────┘
```

---

## AI Agent Architecture

Three specialized agents work in sequence:

```python
# Agent 1: Document Parser
parser_agent = Agent(
    role="Document Intelligence",
    task="Extract all structured information from the document — specs, dimensions, materials, references, approval stamps, revision history.",
    tools=[PDFExtractor, TableParser, DrawingMetadataExtractor],
    model="gpt-4o"
)

# Agent 2: Compliance Reviewer
review_agent = Agent(
    role="Engineering Compliance Analyst",
    task="Compare document content against project specifications, applicable codes, and prior approved documents. Flag every discrepancy with a specific reference.",
    tools=[SpecsRetriever, CodeReferenceDB, ProjectDocumentRAG],
    model="gpt-4o",
    context=parser_agent.output
)

# Agent 3: Report Writer
report_agent = Agent(
    role="Review Report Author",
    task="Produce a structured review report in the firm's standard format. Include disposition recommendation and all flagged items with code references.",
    tools=[ReportTemplateWriter, DocumentStamper],
    model="gpt-4o",
    context=review_agent.output
)
```

---

## RAG Knowledge Base

The review agent queries a vector database of:

```
Project Documents (per-project, scoped):
├── Contract drawings
├── Project specifications (all sections)
├── Approved submittal log
├── RFI log and responses
└── Meeting minutes with engineering decisions

Standards Library (firm-wide):
├── IBC 2021
├── ACI 318-19
├── AISC Steel Construction Manual
├── ASCE 7-22
└── Client-specific design standards
```

```python
retriever = PineconeRetriever(
    index="wpm-project-docs",
    namespace=project_id,   # scoped per project — no cross-project leakage
    top_k=12,
    score_threshold=0.75
)
```

---

## Review Report Output (Sample)

```
DOCUMENT REVIEW — AI FIRST PASS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Project:        Midtown Tower — Phase 2
Document:       Submittal 07-4210-001 Rev C
                Structural Steel — Column Schedule
Submitted by:   Acme Fabricators
Review date:    2026-05-07
AI Disposition: REVISE AND RESUBMIT (2 critical, 3 minor)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CRITICAL ITEMS (require resolution before approval)

[C-01] Column C-14 base plate thickness specified as 1" — contract 
drawings (S-301 Rev 5) require 1.5" minimum per AISC Design Guide 1.
Revise column schedule accordingly.

[C-02] Weld size at beam-to-column connection (grid C/5) shown as 
5/16" fillet. Per spec section 05 12 00 para 2.4, minimum weld size 
for this connection is 3/8" per AISC 360-22 Table J2.4.

MINOR ITEMS (provide written response or revise)

[M-01] Shop primer specification does not match spec section 09 91 00.
[M-02] Mill certification references not included for HSS members.
[M-03] Camber requirements missing on W18×97 beams per Structural Notes.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  Requires engineer review before final disposition.
    Estimated engineer time: 15–20 minutes.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Impact

```
Before: Senior engineers spend 2–4 hours on first-pass reviews
After:  AI handles first pass in 3–7 minutes; engineer reviews output

Time saved per document:   60–90%
Documents processed/week:  200–400
Issues caught by AI:       ~85% match rate with manual review
False positive rate:        < 8% (flagged but not actual issues)
Engineer focus:             Judgment calls only, not document wrangling
```

---

## Tech Stack

| Component | Technology |
|---|---|
| Agent Orchestration | LangChain + custom orchestrator |
| LLM | OpenAI GPT-4o |
| Document Parsing | PyMuPDF + python-docx + pdfplumber |
| Vector Database | Pinecone |
| Embeddings | OpenAI text-embedding-3-large |
| API Layer | FastAPI |
| Document Storage | SharePoint (via Microsoft Graph API) |
| Output | Python-docx (report generation) |

---

<div align="center">

**Built by [Rohan Mukherjee](https://github.com/rohan643)**

*Deployed for Walter P Moore — $600M+ revenue global engineering firm*

</div>
