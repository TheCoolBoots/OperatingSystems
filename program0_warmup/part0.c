#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int main(void)
{
   int i = 0;
   int forkVal;
   printf("root pid: %d\n", getpid());

   while ((forkVal = fork()) && i < 1)
   {
      wait(NULL);
      printf("inside: %d %d %d ", getpid(), forkVal, i);

      i++;
   }

   printf("outside: %d %d %d ", getpid(), forkVal, i);
   return 0;
}

// 0 Yo!1 Yo!Yo!2 Yo!Yo!Yo!3 Yo!Yo!Yo!Yo!4 Yo!Yo!Yo!Yo!Yo!5 Yo!Yo!Yo!Yo!Yo!5