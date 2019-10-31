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
    char sf[100];
    sem_t *sem;
    int val;

    //创建共享内存
    shm_id=shmget(0, BUFSZ, 0666 ) ;
    if (shm_id < 0 )
    {
        perror( "shmget fail!\n" ) ;
        exit ( 1 );
    }
    printf ("Successfully created segment : %d \n", shm_id) ;
    // system("ipcs -m");  

    //映射共享内存到进程空间
    if ( (shm_buf = shmat( shm_id, 0, 0)) < (char *) 0 ){
        perror ( "shmat fail!\n" );
        exit (1);
    }
    printf ( " segment attached at %p\n", shm_buf );
    // system("ipcs -m");  

    //创建一个命名的 flag　的信号量
    sem=sem_open("flag",O_CREAT,0644,1);
    // sem_wait(sem);              //执行 P 操作(-1 操作)

    while(1){
        printf(">>");
        scanf("%s",&sf);
        if (sem_getvalue(sem,&val)|val){
            printf("Please wait comsumer.\n");
        }
        else{
            strcpy(shm_buf,sf);
            sem_post(sem);  //对信号量执行 P 操作(增 1)
            // sem_getvalue(sem,&val);
            // printf("value=%d\n", val);
        }

    }
}