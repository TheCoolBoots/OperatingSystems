
class job:
    def __init__(self, id, runTime, arrivalTime):
        self.arrivalTime = arrivalTime
        self.runTime = runTime
        self.runTimeRemaining = runTime
        self.completionTime = None
        self.idNum = id
        self.scheduled = False
        self.waitTime = 0

    def __eq__(self, other):
        if type(other) != job:
            return False
        return self.idNum == other.idNum and self.arrivalTime == other.arrivalTime and self.runTime == other.runTime

    def __str__(self):
        return f'{self.idNum}, {self.runTime}, {self.arrivalTime}'

def parse_input(filepath : str)-> list[job]:

    jobList = []

    with open(filepath, 'r') as inputFile:
        id = 0
        for line in inputFile.readlines():
            jobList.append(job(id, int(line.split(' ')[0]), int(line.split(' ')[1])))
            id += 1

    return jobList

