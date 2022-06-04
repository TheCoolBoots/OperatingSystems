from headers import *
import libDisk as dsk
from typing import Dict
from math import ceil
from hashlib import md5
from Crypto.Cipher import AES

fileDescriptor = int
dynamicResourceTable : Dict[int, dynamicResourceTableEntry] = {}
FDCounter = 0

cmd:superblock = None
cmdid:int = None
hashedKey = None


def readHelper(targetBlock, b:buffer):
    global hashedKey
    if hashedKey == None:
        dsk.readBlock(cmdid, targetBlock, b)
    else:
        dsk.readBlock(cmdid, cmd.IVNode, b, hashedKey, cmd.IVNodeIV)
        iv = b.contents[AES.block_size*(targetBlock -1) : AES.block_size*targetBlock]
        dsk.readBlock(cmdid, targetBlock, b, hashedKey, iv)

def writeHelper(targetBlock, b:buffer):
    global hashedKey
    if hashedKey == None:
        dsk.writeBlock(cmdid, targetBlock, b)
    else:
        dsk.readBlock(cmdid, cmd.IVNode, b, hashedKey, cmd.IVNodeIV)
        iv = b.contents[AES.block_size*(targetBlock -1) : AES.block_size*targetBlock]
        dsk.writeBlock(cmdid, targetBlock, b, hashedKey, iv)

def tfs_mkfs(diskName:str, diskSizeBytes:int, rawKey = None) -> int:
    # create a brand new disk
    # NOTE: this is the only time we should ever use the disk class
    if rawKey != None:
        hk = md5(rawKey.encode('utf8')).digest()
    else:
        hk = None
    newDisk = disk(diskSizeBytes, hk)


    # convert the disk into bytes
    serialized = newDisk.serialize()

    if rawKey != None:
        rootDirIV = get_random_bytes(AES.block_size)
        rootDirDataIV = get_random_bytes(AES.block_size)
        encryptedRootDir = encryptAES(serialized[BLOCKSIZE:BLOCKSIZE*2], hk, rootDirIV)
        encryptedRootDirData = encryptAES(serialized[BLOCKSIZE*2:BLOCKSIZE*3], hk, rootDirDataIV)
        IVNodeData = rootDirIV + rootDirDataIV + newDisk.blocks[0].IVNodeIV
        encryptedIVNodeData = encryptAES(IVNodeData, hk, newDisk.blocks[0].IVNodeIV)
        serialized = serialized[0:BLOCKSIZE] + encryptedRootDir + encryptedRootDirData + encryptedIVNodeData + serialized[BLOCKSIZE * 4:]

    # write the formatted disk to the given filename
    with open(diskName, 'wb+') as diskFile:
        diskFile.write(serialized)
        return SuccessCodes.SUCCESS


def tfs_mount(diskName:str, rawKey = None) -> int:

    # save the DiskID of the disk that will be opened
    global cmdid
    global cmd
    global hashedKey
    cmdid = dsk.nextDiskID
    if rawKey != None:
        hashedKey = md5(rawKey.encode('utf8')).digest()
        # print(hashedKey)

    # open the disk
    returnCode = dsk.openDisk(diskName)
    if returnCode == SuccessCodes.SUCCESS:
        if cmd == None:
            superblkBuffer = buffer()

            # read the superblock of the opened disk
            dsk.readBlock(cmdid, 0, superblkBuffer)

            # convert the raw bytes into a superblock class
            cmd = bytesToSuperblock(superblkBuffer.contents)

            return SuccessCodes.SUCCESS
        else:
            return ErrorCodes.DISKMOUNT
    return returnCode


def tfs_unmount() -> int:
    global cmd
    global cmdid
    global hashedKey

    if cmd == None:
        return ErrorCodes.DISKMOUNT

    # close all open files, committing them to disk
    files = list(dynamicResourceTable.keys())
    for i in files:
        tfs_close(i)

    # write the superblock of the current FS to disk
    dsk.writeBlock(cmdid, 0, buffer(cmd.toBytes()))
    
    cmd = None
    hashedKey = None
    return dsk.closeDisk(cmdid) 


