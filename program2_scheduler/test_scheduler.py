import unittest

import joblib

from parser import parse_input, job
from scheduler import simulate_fifo_scheduler

class test_scheduler(unittest.TestCase):

    def test_parser(self):
        jobList = parse_input('program2_scheduler/testFiles/SRTN.tst')

        expected = [job(0, 4, 3),
                    job(1, 4, 5),
                    job(2, 3, 1),
                    job(3, 2, 5),
                    job(4, 3, 6)]

        self.assertEqual(jobList, expected)

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
        

if __name__ == '__main__':
    unittest.main()