"""Test AudioPlayer implementation."""

from pathlib import Path

from src.core.media import Media
from src.media.audio_player import AudioPlayer


def main():
    """Run AudioPlayer tests."""

    print()
    print("=" * 70)
    print("MusicTimer Pro - AudioPlayer Test")
    print("=" * 70)
    print()

    player = AudioPlayer()

    print("✓ AudioPlayer initialized.")

    # --------------------------------------------------
    # Test interface
    # --------------------------------------------------

    assert hasattr(player, "play")
    assert hasattr(player, "pause")
    assert hasattr(player, "resume")
    assert hasattr(player, "stop")
    assert hasattr(player, "is_playing")

    print(
        "✓ MediaPlayer interface methods available."
    )

    # --------------------------------------------------
    # Test media object
    # --------------------------------------------------

    media = Media(
        Path("test_audio.mp3")
    )

    assert media.media_type == "audio"

    print(
        "✓ Audio Media object created."
    )

    # --------------------------------------------------
    # Test missing file
    # --------------------------------------------------

    try:

        player.play(media)

        raise AssertionError(
            "Expected FileNotFoundError."
        )

    except FileNotFoundError:

        print(
            "✓ Missing-file validation passed."
        )

    # --------------------------------------------------
    # Test video rejection
    # --------------------------------------------------

    video = Media(
        Path("test_video.mp4")
    )

    try:

        player.play(video)

        raise AssertionError(
            "AudioPlayer should reject video."
        )

    except ValueError:

        print(
            "✓ Video rejection passed."
        )

    # --------------------------------------------------
    # Cleanup
    # --------------------------------------------------

    player.shutdown()

    print(
        "✓ AudioPlayer shutdown completed."
    )

    print()
    print("=" * 70)
    print(
        "All AudioPlayer tests passed!"
    )
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()