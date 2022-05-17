from memClasses import *

def loadInputFile(filepath:str)->list[int]:
    inputList = []

    with open(filepath, 'r') as inputFile:
        id = 0
        for line in inputFile.readlines():
            inputList.append(line)
            id += 1

    return inputList

def initializeSystem(pageReplacementAlgorithm:str, RAMSize:int):
    pass

def runMemSim():
    pass

def memoryLookup(virtualAddress:int, tlb:list[TLBEntry], pageTable:list[PageTableEntry], ram:bytes, backingStore:bytes):
    pass

def getPageToEvict(physicalAddress:int, pageReplacementAlgorithm:str, pageReplaceQueue:list[int]):
    pass

