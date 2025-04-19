import google.generativeai as genai
import os

# Initialize model using environment variable
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Model selection (you can modify this based on your needs)
model = genai.GenerativeModel("models/gemini-1.5-flash")

def generate_questions(resume_text, job_role):
    try:
        prompt = f"""
        You are an expert interviewer.
        Given this resume and job role, generate 5 personalized interview questions combining technical and behavioral topics.
        JOB ROLE: {job_role}
        RESUME:{resume_text}
        Only return numbered questions.
        """
        response = model.generate_content(prompt)
        
        # Extracting text from response and splitting by newlines
        questions = response.text.strip().split("\n")
        questions = [q for q in questions if q.strip()]
        return questions
    except Exception as e:
        print("❌ Gemini API call failed:", e)
        return []
    


def suggest_improvements(resume_text, job_role):
    try:
        prompt = f"""
        You are a professional resume reviewer and recruiter.
        Given the following resume text and the job role "{job_role}", 
        provide specific, constructive suggestions to improve the resume.
        RESUME:{resume_text}
        Format your response as a numbered list of suggestions.
        """

        response = model.generate_content(prompt)
        suggestions = response.text.strip().split("\n")
        suggestions = [s for s in suggestions if s.strip()]
        return suggestions
    except Exception as e:
        print("❌ Gemini suggestion call failed:", e)
        return []

