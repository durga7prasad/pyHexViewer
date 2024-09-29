#! /usr/bin/python
# This is util file with different utility functions
# Author    :   VenkataDurgaPrasad.B
# Email     :   durgababu21@gmail.com
#

import sys
import os

ascii_db = [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".",
            ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".",
            ".", "!", "\"", "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/",
            "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":", ";", "<", "=", ">", "?",
            "@", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O",
            "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "[", "\\", "]", "^", "_",
            "`", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o",
            "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "{", "|", "}", "~", ".",
            ]

def banner(name, style_character='*'):
    banner_frame = style_character * (len(name) + 4)
    str = banner_frame
    str += "\n"
    str += ('{0} {1} {0}'.format(style_character, name))
    str += "\n"
    str += banner_frame
    return str

def VHexDump(fileHandle, filesize):
    Addr = 0
    readCnt = 1
    curCnt = 1
    Hdata = []
    outstr = []
    while True:
        byte = fileHandle.read(1).hex()
        if byte:
            if (readCnt % 16 == 0) or (readCnt == filesize):
                Hdata.append(byte)
                hdatalimit = curCnt
                # Add address
                str = "{:08x}".format(Addr)
                str += ":\t"
                # Add binary hex data
                for i in range(0, hdatalimit):
                    str += "{} ".format(Hdata[i])
                for i in range(hdatalimit, 16):
                    str += ".. "
                str += "\t\t"
                #add ascii equivalent
                for i in range(0, hdatalimit):
                    tmp = int(Hdata[i], base=16)
                    # We use 7bit ascii, so lets ignore values greater than 127
                    if tmp > 127:
                        str += "."
                    else:
                        str += ascii_db[int(Hdata[i], base=16)]
                for i in range(hdatalimit, 16):
                    str += "."
                outstr.append(str)
                Addr += 16
                Hdata.clear()
                curCnt = 0
            else:
                Hdata.append(byte)
            readCnt += 1
            curCnt += 1
        else:
            break
    return outstr
