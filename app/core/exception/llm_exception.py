from app.core.exception.base_exception import SentinelException

class LLMInitializationError(SentinelException):
    def __init__(self, message: str = "Failed to initialize LLM", details: str | None =None):
        super().__init__(message, code="LLM_INITIALIZATION_ERROR", status_code=503, details=details)


class LLMInvocationError(SentinelException):
    def __init__(self, message: str = "LLM invocation failed", details: str | None =None):
        super().__init__(message, code="LLM_INVOCATION_ERROR", status_code=502, details=details)

class NotFoundException(SentinelException):
    def __init__(self, message: str = "Resource not found", details: str | None = None):
        super().__init__(message, code="NOT_FOUND", status_code=404, details=details)

class DatabaseException(SentinelException):
    def __init__(self, message: str = "Database operation failed", details: str | None = None):
        super().__init__(message, code="DATABASE_ERROR", status_code=503, details=details)

class DuplicateResourceException(SentinelException):
    def __init__(self, message: str = "Resource already exists", details: str | None = None):
        super().__init__(message, code="DUPLICATE_RESOURCE", status_code=409, details=details)