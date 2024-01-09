import gi

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
        self.manual_method_dict = {
            "1": 0,
            "2": 1,
            "3": 2,
            "4": 3,
            "5": 4,
            "7": 5,
            "8": 6,
            "9": 7,
            "10": 8,
            "11": 9,
            "12": 10,
            "13": 11,
            "14": 12,
            "15": 13,
            "16": 14,
        }
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

        self.dark_theme_setting = Adw.ActionRow(title="Dark theme")
        self.dark_theme_switch = Gtk.Switch(valign=Gtk.Align.CENTER)
        self.dark_theme_setting.add_suffix(self.dark_theme_switch)
        self.dark_theme_switch.connect("state-set", self.set_theme)
        self.prfgr_appearance.add(self.dark_theme_setting)
        self.set_initial_values()

    def set_initial_values(self):
        if config["Prayer"]["location_mode"] == "Automatic":
            self.location_setting.set_selected(0)
            self.manual_location_country.set_sensitive(False)
            self.manual_location_city.set_sensitive(False)
        elif config["Prayer"]["location_mode"] == "Manual":
            self.location_setting.set_selected(1)
        if config["Prayer"]["method_mode"] == "Automatic":
            self.method_setting.set_selected(0)
            self.manual_method_setting.set_sensitive(False)
        elif config["Prayer"]["method_mode"] == "Manual":
            self.method_setting.set_selected(1)
        self.school_setting.set_selected(int(config["Prayer"]["hanafi_school"]))
        self.manual_method_setting.set_selected(
            self.manual_method_dict[config["Prayer"]["method"]]
        )

    def on_location_mode_set(self, location_setting, event):
        if "Automatic" in self.location_setting.get_selected_item().get_string():
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
            config.set("Prayer", "method_mode", "Automatic")
        if "Manual" in self.method_setting.get_selected_item().get_string():
            self.manual_method_setting.set_sensitive(True)
            config.set("Prayer", "method_mode", "Manual")
        self.update_config()

    def on_manual_method_set(self, manual_method, event):
        config.set(
            "Prayer",
            "method",
            list(self.manual_method_dict.keys())[
                list(self.manual_method_dict.values()).index(
                    self.manual_method_setting.get_selected()
                )
            ],
        )
        self.update_config()

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
