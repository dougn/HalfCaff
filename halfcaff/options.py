import os
import sys
import jsontree
import halfcaff.util

DEFAULTS = jsontree.jsontree(
    vpncli = '/opt/cisco/anyconnect/bin/vpn',
    monitor_interval = int(60*2.5), # 2.5min
    auto_caffeinate = False
)

def load_options(app):
    options = jsontree.clone(DEFAULTS)
    try:
        with app.open('options.json') as optfile:
            options.update(jsontree.load(optfile))
    except:
        #print sys.exc_info()
        app.options = options
        save_options(app)
    if options.monitor_interval != DEFAULTS.monitor_interval:
        timer = halfcaff.util.get_timer(app.monitor)
        if timer:
            timer.interval = options.monitor_interval
    app.options = options
    return options

def save_options(app):
    try:
        with app.open('options.json', 'wb') as optfile:
            jsontree.dump(app.options, optfile)
    except:
        #print sys.exc_info()
        pass
    return app.options
    