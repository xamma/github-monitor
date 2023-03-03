from app.discord_bot import DiscordBot

if __name__ == "__main__":
    Bot = DiscordBot()
    Bot.start_commit_check_threads()
    Bot.run()