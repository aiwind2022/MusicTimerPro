"""Playlist page."""

import customtkinter as ctk


class PlaylistPage(ctk.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        title = ctk.CTkLabel(
            self,
            text="Playlist",
            font=ctk.CTkFont(size=30, weight="bold"),
        )

        title.pack(
            padx=30,
            pady=(30, 20),
            anchor="w",
        )

        self.info_label = ctk.CTkLabel(
            self,
            text="Playlist management will be added in Phase 2.",
            font=ctk.CTkFont(size=16),
        )

        self.info_label.pack(
            padx=30,
            pady=20,
            anchor="w",
        )