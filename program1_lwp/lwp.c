#include <lwp.h>

int new_lwp(lwpfun functionPointer, void * argument, size_t words){
    int *sp = (int*) malloc(4 * words);
    sp += words;

    // push the argument to the stack
    sp -= 1;
    *sp = argument;

    // push return address to stack
    sp -= 1;
    // change -1 to be &lwp_exit eventually
    *sp = -1;

    // push functionPointer to stack
    sp -= 1;
    *sp = functionPointer;

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
    *sp = bbpAddr;


}