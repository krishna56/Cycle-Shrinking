"""
    Implementation of cycle shrinking
"""

"""
    There are some assumptions:
        1) All loop indexes start from 1 and their bounds can be different
        2) The code is written only for constant distance
"""


class constant_distance:
    """
        This class finds the dependence distance vector given all the loop inputs.

        Data variables:
            m = No. of loop indexes
            loop_bounds = list containing loop_bounds of every loop index
            p = No. of reference pairs
            pairs = list containing the [index number,co-efficient of that index,source distance,sink distance] for each reference pair

        Member Functions:
            data_dependence:
                Arguments:
                    Class variables
                Return statement:
                    Returns a dictionary which has following keys and values
                    key : index number
                    values : list containing distance for each reference of that index

            dependence_distance:
                Arguments:
                    Class variables
                    data_dependence_vector from previous function
                Return statement:
                    Returns a dictionary which has the following keys and values
                    key : index number
                    values : dependence distance corresponding to that index number

    """
    def __init__(self,m=0,loop_bounds=[],p=0,pairs=[]):
        self.m = m
        self.loop_bounds = loop_bounds
        self.p = p
        self.pairs = pairs

    def data_dependence(self):
        data_dependence_vector = {}
        for i in range(0,len(self.pairs),4):
            if pairs[i] in data_dependence_vector:
                data_dependence_vector[self.pairs[i]].append((self.pairs[i+2]-self.pairs[i+3])/self.pairs[i+1])
            else:
                data_dependence_vector[self.pairs[i]] = [(self.pairs[i+2]-self.pairs[i+3])/self.pairs[i+1]]
        return data_dependence_vector

    def dependence_distance(self,data_dependence_vector):
        dependence_distance_vector={}
        for k,v in data_dependence_vector.iteritems():
            if (all(i>=0 for i in v)):
                dependence_distance_vector[k] = min(v)
            elif(all(i<0 for i in v)):
                dependence_distance_vector[k] = max(v)
            else:
                dependence_distance_vector[k] = 0
        return dependence_distance_vector


"""
    The input file contains following inputs:

    First line : Number of loop indexes(m)
    Next m lines : Bounds of all loop indexes(loop_bounds)
    (m+2)th line : Number of reference pairs(p)
    Next 4*p lines : Every three lines will have the following inputs (pairs):
                        [index number,coefficient of that index,source distance,sink distance]
"""

# Function for taking input from the file 'input' and storing it in list_input_num
def reading_input():
    input_file = open("input",'r')
    list_input_num = []
    for line in input_file.readlines():
        x = int(line.strip())
        list_input_num.append(x)
    input_file.close()
    return list_input_num

if __name__ == '__main__':

    #Calling function to read input from the file 'input'
    list_input_num = reading_input()

    m = list_input_num[0]
    loop_bounds = list_input_num[1:m+1]
    p = list_input_num[m+1]
    pairs = list_input_num[m+2:len(list_input_num)]

    #cd is class object of class constant_distance
    cd = constant_distance(m,loop_bounds,p,pairs)
    data_dependence_vector = cd.data_dependence()
    dependence_distance_vector = cd.dependence_distance(data_dependence_vector)

    print(cd.m)
    print(cd.loop_bounds)
    print(cd.p)
    print(cd.pairs)
    print(dependence_distance_vector)
