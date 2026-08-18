"""Integration test for Scheduler and EventResolver."""

from datetime import datetime, timedelta

from src.core.schedule import Schedule
from src.core.scheduler import Scheduler


def main():
    """Run the scheduler integration test."""

    print()
    print("=" * 70)
    print("MusicTimer Pro - Scheduler Integration Test")
    print("=" * 70)
    print()

    scheduler = Scheduler()

    # --------------------------------------------------
    # Short reminder
    # --------------------------------------------------

    short_schedule = Schedule(
        name="Short Reminder",
        interval=15,
        unit="minutes",
        playlist="upbeat",
    )

    # --------------------------------------------------
    # Long break
    # --------------------------------------------------

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
    # Start simulation
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
        f"Started: {start_time}"
    )

    print()
    print("Simulating 8 hours...")
    print()

    current_time = start_time

    end_time = (
        start_time
        + timedelta(hours=8)
    )

    events = []

    while current_time <= end_time:

        result = scheduler.process(
            current_time
        )

        if result is not None:

            events.append(
                (
                    current_time,
                    result,
                )
            )

            print(
                current_time.strftime(
                    "%H:%M:%S"
                ),
                end="  ",
            )

            print(
                f"🎵 {result.name}"
                f" | priority={result.priority}"
                f" | playlist={result.playlist}"
            )

            if result.suppressed_events:

                for suppressed in (
                    result.suppressed_events
                ):

                    print(
                        f"       "
                        f"⏭ Suppressed: "
                        f"{suppressed['name']}"
                    )

        current_time += timedelta(
            minutes=1
        )

    # --------------------------------------------------
    # Test expected results
    # --------------------------------------------------

    print()
    print("-" * 70)
    print("Running assertions...")
    print()

    # 32 short events + 2 long events
    #
    # However, two collisions occur:
    # 12:00 and 16:00.
    #
    # The resolver selects Long Break at those times.
    #
    # Therefore the PLAYBACK event count is:
    #
    # 30 short + 2 long = 32 selected events.

    assert len(events) == 32, (
        f"Expected 32 selected events, "
        f"got {len(events)}"
    )

    # --------------------------------------------------
    # Check 12:00
    # --------------------------------------------------

    noon_events = [
        event
        for event in events
        if event[0].hour == 12
        and event[0].minute == 0
    ]

    assert len(noon_events) == 1

    noon_result = noon_events[0][1]

    assert (
        noon_result.name
        == "Long Break"
    )

    assert (
        noon_result.playlist
        == "long_music"
    )

    assert (
        len(noon_result.suppressed_events)
        == 1
    )

    assert (
        noon_result.suppressed_events[0]["name"]
        == "Short Reminder"
    )

    print(
        "✓ 12:00 collision resolved correctly."
    )

    # --------------------------------------------------
    # Check 16:00
    # --------------------------------------------------

    four_pm_events = [
        event
        for event in events
        if event[0].hour == 16
        and event[0].minute == 0
    ]

    assert len(four_pm_events) == 1

    four_pm_result = (
        four_pm_events[0][1]
    )

    assert (
        four_pm_result.name
        == "Long Break"
    )

    assert (
        len(
            four_pm_result.suppressed_events
        )
        == 1
    )

    print(
        "✓ 16:00 collision resolved correctly."
    )

    # --------------------------------------------------
    # Check next short reminder
    # --------------------------------------------------

    final_time = (
        start_time
        + timedelta(hours=8)
    )

    next_event = (
        scheduler.get_next_event(
            final_time
        )
    )

    assert next_event is not None

    assert (
        next_event["name"]
        == "Short Reminder"
    )

    assert (
        next_event["next_trigger"]
        == datetime(
            2026,
            8,
            17,
            16,
            15,
            0,
        )
    )

    print(
        "✓ Short reminder schedule "
        "continues normally."
    )

    # --------------------------------------------------
    # Check scheduler status
    # --------------------------------------------------

    status = scheduler.get_status(
        final_time
    )

    assert status["running"] is True

    print(
        "✓ Scheduler remains running."
    )

    print()
    print("-" * 70)
    print(
        "All Scheduler integration tests passed!"
    )
    print("-" * 70)
    print()


if __name__ == "__main__":
    main()