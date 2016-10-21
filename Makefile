all:
	python parallel_code_generation.py > output_parallel_code.cpp
	
.PHONY: clean
clean:
	rm const_dist.pyc output_parallel_code.cpp 


