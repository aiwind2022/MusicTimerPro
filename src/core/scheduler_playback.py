"""Connect scheduler events to media playback."""

from src.core.playback_controller import PlaybackController


class SchedulerPlaybackService:
    """
    Bridge between the scheduler/event system
    and the playback controller.
    """

    def __init__(
        self,
        playback_controller: PlaybackController,
        logger=None,
    ):
        self.playback_controller = (
            playback_controller
        )

        self.logger = logger

        self._events_processed = 0
        self._events_played = 0
        self._events_skipped = 0

    # ==================================================
    # Event processing
    # ==================================================

    def process_event(self, event):
        """
        Process a resolved scheduler event.

        Returns:
            Media object if something was played.
            None if the event could not be played.
        """

        if event is None:
            self._events_skipped += 1
            return None

        self._events_processed += 1

        self._log(
            f"Processing event: "
            f"{event.name}"
        )

        media = (
            self.playback_controller.play_event(
                event
            )
        )

        if media is not None:

            self._events_played += 1

            self._log(
                f"Playing media: "
                f"{media.title}"
            )

        else:

            self._events_skipped += 1

            self._log(
                f"No media played for event: "
                f"{event.name}"
            )

        return media

    # ==================================================
    # Playback controls
    # ==================================================

    def pause(self):
        """Pause current playback."""

        self.playback_controller.pause()

    def resume(self):
        """Resume current playback."""

        self.playback_controller.resume()

    def stop(self):
        """Stop current playback."""

        self.playback_controller.stop()

    def is_playing(self):
        """Return True if media is playing."""

        return (
            self.playback_controller.is_playing()
        )

    # ==================================================
    # Statistics
    # ==================================================

    @property
    def events_processed(self):
        """Number of events processed."""

        return self._events_processed

    @property
    def events_played(self):
        """Number of events successfully played."""

        return self._events_played

    @property
    def events_skipped(self):
        """Number of events skipped."""

        return self._events_skipped

    def reset_statistics(self):
        """Reset event statistics."""

        self._events_processed = 0
        self._events_played = 0
        self._events_skipped = 0

    # ==================================================
    # Logging
    # ==================================================

    def _log(self, message):
        """Write to application logger."""

        if self.logger is not None:
            self.logger.info(message)