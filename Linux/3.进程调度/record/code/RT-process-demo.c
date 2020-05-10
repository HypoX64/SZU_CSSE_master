#include <sched.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>


int main()
{
    int rc,current_scheduler_policy;
    struct sched_param my_params;
    //将要设置的调度参数
    current_scheduler_policy=sched_getscheduler(0);
    printf("SCHED_OTHER = %d SCHED_FIFO =%d SCHED_RR=%d \n", SCHED_OTHER, SCHED_FIFO,SCHED_RR);
    printf("the current scheduler = %d \n", current_scheduler_policy);
    printf("press any key to change the current scheduler and priority to SCHED_RR\n");
    getchar();
    //checkpoint 1
    my_params.sched_priority=sched_get_priority_max(SCHED_RR); // 最高的 RR 实时优先级
    rc=sched_setscheduler(0,SCHED_RR,&my_params);
    //设置为 RR 实时进程
    if(rc<0)
    {
        perror("sched_setscheduler to SCHED_RR error");
        exit(0);
    }
    current_scheduler_policy=sched_getscheduler(0);
    printf("the current scheduler = %d \n", current_scheduler_policy);
    printf("press any key to change the current scheduler and priority to SCHED_FIFO\n");
    getchar();
    //checkpoint 2
    my_params.sched_priority=sched_get_priority_min(SCHED_FIFO); // 最低 FIFO 实时优先级
    rc=sched_setscheduler(0,SCHED_FIFO,&my_params);
    //设置为 FIFO 实时进程
    if(rc<0)
    {
        perror("sched_setscheduler to SCHED_FIFO error");
        exit(0);
    }
    current_scheduler_policy=sched_getscheduler(0);
    printf("the current scheduler = %d \n", current_scheduler_policy);
    printf("press any key to ange the current scheduler and priority to SCHED_OTHER(CFS)\n");
    getchar();
    //checkpoint 3
    rc=sched_setscheduler(0,SCHED_OTHER,&my_params);
    //设置为普通进程 3
    if(rc<0)
    {
        perror("sched_setscheduler to SCHED_OTHER error");
        exit(0);
    }
    current_scheduler_policy=sched_getscheduler(0);
    printf("the current scheduler = %d \n", current_scheduler_policy);
    printf("press any key to exit\n");
    getchar();
    //checkpoint 4
    return 0;
}