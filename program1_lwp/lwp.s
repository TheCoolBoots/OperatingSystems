	.file	"lwp.c"
	.text
	.globl	schedulingFunction
	.bss
	.align 8
	.type	schedulingFunction, @object
	.size	schedulingFunction, 8
schedulingFunction:
	.zero	8
	.globl	mainSP
	.align 8
	.type	mainSP, @object
	.size	mainSP, 8
mainSP:
	.zero	8
	.comm	lwp_ptable,960,32
	.globl	lwp_procs
	.align 4
	.type	lwp_procs, @object
	.size	lwp_procs, 4
lwp_procs:
	.zero	4
	.globl	lwp_running
	.data
	.align 4
	.type	lwp_running, @object
	.size	lwp_running, 4
lwp_running:
	.long	-1
	.text
	.globl	new_lwp
	.type	new_lwp, @function
new_lwp:
.LFB6:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$96, %rsp
	movq	%rdi, -72(%rbp)
	movq	%rsi, -80(%rbp)
	movq	%rdx, -88(%rbp)
	movq	-88(%rbp), %rax
	salq	$3, %rax
	movq	%rax, %rdi
	call	malloc@PLT
	movq	%rax, -56(%rbp)
	movq	-88(%rbp), %rax
	addq	$1, %rax
	leaq	0(,%rax,8), %rdx
	movq	-56(%rbp), %rax
	addq	%rdx, %rax
	movq	%rax, -48(%rbp)
	subq	$8, -48(%rbp)
	movq	-80(%rbp), %rdx
	movq	-48(%rbp), %rax
	movq	%rdx, (%rax)
	subq	$8, -48(%rbp)
	leaq	lwp_exit(%rip), %rdx
	movq	-48(%rbp), %rax
	movq	%rdx, (%rax)
	subq	$8, -48(%rbp)
	movq	-72(%rbp), %rdx
	movq	-48(%rbp), %rax
	movq	%rdx, (%rax)
	subq	$8, -48(%rbp)
	movq	-48(%rbp), %rax
	movq	$999, (%rax)
	movq	-48(%rbp), %rax
	movq	%rax, -40(%rbp)
	subq	$48, -48(%rbp)
	movq	-48(%rbp), %rax
	movq	$26214, (%rax)
	movq	-48(%rbp), %rax
	addq	$8, %rax
	movq	$21845, (%rax)
	movq	-48(%rbp), %rax
	addq	$16, %rax
	movq	$17476, (%rax)
	movq	-48(%rbp), %rax
	addq	$24, %rax
	movq	$13107, (%rax)
	movq	-48(%rbp), %rax
	addq	$32, %rax
	movq	$8738, (%rax)
	movq	-48(%rbp), %rax
	addq	$40, %rax
	movq	$4369, (%rax)
	subq	$8, -48(%rbp)
	movq	-40(%rbp), %rdx
	movq	-48(%rbp), %rax
	movq	%rdx, (%rax)
	movl	lwp_procs(%rip), %eax
	cltq
	movq	%rax, -32(%rbp)
	movq	-48(%rbp), %rax
	movq	%rax, -8(%rbp)
	movq	-56(%rbp), %rax
	movq	%rax, -24(%rbp)
	movq	-88(%rbp), %rax
	movq	%rax, -16(%rbp)
	movl	lwp_procs(%rip), %eax
	cltq
	salq	$5, %rax
	movq	%rax, %rsi
	leaq	lwp_ptable(%rip), %rcx
	movq	-32(%rbp), %rax
	movq	-24(%rbp), %rdx
	movq	%rax, (%rsi,%rcx)
	movq	%rdx, 8(%rsi,%rcx)
	movq	-16(%rbp), %rax
	movq	-8(%rbp), %rdx
	movq	%rax, 16(%rsi,%rcx)
	movq	%rdx, 24(%rsi,%rcx)
	movl	lwp_procs(%rip), %eax
	addl	$1, %eax
	movl	%eax, lwp_procs(%rip)
	movl	$1, %eax
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE6:
	.size	new_lwp, .-new_lwp
	.globl	lwp_start
	.type	lwp_start, @function
lwp_start:
.LFB7:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	movl	lwp_procs(%rip), %eax
	testl	%eax, %eax
	je	.L6
