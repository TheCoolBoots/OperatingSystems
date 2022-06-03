from typing import Dict
import unittest
import tinyFS as tfs
import libDisk as dsk

from headers import *


class test_scheduler(unittest.TestCase):
    def test_bytesToInode(self):
        nodeExpected = inode(4,1,13)
        nodeExpected.dataBlockPtrs = list(range(59))
        nodeBytesExpected = nodeExpected.toBytes()
        # print(nodeBytesExpected)

        nodeActual = bytesToINode(nodeBytesExpected)

        self.assertEqual(nodeActual.filesize, 4)
        self.assertEqual(nodeActual.filetype, 1)
        self.assertEqual(nodeActual.filePointer, 13)
        self.assertEqual(nodeActual.permissions, 0xffff)
        self.assertEqual(nodeActual.owner, '____root')
        self.assertEqual(nodeActual.dataBlockPtrs, list(range(59)))

    def test_superblockToInode(self):
        nodeExpected = superblock(1991)
        nodeBytesExpected = nodeExpected.toBytes()
        # print(nodeBytesExpected)

        nodeActual = bytesToSuperblock(nodeBytesExpected)

        self.assertEqual(nodeActual.magicNumber, 0x5A)
        self.assertEqual(nodeActual.nextFreeBlockIndex, 3)
        self.assertEqual(nodeActual.rootDirINode, 1)
        self.assertEqual(nodeActual.diskSize, 1991)
        self.assertEqual(len(nodeActual.freeBlocks), 1936)
        self.assertEqual(int(nodeActual.freeBlocks, 2), int('000' + ('1' * 1933), 2))
    

    def initTestDisk(self):
        tfs.fileDescriptor = int
        tfs.dynamicResourceTable = {}
        tfs.FDCounter = 0

        tfs.cmd = None
        tfs.cmdid = None

        dsk.nextDiskID = 0
        dsk.openFiles = {}

        returnCode = tfs.tfs_mkfs('program4_tinyfs/TestFiles/mkfsTest1.tfs', BLOCKSIZE * 5)
        # superblock + root inode + 3 data nodes

        superblk = superblock(1792)
        superblk.nextFreeBlockIndex = 6
        superblk.freeBlocks = '000000' + '1'*1930

        rootDirINode = inode(0, 1, 0)   # owner = root, perms = 0xffff
        rootDirINode.dataBlockPtrs[0] = 2
        rootDirINode.filesize = 16

        dataBlockBytes = '_______file0'.encode('utf-8') + int(3).to_bytes(4, 'little') + bytes(256-16)
        rootDirDataBlock = dataNode(dataBlockBytes)

        file0INode = inode(512, 0)
        file0INode.dataBlockPtrs[0] = 4
        file0INode.dataBlockPtrs[1] = 5

        file0Data1 = bytes(list(range(0, 256)))
        file0Data2 = bytes(list(range(256, 0)))
        file0DataNode1 = dataNode(file0Data1)
        file0DataNode2 = dataNode(file0Data2)

        fakeDisk = disk(1792)
        fakeDisk.blocks[0] = superblk
        fakeDisk.blocks[1] = rootDirINode
        fakeDisk.blocks[2] = rootDirDataBlock
        fakeDisk.blocks[3] = file0INode
        fakeDisk.blocks[4] = file0DataNode1
        fakeDisk.blocks[5] = file0DataNode2

        self.referenceDisk = fakeDisk

        with open('program4_tinyfs/TestFiles/mkfsTest2.tfs', 'wb+') as f:
            f.write(fakeDisk.serialize())  
    
    def initTestDisk2(self):
        tfs.fileDescriptor = int
        tfs.dynamicResourceTable = {}
        tfs.FDCounter = 0

        tfs.cmd = None
        tfs.cmdid = None

        dsk.nextDiskID = 0
        dsk.openFiles = {}

        returnCode = tfs.tfs_mkfs('program4_tinyfs/TestFiles/mkfsTest3.tfs', BLOCKSIZE * 9)
        
        superblk = superblock(2304)
        superblk.nextFreeBlockIndex = 9
        superblk.freeBlocks = '000000000' + '1'*1927

        rootDirINode = inode(0, 1, 0)   # owner = root, perms = 0xffff
        rootDirINode.dataBlockPtrs[0] = 2
        rootDirINode.filesize = 32

        dataBlockBytes1 = '_______file0'.encode('utf-8') + int(3).to_bytes(4, 'little')
        dataBlockBytes2 = '_______file1'.encode('utf-8') + int(6).to_bytes(4, 'little') + bytes(256-32)
        rootDirDataBlock = dataNode(dataBlockBytes1 + dataBlockBytes2)

        file0INode = inode(512, 0)
        file0INode.dataBlockPtrs[0] = 4
        file0INode.dataBlockPtrs[1] = 5

        file0Data1 = bytes(list(range(0, 256)))
        file0Data2 = bytes(list(range(256, 0)))
        file0DataNode1 = dataNode(file0Data1)
        file0DataNode2 = dataNode(file0Data2)

        file1INode = inode(512, 0)
        file1INode.dataBlockPtrs[0] = 7
        file1INode.dataBlockPtrs[1] = 8

        file1Data1 = bytes(list(range(0, 256)))
        file1Data2 = bytes(list(range(256, 0)))
        file1DataNode1 = dataNode(file1Data1)
        file1DataNode2 = dataNode(file1Data2)


        fakeDisk2 = disk(2304)
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

        with open('program4_tinyfs/TestFiles/mkfsTest4.tfs', 'wb+') as f:
            f.write(fakeDisk2.serialize())  
        

    def test_mount_unmount_close(self):
        self.initTestDisk()

        retCode = tfs.tfs_mount('program4_tinyfs/TestFiles/mkfsTest1.tfs')
        self.assertEqual(retCode, SuccessCodes.SUCCESS)
        self.assertEqual(tfs.cmd, superblock(BLOCKSIZE * 5))
        self.assertEqual(tfs.cmdid, 0)
        tfs.cmd.diskSize = BLOCKSIZE * 10
        retCode = tfs.tfs_unmount()
        retCode = tfs.tfs_mount('program4_tinyfs/TestFiles/mkfsTest1.tfs')
        self.assertEqual(tfs.cmd, superblock(BLOCKSIZE * 10))
        retCode = tfs.tfs_unmount()


    def test_seek_readByte(self):
        self.initTestDisk()

        tfs.tfs_mount('program4_tinyfs/TestFiles/mkfsTest2.tfs')
        tfs.tfs_open('file0')
        tfs.tfs_seek(0, 8)
        b = buffer()
        tfs.tfs_readByte(0, b)
        self.assertEqual(b.contents, 8)
        seekRetCode = tfs.tfs_seek(0, 512)
        self.assertEqual(seekRetCode, ErrorCodes.ATENDOFFILE)
        tfs.tfs_unmount()


    def test_tfs_open(self):
        self.initTestDisk()

        tfs.tfs_mount('program4_tinyfs/TestFiles/mkfsTest2.tfs')
        fileNum = tfs.tfs_open("file0")
        self.assertEqual(fileNum, 0)

        blockId = 3
        expectedINode = inode(512, 0)
        expectedINode.dataBlockPtrs[0] = 4
        expectedINode.dataBlockPtrs[1] = 5

        tmp = dynamicResourceTableEntry(blockId, expectedINode)
        self.assertEqual(tfs.dynamicResourceTable[0], tmp)
        self.assertEqual(tfs.FDCounter, 1)
        tfs.tfs_unmount()


    def test_tfs_open2(self):
        self.initTestDisk2()

        tfs.tfs_mount('program4_tinyfs/TestFiles/mkfsTest4.tfs')
        fileNum = tfs.tfs_open("file0")
        fileNum2 = tfs.tfs_open("file1")

        self.assertEqual(fileNum2, 1)

        blockId = 6
        expectedINode = inode(512, 0)
        expectedINode.dataBlockPtrs[0] = 7
        expectedINode.dataBlockPtrs[1] = 8

        tmp = dynamicResourceTableEntry(blockId, expectedINode)
        #self.assertEqual(tfs.dynamicResourceTable[1], tmp)
        print(tfs.dynamicResourceTable[1].inodeBlockNum)
        print(tfs.dynamicResourceTable[1].memINode.dataBlockPtrs[0])
        print(tfs.dynamicResourceTable[1].memINode.dataBlockPtrs[1])
        self.assertEqual(tfs.FDCounter, 2)
        tfs.tfs_unmount()


    # def test_tfs_write1(self):
    #     self.initTestDisk()

    #     tfs.tfs_mount('program4_tinyfs/TestFiles/mkfsTest2.tfs')
    #     fileNum = tfs.tfs_open("file0")
    #     writeData = buffer(bytes([0] * 512))
    #     tfs.tfs_write(fileNum, writeData, 16)
        
    #     b = buffer(256)
    #     dsk.readBlock(0, 4, b)

    #     expectedfile0Data1 = bytes([0] * 16 + list(range(16, 256)))
    #     self.assertEqual(expectedfile0Data1, b.contents)
    #     tfs.tfs_unmount()
    

    def test_tfs_write2(self):
        self.initTestDisk()

        tfs.tfs_mount('program4_tinyfs/TestFiles/mkfsTest2.tfs')
        fileNum = tfs.tfs_open("file0")
        writeData = buffer(bytes([0] * 512))
        tfs.tfs_write(fileNum, writeData, 512)
        
        b = buffer(256)
        dsk.readBlock(0, 4, b)
        expectedfile0Data1 = bytes([0] * 256)
        self.assertEqual(expectedfile0Data1, b.contents)

        dsk.readBlock(0, 5, b)
        expectedfile0Data2 = bytes([0] * 256)
        self.assertEqual(expectedfile0Data2, b.contents)
        tfs.tfs_unmount()


    # def test_tfs_close_withWrite(self):
    #     openCode = tfs.tfs_open("file0")
    #     writeData = [0] * 512
    #     tfs.tfs_write(0, writeData, 512)
        
    #     closeCode = tfs.tfs_close(0)
    #     self.assertEqual(closeCode, SuccessCodes.SUCCESS)

    #     expectedfile0Data1 = [0] * 256
    #     expectedfile0Data2 = [0] * 256

    #     self.assertEqual(expectedfile0Data1, self.referenceDisk.blocks[4])
    #     self.assertEqual(expectedfile0Data2, self.referenceDisk.blocks[5])
    #     self.assertEqual(len(dynamicResourceTableEntry.keys), 0)
    
    
   


        

if __name__ == '__main__':
    unittest.main()
