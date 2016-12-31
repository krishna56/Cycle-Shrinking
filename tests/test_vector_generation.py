"""
    This contains tests for all the functions and class
"""
import unittest
import os
from constant_distance.vector_generation import reading_input
from constant_distance.vector_generation import distributing_input_list
from constant_distance.vector_generation import ConstantDistance

class TestConstDistFile(unittest.TestCase):

    def setUp(self):
        path = os.path.join("." , "input")
        f = open(path,'w')
        f.close()
        c = ConstantDistance()

    def tearDown(self):
        os.remove(os.path.join("." , "input"))

    def test_reading_input_reading_empty_file(self):
        path = os.path.join("." , "input")
        result = reading_input(path)
        self.assertEqual(result , [])

    def test_distributing_input_list(self):
        list_input_num = ['0','0']
        result = distributing_input_list(list_input_num)
        self.assertEqual(result , [0,[],0,[],[]])

    def test_data_dependence(self):
        c = ConstantDistance(1,2,['i',1,3,0,'i',1,2,0])
        result = c.data_dependence()
        self.assertEqual(result, {'i' : [3,2]})

    def test_dependence_distance_all_negative_distance(self):
        c = ConstantDistance(1,2,['i',1,-3,0,'i',1,-2,0])
        result = c.dependence_distance({'i':[-3,-2]})
        self.assertEqual(result, {'i': -2 })

    def test_dependence_distance_all_positive_distance(self):
        c = ConstantDistance(1,2,['i',1,3,0,'i',1,2,0])
        result = c.dependence_distance({'i' : [3,2]})
        self.assertEqual(result, {'i' : 2})

    def test_dependence_distance_both(self):
        c = ConstantDistance(1,2,['i',1,-3,0,'i',1,2,0])
        result = c.dependence_distance({'i' : [-3,2]})
        self.assertEqual(result, {'i' : 0})

if  __name__ == '__main__' :
    unittest.main()

