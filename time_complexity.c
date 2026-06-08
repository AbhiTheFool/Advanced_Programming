#include <stdio.h>
#include <time.h>

int main()
{
    int n, i, j;
    clock_t start, end;
    double time_taken;
    int x = 0;

    printf("Enter input size: ");
    scanf("%d", &n);

    start = clock();
    x = n * n;
    end = clock();
    time_taken = ((double)(end - start)) / CLOCKS_PER_SEC;
    printf("Constant Time: %f seconds\n", time_taken);

    start = clock();
    for(i = 0; i < n; i++)
        x = x + i;
    end = clock();
    time_taken = ((double)(end - start)) / CLOCKS_PER_SEC;
    printf("Linear Time: %f seconds\n", time_taken);

    start = clock();
    for(i = 0; i < n; i++)
        for(j = 0; j < n; j++)
            x = x + i + j;
    end = clock();
    time_taken = ((double)(end - start)) / CLOCKS_PER_SEC;
    printf("Quadratic Time: %f seconds\n", time_taken);

    return 0;
}
