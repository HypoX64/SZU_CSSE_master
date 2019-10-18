#include <semaphore.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>

int main(int argc,char **argv)
{
    sem_t *sem;
    int val;
    if(argc!=2)
    {
        printf("please input a file name!\n");
        exit(1);
    }
    sem=sem_open(argv[1],0);    //获取信号量对象
    sem_wait(sem);              //执行 P 操作(-1 操作)
    sem_getvalue(sem,&val);     //获得出当前信号量的值
    printf("pid %ld has semaphore,value=%d\n",(long)getpid(),val);
    return 0;
}
