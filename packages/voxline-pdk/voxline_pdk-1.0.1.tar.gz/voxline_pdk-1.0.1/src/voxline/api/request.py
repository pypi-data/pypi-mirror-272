from os.path import join
from ..models import VoxSetting
import requests

class SingletonMeta(type):
    __instances = {}
    def __call__(cls, model: VoxSetting):
        if cls not in cls.__instances:
            instance = super().__call__(model)
            cls.__instances[cls] = instance
        return cls.__instances[cls]

class Request(metaclass=SingletonMeta):
    def __init__(self, model: VoxSetting):
        self._entity = model.entity
        subdomain = self.getDomain(model.entity);
        self._model = model
        self._baseUrl = model.base if model.local else self.__getBaseUrl(subdomain)

    def __getBaseUrl(self, subdomain: str):
        return 'https://%s.voxline.com' % (subdomain)

    def __getHeader(self):
        return {
            'voxline-tenant': self._model.tenant,
            'Authorization': self._model.apiKey
        }

    def getDomain(self, entity: str):
        return 'https://%s.voxline.com' % (entity)

    def getOne(self, id: int):
        url = join(self._baseUrl, self._entity, str(id))
        try:
            response = requests.get(url, headers = self.__getHeader())
            return response.json()
        except:
            return {}

    def getAll(self, page: int = 1, items: int = 10):
        url = join(self._baseUrl, self._entity)
        params = { 'page': page, 'items': items }
        try:
            response = requests.get(url, headers = self.__getHeader(), params = params)
            return response.json()
        except:
            return []
