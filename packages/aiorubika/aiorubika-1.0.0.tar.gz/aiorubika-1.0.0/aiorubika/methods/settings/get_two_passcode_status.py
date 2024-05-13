import aiorubika

class GetTwoPasscodeStatus:
    async def get_two_passcode_status(self: "aiorubika.Client"):
        return await self.builder('getTwoPasscodeStatus')
