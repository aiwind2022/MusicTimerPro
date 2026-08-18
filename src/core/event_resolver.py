"""Event resolution for MusicTimer Pro."""

from dataclasses import dataclass


@dataclass
class ResolvedEvent:
    """Represent the event selected for playback."""

    name: str
    playlist: str | None
    priority: int
    trigger_time: object
    suppressed_events: list


class EventResolver:
    """
    Resolve multiple simultaneous scheduler events.

    The highest-priority event wins.

    Lower-priority events are suppressed for that
    occurrence only. Their schedules continue normally.
    """

    def __init__(self, logger=None):
        self.logger = logger

    def resolve(self, events):
        """
        Resolve a list of due events.

        Args:
            events: List of scheduler event dictionaries.

        Returns:
            ResolvedEvent or None.
        """

        if not events:
            return None

        # Highest priority first.
        sorted_events = sorted(
            events,
            key=lambda event: event["priority"],
            reverse=True,
        )

        selected = sorted_events[0]

        suppressed = sorted_events[1:]

        result = ResolvedEvent(
            name=selected["name"],
            playlist=selected["playlist"],
            priority=selected["priority"],
            trigger_time=selected["trigger_time"],
            suppressed_events=suppressed,
        )

        self._log(
            f"Selected event: {selected['name']} "
            f"(priority={selected['priority']})"
        )

        for event in suppressed:
            self._log(
                f"Suppressed event: {event['name']} "
                f"because {selected['name']} "
                f"has higher priority."
            )

        return result

    def _log(self, message):
        """Write to application logger."""

        if self.logger is not None:
            self.logger.info(message)