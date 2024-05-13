from .advanced import Advanced
from .utilities import Utilities
from .auth import Auth
from .messages import Messages
from .decorators import Decorators
from .users import Users
from .settings import Settings


class Methods(
    Advanced,
    Utilities,
    Users,
    Auth,
    Messages,
    Decorators,
    Settings,
):
    pass
