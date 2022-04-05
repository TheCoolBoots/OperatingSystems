#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int main(void)
{
   int i = 0;

   while (fork() && i < 5)
   {
      wait(NULL);
      printf("Yo!");
      fflush(stdout);
      i++;
   }
   printf("%d", i);
   return 0;
}