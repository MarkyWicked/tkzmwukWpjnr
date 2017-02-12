#!/usr/bin/python

import ConfigManager, functions

class shell(object):
    config = ConfigManager.ConfigManager()
    host = config.IpAddress
    port = config.Port
    notConnected = True
    exiting = False

    functions = functions.functions(host, port)

    while(notConnected and not exiting):
        try:
            notConnected = False
            exiting = functions.start()
            notConnected = True
        except:
            notConnected = True









