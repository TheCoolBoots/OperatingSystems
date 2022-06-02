import unittest
import tinyFS
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

    def test_initTestDisk(self):
        
        returnCode = tinyFS.tfs_mkfs('program4_tinyfs/TestFiles/mkfsTest1.tfs', BLOCKSIZE * 5)
        # superblock + root inode + 3 data nodes

    def test_mount(self):
        retCode = tinyFS.tfs_mount('program4_tinyfs/TestFiles/mkfsTest1.tfs')
        self.assertEqual(retCode, SuccessCodes.SUCCESS)
        self.assertEqual(tinyFS.cmd, superblock(BLOCKSIZE * 5))
        self.assertEqual(tinyFS.cmdid, 0)
        tinyFS.cmd.diskSize = BLOCKSIZE * 10
        retCode = tinyFS.tfs_unmount()
        retCode = tinyFS.tfs_mount('program4_tinyfs/TestFiles/mkfsTest1.tfs')
        self.assertEqual(tinyFS.cmd, superblock(BLOCKSIZE * 10))
        retCode = tinyFS.tfs_unmount()


if __name__ == '__main__':
    unittest.main()
