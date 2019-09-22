#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <execinfo.h>
#include <unistd.h>

void my_backtrace()
{
    void *buffer[100] = { NULL };
    char **trace = NULL;

    int size = backtrace(buffer, 100);
    trace = backtrace_symbols(buffer, size);
    if (NULL == trace) {
        return;
    }
    for (int i = 0; i < size; ++i) {
        printf("%s\n", trace[i]);
    }
    free(trace);
    printf("----------done----------\n");
}

void thread(void)
{
    // int i = 0;
    my_backtrace();
    printf("This is a pthread");
    sleep(10);
}
int main(void)
{
    pthread_t id[3];
    int i,ret;
    for(i=0;i<3;i++)
    {
        ret=pthread_create(&id[i],NULL,(void *) thread,NULL);
        if(ret!=0)
        {
        // printf ("Create pthread error!\n");
        exit (1);
        }
    }
    // printf("This is the main process.");
    my_backtrace();
    for(i=0;i<10;i++)
    {
        pthread_join(id[i],NULL);
    }
    return (0);
}