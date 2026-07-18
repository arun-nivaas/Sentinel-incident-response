from langsmith import Client
from functools import lru_cache
from app.core.logger import logger

class PromptFetchError(Exception):
    pass

class PromptRegistry:
    def __init__(self) -> None:
        self.client = Client()

    def get_prompt(self, prompt_name: str):
        return _cached_pull(self.client, prompt_name)

@lru_cache(maxsize=None)
def _cached_pull(client: Client, prompt_name: str):
    try:
        return client.pull_prompt(prompt_name)
    except Exception as e:
        logger.error(f"Failed to pull prompt '{prompt_name}' from LangSmith: {e}")
        raise PromptFetchError(f"Could not load prompt '{prompt_name}'") from e

