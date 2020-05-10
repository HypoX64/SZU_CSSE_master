
#include <stdio.h>
#include <string.h>
 #include <unistd.h>
#include <stdlib.h>


// int **addOne(int a[M][N]){
//     int **b =(int **)malloc(M*sizeof(int *));

char **split(char **args, schar *str, char key){
	// char **args = malloc(10 * sizeof(char*));
	args[0] = "sef";
	return args;
	// static char args[10][64];
	// int part = 0;
	// int flag = 0;
	// int i = 0;
	// while(str[i] != '\0'){
	// 	if (str[i] == key){
	// 		int j;
	// 		for (j = 0; j < (i-flag); ++j){
	// 			args[part][j] = str[i];
	// 		}
	// 		args[part][i-flag]='\0';
	// 		part++;
	// 		flag = i;
	// 	}
	// 	// printf("%d\n",i );

	// 	// printf("%c\n",str[i]);
	// 	i++;
	// }
	// printf("%c\n",args[0][0] );
	// return args;
}

int main(void)
{
	char *str = "abc a";

	char args[10][64];
	
	// printf("%s\n",str );
	char a[10][64] = split(args,str,'a');



	// char **args = malloc(64 * sizeof(char*));
	// args[0] = str;
	// printf("%c\n",args[0][0] );
	// int i = 0;
	// while(str[i] != '\0'){
	// 	printf("%c\n",str[i]);
	// 	i++;
	// }

	// char* str2 = "abc";
	// char *args[10];
	// args[0] = str1;
	// printf("%s\n", args[0]);
	// if (args[3]=="/0")
	// {
	// 	printf("%s\n","true" );
	// 	/* code */
	// }
 

 
	return 0;
}
