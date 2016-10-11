"""
    Implementation of cycle shrinking

    There are some assumptions:
        1) All loop indexes start from 1 and their bounds can be different
        2) The code is written only for constant distance
"""


class ConstantDistance:
    """
        This class finds the dependence distance vector given all the loop inputs.

        Data variables:
            m ->  No. of loop indexes
            loop_bounds ->  dictionary containing loop_bounds(value) of every loop index(key)
            p ->  No. of reference pairs
            pairs -> list containing the [index,co-efficient of that index,source distance,sink distance] for each reference pair
            code_lines -> list containing the inner most lines of the for loops

        Member Functions:
            data_dependence -> Returns a dictionary with (key,value) as (index num,list containing distance for each reference pair)
            dependence_distance:
                Arguments -> data_dependence_vector from previous function
                Return -> dictionary with (key,value) as (index num, dependence distance)
    """

    def __init__(self, m=0, p=0, pairs=[]):
        self.m = m
        self.p = p
        self.pairs = pairs

    def data_dependence(self):
        data_dependence_vector = {}

        for i in range(0,len(self.pairs),4):
            temp = (int(self.pairs[i+2])-int(self.pairs[i+3]))/int(self.pairs[i+1])
            if self.pairs[i] in data_dependence_vector:
                data_dependence_vector[self.pairs[i]].append(temp)
            else:
                data_dependence_vector[self.pairs[i]] = [temp]

        return data_dependence_vector

    def dependence_distance(self,data_dependence_vector):
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

    list_input_num = reading_input()
    m = int(list_input_num[0])
    loop_bounds = []

    for i in range(1, 2*m+1, 2):
        loop_bounds.append([list_input_num[i],int(list_input_num[i+1])])

    p = int(list_input_num[2*m+1])
    pairs = list_input_num[2*m+2 : 2*m+2+4*p]
    code_lines = list_input_num[2*m+2+4*p : len(list_input_num)]
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

