import aiorubika


class GetMySessions:
    async def get_my_sessions(self: "aiorubika.Client"):
        return await self.builder('getMySessions')
