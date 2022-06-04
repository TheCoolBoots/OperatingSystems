from enum import Enum
from math import ceil
from Crypto.Random import get_random_bytes

from encrypt import *

class buffer():
    def __init__(self, contents:bytes = bytes(256)):
        self.contents = contents

class SuccessCodes(Enum):
    SUCCESS = 0

class ErrorCodes(Enum):
    DISKNOTFOUND = -1
    BLOCKSIZE = -2
    DISKID = -3
    INVALIDBLOCKNUM = -4
    DISKMOUNT = -5
    IOERROR = -6
    ATENDOFFILE = -7
    FILERENAMEERROR = -8
    FILENOTFOUND = -9

BLOCKSIZE = 256


class disk():   # using the log file system
    def __init__(self, diskSizeBytes = 10240, encryptionKey = None):
        if diskSizeBytes % BLOCKSIZE != 0:
            raise ValueError(f"diskSizeBytes must be divisible by BLOCKSIZE({BLOCKSIZE})")
        self.diskSizeBytes = diskSizeBytes
        self.maxNumBlocks = ceil(diskSizeBytes/BLOCKSIZE)
        self.blocks:list[block] = [freeNode()] * self.maxNumBlocks

        if encryptionKey == None:
            self.blocks[0] = superblock(diskSizeBytes)
            self.blocks[1] = inode(0, 1)               # inode of root directory
            self.blocks[2] = dataNode(bytes(256))   # data of root directory
        else:
            ivNodeIV = get_random_bytes(AES.block_size)
            self.blocks[0] = superblock(diskSizeBytes, 3, ivNodeIV)
            dirIV = get_random_bytes(AES.block_size)
            self.blocks[1] = inode(0, 1)
            dirDataIV = get_random_bytes(AES.block_size)
            self.blocks[2] = dataNode(bytes(256))
            self.blocks[3] = dataNode(dirIV + dirDataIV + ivNodeIV + bytes(256 - AES.block_size * 3))

    def serialize(self) -> bytes:
        output = bytes()
        for block in self.blocks:

            output += block.toBytes()

        return output


class block():
    def toBytes(self) -> bytes:
        pass


