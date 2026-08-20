"""Test MusicTimer Pro playlist."""

from pathlib import Path

from src.core.media import Media
from src.core.playlist import Playlist


def main():
    """Run playlist tests."""

    print()
    print("=" * 70)
    print("MusicTimer Pro - Playlist Test")
    print("=" * 70)
    print()

    # --------------------------------------------------
    # Create playlist
    # --------------------------------------------------

    playlist = Playlist(
        name="Upbeat",
        description="Short upbeat reminder music.",
    )

    print(
        f"Playlist: {playlist.name}"
    )

    print(
        f"Description: "
        f"{playlist.description}"
    )

    assert playlist.count == 0

    print(
        "✓ Empty playlist created."
    )

    # --------------------------------------------------
    # Add audio
    # --------------------------------------------------

    music1 = Media(
        Path("music/upbeat_01.mp3")
    )

    music2 = Media(
        Path("music/upbeat_02.mp3")
    )

    playlist.add(music1)
    playlist.add(music2)

    assert playlist.count == 2

    print(
        "✓ Two audio files added."
    )

    # --------------------------------------------------
    # Prevent duplicates
    # --------------------------------------------------

    playlist.add(music1)

    assert playlist.count == 2

    print(
        "✓ Duplicate prevention passed."
    )

    # --------------------------------------------------
    # Find media
    # --------------------------------------------------

    found = playlist.find(
        "upbeat_01"
    )

    assert found is music1

    print(
        "✓ Media lookup passed."
    )

    # --------------------------------------------------
    # Test indexing
    # --------------------------------------------------

    first = playlist.get(0)

    assert first is music1

    print(
        "✓ Playlist indexing passed."
    )

    # --------------------------------------------------
    # Disable media
    # --------------------------------------------------

    music1.enabled = False

    playable = playlist.playable_items

    assert len(playable) == 1

    assert playable[0] is music2

    print(
        "✓ Disabled-media filtering passed."
    )

    # --------------------------------------------------
    # Remove media
    # --------------------------------------------------

    playlist.remove(music2)

    assert playlist.count == 1

    print(
        "✓ Media removal passed."
    )

    # --------------------------------------------------
    # Clear
    # --------------------------------------------------

    playlist.clear()

    assert playlist.count == 0

    assert playlist.is_empty

    print(
        "✓ Playlist clear passed."
    )

    print()
    print("=" * 70)
    print(
        "All Playlist tests passed!"
    )
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()