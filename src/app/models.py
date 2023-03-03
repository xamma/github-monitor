from pydantic import BaseModel
from typing import List

class AppConfig(BaseModel):
    """
    This is the configuration Class for the App.
    It uses pydantics BaseModel to declare the Types
    and what happens, when the entry is not defined.
    """
    repo_list : List | None = None
    github_token : str | None = None
    discord_token : str | None = None
    discord_channel_name: str | None = None
