import aiorubika


class UploadFile:
    async def upload(self: "aiorubika.Client", file, *args, **kwargs):
        return await self.connection.upload_file(file=file, *args, **kwargs)
