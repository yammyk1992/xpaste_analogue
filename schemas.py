from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TextForPOST(BaseModel):
    text: str


class TextForGET(TextForPOST):
    id: int
    created_at: Optional[datetime] = None
    salt: Optional[str] = None

