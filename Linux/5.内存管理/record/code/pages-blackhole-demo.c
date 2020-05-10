#include <stdio.h>
#include <sys/mman.h>
#include <stdlib.h>
#include <fcntl.h>
#define MB 1024*1024
int main()
{
    int i,j;
    char temp;
    int fd= -1;
    char * filemap_buf;
    char * anon_buf;
    anon_buf=(char *)malloc(2000*MB);
    while(1)
    { 
        for(i=0;i<2000*MB;i+=4096)
            anon_buf[i]=0xaa;
        sleep(1);
    }
    return 0;
}