#APP
# 88 "lwp.c" 1
	pushq %rax
# 0 "" 2
# 88 "lwp.c" 1
	pushq %rbx
# 0 "" 2
# 88 "lwp.c" 1
	pushq %rcx
# 0 "" 2
# 88 "lwp.c" 1
	pushq %rdx
# 0 "" 2
# 88 "lwp.c" 1
	pushq %rsi
# 0 "" 2
# 88 "lwp.c" 1
	pushq %rdi
# 0 "" 2
# 88 "lwp.c" 1
	pushq %r8
# 0 "" 2
# 88 "lwp.c" 1
	pushq %r9
# 0 "" 2
# 88 "lwp.c" 1
	pushq %r10
# 0 "" 2
# 88 "lwp.c" 1
	pushq %r11
# 0 "" 2
# 88 "lwp.c" 1
	pushq %r12
# 0 "" 2
# 88 "lwp.c" 1
	pushq %r13
# 0 "" 2
# 88 "lwp.c" 1
	pushq %r14
# 0 "" 2
# 88 "lwp.c" 1
	pushq %r15
# 0 "" 2
# 88 "lwp.c" 1
	pushq %rbp
# 0 "" 2
# 90 "lwp.c" 1
	movq  %rsp,%rax
# 0 "" 2
#NO_APP
	movq	%rax, mainSP(%rip)
	movl	$0, -4(%rbp)
	movl	-4(%rbp), %eax
	cltq
	salq	$5, %rax
	movq	%rax, %rdx
	leaq	24+lwp_ptable(%rip), %rax
	movq	(%rdx,%rax), %rax
#APP
# 97 "lwp.c" 1
	movq  %rax,%rsp
# 0 "" 2
#NO_APP
	movl	-4(%rbp), %eax
	movl	%eax, lwp_running(%rip)
#APP
# 100 "lwp.c" 1
	popq  %rbp
# 0 "" 2
# 100 "lwp.c" 1
	popq  %r15
# 0 "" 2
# 100 "lwp.c" 1
	popq  %r14
# 0 "" 2
# 100 "lwp.c" 1
	popq  %r13
# 0 "" 2
# 100 "lwp.c" 1
	popq  %r12
# 0 "" 2
# 100 "lwp.c" 1
	popq  %r11
# 0 "" 2
# 100 "lwp.c" 1
	popq  %r10
# 0 "" 2
# 100 "lwp.c" 1
	popq  %r9
# 0 "" 2
# 100 "lwp.c" 1
	popq  %r8
# 0 "" 2
# 100 "lwp.c" 1
	popq  %rdi
# 0 "" 2
# 100 "lwp.c" 1
	popq  %rsi
# 0 "" 2
# 100 "lwp.c" 1
	popq  %rdx
# 0 "" 2
# 100 "lwp.c" 1
	popq  %rcx
# 0 "" 2
# 100 "lwp.c" 1
	popq  %rbx
# 0 "" 2
# 100 "lwp.c" 1
	popq  %rax
# 0 "" 2
# 100 "lwp.c" 1
	movq  %rbp,%rsp
# 0 "" 2
#NO_APP
	jmp	.L3
.L6:
	nop
.L3:
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE7:
	.size	lwp_start, .-lwp_start
	.globl	lwp_yield
	.type	lwp_yield, @function
lwp_yield:
.LFB8:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$16, %rsp
#APP
# 107 "lwp.c" 1
	pushq %rax
# 0 "" 2
# 107 "lwp.c" 1
	pushq %rbx
# 0 "" 2
# 107 "lwp.c" 1
	pushq %rcx
# 0 "" 2
# 107 "lwp.c" 1
	pushq %rdx
# 0 "" 2
# 107 "lwp.c" 1
	pushq %rsi
# 0 "" 2
# 107 "lwp.c" 1
	pushq %rdi
# 0 "" 2
# 107 "lwp.c" 1
	pushq %r8
# 0 "" 2
# 107 "lwp.c" 1
	pushq %r9
# 0 "" 2
# 107 "lwp.c" 1
	pushq %r10
# 0 "" 2
# 107 "lwp.c" 1
	pushq %r11
# 0 "" 2
# 107 "lwp.c" 1
	pushq %r12
# 0 "" 2
# 107 "lwp.c" 1
	pushq %r13
