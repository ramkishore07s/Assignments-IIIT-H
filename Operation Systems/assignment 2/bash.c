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

#include "input.h"
#include "inbuilt.h"
#include "ls.h"
#include "pinfo.h"

void print_prompt(char user_name[],char home[], char a[]) {
  printf("<%s@Mac_OS_X:",user_name);
  int i;
  getcwd(a,999);
  if( !strcmp(home,a) )
    printf("~>");
  else {
    for( i = strlen(a) -1; i>=0 && a[i] != '/'; --i );
    printf("%s>",a + i + 1);
  }
}

int main() {
  int exit = 0,j,m,k;
  char *b[10];
  char user_name[1000],home[1000],err_message[3000];
  cd("Documents");
  cd("..");
  getlogin_r(user_name,999);
  int i;
  char a[1000],n[1000]; int pointers[100];
  pid_t pid = 1,tpid;
  int background;
  int bg_p[100],bg_c = 0,endID,status; char process_name[20][10], aa[101];
  getcwd(home,1000);

  
  struct cmd_line_args inp;
  while( !exit  && pid ) {    

    for( i=0; i<bg_c; ++i ) {
      endID = waitpid(bg_p[i], &status, WNOHANG );
      //endID = kill(bg_p[i],0);
      if( endID == bg_p[i] ) {
	if( WIFEXITED(status) )
	  printf("process.name: \"%s\" with process.no: \"%d\"  exited successfully\n",process_name[i],bg_p[i]);
	else if( WIFSIGNALED(status) )
	  printf("process.name: \"%s\" with process.no: \"%d\"  terminated due to uncaught signal\n",process_name[i],bg_p[i]);
	else if( WIFSTOPPED(status) )
	  printf("process.name: \"%s\" with process.no: \"%d\"  has stopped\n",process_name[i],bg_p[i]);
    	if( i!=0 ) {
    	  bg_p[i] = bg_p[ bg_c - 1 ];
	  strcpy(process_name[i], process_name[ bg_c -1 ]);
	}
    	--bg_c;
    	--i;
      }
    }

    print_prompt(user_name,home,a);
    input(b,&inp,aa);
    inp.argc[inp.argv] = NULL;

    if( inp.argc[0][0] == '\0' )
      continue;
    
    if( !strcmp("&",inp.argc[inp.argv-1]) ) {
      background = 1;
      inp.argc[inp.argv-1][0] = '\0';
      --inp.argv;
      inp.argc[inp.argv] = NULL;
    }
    else
      background = 0;

    if ( !strcmp("ls", inp.argc[0]) ) {
	ls(inp.argc + 1,inp.argv-1);
    }
    else if ( !strcmp("echo", inp.argc[0]) ) {
      for (i=1; i<inp.argv; ++i)
	printf("%s ",inp.argc[i]);
      printf("\n");
    }	       
    else if( !strcmp("pwd", inp.argc[0]) )
      pwd();
    else if( !strcmp("cd", inp.argc[0]) ) {
      if (inp.argv != 2)
	printf("error\n");
      else
	cd(inp.argc[1]);
    }
    else if( !strcmp("exit",inp.argc[0]) )
      break;
    else if( !strcmp("pinfo",inp.argc[0]) ) {
      if( inp.argv > 1 )
	pinfo_pid( atoi(inp.argc[1]) );
      else
	pinfo_pid( 0 );
    }
    else {
      
      j = 0;m = -1;
      for( i=0; i<inp.argv; ++i ){
	strcpy(n+j,inp.argc[i]);
	pointers[++m] = j; 
	j = strlen(n+j)+ 1 + j;
      }
	
      pid = fork();
      
      if( pid == 0 ) {


	for(k=0; k<i; ++k) {
	  inp.argc[k] = n+pointers[k];
	}
	if( background )
	  setpgid(0,0);
	
	execvp(inp.argc[0],inp.argc);
	printf("\n%s :unknown command\n",inp.argc[0]);
	break;
      }
      else {
	printf("pid:%d\n",pid);
	if( !background )
	  wait(NULL);
	else {
	  bg_p[bg_c] = pid;
	  strcpy(process_name[bg_c],n);
	  bg_c++;
	}

      }

      
    }
  }
  return 0;
}
