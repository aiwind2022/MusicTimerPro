"""Test the MusicTimer Pro scheduling system."""

from datetime import datetime, timedelta

from src.core.schedule import Schedule
from src.core.schedule_manager import ScheduleManager


def main():
    """Run schedule tests."""

    print()
    print("=" * 60)
    print("MusicTimer Pro - Schedule System Test")
    print("=" * 60)
    print()

    # --------------------------------------------------
    # Create schedules
    # --------------------------------------------------

    short_schedule = Schedule(
        name="Short Reminder",
        interval=15,
        unit="minutes",
        playlist="upbeat",
    )

    long_schedule = Schedule(
        name="Long Break",
        interval=4,
        unit="hours",
        playlist="long_music",
    )

    # --------------------------------------------------
    # Create manager
    # --------------------------------------------------

    manager = ScheduleManager()

    manager.add_schedule(
        short_schedule
    )

    manager.add_schedule(
        long_schedule
    )

    # --------------------------------------------------
    # Use a fixed start time
    # --------------------------------------------------

    start_time = datetime(
        2026,
        8,
        14,
        8,
        0,
        0,
    )

    manager.start_all(start_time)

    print(
        f"Start time: {start_time}"
    )

    print()

    # --------------------------------------------------
    # Display initial schedules
    # --------------------------------------------------

    for schedule in manager.schedules:

        print(
            f"{schedule.name}:"
        )

        print(
            f"  Interval: "
            f"{schedule.interval} "
            f"{schedule.unit}"
        )

        print(
            f"  Playlist: "
            f"{schedule.playlist}"
        )

        print(
            f"  Next trigger: "
            f"{schedule.next_trigger}"
        )

        print()

    # --------------------------------------------------
    # Test 15-minute event
    # --------------------------------------------------

    test_time = start_time + timedelta(
        minutes=15
    )

    due = manager.get_due_schedules(
        test_time
    )

    print(
        f"At {test_time}"
    )

    print("Due schedules:")

    for schedule in due:

        print(
            f"  🎵 {schedule.name}"
        )

        manager.trigger_schedule(
            schedule,
            test_time,
        )

    print()

    # --------------------------------------------------
    # Test four-hour event
    # --------------------------------------------------

    test_time = start_time + timedelta(
        hours=4
    )

    due = manager.get_due_schedules(
        test_time
    )

    print(
        f"At {test_time}"
    )

    print("Due schedules:")

    for schedule in due:

        print(
            f"  🎵 {schedule.name}"
        )

        manager.trigger_schedule(
            schedule,
            test_time,
        )

    print()

    # --------------------------------------------------
    # Find next schedule
    # --------------------------------------------------

    test_time = start_time + timedelta(
        hours=4,
        minutes=1,
    )

    next_schedule = (
        manager.get_next_schedule(
            test_time
        )
    )

    if next_schedule:

        print(
            "Next schedule:"
        )

        print(
            f"  {next_schedule.name}"
        )

        print(
            f"  {next_schedule.next_trigger}"
        )

    print()

    print("=" * 60)
    print("Schedule test completed.")
    print("=" * 60)
    print()


if __name__ == "__main__":
    main()