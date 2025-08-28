from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from prompt_router import handle_user_input
from utils import intent_classifier
from Agents.title_generator import generate_chat_title
from Agents.ocrapp import extract_pdf_text_with_vision
from typing import List

app = FastAPI(title="PakLaw Judicial Assistant API", version="1.0.0")

# ---------- Schemas ----------
class QueryRequest(BaseModel):
    query: str
    context: str = None

class TitleRequest(BaseModel):
    conversation: List[str]

class IntentRequest(BaseModel):
    query: str


# ---------- Routes ----------

@app.post("/query")
def process_query(request: QueryRequest):
    """
    Process user query through the main prompt router.
    """
    response = handle_user_input(request.query, context=request.context)
    return {"query": request.query, "response": response}


@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF and extract its text using OCR agent.
    """
    content = await file.read()
    text = extract_pdf_text_with_vision(content)
    return {"filename": file.filename, "extracted_text": text}


@app.post("/generate-title")
def generate_title(request: TitleRequest):
    """
    Generate a chat title from a conversation history.
    """
    title = generate_chat_title(request.conversation)
    return {"title": title}


@app.post("/classify-intent")
def classify_intent(request: IntentRequest):
    """
    Classify user query intent.
    """
    intent = intent_classifier(request.query)
    return {"query": request.query, "intent": intent}
