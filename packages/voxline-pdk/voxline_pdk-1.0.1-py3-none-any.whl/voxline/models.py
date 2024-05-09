from pydantic import BaseModel
from enum import Enum

class VoxSetting(BaseModel):
    tenant: str
    apiKey: str
    local: bool = False
    base: str = ''
    entity: str = 'form'
