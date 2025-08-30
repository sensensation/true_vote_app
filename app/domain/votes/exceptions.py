class BaseRetireveVoteError(Exception):
    pass


class VoteNotFoundError(BaseRetireveVoteError):
    """Raise it if vote wasnt found."""
