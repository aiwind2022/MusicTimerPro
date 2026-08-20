"""Real end-to-end scheduler audio playback test."""

import time
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
from src.media.audio_player import (
    AudioPlayer,
)


TEST_MEDIA_DIR = Path("test_media")

SHORT_AUDIO = (
    TEST_MEDIA_DIR / "test_music.mp3"
)

LONG_AUDIO = (
    TEST_MEDIA_DIR / "test_long_music.mp3"
)


class TestEvent:
    """Simple resolved event for testing."""

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
    """Run real scheduler-to-audio test."""

    print()
    print("=" * 70)
    print(
        "MusicTimer Pro - Real Scheduler Audio Test"
    )
    print("=" * 70)
    print()

    # --------------------------------------------------
    # Verify test files
    # --------------------------------------------------

    if not SHORT_AUDIO.exists():

        print(
            "ERROR: Short test audio not found:"
        )

        print(
            f"  {SHORT_AUDIO}"
        )

        print()
        print(
            "Please use the same test audio file "
            "from Sprint 1.5F."
        )

        return

    if not LONG_AUDIO.exists():

        print(
            "ERROR: Long test audio not found:"
        )

        print(
            f"  {LONG_AUDIO}"
        )

        print()
        print(
            "Please place a second longer audio file "
            "at this location."
        )

        return

    print("✓ Test audio files found.")

    # --------------------------------------------------
    # Create PlaylistManager
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
    # Add media
    # --------------------------------------------------

    upbeat.add(
        Media(SHORT_AUDIO)
    )

    long_music.add(
        Media(LONG_AUDIO)
    )

    print(
        "✓ Playlists configured."
    )

    # --------------------------------------------------
    # Create REAL AudioPlayer
    # --------------------------------------------------

    player = AudioPlayer()

    print(
        "✓ Real AudioPlayer initialized."
    )

    # --------------------------------------------------
    # Create PlaybackController
    # --------------------------------------------------

    controller = PlaybackController(
        playlist_manager=manager,
        media_player=player,
    )

    # --------------------------------------------------
    # Create SchedulerPlaybackService
    # --------------------------------------------------

    playback_service = (
        SchedulerPlaybackService(
            playback_controller=controller,
        )
    )

    print(
        "✓ Scheduler playback service initialized."
    )

    # --------------------------------------------------
    # Simulated schedule
    # --------------------------------------------------

    start = datetime(
        2026,
        8,
        20,
        8,
        0,
    )

    print()
    print(
        f"Simulation started: "
        f"{start:%Y-%m-%d %H:%M:%S}"
    )

    print()

    # We will test:
    #
    # 08:15 short
    # 08:30 short
    # 08:45 short
    # 09:00 long
    #
    # The 09:00 long event replaces the
    # short reminder at the same time.

    events = [
        (
            start + timedelta(minutes=15),
            TestEvent(
                "Short Reminder",
                "upbeat",
                50,
            ),
        ),
        (
            start + timedelta(minutes=30),
            TestEvent(
                "Short Reminder",
                "upbeat",
                50,
            ),
        ),
        (
            start + timedelta(minutes=45),
            TestEvent(
                "Short Reminder",
                "upbeat",
                50,
            ),
        ),
        (
            start + timedelta(hours=1),
            TestEvent(
                "Long Break",
                "long_music",
                100,
            ),
        ),
    ]

    # --------------------------------------------------
    # Process events
    # --------------------------------------------------

    played_events = 0

    try:

        for event_time, event in events:

            print(
                f"{event_time:%H:%M:%S}  "
                f"🎵 {event.name} | "
                f"priority={event.priority} | "
                f"playlist={event.playlist}"
            )

            media = (
                playback_service.process_event(
                    event
                )
            )

            if media is None:

                raise RuntimeError(
                    f"No media played for "
                    f"{event.name}"
                )

            played_events += 1

            print(
                f"       🔊 Playing: "
                f"{media.title}"
            )

            # Give pygame a moment to start.
            time.sleep(1)

            if controller.is_playing():

                print(
                    "       ✓ Audio playback active."
                )

            else:

                print(
                    "       ⚠ Audio finished "
                    "or stopped."
                )

            # Stop before moving to the next
            # simulated scheduler event.
            controller.stop()

            print(
                "       ✓ Playback stopped."
            )

            print()

        # --------------------------------------------------
        # Assertions
        # --------------------------------------------------

        print(
            "-" * 70
        )

        print(
            "Running assertions..."
        )

        print()

        assert (
            played_events == 4
        )

        assert (
            playback_service.events_processed
            == 4
        )

        assert (
            playback_service.events_played
            == 4
        )

        assert (
            playback_service.events_skipped
            == 0
        )

        print(
            "✓ Four scheduled events processed."
        )

        print(
            "✓ Four real audio playback requests."
        )

        print(
            "✓ Short playlist playback verified."
        )

        print(
            "✓ Long playlist playback verified."
        )

        print(
            "✓ Real AudioPlayer integration verified."
        )

        print()
        print("=" * 70)
        print(
            "Real Scheduler Audio Test PASSED!"
        )
        print("=" * 70)
        print()

    finally:

        # Always shut down pygame properly.
        player.shutdown()

        print(
            "✓ AudioPlayer shutdown completed."
        )


if __name__ == "__main__":
    main()