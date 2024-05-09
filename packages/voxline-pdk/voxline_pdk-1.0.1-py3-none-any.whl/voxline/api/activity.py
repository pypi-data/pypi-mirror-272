from .request import Request
from ..models import VoxSetting

class Activity(Request):
    def __init__(self, model: VoxSetting):
        super().__init__(VoxSetting(tenant=model.tenant,apiKey=model.apiKey,local=model.local,base=model.base, entity='activity'))
