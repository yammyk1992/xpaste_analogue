from typing import Optional, Union
from uuid import UUID

from pydantic import BaseModel


class TextForPOST(BaseModel):
    text: str


class TextForGET(TextForPOST):
    text_uuid: Union[int, str, UUID]
    salt: Optional[str] = None
