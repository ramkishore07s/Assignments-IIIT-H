#include<stdio.h>
#include<string.h>

struct cmd_line_args {
  int argv;
  char **argc;
};


void input(char* b[], struct cmd_line_args* mno ,char a[]) {
  fgets(a,100,stdin);
  
  int i = 0,j = 0,flag = 0;
  int l = strlen(a);
  
  while( i < l ) {
    flag = 0; 
    while( a[i] == ' ' )
      ++i;
    b[j] = a + i;
    while(a[i] != ' ' && a[i] != '\0' && i <l && a[i] != '\n') {
      ++i;
      flag = 1;
    }
    if (a[i] != '\0') {
      a[i] = '\0';
    }
    ++j;
    ++i;
  }
  mno->argc = b;
  mno->argv = j;
}
