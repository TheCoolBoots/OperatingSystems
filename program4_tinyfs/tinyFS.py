from headers import *
import libDisk as dsk

fileDescriptor = int
currentMountedDisk:disk = None

def tfs_mkfs(diskName:str, diskSizeBytes:int) -> int:
    newDisk = disk(diskSizeBytes)
    serialized = newDisk.serialize()
    with open(diskName, 'wb+') as diskFile:
        diskFile.write(serialized)

def tfs_mount(diskName:str) -> int:
    tmpDisk = disk()
    with open(diskName, 'rb') as diskFile:
        serialized = diskFile.read()

def tfs_unmount() -> int:
    pass

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




