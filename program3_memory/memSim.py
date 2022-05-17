from memClasses import *
from math import log2
from memClasses import *


PAGE_SIZE = 256
PT_ENTRIES = 256
TLB_ENTRIES = 16


class MemSimulator():
    def __init__(self, pageReplacementAlgorithm:str, numFrames:int, backingStoreFP:str = None, inputFile:str = None) -> None:
        self.pageRepAlg = pageReplacementAlgorithm
        self.numFrames = numFrames
        self.RAMSizeBytes = numFrames * 256
        self.addressSizeBits = int(log2(numFrames))
        if inputFile != None:
            self.loadInputFile(inputFile)
        if backingStoreFP != None:
            self.loadBackingStore(backingStoreFP)

        self.pageTable = PageTable()
        self.tlb = TLB()
        self.ram = RAM(numFrames)
        self.swap = [None * PT_ENTRIES]


    def loadInputFile(self, filepath:str):
        with open(filepath, 'r') as file:
            lines = file.readlines()
            self.memoryAccesses = list(map(lambda string: int(string.strip()), lines))
        return self.memoryAccesses


    def loadBackingStore(self, fp, pt_entries=PT_ENTRIES, page_size=PAGE_SIZE):
        self.backingStore = []
        with open(fp, 'rb') as f:
            raw = f.read()
            # print(raw)
            for i in range(0, pt_entries):
                page = raw[i*page_size: (i+1)*page_size]
                self.backingStore.append(page)
        # print(self.backingStore[0].decode())
        return self.backingStore
            

    def runMemSim():
        pass


    def memoryLookup(self, virtualAddress:int):
        pageTableNum = self.getPageTableNum(virtualAddress)
        frameNum = self.tlb.lookupPage(pageTableNum)
        if frameNum != None:
            return self.ram[frameNum][self.getOffsetBits(virtualAddress)]
        else:
            if self.pageTable[pageTableNum] == None: # if the page hasn't been loaded yet
                page = self.backingStore[pageTableNum]
                if self.ram.isFull():
                    pass # replace with eviction algorithm
                else:
                    self.ram[self.ram.framesFilled] = page
                    self.pageTable.updatePageTable(pageTableNum, self.ram.framesFilled, True)
                    self.tlb.updateTLB(TLBEntry(pageTableNum, self.ram.framesFilled))
                    self.ram.framesFilled += 1
            else:
                pageTableEntry = self.pageTable.getPageEntry(pageTableNum)
                if pageTableEntry.valid:    # page table hit
                    self.pageTable.updatePageTable(pageTableNum, pageTableEntry.frameNum, True)
                    return self.ram[pageTableEntry.frameNum][self.getOffsetBits(virtualAddress)]
                else:
                    page = self.swap[pageTableNum]
                    pass # replace with eviction algorithm
            

    def getPageToEvict(self, physicalAddress:int, pageReplacementAlgorithm:str, pageReplaceQueue:list[int]):
        match pageReplacementAlgorithm:
            case 'FIFO':
                evictPage = pageReplaceQueue.pop(0)
                pageReplaceQueue.append(physicalAddress)
                return evictPage
            case 'LRU':
                evictPage = pageReplaceQueue.pop(0) 
                for i, element in enumerate(pageReplaceQueue):
                    if element == evictPage:
                        pageReplaceQueue.pop(i)
                return evictPage
            case 'OPT':
                # input
                pass


    def getPageTableNum(self, virtualAddress):
        return virtualAddress >> (self.addressSizeBits - 8)


    def getOffsetBits(self, virtualAddress):
        return int('1'*(self.addressSizeBits - 8)) & virtualAddress


memSim = MemSimulator("hello", 2048, "BACKING_STORE.bin", "tst")
# memSim.loadInputFile("tst")
# print(bin(memSim.getPageTableNum(0b11100000000)))
# print(memSim.backingStore[0])


