from headers import *
import libDisk as disk

fileDescriptor = int

def tfs_mkfs(diskName:str, diskSizeBytes:int) -> int:
    pass

def tfs_mount(diskName:str) -> int:
    pass

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




