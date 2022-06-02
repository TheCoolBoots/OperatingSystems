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
    

    def test_aaa_initTestDisk(self):
        
        returnCode = tfs.tfs_mkfs('program4_tinyfs/TestFiles/mkfsTest1.tfs', BLOCKSIZE * 5)
        # superblock + root inode + 3 data nodes

        superblk = superblock(1792)
        superblk.nextFreeBlockIndex = 6
        superblk.freeBlocks = '000000' + '1'*1930

        rootDirINode = inode(0, 1, 0)   # owner = root, perms = 0xffff
        rootDirINode.dataBlockPtrs[0] = 2
        rootDirINode.filesize = 16

        dataBlockBytes = '_______file1'.encode('utf-8') + int(3).to_bytes(4, 'little') + bytes(256-16)
        rootDirDataBlock = dataNode(dataBlockBytes)

        file0INode = inode(512, 0)
        file0INode.dataBlockPtrs[0] = 4
        file0INode.dataBlockPtrs[1] = 5

        file0Data1 = list(range(0, 256))
        file0Data2 = list(range(256, 0))

    #self.referenceDisk = fakeDisk
        


    def test_mount(self):
        retCode = tfs.tfs_mount('program4_tinyfs/TestFiles/mkfsTest1.tfs')
        self.assertEqual(retCode, SuccessCodes.SUCCESS)
        self.assertEqual(tfs.cmd, superblock(BLOCKSIZE * 5))
        self.assertEqual(tfs.cmdid, 0)
        tfs.cmd.diskSize = BLOCKSIZE * 10
        retCode = tfs.tfs_unmount()
        retCode = tfs.tfs_mount('program4_tinyfs/TestFiles/mkfsTest1.tfs')
        self.assertEqual(tfs.cmd, superblock(BLOCKSIZE * 10))
        retCode = tfs.tfs_unmount()


    def test_tfs_open(self):
        returnCode = tfs.tfs_open("file0")
        self.assertEqual(returnCode, SuccessCodes.SUCCESS)

        blockId = 3
        expectedINode = inode(512, 0)
        expectedINode.dataBlockPtrs[0] = 4
        expectedINode.dataBlockPtrs[1] = 5

        tmp = dynamicResourceTableEntry(blockId, expectedINode)
        self.assertEqual(tfs.dynamicResourceTable[0], tmp)
        self.assertEqual(tfs.FDCounter, 1)

    def test_tfs_close_no_write(self):
        openCode = tfs.tfs_open("file0")
        closeCode = tfs.tfs_close(0)
        self.assertEqual(closeCode, SuccessCodes.SUCCESS)

        expectedfile0Data1 = list(range(0, 256))
        expectedfile0Data2 = list(range(256, 0))

        self.assertEqual(expectedfile0Data1, self.referenceDisk.blocks[4])
        self.assertEqual(expectedfile0Data2, self.referenceDisk.blocks[5])
        self.assertEqual(len(dynamicResourceTableEntry.keys), 0)

    
   

if __name__ == '__main__':
    unittest.main()
