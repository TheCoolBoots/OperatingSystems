import tinyFS as tfs
import libDisk as dsk

from headers import *

class Demo():
     def initTestDisk2(self):
        tfs.fileDescriptor = int
        tfs.dynamicResourceTable = {}
        tfs.FDCounter = 0

        tfs.cmd = None
        tfs.cmdid = None

        dsk.nextDiskID = 0
        dsk.openFiles = {}
        
        superblk = superblock(BLOCKSIZE * 10)
        superblk.nextFreeBlockIndex = 9
        superblk.freeBlocks = '000000000' + '1'*(8*222 - 9)

        rootDirINode = inode(32, 1, 0)   # owner = root, perms = 0xffff
        rootDirINode.dataBlockPtrs[0] = 2

        dataBlockBytes1 = '_______file0'.encode('utf-8') + int(3).to_bytes(4, 'little')
        dataBlockBytes2 = '_______file1'.encode('utf-8') + int(6).to_bytes(4, 'little') + bytes(256-32)
        rootDirDataBlock = dataNode(dataBlockBytes1 + dataBlockBytes2)

        file0INode = inode(512, 0)
        file0INode.dataBlockPtrs[0] = 4
        file0INode.dataBlockPtrs[1] = 5

        f0d1 = [0] * 50 + [1] * 50 + [2] * 50 + [3] * 50 + [4] * 50 + [5] * 6
        f0d2 = [6] * 50 + [7] * 50 + [8] * 50 + [9] * 50 + [10] * 50 + [11] * 6
        file0Data1 = bytes(f0d1)
        file0Data2 = bytes(f0d2)
        file0DataNode1 = dataNode(file0Data1)
        file0DataNode2 = dataNode(file0Data2)

        file1INode = inode(512, 0)
        file1INode.dataBlockPtrs[0] = 7
        file1INode.dataBlockPtrs[1] = 8
        
        f1d1 = [1] * 50 + [2] * 50 + [3] * 50 + [4] * 50 + [5] * 50 + [6] * 6
        f1d2 = [7] * 50 + [8] * 50 + [9] * 50 + [10] * 50 + [11] * 50 + [12] * 6
        file1Data1 = bytes(f1d1)
        file1Data2 = bytes(f1d2)
        file1DataNode1 = dataNode(file1Data1)
        file1DataNode2 = dataNode(file1Data2)

        fakeDisk2 = disk(BLOCKSIZE * 10)
        fakeDisk2.blocks[0] = superblk
        fakeDisk2.blocks[1] = rootDirINode
        fakeDisk2.blocks[2] = rootDirDataBlock
        fakeDisk2.blocks[3] = file0INode
        fakeDisk2.blocks[4] = file0DataNode1
        fakeDisk2.blocks[5] = file0DataNode2
        fakeDisk2.blocks[6] = file1INode
        fakeDisk2.blocks[7] = file1DataNode1
        fakeDisk2.blocks[8] = file1DataNode2

        self.referenceDisk2 = fakeDisk2

        with open('DEMOWORK.tfs', 'wb+') as f:
            f.write(fakeDisk2.serialize())

if __name__ == '__main__':

    d = Demo()
    d.initTestDisk2()

    #mount test, sets the cmd ()
    tfs.tfs_mount("DEMOWORK.tfs")

    print("NEXT FREE BLOCK")
    print(tfs.cmd.nextFreeBlockIndex)
    print("FREE BLOCKS")
    print(tfs.cmd.freeBlocks)

    #open file 0
    fileNum = tfs.tfs_open("file0")
    print("FILE0 FILE DESCRIPTOR")
    print(fileNum)
    print("INODE BLOCK NUM")
    print(tfs.dynamicResourceTable[0].inodeBlockNum)
    print("INODE")
    print(tfs.dynamicResourceTable[0].memINode)
    print("DATA BLOCK PTRS")
    print(tfs.dynamicResourceTable[0].memINode.dataBlockPtrs[0])
    print(tfs.dynamicResourceTable[0].memINode.dataBlockPtrs[1])

    #open file 1
    fileNum1 = tfs.tfs_open("file1")
    print("FILE1 FILE DESCRIPTOR")
    print(fileNum1)
    print("INODE BLOCK NUM")
    print(tfs.dynamicResourceTable[1].inodeBlockNum)
    print("INODE")
    print(tfs.dynamicResourceTable[1].memINode)
    print("DATA BLOCK PTRS")
    print(tfs.dynamicResourceTable[1].memINode.dataBlockPtrs[0])
    print(tfs.dynamicResourceTable[1].memINode.dataBlockPtrs[1])

    #do whatchu need to do, example : maybe u need to xor the file contents
    #before write
    b = buffer(256)
    dsk.readBlock(0, 4, b)
    print("CONTENTS BEFORE BEING WRITTEN TO")
    print(b.contents)

    #write 100 0 to file0
    writeData = buffer(bytes([0] * 512))
    tfs.tfs_write(fileNum, writeData, 100)

    print("CONTENTS AFTER BEING WRITTEN TO")
    b = buffer(256)
    dsk.readBlock(0, 4, b)
    print(b.contents)

    #read one byte and moving pointer 
    tfs.tfs_seek(0, 101)
    b = buffer()
    tfs.tfs_readByte(0, b)
    print("READING ONE BYTE")
    print(b.contents)

    #before deleting 
    print("BEFORE DELETING")
    print(tfs.tfs_readdir())

    #delete file1
    tfs.tfs_delete(fileNum1)
    print("FREE BLOCK CONTENTS")
    print(tfs.cmd.freeBlocks[0:16]) # 1 means free

    #renaming file

    tfs.tfs_rename(fileNum, "rename")

    #readdir with one file and rename executed
    print("AFTER DELETING AND RENAMING")
    print(tfs.tfs_readdir())

    #no cmd found
    print("UNMOUNT")
    tfs.tfs_unmount()
    print(tfs.cmd)

    #encryption