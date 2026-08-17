"""Schedule data model for MusicTimer Pro."""

from datetime import datetime, timedelta


class Schedule:
    """Represent one recurring music schedule."""

    VALID_UNITS = {
        "seconds",
        "minutes",
        "hours",
    }

    def __init__(
        self,
        name,
        interval,
        unit="minutes",
        playlist=None,
        enabled=True,
    ):
        self.name = name
        self.interval = interval
        self.unit = unit
        self.playlist = playlist
        self.enabled = enabled

        self.last_triggered = None
        self.next_trigger = None

        self._validate()

    def _validate(self):
        """Validate schedule settings."""

        if not self.name:
            raise ValueError(
                "Schedule name cannot be empty."
            )

        if not isinstance(self.interval, int):
            raise ValueError(
                "Interval must be an integer."
            )

        if self.interval <= 0:
            raise ValueError(
                "Interval must be greater than zero."
            )

        if self.unit not in self.VALID_UNITS:
            raise ValueError(
                f"Invalid time unit: {self.unit}"
            )

    @property
    def interval_delta(self):
        """Return the interval as a timedelta."""

        if self.unit == "seconds":
            return timedelta(
                seconds=self.interval
            )

        if self.unit == "minutes":
            return timedelta(
                minutes=self.interval
            )

        if self.unit == "hours":
            return timedelta(
                hours=self.interval
            )

        raise ValueError(
            f"Unsupported time unit: {self.unit}"
        )

    def start(self, start_time=None):
        """Start the schedule."""

        if start_time is None:
            start_time = datetime.now()

        self.last_triggered = None
        self.next_trigger = (
            start_time + self.interval_delta
        )

    def is_due(self, current_time=None):
        """Return True if the schedule is due."""

        if not self.enabled:
            return False

        if self.next_trigger is None:
            return False

        if current_time is None:
            current_time = datetime.now()

        return current_time >= self.next_trigger

    def trigger(self, trigger_time=None):
        """Trigger the schedule and calculate the next event."""

        if trigger_time is None:
            trigger_time = datetime.now()

        self.last_triggered = trigger_time

        self.next_trigger = (
            trigger_time + self.interval_delta
        )

    def time_until_next(self, current_time=None):
        """Return time remaining until the next event."""

        if current_time is None:
            current_time = datetime.now()

        if self.next_trigger is None:
            return None

        remaining = (
            self.next_trigger - current_time
        )

        if remaining.total_seconds() < 0:
            return timedelta(0)

        return remaining

    def __repr__(self):
        """Return a useful representation."""

        return (
            f"Schedule("
            f"name={self.name!r}, "
            f"interval={self.interval}, "
            f"unit={self.unit!r}, "
            f"enabled={self.enabled})"
        )