"""
    Implementation of cycle shrinking

    There are some assumptions:
        1) This code is written only for constant distance
        2) The code can parallelize only c++ code
"""


class ConstantDistance:
    """
        This class finds the dependence distance vector given all the loop inputs.

        Data variables:

            - m: No. of loop indexes
            - p: No. of reference pairs
            - pairs: list containing the [index,co-efficient of that index,source distance,sink distance]
    """

    def __init__(self, m=0, p=0, pairs=[]):
        self.m = m
        self.p = p
        self.pairs = pairs

    def data_dependence(self):
        """
            Returns a dict as (index num,list containing distance for each reference pair)
        """
        data_dependence_vector = {}

        for i in range(0,len(self.pairs),4):
            temp = (int(self.pairs[i+2])-int(self.pairs[i+3]))/int(self.pairs[i+1])
            if self.pairs[i] in data_dependence_vector:
                data_dependence_vector[self.pairs[i]].append(temp)
            else:
                data_dependence_vector[self.pairs[i]] = [temp]

        return data_dependence_vector

    def dependence_distance(self,data_dependence_vector):
        """
            Arguments: dict data_dependence_vector from data_dependence member

            Return: dependence_distance_vector dict as (index, dependence_distance)
        """
        dependence_distance_vector={}

        for k,v in data_dependence_vector.iteritems():
            if (all(i >= 0 for i in v)):
                dependence_distance_vector[k] = min(v)
            elif(all(i < 0 for i in v)):
                dependence_distance_vector[k] = max(v)
            else:
                dependence_distance_vector[k] = 0

        return dependence_distance_vector


"""
    The input file contains following inputs:

    First line : Number of loop indexes(m)
    Next 2m lines : Bounds of all loop indexes(index, loop_bounds of that index)
    (2m+2)th line : Number of reference pairs(p)
    Next 4*p lines : Every three lines will have the following inputs (pairs):
                        [index,coefficient of that index,source distance,sink distance]
    last m lines : code
"""

def reading_input():
    """
        Function for taking input from the file 'input' and storing it in list_input_num
    """
    input_file = open("input",'r')
    list_input_num = []

    for line in input_file.readlines():
        x = str(line.strip())
        list_input_num.append(x)

    input_file.close()
    return list_input_num

def distributing_input_list(list_input_num):
    """
        Function to distribute the values in the list_input_num to suitable variables
    """

    m = int(list_input_num[0])
    loop_bounds = []

    for i in range(1, 3*m+1, 3):
        loop_bounds.append([list_input_num[i],int(list_input_num[i+1]),int(list_input_num[i+2])])

    p = int(list_input_num[3*m+1])
    pairs = list_input_num[3*m+2 : 3*m+2+4*p]
    code_lines = list_input_num[3*m+2+4*p : len(list_input_num)]
    return [m, loop_bounds, p, pairs, code_lines]

if __name__ == '__main__':

    list_input_num = reading_input()
    [m, loop_bounds, p, pairs, code_lines] = distributing_input_list(list_input_num)

    #cd is the class ConstantDistance object
    cd = ConstantDistance(m, p, pairs)
    data_dependence_vector = cd.data_dependence()
    dependence_distance_vector = cd.dependence_distance(data_dependence_vector)

    print 'Number of loop index:', cd.m
    print 'Number of reference pairs:',cd.p
    print 'List of pairs:',cd.pairs
    print 'Dependence distance vector:',dependence_distance_vector

