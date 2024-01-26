from gi.repository import Adw, Gtk
import sys

import gi
from eeman.configuration import config, get_conf
from eeman.libs import setup as setup

from . import display
from . import preferences as prf

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

app_name = "Eeman"


class WelcomeWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_default_size(400, 600)
        self.set_title(f"As-salamu alaykum - {app_name}")

        self.box_main = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, valign=Gtk.Align.FILL, vexpand=True
        )
        self.set_child(self.box_main)

        # Carousel
        self.carousel = Adw.Carousel(
            hexpand=True, vexpand=True, allow_scroll_wheel=True, allow_long_swipes=False
        )
        self.box_main.append(self.carousel)

        # Indicator
        self.stk_indicator = Gtk.Stack(
            transition_type=Gtk.StackTransitionType.CROSSFADE
        )
        self.box_main.append(self.stk_indicator)
        self.carousel_dots = Adw.CarouselIndicatorDots(carousel=self.carousel)
        self.stk_indicator.add_titled(self.carousel_dots, "page0", "page0")
        # Page 1 - Welcome Page
        self.page1 = Adw.StatusPage(
            title="As-salamu alaykum !",
            description="we will run through the setup process now...",
            icon_name="sh.shuriken.Eeman",
            hexpand=True,
            vexpand=True,
        )
        self.carousel.append(self.page1)
        # Page 2 - Setup Page
        self.page2 = Gtk.Box(
            hexpand=True,
            vexpand=True,
            halign=Gtk.Align.CENTER,
            valign=Gtk.Align.CENTER,
        )
        self.prfbox = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            margin_start=10,
            margin_end=10,
        )
        self.carousel.append(self.page2)
        self.clamp = Adw.Clamp()
        self.page2.append(self.clamp)
        self.clamp.set_child(self.prfbox)
        self.prfbox.append(prf.PreferencesPage())

        # Page 3 - End Setup
        self.end_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, halign=Gtk.Align.CENTER, spacing=10
        )
        self.page3 = Adw.StatusPage(
            title="All set",
            description="Eeman app is now all setup, you can change settings later at any time.",
            icon_name="sh.shuriken.Eeman",
            hexpand=True,
            vexpand=True,
        )
        self.done_button = Gtk.Button(label="Next")
        self.done_button.get_style_context().add_class("suggested-action")
        self.go_back_button = Gtk.Button(label="Go back")
        self.page3.set_child(self.end_box)
        self.end_box.append(self.done_button)
        self.end_box.append(self.go_back_button)
        self.carousel.append(self.page3)
        self.go_back_button.connect("clicked", self.go_back)
        self.done_button.connect("clicked", self.show_display)

    def show_display(self, done_button):
        setup.set_config("App", "first_run", "No")
        display_window = display.DisplayWindow(application=app)
        display_window.present()
        self.close()

    def go_back(self, done_button):
        self.carousel.scroll_to(self.page2, True)


class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect("activate", self.on_activate)

    def on_activate(self, app):
        get_conf()
        sm = Adw.StyleManager().get_default()
        if config["Appearance"]["theme"] == "Dark":
            sm.set_color_scheme(Adw.ColorScheme.FORCE_DARK)
        elif config["Appearance"]["theme"] == "Light":
            sm.set_color_scheme(Adw.ColorScheme.FORCE_LIGHT)

        if config["App"]["first_run"] == "Yes":
            self.win = WelcomeWindow(application=app)
            self.win.present()
        elif config["App"]["first_run"] == "No":
            display_window = display.DisplayWindow(application=app)
            display_window.present()


app = MyApp(application_id="sh.shuriken.Eeman")


def run():
    app.run(sys.argv)
