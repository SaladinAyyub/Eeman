import sys
import gi
import setup

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
        self.prfbox = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            margin_start=20,
            margin_end=20,
        )
        self.carousel.append(self.page2)
        self.clamp = Adw.Clamp()
        self.page2.append(self.clamp)
        self.listbox1 = Gtk.ListBox(selection_mode=Gtk.SelectionMode.NONE)
        self.listbox1.get_style_context().add_class("boxed-list")
        self.listbox2 = Gtk.ListBox(selection_mode=Gtk.SelectionMode.NONE)
        self.listbox2.get_style_context().add_class("boxed-list")
        self.prfgr_setup = Adw.PreferencesGroup(title="Setup")
        self.prfgr_appearance = Adw.PreferencesGroup(title="Appearance")
        self.prfgr_appearance.add(self.listbox2)
        self.prfgr_setup.add(self.listbox1)
        self.clamp.set_child(self.prfbox)
        self.prfbox.append(self.prfgr_setup)
        self.prfbox.append(self.prfgr_appearance)
        self.prfgr_appearance.set_margin_top(10)

        self.location_setting = Adw.ComboRow(title="Location Mode")
        self.location_mode = Gtk.StringList()
        self.location_mode.append("Automatic using IP")
        self.location_mode.append("Manual (City, Country)")
        self.location_setting.set_model(self.location_mode)
        self.location_setting.connect(
            "notify::selected-item", self.on_location_mode_set
        )
        self.listbox1.append(self.location_setting)

        self.method_setting = Adw.ComboRow(title="Calculation Method")
        self.method_mode = Gtk.StringList()
        self.method_mode.append("Automatic (Nearest)")
        self.method_mode.append("Manual (Choose Method)")
        self.method_setting.set_model(self.method_mode)
        self.listbox1.append(self.method_setting)
        self.manual_location_country = Adw.EntryRow(title="Country")
        self.manual_location_city = Adw.EntryRow(title="City")
        self.manual_location_country.set_sensitive(False)
        self.manual_location_city.set_sensitive(False)
        self.manual_method_setting = Adw.ComboRow(title="Calculation Method")
        self.manual_method_mode = Gtk.StringList()
        self.manual_method_mode.append("University of Islamic Sciences, Karachi")
        self.manual_method_mode.append("Islamic Society of North America")
        self.manual_method_mode.append("Muslim World League")
        self.manual_method_mode.append("Umm Al-Qura University, Makkah")
        self.manual_method_mode.append("Egyptian General Authority of Survey")
        self.manual_method_mode.append("Institute of Geophysics, University of Tehran")
        self.manual_method_mode.append("Gulf Region")
        self.manual_method_mode.append("Kuwait")
        self.manual_method_mode.append("Qatar")
        self.manual_method_mode.append("Majlis Ugama Islam Singapura, Singapore")
        self.manual_method_mode.append("Union Organization islamic de France")
        self.manual_method_mode.append("Diyanet İşleri Başkanlığı, Turkey")
        self.manual_method_mode.append("Spiritual Administration of Muslims of Russia")
        self.manual_method_mode.append("Moonsighting Committee Worldwide")
        self.manual_method_mode.append("Dubai (unofficial)")
        self.method_setting.connect("notify::selected-item", self.on_method_mode_set)
        self.manual_method_setting.set_model(self.manual_method_mode)
        self.manual_method_setting.connect(
            "notify::selected-item", self.on_manual_method_set
        )
        self.manual_location_country.set_show_apply_button(True)
        self.manual_location_city.set_show_apply_button(True)
        self.manual_location_country.connect("apply", self.on_manual_location_country)
        self.manual_location_city.connect("apply", self.on_manual_location_city)

        self.listbox1.append(self.manual_location_country)
        self.listbox1.append(self.manual_location_city)
        self.listbox1.append(self.manual_method_setting)
        self.manual_method_setting.set_sensitive(False)

        self.dark_theme_setting = Adw.ActionRow(title="Dark theme")
        self.dark_theme_switch = Gtk.Switch(valign=Gtk.Align.CENTER)
        self.dark_theme_setting.add_suffix(self.dark_theme_switch)
        self.dark_theme_switch.connect("state-set", self.set_theme)
        self.listbox2.append(self.dark_theme_setting)

    def on_location_mode_set(self, location_setting, event):
        if "Automatic" in self.location_setting.get_selected_item().get_string():
            setup.get_location_auto()
            self.manual_location_country.set_sensitive(False)
            self.manual_location_city.set_sensitive(False)
        if "Manual" in self.location_setting.get_selected_item().get_string():
            self.manual_location_country.set_sensitive(True)
            self.manual_location_city.set_sensitive(True)

    def on_method_mode_set(self, method_setting, event):
        if "Automatic" in self.method_setting.get_selected_item().get_string():
            self.manual_method_setting.set_sensitive(False)
            setup.method = None
        if "Manual" in self.method_setting.get_selected_item().get_string():
            self.manual_method_setting.set_sensitive(True)
            self.set_manual_method()

    def on_manual_method_set(self, manual_method, event):
        self.set_manual_method()

    def set_manual_method(self):
        method_string = self.manual_method_setting.get_selected_item().get_string()
        if "Karachi" in method_string:
            setup.method = 1
        if "North America" in method_string:
            setup.method = 2
        if "World League" in method_string:
            setup.method = 3
        if "Makkah" in method_string:
            setup.method = 4
        if "Egyptian" in method_string:
            setup.method = 5
        if "Tehran" in method_string:
            setup.method = 7
        if "Gulf" in method_string:
            setup.method = 8
        if "Kuwait" in method_string:
            setup.method = 9
        if "Qatar" in method_string:
            setup.method = 10
        if "Singapore" in method_string:
            setup.method = 11
        if "France" in method_string:
            setup.method = 12
        if "Turkey" in method_string:
            setup.method = 13
        if "Russia" in method_string:
            setup.method = 14
        if "Moonsighting" in method_string:
            setup.method = 15
        if "Dubai" in method_string:
            setup.method = 16

    def on_manual_location_country(self, manual_location_country):
        setup.country = self.manual_location_country.get_text()

    def on_manual_location_city(self, manual_location_city):
        setup.city = self.manual_location_city.get_text()

    def set_theme(self, dark_theme_switch, state):
        app = self.get_application()
        sm = app.get_style_manager()
        if state:
            sm.set_color_scheme(Adw.ColorScheme.PREFER_DARK)
        else:
            sm.set_color_scheme(Adw.ColorScheme.PREFER_LIGHT)


class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect("activate", self.on_activate)

    def on_activate(self, app):
        self.win = WelcomeWindow(application=app)
        self.win.present()
        setup.get_location_auto()


app = MyApp(application_id="sh.shuriken.Eeman")
app.run(sys.argv)
