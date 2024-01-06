import gi
import gui.welcome as welcome
import libs.setup as setup
import gui.preferences as pref

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, Gio  # noqa E:402


class DisplayWindow(Adw.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_name(welcome.app_name)
        self.set_default_size(400, 600)

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
        self.stack.get_page(self.page1).set_icon_name("emoji-recent-symbolic")
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
        self.timezone_label = Gtk.Label(label=setup.timezone)
        self.box_wrapper.append(self.date_label)
        self.box_wrapper.append(self.timezone_label)

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
                hexpand=True,
            )
            self.prayer_box.append(self.prayer_label)
            self.prayer_box.append(self.prayer_time_label)

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
        self.about_window.set_developer_name("shuriken.sh")
        self.about_window.set_version("1.0.0-alpha")
        self.about_window.set_website("https://shuriken.sh")
        self.about_window.set_license_type(Gtk.License.GPL_3_0)
        self.about_window.set_comments(
            "Eeman is an app to track prayer times, read the quran etc. "
            "Its open source and written in Python and Gtk 4. "
            "50 % of all donations go straight to recognized charities and are posted on the site."
        )

    def show_donate(self, action, params):
        print("open donate")
