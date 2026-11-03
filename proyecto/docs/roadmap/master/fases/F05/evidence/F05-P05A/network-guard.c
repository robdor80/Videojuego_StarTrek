#define _GNU_SOURCE
#include <dlfcn.h>
#include <sys/socket.h>
#include <errno.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
static void denied(void) {const char *p=getenv("F05_NETWORK_ATTEMPTS");if(p){int f=open(p,O_WRONLY|O_CREAT|O_APPEND,0600);if(f>=0){write(f,"internet socket denied\n",23);close(f);}}errno=ENETDOWN;}
int socket(int domain,int type,int protocol){if(domain==AF_INET||domain==AF_INET6){denied();return -1;}int(*real)(int,int,int)=dlsym(RTLD_NEXT,"socket");return real(domain,type,protocol);}
int connect(int fd,const struct sockaddr *addr,socklen_t n){if(addr&&(addr->sa_family==AF_INET||addr->sa_family==AF_INET6)){denied();return -1;}int(*real)(int,const struct sockaddr*,socklen_t)=dlsym(RTLD_NEXT,"connect");return real(fd,addr,n);}
