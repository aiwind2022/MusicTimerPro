"""Media model for MusicTimer Pro."""

from dataclasses import dataclass
from pathlib import Path


AUDIO_EXTENSIONS = {
    ".mp3",
    ".wav",
    ".m4a",
    ".aac",
    ".ogg",
    ".flac",
}

VIDEO_EXTENSIONS = {
    ".mp4",
    ".mov",
    ".avi",
    ".mkv",
    ".webm",
}


@dataclass
class Media:
    """
    Represent a playable media file.

    The model is intentionally independent of the
    actual playback technology.
    """

    path: Path
    title: str | None = None
    media_type: str | None = None
    enabled: bool = True

    def __post_init__(self):
        """Validate and initialize the media object."""

        self.path = Path(self.path)

        if self.title is None:
            self.title = self.path.stem

        if self.media_type is None:
            self.media_type = self.detect_type()

        self.media_type = self.media_type.lower()

        if self.media_type not in {
            "audio",
            "video",
        }:
            raise ValueError(
                f"Unsupported media type: "
                f"{self.media_type}"
            )

    # ==================================================
    # Type detection
    # ==================================================

    def detect_type(self):
        """
        Detect media type from file extension.

        Returns:
            "audio" or "video"

        Raises:
            ValueError if extension is unsupported.
        """

        extension = (
            self.path.suffix.lower()
        )

        if extension in AUDIO_EXTENSIONS:
            return "audio"

        if extension in VIDEO_EXTENSIONS:
            return "video"

        raise ValueError(
            f"Unsupported media extension: "
            f"{extension}"
        )

    # ==================================================
    # Properties
    # ==================================================

    @property
    def filename(self):
        """Return the filename."""

        return self.path.name

    @property
    def extension(self):
        """Return the lowercase extension."""

        return self.path.suffix.lower()

    @property
    def exists(self):
        """Return True if the media file exists."""

        return self.path.exists()

    # ==================================================
    # Representation
    # ==================================================

    def __str__(self):
        """Return a readable description."""

        return (
            f"{self.title} "
            f"({self.media_type})"
        )