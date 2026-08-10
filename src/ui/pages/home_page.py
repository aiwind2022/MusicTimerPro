"""Home page."""

import customtkinter as ctk


class HomePage(ctk.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        title = ctk.CTkLabel(
            self,
            text="Welcome to MusicTimer Pro",
            font=ctk.CTkFont(size=30, weight="bold"),
        )

        title.pack(
            padx=30,
            pady=(30, 10),
            anchor="w",
        )

        description = ctk.CTkLabel(
            self,
            text=(
                "Schedule your music playback with a simple "
                "and flexible timer."
            ),
            font=ctk.CTkFont(size=16),
        )

        description.pack(
            padx=30,
            pady=10,
            anchor="w",
        )

        info = ctk.CTkLabel(
            self,
            text="Use the Timer page to configure your playback interval.",
            font=ctk.CTkFont(size=14),
        )

        info.pack(
            padx=30,
            pady=20,
            anchor="w",
        )