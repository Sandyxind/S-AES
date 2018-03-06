import SBoxs

exponentialTable = [0 for i in range(16)]
logTable = [0 for i in range(16)]
invTable = [[] for i in range(16)]

SBoxs = [[0 for i in range(4)] for i in range(4)]
InvSBoxs = [[0 for i in range(4)] for i in range(4)]
Content = [[0 for i in range(2)] for i in range(2)]
Key = [0 for i in range(6)]

def defaultBox():
    SBoxs[0][0] = 0x9
    SBoxs[0][1] = 0x4
    SBoxs[0][2] = 0xA
    SBoxs[0][3] = 0xB

    SBoxs[1][0] = 0xD
    SBoxs[1][1] = 0x1
    SBoxs[1][2] = 0x8
    SBoxs[1][3] = 0x5

    SBoxs[2][0] = 0x6
    SBoxs[2][1] = 0x2
    SBoxs[2][2] = 0x0
    SBoxs[2][3] = 0x3

    SBoxs[3][0] = 0xC
    SBoxs[3][1] = 0xE
    SBoxs[3][2] = 0xF
    SBoxs[3][3] = 0x7

def defaultInvBox():
    InvSBoxs[0][0] = 0xA
    InvSBoxs[0][1] = 0x5
    InvSBoxs[0][2] = 0x9
    InvSBoxs[0][3] = 0xB

    InvSBoxs[1][0] = 0x1
    InvSBoxs[1][1] = 0x7
    InvSBoxs[1][2] = 0x8
    InvSBoxs[1][3] = 0xF

    InvSBoxs[2][0] = 0x6
    InvSBoxs[2][1] = 0x0
    InvSBoxs[2][2] = 0x2
    InvSBoxs[2][3] = 0x3

    InvSBoxs[3][0] = 0xC
    InvSBoxs[3][1] = 0x4
    InvSBoxs[3][2] = 0xD
    InvSBoxs[3][3] = 0xE

class GetKeys:
    def sepKey(genkey,number):
        leftkey = genkey >> number
        if number == 8:
            rightKey = genkey & 0x00FF
        elif number == 4:
            rightKey = genkey & 0x0F
        elif number == 2:
            rightKey = genkey & 0x3
        return leftkey, rightKey

    def g(w, rc):
        global SBoxs
        # P193 step 1
        n0, n1 = GetKeys.sepKey(w, 4)
        #step 2
        n0, n1 = GetKeys.substitution(n0, n1)
        #step 3
        FinalN = n1 << 4 | n0
        if rc == 1:
            Finalw = FinalN ^ 0x80
        elif rc == 2:
            Finalw = FinalN ^ 0x30
        return Finalw

    #just for 8-bits 0000 0000
    def substitution(left, right):
        defaultBox()
        n0Left, n0Right = GetKeys.sepKey(left, 2)
        n0 = SBoxs[n0Left][n0Right]
        n1Left, n1Right = GetKeys.sepKey(right, 2)
        n1 = SBoxs[n1Left][n1Right]
        return n0, n1

    def invSubstitution(left, right):
        defaultInvBox()
        n0Left, n0Right = GetKeys.sepKey(left, 2)
        n0 = InvSBoxs[n0Left][n0Right]
        n1Left, n1Right = GetKeys.sepKey(right, 2)
        n1 = InvSBoxs[n1Left][n1Right]
        return n0, n1

    def XOR (rc,  w0, w1):
        w2 = w0 ^ GetKeys.g(w1, rc)
        w3 = w2 ^ w1
        return w2, w3

key = 0b1010011100111011
w0, w1 = GetKeys.sepKey(key, 8)
print("0  ", bin(w0))
print("1  ", bin(w1))
w2, w3 = GetKeys.XOR(1, w0, w1)
w4, w5 = GetKeys.XOR(2, w2, w3)

print("2  ", bin(w2))
print("3  ", bin(w3))

print("4  ", bin(w4))
print("5  ", bin(w5))

class Process:
    global Content
    def sepContent(content):
        up, down = GetKeys.sepKey(content, 8)
        Content[0][0], Content[0][1] = GetKeys.sepKey(up, 4)
        Content[1][0], Content[1][1] = GetKeys.sepKey(down, 4)

    def addKey(plaintext,key1, key2):
        key = [[0 for i in range(2)] for i in range(2)]
        key[0][0], key[0][1] = GetKeys.sepKey(key1, 4)
        key[1][0], key[1][1] = GetKeys.sepKey(key2, 4)

        plaintext[0][0] ^= key[0][0]
        plaintext[0][1] ^= key[0][1]
        plaintext[1][0] ^= key[1][0]
        plaintext[1][1] ^= key[1][1]

    def shiftRow(sub):
        a = sub[0][1]
        sub[0][1] = sub[1][1]
        sub[1][1] = a

    def mixColumns(content):
        p00 = GF24.GFmul(content[0][0], 1) ^ GF24.GFmul(content[0][1], 4)
        p10 = GF24.GFmul(content[1][0], 1) ^ GF24.GFmul(content[1][1], 4)
        p01 = GF24.GFmul(content[0][0], 4) ^ GF24.GFmul(content[0][1], 1)
        p11 = GF24.GFmul(content[1][0], 4) ^ GF24.GFmul(content[1][1], 1)
        content[0][0] = p00
        content[0][1] = p01
        content[1][0] = p10
        content[1][1] = p11

    def invMixColumns(content):
        p00 = GF24.GFmul(content[0][0], 9) ^ GF24.GFmul(content[0][1], 2)
        p10 = GF24.GFmul(content[1][0], 9) ^ GF24.GFmul(content[1][1], 2)
        p01 = GF24.GFmul(content[0][0], 2) ^ GF24.GFmul(content[0][1], 9)
        p11 = GF24.GFmul(content[1][0], 2) ^ GF24.GFmul(content[1][1], 9)
        content[0][0] = p00
        content[0][1] = p01
        content[1][0] = p10
        content[1][1] = p11

    def fullBinary(number):
        printSt = str(number).replace("0b","")
        if len(printSt) - 16 < 0:
            printSt = (16 - len(printSt)) * '0' + printSt
        return printSt

    def show(plaintext):
        printFin = ""
        printBinary = plaintext[0][0] << 12 | plaintext[0][1] << 8 | plaintext[1][0] << 4 |plaintext[1][1]
        printSt = str(bin(printBinary)).replace("0b","")
        if len(printSt) - 16 < 0:
            printSt = (16 - len(printSt)) * '0' + printSt
        i = 0
        while i + 4 <= 16 :
            printFin += printSt[i:i+4] + " "
            i = i + 4
        return printFin

    def inputDeal(orgText):
        textFin = ""
        try:
            for i in range(0,4):
                textFin += orgText.split()[i]
            return textFin
        except IndexError:
            textFin = orgText
            return textFin

