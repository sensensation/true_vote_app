from enum import IntEnum


class VoteStatusEnum(IntEnum):
    PENDING = 0  # Голос зарегистрирован, но не обработан, находится в очереди
    REJECTED = 1  # Голос отклонен системой
    CANCELED = 2  # Голос отменен пользователем
    COUNTED = 3  # Голос учтен системой
