"""Playlist manager for MusicTimer Pro."""

from src.core.playlist import Playlist


class PlaylistManager:
    """
    Manage multiple playlists.

    The PlaylistManager is independent of the GUI
    and media playback system.
    """

    def __init__(self):
        self._playlists = {}
        self._selected_playlist = None

    # ==================================================
    # Playlist management
    # ==================================================

    def create(
        self,
        name,
        description="",
    ):
        """
        Create a new playlist.

        Raises:
            ValueError if the name already exists.
        """

        name = name.strip()

        if not name:
            raise ValueError(
                "Playlist name cannot be empty."
            )

        if name in self._playlists:
            raise ValueError(
                f"Playlist already exists: {name}"
            )

        playlist = Playlist(
            name=name,
            description=description,
        )

        self._playlists[name] = playlist

        return playlist

    def add(self, playlist):
        """Add an existing Playlist."""

        if not isinstance(
            playlist,
            Playlist,
        ):
            raise TypeError(
                "playlist must be a Playlist object."
            )

        if playlist.name in self._playlists:
            raise ValueError(
                f"Playlist already exists: "
                f"{playlist.name}"
            )

        self._playlists[
            playlist.name
        ] = playlist

        return playlist

    def remove(self, name):
        """Remove a playlist."""

        if name not in self._playlists:
            return False

        if (
            self._selected_playlist
            == name
        ):
            self._selected_playlist = None

        del self._playlists[name]

        return True

    # ==================================================
    # Lookup
    # ==================================================

    def get(self, name):
        """Return a playlist by name."""

        return self._playlists.get(name)

    def exists(self, name):
        """Return True if playlist exists."""

        return name in self._playlists

    # ==================================================
    # Selection
    # ==================================================

    def select(self, name):
        """Select a playlist."""

        playlist = self.get(name)

        if playlist is None:
            raise ValueError(
                f"Playlist not found: {name}"
            )

        self._selected_playlist = name

        return playlist

    def get_selected(self):
        """Return the selected playlist."""

        if self._selected_playlist is None:
            return None

        return self.get(
            self._selected_playlist
        )

    # ==================================================
    # Information
    # ==================================================

    @property
    def count(self):
        """Return number of playlists."""

        return len(self._playlists)

    @property
    def names(self):
        """Return playlist names."""

        return list(
            self._playlists.keys()
        )

    @property
    def playlists(self):
        """Return all playlists."""

        return list(
            self._playlists.values()
        )

    # ==================================================
    # Media
    # ==================================================

    def get_playable_media(
        self,
        playlist_name,
    ):
        """
        Return enabled media from a playlist.
        """

        playlist = self.get(
            playlist_name
        )

        if playlist is None:
            raise ValueError(
                f"Playlist not found: "
                f"{playlist_name}"
            )

        if not playlist.enabled:
            return []

        return playlist.playable_items