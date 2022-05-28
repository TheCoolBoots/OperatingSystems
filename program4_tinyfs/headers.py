from enum import Enum

class buffer():
    def __init__(self, contents:bytes):
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

BLOCKSIZE = 256


def bytesToINode(block:bytes):
        filesize = int.from_bytes(block[0:4], 'little')
        filetype = int.from_bytes(block[4:6], 'little')
        permissions = int.from_bytes(block[6:8], 'little')
        owner = block[8:16].decode('utf-8')
        filePointer = int.from_bytes(block[16:20], 'little')
        return inode(filesize, filetype, permissions, owner, filePointer)


def bytesToSuperblock(block:bytes):
        superblk = superblock(0)
        superblk.magicNumber = int.from_bytes(block[0:2], 'little')
        superblk.nextFreeBlockIndex = int.from_bytes(block[2:6], 'little')
        superblk.rootDirINode = int.from_bytes(block[6:10], 'little')
        superblk.diskSize = int.from_bytes(block[10:14], 'little')
        return superblk


class disk():   # using the log file system
    def __init__(self, diskSizeBytes = 10240):
        if diskSizeBytes % BLOCKSIZE != 0:
            raise ValueError(f"diskSizeBytes must be divisible by BLOCKSIZE({BLOCKSIZE})")
        self.diskSizeBytes = diskSizeBytes
        self.maxNumBlocks = diskSizeBytes/BLOCKSIZE
        self.blocks:list[block] = [freeNode()] * self.maxNumBlocks

        self.blocks[0] = superblock(diskSizeBytes)
        self.blocks[1] = inode(0)               # inode of root directory
        self.blocks[2] = dataNode(bytes(256))   # data of root directory

    def serialize(self) -> bytes:
        output = bytes()
        for block in self.blocks:
            output += block.toBytes()


class block():
    def toBytes(self) -> bytes:
        pass


class superblock(block):
    def __init__(self, diskSize:int):
        self.magicNumber = 0x5A         # 2 bytes
        self.nextFreeBlockIndex = 3     # 4 bytes
        self.rootDirINode = 1           # 4 bytes
        self.diskSize = diskSize        # 4 bytes
    def toBytes(self) -> bytes:
        output = self.magicNumber.to_bytes(2, 'little', False)
        output += self.nextFreeBlockIndex.to_bytes(4, 'little', False)
        output += self.rootDirINode.to_bytes(4, 'little', False)
        output += self.diskSize.to_bytes(4, 'little', False)
        output += bytes(256-14)


class inode(block):
    def __init__(self, filesize:int, filetype:int, permissions:int = 0xffff, owner:str = 'root', filePointer = 0):
        self.filesize = filesize        # 4 byte integer
        self.filetype = filetype        # 2 byte int; 0 = regular, 1 = directory
        self.permissions = permissions  # 2 byte integer
        self.owner = owner              # 8 byte string
        self.filePointer = filePointer  # 4 byte integer
        
        # 256 - 20 = 236 bytes left for data block pointers
        # max file size = 59 * 256 bytes = 15104 bytes or 15KB
        self.dataBlockPtrs = [0] * 59

    def toBytes(self) -> bytes:
        output = self.filesize.to_bytes(4, 'little', False)
        output += self.filetype.to_bytes(2, 'little', False)
        output += self.permissions.to_bytes(2, 'little', False)
        output += bytes(self.owner, 'utf-8')
        output += self.filePointer.to_bytes(4, 'little', False)

        for ptr in self.dataBlockPtrs:
            output += ptr.to_bytes(4, 'little', False)


class dataNode(block):
    def __init__(self, content:bytes):
        self.content = content    

    # Directory data block structure:
    """
    4 bytes for first 4 characters of name
    4 bytes for last 4 characters of name
    inode # for given name  
    """

    def toBytes(self) -> bytes:
        return self.content


class freeNode(block):
    def __init__(self):
        self.content = bytes(256)
    def toBytes(self) -> bytes:
        pass
