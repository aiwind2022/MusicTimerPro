"""MusicTimer Pro application entry point."""

from src.core.config import ConfigManager
from src.core.logger import setup_logger
from src.ui.main_window import MainWindow


def main():
    """Start MusicTimer Pro."""

    logger = setup_logger()

    logger.info("Starting MusicTimer Pro.")

    config_manager = ConfigManager()

    application = MainWindow(
        config_manager=config_manager,
        logger=logger,
    )

    application.mainloop()

    logger.info("MusicTimer Pro stopped.")


if __name__ == "__main__":
    main()