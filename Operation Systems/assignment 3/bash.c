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
//opened a pipe but didnot close it
//use buffer to pass output between iterations and pipe if child process is invoked
//how to know if fork will happen or not?
//variable error pipe and function pipe!! WTF
void debug() {
  fprintf(stderr, "asdf");
}
int bg_p[100],bg_c = 0,endID,status; char process_name[20][10], aa[101];
int background;
pid_t pid = 1,tpid;
int bg_n[100],child_no = 1, pipefd[2];
char n[1000];
void sigintHandler(int sig_num) {
  
}

void stopHandler(int sig_num) {
  if( pid != 0 ) {
    bg_p[bg_c] = pid;
    bg_n[bg_c] = child_no;
    strcpy( process_name[bg_c], n);
    printf("%d",pid);
    kill( pid, SIGSTOP);
    child_no++;
    bg_c++;
  }
}

void print_prompt(char user_name[],char home[], char a[]);
void background_on_exit(char process_name[][10], int* bg_p, int* bg_cc, int bg_n[] );
void jobs(char process_name[][10], int* bg_p, int* bg_cc, int bg_n[] );

int main() {
  int exit = 0,j,m,k,i123;
  char *b[10],*c[10][10],*command[10], *output[10], *input[10], *d[10][10], a[1000];
  char user_name[1000],home[1000],err_message[3000];
  int i;
  char n_c[100]; int pointers[100];


  signal(SIGTSTP, stopHandler);
  signal(SIGINT, sigintHandler);
  getcwd(home,1000);
  cd("Documents");
  cd("..");
  getlogin_r(user_name,999);
  
  struct cmd_line_args piping, arguments[10];
  while( !exit  && pid ) {    
    
    background_on_exit(process_name, bg_p, &bg_c, bg_n );
    print_prompt(user_name,home,a);

    pipes(b,&piping,a);
    for( i = 0; i < piping.argv; ++i ) {
      outputs(c[i], piping.argc[i], &output[i], &input[i], &command[i] );
      args( d[i], &arguments[i], &command[i]);
      command[i] = strtok(command[i], " ");
    }
    
    if( pipe(pipefd) == -1 )
      perror("pipe");

  /*   int j; */
  /* for(i=0; i<piping.argv; ++i) { */
  /*   printf("command:%s\noutput:%s|\ninput:%s|\n",command[i],output[i],input[i]); */
  /*   for( j=0; j<arguments[i].argv; ++j) */
  /*     printf("%s\n",arguments[i].argc[j]); */
  /* } */


  int pip,stdout_std = dup(1),size,out,buf_size,buffer_i,awe;
  char* inp_file = malloc(1), *buffer_data = malloc(1);
  FILE *inp;
  char temp_inp[1000],temp_inp2[1000];
  FILE *buffer, *buffer_copy;
    
  dup2(STDOUT_FILENO, 1);
//for each piping------------------------------------------------------
    for( i = 0; i < piping.argv; ++i ) {

      inp = NULL;
      out = NULL;
      temp_inp[0] = NULL;
      stdout_std = dup(1);

      if ( command[i] == NULL )
	continue;

      if( arguments[i].argv > 0 && !strcmp("&",arguments[i].argc[ arguments[i].argv-1 ]) ) {
	background = 1;
	arguments[i].argc[arguments[i].argv-1][0] = '\0';
	--arguments[i].argv;
	arguments[i].argc[arguments[i].argv] = NULL;
      }
      else
	background = 0;


      if ( i != 0 ) {
	buffer = fopen("BUFFER","r");
	fseek( buffer, 0L , SEEK_END );
	buf_size = ftell(buffer);
	rewind(buffer);
	buffer_data = calloc(1, buf_size + 1 );
	fread( buffer_data, buf_size, 1, buffer);
	fclose(buffer);
	buffer_copy = fopen("BUFFER_COPY","wab+" );
	fwrite( buffer_data, buf_size, 1, buffer_copy);
	fclose(buffer_copy);
      }
      
      if( i != piping.argv-1 ) {
	buffer_i = open("BUFFER", O_RDWR | O_TRUNC | O_CREAT ,0644);
	dup2( buffer_i, 1 );
	close(buffer_i);
      }

      if( input[i] != NULL) {
	strcpy(temp_inp, input[i]);
	inp = fopen(input[i], "r" );
	if( inp == NULL ) {
	  fprintf(stderr,"no such file: %s\n",input[i]);
	  continue;
	} 
	fseek( inp, 0L,SEEK_END);
	size = ftell(inp);
	rewind(inp);
	inp_file = calloc(1, size + 1 );
	fread( inp_file, size, 1, inp);
	fclose(inp);
	arguments[i].argc[arguments[i].argv] = inp_file;
	arguments[i].argv++;
      }	
      if( output[i] != NULL ) {
	out = open(output[i], O_WRONLY | O_CREAT | O_TRUNC, 0644);
	dup2( out , 1 );
	close(out);
      }

      if ( i != 0 ) {
	arguments[i].argc[arguments[i].argv] = buffer_data;
	arguments[i].argv++;
      }

      if ( !strcmp("ls", command[i]) ) {
	ls(arguments[i].argc, arguments[i].argv);
      }
      else if ( !strcmp("echo", command[i]) ) {
	if( arguments[i].argc[0][0] != '$' )
	  printf("%s",arguments[i].argc[0]);
	else
	  printf("%s",getenv(arguments[i].argc[0] + 1));
      }	       
      else if( !strcmp("pwd", command[i]) )
	pwd();
      else if( !strcmp("cd", command[i]) ) {
	if (arguments[i].argv != 1)
	  fprintf(stderr,"error\n");
	else
	  cd(arguments[i].argc[0]);
      }
      else if( !strcmp("quit",command[i]) )
	goto outside;
      else if( !strcmp("pinfo",command[i]) ) {
	if( arguments[i].argv > 0 )
	  pinfo_pid( atoi(arguments[i].argc[0]) );
	else
	  pinfo_pid( 0 );
      }
      else if( !strcmp("setenv", command[i]) ) {
	if( arguments[i].argv > 2 || arguments[i].argv < 1 )
	  fprintf(stderr, "Usage: setenv var [value]");
	else {
	  if( arguments[i].argv == 1 ){
	    awe = setenv(arguments[i].argc[0], "", 0);
	  }
	  else {
	    strcpy( temp_inp2, arguments[i].argc[1]);
	    awe = setenv(arguments[i].argc[0], temp_inp2, 1 );
	  }
	}
      }
      else if( !strcmp("unsetenv", command[i]) ) {
	if( arguments[i].argv!= 1 )
	  fprintf(stderr, "Usage unsetenv var");
	else {
	  unsetenv(arguments[i].argc[0]);
	}
      }
      else if( !strcmp("jobs", command[i]) ) {
	jobs(process_name, bg_p, &bg_c, bg_n );
      }
      else if( !strcmp("kjob", command[i]) ) {
	if( arguments[i].argv != 2 )
	  fprintf(stderr, "Usage: kjob <job no> <signal>");
	for( j = 0; j< bg_c; ++j )
	  if( bg_n[j] == atoi( arguments[i].argc[0] ) )
	    kill( bg_p[j], atoi( arguments[i].argc[1]) );
      } 
      else if( !strcmp("overkill", command[i]) ) {
	if( arguments[i].argv != 0 ) 
	  fprintf(stderr, "Usage: overkill");
	else
	  for( j=0; j<bg_c; ++j)
	    kill( bg_p[j], 9);
      }
      else if( !strcmp("fg",command[i]) ) {
	if( arguments[i].argv != 1)
	  fprintf(stderr, "usage: bg <no> " );
	else
	  for( j=0; j<bg_c; ++j)
	    if( bg_n[j] == atoi(arguments[i].argc[0] )){
	      kill( bg_p[j], SIGCONT);
	      wait(NULL);
	    }
      }
      else {
      
	j = 0;m = -1;
	strcpy( n, command[i] );
	j = strlen( n ) + 1;
	pointers[++m] = 0;

       	if ( input[i] != NULL )
	  arguments[i].argv--;
	if ( i != 0 )
	  arguments[i].argv--;

	for( i123=0; i123<arguments[i].argv; ++i123 ){
	  strcpy(n+j,arguments[i].argc[i123]);
	  pointers[++m] = j; 
	  j = strlen(n+j)+ 1 + j;
	}

	pid = fork();
	if( pid == -1 )
	  perror("fork");

	if( pid == 0 ) {
	  
	  signal(SIGINT, SIG_DFL);
	  signal(SIGTSTP,SIG_DFL);

	  for(k=0; k<=m; ++k) {
	    arguments[i].argc[k] = n+pointers[k];
	  }
	  arguments[i].argv++;

	  if( temp_inp[0] != NULL ) {
	    strcpy(temp_inp, input[i]);
	    inp = fopen(input[i], "r" );
	    fseek( inp, 0L,SEEK_END);
	    size = ftell(inp);
	    rewind(inp);
	    inp_file = calloc(1, size + 1 );
	    fread( inp_file, size, 1, inp);
	    fclose(inp);
	    arguments[i].argc[ arguments[i].argv  ] = inp_file;
	    arguments[i].argv++;
	  }	
	  if ( i != 0 ) {
	    buffer = fopen("BUFFER_COPY","r");
	    fseek( buffer, 0L , SEEK_END );
	    buf_size = ftell(buffer);
	    rewind(buffer);
	    buffer_data = calloc(1, buf_size + 1 );
	    fread( buffer_data, buf_size, 1, buffer);
	    fclose(buffer);
	    arguments[i].argc[arguments[i].argv] = buffer_data;
	    arguments[i].argv++;
	  }
 
	  if( background )
	    setpgid(0,0);
	  
	  /* fflush(stdout); */
	  /* dup2(stdout_std,1); */
	  /* close(stdout_std); */
	  
	  execvp(arguments[i].argc[0],arguments[i].argc);
	  fprintf(stderr,"\n%s :unknown command\n",arguments[i].argc[0]);
	  break;
	}
	else {
	  //	  printf("pid:%d\n",pid);
	  if( !background )
	      waitpid( 0, &status, WUNTRACED);//	    wait(NULL);
	  else {
	    bg_p[bg_c] = pid;
	    strcpy(process_name[bg_c],n);
	    bg_n[bg_c] = child_no;
	    bg_c++;
	    child_no++;
	  }
	}      
      }
      /* if( output[i] != NULL ) { */
	fflush(stdout);
	dup2(stdout_std,1);
	close(stdout_std);
	/* }	 */
    }
  }
 outside:
  return 0;
}



