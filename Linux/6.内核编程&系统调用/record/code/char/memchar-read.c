#include <stdio.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdlib.h>

char buf_in[1024];

int main()
{
    int fd;
    fd=open("/dev/memchar",O_RDWR|O_CREAT,0666);
    if(fd==-1)
    { 
        perror("open file mytest");
        exit(1);
    }
    read(fd,buf_in,1024);
    printf("retrieved message is : %s !\n",buf_in);
    close(fd);
    return 0;
}