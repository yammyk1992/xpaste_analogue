import random
import string
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


def get_salt():
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(6))


class TextForPOST(BaseModel):
    text: str
    salt: Optional[str] = get_salt()


class TextForGET(TextForPOST):
    text_id: int
    created_at: Optional[datetime] = datetime.utcnow()


