#include <sched.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>

int main(int argc,char ** argv)
{
    long i,j,temp;
    char cmd_str[100];
    int rc,current_scheduler_policy;
    struct sched_param my_params;
    //将要设置的调度参数
    if(argc!=3)
    {
        printf("usage:RR-FIFO-sched sched_class priority \nsched_class: 0 for CFS; 1 forFIFO; 2 for RR\n");
        exit(1);
    }
    my_params.sched_priority=atoi(argv[2]);
    rc=sched_setscheduler(0,atoi(argv[1]),&my_params);
    if(rc<0)
    {
        perror("sched_setscheduler error\n");
        exit(0);
    }
    current_scheduler_policy=sched_getscheduler(0);
    printf("the PID:%d current scheduler = %d \n", getpid(),current_scheduler_policy);
    for(i=0;i<1024*1024*1024;i++)
        for(j=0;j<10;j++)
            temp++;
    sprintf(cmd_str,"cat /proc/%d/sched > ./sched-%d ; date >> ./sched-%d", getpid(),
    getpid(), getpid());
    system(cmd_str);
    //记录各个进程的/proc/PID/sched 以及时间信息
    return 0;
}