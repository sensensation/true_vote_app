import datetime

from pydantic import BaseModel, Field


class NonceRequestDTO(BaseModel):
    address: str = Field(min_length=32, max_length=50, description="Solana pubkey")
    domain: str | None = Field(default=None)


class NonceResponse(BaseModel):
    nonce: str
    message: str
    expires_at: datetime


class VerifyRequestDTO(BaseModel):
    address: str
    nonce: str
    signature: str
    domain: str | None = None


class VerifyResponse(BaseModel):
    token: str
    user: dict
