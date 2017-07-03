import sys
import rumps
import halfcaff.app

if len(sys.argv) == 2 and sys.argv[1] == '-d':
    rumps.debug_mode(True)

app = halfcaff.app.HalfCaff()
app.run()