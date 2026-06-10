// Name - Abhishek Verma
// Roll No - CSB24072

#include <stdio.h>
#include <time.h>

void constantTime(int n)
{
    int a = n;
    a = a + 5;
}

void linearTime(int n)
{
    int sum = 0;

    for (int i = 0; i < n; i++)
    {
        sum = sum + i;
    }
}

void quadraticTime(int n)
{
    int count = 0;

    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < n; j++)
        {
            count++;
        }
    }
}

int main()
{
    int n;
    clock_t start, end;
    double time_taken;

    printf("Enter input size: ");
    scanf("%d", &n);

    start = clock();
    constantTime(n);
    end = clock();

    time_taken =
        (double)(end - start) / CLOCKS_PER_SEC;

    printf("Constant time: %lf sec\n",
           time_taken);

    start = clock();
    linearTime(n);
    end = clock();

    time_taken =
        (double)(end - start) / CLOCKS_PER_SEC;

    printf("Linear time: %lf sec\n",
           time_taken);

    start = clock();
    quadraticTime(n);
    end = clock();

    time_taken =
        (double)(end - start) / CLOCKS_PER_SEC;

    printf("Quadratic time: %lf sec\n",
           time_taken);

    return 0;
}
