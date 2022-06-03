import tinyFS as tfs
import libDisk as dsk

from headers import *
class Demo():
    def initTestDisk2Files(self, encryptionKey = None):
        tfs.fileDescriptor = int
        tfs.dynamicResourceTable = {}
        tfs.FDCounter = 0

        tfs.cmd = None
        tfs.cmdid = None

        dsk.nextDiskID = 0
        dsk.openFiles = {}
        
        superblk = superblock(BLOCKSIZE * 10)
        superblk.nextFreeBlockIndex = 9
        superblk.freeBlocks = '000000000' + '1'*1927

        rootDirINode = inode(32, 1, 0)   # owner = root, perms = 0xffff
        rootDirINode.dataBlockPtrs[0] = 2

        dataBlockBytes1 = '_______file0'.encode('utf-8') + int(3).to_bytes(4, 'little')
        dataBlockBytes2 = '_______file1'.encode('utf-8') + int(6).to_bytes(4, 'little') + bytes(256-32)
        rootDirDataBlock = dataNode(dataBlockBytes1 + dataBlockBytes2)

        file0INode = inode(512, 0)
        file0INode.dataBlockPtrs[0] = 4
        file0INode.dataBlockPtrs[1] = 5


        file0Data1List = [0] * 50 + [1] * 50 + [2] * 50 + [3] * 50 + [4] * 50 + [5] * 6
        file0Data2List = [6] * 50 + [7] * 50 + [8] * 50 + [9] * 50 + [10] * 50 + [11] * 6
        file0Data1 = bytes(file0Data1List)
        file0Data2 = bytes(file0Data2List)
        file0DataNode1 = dataNode(file0Data1)
        file0DataNode2 = dataNode(file0Data2)

        file1INode = inode(512, 0)
        file1INode.dataBlockPtrs[0] = 7
        file1INode.dataBlockPtrs[1] = 8

        file1Data1List = [1] * 50 + [2] * 50 + [3] * 50 + [4] * 50 + [5] * 50 + [6] * 6
        file1Data2List = [7] * 50 + [8] * 50 + [9] * 50 + [10] * 50 + [11] * 50 + [12] * 6
        file1DataNode1 = dataNode(file1Data1List)
        file1DataNode2 = dataNode(file1Data2List)

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

        with open('program4_tinyfs/TestFiles/tinyFSDemoFile.tfs', 'wb+') as f:
            f.write(fakeDisk2.serialize())

if __name__ == '__main__':
        d = Demo()
        d.initTestDisk2Files()
        #mount test, sets the cmd (current mounted disk)
        tfs.tfs_mount("program4_tinyfs/TestFiles/tinyFSDemoFile.tfs")

        print(tfs.cmd.nextFreeBlockIndex)
        print(tfs.cmd.freeBlocks)

        #open file 0
        fileNum = tfs.tfs_open("file0")
        print(fileNum)
        print(tfs.dynamicResourceTable[0].inodeBlockNum)
        print(tfs.dynamicResourceTable[0].memINode)
        print(tfs.dynamicResourceTable[0].memINode.dataBlockPtrs[0])

        #open file 1
        fileNum1 = tfs.tfs_open("file1")
        print("File Num1 = " + fileNum1)
        print(tfs.dynamicResourceTable[1].inodeBlockNum)
        print(tfs.dynamicResourceTable[1].memINode)
        print(tfs.dynamicResourceTable[1].memINode.dataBlockPtrs[0])

        #do whatchu need to do, example : maybe u need to xor the file contents

        #write 32 0 to file0
        writeData = buffer(bytes([0] * 512))
        tfs.tfs_write(fileNum, writeData, 32)

        b = buffer(256)
        dsk.readBlock(0, 4, b)
        print(b.contents)

        #read one byte and moving pointer 
        tfs.tfs_seek(0, 32)
        b = buffer()
        tfs.tfs_readByte(0, b)
        print(b.contents)

        #before deleting 
        print(tfs.tfs_readdir())

        #delete file1
        tfs.tfs_delete(fileNum1)
        print(tfs.cmd.freeBlocks[5:6]) # 1 means free

        #renaming file
        tfs.tfs_rename(fileNum, "rename")
        b = buffer()
        dsk.readBlock(0, 2, b)
        print(b.contents)

        #readdir with one file and rename executed
        print(tfs.tfs_readdir())

        #no cmd found
        tfs.tfs_unmount()
        print(tfs.cmd)

        #encryption


