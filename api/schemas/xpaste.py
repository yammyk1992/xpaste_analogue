from datetime import datetime
from typing import Optional, Union
from uuid import UUID

from pydantic import BaseModel


class TextForPOST(BaseModel):
    text: str
    death_token: bool


class TextForGET(TextForPOST):
    text_uuid: Union[int, str, UUID]
    salt: Optional[str] = None
    created_at: datetime = datetime.now()

