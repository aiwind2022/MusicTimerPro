"""Basic PlaybackPanel GUI test."""

import customtkinter as ctk

from src.ui.widgets.playback_panel import (
    PlaybackPanel,
)


class DummyController:
    """Simple controller for GUI testing."""

    def __init__(self):
        self.played = False
        self.paused = False
        self.stopped = False

    def play_event(self, event):

        self.played = True

        class DummyMedia:
            title = "Test Music"

        return DummyMedia()

    def pause(self):
        self.paused = True

    def stop(self):
        self.stopped = True


class TestEvent:
    name = "Short Reminder"
    playlist = "upbeat"
    priority = 50


def main():

    print()
    print("=" * 70)
    print(
        "MusicTimer Pro - Playback Panel Test"
    )
    print("=" * 70)
    print()

    root = ctk.CTk()

    root.title(
        "Playback Panel Test"
    )

    root.geometry(
        "600x400"
    )

    controller = DummyController()

    panel = PlaybackPanel(
        root,
        playback_controller=controller,
    )

    panel.pack(
        padx=20,
        pady=20,
        fill="both",
        expand=True,
    )

    event = TestEvent()

    panel.set_event(event)

    print(
        "✓ PlaybackPanel created."
    )

    print(
        "✓ Event information displayed."
    )

    print()
    print(
        "A test window will open."
    )

    print(
        "Click Play, Pause, and Stop."
    )

    print()

    root.mainloop()

    print()
    print("=" * 70)
    print(
        "PlaybackPanel test completed."
    )
    print("=" * 70)


if __name__ == "__main__":
    main()