from memClasses import *

def loadInputFile(filepath:str)->list[int]:
    inputList = []

    with open(filepath, 'r') as inputFile:
        for line in inputFile.readlines():
            inputList.append(int(line))

    return inputList

def initializeSystem(pageReplacementAlgorithm:str, RAMSize:int):
    pass

def runMemSim():
    pass

def memoryLookup(virtualAddress:int, tlb:list[TLBEntry], pageTable:list[PageTableEntry], ram:bytes, backingStore:bytes):
    pass

def getPageToEvict(physicalAddress:int, pageReplacementAlgorithm:str, pageReplaceQueue:list[int]):
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


