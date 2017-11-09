from .__import import *

def config_dict(filename):
    config = ConfigParser()
    rc = config.read(filename)
    if rc != [filename]:
        error("ConfigParser: config read failed")
    debug(config.sections())
    ret = OrderedDict((section, dict(config[section])) for section in config.sections())
    debug(ret)
    debug("")
    debug("Config")
    for section in ret:
        debug("\t%r" % section)
        for item in ret[section]:
            debug("\t\t%r: %r" % (item, ret[section][item]))

    return ret


