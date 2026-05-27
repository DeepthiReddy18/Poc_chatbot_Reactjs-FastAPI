from fastapi import FastAPI, UploadFile, File
import shutil
import os
from fastapi.middleware.cors import CORSMiddleware

from rag.pdf_loader import extract_text_from_pdf
from rag.chunker import chunk_text
from rag.vectordb import store_chunks
from rag.retriever import retrieve_relavant_chunks
from rag.chatbot import generate_response

from db.database import engine
from db.models import Base
from sqlalchemy.orm import Session
from db.database import sessionLocal
from db.models import ChatHistory

app = FastAPI()

origins = ["http://localhost:3000","http://localhost:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      
    allow_credentials=True,     
    allow_methods=["*"],        
    allow_headers=["*"],        
)

Base.metadata.create_all(bind = engine)

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/upload")
async def upload_pdf(file:UploadFile= File(...)):
    try:
        file_path = f"{UPLOAD_FOLDER}/{file.filename}"
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        text = extract_text_from_pdf(file_path)

        chunks = chunk_text(text)
        store_chunks(chunks, file.filename)

        return{
            "message":"PDF uploaded and indexed successfully",
            "chunks":len(chunks)
        }
    except Exception as e:
        return {
            "error":str(e)
        }

@app.post("/chat")
async def chat(query:str):
    chunks = retrieve_relavant_chunks(query)

    answer = generate_response(query, chunks)

    db = sessionLocal()

    chat_data = ChatHistory(
        question = query,
        answer = answer
    )

    db.add(chat_data)
    db.commit()

    db.close()

    return{
        "question":query,
        "answer": answer,
        "context":chunks
    }