def tfs_open(filename:str) -> fileDescriptor:
    global FDCounter
    global hashedKey

    b = buffer(BLOCKSIZE)
    readHelper(cmd.rootDirINode, b)

    rootDirINode = bytesToINode(b.contents)

    for dataBlockID in rootDirINode.dataBlockPtrs:
        if dataBlockID != 0:
            readHelper(dataBlockID, b)
            for i in range(0, 256, 16):
                fName = b.contents[i:i+12].decode("utf-8").replace('_', '')
                fileINodeIndex = int.from_bytes(b.contents[i+12:i+16], 'little')
                if(fName == filename):
                    readHelper(fileINodeIndex, b)

                    fileINode = bytesToINode(b.contents)
                    dynamicResourceTable[FDCounter] = dynamicResourceTableEntry(fileINodeIndex, fileINode)
                
                    #increment FD Counter
                    returnFD = FDCounter
                    FDCounter = FDCounter + 1

                    #return the file descriptor
                    return returnFD
    return ErrorCodes.FILENOTFOUND


def tfs_close(FD:fileDescriptor) -> int:
    global hashedKey
    try:
        entry = dynamicResourceTable.pop(FD)
        b = buffer(entry.memINode.toBytes())
        writeHelper(entry.inodeBlockNum, b)   

        return SuccessCodes.SUCCESS
    except KeyError:
        return -1


def tfs_write(FD:fileDescriptor, writeBuffer:buffer, size:int):
    global hashedKey
    fileINode = dynamicResourceTable[FD].memINode
    bytesToWrite = size
    valuePtr = 0


    blocksAllocated = ceil(fileINode.filesize/BLOCKSIZE)
    blocksNeeded = ceil((fileINode.filePointer + size)/BLOCKSIZE)
    if blocksNeeded > blocksAllocated:
        i = 0
        while fileINode.dataBlockPtrs[i] != 0:
            i += 1
        for j in range(0, blocksNeeded - blocksAllocated):
            fileINode.dataBlockPtrs[i+j] = cmd.getNextFreeBlockIndex()
            # TODO make sure the inode is getting updated in the DRT


    # freeBytes in current block = 256 - (fileINode.filePointer % 256)

    # get the index of the first data block we will modify
    dataBlockIndex = fileINode.filePointer//BLOCKSIZE

    # get the number of bytes that can be overwritten in the first data block
    overwriteInBlock = BLOCKSIZE - (fileINode.filePointer % BLOCKSIZE)

    # read the block @ dataBlockIndex
    b = buffer()
    readHelper(fileINode.dataBlockPtrs[dataBlockIndex], b)

    # if we will fill the block that the file pointer is in
    if overwriteInBlock < bytesToWrite:
        # build the contents of the new block
        newContents = b.contents[0:fileINode.filePointer % BLOCKSIZE] + writeBuffer.contents[valuePtr:valuePtr+overwriteInBlock]
        
        # write the new contents to the disk
        writeHelper(fileINode.dataBlockPtrs[dataBlockIndex], buffer(newContents))

        # increment the current index of the values we are writing
        valuePtr += overwriteInBlock
        bytesToWrite -= overwriteInBlock
        fileINode.filePointer += overwriteInBlock
        dataBlockIndex += 1
    
    # will not fill the block that the file pointer is in
    else:
        # build the contents of the new block
        blockPtr = fileINode.filePointer % 256
        newContents = b.contents[0:blockPtr] + writeBuffer.contents[valuePtr:valuePtr+bytesToWrite] + b.contents[blockPtr + bytesToWrite:]
        
        # write the new contents to the disk
        writeHelper(fileINode.dataBlockPtrs[dataBlockIndex], buffer(newContents))

        # increment the current index of the values we are writing
        bytesToWrite = 0

    # write all the blocks that will fill up a whole block
    while bytesToWrite >= BLOCKSIZE:
        writeHelper(fileINode.dataBlockPtrs[dataBlockIndex], buffer(writeBuffer.contents[valuePtr:valuePtr+BLOCKSIZE]))
        valuePtr += BLOCKSIZE
        bytesToWrite -= BLOCKSIZE
        fileINode.filePointer += BLOCKSIZE
        dataBlockIndex += 1

    if bytesToWrite > 0:
        # write the remaining bytes in values to the next data block
        readHelper(fileINode.dataBlockPtrs[dataBlockIndex], b)
        newContents = writeBuffer.contents[valuePtr:] + b.contents[bytesToWrite:]
        writeHelper(fileINode.dataBlockPtrs[dataBlockIndex], buffer(newContents))

    if fileINode.filePointer > fileINode.filesize:
        fileINode.filesize = fileINode.filePointer

    

