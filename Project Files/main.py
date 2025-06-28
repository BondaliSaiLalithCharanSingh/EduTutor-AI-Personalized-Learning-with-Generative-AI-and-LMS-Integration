
import os 
import re
os.environ["TRANSFORMERS_NO_ADVISORY_WARNINGS"] = "1"
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from datetime import datetime
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from pinecone import Pinecone, ServerlessSpec
import uuid
from dotenv import load_dotenv
import re

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

HF_TOKEN = os.getenv("HF_TOKENS")
MODEL_NAME = os.getenv("HF_MODEL")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENVIRONMENT")
PINECONE_INDEX = os.getenv("PINECONE_INDEX")

qa_pipeline = pipeline("text2text-generation", model=MODEL_NAME, tokenizer=MODEL_NAME)

pc = Pinecone(api_key=PINECONE_API_KEY)

if PINECONE_INDEX not in pc.list_indexes().names():
    pc.create_index(
        name=PINECONE_INDEX,
        dimension=1024,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

index = pc.Index(PINECONE_INDEX)

users = {}

class RegisterModel(BaseModel):
    email: str
    password: str
    role: str

class LoginModel(BaseModel):
    email: str
    password: str
    role: str

class QuizRequest(BaseModel):
    name: str
    email: str
    topic: str
    difficulty: str
    num_questions: int

class QuestionResult(BaseModel):
    question: str
    selected: str
    correct: str
    explanation: str

class SubmitQuizModel(BaseModel):
    name: str
    email: str
    topic: str
    difficulty: str
    questions: List[QuestionResult]
    score: int

@app.post("/register")
def register(data: RegisterModel):
    if data.email in users:
        raise HTTPException(status_code=400, detail="Email already exists.")
    users[data.email] = {"password": data.password, "role": data.role}
    return {"message": "Registration successful"}

@app.post("/login")
def login(data: LoginModel):
    u = users.get(data.email)
    if not u:
        raise HTTPException(status_code=401, detail="Email not found.")
    if u["password"] != data.password:
        raise HTTPException(status_code=401, detail="Incorrect password.")
    if u["role"] != data.role:
        raise HTTPException(status_code=401, detail="Role mismatch.")
    return {"message": "Login successful"}

@app.post("/generate_quiz")
def generate_quiz(data: QuizRequest):
    print("🎯 Generating quiz for:", data.topic)

    prompt = (
        f"Generate {data.num_questions} unique {data.difficulty} level multiple choice questions "
        f"on the topic '{data.topic}'. Each question must have 4 options labeled A, B, C, D. "
        f"Provide the correct answer at the end with 'Answer:'.\n"
    )

    output = qa_pipeline(prompt, max_new_tokens=1024)[0]["generated_text"]
    print("📄 Model Output:\n", output)

    raw_parts = output.split("Answer:")

    questions = []
    for i in range(data.num_questions):
        if i < len(raw_parts) - 1:
            q_block = raw_parts[i].strip()
            answer = raw_parts[i + 1].strip().split('\n')[0].strip()

            lines = q_block.split("\n")
            question_line = lines[0].replace("Q:", "").strip() if lines[0].startswith("Q:") else lines[0]
            options = [line.strip()[2:].strip() for line in lines[1:5] if line.strip() and line[1] == '.']

            if len(options) == 4 and answer.upper() in "ABCD":
                questions.append({
                    "question": question_line,
                    "options": options,
                    "answer": options[ord(answer.upper()) - ord("A")],
                    "topic": data.topic,
                    "difficulty": data.difficulty,
                    "explanation": "This answer was selected by the model."
                })

    if not questions:
        raise HTTPException(status_code=400, detail="Quiz generation returned no questions. Try again.")

    return {"questions": questions}


@app.post("/submit_quiz")
def submit_quiz(data: SubmitQuizModel):
    record = {
        "name": data.name,
        "email": data.email,
        "topic": data.topic,
        "difficulty": data.difficulty,
        "score": data.score,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "questions": [q.dict() for q in data.questions]
    }
    index.upsert([(str(uuid.uuid4()), [0.0]*1024, record)])
    return {"message": "Quiz saved successfully"}

@app.get("/student_scores")
def all_scores():
    fetch = index.describe_index_stats()
    return {"message": "Use /student_scores/{email} to fetch specific records."}

@app.get("/student_scores/{email}")
def student_scores(email: str):
    vectors = index.fetch(ids=None)
    results = []
    for v in vectors.vectors.values():
        metadata = v.get("metadata", {})
        if metadata.get("email") == email:
            results.append(metadata)
    return {"results: results"}
