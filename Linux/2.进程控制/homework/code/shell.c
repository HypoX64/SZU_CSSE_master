#include <sys/wait.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define SH_TOK_BUFSIZE 64
#define SH_TOK_DELIM " \t\r\n\a"

char *shell_read_line();
char **shell_split_line(char * line);
int shell_execute(char **args);



void shell_loop(void){
	char *line;
	char **args;

	int size;
	while(1){
		printf(">>");
		line = shell_read_line();
		args = shell_split_line(line);
		shell_execute(args);
		free(line);
		free(args);

	}

}

char *shell_read_line(){
	char *line = NULL;
	ssize_t bufsize = 0; // getline()function will help us allocate a buffer
	getline(&line,&bufsize,stdin);
	return line;
}

char **shell_split_line(char *line){
	int bufsize = SH_TOK_BUFSIZE;
	int position = 0;
	char **tokens = malloc(bufsize * sizeof(char*));
	char **token;

	if(!tokens){
		fprintf(stderr,"allocation error!\n");
		exit(EXIT_FAILURE);
	}

	token = strtok(line,SH_TOK_DELIM);

	while(token != NULL){
		tokens[position] = token;
		position++;

		if(position >= bufsize){
			bufsize += SH_TOK_BUFSIZE;
			tokens = realloc(tokens,bufsize * sizeof(char*));
			if(!tokens){
				fprintf(stderr,"allocation error!\n");
				exit(EXIT_FAILURE);
			}
		}
		token = strtok(NULL,SH_TOK_DELIM);
	}
	tokens[position] = NULL;
	return tokens;
}

// char *shell_read_line(){
// 	static char buff[1024];
//   	//scanf("%s", buff);
// 	fgets(buff, sizeof(buff), stdin);
// 	// printf("stren buff[%ld]\n", strlen(buff));
// 	buff[strlen(buff)-1] = '\0';
// 	return buff;

// }

int shell(char **args){
	pid_t pid,wpid;
	int status;
	pid = fork();
    if(pid == -1 ) 
    {
        printf("error!\n");
    } 
    else if( pid ==0 ) 
    {
    	if(execvp(args[0],args) == -1){
			perror("shell");
		}
		exit(EXIT_FAILURE);
    	// execvp(args[0],args);

    }
	do {
		wpid = waitpid(pid,&status,WUNTRACED);
	}while (!WIFEXITED(status) && !WIFSIGNALED(status));
	return 1;

}


int shell_execute(char **args)
{
	// printf("%s\n",args[0] );

	if (strcmp(args[0], "help") == 0){
		printf("%s\n","This is a smaple shell build by C @Hypo");
	}
	else if(strcmp(args[0], "exit") == 0){
		exit(0);
	}
	else if(strcmp(args[0], "cd") == 0){
		printf("%s\n","No such command!" );
	}
	else{
		shell(args);
	}
}

int main(int argc, char **argv[])
{
	shell_loop();
}