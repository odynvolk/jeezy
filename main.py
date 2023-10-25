from fastapi import FastAPI
from pydantic import BaseModel

from jeezy.app import summarize_article

from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

class Command(BaseModel):
    query: str
    text: str

@app.get("/")
async def read_root():
    return "Trap or die"

@app.post("/summarise")
async def summarise(command: Command = None):
    print("text", command.text)
    output = summarize_article(command.query, command.text)
    
    return {"summary": output["result"]}
