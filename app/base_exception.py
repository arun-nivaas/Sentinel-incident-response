class SentinelException(Exception):
    def __init__(self, message: str, code: str = "APP_ERROR", status_code: int = 400, details: str | None = None):
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details
        super().__init__(message)

class LLMInitializationError(SentinelException):
    def __init__(self, message: str = "Failed to initialize LLM", details: str | None =None):
        super().__init__(message, code="LLM_INITIALIZATION_ERROR", status_code=503, details=details)


class LLMInvocationError(SentinelException):
    def __init__(self, message: str = "LLM invocation failed", details: str | None =None):
        super().__init__(message, code="LLM_INVOCATION_ERROR", status_code=502, details=details)


