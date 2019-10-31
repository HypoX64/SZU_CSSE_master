#include <semaphore.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <string.h>

#define BUFSZ 4096

int main(int argc,char **argv)
{
    int shm_id;
    char * shm_buf;
    sem_t *sem;
    int val;

    //映射共享内存到进程空间
    shm_id = atoi(argv[1]);
    if ( (shm_buf = shmat( shm_id, 0, 0)) < (char *) 0 ){
        perror ( "shmat fail!\n" );
        exit (1);
    }
    printf ( " segment attached at %p\n", shm_buf );

    sem=sem_open("flag",0);   //获取信号量对象

    int i =0;
    for (i = 0; i < 2; ++i)
    {
        int pid = fork(); //fork 
        if(pid == -1) 
        {
            printf("fork error!\n");
        } 
        else if(pid == 0) //fork 
        {
            while(1)
            {
                if (sem_getvalue(sem,&val)|val) //同步
                {
                    printf("Comsumer %d Get message:%s\n",i,shm_buf); //将共享内存区的内容打印出来
                    if ( (shmdt(shm_buf)) < 0 ) //解除共享内存的映射
                    { 
                        perror ( "shmdt");
                        exit(1);
                    }
                    sem_wait(sem);//-1
                }
                sleep(1);
            }
        }
        usleep(500000); 
    }

    getchar();

}