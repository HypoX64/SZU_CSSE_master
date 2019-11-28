#include <stdio.h>
#include <sys/mman.h>
#include <stdlib.h>
#include <fcntl.h>
#define MB 1024*1024
#define KB 1024
int main()
{
    int i,j;
    char temp;
    int fd= -1;
    char * filemap_buf;
    char * anon_buf;
    printf("-----\n");
    getchar(); // checkpoint 1 initial state


    //第二步将在进程初始布局之上，创建两个新的内存区间，一个是8MB 的文件映射,一个是16MB 的非文件映射（匿名）区间。
    if((fd=open("/home/hypo/tempfile",O_RDWR))<0)
        printf("open tmpfile err!\n");
    if((filemap_buf=(char*)mmap(NULL,8*MB,PROT_READ|PROT_WRITE,MAP_SHARED,fd,0))==MAP_FAILED)
        printf("mmap fail!\n");
    anon_buf=(char *)malloc(16*MB);
    printf("allocated/mmapped\n");
    printf("filemapped @ %p \n",filemap_buf);
    printf("anon @ %p \n",anon_buf);
    getchar(); // checkpoint 2 allocation

    //第三步将在上述进程布局之上，对文件映射区间的前4MB 和匿名区间的前8MB 进行读操作。
    for (i=0;i<4*MB;i+=4096)
        temp=filemap_buf[i];
    for(i=0;i<8*MB;i+=4096)
        temp=*(anon_buf+i);
    printf("read finish\n ");
    getchar(); // checkpoint 3 read finish

    //第四步在上述进程布局之上，对文件映射区间的前2MB 和匿名区间的前4MB 进行写操作
    for(i=0;i<2*MB;i+=4096)
        filemap_buf[i]=temp;
    for(i=0;i<4*MB;i+=4096)
        anon_buf[i]=0xaa;
    printf("write finish \n");
    getchar(); // checkpoint 4 write finish/make the pageframes dirty
    
    //最后将通过unmap()和free()释放文件映射区和匿名内存区。
    munmap(filemap_buf,8*MB);
    free(anon_buf);
    printf("all done \n");
    getchar(); // checkpoint 5
    return 0;
}