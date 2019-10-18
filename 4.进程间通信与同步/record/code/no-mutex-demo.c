#include <pthread.h>
#include <unistd.h>
#include <stdio.h>
#include <malloc.h>
#define thread_num 16
#define MB 1024 * 1024

int *array;
int length;//array length

int count;
int t; //number of thread

void *count3s_thread(void* id);
int main()
{
    int i;
    int tid[thread_num];
    pthread_t threads[thread_num];
    length = 64 * MB;
    array = malloc(length*4);     //256MB
    for (i = 0; i < length; i++)     //initial array
    array[i] = i % 2 ? 4 : 3;     //偶数 i 对应数值 3

    for (t = 0; t < thread_num; t++)
    //循环创建 16 个线程
    {
        count = 0;
        tid[t]=t;
        int err = pthread_create(&(threads[t]), NULL, count3s_thread,&(tid[t]) );
        if (err)
        {
            printf("create thread error!\n");
            return 0;
        }
    }
    for (t = 1; t < thread_num; t++)
        pthread_join(threads[t], NULL);    //等待前面创建的计数线程结束

    printf("Total count= %d \n",count);
    return 0;
}
void *count3s_thread(void* id)
//计数线程执行的函数
{
    /*compute portion of the array that this thread should work on*/
    int length_per_thread = length / thread_num;
    //length of every thread
    int start = *(int *)id * length_per_thread;
    //every thread start position
    int i;
    for (i = start; i < start + length_per_thread; i++)
    {
        if (array[i] == 3)
        {
            count++;         //计数,为加入互斥保护
        }
    }
}