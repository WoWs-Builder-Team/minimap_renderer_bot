import argparse

from utils.logging import LOGGER
from dotenv import load_dotenv


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the bot or worker.")
    parser.add_argument(
        "-r", "--run", nargs=1, choices=["bot", "worker"], required=True
    )

    args = parser.parse_args()
    load_dotenv()

    match args.run.pop():
        case "bot":
            from bot import bot

            LOGGER.info("Running the bot...")
            bot.run()
        case "worker":
            from tasks.worker import run_worker

            LOGGER.info("Running the worker...")
            run_worker(["single"])
