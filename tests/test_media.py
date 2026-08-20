"""Test MusicTimer Pro media model."""

from pathlib import Path

from src.core.media import Media


def main():
    """Run media model tests."""

    print()
    print("=" * 70)
    print("MusicTimer Pro - Media Model Test")
    print("=" * 70)
    print()

    # --------------------------------------------------
    # Audio
    # --------------------------------------------------

    audio = Media(
        Path("music/upbeat.mp3")
    )

    print("Audio:")
    print(
        f"  Title: {audio.title}"
    )
    print(
        f"  File: {audio.filename}"
    )
    print(
        f"  Type: {audio.media_type}"
    )
    print(
        f"  Extension: {audio.extension}"
    )

    assert audio.media_type == "audio"

    assert audio.filename == "upbeat.mp3"

    assert (
        audio.extension
        == ".mp3"
    )

    print(
        "  ✓ Audio detection passed."
    )

    print()

    # --------------------------------------------------
    # Video
    # --------------------------------------------------

    video = Media(
        Path("videos/exercise.mp4")
    )

    print("Video:")
    print(
        f"  Title: {video.title}"
    )
    print(
        f"  File: {video.filename}"
    )
    print(
        f"  Type: {video.media_type}"
    )
    print(
        f"  Extension: {video.extension}"
    )

    assert video.media_type == "video"

    assert video.filename == "exercise.mp4"

    assert (
        video.extension
        == ".mp4"
    )

    print(
        "  ✓ Video detection passed."
    )

    print()

    # --------------------------------------------------
    # Custom title
    # --------------------------------------------------

    custom = Media(
        Path("music/break.mp3"),
        title="My Break Music",
    )

    assert (
        custom.title
        == "My Break Music"
    )

    print(
        "✓ Custom title test passed."
    )

    print()

    # --------------------------------------------------
    # Unsupported extension
    # --------------------------------------------------

    try:

        Media(
            Path("documents/test.pdf")
        )

        raise AssertionError(
            "PDF should not be accepted."
        )

    except ValueError:

        print(
            "✓ Unsupported file test passed."
        )

    print()

    print("=" * 70)
    print(
        "All Media Model tests passed!"
    )
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()