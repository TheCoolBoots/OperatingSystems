from enum import Enum

class buffer():
    def __init__(self):
        self.contents = bytes(BLOCKSIZE)

class SuccessCodes(Enum):
    SUCCESS = 0

class ErrorCodes(Enum):
    DISKNOTFOUND = -1
    BLOCKSIZE = -2
    DISKID = -3
    INVALIDBLOCKNUM = -4


BLOCKSIZE = 256

class diskBlock():
    def __init__(self, diskSizeBytes = 10240):
        if diskSizeBytes % BLOCKSIZE != 0:
            raise ValueError(f"diskSizeBytes must be divisible by BLOCKSIZE({BLOCKSIZE})")
        self.diskSizeBytes = diskSizeBytes
        self.maxNumBlocks = diskSizeBytes/BLOCKSIZE
        self.blocks = [None] * self.maxNumBlocks

        self.blocks[0] = superblock()
        self.blocks[1] = inode(0)
        self.blocks[2] = dataNode(bytes(256))

class superblock():
    def __init__(self):
        self.magicNumber = 0x5A
        self.nextFreeBlockIndex = 3
        self.rootDirINode = 1

class inode():
    def __init__(self, filesize, permissions = 0xffff, owner = 'root'):
        self.filesize = filesize        # 4 byte integer
        self.permissions = permissions  # 4 byte string
        self.owner = owner              # 8 byte string
        self.filePointer = 0            # 4 byte integer
        
        # 256 - 20 = 236 bytes left for data block pointers
        # max file size = 236 * 256 bytes = 60416 bytes or 60KB

class dataNode():
    def __init__(self, content:bytes):
        self.content = content    

    # Directory data block structure:
    """
    4 bytes for first 4 characters of name
    4 bytes for last 4 characters of name
    inode # for given name  
    """

