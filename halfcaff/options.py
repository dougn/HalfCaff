import os
import sys
import jsontree
import halfcaff.util

DEFAULTS = jsontree.jsontree(
    vpncli = '/opt/cisco/anyconnect/bin/vpn',
    monitor_interval = int(60*2.5), # 2.5min
    monitor_timemachine = True,
    monitor_vpn = True,
    auto_caffeinate_vpn = False,
    auto_caffeinate_timemachine = False
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
    if 'auto_caffeinate' in options:
        # old version
        options['auto_caffeinate_vpn'] = options['auto_caffeinate']
        options['auto_caffeinate_timemachine'] = options['auto_caffeinate']
        del options['auto_caffeinate']
        save_options(app)
    return options

def save_options(app):
    try:
        with app.open('options.json', 'wb') as optfile:
            jsontree.dump(app.options, optfile)
    except:
        #print sys.exc_info()
        pass
    return app.options
    