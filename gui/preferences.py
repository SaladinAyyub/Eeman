import gi
import libs.setup as setup

from configparser import ConfigParser

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw  # noqa E:402


config = ConfigParser()
config.read("config.ini")


class PreferencesPage(Adw.PreferencesPage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prfgr_setup = Adw.PreferencesGroup(title="Setup")
        self.prfgr_appearance = Adw.PreferencesGroup(title="Appearance")
        self.add(self.prfgr_setup)
        self.add(self.prfgr_appearance)

        self.location_setting = Adw.ComboRow(title="Location Mode")
        self.location_mode = Gtk.StringList()
        self.location_mode.append("Automatic using IP")
        self.location_mode.append("Manual (City, Country)")
        self.location_setting.set_model(self.location_mode)
        if config["Prayer"]["location_mode"] == "Automatic":
            self.location_setting.set_selected(0)
            self.manual_location_country.set_sensitive(False)
            self.manual_location_city.set_sensitive(False)
        elif config["Prayer"]["location_mode"] == "Manual":
            self.location_setting.set_selected(1)
        self.location_setting.connect(
            "notify::selected-item", self.on_location_mode_set
        )
        self.prfgr_setup.add(self.location_setting)

        self.school_setting = Adw.ComboRow(title="School of thought")
        self.school_mode = Gtk.StringList()
        self.school_mode.append("Standard (Shafi'i, Maliki and Hanbali)")
        self.school_mode.append("Hanafi")
        self.school_setting.set_model(self.school_mode)
        self.prfgr_setup.add(self.school_setting)
        self.school_setting.set_selected(int(config["Prayer"]["hanafi_school"]))
        self.school_setting.connect("notify::selected-item", self.on_school_set)

        self.method_setting = Adw.ComboRow(title="Calculation Method")
        self.method_mode = Gtk.StringList()
        self.method_mode.append("Automatic (Nearest)")
        self.method_mode.append("Manual (Choose Method)")
        self.method_setting.set_model(self.method_mode)
        self.prfgr_setup.add(self.method_setting)
        self.manual_location_country = Adw.EntryRow(title="Country")
        self.manual_location_city = Adw.EntryRow(title="City")
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

        self.prfgr_setup.add(self.manual_location_country)
        self.prfgr_setup.add(self.manual_location_city)
        self.prfgr_setup.add(self.manual_method_setting)
        self.manual_method_setting.set_sensitive(False)

        self.dark_theme_setting = Adw.ActionRow(title="Dark theme")
        self.dark_theme_switch = Gtk.Switch(valign=Gtk.Align.CENTER)
        self.dark_theme_setting.add_suffix(self.dark_theme_switch)
        self.dark_theme_switch.connect("state-set", self.set_theme)
        self.prfgr_appearance.add(self.dark_theme_setting)

    def on_location_mode_set(self, location_setting, event):
        if "Automatic" in self.location_setting.get_selected_item().get_string():
            setup.get_location_auto()
            config.set("Prayer", "location_mode", "Automatic")
            self.manual_location_country.set_sensitive(False)
            self.manual_location_city.set_sensitive(False)
        if "Manual" in self.location_setting.get_selected_item().get_string():
            config.set("Prayer", "location_mode", "Manual")
            self.manual_location_country.set_sensitive(True)
            self.manual_location_city.set_sensitive(True)
        self.update_config()

    def on_school_set(self, school_setting, event):
        if "Standard" in self.school_setting.get_selected_item().get_string():
            config.set("Prayer", "hanafi_school", "0")
        if "Hanafi" in self.school_setting.get_selected_item().get_string():
            config.set("Prayer", "hanafi_school", "1")
        self.update_config()

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
        config.set("Prayer", "country", self.manual_location_country.get_text())
        self.update_config()

    def on_manual_location_city(self, manual_location_city):
        config.set("Prayer", "city", self.manual_location_city.get_text())
        self.update_config()

    def update_config(self):
        with open("config.ini", "w") as file:
            config.write(file)

    def set_theme(self, dark_theme_switch, state):
        sm = Adw.StyleManager()
        if state:
            sm.set_color_scheme(Adw.ColorScheme.FORCE_DARK)
        else:
            sm.set_color_scheme(Adw.ColorScheme.FORCE_LIGHT)
