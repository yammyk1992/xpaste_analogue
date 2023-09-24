import random
import string
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


def get_salt():
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(6))


class Text(BaseModel):
    text: str
    created_at: Optional[str] = datetime.utcnow()
    salt: Optional[str] = get_salt()
