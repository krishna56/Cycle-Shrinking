#include<iostream>

using namespace std;

int main()
{
    int A[13][12];
    int B[12][11];
    int length=2;

    int loop_bounds[]= {
    10,
    8,
    };

    int dep_dist[] = {
    2,
    3,
    };

    int partition_no=2.0;

    for(int part=1; part<partition_no; part++)
    {
        int start[length];

        #pragma omp parallel for shared(dep_dist)
        for(int h=0; h<length; h++)
        {
            if (dep_dist[h] >= 0) { start[h] = 1+(part-1)*dep_dist[h]; } 
            else { start[h] = loop_bounds[h]-(part-1)*dep_dist[h]; } 
        }

        #pragma omp parallel for private(J) shared(loop_bounds,dep_dist)
        for(int I=start[0]; I<= min(start[0]+dep_dist[0]-1,loop_bounds[0]); I++)
        {
           for(int J=start[1]; J<=loop_bounds[1]; J++)
           {
               A[I+3][J+4] = B[I][J];
               B[I+2][J+3] = A[I][J];
           }
        }
        #pragma omp parallel for private(I) shared(loop_bounds,dep_dist)
        for(int J=start[1]; J<= min(start[1]+dep_dist[1]-1,loop_bounds[1]); J++)
        {
           for(int I=start[0]+dep_dist[0]; I<=loop_bounds[0]; I++)
           {
               A[I+3][J+4] = B[I][J];
               B[I+2][J+3] = A[I][J];
           }
        }
   }
}
