import gi
from datetime import datetime
from eeman.libs import setup
from eeman.configuration import config

from . import preferences as pref
from . import welcome

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
gi.require_version("Notify", "0.7")
from gi.repository import Adw, Gio, Gtk, Notify, GLib  # noqa E:402

Notify.init("Eeman")


class DisplayWindow(Adw.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_name(welcome.app_name)
        self.set_default_size(500, 600)
        self.set_hide_on_close(True)

        self.box_main = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            halign=Gtk.Align.FILL,
            valign=Gtk.Align.FILL,
            hexpand=True,
            vexpand=True,
        )
        self.set_content(self.box_main)

        self.hb = Adw.HeaderBar(centering_policy=Adw.CenteringPolicy.STRICT)
        self.box_main.append(self.hb)

        # Create a menu
        preferences_action = Gio.SimpleAction.new("pref", None)
        about_action = Gio.SimpleAction.new("about", None)
        donate_action = Gio.SimpleAction.new("donate", None)
        preferences_action.connect("activate", self.show_preferences)
        about_action.connect("activate", self.show_about)
        donate_action.connect("activate", self.show_donate)
        self.add_action(preferences_action)
        self.add_action(about_action)
        self.add_action(donate_action)
        menu = Gio.Menu.new()
        menu.append("Preferences", "win.pref")
        menu.append("About", "win.about")
        menu.append("Donate", "win.donate")
        self.popover = Gtk.PopoverMenu()
        self.popover.set_menu_model(menu)
        self.hamburger = Gtk.MenuButton()
        self.hamburger.set_popover(self.popover)
        self.hamburger.set_icon_name("open-menu-symbolic")  # Give it a nice icon

        # Add menu button to the header bar
        self.hb.pack_end(self.hamburger)
        self.stack = Adw.ViewStack()
        self.box_main.append(self.stack)

        # Squeezer
        self.sq_viewswitcher = Adw.Squeezer(
            halign=Gtk.Align.FILL,
        )
        self.sq_viewswitcher.set_switch_threshold_policy(
            Adw.FoldThresholdPolicy.NATURAL
        )
        self.sq_viewswitcher.set_transition_type(Adw.SqueezerTransitionType.CROSSFADE)
        self.sq_viewswitcher.set_xalign(1)
        self.sq_viewswitcher.set_homogeneous(True)
        self.hb.set_title_widget(self.sq_viewswitcher)

        # ViewSwitcher (wide)
        self.viewswitcher_wide = Adw.ViewSwitcher(
            halign=Gtk.Align.CENTER, margin_start=50, margin_end=50
        )
        self.viewswitcher_wide.set_policy(Adw.ViewSwitcherPolicy.WIDE)
        self.viewswitcher_wide.set_stack(self.stack)
        self.sq_viewswitcher.add(self.viewswitcher_wide)

        # ViewSwitcher (narrow)
        self.viewswitcher_narrow = Adw.ViewSwitcher(
            halign=Gtk.Align.CENTER,
        )
        self.viewswitcher_narrow.set_policy(Adw.ViewSwitcherPolicy.NARROW)
        self.viewswitcher_narrow.set_stack(self.stack)
        self.sq_viewswitcher.add(self.viewswitcher_narrow)

        # ViewSwitcherBar (bottom viewswitcher)
        self.viewswitcherbar = Adw.ViewSwitcherBar(vexpand=True, valign=Gtk.Align.END)
        self.viewswitcherbar.set_stack(self.stack)
        self.viewswitcherbar.set_reveal(False)
        self.box_main.append(self.viewswitcherbar)

        # Window Title
        self.wintitle = Adw.WindowTitle(title=welcome.app_name)
        self.sq_viewswitcher.add(self.wintitle)

        # Connect signals
        self.sq_viewswitcher.connect(
            "notify::visible-child", self.on_sq_get_visible_child
        )

        # Page 1
        self.page1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.stack.add_titled(self.page1, "page0", "Prayer")
        self.stack.get_page(self.page1).set_icon_name("alarm-symbolic")
        setup.get_response()
        self.clamp = Adw.Clamp()
        self.page1.append(self.clamp)
        # Wrapper inside Adw.Clamp
        self.box_wrapper = Gtk.Box(
            spacing=10,
            margin_start=20,
            margin_end=20,
            margin_top=20,
            margin_bottom=20,
            orientation=Gtk.Orientation.VERTICAL,
        )
        self.clamp.set_child(self.box_wrapper)
        self.date_label = Gtk.Label(label=setup.date)
        self.timezone_label = Gtk.Label(label=setup.timezone, margin_top=50)
        self.hijri_date_label = Gtk.Label(label=setup.hijri_date, margin_bottom=50)
        self.box_wrapper.append(self.date_label)
        self.box_wrapper.append(self.hijri_date_label)

        self.prayers = ["Fajr", "Sunrise", "Dhuhr", "Asr", "Maghrib", "Isha"]
        for self.prayer in self.prayers:
            self.prayer_box = Gtk.Box()
            self.prayer_box.get_style_context().add_class("card")
            self.box_wrapper.append(self.prayer_box)
            self.prayer_label = Gtk.Label(
                label=self.prayer,
                margin_start=10,
                margin_end=10,
                margin_top=10,
                margin_bottom=10,
            )
            self.prayer_time_label = Gtk.Label(
                label=setup.prayer[self.prayer],
                margin_start=10,
                margin_end=10,
                margin_top=10,
                margin_bottom=10,
                halign=Gtk.Align.END,
            )
            self.prayer_notify_button = Gtk.Button(
                halign=Gtk.Align.END,
                hexpand=True,
                has_frame=False,
            )
            if config["Prayer"]["%s_notify" % (self.prayer)] == "Yes":
                self.prayer_notify_button.set_icon_name("bell-outline-symbolic")
            else:
                self.prayer_notify_button.set_icon_name("bell-outline-none-symbolic")
            self.prayer_box.append(self.prayer_label)
            self.prayer_box.append(self.prayer_notify_button)
            self.prayer_box.append(self.prayer_time_label)
            self.prayer_notify_button.connect("clicked", self.set_notify, self.prayer)
            GLib.timeout_add_seconds(
                1,
                self.check_time,
                self.prayer,
                self.prayer_time_label.get_label(),
                self.prayer_notify_button,
            )
        self.box_wrapper.append(self.timezone_label)

        self.tb = Adw.ToolbarView()
        self.actionbar = Gtk.ActionBar()
        self.tb.add_top_bar(self.actionbar)
        self.stack.add_titled(self.tb, "page1", "Quran")
        self.stack.get_page(self.tb).set_icon_name("open-book-symbolic")
        self.select_surah = Gtk.DropDown()
        self.actionbar.pack_start(self.select_surah)
        self.surah_list = Gtk.StringList()
        self.surah_data = setup.get_response_quran_surah_data()
        for surah in range(1, 115):
            self.surah_list.append(
                "%s. %s"
                % (surah, setup.get_quran_surah_name_english(surah, self.surah_data))
            )
        self.select_surah.set_model(self.surah_list)
        self.quran_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=20,
            vexpand=True,
            margin_start=10,
            margin_end=10,
            margin_top=10,
            margin_bottom=10,
        )
        self.clamp2 = Adw.Clamp()
        self.scrolled_window = Gtk.ScrolledWindow()
        self.scrolled_window.set_child(self.clamp2)
        self.clamp2.set_child(self.quran_box)
        self.tb.set_content(self.scrolled_window)
        self.surah_heading_arabic = Gtk.Label()
        self.surah_heading_english = Gtk.Label()
        self.surah_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.surah_box.append(self.surah_heading_arabic)
        self.surah_box.append(self.surah_heading_english)
        self.ayah_parent_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.quran_box.append(self.surah_box)
        self.quran_box.append(self.ayah_parent_box)
        self.on_surah_select(self.select_surah, self.select_surah.activate)
        self.select_surah.connect("notify::selected-item", self.on_surah_select)

    def check_time(self, prayer, prayer_time, notify_btn):
        current_time = datetime.now().strftime("%H:%M")
        if (
            current_time == prayer_time
            and notify_btn.get_icon_name() == "bell-outline-symbolic"
        ):
            Notify.Notification.new("Its time for %s!" % (prayer)).show()
            GLib.timeout_add_seconds(
                60, self.check_time, prayer, prayer_time, notify_btn
            )
        else:
            GLib.timeout_add_seconds(
                1, self.check_time, prayer, prayer_time, notify_btn
            )

    def set_notify(self, notify_btn, prayer):
        if notify_btn.get_icon_name() == "bell-outline-symbolic":
            notify_btn.set_icon_name("bell-outline-none-symbolic")
            config["Prayer"]["%s_notify" % (prayer)] == "No"
        elif notify_btn.get_icon_name() == "bell-outline-none-symbolic":
            notify_btn.set_icon_name("bell-outline-symbolic")
            config["Prayer"]["%s_notify" % (prayer)] == "Yes"

    def on_surah_select(self, select_surah, event):
        self.quran_box.remove(self.ayah_parent_box)
        self.ayah_parent_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.quran_box.append(self.ayah_parent_box)
        self.surah_heading_arabic.set_label(
            setup.get_quran_surah_name_arabic(
                self.select_surah.get_selected() + 1, self.surah_data
            )
        )
        self.surah_heading_english.set_label(
            setup.get_quran_surah_name_english(
                self.select_surah.get_selected() + 1, self.surah_data
            )
        )
        total_ayah = setup.get_number_of_ayahs(
            self.select_surah.get_selected() + 1, self.surah_data
        )
        ayah_data_english = setup.get_response_quran_ayah_data_english(
            self.select_surah.get_selected() + 1
        )
        ayah_data_arabic = setup.get_response_quran_ayah_data_arabic(
            self.select_surah.get_selected() + 1
        )
        for ayah in range(1, total_ayah + 1):
            ayah_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
            ayah_box.get_style_context().add_class("card")
            ayah_text_english = setup.get_quran_ayah_text(ayah_data_english, ayah)
            ayah_text_arabic = setup.get_quran_ayah_text(ayah_data_arabic, ayah)
            ayah_english_label = Gtk.Label(
                label="%s. %s" % (ayah, ayah_text_english),
                wrap=True,
                margin_start=10,
                margin_end=10,
                margin_top=10,
                margin_bottom=10,
            )
            ayah_arabic_label = Gtk.Label(
                label=ayah_text_arabic,
                wrap=True,
                hexpand=True,
                margin_start=10,
                margin_end=10,
                margin_top=10,
                margin_bottom=10,
            )
            ayah_box.append(ayah_english_label)
            ayah_box.append(ayah_arabic_label)
            self.ayah_parent_box.append(ayah_box)

    def on_sq_get_visible_child(self, widget, event):
        if self.sq_viewswitcher.get_visible_child() == self.wintitle:
            self.viewswitcherbar.set_reveal(True)
        else:
            self.viewswitcherbar.set_reveal(False)

    def show_preferences(self, action, params):
        self.pref_window = Adw.PreferencesWindow()
        self.pref_window.add(pref.PreferencesPage())
        self.pref_window.present()

    def show_about(self, action, params):
        self.about_window = Adw.AboutWindow()
        self.about_window.present()
        self.about_window.set_application_name("Eeman")
        self.about_window.set_application_icon("sh.shuriken.Eeman")
        self.about_window.set_developer_name("shuriken")
        self.about_window.set_version("0.1.1")
        self.about_window.set_website("https://codeberg.org/SHuRiKeN/Eeman")
        self.about_window.set_license_type(Gtk.License.GPL_3_0)
        self.about_window.set_comments(
            "Eeman is an app to track prayer times, read the quran etc. "
            "Its open source and written in Python and Gtk 4. "
        )

    def show_donate(self, action, params):
        self.donate_launcher = Gtk.UriLauncher()
        self.donate_launcher.set_uri("https://ko-fi.com/shuriken1812")
        self.donate_launcher.launch()
