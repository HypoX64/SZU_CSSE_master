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

int len(char **args){
    int i = 0;
    int length = 0;
    for (i = 0; i < 10; ++i)
    {
        if (args[i]!=NULL)
            {
                length++;
            }    
    }
    return length;
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


int pipe_shell(char **args1, char **args2)
{
    int pfds[2];
    pid_t pid1, pid2, wpid;
    pipe(pfds);
    char buf[1024];
    int nwr = 0;
    int status;
    pid1 = fork();
    if (pid1 < 0) 
    {
        printf("fork error!\n");
    } 
    else if (pid1 == 0)
     {  
        
        // STDIN_FILENO：接收键盘的输入
        // STDOUT_FILENO：向屏幕输出
        // dup2 把 pfds[1](管道数据入口描述符) 复制到 文件描述符1&2
        // 实现把pid1的标准输出和标准错误 输送到管道
         
        dup2(pfds[1], STDOUT_FILENO);
        dup2(pfds[1], STDERR_FILENO);
        close(pfds[0]);
        close(pfds[1]);

        char *args[]={"ls",NULL};
        execvp(args1[0], args1);
        exit(0);
    }

    pid2 = fork();
    if (pid2< 0) 
    {
        printf("error!\n");
    } 
    else if (pid2 == 0){
        
        //dup2 把 pfds[0](管道数据出口描述符) 复制到 文件描述符0
        //实现pid2从管道中读取(pid1的输出)数据        
        dup2(pfds[0], STDIN_FILENO);
        close(pfds[0]);
        close(pfds[1]);

        char *args[]={"more",NULL};
        execvp(args2[0], args2);
        exit(0);
    }

    close(pfds[0]);
    close(pfds[1]);
    do 
    {
        wpid = waitpid(pid2,&status,WUNTRACED);
    }
    while (!WIFEXITED(status) && !WIFSIGNALED(status));
    return 1;
}

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

	// printf("%d\n",cnt );
    // int length = sizeof(args);
    // printf("%d\n",len(args) );

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
        if (len(args)>2)
        {
            if (strcmp(args[1], "|") == 0)
            {
                char *args1[] = {args[0],NULL};
                char *args2[] = {args[2],NULL};
                pipe_shell(args1,args2);
            }
            else{shell(args);}
        }
        else{shell(args);}
    }

}

int main(int argc, char **argv[])
{
	shell_loop();
}