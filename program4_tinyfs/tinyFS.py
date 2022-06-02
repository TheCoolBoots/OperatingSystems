from asyncio.windows_events import NULL
from headers import *
import libDisk as dsk
from typing import Dict

fileDescriptor = int
dynamicResourceTable : Dict[int, dynamicResourceTableEntry] = {}
FDCounter = 0

currentMountedDisk:superblock = None
currentMountedDiskID:int = None

def tfs_mkfs(diskName:str, diskSizeBytes:int) -> int:
    # create a brand new disk
    # NOTE: this is the only time we should ever use the disk class
    newDisk = disk(diskSizeBytes)

    # convert the disk into bytes
    serialized = newDisk.serialize()

    # write the formatted disk to the given filename
    with open(diskName, 'wb+') as diskFile:
        diskFile.write(serialized)
        return SuccessCodes.SUCCESS


def tfs_mount(diskName:str) -> int:

    # save the DiskID of the disk that will be opened
    currentMountedDiskID = dsk.nextDiskID

    # open the disk
    returnCode = dsk.openDisk(diskName)
    if returnCode == SuccessCodes.SUCCESS:
        if currentMountedDisk != None:
            superblkBuffer = buffer(256)

            # read the superblock of the opened disk
            dsk.readBlock(currentMountedDiskID, 0, superblkBuffer)

            # convert the raw bytes into a superblock class
            currentMountedDisk = bytesToSuperblock(superblkBuffer.contents)

            return SuccessCodes.SUCCESS
        else:
            return ErrorCodes.DISKMOUNT
    return returnCode


def tfs_unmount() -> int:
    if currentMountedDisk == None:
        return ErrorCodes.DISKMOUNT

    # close all open files, committing them to disk

    # write the superblock of the current FS to disk
    dsk.writeBlock(currentMountedDiskID, 0, buffer(currentMountedDisk.toBytes()))
    
    currentMountedDisk = None
    return dsk.closeDisk(currentMountedDisk) 

def tfs_open(filename:str) -> fileDescriptor:
    
    b = buffer(BLOCKSIZE)
    dsk.readBlock(currentMountedDiskID, currentMountedDisk.rootDirINode, b)
    rootDirINode = bytesToINode(b.contents)

    for dataBlockID in rootDirINode.dataBlockPtrs:
        dsk.readBlock(currentMountedDiskID, dataBlockID, b)
        for i in range(0, 256, 16):
            fName = b.contents[i:i+12].decode("utf-8")
            fileINode = int.from_bytes(b.contents[i+12:i+16], 'little')
            if(fName == filename):

                #make dynamicResourceTableEntry, add it to the table 
                b = buffer()
                dsk.readBlock(currentMountedDiskID, fileINode, b)
                dynamicResourceTable[FDCounter] = dynamicResourceTableEntry(fileINode, bytesToINode(b.contents))
            
                #increment FD Counter
                returnFD = FDCounter
                FDCounter = FDCounter + 1

                #return the file descriptor
                return returnFD


def tfs_close(FD:fileDescriptor) -> int:
    try:
        entry = dynamicResourceTable.pop(FD)
        b = buffer(entry.memINode.toBytes())
        dsk.writeBlock(currentMountedDiskID, entry.inodeBlockNum, b)

        return SuccessCodes.SUCCESS
    except KeyError:
        return -1


