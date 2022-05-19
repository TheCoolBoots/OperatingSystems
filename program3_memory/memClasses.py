

from telnetlib import PRAGMA_HEARTBEAT


class TLBEntry():
    def __init__(self, pageNum : int, frameNum : int) -> None:
        self.pageNum = pageNum
        self.frameNum = frameNum

class TLB():
    def __init__(self) -> None:
        self.entries : list[TLBEntry] = []
        self.numEntries = 0
        self.maxEntries = 16

    def lookupPage(self, pageNum : int) -> bool:
        for entry in self.entries:
            if entry.pageNum == pageNum:
                return entry.frameNum
        return None

    def updateTLB(self, newEntry: TLBEntry):
        if self.numEntries >= self.maxEntries:
            self.entries.pop(0)
            self.entries.append(newEntry)
        else:
            self.entries.append(newEntry)
            self.numEntries += 1

    def removeTLBEntry(self, pageNum:int):
        for i, entry in enumerate(self.entries):
            if entry.pageNum == pageNum:
                self.entries.pop(i)

    def inTLB(self, pageNum : int) -> bool:
        # searches for pageNum in self.entries
        if pageNum in self.entries:
            return True
        else:
            return False
        
class PageTableEntry():
    def __init__(self, frameNum : int,  valid : bool = False):
        self.frameNum = frameNum
        self.valid = valid
        
class PageTable():
    def __init__(self):
        self.entries : list[PageTableEntry] = [None] * (2 ** 8) # 2 ^ 8 = 256

    def updatePageTable(self, pageIndex, frameNum, valid):
        self.entries[pageIndex] = PageTableEntry(frameNum, valid)

    def getPageEntry(self, pageIndex):
        return self.entries[pageIndex]

class RAM():
    def __init__(self, frames:int):
        self.frames : list[bytes] = [None] * frames
        self.maxFrames = frames
        self.framesFilled = 0
    
    def isFull(self):
        return self.framesFilled >= self.maxFrames
        
