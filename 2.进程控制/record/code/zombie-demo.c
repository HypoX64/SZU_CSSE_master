#include <sys/types.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
main()
{
    pid_t pid;
    pid = fork();
    if(pid < 0)
        printf("error occurred!\n");
    else if(pid == 0) 
    {
        printf("Hi father! I'm a ZOMBIE\n");
        exit(0); //no one waits for this process.
    }
    else 
    {
        sleep(10);
        wait(NULL); //the zombie process will be reaped now.
    }
}