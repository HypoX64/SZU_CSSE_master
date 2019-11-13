#include <fcntl.h>
#include <sys/mman.h>
#include <stdio.h>
#include <string.h>

int main()
{
    int fd;
    void *start_addr;
    struct stat sb;
    char str1[]="Modification in the memory---------";
    fd = open("./file-mapped.txt", O_RDWR); //打开./file-mapped.text
    fstat(fd, &sb);// 取得文件大小

    start_addr = mmap(NULL, sb.st_size, PROT_READ|PROT_WRITE, MAP_SHARED, fd, 0);
    if(start_addr == MAP_FAILED)// 判断是否映射成功

        return;
    printf("Mapped area stared by addr:%p:\n%s\n", start_addr,start_addr);
    getchar();
    strcpy(start_addr,str1);//修改共享内存区

    printf("Write string into the mapped area!\n");
    getchar();
    munmap(start_addr, sb.st_size);//解除映射

    close(fd);
    return 0;
}