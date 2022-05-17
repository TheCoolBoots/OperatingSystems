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


    def loadInputFile(self, filepath:str):
        with open(filepath, 'r') as file:
            lines = file.readlines()
            self.memoryAccesses = list(map(lambda string: int(string.strip()), lines))
        return self.memoryAccesses


    def loadBackingStore(self, fp, pt_entries=PT_ENTRIES, page_size=PAGE_SIZE):
        self.backingStore = []
        with open(fp, 'rb') as f:
            raw = f.read()
            for i in range(0, pt_entries-1):
                page = raw[i*page_size: (i+1)*page_size]
                self.backingStore.append(page)
        return self.backingStore
            

    def runMemSim():
        pass

    def memoryLookup(self, virtualAddress:int, tlb:TLB, pageTable:PageTable, ram:RAM, backingStore:list[bytes], swap:list[bytes]):
        pageTableNum = self.getPageTableNum(virtualAddress)
        frameNum = tlb.lookupPage(pageTableNum)
        if frameNum != None:
            return ram[frameNum][self.getOffsetBits(virtualAddress)]
        else:
            if pageTable[pageTableNum] == None: # if the page hasn't been loaded yet
                page = backingStore[pageTableNum]
                if ram.isFull():
                    pass # replace with eviction algorithm
                else:
                    ram[ram.framesFilled] = page
                    pageTable.updatePageTable(pageTableNum, ram.framesFilled, True)
                    tlb.updateTLB(TLBEntry(pageTableNum, ram.framesFilled))
                    ram.framesFilled += 1
            else:
                pageTableEntry = pageTable.getPageEntry(pageTableNum)
                if pageTableEntry.valid:
                    return ram[pageTableEntry.frameNum][self.getOffsetBits(virtualAddress)]
                else:
                    page = swap[pageTableNum]
                    pass # replace with eviction algorithm
            

    def getPageToEvict(self, physicalAddress:int, pageReplacementAlgorithm:str, pageReplaceQueue:list[int]):
        match pageReplacementAlgorithm:
            case 'FIFO':
                evictPage = pageReplaceQueue.pop(0)
                pageReplaceQueue.append(physicalAddress)
                return evictPage
            case 'LRU':
                evictPage = pageReplaceQueue.pop(0) 
                indexCounter = 0
                for element in pageReplaceQueue:
                    if element == evictPage:
                        pageReplaceQueue.pop(indexCounter)
                    indexCounter = indexCounter + 1
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


