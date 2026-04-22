AI Job Copilot

AI Job Copilot is an AI-powered job assistant for resume-JD matching, skill gap analysis, and knowledge-based career Q&A.

Features
PDF resume upload
Job description input
Skill extraction and normalization
Matched core skills, missing technical skills, and related background
Direct match score and transferable background score
TensorFlow-enhanced resume sentence classification in the main analysis pipeline
Wikipedia-based retrieval Q&A

Tech Stack
Frontend: Vue3, Element Plus, TypeScript, Axios
Backend: FastAPI, Python, Pydantic
AI / ML: TensorFlow, Keras, skill extraction and normalization, rule-based layered matching, retrieval-based Q&A, Wikipedia retrieval

Project Structure
backend
frontend

How to Run/n
Backend: cd backend / pip install -r requirements.txt / python run.py
Frontend: cd frontend / npm install / npm run dev

Project Highlights
Built a layered matching pipeline for resume and JD analysis
Added direct-match and transferable-background dual scoring
Integrated TensorFlow sentence classification into the main matching workflow
Iterated from a small local RAG prototype to a Wikipedia-based retrieval workflow for broader coverage