void background_on_exit(char process_name[][10], int* bg_p, int* bg_cc, int bg_n[] ) {
  int i, bg_c = *bg_cc,status, endID;
  for( i=0; i<bg_c; ++i ) {
    endID = waitpid(bg_p[i], &status, WNOHANG );
    //endID = kill(bg_p[i],0);
    if( endID == bg_p[i] ) {
      if( WIFEXITED(status) ) {
	printf("[%d] process.name: \"%s\" with process.no: \"%d\"  exited successfully\n",bg_n[i],process_name[i],bg_p[i]);
	if( i!=0 ) {
	  bg_p[i] = bg_p[ bg_c - 1 ];
	  strcpy(process_name[i], process_name[ bg_c -1 ]);
	  bg_n[i] = bg_n[ bg_c - 1 ];
	}
	--bg_c;
	--i;
      }
      else if( WIFSIGNALED(status) ) {
	printf("[%d] process.name: \"%s\" with process.no: \"%d\"  terminated due to uncaught signal\n",bg_n[i],process_name[i],bg_p[i]);
	if( i!=0 ) {
	  bg_p[i] = bg_p[ bg_c - 1 ];
	  strcpy(process_name[i], process_name[ bg_c -1 ]);
	  bg_n[i] = bg_n[ bg_c - 1 ];
	}
	--bg_c;
	--i;
      }
      else if( WIFSTOPPED(status) )
	printf("[%d] process.name: \"%s\" with process.no: \"%d\"  has stopped\n",bg_n[i],process_name[i],bg_p[i]);
    }
  }
  *bg_cc = bg_c;
}

