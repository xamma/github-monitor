import discord
from github import Github
import asyncio
from typing import List

#-Logger-----------------------------------
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

#-Settings---------------------------------
from app.config import config_settings

class DiscordBot(discord.Client):
    """
    The Bot informs a defined Discord-Channel about changes/commits to Github
    repositories. These can be defined in the config.py.
    This function is running every 60 secs.
    The discord client needs to be configured with the right intents for interacting
    with the channel.
    """
    def __init__(self) -> None:
        self.github_client = Github(config_settings.github_token)
        intents = discord.Intents().all()
        self.discord_client = discord.Client(intents=intents)
        self.ch = None
        self.message_comp = []

        # @self.discord_client.event
        # async def on_ready():
        #     print(f'{self.discord_client.user} has connected to Discord!')

    # Async event-listener for initialization of the discord client
    async def get_ready(self):
        @self.discord_client.event
        async def on_ready():
            print(f'{self.discord_client.user} has connected to Discord!')
            self.ch = self.discord_client.get_channel(config_settings.discord_channel_id)
            await self.ch.send(f"Hi, I'm monitoring your Github-Repos: {config_settings.repo_list}")
            while True:
                await self.check_for_new_commits(config_settings.repo_list)
                await asyncio.sleep(60)

    async def check_for_new_commits(self, repo_list:List):
        for entry in repo_list:
            repo = self.github_client.get_repo(entry)
            try:
                commits = repo.get_commits()
            except Exception as e:
                logger.info(f"Error getting commits: {e}")
            if commits.totalCount > 0:
                author = commits[0].commit.author.name
                message = commits[0].commit.message
                commit_url = commits[0].html_url

                if message not in self.message_comp:
                    # Send a message to the Discord server with the commit details
                    await self.ch.send(f'New commit by {author} in {repo}: {message} \n {commit_url}')
                    self.message_comp.append(message)
                else:
                    pass
    
    async def greet_members(self):
        @self.discord_client.event
        async def on_member_join(member):
            await member.create_dm()
            await member.dm_channel.send(
                f'Hi {member.name}, welcome to my Discord server!'
            )

    # Function to start the Discord bot
    def run(self):
        asyncio.run(self.get_ready())
        self.discord_client.run(config_settings.discord_token)