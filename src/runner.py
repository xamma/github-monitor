from app.discord_bot import DiscordBot

"""
Runner-file for the DiscordBot.
The run-function is the only one not async,
but needs to be run with asyncio in the Class for the awaits.
"""

if __name__ == "__main__":
    Bot = DiscordBot()
    Bot.run()