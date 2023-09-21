import uuid

from pydantic import BaseModel

import services


class SettingsModel(BaseModel):
    class Config:
        orm_mode = True


class ShowText(SettingsModel):
    id: uuid.UUID
    text: str
    salt: str


class TextObjectCreate(BaseModel):
    text: str
    salt: services.get_salt()
