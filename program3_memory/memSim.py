import sys 

from operator import index
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

        self.pageTable : PageTable = PageTable()
        self.tlb : TLB = TLB()
        self.ram : RAM = RAM(numFrames)
        self.swap = []


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
            

    def runMemSim(self):
        # while accesses is not empty 
        #print
        #For every address in the given addresses file, print one line of comma-separated fields, consisting of
        #The full address (from the reference file)
        #The value of the byte referenced (1 signed integer)
        #The physical memory frame number (one positive integer)
        #The content of the entire frame (256 bytes in hex ASCII characters, no spaces in between)
        #new line character


      
        while len(self.memoryAccesses) != 0:
            currentVA = self.memoryAccesses[0]
            frameContent, accessedByte, physicalMem = self.memoryLookup(self.memoryAccesses[0])
            print( str(currentVA) + ", " + str(accessedByte) + ", " + str(physicalMem) + ", " + str(frameContent) + '\n') 

        
#(memory content, accessed value)
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
                if pageTableEntry.valid:
                    return self.ram[pageTableEntry.frameNum][self.getOffsetBits(virtualAddress)]
                else:
                    page = self.swap[pageTableNum]
                    pass # replace with eviction algorithm
        self.memoryAccesses.pop(0)
            

    def getPageToEvict(self, pageReplacementAlgorithm:str, pageReplaceQueue:list[int]):
        match pageReplacementAlgorithm:
            case 'FIFO':
                evictPage = pageReplaceQueue.pop(0)
                return evictPage
            case 'LRU':
                evictPage = pageReplaceQueue.pop(0) 
                for i, element in enumerate(pageReplaceQueue):
                    if element == evictPage:
                        pageReplaceQueue.pop(i)
                return evictPage
            case 'OPT':
                # make a subset of the elements that have valid bit = 0
                subsetList = []
                for element in self.pageTable:
                    if element.valid:
                        subsetList.append(element)
                
                # make a copy of the memory accesses
                accesses = self.memoryAccesses.copy()

                for i, accessID in enumerate(accesses):
                    if len(subsetList) == 1:
                        break
                    try:
                        subsetList.remove(accessID)
                    except:
                        pass
                
                # remove the last used mem (the only element in QCopy)
                evictPage = subsetList[0]
                return evictPage



    def getPageTableNum(self, virtualAddress):
        return virtualAddress >> (self.addressSizeBits - 8)


    def getOffsetBits(self, virtualAddress):
        return int('1'*(self.addressSizeBits - 8)) & virtualAddress


memSim = MemSimulator("hello", 2048, "BACKING_STORE.bin", "tst")
# memSim.loadInputFile("tst")
# print(bin(memSim.getPageTableNum(0b11100000000)))
# print(memSim.backingStore[0])

# memSim <reference-sequence-file.txt> <FRAMES> <PRA>
# For defaults use 256 frames, and FIFO as the page replacement algorithm.
if __name__ == '__main__':
    match sys.argv:
        case [pyFile, inputFile]:
            memSim = MemSimulator("FIFO", 256, "BACKING_STORE.bin", inputFile)
            pass
        case [pyFile, inputFile, param1a, param1b]:
            memSim = MemSimulator(param1b, param1a, "BACKING_STORE.bin", inputFile)
            pass
        case [pyFile, inputFile, param1a]:
            if param1a == 'FIFO' or param1a == "LRU" or param1a == "OPT":
                memSim = MemSimulator(param1a, 256, "BACKING_STORE.bin", inputFile)
            else:
                memSim = MemSimulator("FIFO", param1a, "BACKING_STORE.bin", inputFile)
        case default:
            print('ERROR: unrecognized input. Use format python memSim.py <reference-sequence-file.txt> <FRAMES> <PRA>')

