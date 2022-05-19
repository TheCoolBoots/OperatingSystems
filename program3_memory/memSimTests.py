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


    def test_fifo1(self):

        memSim = MemSimulator("FIFO", 10, "BACKING_STORE.bin", 'fifo1.txt')
        actual = memSim.runMemSim(True)

        expected = ['Number of Translated Addresses = 10', 
                    'Page Faults = 10', 
                    'Page Fault Rate = 1.000', 
                    'TLB Hits = 0', 
                    'TLB Misses = 10',
                    'TLB Hit Rate = 0.000']

        # print(expected)

        self.assertEqual(actual, expected)

    
    def test_fifo2(self):

        memSim = MemSimulator("FIFO", 5, "BACKING_STORE.bin", 'fifo2.txt')
        output = memSim.runMemSim(True)

        expected = ['Number of Translated Addresses = 10', 
                    'Page Faults = 10', 
                    'Page Fault Rate = 1.000', 
                    'TLB Hits = 0', 
                    'TLB Misses = 10',
                    'TLB Hit Rate = 0.000']

        self.assertEqual(output, expected)
       
    def test_fifo3(self):

        memSim = MemSimulator("FIFO", 5, "BACKING_STORE.bin", 'fifo3.txt')
        output = memSim.runMemSim(True)

        expected = ['Number of Translated Addresses = 10', 
                    'Page Faults = 5', 
                    'Page Fault Rate = 0.500', 
                    'TLB Hits = 5', 
                    'TLB Misses = 5',
                    'TLB Hit Rate = 0.500']

        self.assertEqual(output, expected)


    def test_fifo4(self):

        memSim = MemSimulator("FIFO", 5, "BACKING_STORE.bin", 'fifo4.txt')
        output = memSim.runMemSim(True)

        expected = ['Number of Translated Addresses = 10', 
                    'Page Faults = 8', 
                    'Page Fault Rate = 0.800', 
                    'TLB Hits = 2', 
                    'TLB Misses = 8',
                    'TLB Hit Rate = 0.200']

        self.assertEqual(output, expected)
   
    # def test_fifo5(self):

    #     memSim = MemSimulator("FIFO", 8, "BACKING_STORE.bin", 'fifo5.txt')
    #     output = memSim.runMemSim(True)

    #     expected = ['Number of Translated Addresses = 14', 
    #                 'Page Faults = 11', 
    #                 'Page Fault Rate = 1.000', 
    #                 'TLB Hits = 1', 
    #                 'TLB Misses = 13',
    #                 'TLB Hit Rate = 0.077']

    #     self.assertEqual(output, expected)


if __name__ == '__main__':
    unittest.main()