#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
void thread(void)
{
    // int i = 0;
    printf("This is a pthread. address is %p\n", &thread);
    sleep(10);
}
int main(void)
{
    pthread_t id[10];
    int i,ret;
    for(i=0;i<10;i++)
    {
        ret=pthread_create(&id[i],NULL,(void *) thread,NULL);
        if(ret!=0)
        {
        printf ("Create pthread error!\n");
        exit (1);
        }
    }
    printf("This is the main process.address is %p\n", &main);
    for(i=0;i<10;i++)
    {
        pthread_join(id[i],NULL);
    }
    return (0);
}