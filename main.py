"""
main.py
--------
FastAPI application for EduGenie. Serves the HTML frontend and
exposes the five endpoints described in the project doc:
  /qa                     - question answering
  /explain                - concept explanation
  /quiz                   - MCQ generation
  /summarize              - passage summarization
  /learn/recommendations  - personalized learning path
"""

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from qna import answer_question
from explanation_module import explain_concept
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations

app = FastAPI(title="EduGenie", description="Gemini-powered learning assistant")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/qa")
async def qa_endpoint(text: str = Form(...)):
    return JSONResponse({"result": answer_question(text)})


@app.post("/explain")
async def explain_endpoint(text: str = Form(...)):
    return JSONResponse({"result": explain_concept(text)})


@app.post("/quiz")
async def quiz_endpoint(text: str = Form(...)):
    result = generate_quiz(text)
    return JSONResponse({"result": result})


@app.post("/summarize")
async def summarize_endpoint(text: str = Form(...)):
    return JSONResponse({"result": summarize_text(text)})


@app.post("/learn/recommendations")
async def learning_path_endpoint(text: str = Form(...)):
    return JSONResponse({"result": get_learning_recommendations(text)})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
