#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#define MAX_SEND_SIZE 80
struct mymsgbuf {
    long mtype;
    char mtext[MAX_SEND_SIZE];
};
void send_message(int qid, struct mymsgbuf *qbuf, long type, char *text);
void read_message(int qid, struct mymsgbuf *qbuf, long type);
void remove_queue(int qid);
void change_queue_mode(int qid, char *mode);
void usage(void);


int main(int argc, char *argv[])
{
    key_t key;
    int msgqueue_id;
    struct mymsgbuf qbuf;
    if(argc == 1)
        usage();
    /* Create unique key via call to ftok() */
    key = ftok(".", 'm');
    
    /* Open the queue - create if necessary */
    if((msgqueue_id = msgget(key, IPC_CREAT|0660)) == -1)
    {
        perror("msgget");
        exit(1);
    }
    switch(tolower(argv[1][0]))
    {
        case 's':send_message(msgqueue_id,(struct mymsgbuf*)&qbuf,atol(argv[2]), argv[3]);
        break;
        case 'r': read_message(msgqueue_id, &qbuf, atol(argv[2]));
        break;
        case 'd': remove_queue(msgqueue_id);
        break;
        case 'm': change_queue_mode(msgqueue_id, argv[2]);
        break;
        default: usage();
    }
    return(0);
}
void send_message(int qid, struct mymsgbuf *qbuf, long type, char *text)
{
    /* Send a message to the queue */
    printf("Sending a message \n");
    qbuf->mtype = type;
    //填写消息的类型
    strcpy(qbuf->mtext, text);
    //填写消息内容
    if((msgsnd(qid, (struct msgbuf *)qbuf,strlen(qbuf->mtext)+1, 0)) ==-1)
    {
        perror("msgsnd");
        exit(1);
    }
    return;
}
void read_message(int qid, struct mymsgbuf *qbuf, long type)
{
    /* Read a message from the queue */
    printf("Reading a message \n");
    qbuf->mtype = type;
    msgrcv(qid, (struct msgbuf *)qbuf, MAX_SEND_SIZE, type, 0);
    printf("Type: %ld Text: %s\n", qbuf->mtype, qbuf->mtext);
    return;
}
void remove_queue(int qid)
{
    /* Remove the queue */
    msgctl(qid, IPC_RMID, 0);
    return;
}
void change_queue_mode(int qid, char *mode)
{
    struct msqid_ds myqueue_ds;
    /* Get current info */
    msgctl(qid, IPC_STAT, &myqueue_ds);
    /* Convert and load the mode */
    sscanf(mode, "%ho", &myqueue_ds.msg_perm.mode);
    /* Update the mode */
    msgctl(qid, IPC_SET, &myqueue_ds);
    return;
}
void usage(void)
{
    fprintf(stderr,"msgtool - A utility for tinkering with msg queues\n");
    fprintf(stderr,"nUSAGE: msgtool (s)end \n");
    fprintf(stderr,"msgtool (r)ecv \n");
    fprintf(stderr,"msgtool (d)elete\n");
    fprintf(stderr,"msgtool (m)ode \n");
    exit(1);
}

