from enum import Enum

class RequestResponse(Enum):
    UNAVALIBLE_PAYMENT_PROCESSOR = 1
    INVALID_REQUEST = 2,
    TIME_OUT = 3,
    OK_DEFAULT = 200
    OK_FALLBACK = 269
