"""
    This contains tests for all the functions and class
"""
import unittest
import sys
import os
sys.path.append(os.path.abspath(".."))
from const_dist import reading_input
from const_dist import distributing_input_list
from const_dist import ConstantDistance

class TestConstDistFile(unittest.TestCase):

    def setUp(self):
        path = os.path.join("." , "input")
        f = open(path,'w')
        f.close()

    def tearDown(self):
        os.remove(os.path.join("." , "input"))

    def test_reading_input(self):
        result = reading_input()
        self.assertEqual(result , [])

    def test_distributing_input_list(self):
        list_input_num = ['0','0']
        result = distributing_input_list(list_input_num)
        self.assertEqual(result , [0,[],0,[],[]])

if  __name__ == '__main__' :
    unittest.main()

