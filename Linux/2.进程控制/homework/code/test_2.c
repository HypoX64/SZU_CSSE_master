#include <stdio.h>
#include <string.h>
#include <stdlib.h>
 
//返回一个 char *arr[], size为返回数组的长度
char **split(char sep, const char *str, int *size)
{
    int count = 0, i;
    for(i = 0; i < strlen(str); i++)
    {       
        if (str[i] == sep)
        {       
            count ++;
        }
    }

    char **ret = calloc(++count, sizeof(char *));
    if (count == 0)   {
        ret[0] = calloc(strlen(str), sizeof(char)); //分配子串长度+1的内存空间
        memcpy(ret[0], str, strlen(str) - 1);
        return ret;

    }

    int lastindex = -1;
    int j = 0;

    for(i = 0; i < strlen(str); i++)
    {       
        if (str[i] == sep)
        {       
            ret[j] = calloc(i - lastindex, sizeof(char)); //分配子串长度+1的内存空间
            memcpy(ret[j], str + lastindex + 1, i - lastindex - 1);
            j++;
            lastindex = i;
        }
    }
    //处理最后一个子串
    if (lastindex <= strlen(str) - 1)
    {
        ret[j] = calloc(strlen(str) - lastindex, sizeof(char));
        memcpy(ret[j], str + lastindex + 1, strlen(str) - 1 - lastindex);
        j++;
    }

    *size = j;

    return ret;
}
void test(){
    int size;
    char **args;
    char *str = "aaabbb";
    args = split(',',str, &size);
    printf("%s\n",args[0] );
}
int main()
{   int i =0;
    for (i = 0; i < 10; ++i)
    {
        test();
    }
    


    // int i;
    // for(i = 0; i < size; i++)
    // {
    //     printf("%s\n", ret[i]);
    //     free(ret[i]);
    // }
    // free(ret);
    return 0;
}
