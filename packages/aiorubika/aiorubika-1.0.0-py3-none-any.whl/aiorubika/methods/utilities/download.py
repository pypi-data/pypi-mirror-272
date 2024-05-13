import aiofiles

import aiorubika


class Download:

    async def download(
            self: "aiorubika.Client",
            file_inline: "aiorubika.types.Results",
            save_as: str = None,
            chunk_size: int = 131072,
            callback=None,
            *args,
            **kwargs
    ):
        result = await self.connection.download(
            file_inline.dc_id,
            file_inline.file_id,
            file_inline.access_hash_rec,
            file_inline.size,
            chunk=chunk_size,
            callback=callback
        )

        if isinstance(save_as, str):
            async with aiofiles.open(save_as, 'wb+') as file:
                await file.write(result)
                return save_as

        return result
