#include<iostream>

using namespace std;

int main()
{
    int A[13][10];
    int B[12][10];
    int length=2;

    int lower_loop_bounds[] = {
    1,
    4,
    };

    int loop_bounds[] = {
    10,
    10,
    };

    int dep_dist[] = {
    2,
    -2,
    };

    int partition_no=3.0;

    for(int part=1; part<partition_no; part++)
    {
        int start[length];

        #pragma omp parallel for shared(dep_dist)
        for(int h=0; h<length; h++)
        {
            if (dep_dist[h] >= 0) { start[h] = lower_loop_bounds[h] +(part-1)*dep_dist[h]; } 
            else { start[h] = loop_bounds[h]-(part-1)*dep_dist[h]; } 
        }

        #pragma omp parallel for private(j) shared(loop_bounds,dep_dist)
        for(int i=start[0]; i<= min(start[0]+dep_dist[0]-1,loop_bounds[0]); i++)
        {
           for(int j=start[1]; j<=loop_bounds[1]; j++)
           {
               A[i+3][j-3] = B[i][j];
               B[i+2][j-2] = A[i][j];
           }
        }
        #pragma omp parallel for private(i) shared(loop_bounds,dep_dist)
        for(int j=start[1]; j<= max(start[1]+dep_dist[1]+1,1); j--)
        {
           for(int i=start[0]+dep_dist[0]; i<=loop_bounds[0]; i++)
           {
               A[i+3][j-3] = B[i][j];
               B[i+2][j-2] = A[i][j];
           }
        }
   }
}