def tfs_write(FD:fileDescriptor, writeBuffer:buffer, size:int):
    fileINode = dynamicResourceTable[FD].memINode
    bytesToWrite = len(writeBuffer.contents)
    valuePtr = 0

    if fileINode.filesize > fileINode.filePointer + size:
        # don't need to allocate any new datablocks
        pass
    else:
        # TODO
        # maxSize = num 0's in dataBlockPtrs * 256
        # make maxSize > fileINode.filesize + size by allocating new blocks
        pass


    # freeBytes in current block = 256 - (fileINode.filePointer % 256)

    # get the index of the first data block we will modify
    dataBlockIndex = fileINode.filePointer//BLOCKSIZE

    # get the number of bytes that can be overwritten in the first data block
    overwriteInBlock = 256 - (fileINode.filePointer % 256)

    # read the block @ dataBlockIndex
    b = buffer()
    dsk.readBlock(currentMountedDiskID, fileINode.dataBlockPtrs[dataBlockIndex], b)

    # we will fill the block that the file pointer is in
    if overwriteInBlock < bytesToWrite:
        # build the contents of the new block
        newContents = b.contents[0:overwriteInBlock] + writeBuffer[valuePtr:valuePtr+overwriteInBlock]
        
        # write the new contents to the disk
        dsk.writeBlock(currentMountedDiskID, fileINode.dataBlockPtrs[dataBlockIndex], buffer(newContents))

        # increment the current index of the values we are writing
        valuePtr += overwriteInBlock
        bytesToWrite -= overwriteInBlock
        fileINode.filePointer += overwriteInBlock
        dataBlockIndex += 1
    
    # will not fill the block that the file pointer is in
    else:
        # build the contents of the new block
        blockPtr = fileINode.filePointer % 256
        newContents = b.contents[0:blockPtr] + writeBuffer[valuePtr:valuePtr+bytesToWrite] + b.contents[blockPtr + bytesToWrite:]
        
        # write the new contents to the disk
        dsk.writeBlock(currentMountedDiskID, fileINode.dataBlockPtrs[dataBlockIndex], buffer(newContents))

        # increment the current index of the values we are writing
        bytesToWrite = 0

    # write all the blocks that will fill up a whole block
    while bytesToWrite >= BLOCKSIZE:
        dsk.writeBlock(currentMountedDiskID, fileINode.dataBlockPtrs[dataBlockIndex], writeBuffer.contents[valuePtr:valuePtr+BLOCKSIZE])
        valuePtr += BLOCKSIZE
        bytesToWrite -= BLOCKSIZE
        fileINode.filePointer += BLOCKSIZE
        dataBlockIndex += 1

    if bytesToWrite > 0:
        # write the remaining bytes in values to the next data block
        dsk.readBlock(currentMountedDiskID, fileINode.dataBlockPtrs[dataBlockIndex], b)
        newContents = writeBuffer.contents[:valuePtr] + b.contents[bytesToWrite:]
        dsk.writeBlock(currentMountedDiskID, fileINode.dataBlockPtrs[dataBlockIndex], buffer(newContents))

    

# deletes a file and marks its blocks as free on disk. 
def tfs_delete(FD:fileDescriptor) -> int:

    
    #remove it from table 
    entry = dynamicResourceTable.pop(FD)

    b = buffer(BLOCKSIZE)
    dsk.readBlock(currentMountedDiskID, currentMountedDisk.rootDirINode, b)
    rootDirINode = bytesToINode(b.contents)

    for dataBlockID in rootDirINode.dataBlockPtrs:
        dsk.readBlock(currentMountedDiskID, dataBlockID, b)
        for i in range(0, 256, 16):
            fName = b.contents[i:i+12].decode("utf-8")
            fileINode = int.from_bytes(b.contents[i+12:i+16], 'little')
            for dataBlockPTR in fileINode.dataBlockPtrs:
                index = int.from_bytes(dataBlockPTR)
                currentMountedDisk.rootDirINode.freeBlocks = currentMountedDisk.rootDirINode.freeBlocks[0: index - 1] + '1' + currentMountedDisk.rootDirINode.freeBlocks[index + 1:]
            
    #decrement counter
    FDCounter = FDCounter - 1
    pass

def tfs_readByte(FD:fileDescriptor, buff:buffer) -> int:
    pass

def tfs_seek(FD:fileDescriptor, offset:int) -> int:
    INode = dynamicResourceTable.get(fileDescriptor)
    checkValue = INode.filePointer + offset
    if(checkValue <= INode.filesize):
        INode.filePointer = INode.filePointer + offset
        return SuccessCodes.SUCCESS


def tfs_rename(FD:fileDescriptor, newName:str) -> int:
    pass

def tfs_readdir() -> None:
    pass




