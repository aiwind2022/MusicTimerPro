"""Timer page."""

import customtkinter as ctk


class TimerPage(ctk.CTkFrame):

    def __init__(self, master, config_manager, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.config_manager = config_manager

        self.running = False

        self._create_widgets()

    def _create_widgets(self):
        """Create timer controls."""

        title = ctk.CTkLabel(
            self,
            text="Timer",
            font=ctk.CTkFont(size=30, weight="bold"),
        )

        title.pack(
            padx=30,
            pady=(30, 30),
            anchor="w",
        )

        interval_frame = ctk.CTkFrame(self)

        interval_frame.pack(
            padx=30,
            pady=10,
            fill="x",
        )

        label = ctk.CTkLabel(
            interval_frame,
            text="Interval (minutes):",
            font=ctk.CTkFont(size=16),
        )

        label.pack(
            side="left",
            padx=20,
            pady=20,
        )

        self.interval_entry = ctk.CTkEntry(
            interval_frame,
            width=100,
        )

        self.interval_entry.pack(
            side="left",
            padx=10,
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

        self.countdown_label = ctk.CTkLabel(
            self,
            text="15:00",
            font=ctk.CTkFont(
                size=64,
                weight="bold",
            ),
        )

        self.countdown_label.pack(
            pady=50,
        )

        button_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )

        button_frame.pack()

        self.start_button = ctk.CTkButton(
            button_frame,
            text="▶ Start",
            width=120,
            height=40,
            command=self.start_timer,
        )

        self.start_button.pack(
            side="left",
            padx=10,
        )

        self.stop_button = ctk.CTkButton(
            button_frame,
            text="■ Stop",
            width=120,
            height=40,
            fg_color="#8B0000",
            hover_color="#A00000",
            command=self.stop_timer,
        )

        self.stop_button.pack(
            side="left",
            padx=10,
        )

        self.status_label = ctk.CTkLabel(
            self,
            text="Status: Ready",
        )

        self.status_label.pack(
            pady=30,
        )

    def start_timer(self):
        """Start timer placeholder."""

        self.running = True

        self.status_label.configure(
            text="Status: Timer running"
        )

        self.start_button.configure(
            state="disabled"
        )

    def stop_timer(self):
        """Stop timer placeholder."""

        self.running = False

        self.status_label.configure(
            text="Status: Ready"
        )

        self.start_button.configure(
            state="normal"
        )