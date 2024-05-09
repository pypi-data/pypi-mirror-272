from .request import Request
from ..models import VoxSetting

class Shift(Request):
    def __init__(self, model: VoxSetting):
        super().__init__(VoxSetting(tenant=model.tenant,apiKey=model.apiKey,local=model.local,base=model.base,entity='shift'))
