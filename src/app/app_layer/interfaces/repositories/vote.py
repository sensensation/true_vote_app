from abc import ABC, abstractmethod


class AbstractVoteRepository(ABC):
    @abstractmethod
    def create(self) -> None: ...
