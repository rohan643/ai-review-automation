"""AI Review Automation — FastAPI orchestrator."""
from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from agents.parser_agent import parse_document
from agents.review_agent import review_document
from agents.report_agent import generate_report
import tempfile, os

app = FastAPI(title="AI Review Automation")


@app.post("/review")
async def submit_review(file: UploadFile = File(...), bg: BackgroundTasks = BackgroundTasks()):
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    bg.add_task(run_review_pipeline, tmp_path, file.filename)
    return {"status": "queued", "filename": file.filename}


async def run_review_pipeline(path: str, filename: str):
    print(f"Processing: {filename}")
    parsed = parse_document(path)
    reviewed = review_document(parsed)
    report = generate_report(reviewed)
    print(f"Review complete: {report['disposition']} — {len(report['issues'])} issues")
    os.unlink(path)
