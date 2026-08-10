"""About page."""

import customtkinter as ctk

from ...core.constants import APP_NAME, APP_VERSION


class AboutPage(ctk.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        title = ctk.CTkLabel(
            self,
            text=APP_NAME,
            font=ctk.CTkFont(
                size=32,
                weight="bold",
            ),
        )

        title.pack(
            pady=(60, 10),
        )

        version = ctk.CTkLabel(
            self,
            text=f"Version {APP_VERSION}",
            font=ctk.CTkFont(size=16),
        )

        version.pack(pady=10)

        description = ctk.CTkLabel(
            self,
            text=(
                "A modern desktop music timer application\n"
                "for scheduled music playback."
            ),
            justify="center",
            font=ctk.CTkFont(size=15),
        )

        description.pack(pady=30)