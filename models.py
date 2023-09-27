from typing import Optional, Union
from uuid import UUID
from pydantic import BaseModel


class TextForPOST(BaseModel):
    text: str


class TextForGET(TextForPOST):
    id: Union[int, str, UUID]
    key_with_salt: Optional[str] = None
