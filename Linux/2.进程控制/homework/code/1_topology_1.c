#include <stdio.h>
#include <unistd.h>
//1_topology_1───10*[1_topology_1]
int main(int argc, char ** argv )
{   
    int i = 0;
    for (i = 0; i < 10; ++i)
    {
        int pid = fork();
        if(pid == -1) 
        {
            printf("error!\n");
        } 
        else if(pid ==0) 
        {
            printf("This is the child process %d!\n",i);
            getchar();
        } 
    }
    {
        printf("This is the parent process!");
        getchar();
        wait(NULL);
    }
    return 0;
}