from urllib2 import urlopen
import CryptoLib

class Updater(object):
    version = "1.0"
    crypto = CryptoLib.CryptoLib([2, 6, 4, 8, 5])
    def update(self):
        _version = urlopen("http://85.255.5.44/vxsrfp/xkv{nqt.html").read()
        _version = _version[:-1]
        if self.version == self.crypto.Decrypt(_version):
            pass
        else:
            pass #TODO: do update proccedure
