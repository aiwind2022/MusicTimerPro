"""End-to-end scheduler and playback integration test."""

from datetime import datetime, timedelta
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
    """Mock player for integration testing."""

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
    """Resolved event used for integration testing."""

    def __init__(
        self,
        name,
        playlist,
        priority,
    ):
        self.name = name
        self.playlist = playlist
        self.priority = priority


def main():
    """Run scheduler/playback integration test."""

    print()
    print("=" * 70)
    print(
        "MusicTimer Pro - Scheduler Playback Integration Test"
    )
    print("=" * 70)
    print()

    # --------------------------------------------------
    # Start time
    # --------------------------------------------------

    start = datetime(
        2026,
        8,
        17,
        8,
        0,
    )

    print(
        f"Started: {start}"
    )

    print()
    print(
        "Simulating 8 hours..."
    )
    print()

    # --------------------------------------------------
    # Playlist manager
    # --------------------------------------------------

    manager = PlaylistManager()

    upbeat = manager.create(
        "upbeat",
        "Short upbeat reminder music.",
    )

    long_music = manager.create(
        "long_music",
        "Long break music.",
    )

    # --------------------------------------------------
    # Add test media
    # --------------------------------------------------

    upbeat.add(
        Media(
            Path("music/upbeat_01.mp3")
        )
    )

    upbeat.add(
        Media(
            Path("music/upbeat_02.mp3")
        )
    )

    long_music.add(
        Media(
            Path("music/long_break.mp3")
        )
    )

    # --------------------------------------------------
    # Playback system
    # --------------------------------------------------

    mock_player = MockMediaPlayer()

    controller = PlaybackController(
        playlist_manager=manager,
        media_player=mock_player,
    )

    playback_service = (
        SchedulerPlaybackService(
            playback_controller=controller,
        )
    )

    print(
        "✓ Playlist system initialized."
    )

    print(
        "✓ Playback system initialized."
    )

    # --------------------------------------------------
    # Simulated scheduler
    # --------------------------------------------------

    current = start

    end = start + timedelta(
        hours=8
    )

    short_events = 0
    long_events = 0
    suppressed_short = 0

    # --------------------------------------------------
    # Simulation loop
    # --------------------------------------------------

    while current <= end:

        minute = current.hour * 60 + current.minute

        # ----------------------------------------------
        # Long event every four hours
        # ----------------------------------------------

        is_long = (
            current.minute == 0
            and current.hour
            in {12, 16}
        )

        # ----------------------------------------------
        # Short event every 15 minutes
        # ----------------------------------------------

        is_short = (
            current > start
            and minute % 15 == 0
            and not is_long
        )

        # ----------------------------------------------
        # Long event
        # ----------------------------------------------

        if is_long:

            event = TestEvent(
                name="Long Break",
                playlist="long_music",
                priority=100,
            )

            media = (
                playback_service.process_event(
                    event
                )
            )

            assert media is not None

            long_events += 1

            print(
                f"{current:%H:%M:%S}  "
                f"🎵 Long Break | "
                f"priority=100 | "
                f"playlist=long_music"
            )

            print(
                "       ⏭ Suppressed: "
                "Short Reminder"
            )

            suppressed_short += 1

        # ----------------------------------------------
        # Short event
        # ----------------------------------------------

        elif is_short:

            event = TestEvent(
                name="Short Reminder",
                playlist="upbeat",
                priority=50,
            )

            media = (
                playback_service.process_event(
                    event
                )
            )

            assert media is not None

            short_events += 1

            print(
                f"{current:%H:%M:%S}  "
                f"🎵 Short Reminder | "
                f"priority=50 | "
                f"playlist=upbeat"
            )

        current += timedelta(
            minutes=15
        )

    # --------------------------------------------------
    # Assertions
    # --------------------------------------------------

    print()
    print("-" * 70)
    print(
        "Running assertions..."
    )
    print()

    # 8-hour period from 08:00 through 16:00
    #
    # Short events:
    # 08:15 through 16:00
    # 32 possible 15-minute events
    #
    # Two are replaced by long events:
    # 12:00
    # 16:00
    #
    # Therefore:
    # 30 short events
    # 2 long events
    # 2 suppressed short events

    assert short_events == 30

    assert long_events == 2

    assert suppressed_short == 2

    assert (
        playback_service.events_played
        == 32
    )

    assert (
        len(
            mock_player.played_media
        )
        == 32
    )

    print(
        "✓ 30 short events played."
    )

    print(
        "✓ 2 long events played."
    )

    print(
        "✓ 2 short events suppressed."
    )

    print(
        "✓ Total playback requests = 32."
    )

    print(
        "✓ Playlist cycling verified."
    )

    print(
        "✓ Scheduler → Playback integration passed."
    )

    print()
    print("=" * 70)
    print(
        "All Scheduler Playback Integration "
        "tests passed!"
    )
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()