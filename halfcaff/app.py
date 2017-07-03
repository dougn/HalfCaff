import sys
import os
import rumps
import jsontree
import halfcaff.monitor
import halfcaff.about
import halfcaff.util
import halfcaff.login
import halfcaff.options
import halfcaff.power

### States:
###   VPN  Caff  Status           Button              Icon     Icon Desc
###    0    0    Not Connected    NoVPN (greyed out)  Disabled Cup no steam
###    0    1    ILLEGAL          --                  Error    Upside down cup?
###    1    0    Not Caffeinated  On                  Off      Cup no steam
###    1    1    Caffeinated      Off                 On       Cup steam


_MENU_TITLES = jsontree.jsontree(
    Control = ["Caffeinate", "Decaffeinate", "No VPN Connection (disabled)"],
    Options = jsontree.jsontree(
        Auto  = "Auto Caffeinate on VPN Connection",
        Login = "Run at Startup"
    ),
    About = "About",
    Quit =  "Quit"
)

def _initialize_jtmenu(menu, tree):
    menutree = jsontree.jsontree()
    for name, title in tree.iteritems():
        menuitem = menu[name]
        if isinstance(title, jsontree.jsontree):
            subtree = _initialize_jtmenu(menuitem, title)
            menutree[name] = subtree
        else:
            if isinstance(title, list):
                menuitem.state_titles = title
            else:
                menuitem.title = title
            menutree[name] = menuitem
    return menutree

class HalfCaff(rumps.App):
    def __init__(self):
        self.state_icons = [
            halfcaff.util.icon('halfcaff_off.icns'),
            halfcaff.util.icon('halfcaff_on.icns'),
            halfcaff.util.icon('halfcaff_disabled.icns')]
        super(HalfCaff, self).__init__("HalfCaff", icon=self.state_icons[-1])
        self.menu = [
            "Control",
            rumps.separator,
            "Options",
            rumps.separator,
            "About"]
        
        self.initialized = False
        self.caffeinated = False
        self.enabled = False
        self.options = halfcaff.options.load_options(self)
        self.power = halfcaff.power.Control()
    
    @rumps.clicked("About")
    def about(self, sender):
        halfcaff.about.window.run()
    
    @rumps.clicked("Options", "Auto")
    def option_auto(self, sender):
        self.options.auto_caffeinate = not self.options.auto_caffeinate
        sender.state = int(self.options.auto_caffeinate)
        halfcaff.options.save_options(self)
        
    @rumps.clicked("Options", "Login")
    def option_login(self, sender):
        oldstate = sender.state
        self.update_run_at_login()
        if sender.state == -1:
            return
        if oldstate != sender.state:
            return
        sender.state = int(not sender.state)
        if sender.state:
            halfcaff.login.enable_startup_at_login()
        else:
            halfcaff.login.disable_startup_at_login()
    
    def update_run_at_login(self):
        runatlogin = self.jtmenu.Options.Login
        if runatlogin.state == -1:
            return
        runatlogin.state = -1 if halfcaff.util.is_dev_mode() else int(halfcaff.login.is_login_enabled())
        if runatlogin.state == -1:
            runatlogin.set_callback(None)
            
    def initialize(self):
        if self.initialized:
            return
        self.jtmenu = _initialize_jtmenu(self.menu, _MENU_TITLES)
        self.jtmenu.Options.Auto.state=int(self.options.auto_caffeinate)
        self.quit_button.set_callback(self.finalize)
        self.update_control_state(-1)
        self.initialized = True
    
    def finalize(self, sender):
        if self.initialized:
            self.update_control_state(-1)
            self.initialized = False
        rumps.quit_application(sender)
    
    def update_control_state(self, state=None):
        control = self.jtmenu.Control
        if state in (0, 1, -1, False, True):
            control.state_hidden = int(state)
        control.title = control.state_titles[control.state_hidden]
        self.icon = self.state_icons[control.state_hidden]
        if control.state_hidden == -1:
            self.caffeinated = False
            self.enabled = False
            control.set_callback(None)
            self.power.decaffeinate()
            ## deactivate caffeinate
        else:
            self.caffeinated = bool(control.state_hidden)
            self.enabled = True
            control.set_callback(self.control)
            if self.caffeinated:
                ## activate caffeinate
                self.power.caffeinate()
            else:
                ## deactivate caffeinate
                self.power.decaffeinate()

    @rumps.clicked("Control")
    def control(self, sender):
        self.update_control_state(not sender.state_hidden)
        
    @rumps.timer(halfcaff.options.DEFAULTS.monitor_interval)
    def monitor(self, timer):
        try:
            if not self.initialized:
                self.initialize()
            self.update_run_at_login()
            connected = halfcaff.monitor.connected(self.options.vpncli)
            if not connected and self.enabled:
                self.update_control_state(-1)
            elif not self.enabled and connected:
                self.update_control_state(self.options.auto_caffeinate)
        except:
            pass
            print sys.exc_info()


    

    
