"""Test PlaylistManager."""

from pathlib import Path

from src.core.media import Media
from src.core.playlist_manager import (
    PlaylistManager,
)


def main():
    """Run PlaylistManager tests."""

    print()
    print("=" * 70)
    print("MusicTimer Pro - Playlist Manager Test")
    print("=" * 70)
    print()

    manager = PlaylistManager()

    # --------------------------------------------------
    # Create playlists
    # --------------------------------------------------

    upbeat = manager.create(
        "Upbeat",
        "Short reminder music.",
    )

    long_music = manager.create(
        "Long Music",
        "Long break music.",
    )

    assert manager.count == 2

    print(
        "✓ Two playlists created."
    )

    # --------------------------------------------------
    # Playlist names
    # --------------------------------------------------

    assert "Upbeat" in manager.names

    assert "Long Music" in manager.names

    print(
        "✓ Playlist names verified."
    )

    # --------------------------------------------------
    # Lookup
    # --------------------------------------------------

    found = manager.get(
        "Upbeat"
    )

    assert found is upbeat

    assert manager.exists(
        "Long Music"
    )

    print(
        "✓ Playlist lookup passed."
    )

    # --------------------------------------------------
    # Duplicate prevention
    # --------------------------------------------------

    try:

        manager.create("Upbeat")

        raise AssertionError(
            "Duplicate playlist should fail."
        )

    except ValueError:

        print(
            "✓ Duplicate prevention passed."
        )

    # --------------------------------------------------
    # Add media
    # --------------------------------------------------

    music1 = Media(
        Path("music/upbeat_01.mp3")
    )

    music2 = Media(
        Path("music/upbeat_02.mp3")
    )

    upbeat.add(music1)
    upbeat.add(music2)

    assert upbeat.count == 2

    print(
        "✓ Media added to playlist."
    )

    # --------------------------------------------------
    # Select playlist
    # --------------------------------------------------

    selected = manager.select(
        "Upbeat"
    )

    assert selected is upbeat

    assert (
        manager.get_selected()
        is upbeat
    )

    print(
        "✓ Playlist selection passed."
    )

    # --------------------------------------------------
    # Playable media
    # --------------------------------------------------

    playable = (
        manager.get_playable_media(
            "Upbeat"
        )
    )

    assert len(playable) == 2

    print(
        "✓ Playable-media lookup passed."
    )

    # --------------------------------------------------
    # Disable playlist
    # --------------------------------------------------

    upbeat.enabled = False

    playable = (
        manager.get_playable_media(
            "Upbeat"
        )
    )

    assert len(playable) == 0

    print(
        "✓ Disabled-playlist filtering passed."
    )

    # Re-enable
    upbeat.enabled = True

    # --------------------------------------------------
    # Remove playlist
    # --------------------------------------------------

    removed = manager.remove(
        "Long Music"
    )

    assert removed is True

    assert manager.count == 1

    print(
        "✓ Playlist removal passed."
    )

    # --------------------------------------------------
    # Remove nonexistent playlist
    # --------------------------------------------------

    removed = manager.remove(
        "Does Not Exist"
    )

    assert removed is False

    print(
        "✓ Missing-playlist handling passed."
    )

    print()
    print("=" * 70)
    print(
        "All PlaylistManager tests passed!"
    )
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()