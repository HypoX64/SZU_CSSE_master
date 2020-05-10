#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
int main()
{
    pid_t pid = 0;
    int fds[2];
    char buf[128];
    int nwr = 0;
    pipe(fds);
    //在 fork()前执行
    pid = fork();
    if(pid < 0)
    {
        printf("Fork error!\n");
        return -1;
    }
    else if(pid == 0)
    {
        printf("This is child process, pid = %d\n", getpid());
        printf("Child:waiting for message...\n");
        close(fds[1]);
        //关闭写端 fds[1]
        nwr = read(fds[0], buf, sizeof(buf));
        //从读端 fds[0]读入数据
        printf("Child:received\"%s\"\n", buf);
    }
    else
    {
        printf("This is parent process, pid = %d\n", getpid());
        printf("Parent:sending message...\n");
        close(fds[0]);
        //关闭写端 fds[0]
        strcpy(buf, "Message from parent!");
        nwr = write(fds[1], buf, sizeof(buf));
        //往写端 fds[1]写出数据
        printf("Parent:send %d bytes to child.\n", nwr);
    }
    return 0;
}