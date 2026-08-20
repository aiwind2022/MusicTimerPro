"""Base media player interface for MusicTimer Pro."""

from abc import ABC, abstractmethod

from src.core.media import Media


class MediaPlayer(ABC):
    """
    Abstract interface for media playback.

    Audio and video players will implement this interface.
    """

    @abstractmethod
    def play(self, media: Media):
        """Start playing media."""
        raise NotImplementedError

    @abstractmethod
    def pause(self):
        """Pause playback."""
        raise NotImplementedError

    @abstractmethod
    def resume(self):
        """Resume playback."""
        raise NotImplementedError

    @abstractmethod
    def stop(self):
        """Stop playback."""
        raise NotImplementedError

    @abstractmethod
    def is_playing(self) -> bool:
        """Return True if media is currently playing."""
        raise NotImplementedError

    @abstractmethod
    def get_current_media(self):
        """Return the currently playing Media object."""
        raise NotImplementedError