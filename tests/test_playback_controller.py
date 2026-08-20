"""Test PlaybackController."""

from pathlib import Path

from src.core.media import Media
from src.core.playback_controller import (
    PlaybackController,
)
from src.core.playlist_manager import (
    PlaylistManager,
)
from src.media.media_player import MediaPlayer


class MockMediaPlayer(MediaPlayer):
    """Fake media player for testing."""

    def __init__(self):
        self.played_media = []
        self.playing = False
        self.current_media = None

    def play(self, media):
        self.played_media.append(
            media
        )

        self.current_media = media
        self.playing = True

    def pause(self):
        self.playing = False

    def resume(self):
        self.playing = True

    def stop(self):
        self.playing = False
        self.current_media = None

    def is_playing(self):
        return self.playing

    def get_current_media(self):
        return self.current_media


def main():
    """Run PlaybackController tests."""

    print()
    print("=" * 70)
    print("MusicTimer Pro - Playback Controller Test")
    print("=" * 70)
    print()

    # --------------------------------------------------
    # Create playlist manager
    # --------------------------------------------------

    manager = PlaylistManager()

    playlist = manager.create(
        "Upbeat",
        "Short upbeat music.",
    )

    # --------------------------------------------------
    # Add media
    # --------------------------------------------------

    media1 = Media(
        Path("music/upbeat_01.mp3")
    )

    media2 = Media(
        Path("music/upbeat_02.mp3")
    )

    media3 = Media(
        Path("music/upbeat_03.mp3")
    )

    playlist.add(media1)
    playlist.add(media2)
    playlist.add(media3)

    print(
        "✓ Playlist created with 3 media items."
    )

    # --------------------------------------------------
    # Create mock player
    # --------------------------------------------------

    player = MockMediaPlayer()

    controller = PlaybackController(
        playlist_manager=manager,
        media_player=player,
    )

    print(
        "✓ PlaybackController initialized."
    )

    # --------------------------------------------------
    # Fake resolved event
    # --------------------------------------------------

    class TestEvent:
        name = "Short Reminder"
        playlist = "Upbeat"
        priority = 50

    event = TestEvent()

    # --------------------------------------------------
    # First playback
    # --------------------------------------------------

    selected = controller.play_event(
        event
    )

    assert selected is media1

    assert player.current_media is media1

    print(
        "✓ First media selected correctly."
    )

    # --------------------------------------------------
    # Second playback
    # --------------------------------------------------

    selected = controller.play_event(
        event
    )

    assert selected is media2

    print(
        "✓ Sequential playback passed."
    )

    # --------------------------------------------------
    # Third playback
    # --------------------------------------------------

    selected = controller.play_event(
        event
    )

    assert selected is media3

    print(
        "✓ Third media selected correctly."
    )

    # --------------------------------------------------
    # Wrap around
    # --------------------------------------------------

    selected = controller.play_event(
        event
    )

    assert selected is media1

    print(
        "✓ Playlist wrap-around passed."
    )

    # --------------------------------------------------
    # Playback controls
    # --------------------------------------------------

    controller.pause()

    assert not controller.is_playing()

    print(
        "✓ Pause passed."
    )

    controller.resume()

    assert controller.is_playing()

    print(
        "✓ Resume passed."
    )

    controller.stop()

    assert not controller.is_playing()

    print(
        "✓ Stop passed."
    )

    # --------------------------------------------------
    # Verify total playback
    # --------------------------------------------------

    assert len(
        player.played_media
    ) == 4

    print(
        "✓ Playback history verified."
    )

    print()
    print("=" * 70)
    print(
        "All PlaybackController tests passed!"
    )
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()