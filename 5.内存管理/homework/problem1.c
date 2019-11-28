#include<stdio.h>
#include<malloc.h>

#define kB 1024
void *p;
int main()
{
    int i = 8;
    while(1)
    {
        p = malloc(i*kB);
        free(p);
        printf("%d,succeed,%s\n",i,p);
        i++;
    }
    return 0;
}
