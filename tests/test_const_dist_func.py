"""
    This contains tests for all the functions and class
"""
import unittest
import os
from constant_distance.const_dist import reading_input
from constant_distance.const_dist import distributing_input_list
from constant_distance.const_dist import ConstantDistance

class TestConstDistFile(unittest.TestCase):

    def setUp(self):
        path = os.path.join("." , "input")
        f = open(path,'w')
        f.close()
        c = ConstantDistance()

    def tearDown(self):
        os.remove(os.path.join("." , "input"))

    def test_reading_input_reading_empty_file(self):
        result = reading_input()
        self.assertEqual(result , [])

    def test_distributing_input_list(self):
        list_input_num = ['0','0']
        result = distributing_input_list(list_input_num)
        self.assertEqual(result , [0,[],0,[],[]])

    def test_data_dependence(self):
        pass

if  __name__ == '__main__' :
    unittest.main()

