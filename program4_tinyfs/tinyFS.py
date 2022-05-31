from encodings import utf_8
from headers import *
import libDisk as dsk

fileDescriptor = int
dynanmicResourceTable = []
FDCounter = 0

<<<<<<< Updated upstream
class dynamicResourceTableEntry:  #file descriptor and inode indexes
    def __init__(self, fDescriptor, inodeBlockNum):
        self.fDescriptor = fDescriptor
        self.inodeBlockNum = inodeBlockNum
=======
class dynamicResourceTableEntry: 
    def __init__(self, filename, filepointer):
        self.filename = filename
        self.filepointer = filepointer
>>>>>>> Stashed changes

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

                dynanmicResourceTable.append(dynamicResourceTableEntry(FDCounter, fileINode))
            
                #increment FD Counter
                returnFD = FDCounter
                FDCounter = FDCounter + 1

                #return the file descriptor
                return returnFD


def tfs_close(FD:fileDescriptor) -> int:
    dynanmicResourceTable.remove(fileDescriptor)
    return SuccessCodes.SUCCESS


def tfs_write(FD:fileDescriptor, values:buffer, size:int):
    pass

def tfs_delete(FD:fileDescriptor) -> int:
    pass

def tfs_readByte(FD:fileDescriptor, buff:buffer) -> int:
    pass

def tfs_seek(FD:fileDescriptor, offset:int) -> int:
    pass

def tfs_rename(FD:fileDescriptor, newName:str) -> int:
    pass

def tfs_readdir() -> None:
    pass




