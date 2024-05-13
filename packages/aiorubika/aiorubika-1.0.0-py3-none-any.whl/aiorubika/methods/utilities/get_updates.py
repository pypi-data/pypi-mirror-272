import aiorubika


class GetUpdates:
    async def get_updates(self: "aiorubika.Client"):
        return await self.connection.get_updates()
