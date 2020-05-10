#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <stdlib.h>
#include <stdio.h>

#define BUFSZ 4096
int main ( void )
{
    int shm_id;
    shm_id=shmget(IPC_PRIVATE, BUFSZ, 0666 ) ;
    if (shm_id < 0 )
    {
        perror( "shmget fail!\n" ) ;
        exit ( 1 );
    }
    //创建共享内存
    printf ("Successfully created segment : %d \n", shm_id) ;
    system( "ipcs -m");
    //执行 ipcs –m 命令,显示系统的共享内存信息
    return 0;
}