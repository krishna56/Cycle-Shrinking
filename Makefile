

all: build 
	
.PHONY: clean build docs install tests cleanall

docs: install
	cd docs; make html

install:
	sudo python setup.py install

build:
	cd constant_distance; python parallel_code_generation.py > ../result/parallel_code.cpp

clean: build 
	cd result; rm -rf *.cpp
	cd constant_distance; rm -rf *.pyc

cleanall: tests build clean
	cd tests; rm -rf *.pyc
	cd input; rm -f a.out serial_code_result
	cd result; rm -f a.out parallel_code_result

tests: install build
	cd result; g++ parallel_code.cpp; ./a.out > parallel_code_result
	cd input; g++ serial_code.cpp; ./a.out > serial_code_result
	cd tests; nosetests



