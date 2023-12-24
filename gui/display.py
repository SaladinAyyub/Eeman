import gi
import gui.welcome as welcome

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw  # noqa E:402


class DisplayWindow(Adw.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_name(welcome.app_name)
        self.set_default_size(400, 500)

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
        self.page1 = Gtk.Box(
            hexpand=True,
            vexpand=True,
            halign=Gtk.Align.CENTER,
            valign=Gtk.Align.CENTER,
        )
        self.stack.add_titled(self.page1, "page0", "Prayer")
        self.stack.get_page(self.page1).set_icon_name("emoji-recent-symbolic")

    def on_sq_get_visible_child(self, widget, event):
        if self.sq_viewswitcher.get_visible_child() == self.wintitle:
            self.viewswitcherbar.set_reveal(True)
        else:
            self.viewswitcherbar.set_reveal(False)
