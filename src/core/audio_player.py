"""Audio playback engine for MusicTimer Pro."""

from pathlib import Path

import pygame


class AudioPlayer:
    """Manage audio playback independently of the GUI."""

    SUPPORTED_FORMATS = {
        ".mp3",
        ".wav",
        ".ogg",
        ".flac",
    }

    def __init__(self, logger=None):
        self.logger = logger
        self.current_file = None
        self.initialized = False
        self.volume = 0.8

        self._initialize()

    def _initialize(self):
        """Initialize the pygame audio mixer."""

        try:
            pygame.mixer.init()

            self.initialized = True

            self._log("Audio player initialized.")

        except pygame.error as error:
            self.initialized = False

            self._log(
                f"Unable to initialize audio: {error}"
            )

    def load(self, file_path):
        """Load an audio file."""

        if not self.initialized:
            self._log(
                "Audio system is not initialized."
            )
            return False

        path = Path(file_path)

        if not path.exists():
            self._log(
                f"Audio file does not exist: {path}"
            )
            return False

        if path.suffix.lower() not in self.SUPPORTED_FORMATS:
            self._log(
                f"Unsupported audio format: {path.suffix}"
            )
            return False

        try:
            pygame.mixer.music.load(
                str(path)
            )

            self.current_file = path

            self._log(
                f"Loaded audio: {path.name}"
            )

            return True

        except pygame.error as error:
            self._log(
                f"Unable to load audio: {error}"
            )
            return False

    def play(self):
        """Start playing the currently loaded audio."""

        if not self.initialized:
            return False

        if self.current_file is None:
            self._log(
                "No audio file loaded."
            )
            return False

        try:
            pygame.mixer.music.play()

            pygame.mixer.music.set_volume(
                self.volume
            )

            self._log(
                f"Playing: {self.current_file.name}"
            )

            return True

        except pygame.error as error:
            self._log(
                f"Playback error: {error}"
            )
            return False

    def pause(self):
        """Pause playback."""

        if not self.initialized:
            return

        pygame.mixer.music.pause()

        self._log("Audio paused.")

    def resume(self):
        """Resume paused playback."""

        if not self.initialized:
            return

        pygame.mixer.music.unpause()

        self._log("Audio resumed.")

    def stop(self):
        """Stop playback."""

        if not self.initialized:
            return

        pygame.mixer.music.stop()

        self._log("Audio stopped.")

    def set_volume(self, volume):
        """
        Set volume.

        Args:
            volume: Value between 0.0 and 1.0.
        """

        volume = max(
            0.0,
            min(1.0, float(volume)),
        )

        self.volume = volume

        if self.initialized:
            pygame.mixer.music.set_volume(
                volume
            )

        self._log(
            f"Volume set to {volume:.2f}"
        )

    def is_playing(self):
        """Return True if audio is playing."""

        if not self.initialized:
            return False

        return pygame.mixer.music.get_busy()

    def shutdown(self):
        """Release pygame audio resources."""

        if not self.initialized:
            return

        try:
            pygame.mixer.music.stop()
            pygame.mixer.quit()

        except pygame.error as error:
            self._log(
                f"Audio shutdown error: {error}"
            )

        self.initialized = False

        self._log(
            "Audio player shut down."
        )

    def _log(self, message):
        """Write a message to the application logger."""

        if self.logger is not None:
            self.logger.info(message)