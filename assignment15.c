#include <stdio.h>
#include <pthread.h>

#define NUM_THREADS 4
#define INCREMENTS 1000000

long long counter = 0;

pthread_mutex_t lock;

void* increment_without_mutex(void* arg)
{
    for (int i = 0; i < INCREMENTS; i++)
    {
        counter++;
    }

    return NULL;
}

void* increment_with_mutex(void* arg)
{
    for (int i = 0; i < INCREMENTS; i++)
    {
        pthread_mutex_lock(&lock);
        counter++;
        pthread_mutex_unlock(&lock);
    }

    return NULL;
}

int main()
{
    pthread_t threads[NUM_THREADS];

    counter = 0;

    printf("WITHOUT MUTEX\n");

    for (int i = 0; i < NUM_THREADS; i++)
    {
        pthread_create(&threads[i], NULL,
                       increment_without_mutex, NULL);
    }

    for (int i = 0; i < NUM_THREADS; i++)
    {
        pthread_join(threads[i], NULL);
    }

    printf("Expected Counter = %lld\n",
           (long long)NUM_THREADS * INCREMENTS);

    printf("Actual Counter   = %lld\n\n", counter);

    counter = 0;

    pthread_mutex_init(&lock, NULL);

    printf("WITH MUTEX\n");

    for (int i = 0; i < NUM_THREADS; i++)
    {
        pthread_create(&threads[i], NULL,
                       increment_with_mutex, NULL);
    }

    for (int i = 0; i < NUM_THREADS; i++)
    {
        pthread_join(threads[i], NULL);
    }

    printf("Expected Counter = %lld\n",
           (long long)NUM_THREADS * INCREMENTS);

    printf("Actual Counter   = %lld\n", counter);

    pthread_mutex_destroy(&lock);

    return 0;
}
