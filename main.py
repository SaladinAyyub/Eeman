import sys
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw  # noqa E:402

app_name = "Eeman"


class WelcomeWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_default_size(300, 400)
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
        # Page 1
        self.page1 = Adw.StatusPage(
            title="As-salamu alaykum !",
            description="we will run through the setup process now...",
            icon_name="preferences-desktop-screensaver-symbolic",
            hexpand=True,
            vexpand=True,
        )
        self.carousel.append(self.page1)
        # Page 2
        self.page2 = Gtk.Box(
            hexpand=True,
            vexpand=True,
            halign=Gtk.Align.CENTER,
            valign=Gtk.Align.CENTER,
        )
        self.carousel.append(self.page2)
        self.clamp = Adw.Clamp()
        self.page2.append(self.clamp)


class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect("activate", self.on_activate)

    def on_activate(self, app):
        self.win = WelcomeWindow(application=app)
        self.win.present()


app = MyApp(application_id="sh.shuriken.Eeman")
app.run(sys.argv)
