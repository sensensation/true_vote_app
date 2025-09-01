from abc import ABC, abstractmethod

from app.app_layer.interfaces.api.internal.models.auth import (
    NonceRequestDTO,
    NonceResponse,
    VerifyRequestDTO,
    VerifyResponse,
)


class AbstractAuthService(ABC):
    @abstractmethod
    async def issue_nonce(self, data: NonceRequestDTO) -> NonceResponse: ...

    @abstractmethod
    async def verify(self, data: VerifyRequestDTO) -> VerifyResponse: ...
