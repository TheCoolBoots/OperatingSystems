from enum import Enum
from msilib.schema import Error

class SuccessCodes(Enum):
    SUCCESS = 0

class ErrorCodes(Enum):
    DISKNOTFOUND = -1
    BLOCKSIZE = -2
    DISKID = -3
    INVALIDBLOCKNUM = -4


BLOCKSIZE = 256

class buffer():
    def __init__(self):
        self.contents = bytes(BLOCKSIZE)

openFiles = {}
nextDiskID = 0

def openDisk(diskFile:str, nBytes:int) -> int:
    if nBytes % BLOCKSIZE != 0:
        return ErrorCodes.BLOCKSIZE

    try:
        if nBytes > 0:
            openFile = open(diskFile, 'rwb')
        elif nBytes == 0:
            openFile = open(diskFile, 'rb')
        openFiles[nextDiskID] = openFile
        nextDiskID = nextDiskID + 1
        return SuccessCodes.SUCCESS
    except FileNotFoundError:
        return ErrorCodes.DISKNOTFOUND

def readBlock(diskID:int, bNum:int, blockBuffer:buffer):
    if diskID in openFiles:
        fileContents = openFiles[diskID].read()
        try:
            blockBuffer.contents = fileContents[BLOCKSIZE * bNum:BLOCKSIZE * (bNum + 1)]
            return SuccessCodes.SUCCESS
        except IndexError:
            return ErrorCodes.INVALIDBLOCKNUM
    else:
        return ErrorCodes.DISKID

def writeBlock(diskID:int, bNum:int, blockBuffer:buffer):
    if diskID in openFiles:
        fileContents = openFiles[diskID].read()
        try:
            fileContents[BLOCKSIZE*bNum : BLOCKSIZE*(bNum + 1)] = blockBuffer.contents
            openFiles[diskID].write(fileContents)
            return SuccessCodes.SUCCESS
        except IndexError:
            return ErrorCodes.INVALIDBLOCKNUM
    else:
        return ErrorCodes.DISKID

def closeDisk(diskID:int):
    if diskID in openFiles:
        openFiles[diskID].close()
        openFiles.remove(diskID)
        return SuccessCodes.SUCCESS
    else:
        return ErrorCodes.DISKID

