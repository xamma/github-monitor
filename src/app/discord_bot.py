import time
import discord
from github import Github
import threading

#-Logger-----------------------------------
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

#-Settings---------------------------------
from config import config_settings

class DiscordBot:
    """
    The Bot informs a defined Discord-Channel about changes/commits to Github
    repositories. These can be defined in the config.py.
    This function is running in one Thread per Repo, to ensure performance and 
    to make monitoring of multiple Repos possible.
    The discord client needs to be configured with the right intents for interacting
    with the channel.
    """
    def __init__(self) -> None:
        self.github_client = Github(config_settings.github_token)
        intents = discord.Intents().all()
        self.discord_client = discord.Client(intents=intents)

    async def get_discord_channelobj(self):
        for guild in self.discord_client.guilds:
            for channel in guild.channels:
                if channel.name == config_settings.discord_channel_name:
                    return channel

    # Function to check for new commits
    def check_for_new_commits(self, repo_name:str):
        channel = self.discord_client.loop.run_until_complete(self.get_discord_channelobj())
        while True:
            repo = self.github_client.get_repo(repo_name)
            commits = repo.get_commits()
            logger.info(repo_name)
            logger.info(commits)
            # if commits.totalCount > 0:
            #     author = commits[0].commit.author.name
            #     message = commits[0].commit.message
            #     commit_url = commits[0].html_url

            #     # Send a message to the Discord server with the commit details
            #     self.discord_client.loop.create_task(channel.send('New commit by {}: {} \n {}'.format(author, message, commit_url)))
            # time.sleep(60)

    # Function to start the commit check threads
    def start_commit_check_threads(self):
        for repo_name in config_settings.repo_list:
            threading.Thread(target=self.check_for_new_commits, args=(repo_name,), daemon=True).start()

    # Function to start the Discord bot
    def run(self):
        self.start_commit_check_threads()
        self.discord_client.run(config_settings.discord_token)