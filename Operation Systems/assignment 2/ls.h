#include<sys/stat.h>
#include<stdlib.h>
#include<fcntl.h>
#include<unistd.h>
#include<dirent.h>
#include<string.h>
#include<pwd.h>
#include<grp.h>


struct options{
  char opt[10];
  int no;
};

struct options* contains(char* str[],int no,struct options cmd,struct options* cont){
  int i,j,k,l;
  cont->no = 0;
  cont->opt[0] = '\0';
  int flag;
  for( i=0; i<no; ++i) {
    for( j=0; j<strlen(str[i]); ++j)
      if( !strchr(cmd.opt, str[i][j]) && str[i][j] != '-' )
	return cont;
  }
  for( i = 0; i < no; ++i )
    for( j = 0; j < cmd.no; ++j) {
      if( strchr(str[i], cmd.opt[j]) && !strchr(cont->opt, cmd.opt[j]) ) {
	cont->opt[cont->no] = cmd.opt[j];
	cont->no++;
	cont->opt[cont->no] = '\0';
      }
    }
  return cont;
}

void permissions( char a[] ) {
  struct stat dest_buf;
  lstat(a,&dest_buf);
  if( S_ISDIR(dest_buf.st_mode) )
    printf("d");
  else
    printf("-");
  
  if( dest_buf.st_mode & S_IRUSR )
    printf("r");
  else
    printf("-");

  
  if( dest_buf.st_mode & S_IWUSR )
    printf("w");
  else
    printf("-");

  
  if( dest_buf.st_mode & S_IXUSR )
    printf("x");
  else
    printf("-");

  
  
  
  if( dest_buf.st_mode & S_IRGRP )
    printf("r");
  else
    printf("-");

  
  if( dest_buf.st_mode & S_IWGRP )
    printf("w");
  else
    printf("-");

  
  if( dest_buf.st_mode & S_IXGRP )
    printf("x");
  else
    printf("-");

  
  
  
  if( dest_buf.st_mode & S_IROTH )
    printf("r");
  else
    printf("-");

  
  if( dest_buf.st_mode & S_IWOTH )
    printf("w");
  else
    printf("-");

  
  if( dest_buf.st_mode & S_IXOTH )
    printf("x");
  else
    printf("-");

  printf("          ");

  int i;
  char u[100]; strcpy(u, getpwuid(dest_buf.st_uid)->pw_name);
  char o[100]; strcpy(o, getgrgid(dest_buf.st_gid)->gr_name);
  printf("%s ",u);
  for( i=20; i>= strlen(u); --i)
    printf(" ");
  printf("%s ",o);
  for( i=20; i>= strlen(o); --i)
    printf(" ");
  printf("%s ",a);
  for( i = 100; i>= strlen(a); --i)
    printf(" ");
  printf("%lld ",dest_buf.st_size);
}

void ls( char* argc[] , int argv) {
  
  struct options ls_cmd;
  ls_cmd.opt[0] = 'l';
  ls_cmd.opt[1] = 'a';
  ls_cmd.opt[2] = '\0';
  ls_cmd.no = 2;

  struct dirent *d;
  DIR *dir = opendir(".");
  if ( argv == 0 ) {
    d = readdir(dir);
    while(d != NULL) {
      if( d->d_name[0] != '.')
	printf("%s\n",d->d_name);
      d = readdir(dir);
    }    
  }
  else {
    struct options cont;
    contains( argc, argv, ls_cmd, &cont );
    if( cont.no == 0 )
      printf("Usage: ls [-la]\n");
    else {
      if( strchr(cont.opt,'l') ){
	  d = readdir(dir);
	  while( d!= NULL ) {
	    if( !( !strchr(cont.opt,'a') && d->d_name[0] == '.') ) {
	      permissions( d->d_name );
	      printf("\n");
	    }
	    d = readdir(dir);
	  }
	}
      else {
	d = readdir(dir);
	while( d!=NULL ) {
	  printf("%s\n",d->d_name);
	  d = readdir(dir);
	}
      }
    }
  }  
}
