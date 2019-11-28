#include <stdio.h>
#include <sys/mman.h>
#include <stdlib.h>
#include <fcntl.h>
#define MB 1024*1024
#define KB 1024
int main()
{
    int i,pid;
    char temp;
    int fd= -1;
    char *filemap_buf;
    char command_smaps[100];
    char command_status[100];
    char command_meminfo[100];
    char command_maps[100];
    char * anon_buf;
    pid=getpid();
    sprintf(command_smaps,"cat /proc/%d/smaps > smaps-check",pid);
    sprintf(command_status,"cat /proc/%d/status > status-check",pid);
    sprintf(command_meminfo,"cat /proc/meminfo >meminfo-check");
    sprintf(command_maps,"cat /proc/%d/maps >maps-check",pid);

    //在进程初始布局之上，创建两个新的内存区间，一个是8MB 的文件映射，一个是16MB 的非文件映射（匿名）区间。各自用mlock()函数锁定8KB 和16KB 的空间（不可换出）
    if((fd=open("/home/hypo/tempfile",O_RDWR))<0)
        printf("open tmpfile err!\n");
    if((filemap_buf=(char *) mmap(NULL, 8*MB, PROT_READ|PROT_WRITE, MAP_SHARED,fd,0)) ==MAP_FAILED )
        printf("mmap fail!\n");
    mlock(filemap_buf,8*KB);
    anon_buf=(char *)malloc(16*MB);
    mlock(anon_buf,16*KB);
    printf("allocated/mmapped\n");
    printf("filemapped @ %p \n",filemap_buf);
    printf("anon @ %p \n",anon_buf);
    system(command_maps);
    system(command_smaps);
    system(command_status);
    system(command_meminfo);
    getchar(); // checkpoint 1 allocation

    //对文件映射区间的前4MB 和匿名区间的前8MB 进行读和写操作各一遍。
    for(i=0;i<4*MB;i+=4096)
    filemap_buf[i]=temp;
    for(i=0;i<8*MB;i+=4096)
    anon_buf[i]=0xaa;
    printf("write finish \n");
    system(command_smaps);
    system(command_status);
    system(command_meminfo);
    getchar(); // checkpoint 2 write finish/make the pageframes dirty

    //run pages-blackhole-demo.c
    //该pagesblackhole-demo 进程将大量消耗物理页帧，因此会引起reclaim-swap-writeback-demo进程的页帧被回收
    printf("please run pages-blackhole-demo\n");
    getchar(); // checkpoint 3 be swapped out  
    system(command_smaps);
    system(command_status);
    system(command_meminfo);
    getchar();

    //最后将通过对文件映射区间的前4MB 和匿名区间的前8MB 进行反复的读写操作。可以检查该进程重新获得物理页帧的现象。
    printf("compete for the page frames\n");
    while(1) //compete for the page frames, by writing
    { 
        for(i=0;i<1*MB;i+=4096)
            filemap_buf[i]=temp;
        for(i=0;i<2*MB;i+=4096)
            anon_buf[i]=0xaa;
    }
    getchar(); // checkpoint 4 will never get to this point
    
    munmap(filemap_buf,8*MB);
    free(anon_buf);
    return 0;
}