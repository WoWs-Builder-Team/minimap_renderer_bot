import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
)
LOGGER = logging.getLogger("scanner")
LOGGER_BOT = logging.getLogger("scanner-bot")
LOGGER_SCANNER = logging.getLogger("scanner-proc")
