#include<stdio.h>
#include<string.h>

struct cmd_line_args {
  int argv;
  char **argc;
};


void args(char* b[], struct cmd_line_args* mno ,char** a) {
  mno->argv = 0;
  if ( *a == NULL )
    return ;

  char del_space[] = " ";
  char* token = strtok(*a, del_space);
  token = strtok( NULL, del_space);
  while( token ) {
    b[ mno->argv ] = token;
    mno->argv++;
    if( !strcmp( token, "&" ) )
      break;
    token = strtok( NULL, del_space);
  }
  mno->argc = b;
}

void input2(char* b[], struct cmd_line_args* mno, char a[]) {
  fgets(a,100,stdin);
  char del[] = "|<>; ";
  int i = 0;
  mno->argv = 0;
  char* token = strtok(a,del);
  
  while( token ) {
    b[i] = token;
    mno->argv++;
    token = strtok(NULL, del);
    ++i;
  }
  mno->argc = b;
  int j;
  b[i-1][strlen(b[i-1]) -1] = '\0';

}

void pipes(char* b[], struct cmd_line_args* mno, char a[]) {
  fgets(a,100,stdin);
  char del[] = "|";
  int i = 0;
  mno->argv = 0;
  char* token = strtok(a,del);
  
  while( token != NULL ) {
    b[i] = token;
    mno->argv++;
    token = strtok(NULL, del);
    ++i;
  }

  mno->argc = b;
  int j;
  b[i-1][strlen(b[i-1]) -1] = '\0';
}

void outputs( char* b[], char pipe[], char** output, char** input, char** command ) {
  char del_output[] = ">";
  int i = 0;
  *output = NULL;
  *input = NULL;
  
  *command = strtok(pipe,del_output);
  
  char* token = strtok(NULL, del_output);
  while( token ) {
    *output = token;
    token = strtok(NULL, del_output);
  }

  char del_input[] = "<";
  token = strtok( *command, del_input );
  token = strtok( NULL, del_input );
  while( token ) {
    *input = token;
    token = strtok(NULL, del_input );
  }
  token = strtok( *output, del_input);
  token = strtok( NULL, del_input);
  while( token ) {
    *input = token; 
    token = strtok(NULL, del_input);
  }

  char del_space[] = " ";
  *input = strtok(*input, del_space);
  *output = strtok(*output, del_space);
}



/* void main() { */
/*   char a[1000], *b[10], *c[10], *command[10], *output[10], *input[10], *d[10]; */
/*   int i; */
/*   struct cmd_line_args pipe, arguments[10]; */

/*   pipes(b, &pipe, a); */
/*   for( i = 0; i < pipe.argv; ++i ) { */
/*     outputs(c, pipe.argc[i], &output[i], &input[i], &command[i]); */
/*     args( d, &arguments[i], &command[i]); */
/*     strtok(command[i], " "); */
/*   } */
/*   int j; */
/*   for(i=0; i<pipe.argv; ++i) { */
/*     printf("command:%s\noutput:%s|\ninput:%s|\n",command[i],output[i],input[i]); */
/*     for( j=0; j<arguments[i].argv; ++j) */
/*       printf("%s\n",arguments[i].argc[j]); */
/*   } */
/* } */
