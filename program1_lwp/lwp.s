	.file	"lwp.c"
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
.LFB2:
	.cfi_startproc
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
	call	malloc
	movq	%rax, -8(%rbp)
	movq	-88(%rbp), %rax
	addq	$1, %rax
	leaq	0(,%rax,8), %rdx
	movq	-8(%rbp), %rax
	addq	%rdx, %rax
	movq	%rax, -16(%rbp)
	subq	$8, -16(%rbp)
	movq	-80(%rbp), %rdx
	movq	-16(%rbp), %rax
	movq	%rdx, (%rax)
	subq	$8, -16(%rbp)
	movl	$lwp_exit, %edx
	movq	-16(%rbp), %rax
	movq	%rdx, (%rax)
	subq	$8, -16(%rbp)
	movq	-72(%rbp), %rdx
	movq	-16(%rbp), %rax
	movq	%rdx, (%rax)
	subq	$8, -16(%rbp)
	movq	-16(%rbp), %rax
	movq	$999, (%rax)
	movq	-16(%rbp), %rax
	movq	%rax, -24(%rbp)
	subq	$48, -16(%rbp)
	movq	-16(%rbp), %rax
	movq	$26214, (%rax)
	movq	-16(%rbp), %rax
	addq	$8, %rax
	movq	$21845, (%rax)
	movq	-16(%rbp), %rax
	addq	$16, %rax
	movq	$17476, (%rax)
	movq	-16(%rbp), %rax
	addq	$24, %rax
	movq	$13107, (%rax)
	movq	-16(%rbp), %rax
	addq	$32, %rax
	movq	$8738, (%rax)
	movq	-16(%rbp), %rax
	addq	$40, %rax
	movq	$4369, (%rax)
	subq	$8, -16(%rbp)
	movq	-24(%rbp), %rdx
	movq	-16(%rbp), %rax
	movq	%rdx, (%rax)
	movl	lwp_procs(%rip), %eax
	cltq
	movq	%rax, -64(%rbp)
	movq	-16(%rbp), %rax
	movq	%rax, -40(%rbp)
	movq	-8(%rbp), %rax
	movq	%rax, -56(%rbp)
	movq	-88(%rbp), %rax
	movq	%rax, -48(%rbp)
	movl	lwp_procs(%rip), %eax
	cltq
	salq	$5, %rax
	addq	$lwp_ptable, %rax
	movq	-64(%rbp), %rdx
	movq	%rdx, (%rax)
	movq	-56(%rbp), %rdx
	movq	%rdx, 8(%rax)
	movq	-48(%rbp), %rdx
	movq	%rdx, 16(%rax)
	movq	-40(%rbp), %rdx
	movq	%rdx, 24(%rax)
	movl	lwp_procs(%rip), %eax
	addl	$1, %eax
	movl	%eax, lwp_procs(%rip)
	movl	$1, %eax
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE2:
	.size	new_lwp, .-new_lwp
	.globl	lwp_start
	.type	lwp_start, @function
lwp_start:
.LFB3:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$16, %rsp
	movl	lwp_procs(%rip), %eax
	testl	%eax, %eax
	jne	.L4
	jmp	.L3
.L4:
#APP
# 74 "lwp.c" 1
	pushq %rax
# 0 "" 2
# 74 "lwp.c" 1
	pushq %rbx
# 0 "" 2
# 74 "lwp.c" 1
	pushq %rcx
# 0 "" 2
# 74 "lwp.c" 1
	pushq %rdx
# 0 "" 2
# 74 "lwp.c" 1
	pushq %rsi
# 0 "" 2
# 74 "lwp.c" 1
	pushq %rdi
# 0 "" 2
# 74 "lwp.c" 1
	pushq %r8
# 0 "" 2
# 74 "lwp.c" 1
	pushq %r9
# 0 "" 2
# 74 "lwp.c" 1
	pushq %r10
# 0 "" 2
# 74 "lwp.c" 1
	pushq %r11
# 0 "" 2
# 74 "lwp.c" 1
	pushq %r12
# 0 "" 2
# 74 "lwp.c" 1
	pushq %r13
# 0 "" 2
# 74 "lwp.c" 1
	pushq %r14
# 0 "" 2
# 74 "lwp.c" 1
	pushq %r15
# 0 "" 2
# 74 "lwp.c" 1
	pushq %rbp
