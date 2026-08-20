"""Real audio playback integration test."""

import time
from pathlib import Path

from src.core.media import Media
from src.core.playback_controller import (
    PlaybackController,
)
from src.core.playlist_manager import (
    PlaylistManager,
)
from src.media.audio_player import (
    AudioPlayer,
)


AUDIO_FILE = Path(
    "test_media/test_music.mp3"
)


def main():
    """Run real audio playback test."""

    print()
    print("=" * 70)
    print(
        "MusicTimer Pro - Real Audio Playback Test"
    )
    print("=" * 70)
    print()

    # --------------------------------------------------
    # Verify file
    # --------------------------------------------------

    if not AUDIO_FILE.exists():

        print(
            f"ERROR: Audio file not found:"
        )

        print(
            f"  {AUDIO_FILE}"
        )

        print()
        print(
            "Place a short MP3 or WAV file in:"
        )

        print(
            "  test_media/test_music.mp3"
        )

        return

    print(
        f"✓ Audio file found:"
    )

    print(
        f"  {AUDIO_FILE}"
    )

    # --------------------------------------------------
    # Create media
    # --------------------------------------------------

    media = Media(
        AUDIO_FILE
    )

    assert media.media_type == "audio"

    print(
        "✓ Media object created."
    )

    # --------------------------------------------------
    # Create playlist
    # --------------------------------------------------

    manager = PlaylistManager()

    playlist = manager.create(
        "Test Music",
        "Real audio playback test.",
    )

    playlist.add(media)

    print(
        "✓ Test playlist created."
    )

    # --------------------------------------------------
    # Create real AudioPlayer
    # --------------------------------------------------

    player = AudioPlayer()

    print(
        "✓ AudioPlayer initialized."
    )

    # --------------------------------------------------
    # Create PlaybackController
    # --------------------------------------------------

    controller = PlaybackController(
        playlist_manager=manager,
        media_player=player,
    )

    print(
        "✓ PlaybackController initialized."
    )

    # --------------------------------------------------
    # Create test event
    # --------------------------------------------------

    class TestEvent:
        name = "Test Audio"
        playlist = "Test Music"
        priority = 50

    event = TestEvent()

    # --------------------------------------------------
    # Start playback
    # --------------------------------------------------

    print()
    print(
        "Starting audio playback..."
    )

    print(
        "You should hear the test music now."
    )

    print()

    selected = controller.play_event(
        event
    )

    assert selected is media

    print(
        f"✓ Selected media:"
    )

    print(
        f"  {selected.title}"
    )

    # --------------------------------------------------
    # Monitor playback
    # --------------------------------------------------

    print()
    print(
        "Playback status:"
    )

    for _ in range(10):

        if controller.is_playing():

            print(
                "  🔊 Audio is playing..."
            )

        else:

            print(
                "  ⏹ Audio has stopped."
            )

            break

        time.sleep(1)

    # --------------------------------------------------
    # Stop
    # --------------------------------------------------

    controller.stop()

    print()
    print(
        "✓ Playback stopped."
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
        "Real audio playback test completed."
    )
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()