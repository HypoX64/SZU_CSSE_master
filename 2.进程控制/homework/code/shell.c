#include <sys/wait.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

char *shell_read_line();
char **shell_split_line(char * line);
int shell_execute(char **args);

void shell_loop(void){
	char *line;
	char **args;
	int status;
	do {
		printf(">>");
		line = shell_read_line();
		args = shell_split_line(line);
		status = shell_execute(args);

		free(line);
		free(args);
	}while(status);
}

char *shell_read_line(){
	char *line = NULL;
	ssize_t bufsize = 0; // getline()function will help us allocate a buffer
	getline(&line,&bufsize,stdin);

	return line;
}

int main(int argc, char **argv[])
{
	shell_loop();
}