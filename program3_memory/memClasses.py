

class TLBEntry():
    def __init__(self, pageNum : int, frameNum : int) -> None:
        self.pageNum = pageNum
        self.frameNum = frameNum

class TLB():
    def __init__(self) -> None:
        self.entries : list[TLBEntry] = [None] * 16 

    def inTLB(self, pageNum : int) -> bool:
        # searches for pageNum in self.entries
        if pageNum in self.entries:
            return True
        else:
            return False
        
class PageTableEntry():
    def __init__(self, frameNum : int):
        self.frameNum = frameNum
        self.valid = False
        
class PageTable():
    def __init__(self):
        self.entries : list[PageTableEntry] = [None] * (2 ** 8)

    def inPT(self, frameNum : int) -> bool:
        # searches for frameNum in self.entries
        if frameNum in self.entries:
            return True
        else:
            return False

class RAM():
    def __init__(self, frames:int):
        self.frames : list[bytes] = [None] * frames
