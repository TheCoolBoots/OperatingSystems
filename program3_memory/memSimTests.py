import unittest

from memSim import *


class test_scheduler(unittest.TestCase):


    # def test_backingStore(self):

    #     with open('tmpBackingStore', 'wb+') as f:
    #         f.write(b'fffeeecccdddabc')

    #     memSim = MemSimulator(None, 256)
    #     backingStore = memSim.loadBackingStore('tmpBackingStore', 5, 3)
    #     self.assertEqual(backingStore, [b'fff', b'eee', b'ccc', b'ddd', b'abc'])


    # def test_getPageTableNum(self):

    #     memSim = MemSimulator(None, 256) # 256 = 2^8

    #     self.assertEqual(memSim.getPageTableNum(int('1111111111', 2)), 3)
    #     self.assertEqual(memSim.getOffsetBits(int('11100000101', 2)), 5)


    # def test_fifo1(self):

    #     memSim = MemSimulator("FIFO", 10, "BACKING_STORE.bin", 'fifo1.txt')
    #     actual = memSim.runMemSim(True)

    #     expected = ['Number of Translated Addresses = 10', 
    #                 'Page Faults = 10', 
    #                 'Page Fault Rate = 1.000', 
    #                 'TLB Hits = 0', 
    #                 'TLB Misses = 10',
    #                 'TLB Hit Rate = 0.000']

    #     # print(expected)

    #     self.assertEqual(actual, expected)

    
    # def test_fifo2(self):

    #     memSim = MemSimulator("FIFO", 5, "BACKING_STORE.bin", 'fifo2.txt')
    #     output = memSim.runMemSim(True)

    #     expected = ['Number of Translated Addresses = 10', 
    #                 'Page Faults = 10', 
    #                 'Page Fault Rate = 1.000', 
    #                 'TLB Hits = 0', 
    #                 'TLB Misses = 10',
    #                 'TLB Hit Rate = 0.000']

    #     self.assertEqual(output, expected)
       
    # def test_fifo3(self):

    #     memSim = MemSimulator("FIFO", 5, "BACKING_STORE.bin", 'fifo3.txt')
    #     output = memSim.runMemSim(True)

    #     expected = ['Number of Translated Addresses = 10', 
    #                 'Page Faults = 5', 
    #                 'Page Fault Rate = 0.500', 
    #                 'TLB Hits = 5', 
    #                 'TLB Misses = 5',
    #                 'TLB Hit Rate = 0.500']

    #     self.assertEqual(output, expected)


    # def test_fifo4(self):

    #     memSim = MemSimulator("FIFO", 5, "BACKING_STORE.bin", 'fifo4.txt')
    #     output = memSim.runMemSim(True)

    #     expected = ['Number of Translated Addresses = 10', 
    #                 'Page Faults = 8', 
    #                 'Page Fault Rate = 0.800', 
    #                 'TLB Hits = 2', 
    #                 'TLB Misses = 8',
    #                 'TLB Hit Rate = 0.200']

    #     self.assertEqual(output, expected)
   
    # def test_fifo5(self):

    #     memSim = MemSimulator("FIFO", 8, "BACKING_STORE.bin", 'fifo5.txt', 5)
    #     actual = memSim.runMemSim(True)

    #     expected = ['Number of Translated Addresses = 14', 
    #                 'Page Faults = 11', 
    #                 'Page Fault Rate = 0.786', 
    #                 'TLB Hits = 1', 
    #                 'TLB Misses = 13',
    #                 'TLB Hit Rate = 0.071']

    #     self.assertEqual(actual, expected)

    # def test_lru1(self):

    #     memSim = MemSimulator("LRU", 5, "BACKING_STORE.bin", 'lru1.txt')
    #     actual = memSim.runMemSim(True)

    #     expected = ['Number of Translated Addresses = 10', 
    #                 'Page Faults = 10', 
    #                 'Page Fault Rate = 1.000', 
    #                 'TLB Hits = 0', 
    #                 'TLB Misses = 10',
    #                 'TLB Hit Rate = 0.000']


    #     self.assertEqual(actual, expected)

    # def test_lru2(self):

    #     memSim = MemSimulator("LRU", 5, "BACKING_STORE.bin", 'lru2.txt')
    #     actual = memSim.runMemSim(True)

    #     expected = ['Number of Translated Addresses = 10', 
    #                 'Page Faults = 8', 
    #                 'Page Fault Rate = 0.800', 
    #                 'TLB Hits = 2', 
    #                 'TLB Misses = 8',
    #                 'TLB Hit Rate = 0.200']


    #     self.assertEqual(actual, expected)


    # def test_lru3(self):

    #     memSim = MemSimulator("LRU", 3, "BACKING_STORE.bin", 'lru3.txt')
    #     actual = memSim.runMemSim(True)

    #     expected = ['Number of Translated Addresses = 10', 
    #                 'Page Faults = 7', 
    #                 'Page Fault Rate = 0.700', 
    #                 'TLB Hits = 3', 
    #                 'TLB Misses = 7',
    #                 'TLB Hit Rate = 0.300']

    #     self.assertEqual(actual, expected)

    

    # def test_opt1(self):

    #     memSim = MemSimulator("OPT", 5, "BACKING_STORE.bin", 'opt1.txt')
    #     actual = memSim.runMemSim(True)


    #     expected = ['Number of Translated Addresses = 10', 
    #                 'Page Faults = 10', 
    #                 'Page Fault Rate = 1.000', 
    #                 'TLB Hits = 0', 
    #                 'TLB Misses = 10',
    #                 'TLB Hit Rate = 0.000']


    #     self.assertEqual(actual, expected)

    
    # def test_opt2(self):

    #     memSim = MemSimulator("OPT", 5, "BACKING_STORE.bin", 'opt2.txt')
    #     actual = memSim.runMemSim(True)
    #     #10 requests, 9 faults, 9 misses, 1 hits

    #     expected = ['Number of Translated Addresses = 10', 
    #                 'Page Faults = 9', 
    #                 'Page Fault Rate = 0.900', 
    #                 'TLB Hits = 1', 
    #                 'TLB Misses = 9',
    #                 'TLB Hit Rate = 0.100']


    #     self.assertEqual(actual, expected)

    # def test_opt3(self):
    #     memSim = MemSimulator("OPT", 3, "BACKING_STORE.bin", 'opt3.txt')
    #     actual = memSim.runMemSim(True)

    #     expected = ['Number of Translated Addresses = 20', 
    #                 'Page Faults = 9', 
    #                 'Page Fault Rate = 0.450', 
    #                 'TLB Hits = 11', 
    #                 'TLB Misses = 9',
    #                 'TLB Hit Rate = 0.550']


    #     self.assertEqual(actual, expected)

    def test_fullTest(self):
        memSim = MemSimulator("FIFO", 256, "BACKING_STORE.bin", 'outputTst')
        actual = memSim.runMemSim(False)
        expected = ['16916, 0, 0, 000010800000108100001082000010830000108400001085000010860000108700001088000010890000108a0000108b0000108c0000108d0000108e0000108f000010900000109100001092000010930000109400001095000010960000109700001098000010990000109a0000109b0000109c0000109d0000109e0000109f000010a0000010a1000010a2000010a3000010a4000010a5000010a6000010a7000010a8000010a9000010aa000010ab000010ac000010ad000010ae000010af000010b0000010b1000010b2000010b3000010b4000010b5000010b6000010b7000010b8000010b9000010ba000010bb000010bc000010bd000010be000010bf\n', '62493, 0, 1, 00003d0000003d0100003d0200003d0300003d0400003d0500003d0600003d0700003d0800003d0900003d0a00003d0b00003d0c00003d0d00003d0e00003d0f00003d1000003d1100003d1200003d1300003d1400003d1500003d1600003d1700003d1800003d1900003d1a00003d1b00003d1c00003d1d00003d1e00003d1f00003d2000003d2100003d2200003d2300003d2400003d2500003d2600003d2700003d2800003d2900003d2a00003d2b00003d2c00003d2d00003d2e00003d2f00003d3000003d3100003d3200003d3300003d3400003d3500003d3600003d3700003d3800003d3900003d3a00003d3b00003d3c00003d3d00003d3e00003d3f\n', '30198, 29, 2, 00001d4000001d4100001d4200001d4300001d4400001d4500001d4600001d4700001d4800001d4900001d4a00001d4b00001d4c00001d4d00001d4e00001d4f00001d5000001d5100001d5200001d5300001d5400001d5500001d5600001d5700001d5800001d5900001d5a00001d5b00001d5c00001d5d00001d5e00001d5f00001d6000001d6100001d6200001d6300001d6400001d6500001d6600001d6700001d6800001d6900001d6a00001d6b00001d6c00001d6d00001d6e00001d6f00001d7000001d7100001d7200001d7300001d7400001d7500001d7600001d7700001d7800001d7900001d7a00001d7b00001d7c00001d7d00001d7e00001d7f\n', '53683, 108, 3, 000034400000344100003442000034430000344400003445000034460000344700003448000034490000344a0000344b0000344c0000344d0000344e0000344f000034500000345100003452000034530000345400003455000034560000345700003458000034590000345a0000345b0000345c0000345d0000345e0000345f000034600000346100003462000034630000346400003465000034660000346700003468000034690000346a0000346b0000346c0000346d0000346e0000346f000034700000347100003472000034730000347400003475000034760000347700003478000034790000347a0000347b0000347c0000347d0000347e0000347f\n', '40185, 0, 4, 000027000000270100002702000027030000270400002705000027060000270700002708000027090000270a0000270b0000270c0000270d0000270e0000270f000027100000271100002712000027130000271400002715000027160000271700002718000027190000271a0000271b0000271c0000271d0000271e0000271f000027200000272100002722000027230000272400002725000027260000272700002728000027290000272a0000272b0000272c0000272d0000272e0000272f000027300000273100002732000027330000273400002735000027360000273700002738000027390000273a0000273b0000273c0000273d0000273e0000273f\n', '28781, 0, 5, 00001c0000001c0100001c0200001c0300001c0400001c0500001c0600001c0700001c0800001c0900001c0a00001c0b00001c0c00001c0d00001c0e00001c0f00001c1000001c1100001c1200001c1300001c1400001c1500001c1600001c1700001c1800001c1900001c1a00001c1b00001c1c00001c1d00001c1e00001c1f00001c2000001c2100001c2200001c2300001c2400001c2500001c2600001c2700001c2800001c2900001c2a00001c2b00001c2c00001c2d00001c2e00001c2f00001c3000001c3100001c3200001c3300001c3400001c3500001c3600001c3700001c3800001c3900001c3a00001c3b00001c3c00001c3d00001c3e00001c3f\n', '24462, 23, 6, 000017c0000017c1000017c2000017c3000017c4000017c5000017c6000017c7000017c8000017c9000017ca000017cb000017cc000017cd000017ce000017cf000017d0000017d1000017d2000017d3000017d4000017d5000017d6000017d7000017d8000017d9000017da000017db000017dc000017dd000017de000017df000017e0000017e1000017e2000017e3000017e4000017e5000017e6000017e7000017e8000017e9000017ea000017eb000017ec000017ed000017ee000017ef000017f0000017f1000017f2000017f3000017f4000017f5000017f6000017f7000017f8000017f9000017fa000017fb000017fc000017fd000017fe000017ff\n', '48399, 67, 7, 00002f4000002f4100002f4200002f4300002f4400002f4500002f4600002f4700002f4800002f4900002f4a00002f4b00002f4c00002f4d00002f4e00002f4f00002f5000002f5100002f5200002f5300002f5400002f5500002f5600002f5700002f5800002f5900002f5a00002f5b00002f5c00002f5d00002f5e00002f5f00002f6000002f6100002f6200002f6300002f6400002f6500002f6600002f6700002f6800002f6900002f6a00002f6b00002f6c00002f6d00002f6e00002f6f00002f7000002f7100002f7200002f7300002f7400002f7500002f7600002f7700002f7800002f7900002f7a00002f7b00002f7c00002f7d00002f7e00002f7f\n', '64815, 75, 8, 00003f4000003f4100003f4200003f4300003f4400003f4500003f4600003f4700003f4800003f4900003f4a00003f4b00003f4c00003f4d00003f4e00003f4f00003f5000003f5100003f5200003f5300003f5400003f5500003f5600003f5700003f5800003f5900003f5a00003f5b00003f5c00003f5d00003f5e00003f5f00003f6000003f6100003f6200003f6300003f6400003f6500003f6600003f6700003f6800003f6900003f6a00003f6b00003f6c00003f6d00003f6e00003f6f00003f7000003f7100003f7200003f7300003f7400003f7500003f7600003f7700003f7800003f7900003f7a00003f7b00003f7c00003f7d00003f7e00003f7f\n', '18295, -35, 9, 000011c0000011c1000011c2000011c3000011c4000011c5000011c6000011c7000011c8000011c9000011ca000011cb000011cc000011cd000011ce000011cf000011d0000011d1000011d2000011d3000011d4000011d5000011d6000011d7000011d8000011d9000011da000011db000011dc000011dd000011de000011df000011e0000011e1000011e2000011e3000011e4000011e5000011e6000011e7000011e8000011e9000011ea000011eb000011ec000011ed000011ee000011ef000011f0000011f1000011f2000011f3000011f4000011f5000011f6000011f7000011f8000011f9000011fa000011fb000011fc000011fd000011fe000011ff\n', 'Number of Translated Addresses = 10', 'Page Faults = 10', 'Page Fault Rate = 1.000', 'TLB Hits = 0', 'TLB Misses = 10', 'TLB Hit Rate = 0.000']

        self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()