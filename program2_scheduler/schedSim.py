import sys

import joblib

from parser import *

def simulate_fifo_scheduler(jobList: list[job]):
    output = []
    # jobList.sort(key = lambda j: (j.arrivalTime, j.runTime))
    jobList.sort(key = lambda j: j.arrivalTime) # docs say to resolve ties by order in the file
    completedJobs = []
    currentTime = 0
    totalWaitTime = 0
    totalTurnaroundTime = 0

    while len(jobList) > 0:
        
        # no jobs to run
        if jobList[0].arrivalTime > currentTime:
            currentTime += 1

        # is a job to run
        else:
            if not jobList[0].scheduled:
                # calculate wait time
                jobList[0].waitTime = currentTime - jobList[0].arrivalTime 
                # add to total wait time
                totalWaitTime += jobList[0].waitTime
                # change scheduled to True
                jobList[0].scheduled = True
            
            jobList[0].runTimeRemaining -= 1

            currentTime += 1
            
            if jobList[0].runTimeRemaining == 0:
                # calculate turnaround time
                turnaroundTime = currentTime - jobList[0].arrivalTime
                totalTurnaroundTime += turnaroundTime
                # print turnaround time, wait time
                output.append(f'Job {jobList[0].idNum} -- Turnaround {turnaroundTime}  Wait {jobList[0].waitTime}')
                # pop from queue
                completedJobs.append(jobList.pop(0))

    output.sort()
    output.append("Average -- Turnaround {:.2f}  Wait {:.2f}".format(totalTurnaroundTime/len(completedJobs), totalWaitTime/len(completedJobs)))
    return output


def simulate_rr(jobList: list[job], quantum: int = 1):
    output = []
    jobList.sort(key = lambda j: j.arrivalTime) # docs say to resolve ties by order in the file
    completedJobs = []
    queuedJobs = []

    currentTime = 0
    totalWaitTime = 0
    totalTurnaroundTime = 0

    currentJobIndex = None
    currentCycles = 0

    while len(jobList) > 0 or len(queuedJobs) > 0:

        while len(jobList) > 0 and jobList[0].arrivalTime == currentTime:
            queuedJobs.append(jobList.pop(0))
        
        if len(queuedJobs) == 0:
            currentTime += 1
            continue
            
        if currentJobIndex == None:
            currentJobIndex = 0
            currentCycles = 0

        currentCycles += 1
        currentTime += 1
        for i, j in enumerate(queuedJobs):
            if (i != currentJobIndex):
                j.waitTime += 1
            
        queuedJobs[currentJobIndex].runTimeRemaining -= 1

        if queuedJobs[currentJobIndex].runTimeRemaining == 0:
            turnaroundTime = currentTime - queuedJobs[currentJobIndex].arrivalTime
            totalTurnaroundTime += turnaroundTime
            output.append(f'Job {queuedJobs[currentJobIndex].idNum} -- Turnaround {turnaroundTime}  Wait {queuedJobs[currentJobIndex].waitTime}')
            completedJobs.append(queuedJobs.pop(currentJobIndex))
            if(len(queuedJobs) != 0):
                currentJobIndex = currentJobIndex % len(queuedJobs)
            else:
                currentJobIndex = None
            currentCycles = 0
            

        # elif currentCycles == quantum
        elif(currentCycles == quantum):
            if(len(queuedJobs) > 1):
                currentJobIndex = (currentJobIndex + 1) % len(queuedJobs)
            currentCycles = 0

    for i, job in enumerate(completedJobs):
        totalWaitTime += job.waitTime

    output.sort()
    output.append("Average -- Turnaround {:.2f}  Wait {:.2f}".format(totalTurnaroundTime/len(completedJobs), totalWaitTime/len(completedJobs)))
    return output


def simulate_srtn(jobList: list[job]):
    output = []
    jobList.sort(key = lambda j: j.arrivalTime) # docs say to resolve ties by order in the file
    completedJobs = []
    queuedJobs = []

    currentTime = 0
    totalWaitTime = 0
    totalTurnaroundTime = 0

    while len(jobList) > 0 or len(queuedJobs) > 0:

        addedStuff = False
        while len(jobList) > 0 and jobList[0].arrivalTime == currentTime:
            queuedJobs.append(jobList.pop(0))
            addedStuff = True
        if addedStuff:
            queuedJobs.sort(key = lambda j: j.runTimeRemaining)
        
        if len(queuedJobs) == 0:
            currentTime += 1
            continue
            
        currentTime += 1
        for j in queuedJobs[1:]:
            j.waitTime += 1
            
        queuedJobs[0].runTimeRemaining -= 1

        if queuedJobs[0].runTimeRemaining == 0:
            turnaroundTime = currentTime - queuedJobs[0].arrivalTime
            totalTurnaroundTime += turnaroundTime
            output.append(f'Job {queuedJobs[0].idNum} -- Turnaround {turnaroundTime}  Wait {queuedJobs[0].waitTime}')
            completedJobs.append(queuedJobs.pop(0))
            if  len(queuedJobs) == 0:
                currentJobIndex = None     

    for i, job in enumerate(completedJobs):
        totalWaitTime += job.waitTime

    output.sort()
    output.append("Average -- Turnaround {:.2f}  Wait {:.2f}".format(totalTurnaroundTime/len(completedJobs), totalWaitTime/len(completedJobs)))
    return output


def runScheduler(inputFilepath:str, algorithm:str = 'FIFO', quantum:int = 1):
    jobList = parse_input(inputFilepath)
    match algorithm:
        case 'FIFO':
            return '\n'.join(simulate_fifo_scheduler(jobList))
        case 'RR':
            if quantum > 0:
                return '\n'.join(simulate_rr(jobList, quantum))
            else:
                return 'ERROR: quantum must be > 0'
        case 'SRTN':
            return '\n'.join(simulate_srtn(jobList))
        case other:
            return f'ERROR: unrecognized algorithm {other}'


if __name__ == '__main__':
    match sys.argv:
        case [pyFile, inputFile]:
            jobList = parse_input(inputFile)
            print(runScheduler(inputFile))
            pass
        case [pyFile, inputFile, param1a, param1b]:
            jobList = parse_input(inputFile)
            match param1a:
                case '-p':
                    print(runScheduler(inputFile, param1b))
                case '-q':
                    print(runScheduler(inputFile, quantum=int(param1b)))
                case other:
                    print(f'ERROR: unrecognized option {other}')
        case [pyFile, inputFile, '-p', param1b, '-q', param2b]:
            print(runScheduler(inputFile, param1b, int(param2b)))
        case [pyFile, inputFile, '-q', param1b, '-p', param2b]:
            print(runScheduler(inputFile, param2b, int(param1b)))
        case default:
            print('ERROR: unrecognized input. Use format python scheduler.py <job-file.txt> [-p <ALGORITHM>] [-q <QUANTUM>]')