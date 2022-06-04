from io import FileIO
from headers import *
from typing import Dict

nextDiskID = 0
openFiles:Dict[int, FileIO] = {}

def openDisk(diskFile:str, nBytes:int = 0) -> int:
    if nBytes % BLOCKSIZE != 0:
        return ErrorCodes.BLOCKSIZE

    try:

        openFile = open(diskFile, 'rb+')
        # openFile = open(diskFile, 'rb+')
        global nextDiskID
        openFiles[nextDiskID] = openFile
        nextDiskID +=  1
        return SuccessCodes.SUCCESS
    except FileNotFoundError:
        return ErrorCodes.DISKNOTFOUND

def readBlock(diskID:int, bNum:int, blockBuffer:buffer, decryptionKey = None):
    if diskID in openFiles:
        openFiles[diskID].seek(bNum * BLOCKSIZE)

        if decryptionKey == None:
            blockBuffer.contents = openFiles[diskID].read(BLOCKSIZE)
        else:
            rawData = openFiles[diskID].read(BLOCKSIZE)
            decryptedData = decryptAES(rawData, decryptionKey)
            blockBuffer.contents = decryptedData
        return SuccessCodes.SUCCESS
    else:
        return ErrorCodes.DISKID

def writeBlock(diskID:int, bNum:int, blockBuffer:buffer, encryptionKey = None):
    if diskID in openFiles:
        try:
            openFiles[diskID].seek(bNum * BLOCKSIZE)
            if encryptionKey == None:
                bytesWritten = openFiles[diskID].write(blockBuffer.contents)
            else:
                bytesWritten = openFiles[diskID].write(encryptAES(blockBuffer.contents, encryptionKey))

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

