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
	salq	$2, %rax
	movq	%rax, %rdi
	call	malloc@PLT
	movq	%rax, -56(%rbp)
	movq	-88(%rbp), %rax
	leaq	0(,%rax,4), %rdx
	movq	-56(%rbp), %rax
	addq	%rdx, %rax
	movq	%rax, -48(%rbp)
	subq	$4, -48(%rbp)
	movq	-80(%rbp), %rax
	movl	%eax, %edx
	movq	-48(%rbp), %rax
	movl	%edx, (%rax)
	subq	$4, -48(%rbp)
	movq	-48(%rbp), %rax
	movl	$-1, (%rax)
	subq	$4, -48(%rbp)
	movq	-72(%rbp), %rax
	movl	%eax, %edx
	movq	-48(%rbp), %rax
	movl	%edx, (%rax)
	subq	$4, -48(%rbp)
	movq	-48(%rbp), %rax
	movl	$-1, (%rax)
	movq	-48(%rbp), %rax
	movq	%rax, -40(%rbp)
	subq	$24, -48(%rbp)
	movq	-48(%rbp), %rax
	movl	$26214, (%rax)
	movq	-48(%rbp), %rax
	addq	$4, %rax
	movl	$21845, (%rax)
	movq	-48(%rbp), %rax
	addq	$8, %rax
	movl	$17476, (%rax)
	movq	-48(%rbp), %rax
	addq	$12, %rax
	movl	$13107, (%rax)
	movq	-48(%rbp), %rax
	addq	$16, %rax
	movl	$8738, (%rax)
	movq	-48(%rbp), %rax
	addq	$20, %rax
	movl	$4369, (%rax)
	subq	$28, -48(%rbp)
	movq	-40(%rbp), %rax
	movl	%eax, %edx
	movq	-48(%rbp), %rax
	movl	%edx, (%rax)
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
	subq	$16, %rsp
	movl	lwp_procs(%rip), %eax
	testl	%eax, %eax
	je	.L10
#APP
# 86 "lwp.c" 1
	pushq %rax
# 0 "" 2
# 86 "lwp.c" 1
	pushq %rbx
# 0 "" 2
# 86 "lwp.c" 1
	pushq %rcx
# 0 "" 2
# 86 "lwp.c" 1
	pushq %rdx
# 0 "" 2
# 86 "lwp.c" 1
	pushq %rsi
# 0 "" 2
# 86 "lwp.c" 1
	pushq %rdi
# 0 "" 2
# 86 "lwp.c" 1
	pushq %r8
# 0 "" 2
# 86 "lwp.c" 1
	pushq %r9
# 0 "" 2
# 86 "lwp.c" 1
	pushq %r10
# 0 "" 2
# 86 "lwp.c" 1
	pushq %r11
# 0 "" 2
# 86 "lwp.c" 1
	pushq %r12
# 0 "" 2
# 86 "lwp.c" 1
	pushq %r13
# 0 "" 2
# 86 "lwp.c" 1
	pushq %r14
# 0 "" 2
# 86 "lwp.c" 1
	pushq %r15
# 0 "" 2
# 86 "lwp.c" 1
	pushq %rbp
# 0 "" 2
#NO_APP
	movl	lwp_running(%rip), %eax
	cmpl	$-1, %eax
	je	.L6
	movl	lwp_running(%rip), %edx
#APP
# 90 "lwp.c" 1
	movq  %rsp,%rax
# 0 "" 2
#NO_APP
	movslq	%edx, %rdx
	movq	%rdx, %rcx
	salq	$5, %rcx
	leaq	24+lwp_ptable(%rip), %rdx
	movq	%rax, (%rcx,%rdx)
	jmp	.L7
.L6:
#APP
# 94 "lwp.c" 1
	movq  %rsp,%rax
# 0 "" 2
#NO_APP
	movq	%rax, mainSP(%rip)
.L7:
	movq	schedulingFunction(%rip), %rax
	testq	%rax, %rax
	jne	.L8
	movl	lwp_running(%rip), %eax
	addl	$1, %eax
	movl	lwp_procs(%rip), %ecx
	cltd
	idivl	%ecx
	movl	%edx, -4(%rbp)
	jmp	.L9
.L8:
	movq	schedulingFunction(%rip), %rax
	call	*%rax
	movl	%eax, -4(%rbp)
.L9:
	movl	-4(%rbp), %eax
	cltq
	salq	$5, %rax
	movq	%rax, %rdx
	leaq	24+lwp_ptable(%rip), %rax
	movq	(%rdx,%rax), %rax
#APP
# 107 "lwp.c" 1
	movq  %rax,%rsp
# 0 "" 2
#NO_APP
	movl	-4(%rbp), %eax
	movl	%eax, lwp_running(%rip)
#APP
# 110 "lwp.c" 1
	popq  %rbp
# 0 "" 2
# 110 "lwp.c" 1
	popq  %r15
# 0 "" 2
# 110 "lwp.c" 1
	popq  %r14
# 0 "" 2
# 110 "lwp.c" 1
	popq  %r13
# 0 "" 2
# 110 "lwp.c" 1
	popq  %r12
# 0 "" 2
# 110 "lwp.c" 1
	popq  %r11
# 0 "" 2
# 110 "lwp.c" 1
	popq  %r10
# 0 "" 2
# 110 "lwp.c" 1
	popq  %r9
# 0 "" 2
# 110 "lwp.c" 1
	popq  %r8
# 0 "" 2
# 110 "lwp.c" 1
	popq  %rdi
# 0 "" 2
# 110 "lwp.c" 1
	popq  %rsi
# 0 "" 2
# 110 "lwp.c" 1
	popq  %rdx
# 0 "" 2
# 110 "lwp.c" 1
	popq  %rcx
# 0 "" 2
# 110 "lwp.c" 1
	popq  %rbx
# 0 "" 2
# 110 "lwp.c" 1
	popq  %rax
# 0 "" 2
# 110 "lwp.c" 1
	movq  %rbp,%rsp
# 0 "" 2
#NO_APP
	jmp	.L3
.L10:
	nop
.L3:
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE7:
	.size	lwp_start, .-lwp_start
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
