class CryptoLib:
    arr = None

    def __init__(self,arr):
        self.arr = arr

    def Encrypt(self,text):
        j = 0
        string = ""
        for c in text:
            c = chr(ord(c) + self.arr[j])
            string = string + c
            if j < len(self.arr)-1:
                j =j+1
            else:
                j = 0
        return string

    def Decrypt(self,text):
        j = 0
        string = ""
        for c in text:
            c = chr(ord(c) - self.arr[j])
            string = string + c
            if j < len(self.arr) - 1:
                j += 1
            else:
                j = 0
        return string