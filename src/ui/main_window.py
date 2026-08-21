"""Main application window."""

import customtkinter as ctk

from pathlib import Path

from .sidebar import Sidebar
from ..media.audio_player import AudioPlayer

from ..core.media import Media
from ..core.playlist_manager import PlaylistManager
from ..core.playback_controller import PlaybackController

from .pages.home_page import HomePage
from .pages.timer_page import TimerPage
from .pages.playlist_page import PlaylistPage
from .pages.settings_page import SettingsPage
from .pages.about_page import AboutPage

from ..core.constants import (
    APP_NAME,
    MIN_WINDOW_HEIGHT,
    MIN_WINDOW_WIDTH,
)


class MainWindow(ctk.CTk):
    """Main MusicTimer Pro application window."""

    def __init__(self, config_manager, logger):

        super().__init__()

        self.config_manager = config_manager
        self.logger = logger

        self.audio_player = AudioPlayer()

        self.playlist_manager = PlaylistManager()

        self.playback_controller = PlaybackController(
            playlist_manager=self.playlist_manager,
            media_player=self.audio_player,
            logger=self.logger,
        )

        # Temporary Sprint 1.6F test playlist
        test_playlist = self.playlist_manager.create(
            "upbeat",
            "Short upbeat reminder music.",
        )

        test_media_path = (
            Path(__file__).resolve().parents[2]
            / "test_media"
            / "upbeat.mp3"
        )

        if test_media_path.exists():
            test_media = Media(
            path=test_media_path,
            title="Upbeat Test Music",
            )

            test_playlist.add(test_media)

            self.logger.info(
                f"Test media added: {test_media_path}"
            )
        else:
            self.logger.warning(
            f"Test media not found: {test_media_path}"
        )
        # Temporary Sprint 1.6F test playlist
        #if self.playlist_manager.get("upbeat") is None:
        #   self.playlist_manager.create(
        #  "upbeat",
        # "Short upbeat reminder music.",
        #)
            
        self.title(APP_NAME)

        width = self.config_manager.get(
            "window_width",
            1100,
        )

        height = self.config_manager.get(
            "window_height",
            700,
        )

        self.geometry(
            f"{width}x{height}"
        )

        self.minsize(
            MIN_WINDOW_WIDTH,
            MIN_WINDOW_HEIGHT,
        )

        appearance_mode = self.config_manager.get(
            "appearance_mode",
            "dark",
        )

        ctk.set_appearance_mode(
            appearance_mode
        )

        ctk.set_default_color_theme(
            "blue"
        )

        # Create the page dictionary BEFORE creating
        # the sidebar. The sidebar immediately calls
        # show_page("home") during initialization.
        self.pages = {}

        self._create_layout()

        self.protocol(
            "WM_DELETE_WINDOW",
            self._on_close,
        )

        self.logger.info(
            "Main window initialized."
        )

    def _create_layout(self):
        """Create the main application layout."""

        self.grid_columnconfigure(
            0,
            weight=0,
        )

        self.grid_columnconfigure(
            1,
            weight=1,
        )

        self.grid_rowconfigure(
            0,
            weight=1,
        )

        self.grid_rowconfigure(
            1,
            weight=0,
        )

        # -------------------------------------------------
        # Content frame
        # -------------------------------------------------

        self.content_frame = ctk.CTkFrame(
            self,
            corner_radius=0,
        )

        self.content_frame.grid(
            row=0,
            column=1,
            sticky="nsew",
        )

        self.content_frame.grid_rowconfigure(
            0,
            weight=1,
        )

        self.content_frame.grid_columnconfigure(
            0,
            weight=1,
        )

        # -------------------------------------------------
        # Status bar
        # -------------------------------------------------

        self.status_bar = ctk.CTkLabel(
            self,
            text="Ready",
            anchor="w",
            height=28,
        )

        self.status_bar.grid(
            row=1,
            column=1,
            sticky="ew",
        )

        # -------------------------------------------------
        # Create application pages
        # -------------------------------------------------

        self.pages = {
            "home": HomePage(
                self.content_frame
            ),

            "timer": TimerPage(
                 self.content_frame,
                 config_manager=self.config_manager,
                 logger=self.logger,
                 audio_player=self.audio_player,
                 playlist_manager=self.playlist_manager,
                 playback_controller=self.playback_controller,                
             ),

            "playlist": PlaylistPage(
                self.content_frame
            ),

            "settings": SettingsPage(
                self.content_frame,
                self.config_manager,
            ),

            "about": AboutPage(
                self.content_frame
            ),
        }

        # -------------------------------------------------
        # Sidebar
        # -------------------------------------------------

        self.sidebar = Sidebar(
            self,
            self.show_page,
        )

        self.sidebar.grid(
            row=0,
            column=0,
            rowspan=2,
            sticky="nsew",
        )

        # The Sidebar selects Home during initialization.
        # At this point self.pages already exists.
        self.show_page("home")

    def show_page(self, page_name: str):
        """Display the requested application page."""

        if not hasattr(self, "pages"):
            return

        for page in self.pages.values():
            page.grid_forget()

        page = self.pages.get(page_name)

        if page is not None:

            page.grid(
                row=0,
                column=0,
                sticky="nsew",
            )

            self.status_bar.configure(
                text=f"Ready | {page_name.capitalize()}"
            )

            self.logger.info(
                "Displayed page: %s",
                page_name,
            )

    def _on_close(self):
        """Save settings and close the application."""

        self.config_manager.update(
        {
            "window_width": self.winfo_width(),
            "window_height": self.winfo_height(),
        }
        )

        self.audio_player.shutdown()

        self.logger.info(
            "Application closing."
        )

        self.destroy()