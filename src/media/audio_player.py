"""Audio player implementation for MusicTimer Pro."""

from pathlib import Path

import pygame

from src.core.media import Media
from src.media.media_player import MediaPlayer


class AudioPlayer(MediaPlayer):
    """
    Pygame-based audio player.

    This class handles audio playback only.
    """

    def __init__(self):
        """Initialize the audio player."""

        if not pygame.mixer.get_init():
            pygame.mixer.init()

        self.current_media = None
        self._playing = False

    # ==================================================
    # Playback
    # ==================================================

    def play(self, media: Media):
        """
        Play a Media object.

        Args:
            media: Media object containing an audio file.
        """

        if not isinstance(media, Media):
            raise TypeError(
                "media must be a Media object."
            )

        if media.media_type != "audio":
            raise ValueError(
                "AudioPlayer can only play audio media."
            )

        if not media.exists:
            raise FileNotFoundError(
                f"Media file not found: {media.path}"
            )

        pygame.mixer.music.load(
            str(media.path)
        )

        pygame.mixer.music.play()

        self.current_media = media
        self._playing = True

    def pause(self):
        """Pause the current audio."""

        if self._playing:
            pygame.mixer.music.pause()

    def resume(self):
        """Resume paused audio."""

        if self._playing:
            pygame.mixer.music.unpause()

    def stop(self):
        """Stop the current audio."""

        pygame.mixer.music.stop()

        self._playing = False
        self.current_media = None

    # ==================================================
    # Status
    # ==================================================

    def is_playing(self) -> bool:
        """
        Return whether audio is currently playing.
        """

        return (
            self._playing
            and pygame.mixer.music.get_busy()
        )

    def get_current_media(self):
        """Return the currently playing media."""

        return self.current_media

    # ==================================================
    # Cleanup
    # ==================================================

    def shutdown(self):
        """Release pygame mixer resources."""

        pygame.mixer.music.stop()

        if pygame.mixer.get_init():
            pygame.mixer.quit()

        self.current_media = None
        self._playing = False