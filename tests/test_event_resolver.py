"""Test event resolution."""

from datetime import datetime

from src.core.event_resolver import EventResolver


def main():
    """Run event resolver tests."""

    print()
    print("=" * 70)
    print("MusicTimer Pro - Event Resolver Test")
    print("=" * 70)
    print()

    resolver = EventResolver()

    trigger_time = datetime(
        2026,
        8,
        17,
        12,
        0,
        0,
    )

    # --------------------------------------------------
    # Simulate simultaneous events
    # --------------------------------------------------

    events = [
        {
            "name": "Short Reminder",
            "priority": 50,
            "playlist": "upbeat",
            "trigger_time": trigger_time,
        },
        {
            "name": "Long Break",
            "priority": 100,
            "playlist": "long_music",
            "trigger_time": trigger_time,
        },
    ]

    print("Events detected at 12:00:")
    print()

    for event in events:
        print(
            f"  {event['name']} "
            f"(priority={event['priority']})"
        )

    print()

    # --------------------------------------------------
    # Resolve
    # --------------------------------------------------

    result = resolver.resolve(events)

    if result is None:
        print("ERROR: No event selected.")
        return

    print("Selected event:")
    print(
        f"  🎵 {result.name}"
    )

    print(
        f"  Playlist: {result.playlist}"
    )

    print(
        f"  Priority: {result.priority}"
    )

    print()

    print("Suppressed events:")

    for event in result.suppressed_events:

        print(
            f"  ⏭ {event['name']}"
        )

    print()

    # --------------------------------------------------
    # Verify Option C
    # --------------------------------------------------

    assert result.name == "Long Break"

    assert result.playlist == "long_music"

    assert result.priority == 100

    assert len(
        result.suppressed_events
    ) == 1

    assert (
        result.suppressed_events[0]["name"]
        == "Short Reminder"
    )

    print(
        "✓ Option C behavior verified."
    )

    print()

    print("=" * 70)
    print("Event resolver test completed successfully.")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()