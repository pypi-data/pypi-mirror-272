from .sessions import SQLiteSession, StringSession
from .methods import Methods
from .parser import Markdown

from typing import Optional


class Client(Methods):

    DEFAULT_PLATFORM = {
        'app_name': 'Main',
        'app_version': '4.4.6',
        'platform': 'Web',
        'package': 'web.rubika.ir',
    }

    USER_AGENT: str = (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko)'
        'Chrome/102.0.0.0 Safari/537.36'
    )

    API_VERSION = '6'

    def __init__(
            self,
            name: str,
            auth: Optional[str] = None,
            private_key: Optional[str] = None,
            bot_token: Optional[str] = None,
            phone_number: Optional[str] = None,
            user_agent: Optional[str] = None or USER_AGENT,
            timeout: Optional[int] = 20,
            lang_code: Optional[str] = 'fa',
            parse_mode: Optional[str] = 'All',
    ) -> None:
        super().__init__()
        if auth and not isinstance(auth, str):
            raise ValueError('`auth` is `string` arg.')

        if private_key:
            if not type(private_key) in (str, bytes):
                raise ValueError('`private_key` is `string` or `bytes` arg.')

        if bot_token and not isinstance(bot_token, str):
            raise ValueError('`bot_token` is `string` arg.')

        if phone_number and not isinstance(phone_number, str):
            raise ValueError('`phone_number` is `string` arg.')

        if user_agent and not isinstance(user_agent, str):
            raise ValueError('`user_agent` is `string` arg.')

        if not isinstance(timeout, int):
            timeout = int(timeout)

        if isinstance(name, str):
            session = SQLiteSession(name)

        elif not isinstance(name, StringSession):
            raise TypeError(
                'The given session must be a str or [rubpy.sessions.StringSession]'
            )

        if parse_mode not in ('All', 'html', 'markdown', 'mk'):
            raise ValueError(
                'The `parse_mode` argument can only be in `("All", "html", "markdown", "mk")`.'
            )

        self.name = name
        self.auth = auth
        self.session = session
        self.timeout = timeout
        self.private_key = private_key
        self.phone_number = phone_number
        self.bot_token = bot_token
        self.user_agent = user_agent
        self.lang_code = lang_code
        self.parse_mode = parse_mode
        self.handlers = dict()
        self.markdown = Markdown()
        self.guid = None
        self.key = None
        self.database = None
        self.decode_auth = None
        self.import_key = None
        self.DEFAULT_PLATFORM['lang_code'] = lang_code

    def __enter__(self):
        return self.start()

    def __exit__(self, *args, **kwargs):
        try:
            return self.disconnect()
        except Exception as exc:
            print(exc.__name__, exc)

    async def __aenter__(self):
        return await self.start()

    async def __aexit__(self, *args, **kwargs):
        try:
            return await self.disconnect()
        except Exception as exc:
            print(exc.__name__, exc)
