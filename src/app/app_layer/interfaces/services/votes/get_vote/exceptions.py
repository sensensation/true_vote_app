class BaseVoteException(Exception):
    def __init__(
        self,
        error_desc: str | None = None,
        error_code: int | None = None,
    ) -> None:
        self.error_code = error_code
        self.error_desc = error_desc


class VoteNotFoundException(BaseVoteException):
    """Raise it if vote was not found"""
