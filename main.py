import os
from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from resume_parser import extract_text_from_pdf
from question_generator import generate_questions, suggest_improvements
from dotenv import load_dotenv
import google.generativeai as genai 
import traceback 

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Configure Google Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load template configuration
templates = Jinja2Templates(directory="templates")

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Homepage route
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Upload + question generation + suggestions
@app.post("/generate-questions/", response_class=HTMLResponse)
async def generate_questions_endpoint(
    request: Request, 
    file: UploadFile = File(...), 
    job_role: str = Form(...)
):
    try:
        # Read uploaded resume
        pdf_bytes = await file.read()

        # Extract text from the PDF
        resume_text = extract_text_from_pdf(pdf_bytes)

        # Debug (optional)
        print("✅ Job Role:", job_role)
        print("✅ Resume Text (preview):", resume_text[:300])

        # Generate questions & suggestions
        questions = generate_questions(resume_text, job_role)
        suggestions = suggest_improvements(resume_text, job_role)

        # Check if questions generated
        if not questions:
            questions = ["No questions generated. Please try again."]

        # Render response
        return templates.TemplateResponse("index.html", {
            "request": request,
            "questions": questions,
            "suggestions": suggestions
        })

    except Exception as e:
        print("❌ Error:", e)
        traceback.print_exc()
        return templates.TemplateResponse("index.html", {
            "request": request,
            "questions": ["An error occurred while processing your request."],
            "suggestions": []
        })
