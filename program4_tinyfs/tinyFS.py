from headers import *
import libDisk as disk

fileDescriptor = int
dynanmicResourceTable = []

class dynamicResourceTableEntry: 
    def __init__(self, filename, filepointer  ):
        self.filename = filename
        self.filepointer = filepointer


def tfs_mkfs(diskName:str, diskSizeBytes:int) -> int:
    pass

def tfs_mount(diskName:str) -> int:
    pass

def tfs_unmount() -> int:
    pass

def tfs_open(filename:str) -> fileDescriptor:
    pass
    #search through currentMountedDisk for inode
    for i, curInode in enumerate(currentMountedDisk.blocks):
        if curInode == filename: #there isnt a filename attribute in the super block
            #create a dynamic resource table entry
            dynanmicResourceTable.append(dynamicResourceTableEntry(filename, 0)) #filename,internal file pointer 
            #successful = disk.openDisk(filename, curInode.filesize) #open file?
            # return file descriptor , the index in the dynamic Resoruce table?



def tfs_close(FD:fileDescriptor) -> int:
    dynanmicResourceTable.remove(fileDescriptor)
    #closeDisk?


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




