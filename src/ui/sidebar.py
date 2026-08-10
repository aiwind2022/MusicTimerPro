"""Sidebar navigation for MusicTimer Pro."""

import customtkinter as ctk


class Sidebar(ctk.CTkFrame):
    """Application navigation sidebar."""

    def __init__(self, master, on_page_change, **kwargs):
        super().__init__(master, width=220, corner_radius=0, **kwargs)

        self.on_page_change = on_page_change

        self.grid_propagate(False)

        self._create_widgets()

    def _create_widgets(self):
        """Create sidebar controls."""

        self.logo_label = ctk.CTkLabel(
            self,
            text="🎵 MusicTimer\nPro",
            font=ctk.CTkFont(
                size=24,
                weight="bold",
            ),
        )

        self.logo_label.pack(
            padx=20,
            pady=(30, 40),
        )

        self.buttons = {}

        navigation = [
            ("home", "🏠  Home"),
            ("timer", "⏱  Timer"),
            ("playlist", "🎵  Playlist"),
            ("settings", "⚙  Settings"),
            ("about", "ℹ  About"),
        ]

        for page_name, text in navigation:
            button = ctk.CTkButton(
                self,
                text=text,
                height=42,
                anchor="w",
                fg_color="transparent",
                hover_color=("gray75", "gray25"),
                command=lambda page=page_name: self._select_page(page),
            )

            button.pack(
                fill="x",
                padx=15,
                pady=5,
            )

            self.buttons[page_name] = button

        self._select_page("home")

    def _select_page(self, page_name: str):
        """Select a page."""

        for name, button in self.buttons.items():
            if name == page_name:
                button.configure(
                    fg_color=("gray80", "gray20")
                )
            else:
                button.configure(
                    fg_color="transparent"
                )

        self.on_page_change(page_name)