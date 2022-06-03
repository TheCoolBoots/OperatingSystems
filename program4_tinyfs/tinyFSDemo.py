import tinyFS as tfs
import libDisk as dsk

from headers import *

def main():
    print("Hello, world!")

if __name__ == '__main__':

    #mount test, sets the cmd ()
    tfs.tfs_mount(" ")

    print(tfs.cmd.magicNumber)
    print(tfs.cmd.freeBlocks)

    #open file 0
    fileNum = tfs.tfs_open("file0")
    print("File Num = " + fileNum)
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


