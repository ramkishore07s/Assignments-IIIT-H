#include<sys/stat.h>
#include<stdlib.h>
#include<fcntl.h>
#include<unistd.h>
#include<dirent.h>
#include<string.h>
#include<pwd.h>
#include<grp.h>


int cd(char* dir) {
  return chdir(dir);
}

void pwd() {
  char a[1000];
  getcwd(a,999);
  printf("%s\n",a);
}


