"""Agent 2: Compliance Reviewer — checks document against specs and flags issues."""
import os, json
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

SYSTEM_PROMPT = """You are an expert document reviewer. Your job is to:
1. Read the submitted document carefully
2. Check for compliance issues, missing information, and discrepancies
3. Return a JSON array of issues, each with: id, severity (CRITICAL/MINOR), description, reference

Be specific. Cite section numbers, code references, or spec clauses where applicable."""


def review_document(parsed: dict) -> dict:
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Review this document:\n\n{parsed['full_text'][:8000]}"}
        ],
        response_format={"type": "json_object"},
        temperature=0.1
    )
    issues = json.loads(resp.choices[0].message.content).get("issues", [])
    parsed["issues"] = issues
    parsed["critical_count"] = sum(1 for i in issues if i.get("severity") == "CRITICAL")
    parsed["minor_count"] = sum(1 for i in issues if i.get("severity") == "MINOR")
    return parsed
