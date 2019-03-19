#include<stdio.h>
#include<sys/stat.h>
#include<stdlib.h>
#include<fcntl.h>
#include<unistd.h>
#include<dirent.h>
#include<string.h>
#include<sys/wait.h>
#include<signal.h>
#include<errno.h>
#include<sys/sysctl.h>
#include<stdlib.h>


void pinfo_pid(int pid) {
  if( pid == 0 ){
    pid = getpid();
    printf("process no: %d\n",pid);
  }
  char proc[500];
  strcpy(proc, "/proc/");
  int i;
  char a[10];
  a[9] = NULL;
  for( i=8; pid!=0 && i>0 ; --i ) {
    a[i] = pid%10 + 48;
    pid/=10;
  }
  strcpy( proc + strlen( proc ) , a+i+1);
  strcpy( proc + strlen( proc ), "/cmdline");
  FILE * fp = fopen(proc,"r");
  char proc_name[100];
  fgets(proc_name,99,fp);
  printf("process name: %s\n",proc_name);
  strcpy( proc + strlen( proc ) - strlen("/cmdline") , "/status" );
  fp = fopen(proc,"r");
  char memory[1000];
  if( fp ) {
    for(i=0; i<17; ++i)
      fgets(memory,1000,fp);
    printf("%s",memory);
  }
  
}
