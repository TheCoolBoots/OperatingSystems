#include "lwp.h"
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

schedfun schedulingFunction = NULL;
int* mainSP = NULL;

int new_lwp(lwpfun functionPointer, void * argument, size_t words){
    int *stack = (int*) malloc(4 * words);
    int *sp = stack + words;

    // push the argument to the stack
    sp -= 1;
    *sp = (intptr_t) argument;

    // push return address to stack
    sp -= 1;
    // TODO: change -1 to be &lwp_exit
    *sp = -1;

    // push functionPointer to stack
    sp -= 1;
    // ASK PROFESSOR ABOUT THIS CAST
    *sp = (intptr_t) functionPointer;

    // push bogus base pointer to stack
    sp -= 1;
    *sp = -1;

    int* bbpAddr = sp;

    sp -= 6;
    *sp = 0x6666;
    *(sp + 1) = 0x5555;
    *(sp + 2) = 0x4444;
    *(sp + 3) = 0x3333;
    *(sp + 4) = 0x2222;
    *(sp + 5) = 0x1111;

    sp -= 7;
    *sp = (intptr_t) bbpAddr;

    if(lwp_procs == 0){
        //lwp_ptable = (lwp_context*) malloc(sizeof(lwp_context) * 256);
    }

    // create new context
    lwp_context newContext;
    newContext.pid = lwp_procs;
    newContext.sp = (ptr_int_t*) sp;
    newContext.stack = (ptr_int_t*) stack;
    // stacksize is number of words in stack not byte size of stack
    newContext.stacksize = words;

    lwp_ptable[lwp_procs] = newContext;
    lwp_procs += 1;

    return 1;
}


/*

lwp_new()
lwp_start()
lwp_yield()
lwp_new()
lwp_start()
lwp_yield()
lwp_exit()
lwp_start()
lwp_exit()

*/


void lwp_start(){
    // if there arent any threads to run, just return
    if(lwp_procs == 0){
        return;
    }

    // save current thread's context
    SAVE_STATE();

    // current thread is not main thread (may not need this check)
    if(lwp_running != -1){
        GetSP(lwp_ptable[lwp_running].sp);
    }
    // current thread is main thread
    else{
        GetSP(mainSP);
    }

    // select thread to run
    int threadToRun;
    if(schedulingFunction == NULL){
        threadToRun = (lwp_running + 1)%lwp_procs; 
    }
    else{
        threadToRun = schedulingFunction();
    }

    // set stack pointer to thread's stack pointer
    SetSP(lwp_ptable[threadToRun].sp);
    lwp_running = threadToRun;
    // load new thread's state
    RESTORE_STATE();

    // return (using the trick to jump into thread's function)
    return;
}

void lwp_set_scheduler(schedfun sched){
    schedulingFunction = sched;
}