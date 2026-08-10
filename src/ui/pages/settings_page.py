"""Settings page."""

import customtkinter as ctk


class SettingsPage(ctk.CTkFrame):

    def __init__(self, master, config_manager, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.config_manager = config_manager

        self._create_widgets()

    def _create_widgets(self):

        title = ctk.CTkLabel(
            self,
            text="Settings",
            font=ctk.CTkFont(size=30, weight="bold"),
        )

        title.pack(
            padx=30,
            pady=(30, 30),
            anchor="w",
        )

        appearance_label = ctk.CTkLabel(
            self,
            text="Appearance",
            font=ctk.CTkFont(size=16),
        )

        appearance_label.pack(
            padx=30,
            pady=(10, 5),
            anchor="w",
        )

        self.appearance_menu = ctk.CTkOptionMenu(
            self,
            values=["Dark", "Light", "System"],
            command=self.change_appearance,
        )

        self.appearance_menu.pack(
            padx=30,
            pady=10,
            anchor="w",
        )

        current_mode = self.config_manager.get(
            "appearance_mode",
            "dark",
        )

        self.appearance_menu.set(
            current_mode.capitalize()
        )

    def change_appearance(self, value):

        mode = value.lower()

        ctk.set_appearance_mode(mode)

        self.config_manager.set(
            "appearance_mode",
            mode,
        )