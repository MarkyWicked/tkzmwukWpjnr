import os
import socket

class ConfigManager:
    IpAddress = ""
    Port = 0
    Localization = ""
    DnsString = ""
    Dns = False

    def __init__(self):
        self.testDirs()
        self.LoadConfiguration()

    def testDirs(self):
        if not os.path.isdir(os.path.join(os.getcwd(),"Data")):
            os.makedirs(os.path.join(os.getcwd(),"Data"))

    def LoadConfiguration(self):
        path = os.path.join(os.getcwd(),"Data")
        path = os.path.join(path, "config.cfg")

        if not os.path.exists(path):
            configFile = open(path,"w+")
            configFile.write("dns=0\n")
            configFile.write("ip=127.0.0.1\n")
            configFile.write("hostname=localhost\n")
            configFile.write("port=6666\n")
            configFile.write("localization=en-US\n")
            configFile.close()

        with open(path, "r") as configFile:
            config = configFile.readlines()
            config = [x.strip() for x in config]

        words = []
        for c in config:
            words+=c.split("=")

        if words[1] == "0":
            self.Dns = False
        elif words[1] == "1":
            self.Dns = True
        else:
            self.Dns = False

        self.IpAddress = words[3]
        self.DnsString = words[5]
        self.Port = int(words[7])
        self.Localization = words[9]

        if self.Dns:
            self.IpAddress = socket.gethostbyname(self.DnsString)