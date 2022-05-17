import unittest

from program3_memory.memSim import MemSimulator


class test_scheduler(unittest.TestCase):
    def test_backingStore(self):
        memSim = MemSimulator(None, 256)
        backingStore = memSim.loadBackingStore('backingStoreTest')

if __name__ == '__main__':
    unittest.main()