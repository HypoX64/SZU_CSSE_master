#include <semaphore.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <string.h>

int main(int argc, char **argv)
{

    int pfds[2];
    pid_t pid1, pid2, wpid;
    pipe(pfds);
    char buf[1024];
    int nwr = 0;
    int status;
    pid1 = fork();
    if (pid1 < 0) 
    {
        printf("fork error!\n");
    } 
    else if (pid1 == 0)
     {  
        
        // STDIN_FILENO：接收键盘的输入
        // STDOUT_FILENO：向屏幕输出
        // dup2 把 pfds[1](管道数据入口描述符) 复制到 文件描述符1&2
        // 实现把pid1的标准输出和标准错误 输送到管道
         
        dup2(pfds[1], STDOUT_FILENO);
        dup2(pfds[1], STDERR_FILENO);
        close(pfds[0]);
        close(pfds[1]);

        char *args[]={"ls",NULL};
        execvp(args[0], args);
        exit(0);
    }

    pid2 = fork();
    if (pid2< 0) 
    {
        printf("error!\n");
    } 
    else if (pid2 == 0){
        
        //dup2 把 pfds[0](管道数据出口描述符) 复制到 文件描述符0
        //实现pid2从管道中读取(pid1的输出)数据        
        dup2(pfds[0], STDIN_FILENO);
        close(pfds[0]);
        close(pfds[1]);

        char *args[]={"more",NULL};
        execvp(args[0], args);
        exit(0);
    }

    close(pfds[0]);
    close(pfds[1]);
    do 
    {
        wpid = waitpid(pid2,&status,WUNTRACED);
    }
    while (!WIFEXITED(status) && !WIFSIGNALED(status));

}