# 0 "" 2
# 107 "lwp.c" 1
	pushq %r14
# 0 "" 2
# 107 "lwp.c" 1
	pushq %r15
# 0 "" 2
# 107 "lwp.c" 1
	pushq %rbp
# 0 "" 2
#NO_APP
	movl	lwp_running(%rip), %edx
#APP
# 109 "lwp.c" 1
	movq  %rsp,%rax
# 0 "" 2
#NO_APP
	movslq	%edx, %rdx
	movq	%rdx, %rcx
	salq	$5, %rcx
	leaq	24+lwp_ptable(%rip), %rdx
	movq	%rax, (%rcx,%rdx)
	movl	$0, %eax
	call	getScheduledThread
	movl	%eax, -4(%rbp)
	movl	-4(%rbp), %eax
	cltq
	salq	$5, %rax
	movq	%rax, %rdx
	leaq	24+lwp_ptable(%rip), %rax
	movq	(%rdx,%rax), %rax
#APP
# 115 "lwp.c" 1
	movq  %rax,%rsp
# 0 "" 2
#NO_APP
	movl	-4(%rbp), %eax
	movl	%eax, lwp_running(%rip)
#APP
# 118 "lwp.c" 1
	popq  %rbp
# 0 "" 2
# 118 "lwp.c" 1
	popq  %r15
# 0 "" 2
# 118 "lwp.c" 1
	popq  %r14
# 0 "" 2
# 118 "lwp.c" 1
	popq  %r13
# 0 "" 2
# 118 "lwp.c" 1
	popq  %r12
# 0 "" 2
# 118 "lwp.c" 1
	popq  %r11
# 0 "" 2
# 118 "lwp.c" 1
	popq  %r10
# 0 "" 2
# 118 "lwp.c" 1
	popq  %r9
# 0 "" 2
# 118 "lwp.c" 1
	popq  %r8
# 0 "" 2
# 118 "lwp.c" 1
	popq  %rdi
# 0 "" 2
# 118 "lwp.c" 1
	popq  %rsi
# 0 "" 2
# 118 "lwp.c" 1
	popq  %rdx
# 0 "" 2
# 118 "lwp.c" 1
	popq  %rcx
# 0 "" 2
# 118 "lwp.c" 1
	popq  %rbx
# 0 "" 2
# 118 "lwp.c" 1
	popq  %rax
# 0 "" 2
# 118 "lwp.c" 1
	movq  %rbp,%rsp
# 0 "" 2
#NO_APP
	nop
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE8:
	.size	lwp_yield, .-lwp_yield
	.globl	getScheduledThread
	.type	getScheduledThread, @function
getScheduledThread:
.LFB9:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	movq	schedulingFunction(%rip), %rax
	testq	%rax, %rax
	jne	.L10
	movl	$0, %eax
	call	roundRobinScheduling
	jmp	.L11
.L10:
	movq	schedulingFunction(%rip), %rax
	call	*%rax
.L11:
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE9:
	.size	getScheduledThread, .-getScheduledThread
	.globl	roundRobinScheduling
	.type	roundRobinScheduling, @function
roundRobinScheduling:
.LFB10:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	movl	$1, %eax
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE10:
	.size	roundRobinScheduling, .-roundRobinScheduling
	.globl	lwp_set_scheduler
	.type	lwp_set_scheduler, @function
lwp_set_scheduler:
.LFB11:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	movq	%rdi, -8(%rbp)
	movq	-8(%rbp), %rax
	movq	%rax, schedulingFunction(%rip)
	nop
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE11:
	.size	lwp_set_scheduler, .-lwp_set_scheduler
	.globl	lwp_exit
	.type	lwp_exit, @function
lwp_exit:
.LFB12:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	nop
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE12:
	.size	lwp_exit, .-lwp_exit
	.ident	"GCC: (Ubuntu 9.4.0-1ubuntu1~20.04.1) 9.4.0"
	.section	.note.GNU-stack,"",@progbits
	.section	.note.gnu.property,"a"
	.align 8
	.long	 1f - 0f
	.long	 4f - 1f
	.long	 5
0:
	.string	 "GNU"
1:
	.align 8
	.long	 0xc0000002
	.long	 3f - 2f
2:
	.long	 0x3
3:
	.align 8
4:
