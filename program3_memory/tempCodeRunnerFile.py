    def test_lru3(self):

        memSim = MemSimulator("LRU", 3, "BACKING_STORE.bin", 'lru3.txt')
        actual = memSim.runMemSim(True)

        expected = ['Number of Translated Addresses = 10', 
                    'Page Faults = 10', 
                    'Page Fault Rate = 1.000', 
                    'TLB Hits = 0', 
                    'TLB Misses = 10',
                    'TLB Hit Rate = 0.000']



        self.assertEqual(actual, expected)