# 0 "" 2
# 76 "lwp.c" 1
	movq  %rsp,%rax
# 0 "" 2
#NO_APP
	movq	%rax, mainSP(%rip)
	movl	$0, %eax
	call	getScheduledThread
	movl	%eax, -4(%rbp)
	movl	-4(%rbp), %eax
	cltq
	salq	$5, %rax
	addq	$lwp_ptable+16, %rax
	movq	8(%rax), %rax
#APP
# 83 "lwp.c" 1
	movq  %rax,%rsp
# 0 "" 2
#NO_APP
	movl	-4(%rbp), %eax
	movl	%eax, lwp_running(%rip)
#APP
# 86 "lwp.c" 1
	popq  %rbp
# 0 "" 2
# 86 "lwp.c" 1
	popq  %r15
# 0 "" 2
# 86 "lwp.c" 1
	popq  %r14
# 0 "" 2
# 86 "lwp.c" 1
	popq  %r13
# 0 "" 2
# 86 "lwp.c" 1
	popq  %r12
# 0 "" 2
# 86 "lwp.c" 1
	popq  %r11
# 0 "" 2
# 86 "lwp.c" 1
	popq  %r10
# 0 "" 2
# 86 "lwp.c" 1
	popq  %r9
# 0 "" 2
# 86 "lwp.c" 1
	popq  %r8
# 0 "" 2
# 86 "lwp.c" 1
	popq  %rdi
# 0 "" 2
# 86 "lwp.c" 1
	popq  %rsi
# 0 "" 2
# 86 "lwp.c" 1
	popq  %rdx
# 0 "" 2
# 86 "lwp.c" 1
	popq  %rcx
# 0 "" 2
# 86 "lwp.c" 1
	popq  %rbx
# 0 "" 2
# 86 "lwp.c" 1
	popq  %rax
# 0 "" 2
# 86 "lwp.c" 1
	movq  %rbp,%rsp
# 0 "" 2
#NO_APP
	nop
.L3:
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE3:
	.size	lwp_start, .-lwp_start
	.globl	lwp_yield
	.type	lwp_yield, @function
lwp_yield:
.LFB4:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$16, %rsp
#APP
# 94 "lwp.c" 1
	pushq %rax
# 0 "" 2
# 94 "lwp.c" 1
	pushq %rbx
# 0 "" 2
# 94 "lwp.c" 1
	pushq %rcx
# 0 "" 2
# 94 "lwp.c" 1
	pushq %rdx
# 0 "" 2
# 94 "lwp.c" 1
	pushq %rsi
# 0 "" 2
# 94 "lwp.c" 1
	pushq %rdi
# 0 "" 2
# 94 "lwp.c" 1
	pushq %r8
# 0 "" 2
# 94 "lwp.c" 1
	pushq %r9
# 0 "" 2
# 94 "lwp.c" 1
	pushq %r10
# 0 "" 2
# 94 "lwp.c" 1
	pushq %r11
# 0 "" 2
# 94 "lwp.c" 1
	pushq %r12
# 0 "" 2
# 94 "lwp.c" 1
	pushq %r13
# 0 "" 2
# 94 "lwp.c" 1
	pushq %r14
# 0 "" 2
# 94 "lwp.c" 1
	pushq %r15
# 0 "" 2
# 94 "lwp.c" 1
	pushq %rbp
# 0 "" 2
#NO_APP
	movl	lwp_running(%rip), %edx
#APP
# 96 "lwp.c" 1
	movq  %rsp,%rax
# 0 "" 2
#NO_APP
	movslq	%edx, %rdx
	salq	$5, %rdx
	addq	$lwp_ptable+16, %rdx
	movq	%rax, 8(%rdx)
	movl	$0, %eax
	call	getScheduledThread
	movl	%eax, -4(%rbp)
	movl	-4(%rbp), %eax
	cltq
	salq	$5, %rax
	addq	$lwp_ptable+16, %rax
	movq	8(%rax), %rax
#APP
# 102 "lwp.c" 1
	movq  %rax,%rsp
# 0 "" 2
#NO_APP
	movl	-4(%rbp), %eax
	movl	%eax, lwp_running(%rip)
#APP
# 106 "lwp.c" 1
	popq  %rbp
# 0 "" 2
# 106 "lwp.c" 1
	popq  %r15
