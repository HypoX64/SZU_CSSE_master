#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
int main ( int argc, char *argv[] )
{
    int shm_id ;
    char * shm_buf;
    if ( argc != 2 ){
        printf ( "USAGE: atshm <identifier>" );
        exit (1 );
    }
    shm_id = atoi(argv[1]);
    if ( (shm_buf = shmat( shm_id, 0, 0)) < (char *) 0 ){
        perror ( "shmat fail!\n" );
        exit (1);
    }
    printf ( " segment attached at %p\n", shm_buf );
    system("ipcs -m");
    printf("The string in SHM is :%s\n",shm_buf); //将共享内存区的内容打印出来
    getchar();
    if ( (shmdt(shm_buf)) < 0 ) {
        perror ( "shmdt");
        exit(1);
    }
    printf ( "segment detached \n" );
    system ( "ipcs -m " );
    getchar();
    exit ( 0 );
}