from memClasses import *


def loadInputFile(filepath:str):
    pass

def initializeSystem(pageReplacementAlgorithm:str, RAMSize:int):
    pass

def runMemSim():
    pass

def memoryLookup(virtualAddress:int, tlb:list[TLBEntry], pageTable:list[PageTableEntry], ram:bytes, backingStore:bytes):
    pass

def getPageToEvict(physicalAddress:int, pageReplacementAlgorithm:str, pageReplaceQueue:list[int]):
    pass

