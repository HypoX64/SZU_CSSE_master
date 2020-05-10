#define SH_TOK_BUFSIZE 64
#define SH_TOK_DELIM " \t\r\n\a"

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

char **shell_split_line(char *line){
	int bufsize = SH_TOK_BUFSIZE;
	int position = 0;
	char **tokens = malloc(bufsize * sizeof(char*));
	char **token;

	if(!tokens){
		fprintf(stderr,"Mycshell:allocation error!\n");
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
				fprintf(stderr,"Mycshell:allocation error!\n");
				exit(EXIT_FAILURE);
			}
		}

		token = strtok(NULL,SH_TOK_DELIM);
	}
	tokens[position] = NULL;

	return tokens;
}

int shell_launch(char **args){
	pid_t pid,wpid;
	int status;

	pid = fork();
	if(pid == 0){
		if(execvp(args[0],args) == -1){
			perror("mycshell");
		}
		exit(EXIT_FAILURE);
	} else if (pid < 0) {
		//Error fork()
		perror("mycshell");
	} else {
		do {
			wpid = waitpid(pid,&status,WUNTRACED);
		}while (!WIFEXITED(status) && !WIFSIGNALED(status));
	}

	return 1;
}

/* Builtin Function part*/

int shell_help(char **args);
int shell_exit();

char *builtin_str[] = {"help","exit"};
int (*builtin_func[])(char **) = {&shell_help,&shell_exit};

int shell_num_builtins(){
	return sizeof(builtin_str) / sizeof(char *);
}

int shell_help(char **args){
	int i;
	printf("This is J's cshell,\n");
	printf("Type program names and arguments,then enter.\n");
	printf("The following are built in:\n");

	for(i = 0;i < shell_num_builtins();i++){
		printf("  %s\n",builtin_str[i]);
	}

	printf("Please use the man command for information on other programs.\n");
	return 1;
}

int shell_exit(char **args){
	return 0;
}

int shell_execute(char **args){
	int i;
	if(args[0] == NULL){
		//if input an empty command
		return 1;
	}

	for(i = 0;i<shell_num_builtins();i++){
		if(strcmp(args[0],builtin_str[i]) == 0){
			return (*builtin_func[i])(args);
		}
	}

	return shell_launch(args);
}

int main(int argc,char **agrv){
	//Load config files;

	shell_loop();

	//Shutdown or Clean up;
}
