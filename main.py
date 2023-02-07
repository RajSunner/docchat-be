import pickle
from typing import Any
from fastapi import FastAPI
from pydantic import BaseModel
from query_data import get_chain

app = FastAPI()

with open("vectorstore.pkl", "rb") as f:
        vectorstore = pickle.load(f)

class Query(BaseModel):
    question: str
    history: Any

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/chat")
async def query(query: Query):
    qa_chain = get_chain(vectorstore)
    result = qa_chain({"question": query.question, "chat_history": query.history})
    results = {"answer": result["answer"]}
    return results