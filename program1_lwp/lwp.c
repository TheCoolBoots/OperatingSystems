#include "lwp.h"
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int roundRobinScheduling();
int getScheduledThread();

schedfun schedulingFunction = NULL;
int* mainSP = NULL;

lwp_context lwp_ptable[LWP_PROC_LIMIT];
int lwp_procs = 0;
int lwp_running = -1;


int new_lwp(lwpfun functionPointer, void * argument, size_t words){
    ptr_int_t *stack = (ptr_int_t*) malloc(sizeof(ptr_int_t) * words);
    ptr_int_t *sp = stack + words + 1;

    // push the argument to the stack
    sp -= 1;
    *sp = (ptr_int_t) argument;

    // push return address to stack
    sp -= 1;
    // TODO: change -1 to be &lwp_exit
    *sp = (ptr_int_t) lwp_exit;

    // push functionPointer to stack
    sp -= 1;
    // ASK PROFESSOR ABOUT THIS CAST
    *sp = (ptr_int_t) functionPointer;

    // push bogus base pointer to stack
    sp -= 1;
    *sp = 999;

    ptr_int_t *bbpAddr = sp;

    sp -= 6;
    *sp = 0x6666;
    *(sp + 1) = 0x5555;
    *(sp + 2) = 0x4444;
    *(sp + 3) = 0x3333;
    *(sp + 4) = 0x2222;
    *(sp + 5) = 0x1111;

    sp -= 1;
    *sp = (ptr_int_t) bbpAddr;

    // create new context
    lwp_context newContext;
    newContext.pid = lwp_procs;
    newContext.sp = sp;
    newContext.stack = stack;
    // stacksize is number of words in stack not byte size of stack
    newContext.stacksize = words;

    lwp_ptable[lwp_procs] = newContext;
    lwp_procs += 1;

    return 1;
}


void lwp_start(){
    // if there arent any threads to run, just return
    if(lwp_procs == 0){
        return;
    }

    // save current thread's context
    SAVE_STATE();

    GetSP(mainSP);

    // select thread to run
    int threadToRun = getScheduledThread();
    // int threadToRun = 0;

    // set stack pointer to thread's stack pointer
    SetSP(lwp_ptable[threadToRun].sp);
    lwp_running = threadToRun;
    // load new thread's state
    RESTORE_STATE();

    // return (using the trick to jump into thread's function)
    return;
}


void lwp_yield(){
    SAVE_STATE();

    GetSP(lwp_ptable[lwp_running].sp);

    // select thread to run
    int threadToRun = getScheduledThread();

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


void lwp_exit(){
    // delete the current running entry in lwp_ptable
    // free(lwp_ptable[lwp_running].stack);

    // move subsequent entries to one lower
    int i;
    for(i = lwp_running; i < lwp_procs - 1; i++){
        lwp_ptable[i] = lwp_ptable[i + 1];
    } 

    // decrement lwp_procs
    lwp_procs -= 1;
    lwp_running -= 1;

    // if no more threads to run, stop lwp
    if(lwp_procs == 0){
        lwp_stop();
    }
    else{ 
        lwp_running = getScheduledThread();
        SetSP(lwp_ptable[lwp_running].sp);
        RESTORE_STATE();
    }
}


void lwp_stop(){
    SAVE_STATE();
    SetSP(mainSP);
    RESTORE_STATE();
}


int getScheduledThread(){
    if(schedulingFunction == NULL){
        // change this to round robin (each one gets equal time)
        return roundRobinScheduling();
    }
    else{
        return schedulingFunction();
    }
}


int roundRobinScheduling(){
    return (lwp_running + 1)%lwp_procs;
}