# 0 "" 2
# 106 "lwp.c" 1
	popq  %r14
# 0 "" 2
# 106 "lwp.c" 1
	popq  %r13
# 0 "" 2
# 106 "lwp.c" 1
	popq  %r12
# 0 "" 2
# 106 "lwp.c" 1
	popq  %r11
# 0 "" 2
# 106 "lwp.c" 1
	popq  %r10
# 0 "" 2
# 106 "lwp.c" 1
	popq  %r9
# 0 "" 2
# 106 "lwp.c" 1
	popq  %r8
# 0 "" 2
# 106 "lwp.c" 1
	popq  %rdi
# 0 "" 2
# 106 "lwp.c" 1
	popq  %rsi
# 0 "" 2
# 106 "lwp.c" 1
	popq  %rdx
# 0 "" 2
# 106 "lwp.c" 1
	popq  %rcx
# 0 "" 2
# 106 "lwp.c" 1
	popq  %rbx
# 0 "" 2
# 106 "lwp.c" 1
	popq  %rax
# 0 "" 2
# 106 "lwp.c" 1
	movq  %rbp,%rsp
# 0 "" 2
#NO_APP
	nop
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE4:
	.size	lwp_yield, .-lwp_yield
	.globl	lwp_set_scheduler
	.type	lwp_set_scheduler, @function
lwp_set_scheduler:
.LFB5:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	movq	%rdi, -8(%rbp)
	movq	-8(%rbp), %rax
	movq	%rax, schedulingFunction(%rip)
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE5:
	.size	lwp_set_scheduler, .-lwp_set_scheduler
	.globl	lwp_exit
	.type	lwp_exit, @function
lwp_exit:
.LFB6:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$16, %rsp
	movl	lwp_running(%rip), %eax
	movl	%eax, -4(%rbp)
	jmp	.L10
.L11:
	movl	-4(%rbp), %eax
	leal	1(%rax), %edx
	movl	-4(%rbp), %eax
	cltq
	salq	$5, %rax
	addq	$lwp_ptable, %rax
	movslq	%edx, %rdx
	salq	$5, %rdx
	addq	$lwp_ptable, %rdx
	movq	(%rdx), %rcx
	movq	%rcx, (%rax)
	movq	8(%rdx), %rcx
	movq	%rcx, 8(%rax)
	movq	16(%rdx), %rcx
	movq	%rcx, 16(%rax)
	movq	24(%rdx), %rdx
	movq	%rdx, 24(%rax)
	addl	$1, -4(%rbp)
.L10:
	movl	lwp_procs(%rip), %eax
	subl	$1, %eax
	cmpl	-4(%rbp), %eax
	jg	.L11
	movl	lwp_procs(%rip), %eax
	subl	$1, %eax
	movl	%eax, lwp_procs(%rip)
	movl	lwp_running(%rip), %eax
	subl	$1, %eax
	movl	%eax, lwp_running(%rip)
	movl	lwp_procs(%rip), %eax
	testl	%eax, %eax
	jne	.L12
	movl	$0, %eax
	call	lwp_stop
	jmp	.L9
.L12:
	movl	$0, %eax
	call	getScheduledThread
	movl	%eax, lwp_running(%rip)
	movl	lwp_running(%rip), %eax
	cltq
	salq	$5, %rax
	addq	$lwp_ptable+16, %rax
	movq	8(%rax), %rax
#APP
# 138 "lwp.c" 1
	movq  %rax,%rsp
# 0 "" 2
# 139 "lwp.c" 1
	popq  %rbp
# 0 "" 2
# 139 "lwp.c" 1
	popq  %r15
# 0 "" 2
# 139 "lwp.c" 1
	popq  %r14
# 0 "" 2
# 139 "lwp.c" 1
	popq  %r13
# 0 "" 2
# 139 "lwp.c" 1
	popq  %r12
# 0 "" 2
# 139 "lwp.c" 1
	popq  %r11
# 0 "" 2
# 139 "lwp.c" 1
	popq  %r10
# 0 "" 2
# 139 "lwp.c" 1
	popq  %r9
# 0 "" 2
# 139 "lwp.c" 1
	popq  %r8
# 0 "" 2
# 139 "lwp.c" 1
	popq  %rdi
# 0 "" 2
# 139 "lwp.c" 1
	popq  %rsi
