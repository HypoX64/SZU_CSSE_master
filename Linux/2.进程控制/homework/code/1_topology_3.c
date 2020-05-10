#include <stdio.h>
#include <unistd.h>
/*
  |   |   `-1_topology_3
  |   |       |-1_topology_3
  |   |       |   |-1_topology_3
  |   |       |   |   |-1_topology_3
  |   |       |   |   `-1_topology_3
  |   |       |   `-1_topology_3
  |   |       |       |-1_topology_3
  |   |       |       `-1_topology_3
  |   |       `-1_topology_3
  |   |           |-1_topology_3
  |   |           |   |-1_topology_3
  |   |           |   `-1_topology_3
  |   |           `-1_topology_3
  |   |               |-1_topology_3
  |   |               `-1_topology_3
  |   |   |-grep --color=auto 1_topology_3

*/
void btree_fork(num)
{
    num--;
    if (num != -1)
    {
        int j = 0;
        for (j = 0; j < 2; ++j)
        {
            int pid = fork();
            if(pid == -1) 
            {
                printf("error!\n");
            } 
            else if(pid ==0) 
            {
                printf("This is the child process %d_%d\n",j);
                btree_fork(num);
                getchar();
            } 
        }

    }
}

int main(int argc, char ** argv )
{   
    int i = 0;
    btree_fork(3);
    {
        printf("This is the parent process!\n");
        getchar();
        wait(NULL);
    }
    return 0;
}