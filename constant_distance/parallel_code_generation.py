"""
    Generates c++ parallel code in OpenMP using cycle shrinking algorithm
"""

import math
from vector_generation import ConstantDistance
from vector_generation import reading_input
from vector_generation import distributing_input_list
import sys

class ParallelCode:

    """
       This class generates the c++ parallel code given the dependence distance vector

       Data Variables:

           - loop_bounds: list containing list of index and its loop bounds
           - code_lines: list containing lines for initialization and inner most loop code
           - dependence_vector: dictionary containing dependence distance vector(value) with index as (key)
    """

    def __init__(self, loop_bounds=[], dependence_vector={}, code_lines=[]):

        self.loop_bounds = loop_bounds
        self.code_lines = code_lines
        self.dependence_vector = dependence_vector

    def partition_num(self):
        """
            Returns the minimum number of partition of iteration space
        """
        partition_no=[]

        for i in range(len(self.loop_bounds)):
            x = abs(self.dependence_vector[self.loop_bounds[i][0]])
            if(x != 0):
                temp = math.ceil(float((self.loop_bounds[i][2] - self.loop_bounds[i][1] + 1)) /float(x))
                partition_no.append(temp)

        return min(partition_no)

    def generate_code(self, partition_no):
        """
            Prints the final parallel code to the screen
        """

        # Include statements
        print "#include<iostream>"
        print ""
        print "using namespace std;"
        print ""

        # Main function starts here
        print "int main()"
        print "{"

        # Initializing matrix using initialization file
        initialization = open("../input/initialization",'r')
        for lines in initialization.readlines():
            print "    " + str(lines.strip())

        print ""

        # Initializing the length
        print "    int length=" + str(len(self.loop_bounds)) + ";"
        print ""

        # Initializing the lower_loop_bound
        print "    int lower_loop_bounds[] = {"

        for i in range(len(self.loop_bounds)):
            print "    " + str(self.loop_bounds[i][1]) + ","

        print "    };"
        print ""

        # Initializing loop_bounds
        print "    int loop_bounds[] = {"

        for i in range(len(self.loop_bounds)):
            print "    " + str(self.loop_bounds[i][2]) + ","

        print "    };"
        print ""

        # Initializing the dependence distance
        print "    int dep_dist[] = {"

        for i in range(len(self.loop_bounds)):
            print "    " + str(self.dependence_vector[self.loop_bounds[i][0]]) + ","

        print "    };"
        print ""

        # Initializing the loop index
        print "    int "

        for i in range(len(self.loop_bounds)-1):
            print "    " + str(self.loop_bounds[i][0]) + ","

        print "    " + str(self.loop_bounds[len(self.loop_bounds)-1][0]) + ";"
        print ""

        # Initializing the partition number
        print "    int partition_no=" + str(partition_no) + ";"
        print ""

        # Main loop starts here
        print "    for(int part=1; part <= partition_no; part++)"
        print "    {"

        # Initializing the length
        print "        int start[length];"
        print ""

        # Loop for calculation of start[h] based on dependence distance
        print "        #pragma omp parallel for shared(dep_dist)"
        print "        for(int h=0; h<length; h++)"
        print "        {"
        print "            if (dep_dist[h] > 0) { start[h] = lower_loop_bounds[h] +(part-1)*dep_dist[h]; } "
        print "            else if (dep_dist[h] == 0) { start[h] = lower_loop_bounds[h];}"
        print "            else { start[h] = loop_bounds[h] + (part-1)*dep_dist[h]; } "
        print "        }"
        print ""

        # Main parallel portion starts here
        for i in range(len(self.loop_bounds)):
            if (self.dependence_vector[self.loop_bounds[i][0]] != 0):

                temp = ""
                st = ""

                # Below two for loops are creating string(st) to be put in pragma statement
                for j in range(len(self.loop_bounds)):
                    if (self.loop_bounds[i][0] != self.loop_bounds[j][0]):
                        temp = temp + self.loop_bounds[j][0]

                for j in range(len(temp)):
                    if (j != len(temp)-1): st = st + temp[j] + ","
                    else: st = st + temp[j]

                print "        #pragma omp parallel for private(" + st + ") shared(loop_bounds,dep_dist)"
                x = self.loop_bounds[i][0]
                y = str(i)
                if (self.dependence_vector[x] > 0):
                    print "        for(" + x  + "=start[" + y + "]; " + x + \
                            "<= min(start[" + y + "]+dep_dist[" + y + "]-1,loop_bounds[" + y + "]); " + x + "++)"
                    print "        {"

                    for k in range(i):
                        a = self.loop_bounds[k][0]
                        b = str(k)
                        if (self.dependence_vector[a] > 0):
                            print "           for(" + a + "=start[" + b + "]+dep_dist[" + b + "]; " + a + "<=loop_bounds[" + b + "]; " + a + "++)"
                            print "           {"
                        elif (self.dependence_vector[a] == 0):
                            print "           for(" + a + "=start[" + b + "]; "+ a + " <= loop_bounds[" + b + "]; " + a + "++)"
                            print "           {"
                        else:
                            print "           for(" + a + "=start[" + b + "]+ dep_dist[" + b + "]; " + a + ">= lower_loop_bounds[" + b + "];" + a + "--)"
                            print "           {"

                    for m in range(i+1, len(self.loop_bounds)):
                        a = self.loop_bounds[m][0]
                        b = str(m)
                        if (self.dependence_vector[a] > 0):
                            print "           for(" + a + "=start[" + b + "]; " + a + "<=loop_bounds[" + b + "]; " + a + "++)"
                            print "           {"
                        elif (self.dependence_vector[a] == 0):
                            print "           for(" + a + "=start[" + b + "]; "+ a + " <= loop_bounds[" + b + "]; " + a + "++)"
                            print "           {"
                        else:
                            print "           for(" + a + "=start[" + b + "];" + a + ">= lower_loop_bounds[" + b + "]; " + a + "--)"
                            print "           {"

                    for l in range(len(self.code_lines)):
                        print "               " + self.code_lines[l]

                    for k in range(i):
                        print "           }"

                    for m in range(i+1, len(self.loop_bounds)):
                        print "           }"

                    print "        }"

                elif (self.dependence_vector[x] < 0):
                    print "        for(" + x  + "=start[" + y + "]; " + x + ">= max(start[" + y + "]+dep_dist[" + y + "]+1,lower_loop_bounds[" + b +"]); " + x + "--)"
                    print "        {"

                    for k in range(i):
                        a = self.loop_bounds[k][0]
                        b = str(k)
                        if (self.dependence_vector[a] > 0):
                            print "           for(" + a + "=start[" + b + "]+dep_dist[" + b + "]; " + a + "<=loop_bounds[" + b + "]; " + a + "++)"
                            print "           {"
                        elif (self.dependence_vector[a] == 0):
                            print "           for(" + a + "=start[" + b + "]; "+ a + " <= loop_bounds[" + b + "]; " + a + "++)"
                            print "           {"
                        else:
                            print "           for(" + a + "=start[" + b + "]+ dep_dist[" + b + "]; " + a + ">= lower_loop_bounds[" + b + "];" + a + "--)"
                            print "           {"

                    for m in range(i+1, len(self.loop_bounds)):
                        a = self.loop_bounds[m][0]
                        b = str(m)
                        if (self.dependence_vector[a] > 0):
                            print "           for(" + a + "=start[" + b + "]; " + a + "<=loop_bounds[" + b + "]; " + a + "++)"
                            print "           {"
                        elif (self.dependence_vector[a] == 0):
                            print "           for(" + a + "=start[" + b + "]; "+ a + " <= loop_bounds[" + b + "]; " + a + "++)"
                            print "           {"
                        else:
                            print "           for(" + a + "=start[" + b + "]; " + a + ">= lower_loop_bounds[" + b + "];" + a + "--)"
                            print "           {"

                    for l in range(len(self.code_lines)):
                        print "               " + self.code_lines[l]

                    for k in range(i):
                        print "           }"

                    for m in range(i+1, len(self.loop_bounds)):
                        print "           }"

                    print "        }"

        print "    }"
        print ""

        # Print lines from the print_lines file for checking the output
        print_lines = open("../input/print_lines",'r')

        for lines in print_lines.readlines():
            print "    " + str(lines.rstrip())

        print ""

        # End of main function
        print "    return 0;"
        print ""
        print "}"

if (__name__ == '__main__'):

    path = "../input/input"
    list_input_num = reading_input(path)
    [m, loop_bounds, p, pairs, code_lines] = distributing_input_list(list_input_num)

    cd = ConstantDistance(m, p, pairs)
    data_dependence_vector = cd.data_dependence()
    dependence_distance_vector = cd.dependence_distance(data_dependence_vector)

    pc = ParallelCode(loop_bounds, dependence_distance_vector, code_lines)
    partition_no = pc.partition_num()
    pc.generate_code(partition_no)
