#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
void thread(void)
{
    printf("This is a pthread.\n");
    sleep(10);
}
int main(void)
{
    pthread_t id[100];
    int i,ret;
    for(i=0;i<100;i++)
    {
        ret=pthread_create(&id[i],NULL,(void *) thread,NULL);
        if(ret!=0)
        {
        printf ("Create pthread error!\n");
        exit (1);
        }
    }
    printf("This is the main process.\n");
    for(i=0;i<100;i++)
    {
        pthread_join(id[i],NULL);
    }
    return (0);
}