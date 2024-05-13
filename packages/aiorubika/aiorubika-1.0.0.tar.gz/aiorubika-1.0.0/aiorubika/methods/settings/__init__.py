from .setup_two_step_verification import SetupTwoStepVerification
from .get_two_passcode_status import GetTwoPasscodeStatus
from .terminate_session import TerminateSession
from .get_my_sessions import GetMySessions


class Settings(
    SetupTwoStepVerification,
    GetTwoPasscodeStatus,
    TerminateSession,
    GetMySessions,
):
    pass
