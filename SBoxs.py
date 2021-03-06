SBoxs = [[None for _ in range(4)] for _ in range(4)]
InvSBoxs = [[None for _ in range(4)] for _ in range(4)]

def defaultBox():
    SBoxs[0x00][0x00] = 0x9
    SBoxs[0x00][0x01] = 0x4
    SBoxs[0x00][0x10] = 0xA
    SBoxs[0x00][0x11] = 0xB

    SBoxs[0x01][0x00] = 0xD
    SBoxs[0x01][0x01] = 0x1
    SBoxs[0x01][0x10] = 0x8
    SBoxs[0x01][0x11] = 0x5

    SBoxs[0x10][0x00] = 0x6
    SBoxs[0x10][0x01] = 0x2
    SBoxs[0x10][0x10] = 0x0
    SBoxs[0x10][0x11] = 0x7

    SBoxs[0x11][0x00] = 0xC
    SBoxs[0x11][0x01] = 0xE
    SBoxs[0x11][0x10] = 0xF
    SBoxs[0x11][0x11] = 0x7

def defaultInvBox():
    #Invbox
    InvSBoxs[0x00][0x00] = 0xA
    InvSBoxs[0x00][0x01] = 0x5
    InvSBoxs[0x00][0x10] = 0x9
    InvSBoxs[0x00][0x11] = 0xB

    InvSBoxs[0x01][0x00] = 0x1
    InvSBoxs[0x01][0x01] = 0x7
    InvSBoxs[0x01][0x10] = 0x8
    InvSBoxs[0x01][0x11] = 0xF

    InvSBoxs[0x10][0x00] = 0x6
    InvSBoxs[0x10][0x01] = 0x0
    InvSBoxs[0x10][0x10] = 0x2
    InvSBoxs[0x10][0x11] = 0x3

    InvSBoxs[0x11][0x00] = 0xC
    InvSBoxs[0x11][0x01] = 0x4
    InvSBoxs[0x11][0x10] = 0xD
    InvSBoxs[0x11][0x11] = 0xE