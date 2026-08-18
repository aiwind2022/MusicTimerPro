"""Scheduler engine for MusicTimer Pro."""

from datetime import datetime

from .schedule_manager import ScheduleManager


class Scheduler:
    """
    Coordinate multiple independent music schedules.

    The Scheduler is responsible for deciding WHAT event
    should happen and WHEN it should happen.

    It does not play music directly. Audio playback remains
    the responsibility of AudioPlayer.
    """

    def __init__(
        self,
        schedule_manager=None,
        logger=None,
    ):
        self.schedule_manager = (
            schedule_manager
            if schedule_manager is not None
            else ScheduleManager(logger=logger)
        )

        self.logger = logger

        self.running = False
        self.started_at = None

        # Higher number = higher priority.
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
        """
        Add a schedule to the scheduler.

        Args:
            schedule: Schedule object.
            priority: Optional integer priority.
        """

        self.schedule_manager.add_schedule(
            schedule
        )

        if priority is None:
            priority = self.default_priority

        self._priorities[
            schedule.name
        ] = priority

        self._log(
            f"Scheduler added: "
            f"{schedule.name} "
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

        self._log(
            f"Priority changed: "
            f"{schedule_name} = {priority}"
        )

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
    # Scheduler lifecycle
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
            f"Scheduler started at "
            f"{start_time}"
        )

    def stop(self):
        """Stop the scheduler."""

        self.running = False

        self._log(
            "Scheduler stopped."
        )

    # ==================================================
    # Event processing
    # ==================================================

    def check(self, current_time=None):
        """
        Check for due schedules.

        Returns:
            A list of schedule events ordered by priority.
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

        if not due_schedules:
            return []

        # Sort highest priority first.
        due_schedules.sort(
            key=lambda schedule:
                self.get_priority(
                    schedule.name
                ),
            reverse=True,
        )

        events = []

        for schedule in due_schedules:

            priority = self.get_priority(
                schedule.name
            )

            events.append(
                {
                    "schedule": schedule,
                    "name": schedule.name,
                    "priority": priority,
                    "playlist": schedule.playlist,
                    "trigger_time": current_time,
                }
            )

        return events

    def process(self, current_time=None):
        """
        Check and process all due schedules.

        The returned events represent actions that should
        be handled by the application/audio system.
        """

        if current_time is None:
            current_time = datetime.now()

        events = self.check(
            current_time
        )

        if not events:
            return []

        processed = []

        for event in events:

            schedule = event[
                "schedule"
            ]

            self._log(
                f"Processing schedule: "
                f"{schedule.name}"
            )

            self.schedule_manager.trigger_schedule(
                schedule,
                current_time,
            )

            processed.append(
                event
            )

        return processed

    # ==================================================
    # Next event
    # ==================================================

    def get_next_event(
        self,
        current_time=None,
    ):
        """
        Return the next scheduled event.

        Returns:
            Dictionary containing schedule information,
            or None if no event exists.
        """

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
        """Return scheduler status information."""

        if current_time is None:
            current_time = datetime.now()

        schedules = []

        for schedule in (
            self.schedule_manager.schedules
        ):

            remaining = (
                schedule.time_until_next(
                    current_time
                )
            )

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
                    "time_remaining": remaining,
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