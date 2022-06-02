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
    


    def test_initTestDisk(self):
        
        returnCode = tfs.tfs_mkfs('program4_tinyfs/TestFiles/mkfsTest1.tfs', BLOCKSIZE * 5)
        # superblock + root inode + 3 data nodes

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
        returnVal = tfs.tfs_open("file0")
        self.assertEqual(returnVal, SuccessCodes.SUCCESS)
        self.assertEqual(tfs.dynamicResourceTable[0], dynamicResourceTableEntry(0,  ))
        self.assertEqual(tfs.FDCounter, 1)


        



        self.assertEqual(tfs.tfs_open(" "), )
       


    # def test_tfs_close_IsOpen(self):
    #     returnVal = tfs.tfs_open(" ")
    #     self.assertEqual(tfs.tfs_close(" "), 1)

    # def test_tfs_delete_FirstEntry(self):
    #     returnVal = tfs.tfs_open(" ")
    #     self.assertEqual(tfs.tfs_delete(0), 1)
    
    # def test_tfs_delete_NotFirstEntry(self):
    #     returnVal0 = tfs.tfs_open(" ")
    #     returnVal1 = tfs.tfs_open(" ")
    #     returnVal2 = tfs.tfs_open(" ")
    #     self.assertEqual(tfs.tfs_delete(2), 1)
    
    # def test_tfs_readByte_FirstEntry(self):
    #     returnVal = tfs.tfs_open(" ")
    #     b = buffer()
    #     returnVal = tfs.tfs_readByte(0, b)
    #     self.assertEqual(returnVal, 1)
    #     self.assertEqual(b, " ")

    # def test_tfs_readByte_NotFirstEntry(self):
    #     returnVal0 = tfs.tfs_open(" ")
    #     returnVal1 = tfs.tfs_open(" ")
    #     returnVal2 = tfs.tfs_open(" ")
    #     b = buffer()
    #     returnVal = tfs.tfs_readByte(2, b)
    #     self.assertEqual(returnVal, 1)
    #     self.assertEqual(b, " ")


    # def test_tfs_seek_inBounds(self):
    #     returnVal0 = tfs.tfs_open(" ")
    #     self.assertEqual(tfs.tfs_seek(0, 5), 1)
    
    # def test_tfs_seek_outOfBounds(self):
    #     returnVal = tfs.tfs_open(" ")
    #     self.assertEqual(tfs.tfs_seek(0, ), -7) #figure out a value that would make it not move pointer 

    # def test_tfs_rename_IsOpen(self):
    #     returnVal = tfs.tfs_open(" ")
    #     self.assertEqual(tfs.tfs_rename(0, "NEWNAMETEST"), 1) 
    
    # def test_tfs_rename_IsNotOpen(self): 
    #     self.assertEqual(tfs.tfs_rename(0, "NEWNAMETEST"), 0) 
        

if __name__ == '__main__':
    unittest.main()
