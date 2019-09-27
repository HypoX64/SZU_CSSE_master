#include <stdio.h>
#include <unistd.h>
int main(int argc, char ** argv )
{
    int pid = fork();
    if(pid == -1 ) 
    {
        printf("error!\n");
    } 
    else if( pid ==0 ) 
    {
        printf("This is the child process!\n");
        char *argv[ ]={"ls", "-al", "/etc/passwd", NULL};
        char *envp[ ]={"PATH=/usr/bin", NULL};
        execve("/usr/bin/ls", argv, envp);
        printf("this printf() will not be executed,because it will be replaced by /usr/bin/ls code!\n");
    } 
    else 
    {
        printf("This is the parent process! child process id = %d\n", pid);
        getchar();
    }
    return 0;
}