class superblock(block):
    def __init__(self, diskSize:int, IVNode:int = None, IVNodeIV:bytes = None):
        self.magicNumber = 0x5A         # 2 bytes; 16 bits
        self.nextFreeBlockIndex = 3     # 4 bytes
        self.rootDirINode = 1           # 4 bytes
        self.diskSize = diskSize        # 4 bytes
        self.IVNode = IVNode            # 4 bytes
        self.IVNodeIV = IVNodeIV        # 16 bytes
        # TODO change to array of 1's and 0's to be more efficient
        if IVNode == None:
            self.freeBlocks = '000' + ('1' * (222 * 8 - 3)) # 0 is not free, 1 is free 
        else:
            self.freeBlocks = '0000' + ('1' * (222 * 8 - 4))

        # 256 - 34 bytes free for free block tracking
        # = 222 bytes = 1776 bits

    def toBytes(self) -> bytes:
        output = self.magicNumber.to_bytes(2, 'little')
        output += self.nextFreeBlockIndex.to_bytes(4, 'little')
        output += self.rootDirINode.to_bytes(4, 'little')
        output += self.diskSize.to_bytes(4, 'little')
        if self.IVNode != None:
            output += self.IVNode.to_bytes(4, 'little')
            output += self.IVNodeIV
        else:
            output += bytes(20)
        output += int(self.freeBlocks, 2).to_bytes(len(self.freeBlocks)//8,'big')
        return output

    def getNextFreeBlockIndex(self):
        found = False

        # save the next free block index because it will be modified below
        returnIndex = self.nextFreeBlockIndex

        while not found:
            self.nextFreeBlockIndex += 1

            # if we reach the end of the file system's available blocks,
            # wrap around back to the first block
            if self.nextFreeBlockIndex >= self.diskSize//256:
                self.nextFreeBlockIndex = 0

            # if the free block bitmap shows the block is free, break out of the loop
            if self.freeBlocks[self.nextFreeBlockIndex] == '1':
                found = True

        # update the freeblocks bitmap
        self.freeBlocks = self.freeBlocks[:returnIndex] + '0' + self.freeBlocks[returnIndex + 1:]
        return returnIndex

    def __eq__(self, other):
        if type(other) != superblock:
            return False
        # print(len(self.freeBlocks), len(other.freeBlocks))
        return self.magicNumber == other.magicNumber and self.nextFreeBlockIndex == other.nextFreeBlockIndex and self.diskSize == other.diskSize and self.freeBlocks == other.freeBlocks
            


def bytesToSuperblock(block:bytes):
        superblk = superblock(0)
        superblk.magicNumber = int.from_bytes(block[0:2], 'little')
        superblk.nextFreeBlockIndex = int.from_bytes(block[2:6], 'little')
        superblk.rootDirINode = int.from_bytes(block[6:10], 'little')
        superblk.diskSize = int.from_bytes(block[10:14], 'little')
        superblk.IVNode = int.from_bytes(block[14:18], 'little')
        superblk.IVNodeIV = block[18:34]
        if superblk.IVNode == 0:
            superblk.IVNode = None
            superblk.IVNodeIV = None
        superblk.freeBlocks = format(int.from_bytes(block[34:], 'big'), 'b')
        superblk.freeBlocks = '0'*((222 * 8) - len(superblk.freeBlocks)) + superblk.freeBlocks
        return superblk


class inode(block):
    def __init__(self, filesize:int, filetype:int, filePointer = 0, permissions:int = 0xffff, owner:str = 'root'):
        self.filesize = filesize        # 4 byte integer
        self.filetype = filetype        # 2 byte int; 0 = regular, 1 = directory
        self.permissions = permissions  # 2 byte integer
        # self.owner = owner              # 8 byte string
        self.owner = '_'*(8-len(owner)) + owner
        self.filePointer = filePointer  # 4 byte integer
        
        # 256 - 20 = 236 bytes left for data block pointers
        # 236/4 = 59 ; 59 4 byte integer pointers
        # max file size = 59 * 256 bytes = 15104 bytes or 15KB
        self.dataBlockPtrs = [0] * 59 

    def toBytes(self) -> bytes:
        output = self.filesize.to_bytes(4, 'little')
        output += self.filetype.to_bytes(2, 'little')
        output += self.permissions.to_bytes(2, 'little')
        output += bytes(self.owner, 'utf-8')
        output += self.filePointer.to_bytes(4, 'little')

        for ptr in self.dataBlockPtrs:
            output += ptr.to_bytes(4, 'little')
        

        return output

    def __eq__(self, other):
        if type(other) != inode:
            return False
        return self.dataBlockPtrs == other.dataBlockPtrs and self.filesize == other.filesize and self.filetype == other.filetype


def bytesToINode(block:bytes):
        # print(block[0:4])
        filesize = int.from_bytes(block[0:4], 'little')
        filetype = int.from_bytes(block[4:6], 'little')
        permissions = int.from_bytes(block[6:8], 'little')
        owner = block[8:16].decode('utf-8')
        # print(owner)
        filePointer = int.from_bytes(block[16:20], 'little')
        node = inode(filesize, filetype, filePointer, permissions, owner)
        for i in range(20, 256, 4):
            node.dataBlockPtrs[(i-20)//4] = int.from_bytes(block[i:i+4], 'little')
        return node


class dataNode(block):
    def __init__(self, content:bytes):
        self.content = content    
    def __eq__(self, other):
        if self.content == other.content:
            return True
        else:
            return False 

    # Directory data block structure:
    """
    4 bytes for first 4 characters of name
    4 bytes for middle 4 characters of name
    4 bytes for last 4 characters of name
    inode # for given name  
    """

    def toBytes(self) -> bytes:
        return self.content


class freeNode(block):
    def __init__(self):
        self.content = bytes([0] * BLOCKSIZE)
    def toBytes(self) -> bytes:
        return self.content


class dynamicResourceTableEntry:  #file descriptor and inode indexes
    def __init__(self, inodeBlockNum:int, memINode:inode):
        self.inodeBlockNum = inodeBlockNum
        self.memINode = memINode
    
    def __eq__(self, other):
        if type(other) != dynamicResourceTableEntry:
            return False
        return self.inodeBlockNum == other.inodeBlockNum and self.memINode == other.memINode

        
