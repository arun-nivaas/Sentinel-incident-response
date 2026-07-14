class LLMError(Exception):
    def __init__(self, message: str):
            super().__init__(message)
            self.message = message

    def __str__(self):
        return f"{self.__class__.__name__}: {self.message}"
    


class LLMInvocationError(LLMError):
    pass

class LLMInitializationError(LLMError):
    pass