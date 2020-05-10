#include <stdio.h>
#include <malloc.h>
#define kb 1024

void *bufs[134]; //1+1+1+2+1+4+1+8+1+16+1+32+1+64 = 134
// int list[]={0,2,5,10,19,36,69};

int main(){
    int i;
    for (i = 0; i < 134; ++i){
        bufs[i] = malloc(1*kb);
    }

    for (i = 0; i < 134; ++i){
        if (i==0)
            printf("<1kb pre-addr:%p\n",bufs[i+1] );
        else if (i == 2)
            printf("1~2kb pre-addr:%p\n",bufs[i+1] );
        else if (i == 5)
            printf("2~4kb pre-addr:%p\n",bufs[i+1] );
        else if (i == 10)
            printf("4-8kb pre-addr:%p\n",bufs[i+1] );
        else if (i == 19)
            printf("8-16kb pre-addr:%p\n",bufs[i+1] );
        else if (i == 36)
            printf("16-32kb pre-addr:%p\n",bufs[i+1] );
        else if (i == 69)
            printf("32-64kb pre-addr:%p\n",bufs[i+1] );
        else
            free(bufs[i]);
    }

    while(1){
        int size;
        printf("input size(<64kb):\n");
        scanf("%d",&size);
        void *ptr;
        ptr = malloc(size*kb);
        printf("true:addr:%p\n",ptr );
    }
    return 0;
}