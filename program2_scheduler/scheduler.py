
from calendar import c
from re import L


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


def simulate_rr(jobList: list[job], quantum: int):
    output = []
    jobList.sort(key = lambda j: j.arrivalTime) # docs say to resolve ties by order in the file
    completedJobs = []
    queuedJobs = []

    currentTime = 0
    totalWaitTime = 0
    totalTurnaroundTime = 0

    currentJobIndex = None
    currentCycles = 0

    while len(jobList) > 0 and len(queuedJobs) > 0:

        # move all jobs that arrive at current time to queued jobs
        while(jobList[0].arrrivalTime == currentTime):
            queuedJobs.append(jobList.pop(0))
        

        # if no job in queue, skip cycle
        if(len(queuedJobs) == 0):
            currentTime += 1
            continue
            

        # if no job is scheduled
            # schedule queuedJobs[0]
            # set currentCycles to 0
        if(currentJobIndex == None):
            currentJobIndex = 0
            currentCycles = 0
        
        # simluate the cycle
            # add 1 to currentCycles
            # add 1 to currentTime
            # add 1 to wait time of all non-scheduled jobs
            # decrement remaining time for current job
        currentCycles += 1
        currentTime += 1
        for i, job in enumerate(queuedJobs):
            if (i != currentJobIndex):
                job.waitTime += 1
            
        queuedJobs[currentJobIndex].remainingTime -= 1

        # if remaining time for current job = 0
            # calculate turnaround time
            # if queue is not empty
                # schedule next job in queue
            # else
                # set current job to -1
            # move current job to completed jobs
            # set currentCycles to 0
        if(queuedJobs[currentJobIndex].remainingTime == 0):
            turnaroundTime = currentTime - queuedJobs[currentJobIndex].arrivalTime
            totalTurnaroundTime += turnaroundTime
                # print turnaround time, wait time
            output.append(f'Job {queuedJobs[currentJobIndex].idNum} -- Turnaround {turnaroundTime}  Wait {queuedJobs[currentJobIndex].waitTime}')
                # pop from queue
            completedJobs.append(queuedJobs.pop(currentJobIndex))
            if(len(queuedJobs) != 0):
                currentJobIndex = currentJobIndex % len(queuedJobs)
            else:
                currentJobIndex = None
            currentCycles = 0
            

        # elif currentCycles == quantum
        elif(currentCycles == quantum):
            if(len(queuedJobs) > 1):
                currentJobIndex = currentJobIndex % len(queuedJobs)
            currentCycles = 0
            # calculate turnaround time
            # if queue is not empty
                # schedule next job in queue
            # else
                # set current job to -1
            # set currentCycles = 0
    for i, job in enumerate(completedJobs):
        totalWaitTime += job.waitTime

    output.sort()
    output.append("Average -- Turnaround {:.2f}  Wait {:.2f}".format(totalTurnaroundTime/len(completedJobs), totalWaitTime/len(completedJobs)))
    return output