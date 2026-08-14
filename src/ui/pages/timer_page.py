"""Timer page for MusicTimer Pro."""

from pathlib import Path
from tkinter import filedialog

import customtkinter as ctk


class TimerPage(ctk.CTkFrame):
    """Countdown timer and music control interface."""

    def __init__(
        self,
        master,
        config_manager,
        logger=None,
        audio_player=None,
        **kwargs,
    ):
        super().__init__(
            master,
            fg_color="transparent",
            **kwargs,
        )

        self.config_manager = config_manager
        self.logger = logger
        self.audio_player = audio_player

        # Timer state
        self.timer_running = False
        self.timer_paused = False
        self.timer_after_id = None

        self.interval_seconds = (
            self.config_manager.get(
                "interval_minutes",
                15,
            ) * 60
        )

        self.remaining_seconds = self.interval_seconds

        self._create_widgets()
        self._update_display()

    # ==================================================
    # UI
    # ==================================================

    def _create_widgets(self):
        """Create the timer interface."""

        title = ctk.CTkLabel(
            self,
            text="Timer",
            font=ctk.CTkFont(
                size=30,
                weight="bold",
            ),
        )

        title.pack(
            padx=30,
            pady=(30, 10),
            anchor="w",
        )

        description = ctk.CTkLabel(
            self,
            text=(
                "Set an interval and control "
                "music playback."
            ),
            font=ctk.CTkFont(size=14),
        )

        description.pack(
            padx=30,
            pady=(0, 20),
            anchor="w",
        )

        # --------------------------------------------------
        # Interval controls
        # --------------------------------------------------

        interval_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )

        interval_frame.pack(
            padx=30,
            pady=10,
            fill="x",
        )

        interval_label = ctk.CTkLabel(
            interval_frame,
            text="Interval:",
            font=ctk.CTkFont(size=16),
        )

        interval_label.pack(
            side="left",
            padx=(0, 10),
        )

        self.interval_entry = ctk.CTkEntry(
            interval_frame,
            width=100,
            justify="center",
        )

        self.interval_entry.pack(
            side="left",
        )

        self.interval_entry.insert(
            0,
            str(
                self.config_manager.get(
                    "interval_minutes",
                    15,
                )
            ),
        )

        minutes_label = ctk.CTkLabel(
            interval_frame,
            text="minutes",
        )

        minutes_label.pack(
            side="left",
            padx=10,
        )

        self.apply_button = ctk.CTkButton(
            interval_frame,
            text="Apply",
            width=90,
            command=self.apply_interval,
        )

        self.apply_button.pack(
            side="left",
            padx=20,
        )

        # --------------------------------------------------
        # Music selection
        # --------------------------------------------------

        music_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )

        music_frame.pack(
            padx=30,
            pady=10,
            fill="x",
        )

        music_label = ctk.CTkLabel(
            music_frame,
            text="Music:",
            font=ctk.CTkFont(size=16),
        )

        music_label.pack(
            side="left",
            padx=(0, 10),
        )

        self.music_file_label = ctk.CTkLabel(
            music_frame,
            text="No music selected",
            anchor="w",
        )

        self.music_file_label.pack(
            side="left",
            padx=10,
            fill="x",
            expand=True,
        )

        self.browse_button = ctk.CTkButton(
            music_frame,
            text="Browse",
            width=100,
            command=self.select_music,
        )

        self.browse_button.pack(
            side="right",
        )

        # --------------------------------------------------
        # Countdown display
        # --------------------------------------------------

        self.countdown_label = ctk.CTkLabel(
            self,
            text="15:00",
            font=ctk.CTkFont(
                size=72,
                weight="bold",
            ),
        )

        self.countdown_label.pack(
            pady=(30, 10),
        )

        # --------------------------------------------------
        # Timer status
        # --------------------------------------------------

        self.status_label = ctk.CTkLabel(
            self,
            text="Ready",
            font=ctk.CTkFont(size=16),
        )

        self.status_label.pack(
            pady=5,
        )

        # --------------------------------------------------
        # Timer buttons
        # --------------------------------------------------

        timer_button_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )

        timer_button_frame.pack(
            pady=10,
        )

        self.start_button = ctk.CTkButton(
            timer_button_frame,
            text="▶ Start",
            width=110,
            height=40,
            command=self.start_timer,
        )

        self.start_button.pack(
            side="left",
            padx=5,
        )

        self.pause_button = ctk.CTkButton(
            timer_button_frame,
            text="Ⅱ Pause",
            width=110,
            height=40,
            command=self.pause_timer,
            state="disabled",
        )

        self.pause_button.pack(
            side="left",
            padx=5,
        )

        self.stop_button = ctk.CTkButton(
            timer_button_frame,
            text="■ Stop",
            width=110,
            height=40,
            command=self.stop_timer,
        )

        self.stop_button.pack(
            side="left",
            padx=5,
        )

        self.reset_button = ctk.CTkButton(
            timer_button_frame,
            text="↻ Reset",
            width=110,
            height=40,
            command=self.reset_timer,
        )

        self.reset_button.pack(
            side="left",
            padx=5,
        )

        # --------------------------------------------------
        # Music buttons
        # --------------------------------------------------

        music_button_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )

        music_button_frame.pack(
            pady=5,
        )

        self.play_music_button = ctk.CTkButton(
            music_button_frame,
            text="▶ Play",
            width=110,
            command=self.play_music,
        )

        self.play_music_button.pack(
            side="left",
            padx=5,
        )

        self.pause_music_button = ctk.CTkButton(
            music_button_frame,
            text="Ⅱ Pause",
            width=110,
            command=self.pause_music,
        )

        self.pause_music_button.pack(
            side="left",
            padx=5,
        )

        self.stop_music_button = ctk.CTkButton(
            music_button_frame,
            text="■ Stop",
            width=110,
            command=self.stop_music,
        )

        self.stop_music_button.pack(
            side="left",
            padx=5,
        )

    # ==================================================
    # Interval
    # ==================================================

    def apply_interval(self):
        """Apply a new timer interval."""

        try:
            minutes = int(
                self.interval_entry.get().strip()
            )

        except ValueError:
            self.status_label.configure(
                text="Please enter a whole number."
            )
            return

        if minutes < 1:
            self.status_label.configure(
                text="Interval must be at least 1 minute."
            )
            return

        if minutes > 1440:
            self.status_label.configure(
                text="Interval cannot exceed 1440 minutes."
            )
            return

        self.interval_seconds = minutes * 60
        self.remaining_seconds = self.interval_seconds

        self.config_manager.set(
            "interval_minutes",
            minutes,
        )

        self._update_display()

        self.status_label.configure(
            text=f"Interval set to {minutes} minute(s)."
        )

        self._log(
            f"Interval changed to {minutes} minute(s)."
        )

    # ==================================================
    # Timer controls
    # ==================================================

    def start_timer(self):
        """Start or resume the timer."""

        if self.timer_running:
            return

        if self.remaining_seconds <= 0:
            self.remaining_seconds = (
                self.interval_seconds
            )

        self.timer_running = True
        self.timer_paused = False

        self.start_button.configure(
            state="disabled"
        )

        self.pause_button.configure(
            state="normal"
        )

        self.status_label.configure(
            text="Running"
        )

        self._log("Timer started.")

        self._schedule_tick()

    def pause_timer(self):
        """Pause the timer."""

        if not self.timer_running:
            return

        self.timer_running = False
        self.timer_paused = True

        self._cancel_scheduled_tick()

        self.start_button.configure(
            state="normal"
        )

        self.pause_button.configure(
            state="disabled"
        )

        self.status_label.configure(
            text="Paused"
        )

        self._log("Timer paused.")

    def stop_timer(self):
        """Stop the timer."""

        self.timer_running = False
        self.timer_paused = False

        self._cancel_scheduled_tick()

        self.remaining_seconds = (
            self.interval_seconds
        )

        self.start_button.configure(
            state="normal"
        )

        self.pause_button.configure(
            state="disabled"
        )

        self.status_label.configure(
            text="Stopped"
        )

        self._update_display()

        self._log("Timer stopped.")

    def reset_timer(self):
        """Reset the timer."""

        self.timer_running = False
        self.timer_paused = False

        self._cancel_scheduled_tick()

        self.remaining_seconds = (
            self.interval_seconds
        )

        self.start_button.configure(
            state="normal"
        )

        self.pause_button.configure(
            state="disabled"
        )

        self.status_label.configure(
            text="Ready"
        )

        self._update_display()

        self._log("Timer reset.")

    # ==================================================
    # Countdown
    # ==================================================

    def _schedule_tick(self):
        """Schedule the next countdown update."""

        self._cancel_scheduled_tick()

        if self.timer_running:
            self.timer_after_id = self.after(
                1000,
                self._timer_tick,
            )

    def _timer_tick(self):
        """Process one second of the countdown."""

        if not self.timer_running:
            return

        if self.remaining_seconds > 0:

            self.remaining_seconds -= 1

            self._update_display()

            self._schedule_tick()

        else:

            self._timer_finished()

    def _timer_finished(self):
        """Handle timer reaching zero."""

        self._log(
            "Timer interval completed."
        )

        self.status_label.configure(
            text="Interval completed."
        )

        # Trigger music playback.
        if self.audio_player is not None:

            if self.audio_player.current_file is not None:

                self.audio_player.play()

                self._log(
                    "Timer triggered music playback."
                )

        # Reset countdown for next interval.
        self.remaining_seconds = (
            self.interval_seconds
        )

        self._update_display()

        # Continue timer.
        self._schedule_tick()

    # ==================================================
    # Display
    # ==================================================

    def _update_display(self):
        """Update countdown display."""

        minutes = self.remaining_seconds // 60
        seconds = self.remaining_seconds % 60

        self.countdown_label.configure(
            text=f"{minutes:02d}:{seconds:02d}"
        )

    # ==================================================
    # Music controls
    # ==================================================

    def select_music(self):
        """Select an audio file."""

        file_path = filedialog.askopenfilename(
            title="Select Music",
            filetypes=[
                (
                    "Audio Files",
                    "*.mp3 *.wav *.ogg *.flac",
                ),
                (
                    "MP3 Files",
                    "*.mp3",
                ),
                (
                    "WAV Files",
                    "*.wav",
                ),
                (
                    "All Files",
                    "*.*",
                ),
            ],
        )

        if not file_path:
            return

        if self.audio_player is None:

            self.status_label.configure(
                text="Audio player unavailable."
            )

            return

        success = self.audio_player.load(
            file_path
        )

        if success:

            filename = Path(
                file_path
            ).name

            self.music_file_label.configure(
                text=filename
            )

            self.status_label.configure(
                text=f"Loaded: {filename}"
            )

            self._log(
                f"Selected music: {file_path}"
            )

        else:

            self.status_label.configure(
                text="Unable to load music."
            )

    def play_music(self):
        """Play selected music."""

        if self.audio_player is None:
            return

        if self.audio_player.play():

            self.status_label.configure(
                text="Playing music"
            )

    def pause_music(self):
        """Pause music."""

        if self.audio_player is None:
            return

        self.audio_player.pause()

        self.status_label.configure(
            text="Music paused"
        )

    def stop_music(self):
        """Stop music."""

        if self.audio_player is None:
            return

        self.audio_player.stop()

        self.status_label.configure(
            text="Music stopped"
        )

    # ==================================================
    # Timer cleanup
    # ==================================================

    def _cancel_scheduled_tick(self):
        """Cancel the scheduled timer callback."""

        if self.timer_after_id is not None:

            try:
                self.after_cancel(
                    self.timer_after_id
                )

            except Exception:
                pass

            self.timer_after_id = None

    # ==================================================
    # Logging
    # ==================================================

    def _log(self, message):
        """Write a message to the application logger."""

        if self.logger is not None:
            self.logger.info(message)

    # ==================================================
    # Cleanup
    # ==================================================

    def destroy(self):
        """Clean up timer resources."""

        self._cancel_scheduled_tick()

        super().destroy()