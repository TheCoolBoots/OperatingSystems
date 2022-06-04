from typing import Dict
import unittest
import tinyFS as tfs
import libDisk as dsk
from hashlib import md5

from headers import *
from encrypt import *


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
        self.assertEqual(len(nodeActual.freeBlocks), 8*222)
        self.assertEqual(int(nodeActual.freeBlocks, 2), int('000' + ('1' * (8*222 - 3)), 2))
    

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

        superblk = superblock(2048)
        superblk.nextFreeBlockIndex = 6
        superblk.freeBlocks = '000000' + '1'*(8*222 - 6)

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

        fakeDisk = disk(2048)
        fakeDisk.blocks[0] = superblk
        fakeDisk.blocks[1] = rootDirINode
        fakeDisk.blocks[2] = rootDirDataBlock
        fakeDisk.blocks[3] = file0INode
        fakeDisk.blocks[4] = file0DataNode1
        fakeDisk.blocks[5] = file0DataNode2

        self.referenceDisk = fakeDisk

        with open('program4_tinyfs/TestFiles/mkfsTest2.tfs', 'wb+') as f:
            f.write(fakeDisk.serialize())  
            # self.assertEqual(fakeDisk.serialize(), f.read())

    
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

        file0Data1 = bytes(list(range(0, 256)))
        file0Data2 = bytes(list(range(0, 256)))
        file0DataNode1 = dataNode(file0Data1)
        file0DataNode2 = dataNode(file0Data2)

        file1INode = inode(512, 0)
        file1INode.dataBlockPtrs[0] = 7
        file1INode.dataBlockPtrs[1] = 8

        file1Data1 = bytes(list(range(0, 256)))
        file1Data2 = bytes(list(range(0, 256)))
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

        with open('program4_tinyfs/TestFiles/mkfsTest3.tfs', 'wb+') as f:
            f.write(fakeDisk2.serialize())
            # self.assertEqual(fakeDisk2.serialize(), f.read())
        



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

        tfs.tfs_mount('program4_tinyfs/TestFiles/mkfsTest3.tfs')
        f1 = tfs.tfs_open("file0")
        b = buffer()
        dsk.readBlock(0, 6, b)
        dsk.readBlock(0, 7, b)
        dsk.readBlock(0, 8, b)
        f2 = tfs.tfs_open("file1")

        self.assertEqual(f1, 0)
        self.assertEqual(f2, 1)

        blockId = 6
        expectedINode = inode(512, 0)
        expectedINode.dataBlockPtrs[0] = 7
        expectedINode.dataBlockPtrs[1] = 8

        tmp = dynamicResourceTableEntry(blockId, expectedINode)
        self.assertEqual(tmp, tfs.dynamicResourceTable[f2])
        self.assertEqual(tfs.FDCounter, 2)
        tfs.tfs_unmount()


    def test_tfs_write1(self):
        self.initTestDisk()

        tfs.tfs_mount('program4_tinyfs/TestFiles/mkfsTest2.tfs')
        fileNum = tfs.tfs_open("file0")
        writeData = buffer(bytes([0] * 512))
        tfs.tfs_write(fileNum, writeData, 16)
        
        b = buffer(256)
        dsk.readBlock(0, 4, b)

        expectedfile0Data1 = bytes([0] * 16 + list(range(16, 256)))
        self.assertEqual(expectedfile0Data1, b.contents)
        tfs.tfs_unmount()
    

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

    
    def test_tfs_write3(self):
        self.initTestDisk()

        tfs.tfs_mount('program4_tinyfs/TestFiles/mkfsTest2.tfs')
        fileNum = tfs.tfs_open("file0")
        writeData = buffer(bytes([0] * 512 + list(range(0,10))))
        tfs.tfs_write(fileNum, writeData, 522)
        
        b = buffer(256)
        dsk.readBlock(0, 4, b)
        expectedfile0Data1 = bytes([0] * 256)
        self.assertEqual(expectedfile0Data1, b.contents)

        dsk.readBlock(0, 5, b)
        expectedfile0Data2 = bytes([0] * 256)
        self.assertEqual(expectedfile0Data2, b.contents)

        dsk.readBlock(0, 6, b)
        expectedfile0Data3 = bytes(list(range(0, 10))) + bytes(246)
        self.assertEqual(expectedfile0Data3, b.contents)

        blk = superblock(2048)
        blk.nextFreeBlockIndex = 7
        blk.freeBlocks = '0000000' + '1'*(8*222 - 7)
        self.assertEqual(blk, tfs.cmd)

        tfs.tfs_unmount()

    '''
    need to test rename, readdir, delete
    '''

    def test_rename(self):
        self.initTestDisk()

        tfs.tfs_mount('program4_tinyfs/TestFiles/mkfsTest2.tfs')
        fileNum = tfs.tfs_open("file0")

        tfs.tfs_rename(fileNum, "magicBoop")

        expected = '___magicBoop'.encode('utf-8') + int(3).to_bytes(4, 'little') + bytes(256-16)
        b = buffer()
        dsk.readBlock(0, 2, b)
        self.assertEqual(expected, b.contents)
        tfs.tfs_unmount()

    
    def test_delete(self):
        self.initTestDisk()

        tfs.tfs_mount('program4_tinyfs/TestFiles/mkfsTest2.tfs')
        fileNum = tfs.tfs_open("file0")

        tfs.tfs_delete(fileNum)

        self.assertEqual(tfs.cmd.freeBlocks[3:6], '111')
        # print(tfs.cmd.freeBlocks[0:15])
        expectedData = bytes(256)
        b = buffer()
        dsk.readBlock(0, 2, b)
        self.assertEqual(b.contents, expectedData)
        tfs.tfs_unmount()


    def test_readdir(self):
        self.initTestDisk2()

        tfs.tfs_mount('program4_tinyfs/TestFiles/mkfsTest3.tfs')
        actual = tfs.tfs_readdir()
        expected = ['file0', 'file1']
        self.assertEqual(actual, expected)
        tfs.tfs_unmount()

    

    def initEncryptedDisk(self, rawKey):
        tfs.fileDescriptor = int
        tfs.dynamicResourceTable = {}
        tfs.FDCounter = 0

        tfs.cmd = None
        tfs.cmdid = None

        dsk.nextDiskID = 0
        dsk.openFiles = {}

        encryptionKey = md5(rawKey.encode('utf8')).digest()

        # indices are shifted 1 down b/c no IV for superblock
        initVectors = [b'04cl}\xad\x02\x83\x03%A\x12vEC\xd9',
                    b'\x00\xb6\xb9\xbe\xd0\xbe\xbb\xdc4\x13+\x8f/\x8dI\t',
                    b'\xf8\xc2f\x1e"\xd2\xfd\xfe\t\xfaqm\xa0\x16\xc7t',
                    b'\xae\x14\x9e\x9e\xcb\xb5\xba\xfbA0\xacx2\xda&\xb1',
                    b'\xcc\x9b\xa6g\xc1[\x1cc\xb6\xaes\x91\x0c\x163=',
                    b'\xea)\ta\x8f\xb6\xceq\xe8\x1e\x0c\x10\xe9I\xb86',
                    b'W\x04\x15\x82Lun\xfc~\xcaf\x1dP<\x80\xd4',
                    b"\xde0\x1d0'\x7f\x13\x86h\r\x9a(\x1b\x9a#\x82"]

        superblk = superblock(BLOCKSIZE * 8, 3, initVectors[2])
        superblk.nextFreeBlockIndex = 7
        superblk.freeBlocks = '0000000' + '1'*(222 * 8 - 7)
        # self.assertEqual(len(superblk.toBytes()), BLOCKSIZE)
        serialized = superblk.toBytes()

        rootDirINode = inode(0, 1, 0)   # owner = root, perms = 0xffff
        rootDirINode.dataBlockPtrs[0] = 2
        rootDirINode.filesize = 16
        # t = encryptAES(rootDirINode.toBytes(), encryptionKey, initVectors[0])
        # self.assertEqual(len(t), BLOCKSIZE)
        serialized += encryptAES(rootDirINode.toBytes(), encryptionKey, initVectors[0])
        

        dataBlockBytes = '_______file0'.encode('utf-8') + int(4).to_bytes(4, 'little') + bytes(256-16)
        rootDirDataBlock = dataNode(dataBlockBytes)
        # t = encryptAES(rootDirDataBlock.toBytes(), encryptionKey, initVectors[1])
        # self.assertEqual(len(t), BLOCKSIZE)
        serialized += encryptAES(rootDirDataBlock.toBytes(), encryptionKey, initVectors[1])

        IVNodeData = initVectors[0] + initVectors[1] + initVectors[2] +initVectors[3] +initVectors[4] +initVectors[5]
        # print(IVNodeData)
        # print('\n')
        contents = IVNodeData + bytes(256-len(IVNodeData))
        t = encryptAES(contents, encryptionKey, initVectors[2])
        # print(t)
        # self.assertEqual(len(t), BLOCKSIZE)
        serialized += encryptAES(contents, encryptionKey, initVectors[2])

        file0INode = inode(512, 0)
        file0INode.dataBlockPtrs[0] = 5
        file0INode.dataBlockPtrs[1] = 6
        # t = encryptAES(file0INode.toBytes(), encryptionKey, initVectors[3])
        # self.assertEqual(len(t), BLOCKSIZE)
        serialized += encryptAES(file0INode.toBytes(), encryptionKey, initVectors[3])

        file0Data1 = bytes(list(range(0, 256)))
        file0Data2 = bytes(list(range(0, 256)))
        file0DataNode1 = dataNode(file0Data1)
        # t = encryptAES(file0DataNode1.toBytes(), encryptionKey, initVectors[4])
        # self.assertEqual(len(t), BLOCKSIZE)
        serialized += encryptAES(file0DataNode1.toBytes(), encryptionKey, initVectors[4])

        file0DataNode2 = dataNode(file0Data2)
        # t = encryptAES(file0DataNode2.toBytes(), encryptionKey, initVectors[5])
        # self.assertEqual(len(t), BLOCKSIZE)
        serialized += encryptAES(file0DataNode2.toBytes(), encryptionKey, initVectors[5])

        serialized += bytes(256)

        # print(len(serialized))

        with open('program4_tinyfs/TestFiles/encrypted2.tfs', 'wb+') as f:
            f.write(serialized)  

    # def test_mkfs_encrypted(self):
    #     tfs.tfs_mkfs('program4_tinyfs/TestFiles/encrypted.tfs', 2048, 'BeepBoop')
    #     tfs.tfs_mount('program4_tinyfs/TestFiles/encrypted.tfs')
    #     tfs.tfs_unmount()

    def test_mkfs_encrypted2(self):
        self.initEncryptedDisk('BeepBoop')
        tfs.tfs_mount('program4_tinyfs/TestFiles/encrypted2.tfs', 'BeepBoop')

        b1 = buffer()

        tfs.tfs_open('file0')
        tfs.tfs_seek(0, 20)
        tfs.tfs_readByte(0, b1)
        self.assertEqual(b1.contents, 20)
        tfs.tfs_unmount()



if __name__ == '__main__':
    unittest.main()
