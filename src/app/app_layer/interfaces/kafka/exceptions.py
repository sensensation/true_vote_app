class KafkaException(Exception):
    """Base exception"""


class KafkaConnectionException(KafkaException):
    """All connection errors"""


class KafkaTopicException(KafkaException):
    """Topic not found"""


class KafkaProducerError(KafkaException):
    """Something goes wrong during the message produce process"""
