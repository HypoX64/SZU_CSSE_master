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
    pthread_t id;
    int i,ret;
    ret=pthread_create(&id,NULL,(void *) thread,NULL);
    if(ret!=0)
    {
        printf ("Create pthread error!\n");
        exit (1);
    }
    printf("This is the main process.\n");
    pthread_join(id,NULL);
    return (0);
}