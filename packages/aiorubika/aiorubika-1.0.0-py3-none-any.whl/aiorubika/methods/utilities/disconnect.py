from ... import exceptions

import aiorubika


class Disconnect:

    async def disconnect(self: "aiorubika.Client"):
        try:
            return await self.connection.close()

        except AttributeError:
            raise exceptions.NoConnection(
                'You must first connect the Client with the *.connect() method'
            )
