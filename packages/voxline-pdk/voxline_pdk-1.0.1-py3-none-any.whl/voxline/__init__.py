from .models import VoxSetting
from .api.activity import Activity
from .api.form import Form
from .api.memo import Memo
from .api.shift import Shift
from .api.user import User

class Voxline(object):
    activities: Activity
    shifts: Shift
    memos: Memo
    user: User
    def __init__(self, tenant: str, apiKey: str, local: bool = False):
        model = VoxSetting(tenant=tenant, apiKey=apiKey, local=local)

        if (local): model.base = self.__getLocal(port=3118)
        self.activities = Activity(model=model)
        self.shifts = Shift(model=model)

        if (local): model.base = self.__getLocal(port=3116)
        self.forms = Form(model=model)

        if (local): model.base = self.__getLocal(port=3117)
        self.memos = Memo(model=model)

        if (local): model.base = self.__getLocal(port=3119)
        self.users = User(model=model)

    def __getLocal(self, port: int) -> str:
        return 'http://localhost:%i' % (port)
