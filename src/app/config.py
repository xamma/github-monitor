import os
from typing import List
from models import AppConfig

#-Set user config-----------------------
"""
Here you can setup your custom configuration for running the app.
Make sure to match the types defined in the AppConfig in models.py
"""

user_data = {
  "repo_list": [],
  "github_token": "",
  "discord_token": "",
  "discord_channel_name": ""
}

#-Create settings object----------------
config_settings = AppConfig(**user_data)

#-Config via Envs-----------------------
"""
Configuration via ENVs has Precedence.
They need to be set upper case.
You can pass a list of repos via ENVS like this:
$env:REPO_LIST="repo1", "repo2"
It is recommended to set your configuration via ENVs,
to not expose secrets.
"""

for key, val in config_settings.dict().items():
  env = key.upper()
  if os.environ.get(env):
    try:
      # Check if the type annotation of the attribute is List, and if it is, convert the value to a list
      if isinstance(val, List):
        setattr(config_settings, key, os.environ.get(env).split(', ') if ', ' in os.environ.get(env) else os.environ.get(env).split(','))
      else:
        setattr(config_settings, key, os.environ.get(env))
    except Exception as e:
      print(e)
