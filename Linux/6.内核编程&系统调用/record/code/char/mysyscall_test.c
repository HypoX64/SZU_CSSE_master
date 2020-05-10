#include <stdio.h>
#include <stdlib.h>
int main(int argc,void **argv)
{   int input_num,result;
    input_num= atoi(argv[1]);
    result=syscall(326,input_num);
    printf("result of mysyscall(%d) is: %d.\n",input_num,result);
    return 0;
}