import sys 

from operator import index
from typing import Tuple
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
        self.swap = [None] * PT_ENTRIES

        self.runMemSim()



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
            # TLB Hit
            physAddr = int(format(frameNum, 'b') + format(self.getOffsetBits(virtualAddress), 'b'))
            return self.ram.frames[frameNum], self.ram.frames[frameNum][self.getOffsetBits(virtualAddress)], physAddr
        else:  
            # TLB Miss
            if self.pageTable.entries[pageTableNum] == None: # if the page hasn't been accessed yet
                page = self.backingStore[pageTableNum]
                if self.ram.isFull():
                    # hard page miss
                    return self.pageMiss(pageTableNum, self.getOffsetBits(virtualAddress), True)
                else: 
                    # if ram isn't full, fill RAM sequentially
                    frameNum = self.ram.framesFilled
                    self.ram.frames[frameNum] = page
                    self.pageTable.updatePageTable(pageTableNum, frameNum, True)
                    self.tlb.updateTLB(TLBEntry(pageTableNum, frameNum))
                    self.ram.framesFilled += 1

                    offsetBits = self.getOffsetBits(virtualAddress)
                    physAddr = int(format(frameNum, 'b') + format(offsetBits, 'b'))

                    return self.ram.frames[frameNum], self.ram.frames[frameNum][offsetBits], physAddr
            else: # page has been accessed previously
                pageTableEntry = self.pageTable.getPageEntry(pageTableNum)
                if pageTableEntry.valid:    
                    # page table hit
                    self.tlb.updateTLB(TLBEntry(pageTableNum, pageTableEntry.frameNum))
                    offsetBits = self.getOffsetBits(virtualAddress)
                    physAddr = int(format(pageTableEntry.frameNum, 'b') + format(offsetBits, 'b'))
                    return self.ram[pageTableEntry.frameNum], self.ram[pageTableEntry.frameNum][offsetBits], physAddr
                else:   
                    # soft page miss
                    # page is in swap
                    return self.pageMiss(pageTableNum, self.getOffsetBits(virtualAddress))

            

    def pageMiss(self, pageIndex, offsetBits, hardMiss = False):
        if hardMiss:
            pageIn = self.backingStore[pageIndex]
        else:
            pageIn = self.swap[pageIndex]

        # get page number of page to evict from RAM
        pageNumToReplace = self.getPageToEvict()

        # get the frame number that is housing the evictee
        relevantFrame = self.pageTable.getPageEntry(pageNumToReplace).frameNum

        # set the evictee's swap to the contents in ram
        self.swap[pageNumToReplace] = self.ram.frames[relevantFrame]

        # set the frame to the page retreived from swap or backing store
        self.ram.frames[relevantFrame] = pageIn

        # update the page table
        self.pageTable.updatePageTable(pageNumToReplace, relevantFrame, False)
        self.pageTable.updatePageTable(pageIndex, relevantFrame, True)

        # update the TLB
        self.tlb.updateTLB(TLBEntry(pageIndex, relevantFrame))
        
        physAddr = int(format(relevantFrame, 'b') + format(offsetBits, 'b'))

        return self.ram.frames[relevantFrame], self.ram.frames[relevantFrame][offsetBits], physAddr



    def getPageToEvict(self, pageReplaceQueue:list[int] = None):
        match self.pageRepAlg:
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


#memSim = MemSimulator("hello", 2048, "BACKING_STORE.bin", "tst")
# memSim.loadInputFile("tst")
# print(bin(memSim.getPageTableNum(0b11100000000)))
# print(memSim.backingStore[0])

# memSim <reference-sequence-file.txt> <FRAMES> <PRA>
# For defaults use 256 frames, and FIFO as the page replacement algorithm.
if __name__ == '__main__':
    match sys.argv:
        case [pyFile, inputFile]:
            memSim = MemSimulator("FIFO", 256, "BACKING_STORE.bin", inputFile)
        case [pyFile, inputFile, numOfFrames, algor]:
            if int(numOfFrames) > 256:
                print('ERROR')
            else:
                memSim = MemSimulator(algor, int(numOfFrames), "BACKING_STORE.bin", inputFile)
        case default:
            print('ERROR: unrecognized input. Use format python memSim.py <reference-sequence-file.txt> <FRAMES> <PRA>')

