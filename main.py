from datetime import datetime
from typing import Optional
from fastapi import FastAPI, requests
from pydantic import BaseModel

import services

app = FastAPI(title="text_project")


class Text(BaseModel):
    text: str
    created_at: Optional[datetime] = None
    salt: Optional[str] = None


@app.post("/", response_model=Text)
async def create_txt(text: Text):
    text.salt = services.get_salt()
    text.created_at = datetime.utcnow()
    return text
