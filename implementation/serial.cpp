for (int i=1; i<=10; i++)
{
    for (int j=1; j<=8; j++)
    {
        A[i+3][j+4] = B[i][j];
        B[i+2][j+3] = A[i][j];
    }
}


