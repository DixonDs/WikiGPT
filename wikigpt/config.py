import os
from pathlib import Path

from dotenv import load_dotenv


class Config:
    def __init__(self):
        load_dotenv()
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")

        # "gpt-3.5-turbo" or "gpt-4"
        self.openai_model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

        self.prompts_directory = os.getenv("PROMPTS_DIRECTORY")
        if not self.prompts_directory:
            self.prompts_directory = Path(__file__).parent / "prompts"

        self.drafts_directory = os.getenv("DRAFTS_DIRECTORY")
        if not self.drafts_directory:
            self.drafts_directory = Path(__file__).parent.parent / "drafts"
