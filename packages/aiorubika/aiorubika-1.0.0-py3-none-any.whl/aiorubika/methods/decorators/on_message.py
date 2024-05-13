from ... import handlers

import aiorubika


class OnMessage:
    def on_message(
            self: "aiorubika.Client",
            *args,
            **kwargs,
    ):
        def MetaHandler(func):
            self.add_handler(func, handlers.MessageUpdates(*args, **kwargs))
            return func
        return MetaHandler
