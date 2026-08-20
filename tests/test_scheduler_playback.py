"""Test SchedulerPlaybackService."""

from pathlib import Path

from src.core.media import Media
from src.core.playback_controller import (
    PlaybackController,
)
from src.core.playlist_manager import (
    PlaylistManager,
)
from src.core.scheduler_playback import (
    SchedulerPlaybackService,
)
from src.media.media_player import MediaPlayer


class MockMediaPlayer(MediaPlayer):
    """Fake media player for testing."""

    def __init__(self):
        self.current_media = None
        self.played_media = []
        self.playing = False

    def play(self, media):
        self.current_media = media
        self.played_media.append(media)
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


class TestEvent:
    """Simple resolved-event test object."""

    def __init__(
        self,
        name,
        playlist,
        priority=50,
    ):
        self.name = name
        self.playlist = playlist
        self.priority = priority


def main():
    """Run SchedulerPlaybackService tests."""

    print()
    print("=" * 70)
    print(
        "MusicTimer Pro - Scheduler Playback Service Test"
    )
    print("=" * 70)
    print()

    # --------------------------------------------------
    # Playlist setup
    # --------------------------------------------------

    manager = PlaylistManager()

    playlist = manager.create(
        "Upbeat",
        "Short reminder music.",
    )

    media1 = Media(
        Path("music/upbeat_01.mp3")
    )

    media2 = Media(
        Path("music/upbeat_02.mp3")
    )

    playlist.add(media1)
    playlist.add(media2)

    print(
        "✓ Test playlist created."
    )

    # --------------------------------------------------
    # Playback setup
    # --------------------------------------------------

    mock_player = MockMediaPlayer()

    controller = PlaybackController(
        playlist_manager=manager,
        media_player=mock_player,
    )

    service = SchedulerPlaybackService(
        playback_controller=controller,
    )

    print(
        "✓ SchedulerPlaybackService initialized."
    )

    # --------------------------------------------------
    # First event
    # --------------------------------------------------

    event = TestEvent(
        name="Short Reminder",
        playlist="Upbeat",
        priority=50,
    )

    media = service.process_event(
        event
    )

    assert media is media1

    assert service.events_processed == 1

    assert service.events_played == 1

    assert service.events_skipped == 0

    print(
        "✓ First scheduler event played."
    )

    # --------------------------------------------------
    # Second event
    # --------------------------------------------------

    media = service.process_event(
        event
    )

    assert media is media2

    assert service.events_processed == 2

    assert service.events_played == 2

    print(
        "✓ Second scheduler event played."
    )

    # --------------------------------------------------
    # Third event should wrap around
    # --------------------------------------------------

    media = service.process_event(
        event
    )

    assert media is media1

    print(
        "✓ Playlist cycling works."
    )

    # --------------------------------------------------
    # None event
    # --------------------------------------------------

    media = service.process_event(
        None
    )

    assert media is None

    assert service.events_skipped == 1

    print(
        "✓ Empty event handling passed."
    )

    # --------------------------------------------------
    # Playback controls
    # --------------------------------------------------

    service.pause()

    assert not service.is_playing()

    print(
        "✓ Pause passed."
    )

    service.resume()

    assert service.is_playing()

    print(
        "✓ Resume passed."
    )

    service.stop()

    assert not service.is_playing()

    print(
        "✓ Stop passed."
    )

    # --------------------------------------------------
    # Statistics
    # --------------------------------------------------

    assert service.events_processed == 3

    assert service.events_played == 3

    assert service.events_skipped == 1

    print(
        "✓ Event statistics verified."
    )

    service.reset_statistics()

    assert service.events_processed == 0
    assert service.events_played == 0
    assert service.events_skipped == 0

    print(
        "✓ Statistics reset passed."
    )

    print()
    print("=" * 70)
    print(
        "All Scheduler Playback Service tests passed!"
    )
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()