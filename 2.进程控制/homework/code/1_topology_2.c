#include <stdio.h>
#include <unistd.h>
//1_topology_2───1_topology_2───1_topology_2───1_topology_2───1_topology_2───1_topology_2───1_topology_2───1_topology_2───1_topology_2───1_topology_2───1_topology_2
void recursive_fork(num)
{
    num--;
    if (num != -1)
    {
        int pid = fork();
        if(pid == -1) 
        {
            printf("error!\n");
        } 
        else if(pid ==0) 
        {
            printf("This is the child process %d!\n",num);
            recursive_fork(num);
            getchar();
        } 
    }
}

int main(int argc, char ** argv )
{   
    int i = 0;
    recursive_fork(10);
    {
        printf("This is the parent process!\n");
        getchar();
        wait(NULL);
    }
    return 0;
}