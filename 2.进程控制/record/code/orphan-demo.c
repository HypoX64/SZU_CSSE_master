#include <stdio.h>
#include <unistd.h>
int main(int argc, char ** argv )
{
    int pid = fork();
    if(pid == -1) 
    {
        printf("error!\n");
    } 
    else if(pid ==0) 
    {
        printf("This is the child process!\n");
        getchar();
    } 
    else 
    {
        printf("This is the parent process! child process id = %d\n", pid);
        getchar();
        // wait(NULL);
    }
    return 0;
}