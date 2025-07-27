from fastapi import FastAPI, Request
from pydantic import BaseModel
from chatbot import get_response

app = FastAPI()

# Define the request schema
class ChatRequest(BaseModel):
    query: str
    chat_history: list[tuple[str, str]] = []


# Define the response schema
class ChatResponse(BaseModel):
    answer: str

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chat_request: ChatRequest):
    response = get_response(chat_request.query, chat_request.chat_history)
    return ChatResponse(response=response)