void jobs(char process_name[][10], int* bg_p, int* bg_cc, int bg_n[] ) {
  int i, bg_c = *bg_cc,status, endID;
  for( i=0; i<bg_c; ++i ) {
    endID = waitpid(bg_p[i], &status, WNOHANG );
    //endID = kill(bg_p[i],0);
    if( endID == bg_p[i] ) {
      if( WIFEXITED(status) ) {
	printf("[%d] process.name: \"%s\" with process.no: \"%d\"  exited successfully\n",bg_n[i],process_name[i],bg_p[i]);
	if( i!=0 ) {
	  bg_p[i] = bg_p[ bg_c - 1 ];
	  strcpy(process_name[i], process_name[ bg_c -1 ]);
	  bg_n[i] = bg_n[ bg_c - 1 ];
	}
	--bg_c;
	--i;
      }
      else if( WIFSIGNALED(status) ) {
	printf("[%d] process.name: \"%s\" with process.no: \"%d\"  terminated due to uncaught signal\n",bg_n[i],process_name[i],bg_p[i]);
	if( i!=0 ) {
	  bg_p[i] = bg_p[ bg_c - 1 ];
	  strcpy(process_name[i], process_name[ bg_c -1 ]);
	  bg_n[i] = bg_n[ bg_c - 1 ];
	}
	--bg_c;
	--i;
      }      
      else if( WIFSTOPPED(status) )
	printf("[%d] \"%s\" with process.no: [%d]  stopped\n",bg_n[i],process_name[i],bg_p[i]);
    }
    else if( endID == 0 )
      printf("[%d] \"%s\" with process.no: [%d]  running\n",bg_n[i],process_name[i],bg_p[i]);
  }
  *bg_cc = bg_c;
}
  
void print_prompt(char user_name[],char home[], char a[]) {
  printf("<%s@Mac_OS_X:",user_name);
  int i,flag=0;
  getcwd(a,999);
  if( !strcmp(home,a) )
    printf("~>");
  else {
    for( i = strlen(a) -1; i>=0 && a[i] != '/'; --i,--flag ); 
    if( !strcmp( a + i + 1, "ramkishore" ))
      printf("~");
    else
      printf("%s",a + i + 1);
    if ( flag >= -1 )
      printf("/");
    printf(">");
  }
}


  
