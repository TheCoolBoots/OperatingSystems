import unittest


from parser import parse_input, job
from scheduler import simulate_fifo_scheduler, simulate_rr, simulate_srtn

class test_scheduler(unittest.TestCase):

    def test_fifo(self):
        jobList = parse_input('program2_scheduler/testFiles/FCFS.tst')

        expected = ['Job 0 -- Turnaround 6  Wait 5', 
                    'Job 1 -- Turnaround 6  Wait 2', 
                    'Job 2 -- Turnaround 12  Wait 8', 
                    'Job 3 -- Turnaround 12  Wait 6', 
                    'Job 4 -- Turnaround 3  Wait 0', 
                    'Average -- Turnaround 7.80  Wait 4.20']

        actual = simulate_fifo_scheduler(jobList)
        self.assertEqual(expected, actual)
    

    def test_rr(self):
        jobList = parse_input('program2_scheduler/testFiles/RR.tst')

        expected = ['Job 0 -- Turnaround 16  Wait 11', 
                    'Job 1 -- Turnaround 6  Wait 4', 
                    'Job 2 -- Turnaround 17  Wait 12', 
                    'Job 3 -- Turnaround 14  Wait 11', 
                    'Job 4 -- Turnaround 12  Wait 10', 
                    'Average -- Turnaround 13.00  Wait 9.60']

        actual = simulate_rr(jobList, 4)
        self.assertEqual(expected, actual)
        
    def test_srtn(self):
        jobList = parse_input('program2_scheduler/testFiles/SRTN.tst')

        expected = ['Job 0 -- Turnaround 7  Wait 3', 
                    'Job 1 -- Turnaround 2  Wait 0', 
                    'Job 2 -- Turnaround 3  Wait 0', 
                    'Job 3 -- Turnaround 12  Wait 8', 
                    'Job 4 -- Turnaround 7  Wait 4', 
                    'Average -- Turnaround 6.20  Wait 3.00']

        actual = simulate_srtn(jobList)
        print(actual)

if __name__ == '__main__':
    unittest.main()