#include <stdio.h>
void main()
{
    char *str = "Hello world!\n";
    printf("%s @ %p\n", str, str);
    getchar();
    return;
}