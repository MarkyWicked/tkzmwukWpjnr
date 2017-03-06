#!/usr/bin/python

import ConfigManager, functions

class shell(object):
    config = ConfigManager.ConfigManager()
    host = config.IpAddress
    port = config.Port
    notConnected = True
    exiting = False

    functions = functions.functions(host, port)
    def main(self):
        while (self.notConnected and not self.exiting):
            try:
                self.notConnected = False
                self.exiting = self.functions.start()
                self.notConnected = True
            except:
                self.notConnected = True

if __name__ == '__main__':
    shell().main()










