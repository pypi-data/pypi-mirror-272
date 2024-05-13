from typing import Union

import aiorubika


class SetupTwoStepVerification:
    async def setup_two_step_verification(
            self: "aiorubika.Client",
            password: Union[int, str],
            hint: str,
            recovery_email: str,
    ):
        return await self.builder(
            name='setupTwoStepVerification',
            input={
                'password': str(password),
                 'hint': hint,
                 'recovery_email': recovery_email
            }
        )
