from headers import *


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

