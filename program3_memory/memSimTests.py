import unittest

from memSim import *


class test_scheduler(unittest.TestCase):
    def test_backingStore(self):

        with open('tmpBackingStore', 'wb+') as f:
            f.write(b'fffeeecccdddabc')

        memSim = MemSimulator(None, 256)
        backingStore = memSim.loadBackingStore('tmpBackingStore', 5, 3)
        self.assertEqual(backingStore, [b'fff', b'eee', b'ccc', b'ddd', b'abc'])
    


if __name__ == '__main__':
    unittest.main()