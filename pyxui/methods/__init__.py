from pyxui.methods.base import Base
from pyxui.methods.clients import Clients
from pyxui.methods.inbounds import Inbounds
from pyxui.methods.login import Login


class Methods(
    Base,
    Login,
    Inbounds,
    Clients
):
    pass
