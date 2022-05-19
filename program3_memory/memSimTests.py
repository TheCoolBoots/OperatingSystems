import unittest

from memSim import *


class test_scheduler(unittest.TestCase):


    def test_backingStore(self):

        with open('tmpBackingStore', 'wb+') as f:
            f.write(b'fffeeecccdddabc')

        memSim = MemSimulator(None, 256)
        backingStore = memSim.loadBackingStore('tmpBackingStore', 5, 3)
        self.assertEqual(backingStore, [b'fff', b'eee', b'ccc', b'ddd', b'abc'])


    def test_getPageTableNum(self):

        memSim = MemSimulator(None, 256) # 256 = 2^8

        self.assertEqual(memSim.getPageTableNum(int('1111111111', 2)), 3)
        self.assertEqual(memSim.getOffsetBits(int('11100000101', 2)), 5)

    
    def test_fifo5():
        memSim = MemSimulator("FIFO", 5, "BACKING_STORE.bin", 'fifo5.txt')



if __name__ == '__main__':
    unittest.main()