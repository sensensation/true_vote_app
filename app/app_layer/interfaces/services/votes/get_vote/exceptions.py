class BaseVoteError(Exception):
    def __init__(
        self,
        error_desc: str | None = None,
        error_code: int | None = None,
    ) -> None:
        self.error_code = error_code
        self.error_desc = error_desc


class VoteNotFoundError(BaseVoteError):
    """Raise it if vote was not found."""
