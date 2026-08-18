"""Scheduler engine for MusicTimer Pro."""

from datetime import datetime

from .event_resolver import EventResolver
from .schedule_manager import ScheduleManager


class Scheduler:
    """
    Coordinate multiple independent schedules.

    The Scheduler determines when schedules are due.
    EventResolver determines which event should be played
    when multiple schedules occur at the same time.

    The Scheduler does not play media directly.
    """

    def __init__(
        self,
        schedule_manager=None,
        event_resolver=None,
        logger=None,
    ):
        self.schedule_manager = (
            schedule_manager
            if schedule_manager is not None
            else ScheduleManager(logger=logger)
        )

        self.event_resolver = (
            event_resolver
            if event_resolver is not None
            else EventResolver(logger=logger)
        )

        self.logger = logger

        self.running = False
        self.started_at = None

        self.default_priority = 50
        self._priorities = {}

    # ==================================================
    # Schedule management
    # ==================================================

    def add_schedule(
        self,
        schedule,
        priority=None,
    ):
        """Add a schedule to the scheduler."""

        self.schedule_manager.add_schedule(
            schedule
        )

        if priority is None:
            priority = self.default_priority

        self._priorities[
            schedule.name
        ] = priority

        self._log(
            f"Scheduler added: {schedule.name} "
            f"(priority={priority})"
        )

    def remove_schedule(self, name):
        """Remove a schedule."""

        removed = (
            self.schedule_manager
            .remove_schedule(name)
        )

        if removed:
            self._priorities.pop(
                name,
                None,
            )

        return removed

    def set_priority(
        self,
        schedule_name,
        priority,
    ):
        """Set schedule priority."""

        if not isinstance(priority, int):
            raise ValueError(
                "Priority must be an integer."
            )

        schedule = (
            self.schedule_manager
            .get_schedule(schedule_name)
        )

        if schedule is None:
            return False

        self._priorities[
            schedule_name
        ] = priority

        return True

    def get_priority(
        self,
        schedule_name,
    ):
        """Return schedule priority."""

        return self._priorities.get(
            schedule_name,
            self.default_priority,
        )

    # ==================================================
    # Lifecycle
    # ==================================================

    def start(self, start_time=None):
        """Start all enabled schedules."""

        if start_time is None:
            start_time = datetime.now()

        self.schedule_manager.start_all(
            start_time
        )

        self.running = True
        self.started_at = start_time

        self._log(
            f"Scheduler started at {start_time}"
        )

    def stop(self):
        """Stop the scheduler."""

        self.running = False

        self._log(
            "Scheduler stopped."
        )

    # ==================================================
    # Due events
    # ==================================================

    def get_due_events(
        self,
        current_time=None,
    ):
        """
        Return all schedules currently due.

        This method does not resolve competing events.
        """

        if not self.running:
            return []

        if current_time is None:
            current_time = datetime.now()

        due_schedules = (
            self.schedule_manager
            .get_due_schedules(
                current_time
            )
        )

        events = []

        for schedule in due_schedules:

            events.append(
                {
                    "schedule": schedule,
                    "name": schedule.name,
                    "priority": self.get_priority(
                        schedule.name
                    ),
                    "playlist": schedule.playlist,
                    "trigger_time": current_time,
                }
            )

        return events

    # ==================================================
    # Event resolution
    # ==================================================

    def resolve_events(
        self,
        current_time=None,
    ):
        """
        Find due events and select the highest-priority event.

        Returns:
            ResolvedEvent or None.
        """

        events = self.get_due_events(
            current_time
        )

        if not events:
            return None

        resolved = (
            self.event_resolver.resolve(
                events
            )
        )

        return resolved

    # ==================================================
    # Process events
    # ==================================================

    def process(
        self,
        current_time=None,
    ):
        """
        Process all schedules due at current_time.

        The highest-priority event is selected for playback.

        All due schedules are advanced so that suppressed
        lower-priority events do not become stuck.
        """

        if not self.running:
            return None

        if current_time is None:
            current_time = datetime.now()

        events = self.get_due_events(
            current_time
        )

        if not events:
            return None

        resolved = (
            self.event_resolver.resolve(
                events
            )
        )

        # Advance EVERY due schedule.
        #
        # This is important for Option C:
        # a suppressed short reminder should still
        # continue its normal 15-minute schedule.
        for event in events:

            schedule = event[
                "schedule"
            ]

            self.schedule_manager.trigger_schedule(
                schedule,
                current_time,
            )

        self._log(
            f"Selected event: "
            f"{resolved.name}"
        )

        return resolved

    # ==================================================
    # Next event
    # ==================================================

    def get_next_event(
        self,
        current_time=None,
    ):
        """Return the next scheduled event."""

        if current_time is None:
            current_time = datetime.now()

        schedule = (
            self.schedule_manager
            .get_next_schedule(
                current_time
            )
        )

        if schedule is None:
            return None

        return {
            "schedule": schedule,
            "name": schedule.name,
            "priority": self.get_priority(
                schedule.name
            ),
            "playlist": schedule.playlist,
            "next_trigger": schedule.next_trigger,
        }

    # ==================================================
    # Status
    # ==================================================

    def get_status(
        self,
        current_time=None,
    ):
        """Return scheduler status."""

        if current_time is None:
            current_time = datetime.now()

        schedules = []

        for schedule in (
            self.schedule_manager.schedules
        ):

            schedules.append(
                {
                    "name": schedule.name,
                    "enabled": schedule.enabled,
                    "interval": schedule.interval,
                    "unit": schedule.unit,
                    "playlist": schedule.playlist,
                    "priority": self.get_priority(
                        schedule.name
                    ),
                    "next_trigger": (
                        schedule.next_trigger
                    ),
                    "time_remaining": (
                        schedule.time_until_next(
                            current_time
                        )
                    ),
                }
            )

        return {
            "running": self.running,
            "started_at": self.started_at,
            "schedules": schedules,
        }

    # ==================================================
    # Logging
    # ==================================================

    def _log(self, message):
        """Write to the application logger."""

        if self.logger is not None:
            self.logger.info(message)