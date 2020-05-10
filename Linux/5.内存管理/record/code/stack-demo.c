#include<stdio.h>

void up_and_down(int);

int main(void)
{
    printf("Initial state, please check /proc/PID/maps!\n");
    getchar();
    up_and_down(1);
    return 0;
}
void up_and_down(int n)
{
    int var_in_stack_frame[64*1024];    //局部数组,占用堆栈空间
    printf("Level %d:n location %p\n",n,&n);
    getchar();
    if(n<3)
        up_and_down(n+1);
    printf("Level %d:n location %p\n",n,&n);
    getchar();
    return;
}