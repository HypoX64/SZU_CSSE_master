#include <stdio.h>
#include <malloc.h>
void *bufs[5];
int main()
{
    printf("Before malloc()s.\n");
    getchar();
    bufs[0]=malloc(1024*1024*8);
    bufs[1]=malloc(1024*1024*8);
    bufs[2]=malloc(1024*1024*8);
    bufs[3]=malloc(1024*1024*8);
    bufs[4]=malloc(1024*1024*8);
    printf("After 5 malloc()s.\n");
    getchar();
    free(bufs[1]);
    free(bufs[3]);
    printf("After 2 free()s.\n");
    getchar();
    return 0;
}