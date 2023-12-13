import sys
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw  # noqa E:402

app_name = "Eeman"


class WelcomeWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_default_size(400, 500)
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
            icon_name="preferences-desktop-screensaver-symbolic",
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
        self.page2.set_margin_start(20)
        self.page2.set_margin_end(20)
        self.carousel.append(self.page2)
        self.clamp = Adw.Clamp()
        self.page2.append(self.clamp)
        self.listbox = Gtk.ListBox(selection_mode=Gtk.SelectionMode.NONE)
        self.listbox.get_style_context().add_class("boxed-list")
        self.prfgr_setup = Adw.PreferencesGroup(title="Setup")
        self.prfgr_setup.add(self.listbox)
        self.clamp.set_child(self.prfgr_setup)

        self.location_setting = Adw.ComboRow(title="Location Mode")
        self.location_mode = Gtk.StringList()
        self.location_mode.append("Automatic using IP")
        self.location_mode.append("Manual (City, Country)")
        self.location_setting.set_model(self.location_mode)
        self.listbox.append(self.location_setting)

        self.method_setting = Adw.ComboRow(title="Calculation Method")
        self.method_mode = Gtk.StringList()
        self.method_mode.append("Automatic (Nearest)")
        self.method_mode.append("Manual (Choose Method)")
        self.method_setting.set_model(self.method_mode)
        self.listbox.append(self.method_setting)


class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect("activate", self.on_activate)

    def on_activate(self, app):
        self.win = WelcomeWindow(application=app)
        self.win.present()


app = MyApp(application_id="sh.shuriken.Eeman")
app.run(sys.argv)
