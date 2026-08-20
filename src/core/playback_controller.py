"""Playback controller for MusicTimer Pro."""

from src.core.playlist_manager import PlaylistManager
from src.media.media_player import MediaPlayer


class PlaybackController:
    """
    Connect scheduler events to media playback.

    The controller does not know how audio or video
    playback is implemented.
    """

    def __init__(
        self,
        playlist_manager: PlaylistManager,
        media_player: MediaPlayer,
        logger=None,
    ):
        self.playlist_manager = (
            playlist_manager
        )

        self.media_player = media_player

        self.logger = logger

        self._positions = {}

    # ==================================================
    # Event playback
    # ==================================================

    def play_event(self, event):
        """
        Play the next media item associated
        with a resolved scheduler event.

        Args:
            event: ResolvedEvent returned by EventResolver.

        Returns:
            Media object that was selected.
        """

        if event is None:
            return None

        playlist_name = event.playlist

        if not playlist_name:
            self._log(
                f"Event '{event.name}' "
                "has no playlist."
            )

            return None

        playlist = (
            self.playlist_manager.get(
                playlist_name
            )
        )

        if playlist is None:
            raise ValueError(
                f"Playlist not found: "
                f"{playlist_name}"
            )

        media_items = (
            playlist.playable_items
        )

        if not media_items:
            self._log(
                f"Playlist '{playlist_name}' "
                "contains no playable media."
            )

            return None

        # ----------------------------------------------
        # Get current position
        # ----------------------------------------------

        position = self._positions.get(
            playlist_name,
            0,
        )

        # Protect against changes to the playlist.
        position %= len(media_items)

        media = media_items[position]

        # ----------------------------------------------
        # Advance position
        # ----------------------------------------------

        self._positions[
            playlist_name
        ] = (
            position + 1
        ) % len(media_items)

        # ----------------------------------------------
        # Play
        # ----------------------------------------------

        self.media_player.play(
            media
        )

        self._log(
            f"Playing '{media.title}' "
            f"from playlist "
            f"'{playlist_name}'."
        )

        return media

    # ==================================================
    # Playback controls
    # ==================================================

    def pause(self):
        """Pause current media."""

        self.media_player.pause()

    def resume(self):
        """Resume current media."""

        self.media_player.resume()

    def stop(self):
        """Stop current media."""

        self.media_player.stop()

    def is_playing(self):
        """Return playback state."""

        return self.media_player.is_playing()

    # ==================================================
    # Playlist position
    # ==================================================

    def reset_playlist(
        self,
        playlist_name,
    ):
        """Reset sequential playback position."""

        self._positions[
            playlist_name
        ] = 0

    def reset_all(self):
        """Reset all playlist positions."""

        self._positions.clear()

    # ==================================================
    # Logging
    # ==================================================

    def _log(self, message):
        """Write to application logger."""

        if self.logger is not None:
            self.logger.info(message)