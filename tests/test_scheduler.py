"""Test the MusicTimer Pro Scheduler."""

from datetime import datetime, timedelta

from src.core.schedule import Schedule
from src.core.scheduler import Scheduler


def print_event(event):
    """Display a scheduler event."""

    print(
        f"  🎵 {event['name']} "
        f"| priority={event['priority']} "
        f"| playlist={event['playlist']}"
    )


def main():
    """Run scheduler tests."""

    print()
    print("=" * 70)
    print("MusicTimer Pro - Scheduler Test")
    print("=" * 70)
    print()

    # --------------------------------------------------
    # Create scheduler
    # --------------------------------------------------

    scheduler = Scheduler()

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
    # Add schedules
    # --------------------------------------------------

    scheduler.add_schedule(
        short_schedule,
        priority=50,
    )

    scheduler.add_schedule(
        long_schedule,
        priority=100,
    )

    # --------------------------------------------------
    # Start at fixed time
    # --------------------------------------------------

    start_time = datetime(
        2026,
        8,
        17,
        8,
        0,
        0,
    )

    scheduler.start(
        start_time
    )

    print(
        f"Scheduler started: {start_time}"
    )

    print()

    # --------------------------------------------------
    # Simulate 8 hours
    # --------------------------------------------------

    print(
        "Simulating 8 hours..."
    )

    print()

    current_time = start_time

    end_time = (
        start_time
        + timedelta(hours=8)
    )

    event_count = 0

    while current_time <= end_time:

        events = scheduler.process(
            current_time
        )

        for event in events:

            event_count += 1

            print(
                current_time.strftime(
                    "%H:%M:%S"
                ),
                end="  ",
            )

            print_event(event)

        current_time += timedelta(
            minutes=1
        )

    print()

    print(
        f"Total events processed: "
        f"{event_count}"
    )

    # --------------------------------------------------
    # Check next event
    # --------------------------------------------------

    next_event = (
        scheduler.get_next_event(
            current_time
        )
    )

    print()

    if next_event:

        print(
            "Next event:"
        )

        print(
            f"  Name: "
            f"{next_event['name']}"
        )

        print(
            f"  Playlist: "
            f"{next_event['playlist']}"
        )

        print(
            f"  Priority: "
            f"{next_event['priority']}"
        )

        print(
            f"  Time: "
            f"{next_event['next_trigger']}"
        )

    else:

        print(
            "No next event found."
        )

    # --------------------------------------------------
    # Status
    # --------------------------------------------------

    print()

    status = scheduler.get_status(
        current_time
    )

    print(
        f"Scheduler running: "
        f"{status['running']}"
    )

    print()

    print("=" * 70)
    print("Scheduler test completed.")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()