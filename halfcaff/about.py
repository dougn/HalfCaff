import os
import sys
from Foundation import NSMakeRect
from AppKit import NSTextView
import rumps
import rumps.compat
try:
    from py2app import __version__ as py2app_version
except:
    py2app_version = "0.14" # FML
import jsontree
import halfcaff.util
import halfcaff.version

_message = """\
Prevent OSX from Sleeping when Cisco VPN is connected.

%(copyright)s
""" % dict(
    copyright=halfcaff.version.copyright)

_text = """\
Built with Python %(sys_version)s

Python Packages:
  rumps %(rumps_version)s %(rumps_url)s
  py2app %(py2app_version)s %(py2app_url)s
  jsontree %(jsontree_version)s %(jsontree_url)s

Additional code from:
  https://github.com/pudquick/pyLoginItems
  http://benden.us/journal/2014/OS-X-Power-Management-No-Sleep-Howto/
""" % dict(
    sys_version = sys.version,
    rumps_version = rumps.__version__,
    rumps_url = 'https://rumps.readthedocs.io/',
    py2app_version = py2app_version,
    py2app_url = 'https://py2app.readthedocs.io/',
    jsontree_version = jsontree.__version_string__,
    jsontree_url = 'https://github.com/dougn/jsontree'
)

class AboutWindow(rumps.Window):
    def __init__(self):
        text = "Python " + sys.version + "\n\n" + sys.copyright
        title = "HalfCaff " + halfcaff.version.version
        if halfcaff.util.is_dev_mode():
            title += '-dev'
        super(AboutWindow, self).__init__(
            title=title, message=_message, default_text=_text)
        self.icon = halfcaff.util.icon('halfcaff.icns')
        #self._textfield.dealloc()
        self._textfield = NSTextView.alloc().initWithFrame_(NSMakeRect(0, 0, 320, 160))
        self._textfield.setSelectable_(True)
        #self._textfield.usesRuler_(True)
        self._alert.setAccessoryView_(self._textfield)
        self._textfield.setString_(rumps.compat.text_type(_text))

window = AboutWindow()

        