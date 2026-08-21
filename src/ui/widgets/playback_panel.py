"""Playback controls for MusicTimer Pro."""

import customtkinter as ctk


class PlaybackPanel(ctk.CTkFrame):
    """
    GUI controls for media playback.

    The panel communicates with a playback controller
    supplied by the application.
    """

    def __init__(
        self,
        master,
        playback_controller=None,
        **kwargs,
    ):
        super().__init__(
            master,
            **kwargs,
        )

        self.playback_controller = (
            playback_controller
        )

        self.current_event = None
        self.current_playlist = None

        self._create_widgets()

    # ==================================================
    # GUI
    # ==================================================

    def _create_widgets(self):

        self.title_label = ctk.CTkLabel(
            self,
            text="Playback",
            font=ctk.CTkFont(
                size=20,
                weight="bold",
            ),
        )

        self.title_label.pack(
            padx=20,
            pady=(15, 10),
            anchor="w",
        )

        # ----------------------------------------------
        # Event
        # ----------------------------------------------

        self.event_label = ctk.CTkLabel(
            self,
            text="Event: None",
            anchor="w",
        )

        self.event_label.pack(
            padx=20,
            pady=3,
            fill="x",
        )

        # ----------------------------------------------
        # Playlist
        # ----------------------------------------------

        self.playlist_label = ctk.CTkLabel(
            self,
            text="Playlist: None",
            anchor="w",
        )

        self.playlist_label.pack(
            padx=20,
            pady=3,
            fill="x",
        )

        # ----------------------------------------------
        # Status
        # ----------------------------------------------

        self.status_label = ctk.CTkLabel(
            self,
            text="Status: Ready",
            anchor="w",
        )

        self.status_label.pack(
            padx=20,
            pady=3,
            fill="x",
        )

        # ----------------------------------------------
        # Buttons
        # ----------------------------------------------

        self.button_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )

        self.button_frame.pack(
            padx=20,
            pady=15,
            fill="x",
        )

        self.play_button = ctk.CTkButton(
            self.button_frame,
            text="▶ Play",
            command=self._play,
            width=100,
        )

        self.play_button.pack(
            side="left",
            padx=(0, 5),
        )

        self.pause_button = ctk.CTkButton(
            self.button_frame,
            text="⏸ Pause",
            command=self._pause,
            width=100,
        )

        self.pause_button.pack(
            side="left",
            padx=5,
        )

        self.stop_button = ctk.CTkButton(
            self.button_frame,
            text="⏹ Stop",
            command=self._stop,
            width=100,
        )

        self.stop_button.pack(
            side="left",
            padx=5,
        )

    # ==================================================
    # Public API
    # ==================================================

    def set_event(
        self,
        event,
    ):
        """
        Display the current scheduler event.
        """

        self.current_event = event

        if event is None:

            self.event_label.configure(
                text="Event: None"
            )

            self.playlist_label.configure(
                text="Playlist: None"
            )

            return

        self.event_label.configure(
            text=(
                f"Event: {event.name}"
            )
        )

        self.playlist_label.configure(
            text=(
                f"Playlist: "
                f"{event.playlist}"
            )
        )

    def set_status(
        self,
        status,
    ):
        """Update playback status."""

        self.status_label.configure(
            text=f"Status: {status}"
        )

    # ==================================================
    # Playback
    # ==================================================

    def _play(self):

        if (
            self.playback_controller is None
        ):
            self.set_status(
                "No playback controller"
            )
            return

        if self.current_event is None:

            self.set_status(
                "No event selected"
            )

            return

        try:

            media = (
                self.playback_controller
                .play_event(
                    self.current_event
                )
            )

            if media is not None:

                self.set_status(
                    f"Playing: "
                    f"{media.title}"
                )

            else:

                self.set_status(
                    "No playable media"
                )

        except Exception as exc:

            self.set_status(
                f"Playback error: {exc}"
            )

    def _pause(self):

        if (
            self.playback_controller is None
        ):
            return

        self.playback_controller.pause()

        self.set_status(
            "Paused"
        )

    def _stop(self):

        if (
            self.playback_controller is None
        ):
            return

        self.playback_controller.stop()

        self.set_status(
            "Stopped"
        )