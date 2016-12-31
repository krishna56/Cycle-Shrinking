"""
    This file contains tests for all the functions and class members
"""

import unittest
import os
from constant_distance.parallel_code_generation import ParallelCode

class TestCodeGenerationFile(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_partition_num(self):
        p = ParallelCode([['i',1,10],['j',1,8]], {'i': 2,'j': 3} , ["A[i+3][j+2] = B[i][j];"])
        result = p.partition_num()
        self.assertEqual(result, 3)

    def test_generate_code(self):
        temp1 = []
        temp2 = []

        file1 = open("../input/serial_code_result",'r')
        file2 = open("../result/parallel_code_result" , 'r')

        for line in file1.readlines():
            temp1.append(line)

        for line in file2.readlines():
            temp2.append(line)

        self.assertEqual(temp1, temp2)

if __name__ == '__main__':
    unittest.main()


