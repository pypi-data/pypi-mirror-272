import os
from typing import Union, Optional

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .method_mapper import MethodMapper
    from PySimultan2.data_model import DataModel
    from PySimultan2.object_mapper import PythonMapper

initial_user_name = os.environ.get('INITIAL_USER_NAME', 'admin')
initial_user_email = os.environ.get('INITIAL_USER_EMAIL', 'example@test.de')
initial_user_password = os.environ.get('INITIAL_USER_PASSWORD', 'admin')


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DetailHistory:
    def __init__(self):
        self.detail_history = []
        self.detail_history_index = 0
        self.current_detail = None

    def add_item(self, item):
        if len(self.detail_history) > 0 and self.detail_history_index <= len(self.detail_history) -1:
            self.detail_history = self.detail_history[:self.detail_history_index]
            self.detail_history_index = len(self.detail_history)

        self.detail_history.append(item)
        if len(self.detail_history) > 10:
            self.detail_history.pop(0)
            self.detail_history_index = len(self.detail_history)
        self.current_detail = item

    def get_current_detail(self):
        return self.current_detail

    def get_previous_detail(self):
        if self.detail_history_index > 0:
            return self.detail_history[self.detail_history_index]

    def get_next_detail(self):
        if self.detail_history_index < len(self.detail_history) - 1:
            return self.detail_history[self.detail_history_index]

    def __len__(self):
        return len(self.detail_history)

    def move_next(self):
        if self.detail_history_index < len(self.detail_history) - 1:
            self.detail_history_index += 1
            return self.detail_history[self.detail_history_index]

    def move_previous(self):
        if self.detail_history_index > 0:
            self.detail_history_index -= 1
            return self.detail_history[self.detail_history_index]


class User:

    def __init__(self, *args, **kwargs):

        from ..core import method_mapper, mapper

        self._project_manager = None
        self._view_manager = None
        self._asset_manager = None
        self._geometry_manager = None
        self._navigation = None

        self.user_manager = kwargs.get('user_manager', None)

        self.name = kwargs.get('name', None)
        self.email = kwargs.get('email', None)
        self.password = kwargs.get('password', None)

        self.mapper: Optional[PythonMapper] = kwargs.get('mapper', mapper)
        self.method_mapper: Optional[MethodMapper] = kwargs.get('method_mapper', method_mapper)
        self.data_model: Union[DataModel, None] = kwargs.get('data_model', None)

        self.navigation_drawer = kwargs.get('navigation_drawer', None)
        self.project_tab = kwargs.get('navigation_drawer', None)
        self.detail_view = kwargs.get('navigation_drawer', None)
        self.home_tab = kwargs.get('navigation_drawer', None)

        self.detail_history = DetailHistory()

    @property
    def project_manager(self):
        if self._project_manager is None:
            from .project_manager import ProjectManager
            self._project_manager = ProjectManager(user_manager=self.user_manager,
                                                   mapper=self.mapper)
        return self._project_manager

    @property
    def view_manager(self):
        if self._view_manager is None:
            from ..views.view_manager import ViewManager
            self._view_manager = ViewManager(mapper=self.mapper,
                                             parent=self.project_manager)
        return self._view_manager

    @property
    def asset_manager(self):
        if self._asset_manager is None:
            from ..views.asset_view import AssetManager
            self._asset_manager = AssetManager()
        return self._asset_manager

    @property
    def geometry_manager(self):
        if self._geometry_manager is None:
            from ..views.geometry_view import GeometryManager
            self._geometry_manager = GeometryManager(data_model=self.data_model)
        return self._geometry_manager

    @property
    def navigation(self):
        if self._navigation is None:
            from .navigation import Navigation
            self._navigation = Navigation()
        return self._navigation


class Admin(User):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class UserManager(metaclass=Singleton):

    def __init__(self):
        self.users = {}
        self.create_initial_users()

    def create_initial_users(self):
        admin = Admin(name=initial_user_name,
                      email=initial_user_email,
                      password=initial_user_password,
                      user_manager=self)

        self.users[initial_user_name] = admin

        user_1 = User(name=initial_user_name + '_2',
                      email=initial_user_email + '_2',
                      password=initial_user_password + '_2',
                      user_manager=self)

        self.users[initial_user_name + '_2'] = user_1

    def authenticate(self, username, password):
        if username in self.users and self.users[username].password == password:
            return True
        return False

    def __getitem__(self, key):
        return self.users[key]
