#include <stdio.h>
#include <malloc.h>
#include <fcntl.h>
#include <string.h>
#include <sys/mman.h>


#define MB (1024*1024)

int main()
{
    int pid,i;
    char *buf;

    pid = getpid();
    printf("PID:%d\n",pid );

    buf=(char*)malloc(1024*MB);
    printf("addr_start:%p\n",buf);

    for(i=0;i<1024*MB;i++)
    {
        buf[i]=0xaa;
    }

    printf("addr_end:%p\n",&buf[i]);

    long size = &buf[i]-&buf[0];
    printf("malloc size:%dMB\n", size/MB);
    
  
    printf("please run pages-blackhole-demo\n");

    getchar();

    free(buf);
    return 0;
}