# deletes a file and marks its blocks as free on disk. 
def tfs_delete(FD:fileDescriptor) -> int:
    
    # remove it from table 
    oldTableEntry = dynamicResourceTable.pop(FD)

    b = buffer(BLOCKSIZE)
    readHelper(cmd.rootDirINode, b)
    rootDirINode = bytesToINode(b.contents)

    # for each data block in the root directory, search for the entry that points to index FD
    for dataBlockID in rootDirINode.dataBlockPtrs:
        if dataBlockID != 0:
            readHelper(dataBlockID, b)
            for i in range(0, 256, 16):
                fileINodeIndex = int.from_bytes(b.contents[i+12:i+16], 'little')

                if fileINodeIndex == oldTableEntry.inodeBlockNum:
                    # remove the given entry from the directory
                    newBlockContents = b.contents[:i] + bytes(16) + b.contents[i+16:]
                    writeHelper(dataBlockID, buffer(newBlockContents))

                    # mark all data blocks that the inode points to as free
                    readHelper(fileINodeIndex, b)
                    fileINode = bytesToINode(b.contents)
                    for i in fileINode.dataBlockPtrs:
                        # NOTE this may be able to be optimized
                        if i != 0:
                            cmd.freeBlocks = cmd.freeBlocks[0: i] + '1' + cmd.freeBlocks[i + 1:]
                
                    # mark the file's inode as free
                    cmd.freeBlocks = cmd.freeBlocks[0: oldTableEntry.inodeBlockNum] + '1' + cmd.freeBlocks[oldTableEntry.inodeBlockNum + 1:]
                    return SuccessCodes.SUCCESS


def tfs_readByte(FD:fileDescriptor, buff:buffer) -> int:
    INode = dynamicResourceTable[FD].memINode
     
    if(INode.filePointer < INode.filesize):
        dataBlockIndex = INode.filePointer//BLOCKSIZE
        b = buffer()
        readHelper(INode.dataBlockPtrs[dataBlockIndex], b)
        buff.contents = b.contents[INode.filePointer%BLOCKSIZE]
        INode.filePointer = INode.filePointer + 1
        return SuccessCodes.SUCCESS
    else:
        return ErrorCodes.ATENDOFFILE


def tfs_seek(FD:fileDescriptor, offset:int) -> int:
    INode = dynamicResourceTable.get(FD).memINode
    checkValue = INode.filePointer + offset
    if(checkValue <= INode.filesize):
        INode.filePointer = INode.filePointer + offset
        return SuccessCodes.SUCCESS
    return ErrorCodes.ATENDOFFILE


def tfs_rename(FD:fileDescriptor, newName:str) -> int:
    b = buffer()
    readHelper(cmd.rootDirINode, b)
    rootDirINode = bytesToINode(b.contents)

    if len(newName) > 12:
        return ErrorCodes.FILERENAMEERROR
    newName = '_'*(12-len(newName)) + newName

    for dataBlockID in rootDirINode.dataBlockPtrs:
        if dataBlockID != 0:
            readHelper(dataBlockID, b)
            ##find the correct data block
            for i in range(0, 256, 16):
                fileINode = int.from_bytes(b.contents[i+12:i+16], 'little')

                if fileINode == dynamicResourceTable[FD].inodeBlockNum:
                    b.contents = b.contents[0:i] + newName.encode("utf-8") + b.contents[i+12:]
                    writeHelper(dataBlockID, b)
                    return SuccessCodes.SUCCESS
    return ErrorCodes.FILERENAMEERROR    


def tfs_readdir():
    b = buffer(BLOCKSIZE)
    readHelper(cmd.rootDirINode, b)
    rootDirINode = bytesToINode(b.contents)

    output = []

    for dataBlockID in rootDirINode.dataBlockPtrs:
        if dataBlockID != 0:
            readHelper(dataBlockID, b)
            for i in range(0, 256, 16):
                fileINode = int.from_bytes(b.contents[i+12:i+16], 'little')
                if fileINode != 0:
                    fName = b.contents[i:i+12].decode("utf-8").replace('_', '')
                    output.append(fName)
                    # print(fName)

    return output
