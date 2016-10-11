"""
    This code takes an input code and generates suitable output to generate parallel code
"""

def read_serial_code(filepath):

    input_file = open(filepath,'r')
    input_lines = []

    for lines in input_file.readlines():
        lines = lines.strip()
        if (lines != '}') and (lines != '{') and (lines != "") and (lines != ""):
            input_lines.append(lines)

    print input_lines
    for_lines = []
    other_lines = []

    for i in input_lines:
        x = i.split('(')
        if (x[0]=='for' or x[0]=='for '):
            for_lines.append(i)
        else:
            other_lines.append(i)

    print for_lines
    print other_lines



if __name__ == '__main__' :

    read_serial_code('serial.cpp')




