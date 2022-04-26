
from re import L


from parser import *

def simulate_fifo_scheduler(jobList: list[job]):
    output = []
    jobList.sort(key = lambda j: (j.arrivalTime, j.runTime))
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

        
