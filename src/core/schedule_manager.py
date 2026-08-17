"""Schedule manager for MusicTimer Pro."""

from datetime import datetime

from .schedule import Schedule


class ScheduleManager:
    """Manage multiple independent schedules."""

    def __init__(self, logger=None):
        self.logger = logger
        self.schedules = []

    def add_schedule(self, schedule):
        """Add a schedule."""

        if not isinstance(schedule, Schedule):
            raise TypeError(
                "schedule must be a Schedule object."
            )

        self.schedules.append(schedule)

        self._log(
            f"Added schedule: {schedule.name}"
        )

    def remove_schedule(self, name):
        """Remove a schedule by name."""

        for schedule in self.schedules:

            if schedule.name == name:

                self.schedules.remove(
                    schedule
                )

                self._log(
                    f"Removed schedule: {name}"
                )

                return True

        return False

    def get_schedule(self, name):
        """Return a schedule by name."""

        for schedule in self.schedules:

            if schedule.name == name:
                return schedule

        return None

    def start_all(self, start_time=None):
        """Start all enabled schedules."""

        if start_time is None:
            start_time = datetime.now()

        for schedule in self.schedules:

            if schedule.enabled:
                schedule.start(
                    start_time
                )

                self._log(
                    f"Started schedule: "
                    f"{schedule.name}"
                )

    def get_due_schedules(
        self,
        current_time=None,
    ):
        """Return all schedules that are due."""

        if current_time is None:
            current_time = datetime.now()

        due = []

        for schedule in self.schedules:

            if schedule.is_due(
                current_time
            ):
                due.append(schedule)

        return due

    def trigger_schedule(
        self,
        schedule,
        trigger_time=None,
    ):
        """Trigger one schedule."""

        if schedule not in self.schedules:
            return False

        schedule.trigger(
            trigger_time
        )

        self._log(
            f"Triggered schedule: "
            f"{schedule.name}"
        )

        return True

    def get_next_schedule(
        self,
        current_time=None,
    ):
        """Return the next upcoming schedule."""

        if current_time is None:
            current_time = datetime.now()

        upcoming = [
            schedule
            for schedule in self.schedules
            if schedule.enabled
            and schedule.next_trigger is not None
            and schedule.next_trigger > current_time
        ]

        if not upcoming:
            return None

        return min(
            upcoming,
            key=lambda schedule:
                schedule.next_trigger,
        )

    def clear(self):
        """Remove all schedules."""

        self.schedules.clear()

        self._log(
            "All schedules removed."
        )

    def _log(self, message):
        """Write to the application logger."""

        if self.logger is not None:
            self.logger.info(message)