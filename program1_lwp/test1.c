#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include "lwp.h"

#define MAXSNAKES  100
#define INITIALSTACK 2048

typedef void (*sigfun)(int signum);
static void indentnum(void *num);

int AlwaysZero() {
  return 0;
}

int main(int argc, char *argv[]){
    lwp_set_scheduler(AlwaysZero);
    new_lwp(indentnum,(void*)1,INITIALSTACK);
    lwp_start();
    return 0;
}

static void indentnum(void *num) {
    printf("Finished One Thing");
    lwp_exit();
}

