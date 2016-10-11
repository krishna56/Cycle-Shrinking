"""
    Parallel code generation using cycle shrinking for constant distance
"""

import math
from const_dist import ConstantDistance
from const_dist import reading_input
from const_dist import distributing_input_list

class ParallelCode:

    def __init__(self, loop_bounds=[], dependence_vector={}, code_lines=[]):
        self.loop_bounds = loop_bounds
        self.code_lines = code_lines
        self.dependence_vector = dependence_vector

    def partition_num(self):
        partition_no=[]

        for i in range(len(self.loop_bounds)):
            x = abs(self.dependence_vector[self.loop_bounds[i][0]])
            temp = math.ceil(self.loop_bounds[i][1]/x)
            partition_no.append(temp)

        return min(partition_no)

    def generate_code(self, partition_no):

        initialization = []
        other_lines = []

        for i in range(len(code_lines)):
            temp = code_lines[i].split(" ")
            if (temp[0] == 'int'):
                initialization.append(code_lines[i])
            else:
                other_lines.append(code_lines[i])

        print "#include<iostream>"
        print ""
        print "using namespace std;"
        print ""
        print "int main()"
        print "{"

        for i in range(len(initialization)):
            print "    " + initialization[i] + ";"

        print "    int length=" + str(len(self.loop_bounds)) + ";"
        print ""
        print "    int loop_bounds[]= {"

        for i in range(len(self.loop_bounds)):
            print "    " + str(self.loop_bounds[i][1]) + ","

        print "    };"
        print ""
        print "    int dep_dist[] = {"

        for i in range(len(self.loop_bounds)):
            print "    " + str(self.dependence_vector[self.loop_bounds[i][0]]) + ","

        print "    };"
        print ""
        print "    int partition_no=" + str(partition_no) + ";"
        print ""
        print "    for(int part=1; part<partition_no; part++)"
        print "    {"
        print "        int start[length];"
        print ""
        print "        #pragma omp parallel for shared(dep_dist)"
        print "        for(int h=0; h<length; h++)"
        print "        {"
        print "            if (dep_dist[h] >= 0) { start[h] = 1+(part-1)*dep_dist[h]; } "
        print "            else { start[h] = loop_bounds[h]-(part-1)*dep_dist[h]; } "
        print "        }"
        print ""

        for i in range(len(self.loop_bounds)):
            if (self.dependence_vector[self.loop_bounds[i][0]] != 0):
                temp = ""
                st = ""

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
                    print "        for(int " + x  + "=start[" + y + "]; " + x + "<= min(start[" + y + "]+dep_dist[" + y + "]-1,loop_bounds[" + y + "]); " + x + "++)"
                    print "        {"

                    for k in range(i):
                        a = self.loop_bounds[k][0]
                        b = str(k)
                        if (self.loop_bounds[k][1] > 0):
                            print "           for(int " + a + "=start[" + b + "]+dep_dist[" + b + "]; " + a + "<=loop_bounds[" + b + "]; " + a + "++)"
                            print "           {"
                        else:
                            print "           for(int " + a + "=start[" + b + "]+ dep_dist[" + b + "]; " + a + ">= 1; " + a + "--)"
                            print "           {"

                    for m in range(i+1, len(self.loop_bounds)):
                        a = self.loop_bounds[m][0]
                        b = str(m)
                        if (self.loop_bounds[m][1] > 0):
                            print "           for(int " + a + "=start[" + b + "]; " + a + "<=loop_bounds[" + b + "]; " + a + "++)"
                            print "           {"
                        else:
                            print "           for(int " + a + "=start[" + b + "]; " + a + ">= 1; " + a + "--)"
                            print "           {"

                    for l in range(len(other_lines)):
                        print "               " + other_lines[l] + ";"

                    for k in range(i):
                        print "           }"

                    for m in range(i+1, len(self.loop_bounds)):
                        print "           }"

                    print "        }"
                else:
                    print "        for(int " + x  + "=start[" + y + "]; " + x + "<= max(start[" + y + "]+dep_dist[" + y + "]+1,1); " + x + "--)"
                    print "        {"

                    for k in range(i):
                        a = self.loop_bounds[k][0]
                        b = str(k)
                        if (self.loop_bounds[k][1] > 0):
                            print "           for(int " + a + "=start[" + b + "]+dep_dist[" + b + "]; " + a + "<=loop_bounds[" + b + "]; " + a + "++)"
                            print "           {"
                        else:
                            print "           for(int " + a + "=start[" + b + "]+ dep_dist[" + b + "]; " + a + ">= 1; " + a + "--)"
                            print "           {"

                    for m in range(i+1, len(self.loop_bounds)):
                        a = self.loop_bounds[m][0]
                        b = str(m)
                        if (self.loop_bounds[m][1] > 0):
                            print "           for(int " + a + "=start[" + b + "]; " + a + "<=loop_bounds[" + b + "]; " + a + "++)"
                            print "           {"
                        else:
                            print "           for(int " + a + "=start[" + b + "]; " + a + ">= 1; " + a + "--)"
                            print "           {"

                    for l in range(len(self.code_lines)):
                        print "               " + code_lines[l]

                    for k in range(i):
                        print "           }"

                    for m in range(i+1, len(self.loop_bounds)):
                        print "           }"

                    print "        }"

        print "   }"
        print "}"

if (__name__ == '__main__'):

    list_input_num = reading_input()
    [m, loop_bounds, p, pairs, code_lines] = distributing_input_list(list_input_num)

    cd = ConstantDistance(m, p, pairs)
    data_dependence_vector = cd.data_dependence()
    dependence_distance_vector = cd.dependence_distance(data_dependence_vector)

    pc = ParallelCode(loop_bounds, dependence_distance_vector, code_lines)
    partition_no = pc.partition_num()
    pc.generate_code(partition_no)
