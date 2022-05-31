from io import FileIO
from headers import *
from typing import Dict


openFiles:Dict[int, FileIO] = {}
nextDiskID = 0

def openDisk(diskFile:str, nBytes:int) -> int:
    if nBytes % BLOCKSIZE != 0:
        return ErrorCodes.BLOCKSIZE

    try:
        openFile = open(diskFile, 'rwb+')
        openFile = open(diskFile, 'rb+')
        openFiles[nextDiskID] = openFile
        nextDiskID = nextDiskID + 1
        return SuccessCodes.SUCCESS
    except FileNotFoundError:
        return ErrorCodes.DISKNOTFOUND

def readBlock(diskID:int, bNum:int, blockBuffer:buffer):
    if diskID in openFiles:
        try:
            # this might allow us to not require to read the whole 
            # file every time we want to read/write
            openFiles[diskID].seek(bNum * BLOCKSIZE)
            blockBuffer.contents = openFiles[diskID].read(BLOCKSIZE)
            return SuccessCodes.SUCCESS
        except:
            return ErrorCodes.INVALIDBLOCKNUM
    else:
        return ErrorCodes.DISKID

def writeBlock(diskID:int, bNum:int, blockBuffer:buffer):
    if diskID in openFiles:
        # fileContents = openFiles[diskID].read()
        # try:
        #     fileContents[BLOCKSIZE*bNum : BLOCKSIZE*(bNum + 1)] = blockBuffer.contents
        #     openFiles[diskID].write(fileContents)
        try:
            # this might allow us to not require to read the whole 
            # file every time we want to read/write
            openFiles[diskID].seek(bNum * BLOCKSIZE)
            bytesWritten = openFiles[diskID].write(blockBuffer.contents)
            if bytesWritten == BLOCKSIZE:
                return SuccessCodes.SUCCESS
            else:
                return ErrorCodes.IOERROR
        except IndexError:
            return ErrorCodes.INVALIDBLOCKNUM
    else:
        return ErrorCodes.DISKID

def closeDisk(diskID:int):
    if diskID in openFiles:
        openFiles[diskID].close()
        openFiles.pop(diskID)
        return SuccessCodes.SUCCESS
    else:
        return ErrorCodes.DISKID

