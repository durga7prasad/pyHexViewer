#! /usr/bin/python
# This is the Hex dump
# Author    :   VenkataDurgaPrasad.B
# Email     :   durgababu21@gmail.com
#

import sys
import os
import logging
from VUtil import *

IsVerbose = False
InFile = None
InFileHandle = None
OutFile = None
OutFileHandle = None
IsHelp = False
IsVersion = False
MinArgs = 2

def help():
    print ("usage: VHexDump [-h] [-i INPUT] [-o OUTPUT] [-v] [-V]\n")
    print ("dump/save the file content in Hexadecimal view\n")
    print ("options:\n\
                -h\n\
                        show this help message and exit\n\
                -i  [INPUT]\n\
                        input binfile to view in hex\n\
                -o  [OUTPUT]\n\
                        output file to save hex dump\n\
                -v\n\
                        Verbosity (more debug logs)\n\
                -V\n\
                        prints version and exit\n\
        \nMandatory arguments:\n\
                -i  [INPUT]\n\
                        binary file\n\
        \nOptional arguments:\n\
                -o  [OUTPUT]\n\
                        if not used, then hex data shall be displayed on stdout\n\
                -v\n\
                        default log level is Info, use -v to get debug logs\n\
               ")
    return

def VParseCmdArgs():
    global IsHelp, IsVerbose, IsVersion, InFile, OutFile
    args = sys.argv
    argcnt = len(args)
    #print (f"Total arg count {argcnt}")
    if argcnt < MinArgs:
        help()
        sys.exit(1)
    option = None
    value = None
    # The first element is the script name, so start from index 1
    for idx in range(1, (argcnt)):
        #print ("arg_{}{}{}" .format(idx, ": ", args[idx]))
        if args[idx].startswith('-'):
            option = args[idx][1:]
            #print ("Option: {}" .format(option))
            if option == "h":
                IsHelp = True
                continue
            elif option == "V":
                IsVersion = True
                continue
            elif option == "v":
                IsVerbose = True
                continue
            elif not (((option == "i") or (option == "o")) and (idx+1 < argcnt)):
                # argument option value missing
                print ("Expecting value for an argument/option\n")
                help()
                sys.exit(1)
        else:
            if option == None:
                # Invalid argument
                help()
                sys.exit(1)
            else:
                value = args[idx]
                #print ("Value: {}" .format(value))
                if option == "i":
                    InFile = value
                elif option == "o":
                    OutFile = value
                option = None

    if IsHelp == True:
        help()
        sys.exit(1)

    if IsVersion == True:
        str = banner("VHexDump V1.0")
        print(str)
        sys.exit(1)

    if IsVerbose == True:
        # debug logging level
        logging.basicConfig(format='%(message)s', level=logging.DEBUG)
    else:
        logging.basicConfig(format='%(message)s', level=logging.INFO)

    if InFile is None:
        logging.error ("Input binfile is required (use -h for more help)\n")
        sys.exit(1)
    else:
        logging.debug ("input file  -> {}" .format(InFile))

    # Verify file
    if not os.path.isfile(InFile):
        logging.error ("Infile ({}) does not exist".format(InFile))
        sys.exit(1)

    logging.debug("Checking output file ({})..." .format(OutFile))
    if not OutFile is None:
        if (os.path.exists(OutFile)):
            logging.debug("{} already exist, removing..." .format(OutFile))
            os.remove(OutFile)
    return

def VOpenFile():
    global InFileHandle, TotalSize, OutFileHandle
    # Open "InFile" file
    logging.debug ("Opening file -> {}" .format(InFile))
    try:
        InFileHandle = open(InFile, "rb")
    except Exception as err:
        print (f"System Error!! {err}")
        sys.exit(1)
    TotalSize = os.stat(InFile).st_size
    if not OutFile is None:
        # Open "OutFile" file
        logging.debug ("Opening file -> {}" .format(OutFile))
        try:
            OutFileHandle = open(OutFile, "w")
        except Exception as err:
            print (f"System Error!! {err}")
            sys.exit(1)
    else:
        OutFileHandle = None
        logging.debug("No output file selected, dumping hex data on stdout\n")
    return

def VCloseFile():
    logging.debug ("Closing file\n")
    if not InFileHandle is None:
        InFileHandle.close()
    if not OutFileHandle is None:
        OutFileHandle.close()


def main():
    # Parse command line arguments
    VParseCmdArgs()
    # open file
    VOpenFile()
    # Hex dump
    logging.debug ("VHexDump Start...\n")
    VHData = VHexDump(InFileHandle, TotalSize)
    for i in VHData:
        print(i)
    # close file
    VCloseFile()

# This is the main entry
if __name__ == '__main__':
    main()
