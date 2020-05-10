#include <stdio.h>
#include <unistd.h>
int main(int argc, char ** argv )
{
    int i;
    for(i=0;i<100;i++)
    {
        int pid = fork();
        if(pid == -1 ) 
        {
            printf("error!\n");
        } 
        else if( pid ==0 ) 
        {
            printf("This is the child process!\n");
            sleep(10);
            return 0;
        } 
        else 
        {
            printf("This is the parent process! child process id = %d\n", pid);
        }
    }
    sleep(10);
    return 0;
}