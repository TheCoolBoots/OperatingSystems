from headers import *
import libDisk as dsk

fileDescriptor = int
currentMountedDisk:superblock = None
currentMountedDiskID:int = None

def tfs_mkfs(diskName:str, diskSizeBytes:int) -> int:
    newDisk = disk(diskSizeBytes)
    serialized = newDisk.serialize()
    with open(diskName, 'wb+') as diskFile:
        diskFile.write(serialized)
        return SuccessCodes.SUCCESS


def tfs_mount(diskName:str) -> int:
    currentMountedDiskID = dsk.nextDiskID
    returnCode = dsk.openDisk(diskName)
    if returnCode == SuccessCodes.SUCCESS:
        if currentMountedDisk != None:
            superblkBuffer = buffer(256)
            dsk.readBlock(currentMountedDiskID, 0, superblkBuffer)
            currentMountedDisk = bytesToSuperblock(superblkBuffer.contents)
            return SuccessCodes.SUCCESS
        else:
            return ErrorCodes.DISKMOUNT
    return returnCode


def tfs_unmount() -> int:
    if currentMountedDisk == None:
        return ErrorCodes.DISKMOUNT
    currentMountedDisk = None
    return dsk.closeDisk(currentMountedDisk) 

def tfs_open(filename:str) -> fileDescriptor:
    pass

def tfs_close(FD:fileDescriptor) -> int:
    pass

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




