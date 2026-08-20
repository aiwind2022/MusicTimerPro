"""Playlist management for MusicTimer Pro."""

from dataclasses import dataclass, field

from src.core.media import Media


@dataclass
class Playlist:
    """
    Represent a collection of media files.

    A playlist can contain audio, video, or mixed media.
    """

    name: str
    description: str = ""
    enabled: bool = True
    items: list[Media] = field(
        default_factory=list
    )

    # ==================================================
    # Media management
    # ==================================================

    def add(self, media: Media):
        """Add media to the playlist."""

        if not isinstance(media, Media):
            raise TypeError(
                "media must be a Media object."
            )

        if media not in self.items:
            self.items.append(media)

    def remove(self, media: Media):
        """Remove media from the playlist."""

        if media in self.items:
            self.items.remove(media)

    def clear(self):
        """Remove all media."""

        self.items.clear()

    # ==================================================
    # Information
    # ==================================================

    @property
    def count(self):
        """Return number of media items."""

        return len(self.items)

    @property
    def playable_items(self):
        """
        Return enabled media items.

        Media files that are disabled are excluded.
        """

        return [
            media
            for media in self.items
            if media.enabled
        ]

    @property
    def is_empty(self):
        """Return True if playlist contains no media."""

        return len(self.items) == 0

    # ==================================================
    # Lookup
    # ==================================================

    def get(self, index):
        """Return media at a specific position."""

        if index < 0 or index >= len(self.items):
            raise IndexError(
                "Playlist index out of range."
            )

        return self.items[index]

    def find(self, title):
        """Find media by title."""

        for media in self.items:
            if media.title == title:
                return media

        return None

    # ==================================================
    # Representation
    # ==================================================

    def __str__(self):
        return (
            f"{self.name} "
            f"({self.count} items)"
        )