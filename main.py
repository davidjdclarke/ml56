import logging

from src.app import Application

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Initailzing the application...")
    app = Application()
    app.run()