# 0 "" 2
# 139 "lwp.c" 1
	popq  %rdx
# 0 "" 2
# 139 "lwp.c" 1
	popq  %rcx
# 0 "" 2
# 139 "lwp.c" 1
	popq  %rbx
# 0 "" 2
# 139 "lwp.c" 1
	popq  %rax
# 0 "" 2
# 139 "lwp.c" 1
	movq  %rbp,%rsp
# 0 "" 2
#NO_APP
.L9:
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE6:
	.size	lwp_exit, .-lwp_exit
	.globl	lwp_stop
	.type	lwp_stop, @function
lwp_stop:
.LFB7:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
#APP
# 145 "lwp.c" 1
	pushq %rax
# 0 "" 2
# 145 "lwp.c" 1
	pushq %rbx
# 0 "" 2
# 145 "lwp.c" 1
	pushq %rcx
# 0 "" 2
# 145 "lwp.c" 1
	pushq %rdx
# 0 "" 2
# 145 "lwp.c" 1
	pushq %rsi
# 0 "" 2
# 145 "lwp.c" 1
	pushq %rdi
# 0 "" 2
# 145 "lwp.c" 1
	pushq %r8
# 0 "" 2
# 145 "lwp.c" 1
	pushq %r9
# 0 "" 2
# 145 "lwp.c" 1
	pushq %r10
# 0 "" 2
# 145 "lwp.c" 1
	pushq %r11
# 0 "" 2
# 145 "lwp.c" 1
	pushq %r12
# 0 "" 2
# 145 "lwp.c" 1
	pushq %r13
# 0 "" 2
# 145 "lwp.c" 1
	pushq %r14
# 0 "" 2
# 145 "lwp.c" 1
	pushq %r15
# 0 "" 2
# 145 "lwp.c" 1
	pushq %rbp
# 0 "" 2
#NO_APP
	movq	mainSP(%rip), %rax
#APP
# 146 "lwp.c" 1
	movq  %rax,%rsp
# 0 "" 2
# 147 "lwp.c" 1
	popq  %rbp
# 0 "" 2
# 147 "lwp.c" 1
	popq  %r15
# 0 "" 2
# 147 "lwp.c" 1
	popq  %r14
# 0 "" 2
# 147 "lwp.c" 1
	popq  %r13
# 0 "" 2
# 147 "lwp.c" 1
	popq  %r12
# 0 "" 2
# 147 "lwp.c" 1
	popq  %r11
# 0 "" 2
# 147 "lwp.c" 1
	popq  %r10
# 0 "" 2
# 147 "lwp.c" 1
	popq  %r9
# 0 "" 2
# 147 "lwp.c" 1
	popq  %r8
# 0 "" 2
# 147 "lwp.c" 1
	popq  %rdi
# 0 "" 2
# 147 "lwp.c" 1
	popq  %rsi
# 0 "" 2
# 147 "lwp.c" 1
	popq  %rdx
# 0 "" 2
# 147 "lwp.c" 1
	popq  %rcx
# 0 "" 2
# 147 "lwp.c" 1
	popq  %rbx
# 0 "" 2
# 147 "lwp.c" 1
	popq  %rax
# 0 "" 2
# 147 "lwp.c" 1
	movq  %rbp,%rsp
# 0 "" 2
#NO_APP
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE7:
	.size	lwp_stop, .-lwp_stop
	.globl	getScheduledThread
	.type	getScheduledThread, @function
getScheduledThread:
.LFB8:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	movq	schedulingFunction(%rip), %rax
	testq	%rax, %rax
	jne	.L16
	movl	$0, %eax
	call	roundRobinScheduling
	jmp	.L17
.L16:
	movq	schedulingFunction(%rip), %rax
	call	*%rax
.L17:
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE8:
	.size	getScheduledThread, .-getScheduledThread
	.globl	roundRobinScheduling
	.type	roundRobinScheduling, @function
roundRobinScheduling:
.LFB9:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	movl	lwp_running(%rip), %eax
	addl	$1, %eax
	movl	lwp_procs(%rip), %ecx
	cltd
	idivl	%ecx
	movl	%edx, %eax
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE9:
	.size	roundRobinScheduling, .-roundRobinScheduling
	.ident	"GCC: (GNU) 4.8.5 20150623 (Red Hat 4.8.5-44)"
	.section	.note.GNU-stack,"",@progbits