Process.sepContent(0x6f6b)
print("up ", bin(Content[0][0]),"right ", bin(Content[0][1]))
print("down ", bin(Content[1][0]),"right ", bin(Content[1][1]))


class GF24:

    def exponentialTables():
        exponentialTable[0] = 1
        for i in range(1, 16):
            exponentialTable[i] = (exponentialTable[i - 1] << 1) ^ exponentialTable[i - 1]
            if exponentialTable[i] > 15:
                exponentialTable[i] ^= 0x13

    def logTables():
        logTable[0] = 0
        for i in range(0, 16):
            logTable[exponentialTable[i]] = i

    def invTables():
        for i in range(1, 15):
            k = logTable[i]
            k = 15 - k;
            k %= 15
            invTable[i].append(exponentialTable[k])

    def GFmul(number1, number2):
        global exponentialTable, logTable
        if number1 and number2:
            return exponentialTable[(logTable[number1] + logTable[number2]) % 15]
        else:
            return 0

    def GFdivide(number1, number2):
        global invTable
        if number2 != 0:
            return GF24.GFmul(number1, invTable[number2][0])
        else:
            return "Numebr cannot be set 0"


def key(inputKey):
    global Key
    Key[0], Key[1] = GetKeys.sepKey(inputKey, 8)
    Key[2], Key[3] = GetKeys.XOR(1, w0, w1)
    Key[4], Key[5] = GetKeys.XOR(2, w2, w3)

def roundOne(plaintexts):
    global Key, Content
    # round 0
    Process.sepContent(plaintexts)
    Process.addKey(Content, Key[0], Key[1])
    Content[0][0], Content[0][1] = GetKeys.substitution(Content[0][0], Content[0][1])
    Content[1][0], Content[1][1] = GetKeys.substitution(Content[1][0], Content[1][1])
    Process.shiftRow(Content)
    Process.mixColumns(Content)
    Process.addKey(Content, Key[2], Key[3])

def roundTwo():
    Content[0][0], Content[0][1] = GetKeys.substitution(Content[0][0], Content[0][1])
    Content[1][0], Content[1][1] = GetKeys.substitution(Content[1][0], Content[1][1])
    Process.shiftRow(Content)
    Process.addKey(Content, Key[4], Key[5])

def decryptionRoundOne(plaintexts):
    global Content
    Process.sepContent(plaintexts)
    Process.addKey(Content, Key[4], Key[5])
    Process.shiftRow(Content)
    Content[0][0], Content[0][1] = GetKeys.invSubstitution(Content[0][0], Content[0][1])
    Content[1][0], Content[1][1] = GetKeys.invSubstitution(Content[1][0], Content[1][1])
    Process.addKey(Content, Key[2],Key[3])
    Process.invMixColumns(Content)

def decryptionRoundTwo():
    global Content
    Process.shiftRow(Content)
    Content[0][0], Content[0][1] = GetKeys.invSubstitution(Content[0][0], Content[0][1])
    Content[1][0], Content[1][1] = GetKeys.invSubstitution(Content[1][0], Content[1][1])
    Process.addKey(Content, Key[0], Key[1])

def encryption(plaintext):
    roundOne(plaintext)
    roundTwo()

def decryption(plaintext):
    decryptionRoundOne(plaintext)
    decryptionRoundTwo()


def main():
    global Content
    GF24.exponentialTables()
    GF24.logTables()
    GF24.invTables()
    AES = True
    choice = 0
    while AES:
        choice = input("what do you want to do? 1. Encryption 2. Decryption 3.Exit ")
        if choice is "1":
            plaintexts = input("Please input plaintext: ")
            keys = input("Please input key: ")
            plaintexts = Process.inputDeal(plaintexts)
            keys = Process.inputDeal(keys)
            if len(Process.fullBinary(keys)) or len(Process.fullBinary(plaintexts)) is not 16:
                print("Please enter right keys or plaintexts: ")
                continue
            key(int(keys, 2))
            encryption(int(plaintexts, 2))
            printShow = Process.show(Content)
            print("The ciphertext is: ", printShow)
        elif choice is "2":
            ciphertext = input("Please input ciphertext ")
            keys = input("Please input key: ")
            ciphertext = Process.inputDeal(ciphertext)
            keys = Process.inputDeal(keys)
            if len(Process.fullBinary(keys)) or len(Process.fullBinary(ciphertext)) is not 16:
                print("Please enter right keys or plaintexts: ")
                continue
            key(int(keys, 2))
            decryption(int(ciphertext, 2))
            printShow = Process.show(Content)
            print("The plaintext is: ", printShow)
        elif choice is "3":
            AES = False
        else:
            print("Please input right number.")

main()
