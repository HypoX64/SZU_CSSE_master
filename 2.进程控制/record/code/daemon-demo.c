#include <unistd.h>
#include <signal.h>
#include <fcntl.h>
#include <sys/syslog.h>
#include <sys/param.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
int init_daemon(void)
{
    int pid;
    int i;
    // 1）忽略一些控制终端发来的信号,信号的内容请参考其他文献
    signal(SIGTTOU,SIG_IGN);
    signal(SIGTTIN,SIG_IGN);
    signal(SIGTSTP,SIG_IGN);
    signal(SIGHUP ,SIG_IGN);
    // 2）在后台运行
    if( pid=fork() )
    {   // 父进程
        exit(0); //结束父进程，子进程继续
    }
    else if(pid< 0)
    {   // 出错
        perror("fork");
        exit(EXIT_FAILURE);
    }
    // 3）脱离控制终端、登录会话和进程组
    setsid();
    // 4）禁止进程重新打开控制终端
    if( pid=fork() )
    { // 父进程
        exit(0); // 结束第1 代子进程，第2 代子进程继续（第2 代子进程不再是会话组长）
    }
    else if(pid< 0)
    { // 出错
        perror("fork");
        exit(EXIT_FAILURE);
    }
    // 5）关闭打开的文件描述符
    // NOFILE 为文件描述符最大个数，不同系统有不同限制,<sys/param.h> 的宏定义
    for(i=0; i< NOFILE; ++i)
    {
        close(i);
    }
    // 6）改变当前工作目录
    chdir("/tmp");
    // 7）重设文件创建掩模
    umask(0);
    // 8）处理 SIGCHLD 信号
    signal(SIGCHLD,SIG_IGN);
    // 9) 输出日志
    openlog("daemon-demo.log",LOG_PID,0);
    syslog(LOG_INFO,"daemon-demo is running ...\n");
    return 0;
}
int main(int argc, char *argv[])
{
    init_daemon();
    while(1);
    return 0;
}