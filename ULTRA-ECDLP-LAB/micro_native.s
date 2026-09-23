	.file	"micro_main.cpp"
	.text
	.section .rdata,"dr"
.LC2:
	.ascii "EC,%s,affine_dbl,%.3f\12\0"
.LC3:
	.ascii "EC,%s,affine_add,%.3f\12\0"
.LC4:
	.ascii "EC,%s,jacobian_dbl,%.3f\12\0"
	.align 8
.LC5:
	.ascii "EC,%s,jacobian_mixed_add,%.3f\12\0"
.LC6:
	.ascii "EC,%s,jacobian_add,%.3f\12\0"
	.section	.text$_Z8bench_ecIN2fp7FpNaiveILj4294966177EEEEvPKc,"x"
	.linkonce discard
	.p2align 4
	.globl	_Z8bench_ecIN2fp7FpNaiveILj4294966177EEEEvPKc
	.def	_Z8bench_ecIN2fp7FpNaiveILj4294966177EEEEvPKc;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8bench_ecIN2fp7FpNaiveILj4294966177EEEEvPKc
_Z8bench_ecIN2fp7FpNaiveILj4294966177EEEEvPKc:
.LFB4618:
	pushq	%r15
	.seh_pushreg	%r15
	pushq	%r14
	.seh_pushreg	%r14
	pushq	%r13
	.seh_pushreg	%r13
	pushq	%r12
	.seh_pushreg	%r12
	pushq	%rbp
	.seh_pushreg	%rbp
	pushq	%rdi
	.seh_pushreg	%rdi
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$1192, %rsp
	.seh_stackalloc	1192
	vmovaps	%xmm6, 1136(%rsp)
	.seh_savexmm	%xmm6, 1136
	vmovaps	%xmm7, 1152(%rsp)
	.seh_savexmm	%xmm7, 1152
	vmovaps	%xmm8, 1168(%rsp)
	.seh_savexmm	%xmm8, 1168
	.seh_endprologue
	vmovsd	.LC0(%rip), %xmm8
	vmovsd	.LC1(%rip), %xmm6
	vxorps	%xmm7, %xmm7, %xmm7
	movl	$560815139, %ebx
	movl	$1960037684, %r15d
	movabsq	$-9223369633819947615, %r13
	movl	$4294966176, %edi
	movq	%rcx, 64(%rsp)
	leaq	112(%rsp), %rsi
	movl	$3, 48(%rsp)
	.p2align 4
	.p2align 3
.L26:
	movl	$0, 108(%rsp)
	movl	$4294966177, %ebp
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	xorl	%r11d, %r11d
	movq	%rax, 40(%rsp)
	.p2align 4
	.p2align 3
.L21:
	movl	%r15d, %r10d
	movzbl	%r11b, %eax
	movq	%r10, %rcx
	leaq	(%rsi,%rax,4), %r14
	imulq	%r10, %rcx
	movq	%rcx, %rax
	mulq	%r13
	shrq	$31, %rdx
	movq	%rdx, %rax
	imulq	%rbp, %rax
	subq	%rax, %rcx
	movq	%rcx, %rdx
	leal	(%rcx,%rcx), %r12d
	leaq	(%rcx,%rcx), %rcx
	cmpq	%rcx, %rdi
	leal	1119(%r12), %eax
	cmovb	%eax, %r12d
	movl	%r12d, %eax
	leal	1119(%r12,%rdx), %ecx
	addl	%edx, %r12d
	addq	%rdx, %rax
	leal	(%rbx,%rbx), %edx
	cmpq	%rax, %rdi
	movl	%ebx, %eax
	cmovb	%rcx, %r12
	addq	%rax, %rax
	leal	1119(%rdx), %ecx
	cmpq	%rax, %rdi
	jb	.L6
	movl	%edx, %ecx
	testl	%edx, %edx
	je	.L179
.L6:
	xorl	%r9d, %r9d
	movl	$1, %r8d
	movq	%rbp, %rax
	movl	%r15d, 32(%rsp)
	jmp	.L11
	.p2align 5
	.p2align 4
	.p2align 3
.L147:
	movq	%r15, %r8
.L11:
	cqto
	movq	%r9, %r15
	movq	%r8, %r9
	idivq	%rcx
	imulq	%r8, %rax
	subq	%rax, %r15
	movq	%rcx, %rax
	movq	%rdx, %rcx
	testq	%rdx, %rdx
	jne	.L147
	movl	32(%rsp), %r15d
	cmpq	$1, %rax
	jg	.L180
	testq	%r8, %r8
	leaq	(%r8,%rbp), %rax
	cmovs	%rax, %r8
	addq	%r10, %r10
	movl	%r8d, %r8d
	imulq	%r12, %r8
	movq	%r8, %rax
	mulq	%r13
	shrq	$31, %rdx
	movq	%rdx, %rax
	imulq	%rbp, %rax
	subq	%rax, %r8
	movq	%r8, %rcx
	movq	%r8, %r9
	imulq	%r8, %rcx
	leal	(%r15,%r15), %r8d
	movq	%rcx, %rax
	mulq	%r13
	leal	1119(%r8), %eax
	shrq	$31, %rdx
	imulq	%rbp, %rdx
	subq	%rdx, %rcx
	cmpq	%r10, %rdi
	cmovb	%eax, %r8d
	movl	%ecx, %edx
	cmpl	%r8d, %ecx
	jb	.L10
	movl	%ecx, %eax
	subl	%r8d, %eax
	movl	%eax, %r8d
.L16:
	cmpl	%r8d, %r15d
	jnb	.L9
	leal	-1119(%r15), %ecx
	movl	%r8d, %r15d
	subl	%r8d, %ecx
.L18:
	imulq	%r9, %rcx
	movl	%r8d, (%r14)
	movq	%rcx, %rax
	mulq	%r13
	movl	$-1119, %eax
	subl	%ebx, %eax
	shrq	$31, %rdx
	imulq	%rbp, %rdx
	subq	%rdx, %rcx
	movl	%ecx, %edx
	addl	%ecx, %eax
	subl	%ebx, %edx
	cmpl	%ebx, %ecx
	movl	%edx, %ebx
	cmovb	%eax, %ebx
	incq	%r11
	xorl	%r8d, 108(%rsp)
	cmpq	$3000000, %r11
	jne	.L21
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	subq	40(%rsp), %rax
	js	.L22
	vcvtsi2sdq	%rax, %xmm7, %xmm0
.L23:
	vdivsd	%xmm6, %xmm0, %xmm0
	decl	48(%rsp)
	movl	108(%rsp), %eax
	vminsd	%xmm8, %xmm0, %xmm2
	vmovapd	%xmm2, %xmm8
	jne	.L26
	movq	64(%rsp), %rdx
	leaq	.LC2(%rip), %rcx
	vmovq	%xmm2, %r8
	xorl	%ebp, %ebp
	movl	$560815139, %edi
	movl	$1960037684, %r15d
	movl	$4294966177, %ebx
	call	__mingw_printf
	vmovsd	.LC0(%rip), %xmm8
	movl	$3, 40(%rsp)
	.p2align 4
	.p2align 3
.L54:
	movl	$0, 104(%rsp)
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	xorl	%r8d, %r8d
	movq	%rax, 32(%rsp)
	.p2align 4
	.p2align 3
.L49:
	movzbl	%r8b, %eax
	leaq	(%rsi,%rax,4), %r10
	testb	%bpl, %bpl
	jne	.L149
	cmpl	$1960037684, %r15d
	je	.L181
	movl	$1960037684, %eax
	movl	$1960036565, %ecx
	movl	$560814020, %r11d
	movl	$1, %r12d
	subl	%r15d, %eax
	subl	%r15d, %ecx
	cmpl	$1960037684, %r15d
	cmovbe	%eax, %ecx
	movl	$560815139, %eax
	subl	%edi, %r11d
	subl	%edi, %eax
	cmpl	$560815139, %edi
	cmovbe	%rax, %r11
	xorl	%r9d, %r9d
	movq	%rbx, %rax
	jmp	.L39
	.p2align 5
	.p2align 4
	.p2align 3
.L153:
	movq	%r13, %r12
.L39:
	cqto
	idivq	%rcx
	imulq	%r12, %rax
	subq	%rax, %r9
	movq	%rcx, %rax
	movq	%rdx, %rcx
	movq	%r9, %r13
	movq	%r12, %r9
	testq	%rdx, %rdx
	jne	.L153
	cmpq	$1, %rax
	jg	.L182
	testq	%r12, %r12
	leaq	(%r12,%rbx), %rax
	cmovs	%rax, %r12
	movabsq	$-9223369633819947615, %rax
	movl	%r12d, %r12d
	imulq	%r11, %r12
	mulq	%r12
	movq	%r12, %r9
	shrq	$31, %rdx
	movq	%rdx, %rax
	imulq	%rbx, %rax
	subq	%rax, %r9
	movabsq	$-9223369633819947615, %rax
	movq	%r9, %rcx
	imulq	%r9, %rcx
	mulq	%rcx
	shrq	$31, %rdx
	imulq	%rbx, %rdx
	subq	%rdx, %rcx
	movl	%ecx, %eax
	cmpl	%r15d, %ecx
	jb	.L42
	subl	%r15d, %ecx
.L44:
	leal	-1960037684(%rcx), %eax
	leal	-1960038803(%rcx), %edx
	cmpl	$1960037684, %ecx
	cmovb	%edx, %eax
	movl	%eax, %ecx
	leal	-1119(%r15), %eax
	cmpl	%ecx, %r15d
	jb	.L176
	movl	%r15d, %eax
.L176:
	subl	%ecx, %eax
	movl	%ecx, %r15d
	imulq	%rax, %r9
	movabsq	$-9223369633819947615, %rax
	mulq	%r9
	movl	%r9d, %eax
	shrq	$31, %rdx
	imulq	%rbx, %rdx
	subl	%edx, %eax
.L41:
	movl	%eax, %ecx
	movl	$-1119, %edx
	subl	%edi, %edx
	subl	%edi, %ecx
	addl	%eax, %edx
	cmpl	%edi, %eax
	movl	%ecx, %edi
	cmovb	%edx, %edi
.L27:
	incq	%r8
	xorl	%r15d, 104(%rsp)
	movl	%r15d, (%r10)
	cmpq	$3000000, %r8
	jne	.L49
	movq	32(%rsp), %r13
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	subq	%r13, %rax
	js	.L50
	vcvtsi2sdq	%rax, %xmm7, %xmm0
.L51:
	vdivsd	%xmm6, %xmm0, %xmm0
	decl	40(%rsp)
	movl	104(%rsp), %eax
	vminsd	%xmm8, %xmm0, %xmm2
	vmovapd	%xmm2, %xmm8
	jne	.L54
	movq	64(%rsp), %rdx
	leaq	.LC3(%rip), %rcx
	vmovq	%xmm2, %r8
	movabsq	$-9223369633819947615, %rbp
	movl	$4294966177, %edi
	movl	$4294966176, %ebx
	movl	$560815139, %r12d
	call	__mingw_printf
	vmovsd	.LC0(%rip), %xmm8
	movl	$3, 48(%rsp)
	movl	$1960037684, %ecx
	.p2align 4
	.p2align 3
.L75:
	movl	%ecx, 40(%rsp)
	movl	$0, 100(%rsp)
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	xorl	%r13d, %r13d
	movq	%rax, 32(%rsp)
	movl	%r12d, %r9d
	movl	40(%rsp), %ecx
	.p2align 4
	.p2align 3
.L70:
	movl	%ecx, %r14d
	movl	%r9d, %r9d
	movzbl	%r13b, %r11d
	movq	%r14, %rcx
	imulq	%r9, %r9
	imulq	%r14, %rcx
	movq	%rcx, %rax
	mulq	%rbp
	shrq	$31, %rdx
	movq	%rdx, %rax
	imulq	%rdi, %rax
	subq	%rax, %rcx
	movq	%r9, %rax
	mulq	%rbp
	movq	%rcx, %r10
	shrq	$31, %rdx
	movq	%rdx, %rax
	imulq	%rdi, %rax
	subq	%rax, %r9
	leal	(%r9,%r9), %eax
	leaq	(%r9,%r9), %rdx
	movq	%r9, %r8
	cmpq	%rdx, %rbx
	leal	1119(%rax), %ecx
	cmovnb	%eax, %ecx
	imulq	%r14, %rcx
	movq	%rcx, %rax
	mulq	%rbp
	shrq	$31, %rdx
	movq	%rdx, %rax
	imulq	%rdi, %rax
	subq	%rax, %rcx
	leal	(%rcx,%rcx), %r9d
	leaq	(%rcx,%rcx), %rax
	leaq	(%r10,%r10), %rcx
	cmpq	%rax, %rbx
	leal	1119(%r9), %edx
	cmovb	%edx, %r9d
	leal	(%r10,%r10), %edx
	cmpq	%rcx, %rbx
	leal	1119(%rdx), %eax
	leal	(%r9,%r9), %r12d
	cmovb	%eax, %edx
	movl	%edx, %eax
	leal	(%rdx,%r10), %ecx
	addq	%r10, %rax
	leal	1119(%rdx,%r10), %r10d
	leal	1119(%r12), %edx
	cmpq	%rax, %rbx
	movl	%r9d, %eax
	cmovnb	%ecx, %r10d
	addq	%rax, %rax
	cmpq	%rax, %rbx
	movq	%r10, %rcx
	cmovb	%edx, %r12d
	imulq	%r10, %rcx
	movq	%rcx, %rax
	mulq	%rbp
	shrq	$31, %rdx
	imulq	%rdi, %rdx
	subq	%rdx, %rcx
	leal	-1119(%rcx), %eax
	movl	%ecx, %edx
	subl	%r12d, %edx
	subl	%r12d, %eax
	cmpl	%r12d, %ecx
	cmovnb	%edx, %eax
	imulq	%r8, %r8
	movl	%eax, %ecx
	movl	%ecx, (%rsi,%r11,4)
	movq	%r8, %rax
	mulq	%rbp
	shrq	$31, %rdx
	movq	%rdx, %rax
	movq	%r8, %rdx
	imulq	%rdi, %rax
	subq	%rax, %rdx
	leal	(%rdx,%rdx), %eax
	addq	%rdx, %rdx
	cmpq	%rdx, %rbx
	leal	1119(%rax), %r8d
	cmovb	%r8, %rax
	leal	(%rax,%rax), %edx
	addq	%rax, %rax
	cmpq	%rax, %rbx
	leal	1119(%rdx), %r8d
	cmovb	%r8, %rdx
	leal	(%rdx,%rdx), %r8d
	addq	%rdx, %rdx
	cmpq	%rdx, %rbx
	leal	1119(%r8), %eax
	leal	-1119(%r9), %edx
	cmovb	%eax, %r8d
	movl	%r9d, %eax
	subl	%ecx, %edx
	subl	%ecx, %eax
	cmpl	%ecx, %r9d
	cmovb	%edx, %eax
	imulq	%r10, %rax
	movq	%rax, %r9
	mulq	%rbp
	movq	%r9, %rax
	shrq	$31, %rdx
	imulq	%rdi, %rdx
	subq	%rdx, %rax
	movl	$-1119, %edx
	subl	%r8d, %edx
	movl	%eax, %r9d
	addl	%eax, %edx
	subl	%r8d, %r9d
	cmpl	%r8d, %eax
	cmovb	%edx, %r9d
	incq	%r13
	xorl	%ecx, 100(%rsp)
	cmpq	$3000000, %r13
	jne	.L70
	movl	%ecx, 40(%rsp)
	movl	%r9d, %r12d
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	subq	32(%rsp), %rax
	movl	40(%rsp), %ecx
	js	.L71
	vcvtsi2sdq	%rax, %xmm7, %xmm0
.L72:
	vdivsd	%xmm6, %xmm0, %xmm0
	decl	48(%rsp)
	movl	100(%rsp), %eax
	vminsd	%xmm8, %xmm0, %xmm2
	vmovapd	%xmm2, %xmm8
	jne	.L75
	movq	64(%rsp), %rdx
	leaq	.LC4(%rip), %rcx
	vmovq	%xmm2, %r8
	movl	$1, %r12d
	movl	$1960037684, %r13d
	movabsq	$-9223369633819947615, %rbx
	movl	$560815139, %edi
	xorl	%r15d, %r15d
	call	__mingw_printf
	vmovsd	.LC0(%rip), %xmm8
	movl	$3, 48(%rsp)
	.p2align 4
	.p2align 3
.L111:
	movl	$0, 96(%rsp)
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	xorl	%r14d, %r14d
	movl	$4294966177, %r10d
	movq	%rax, 40(%rsp)
	jmp	.L106
	.p2align 4
	.p2align 3
.L185:
	movl	%r12d, %r11d
	movq	%r11, %r9
	movq	%r11, 32(%rsp)
	imulq	%r11, %r9
	movq	%r9, %rax
	mulq	%rbx
	shrq	$31, %rdx
	movq	%rdx, %rax
	imulq	%r10, %rax
	subq	%rax, %r9
	movq	%r9, %r8
	imulq	$1960037684, %r9, %r9
	imulq	%r11, %r8
	movq	%r9, %rax
	mulq	%rbx
	movq	%r8, %rax
	shrq	$31, %rdx
	imulq	%r10, %rdx
	subq	%rdx, %r9
	mulq	%rbx
	shrq	$31, %rdx
	imulq	%r10, %rdx
	subq	%rdx, %r8
	imulq	$560815139, %r8, %r8
	movq	%r8, %rax
	mulq	%rbx
	shrq	$31, %rdx
	imulq	%r10, %rdx
	subq	%rdx, %r8
	cmpl	%r13d, %r9d
	je	.L183
	movl	$-1119, %r12d
	movl	%r9d, %eax
	movl	%r8d, %edx
	subl	%r13d, %r12d
	subl	%r13d, %eax
	addl	%r9d, %r12d
	cmpl	%r13d, %r9d
	cmovnb	%eax, %r12d
	movl	$-1119, %eax
	subl	%edi, %edx
	subl	%edi, %eax
	movq	%r12, %r11
	movq	%r12, %rbp
	addl	%r8d, %eax
	cmpl	%edi, %r8d
	cmovb	%eax, %edx
	imulq	%r12, %r11
	movl	%edx, %r8d
	movq	%r11, %rax
	mulq	%rbx
	shrq	$31, %rdx
	movq	%rdx, %rax
	imulq	%r10, %rax
	subq	%rax, %r11
	imulq	%r11, %rbp
	movq	%r11, %r9
	imulq	%r9, %r13
	movq	%rbp, %rax
	movq	%rbp, %r11
	mulq	%rbx
	movq	%r13, %r9
	shrq	$31, %rdx
	movq	%rdx, %rax
	imulq	%r10, %rax
	subq	%rax, %r11
	movq	%r13, %rax
	movl	$4294966176, %r13d
	mulq	%rbx
	shrq	$31, %rdx
	movq	%rdx, %rax
	imulq	%r10, %rax
	subq	%rax, %r9
	leal	(%r9,%r9), %ebp
	leaq	(%r9,%r9), %rdx
	cmpq	%rdx, %r13
	leal	1119(%rbp), %eax
	movq	%r8, %r13
	cmovb	%eax, %ebp
	imulq	%r8, %r13
	movq	%r13, %rax
	mulq	%rbx
	movl	$-1119, %eax
	subl	%r11d, %eax
	shrq	$31, %rdx
	imulq	%r10, %rdx
	subq	%rdx, %r13
	movl	%r13d, %edx
	addl	%r13d, %eax
	subl	%r11d, %edx
	cmpl	%r11d, %r13d
	movl	$-1119, %r13d
	cmovnb	%edx, %eax
	subl	%ebp, %r13d
	movl	%eax, %edx
	addl	%eax, %r13d
	subl	%ebp, %edx
	cmpl	%ebp, %eax
	cmovnb	%rdx, %r13
	imulq	%r11, %rdi
	movq	%rdi, %rax
	mulq	%rbx
	leal	-1119(%r9), %eax
	subl	%r13d, %eax
	shrq	$31, %rdx
	imulq	%r10, %rdx
	subq	%rdx, %rdi
	movl	%r9d, %edx
	subl	%r13d, %edx
	cmpl	%r13d, %r9d
	cmovnb	%edx, %eax
	imulq	%rax, %r8
	movq	%r8, %rax
	mulq	%rbx
	movl	$-1119, %eax
	subl	%edi, %eax
	shrq	$31, %rdx
	imulq	%r10, %rdx
	subq	%rdx, %r8
	movl	%r8d, %edx
	addl	%r8d, %eax
	subl	%edi, %edx
	cmpl	%edi, %r8d
	movl	%edx, %edi
	cmovb	%rax, %rdi
	movq	32(%rsp), %rax
	imulq	%r12, %rax
	movq	%rax, %r12
	mulq	%rbx
	shrq	$31, %rdx
	imulq	%r10, %rdx
	subl	%edx, %r12d
.L76:
	incq	%r14
	xorl	%r13d, 96(%rsp)
	movl	%r13d, (%rcx)
	cmpq	$3000000, %r14
	je	.L184
.L106:
	movzbl	%r14b, %eax
	leaq	(%rsi,%rax,4), %rcx
	testb	%r15b, %r15b
	je	.L185
	xorl	%r15d, %r15d
	movl	$1, %r12d
	movl	$560815139, %edi
	movl	$1960037684, %r13d
	jmp	.L76
	.p2align 4
	.p2align 3
.L149:
	xorl	%ebp, %ebp
	movl	$560815139, %edi
	movl	$1960037684, %r15d
	jmp	.L27
	.p2align 4
	.p2align 3
.L13:
	xorl	%r9d, %r9d
	xorl	%edx, %edx
	testl	%r8d, %r8d
	jne	.L10
.L9:
	movl	%r15d, %ecx
	movl	%r8d, %r15d
	subl	%r8d, %ecx
	jmp	.L18
	.p2align 4
	.p2align 3
.L180:
	addq	%r10, %r10
	leal	(%r15,%r15), %r8d
	cmpq	%r10, %rdi
	jnb	.L13
	addl	$1119, %r8d
	xorl	%edx, %edx
	xorl	%r9d, %r9d
.L10:
	subl	$1119, %edx
	subl	%r8d, %edx
	movl	%edx, %r8d
	jmp	.L16
	.p2align 4
	.p2align 3
.L184:
	movq	40(%rsp), %rbp
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	subq	%rbp, %rax
	js	.L107
	vcvtsi2sdq	%rax, %xmm7, %xmm0
.L108:
	vdivsd	%xmm6, %xmm0, %xmm0
	decl	48(%rsp)
	movl	96(%rsp), %eax
	vminsd	%xmm8, %xmm0, %xmm2
	vmovapd	%xmm2, %xmm8
	jne	.L111
	movq	64(%rsp), %rdx
	leaq	.LC5(%rip), %rcx
	vmovq	%xmm2, %r8
	movl	$3, %ebp
	movl	$560815139, %r12d
	movabsq	$-9223369633819947615, %r14
	movl	$1960037684, %r13d
	call	__mingw_printf
	vmovsd	.LC0(%rip), %xmm8
	movl	$1, 40(%rsp)
	movb	$0, 32(%rsp)
	movl	%ebp, 56(%rsp)
	.p2align 4
	.p2align 3
.L145:
	movl	$0, 92(%rsp)
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	movl	$4294966177, %r15d
	xorl	%r10d, %r10d
	movq	%rax, 48(%rsp)
	jmp	.L142
	.p2align 4
	.p2align 3
.L188:
	movl	40(%rsp), %r11d
	imulq	$241954289, %r12, %rbp
	movq	%r11, %r8
	imulq	%r11, %r8
	movq	%r8, %rax
	mulq	%r14
	movq	%rdx, %rcx
	shrq	$31, %rcx
	movq	%rcx, %rax
	movq	%r8, %rcx
	movl	$3296770614, %r8d
	imulq	%r13, %r8
	imulq	%r15, %rax
	movq	%r8, %r9
	subq	%rax, %rcx
	movq	%r8, %rax
	movq	%rbp, %r8
	mulq	%r14
	imulq	$2063954862, %rcx, %rdi
	imulq	%r11, %rcx
	shrq	$31, %rdx
	movq	%rdx, %rax
	imulq	%r15, %rax
	subq	%rax, %r9
	movq	%rdi, %rax
	mulq	%r14
	movq	%rbp, %rax
	shrq	$31, %rdx
	imulq	%r15, %rdx
	subq	%rdx, %rdi
	mulq	%r14
	shrq	$31, %rdx
	movq	%rdx, %rax
	imulq	%r15, %rax
	subq	%rax, %r8
	movq	%rcx, %rax
	mulq	%r14
	movl	$4187585258, %eax
	shrq	$31, %rdx
	imulq	%r15, %rdx
	subq	%rdx, %rcx
	imulq	%rax, %rcx
	movq	%rcx, %rax
	mulq	%r14
	shrq	$31, %rdx
	imulq	%r15, %rdx
	subq	%rdx, %rcx
	cmpl	%edi, %r9d
	je	.L186
	movl	$-1119, %eax
	movl	%edi, %edx
	movl	$-1119, %r13d
	subl	%r9d, %eax
	subl	%r9d, %edx
	addl	%edi, %eax
	cmpl	%r9d, %edi
	cmovnb	%edx, %eax
	subl	%r8d, %r13d
	movl	%ecx, %edx
	subl	%r8d, %edx
	addl	%ecx, %r13d
	cmpl	%r8d, %ecx
	movl	%eax, %ecx
	movq	%rcx, %rbp
	cmovnb	%edx, %r13d
	movq	%rcx, %r12
	imulq	%rcx, %rbp
	movq	%rbp, %rax
	mulq	%r14
	movq	%rdx, %rdi
	shrq	$31, %rdi
	movq	%rdi, %rax
	movq	%rbp, %rdi
	imulq	%r15, %rax
	subq	%rax, %rdi
	imulq	%rdi, %r12
	imulq	%rdi, %r9
	movq	%r12, %rax
	movq	%r12, %rbp
	mulq	%r14
	shrq	$31, %rdx
	movq	%rdx, %rax
	imulq	%r15, %rax
	subq	%rax, %rbp
	movq	%r9, %rax
	mulq	%r14
	movq	%rdx, %rdi
	shrq	$31, %rdi
	movq	%rdi, %rax
	movq	%r9, %rdi
	movl	$4294966176, %r9d
	imulq	%r15, %rax
	subq	%rax, %rdi
	leaq	(%rdi,%rdi), %rdx
	leal	(%rdi,%rdi), %r12d
	cmpq	%rdx, %r9
	movl	%r13d, %r9d
	leal	1119(%r12), %eax
	movq	%r9, %r13
	cmovb	%eax, %r12d
	imulq	%r9, %r13
	movq	%r13, %rax
	mulq	%r14
	movl	$-1119, %eax
	subl	%ebp, %eax
	shrq	$31, %rdx
	imulq	%r15, %rdx
	subq	%rdx, %r13
	movl	%r13d, %edx
	addl	%r13d, %eax
	subl	%ebp, %edx
	cmpl	%ebp, %r13d
	movl	$-1119, %r13d
	cmovnb	%edx, %eax
	subl	%r12d, %r13d
	movl	%eax, %edx
	addl	%eax, %r13d
	subl	%r12d, %edx
	cmpl	%r12d, %eax
	movl	$-1119, %r12d
	cmovnb	%rdx, %r13
	imulq	%rbp, %r8
	movq	%r8, %rax
	mulq	%r14
	leal	-1119(%rdi), %eax
	subl	%r13d, %eax
	shrq	$31, %rdx
	imulq	%r15, %rdx
	subq	%rdx, %r8
	movl	%edi, %edx
	subl	%r13d, %edx
	cmpl	%r13d, %edi
	cmovnb	%edx, %eax
	subl	%r8d, %r12d
	imulq	%rax, %r9
	movq	%r9, %rax
	mulq	%r14
	shrq	$31, %rdx
	imulq	%r15, %rdx
	subq	%rdx, %r9
	movl	%r9d, %eax
	addl	%r9d, %r12d
	subl	%r8d, %eax
	cmpl	%r8d, %r9d
	cmovnb	%rax, %r12
	imulq	$1121630278, %r11, %r11
	movq	%r11, %rax
	mulq	%r14
	shrq	$31, %rdx
	imulq	%r15, %rdx
	subq	%rdx, %r11
	imulq	%rcx, %r11
	movq	%r11, %rax
	mulq	%r14
	movl	%r11d, %eax
	shrq	$31, %rdx
	imulq	%r15, %rdx
	subl	%edx, %eax
	movl	%eax, 40(%rsp)
.L112:
	incq	%r10
	xorl	%r13d, 92(%rsp)
	movl	%r13d, (%rbx)
	cmpq	$3000000, %r10
	je	.L187
.L142:
	cmpb	$0, 32(%rsp)
	movzbl	%r10b, %eax
	leaq	(%rsi,%rax,4), %rbx
	je	.L188
	movb	$0, 32(%rsp)
	movl	$1121630278, 40(%rsp)
	movl	$4187585258, %r12d
	movl	$2063954862, %r13d
	jmp	.L112
	.p2align 4
	.p2align 3
.L187:
	movq	48(%rsp), %rbp
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	subq	%rbp, %rax
	js	.L143
	vcvtsi2sdq	%rax, %xmm7, %xmm0
.L144:
	vdivsd	%xmm6, %xmm0, %xmm0
	decl	56(%rsp)
	movl	92(%rsp), %eax
	vminsd	%xmm8, %xmm0, %xmm8
	jne	.L145
	vmovapd	%xmm8, %xmm2
	vmovq	%xmm8, %r8
	vmovaps	1136(%rsp), %xmm6
	vmovaps	1152(%rsp), %xmm7
	vmovaps	1168(%rsp), %xmm8
	movq	64(%rsp), %rdx
	leaq	.LC6(%rip), %rcx
	addq	$1192, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	jmp	__mingw_printf
	.p2align 4
	.p2align 3
.L183:
	cmpl	%r8d, %edi
	je	.L189
	xorl	%r12d, %r12d
	xorl	%edi, %edi
	xorl	%r13d, %r13d
	movl	$1, %r15d
	jmp	.L76
	.p2align 4
	.p2align 3
.L186:
	cmpl	%ecx, %r8d
	je	.L190
	movl	$0, 40(%rsp)
	xorl	%r12d, %r12d
	xorl	%r13d, %r13d
	movb	$1, 32(%rsp)
	jmp	.L112
	.p2align 4
	.p2align 3
.L181:
	cmpl	$560815139, %edi
	je	.L191
	xorl	%edi, %edi
	xorl	%r15d, %r15d
	movl	$1, %ebp
	jmp	.L27
	.p2align 4
	.p2align 3
.L42:
	subl	%r15d, %eax
	leal	-1119(%rax), %ecx
	jmp	.L44
	.p2align 4
	.p2align 3
.L182:
	xorl	%eax, %eax
	xorl	%r9d, %r9d
	testl	%r15d, %r15d
	jne	.L42
	movl	$-1960038803, %r15d
	jmp	.L41
	.p2align 4
	.p2align 3
.L179:
	addq	%r10, %r10
	leal	(%r15,%r15), %r8d
	cmpq	%r10, %rdi
	jb	.L8
	xorl	%r9d, %r9d
	testl	%r8d, %r8d
	jne	.L10
	movl	%r15d, %ecx
	movl	%r8d, %r15d
	subl	%r8d, %ecx
	jmp	.L18
	.p2align 4
	.p2align 3
.L107:
	movq	%rax, %rdx
	andl	$1, %eax
	shrq	%rdx
	orq	%rax, %rdx
	vcvtsi2sdq	%rdx, %xmm7, %xmm0
	vaddsd	%xmm0, %xmm0, %xmm0
	jmp	.L108
	.p2align 4
	.p2align 3
.L50:
	movq	%rax, %rdx
	andl	$1, %eax
	shrq	%rdx
	orq	%rax, %rdx
	vcvtsi2sdq	%rdx, %xmm7, %xmm0
	vaddsd	%xmm0, %xmm0, %xmm0
	jmp	.L51
	.p2align 4
	.p2align 3
.L71:
	movq	%rax, %rdx
	andl	$1, %eax
	shrq	%rdx
	orq	%rax, %rdx
	vcvtsi2sdq	%rdx, %xmm7, %xmm0
	vaddsd	%xmm0, %xmm0, %xmm0
	jmp	.L72
	.p2align 4
	.p2align 3
.L22:
	movq	%rax, %rdx
	andl	$1, %eax
	shrq	%rdx
	orq	%rax, %rdx
	vcvtsi2sdq	%rdx, %xmm7, %xmm0
	vaddsd	%xmm0, %xmm0, %xmm0
	jmp	.L23
	.p2align 4
	.p2align 3
.L143:
	movq	%rax, %rdx
	andl	$1, %eax
	shrq	%rdx
	orq	%rax, %rdx
	vcvtsi2sdq	%rdx, %xmm7, %xmm0
	vaddsd	%xmm0, %xmm0, %xmm0
	jmp	.L144
.L191:
	xorl	%r9d, %r9d
	movl	$1, %r11d
	movl	$1121630278, %ecx
	movq	%rbx, %rax
	jmp	.L29
	.p2align 5
	.p2align 4
	.p2align 3
.L151:
	movq	%rdi, %r11
.L29:
	cqto
	movq	%r9, %rdi
	movq	%r11, %r9
	idivq	%rcx
	imulq	%r11, %rax
	subq	%rax, %rdi
	movq	%rcx, %rax
	movq	%rdx, %rcx
	testq	%rdx, %rdx
	jne	.L151
	cmpq	$1, %rax
	jg	.L152
	movl	$4294966177, %r9d
	testq	%r11, %r11
	leaq	(%r11,%r9), %rax
	cmovs	%rax, %r11
	movl	%r11d, %ecx
	movabsq	$-9223369633819947615, %r11
	imulq	$989511900, %rcx, %rcx
	movq	%rcx, %rax
	mulq	%r11
	movq	%rdx, %rdi
	shrq	$31, %rdi
	movq	%rdi, %rax
	movq	%rcx, %rdi
	imulq	%r9, %rax
	subq	%rax, %rdi
	movq	%rdi, %rcx
	imulq	%rdi, %rcx
	movq	%rcx, %rax
	mulq	%r11
	movq	%rdx, %r15
	shrq	$31, %r15
	movq	%r15, %rax
	imulq	%r9, %rax
	subq	%rax, %rcx
	movl	$3920075367, %eax
	cmpq	%rcx, %rax
	jb	.L192
	leal	374890809(%rcx), %r15d
	cmpl	$1960037684, %r15d
	jbe	.L193
	movl	$1960036565, %ecx
.L175:
	subl	%r15d, %ecx
	imulq	%rdi, %rcx
	movq	%rcx, %rax
	mulq	%r11
	shrq	$31, %rdx
	imulq	%rdx, %r9
	subq	%r9, %rcx
	movq	%rcx, %rdx
	movl	%ecx, %edi
.L33:
	cmpq	$560815138, %rdx
	jbe	.L30
	subl	$560815139, %edi
	jmp	.L27
.L8:
	addl	$1119, %r8d
	subl	$1119, %edx
	xorl	%r9d, %r9d
	subl	%r8d, %edx
	movl	%edx, %r8d
	jmp	.L16
.L189:
	movq	%r13, %r8
	imulq	%r13, %r8
	movq	%r8, %rax
	movq	%r8, %r9
	movl	%edi, %r8d
	movl	$4294966177, %edi
	mulq	%rbx
	movq	%r8, 56(%rsp)
	imulq	%r8, %r8
	shrq	$31, %rdx
	movq	%rdx, %rax
	imulq	%r10, %rax
	subq	%rax, %r9
	movq	%r8, %rax
	mulq	%rbx
	shrq	$31, %rdx
	movq	%rdx, %rbp
	imulq	%r10, %rbp
	movq	%rbp, %rax
	movq	%r8, %rbp
	movl	$4294966176, %r8d
	subq	%rax, %rbp
	leaq	(%rbp,%rbp), %r11
	leal	1119(%rbp,%rbp), %eax
	cmpq	%r11, %r8
	leal	(%rbp,%rbp), %r11d
	cmovb	%eax, %r11d
	movabsq	$-9223369633819947615, %rax
	imulq	%r13, %r11
	mulq	%r11
	shrq	$31, %rdx
	imulq	%rdx, %rdi
	movq	%r11, %rdx
	subq	%rdi, %rdx
	leaq	(%r9,%r9), %rdi
	leal	(%rdx,%rdx), %r11d
	addq	%rdx, %rdx
	cmpq	%rdx, %r8
	leal	1119(%r11), %eax
	cmovb	%eax, %r11d
	leal	(%r9,%r9), %eax
	cmpq	%rdi, %r8
	leal	1119(%rax), %edx
	cmovb	%edx, %eax
	movl	%eax, %edx
	leal	1119(%rax,%r9), %edi
	addl	%r9d, %eax
	addq	%r9, %rdx
	leal	(%r11,%r11), %r9d
	cmpq	%rdx, %r8
	movl	%r11d, %edx
	cmovb	%edi, %eax
	addq	%rdx, %rdx
	leal	1119(%r9), %edi
	cmpq	%rdx, %r8
	cmovb	%edi, %r9d
	movl	%eax, %edi
	movabsq	$-9223369633819947615, %rax
	movq	%rdi, %r13
	imulq	%rdi, %r13
	mulq	%r13
	movl	$4294966177, %eax
	shrq	$31, %rdx
	imulq	%rax, %rdx
	subq	%rdx, %r13
	movq	%r13, %rax
	movl	%r13d, %edx
	leal	-1119(%r13), %r13d
	subl	%r9d, %edx
	subl	%r9d, %r13d
	cmpl	%r9d, %eax
	movq	32(%rsp), %r9
	cmovnb	%rdx, %r13
	leal	1119(%r12,%r12), %eax
	leal	(%r12,%r12), %r12d
	addq	%r9, %r9
	cmpq	%r9, %r8
	cmovb	%eax, %r12d
	imulq	56(%rsp), %r12
	imulq	%rbp, %rbp
	movabsq	$-9223369633819947615, %rax
	mulq	%r12
	movq	%rdx, %rax
	movl	$4294966177, %edx
	shrq	$31, %rax
	imulq	%rdx, %rax
	subl	%eax, %r12d
	movabsq	$-9223369633819947615, %rax
	mulq	%rbp
	shrq	$31, %rdx
	movq	%rdx, %rax
	movl	$4294966177, %edx
	imulq	%rax, %rdx
	subq	%rdx, %rbp
	leal	(%rbp,%rbp), %r9d
	leaq	(%rbp,%rbp), %rax
	cmpq	%rax, %r8
	leal	1119(%r9), %edx
	cmovb	%edx, %r9d
	movl	%r9d, %edx
	leal	(%r9,%r9), %eax
	addq	%rdx, %rdx
	leal	1119(%rax), %r9d
	cmpq	%rdx, %r8
	cmovb	%r9, %rax
	leal	(%rax,%rax), %r9d
	addq	%rax, %rax
	cmpq	%rax, %r8
	leal	1119(%r9), %edx
	movl	%r11d, %r8d
	cmovb	%edx, %r9d
	subl	%r13d, %r8d
	movl	%r8d, %eax
	leal	-1119(%r11), %r8d
	subl	%r13d, %r8d
	cmpl	%r13d, %r11d
	cmovnb	%eax, %r8d
	movabsq	$-9223369633819947615, %rax
	imulq	%rdi, %r8
	mulq	%r8
	movl	$4294966177, %eax
	shrq	$31, %rdx
	imulq	%rax, %rdx
	subq	%rdx, %r8
	movl	%r8d, %eax
	subl	%r9d, %eax
	cmpl	%r9d, %r8d
	leal	-1119(%rax), %edi
	cmovnb	%rax, %rdi
	jmp	.L76
.L190:
	movq	%r13, %rcx
	movl	$4294966176, %r8d
	imulq	%r13, %rcx
	movq	%rcx, %rax
	mulq	%r14
	shrq	$31, %rdx
	movq	%rdx, %rax
	imulq	%r15, %rax
	subq	%rax, %rcx
	movq	%rcx, %r9
	movq	%r12, %rcx
	imulq	%r12, %rcx
	movq	%rcx, %rax
	mulq	%r14
	shrq	$31, %rdx
	movq	%rdx, %rax
	imulq	%r15, %rax
	subq	%rax, %rcx
	movq	%rcx, %rbp
	leaq	(%rcx,%rcx), %rcx
	cmpq	%rcx, %r8
	leal	1119(%rbp,%rbp), %eax
	leal	(%rbp,%rbp), %ecx
	cmovb	%eax, %ecx
	movabsq	$-9223369633819947615, %rax
	imulq	%r13, %rcx
	mulq	%rcx
	movl	$4294966177, %eax
	shrq	$31, %rdx
	imulq	%rdx, %rax
	subq	%rax, %rcx
	leal	(%rcx,%rcx), %edi
	leaq	(%rcx,%rcx), %rdx
	leaq	(%r9,%r9), %rcx
	cmpq	%rdx, %r8
	leal	1119(%rdi), %eax
	cmovb	%eax, %edi
	leal	(%r9,%r9), %eax
	cmpq	%rcx, %r8
	leal	1119(%rax), %edx
	cmovb	%edx, %eax
	movl	%eax, %edx
	leal	1119(%rax,%r9), %ecx
	addl	%r9d, %eax
	addq	%r9, %rdx
	leal	(%rdi,%rdi), %r9d
	cmpq	%rdx, %r8
	movl	%edi, %edx
	cmovb	%ecx, %eax
	addq	%rdx, %rdx
	leal	1119(%r9), %ecx
	cmpq	%rdx, %r8
	cmovb	%ecx, %r9d
	movl	%eax, %ecx
	movabsq	$-9223369633819947615, %rax
	movq	%rcx, 72(%rsp)
	imulq	%rcx, %rcx
	mulq	%rcx
	shrq	$31, %rdx
	movq	%rdx, %rax
	movl	$4294966177, %edx
	imulq	%rdx, %rax
	movl	40(%rsp), %edx
	subq	%rax, %rcx
	movl	%ecx, %r13d
	subl	%r9d, %r13d
	movl	%r13d, %eax
	leal	-1119(%rcx), %r13d
	subl	%r9d, %r13d
	cmpl	%r9d, %ecx
	leal	(%rdx,%rdx), %ecx
	cmovnb	%rax, %r13
	addq	%r11, %r11
	leal	1119(%rdx,%rdx), %eax
	cmpq	%r11, %r8
	movl	$4294966177, %r11d
	cmovb	%eax, %ecx
	imulq	%rbp, %rbp
	movabsq	$-9223369633819947615, %rax
	imulq	%r12, %rcx
	mulq	%rcx
	shrq	$31, %rdx
	movq	%rdx, %rax
	movl	%ecx, %edx
	imulq	%r11, %rax
	subl	%eax, %edx
	movabsq	$-9223369633819947615, %rax
	movl	%edx, 40(%rsp)
	mulq	%rbp
	shrq	$31, %rdx
	movq	%rdx, %rax
	movq	%r11, %rdx
	imulq	%rax, %rdx
	subq	%rdx, %rbp
	leal	(%rbp,%rbp), %ecx
	leaq	(%rbp,%rbp), %rax
	cmpq	%rax, %r8
	leal	1119(%rcx), %edx
	cmovb	%edx, %ecx
	movl	%ecx, %edx
	leal	(%rcx,%rcx), %eax
	addq	%rdx, %rdx
	leal	1119(%rax), %ecx
	cmpq	%rdx, %r8
	cmovb	%rcx, %rax
	leal	(%rax,%rax), %ecx
	addq	%rax, %rax
	cmpq	%rax, %r8
	leal	1119(%rcx), %edx
	leal	-1119(%rdi), %r8d
	movabsq	$-9223369633819947615, %rax
	cmovb	%edx, %ecx
	movl	%edi, %edx
	subl	%r13d, %r8d
	subl	%r13d, %edx
	cmpl	%r13d, %edi
	cmovnb	%edx, %r8d
	imulq	72(%rsp), %r8
	mulq	%r8
	movq	%rdx, %rax
	shrq	$31, %rax
	imulq	%r11, %rax
	subq	%rax, %r8
	movl	%r8d, %eax
	subl	%ecx, %eax
	cmpl	%ecx, %r8d
	leal	-1119(%rax), %r12d
	cmovnb	%rax, %r12
	jmp	.L112
.L192:
	leal	374891928(%rcx), %r15d
	movl	$1960037684, %ecx
	jmp	.L175
.L152:
	xorl	%edi, %edi
	movl	$374890809, %r15d
.L30:
	subl	$560816258, %edi
	jmp	.L27
.L193:
	movl	$1960037684, %eax
	xorl	%edx, %edx
	subl	%r15d, %eax
	imulq	%rdi, %rax
	divq	%r9
	movl	%edx, %edi
	jmp	.L33
	.seh_endproc
	.section	.text$_Z8bench_ecIN2fp6FpMontILj4294966177EEEEvPKc,"x"
	.linkonce discard
	.p2align 4
	.globl	_Z8bench_ecIN2fp6FpMontILj4294966177EEEEvPKc
	.def	_Z8bench_ecIN2fp6FpMontILj4294966177EEEEvPKc;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8bench_ecIN2fp6FpMontILj4294966177EEEEvPKc
_Z8bench_ecIN2fp6FpMontILj4294966177EEEEvPKc:
.LFB4630:
	pushq	%r15
	.seh_pushreg	%r15
	pushq	%r14
	.seh_pushreg	%r14
	pushq	%r13
	.seh_pushreg	%r13
	pushq	%r12
	.seh_pushreg	%r12
	pushq	%rbp
	.seh_pushreg	%rbp
	pushq	%rdi
	.seh_pushreg	%rdi
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$1192, %rsp
	.seh_stackalloc	1192
	vmovaps	%xmm6, 1136(%rsp)
	.seh_savexmm	%xmm6, 1136
	vmovaps	%xmm7, 1152(%rsp)
	.seh_savexmm	%xmm7, 1152
	vmovaps	%xmm8, 1168(%rsp)
	.seh_savexmm	%xmm8, 1168
	.seh_endprologue
	vmovsd	.LC0(%rip), %xmm8
	vmovsd	.LC1(%rip), %xmm6
	vxorps	%xmm7, %xmm7, %xmm7
	movl	$487078699, %esi
	movl	$-1445549170, %r15d
	movl	$4294966177, %edi
	movl	$4294966176, %r12d
	movq	%rcx, 72(%rsp)
	movl	$3, 48(%rsp)
	.p2align 4
	.p2align 3
.L225:
	movl	$0, 108(%rsp)
	movl	$-1119, %ebp
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	xorl	%r9d, %r9d
	movq	%rax, 32(%rsp)
	.p2align 4
	.p2align 3
.L220:
	movzbl	%r9b, %eax
	movl	%r15d, %ecx
	xorl	%edx, %edx
	leaq	112(%rsp,%rax,4), %r8
	movq	%rcx, %rax
	imulq	%rcx, %rax
	imull	$-383821921, %eax, %r10d
	imulq	%rdi, %r10
	addq	%r10, %rax
	adcq	$0, %rdx
	shrdq	$32, %rdx, %rax
	movl	%eax, %r14d
	cmpq	%rax, %r12
	jnb	.L195
	addl	$1119, %r14d
.L195:
	movl	%r14d, %r11d
	leal	(%r14,%r14), %eax
	leaq	(%r11,%r11), %rbx
	leal	1119(%rax), %r10d
	cmpq	%rbx, %r12
	cmovb	%r10d, %eax
	movl	%eax, %r10d
	leal	(%r14,%rax), %edx
	addq	%r11, %r10
	cmpq	%r10, %r12
	leal	1119(%r14,%rax), %r10d
	movl	%esi, %eax
	cmovnb	%edx, %r10d
	addq	%rax, %rax
	cmpq	%rax, %r12
	jnb	.L199
	leal	1119(%rsi,%rsi), %eax
	xorl	%edx, %edx
	imull	$-383821921, %eax, %r11d
	imulq	%rdi, %r11
	addq	%r11, %rax
	adcq	$0, %rdx
	shrdq	$32, %rdx, %rax
	cmpq	%rdi, %rax
	jne	.L200
	addq	%rcx, %rcx
	leal	(%r15,%r15), %r11d
	cmpq	%rcx, %r12
	jnb	.L445
.L207:
	addl	$1119, %r11d
	xorl	%eax, %eax
.L444:
	xorl	%edx, %edx
.L203:
	movl	%ebp, %ecx
	subl	%r11d, %ecx
	leal	(%rcx,%rdx), %r11d
.L214:
	cmpl	%r11d, %r15d
	jnb	.L202
	leal	-1119(%r15), %edx
	movl	%r11d, %r15d
	subl	%r11d, %edx
.L216:
	imulq	%rdx, %rax
	xorl	%edx, %edx
	imull	$-383821921, %eax, %ecx
	imulq	%rdi, %rcx
	addq	%rcx, %rax
	adcq	$0, %rdx
	shrdq	$32, %rdx, %rax
	movl	%eax, %ebx
	cmpq	%rax, %r12
	jnb	.L217
	addl	$1119, %ebx
.L217:
	movl	%ebx, %ecx
	movl	%ebp, %eax
	movl	%r11d, (%r8)
	subl	%esi, %eax
	subl	%esi, %ecx
	addl	%ebx, %eax
	cmpl	%esi, %ebx
	movl	%ecx, %esi
	cmovb	%eax, %esi
	incq	%r9
	xorl	%r11d, 108(%rsp)
	cmpq	$3000000, %r9
	jne	.L220
	movq	32(%rsp), %r14
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	subq	%r14, %rax
	js	.L221
	vcvtsi2sdq	%rax, %xmm7, %xmm0
.L222:
	vdivsd	%xmm6, %xmm0, %xmm0
	decl	48(%rsp)
	movl	108(%rsp), %eax
	vminsd	%xmm8, %xmm0, %xmm2
	vmovapd	%xmm2, %xmm8
	jne	.L225
	movq	72(%rsp), %rdx
	leaq	.LC2(%rip), %rcx
	vmovq	%xmm2, %r8
	xorl	%ebp, %ebp
	movl	$487078699, %edi
	movl	$-1445549170, %r15d
	movl	$4294966177, %ebx
	movl	$3, %r14d
	call	__mingw_printf
	vmovsd	.LC0(%rip), %xmm8
	.p2align 4
	.p2align 3
.L266:
	movl	$0, 104(%rsp)
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	movl	$4294966176, %esi
	xorl	%ecx, %ecx
	movq	%rax, 48(%rsp)
	.p2align 4
	.p2align 3
.L261:
	movzbl	%cl, %eax
	leaq	112(%rsp,%rax,4), %r8
	testb	%bpl, %bpl
	jne	.L406
	cmpl	$-1445549170, %r15d
	je	.L452
	movl	$-1445549170, %edx
	movl	$-1445550289, %eax
	movl	$487077580, %r10d
	movl	$1, %r13d
	subl	%r15d, %edx
	subl	%r15d, %eax
	cmpl	$-1445549170, %r15d
	cmovbe	%rdx, %rax
	xorl	%edx, %edx
	imull	$-383821921, %eax, %r9d
	imulq	%rbx, %r9
	addq	%r9, %rax
	movl	$487078699, %r9d
	adcq	$0, %rdx
	subl	%edi, %r10d
	subl	%edi, %r9d
	cmpl	$487078699, %edi
	cmova	%r10d, %r9d
	movq	%rax, %r10
	xorl	%r11d, %r11d
	movq	%rbx, %rax
	shrdq	$32, %rdx, %r10
	testq	%r10, %r10
	je	.L449
	movb	%bpl, 32(%rsp)
	jmp	.L244
	.p2align 5
	.p2align 4
	.p2align 3
.L411:
	movq	%rbp, %r13
.L244:
	cqto
	idivq	%r10
	imulq	%r13, %rax
	subq	%rax, %r11
	movq	%r10, %rax
	movq	%rdx, %r10
	movq	%r11, %rbp
	movq	%r13, %r11
	testq	%rdx, %rdx
	jne	.L411
	movzbl	32(%rsp), %ebp
	cmpq	$1, %rax
	jg	.L449
	testq	%r13, %r13
	leaq	0(%r13,%rbx), %rax
	cmovs	%rax, %r13
	xorl	%edx, %edx
	movl	%r13d, %eax
	imulq	$1252161, %rax, %rax
	imull	$-383821921, %eax, %r10d
	imulq	%rbx, %r10
	addq	%r10, %rax
	movl	$4294966176, %r10d
	adcq	$0, %rdx
	shrdq	$32, %rdx, %rax
	shrq	$32, %rdx
	movq	%rax, 32(%rsp)
	cmpq	32(%rsp), %r10
	movq	%rdx, 40(%rsp)
	movl	32(%rsp), %edx
	jnb	.L249
	addl	$1119, %edx
.L249:
	movl	%r9d, %eax
	movl	$4294966176, %r9d
	imulq	%rdx, %rax
	xorl	%edx, %edx
	imull	$-383821921, %eax, %r10d
	imulq	%rbx, %r10
	addq	%r10, %rax
	adcq	$0, %rdx
	shrdq	$32, %rdx, %rax
	cmpq	%rax, %r9
	jnb	.L453
	addl	$1119, %eax
	movq	%rax, %r10
	imulq	%rax, %r10
	imull	$-383821921, %r10d, %edx
	imulq	%rbx, %rdx
.L447:
	xorl	%r11d, %r11d
	addq	%rdx, %r10
	adcq	$0, %r11
	shrdq	$32, %r11, %r10
	shrq	$32, %r11
	movq	%r10, 32(%rsp)
	movq	%r11, 40(%rsp)
	movl	$4294966176, %r11d
	cmpq	32(%rsp), %r11
	movq	%r10, %r9
	movl	%r10d, %edx
	jnb	.L252
	leal	1119(%r9), %edx
.L252:
	cmpl	%r15d, %edx
	jb	.L253
	subl	%r15d, %edx
.L254:
	leal	1445549170(%rdx), %r10d
	leal	1445548051(%rdx), %r9d
	cmpl	$-1445549171, %edx
	cmova	%r10d, %r9d
	cmpl	%r9d, %r15d
	jb	.L257
	movl	%r15d, %edx
	movl	%r9d, %r15d
	subl	%r9d, %edx
.L258:
	imulq	%rdx, %rax
	xorl	%edx, %edx
	imull	$-383821921, %eax, %r9d
	imulq	%rbx, %r9
	addq	%r9, %rax
	adcq	$0, %rdx
	shrdq	$32, %rdx, %rax
	movl	%eax, %r10d
	cmpq	%rax, %rsi
	jnb	.L259
	addl	$1119, %r10d
.L259:
	movl	%r10d, %edx
	movl	$-1119, %eax
	subl	%edi, %eax
	subl	%edi, %edx
	addl	%r10d, %eax
	cmpl	%edi, %r10d
	movl	%edx, %edi
	cmovb	%eax, %edi
.L226:
	incq	%rcx
	xorl	%r15d, 104(%rsp)
	movl	%r15d, (%r8)
	cmpq	$3000000, %rcx
	jne	.L261
	movq	48(%rsp), %r13
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	subq	%r13, %rax
	js	.L262
	vcvtsi2sdq	%rax, %xmm7, %xmm0
.L263:
	vdivsd	%xmm6, %xmm0, %xmm0
	decl	%r14d
	movl	104(%rsp), %eax
	vminsd	%xmm8, %xmm0, %xmm2
	vmovapd	%xmm2, %xmm8
	jne	.L266
	movq	72(%rsp), %rdx
	leaq	.LC3(%rip), %rcx
	vmovq	%xmm2, %r8
	movl	$3, %r15d
	movl	$487078699, %ebx
	movl	$2849418126, %esi
	movl	$4294966177, %ebp
	movl	$4294966176, %edi
	movl	$-1119, %r14d
	call	__mingw_printf
	vmovsd	.LC0(%rip), %xmm8
	.p2align 4
	.p2align 3
.L293:
	movl	$0, 100(%rsp)
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	xorl	%r8d, %r8d
	movq	%rax, %r11
	.p2align 4
	.p2align 3
.L288:
	movzbl	%r8b, %eax
	xorl	%edx, %edx
	leaq	112(%rsp,%rax,4), %r10
	movq	%rsi, %rax
	imulq	%rsi, %rax
	imull	$-383821921, %eax, %ecx
	imulq	%rbp, %rcx
	addq	%rcx, %rax
	adcq	$0, %rdx
	shrdq	$32, %rdx, %rax
	movl	%eax, %r13d
	cmpq	%rax, %rdi
	jnb	.L267
	addl	$1119, %r13d
.L267:
	movl	%ebx, %ecx
	xorl	%ebx, %ebx
	imulq	%rcx, %rcx
	imull	$-383821921, %ecx, %eax
	imulq	%rbp, %rax
	addq	%rax, %rcx
	adcq	$0, %rbx
	shrdq	$32, %rbx, %rcx
	movl	%ecx, %r9d
	cmpq	%rcx, %rdi
	jnb	.L268
	addl	$1119, %r9d
.L268:
	movl	%r9d, %eax
	addl	%r9d, %r9d
	leaq	(%rax,%rax), %rbx
	leal	1119(%r9), %ecx
	cmpq	%rbx, %rdi
	cmovnb	%r9d, %ecx
	xorl	%ebx, %ebx
	imulq	%rsi, %rcx
	imull	$-383821921, %ecx, %r9d
	imulq	%rbp, %r9
	addq	%r9, %rcx
	adcq	$0, %rbx
	shrdq	$32, %rbx, %rcx
	movl	%ecx, %r9d
	cmpq	%rcx, %rdi
	jnb	.L270
	addl	$1119, %r9d
.L270:
	movl	%r13d, %esi
	leal	(%r9,%r9), %ecx
	addq	%r9, %r9
	cmpq	%r9, %rdi
	leaq	(%rsi,%rsi), %r12
	leal	(%r13,%r13), %r9d
	leal	1119(%rcx), %ebx
	cmovb	%ebx, %ecx
	cmpq	%r12, %rdi
	leal	1119(%r9), %ebx
	cmovb	%ebx, %r9d
	leal	(%rcx,%rcx), %edx
	movl	%r9d, %ebx
	addq	%rsi, %rbx
	leal	(%r9,%r13), %esi
	leal	1119(%r9,%r13), %r9d
	cmpq	%rbx, %rdi
	movl	%ecx, %ebx
	cmovnb	%esi, %r9d
	addq	%rbx, %rbx
	leal	1119(%rdx), %esi
	cmpq	%rbx, %rdi
	movq	%r9, %r12
	cmovb	%esi, %edx
	imulq	%r9, %r12
	xorl	%r13d, %r13d
	imull	$-383821921, %r12d, %ebx
	imulq	%rbp, %rbx
	addq	%rbx, %r12
	adcq	$0, %r13
	shrdq	$32, %r13, %r12
	movl	%r12d, %esi
	cmpq	%r12, %rdi
	jnb	.L276
	addl	$1119, %esi
.L276:
	movl	%r14d, %ebx
	movl	%esi, %r12d
	subl	%edx, %ebx
	addl	%esi, %ebx
	subl	%edx, %esi
	cmpl	%edx, %r12d
	cmovb	%rbx, %rsi
	imulq	%rax, %rax
	xorl	%edx, %edx
	imull	$-383821921, %eax, %ebx
	imulq	%rbp, %rbx
	addq	%rbx, %rax
	adcq	$0, %rdx
	shrdq	$32, %rdx, %rax
	movl	%eax, %ebx
	cmpq	%rax, %rdi
	jnb	.L279
	addl	$1119, %ebx
.L279:
	leal	(%rbx,%rbx), %edx
	addq	%rbx, %rbx
	cmpq	%rbx, %rdi
	leal	1119(%rdx), %eax
	cmovb	%rax, %rdx
	leal	(%rdx,%rdx), %eax
	addq	%rdx, %rdx
	cmpq	%rdx, %rdi
	leal	1119(%rax), %ebx
	cmovb	%rbx, %rax
	leal	(%rax,%rax), %r12d
	addq	%rax, %rax
	cmpq	%rax, %rdi
	leal	1119(%r12), %edx
	movl	%ecx, %eax
	cmovb	%edx, %r12d
	leal	-1119(%rcx), %edx
	subl	%esi, %eax
	subl	%esi, %edx
	cmpl	%esi, %ecx
	cmovb	%edx, %eax
	xorl	%edx, %edx
	imulq	%r9, %rax
	imull	$-383821921, %eax, %ecx
	imulq	%rbp, %rcx
	addq	%rcx, %rax
	adcq	$0, %rdx
	shrdq	$32, %rdx, %rax
	movl	%eax, %ecx
	cmpq	%rax, %rdi
	jnb	.L285
	addl	$1119, %ecx
.L285:
	movl	%r14d, %eax
	movl	%ecx, %ebx
	movl	%esi, (%r10)
	subl	%r12d, %eax
	subl	%r12d, %ebx
	addl	%ecx, %eax
	cmpl	%r12d, %ecx
	cmovb	%eax, %ebx
	incq	%r8
	xorl	%esi, 100(%rsp)
	cmpq	$3000000, %r8
	jne	.L288
	movq	%r11, %r13
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	subq	%r13, %rax
	js	.L289
	vcvtsi2sdq	%rax, %xmm7, %xmm0
.L290:
	vdivsd	%xmm6, %xmm0, %xmm0
	decl	%r15d
	movl	100(%rsp), %eax
	vminsd	%xmm8, %xmm0, %xmm2
	vmovapd	%xmm2, %xmm8
	jne	.L293
	movq	72(%rsp), %rdx
	leaq	.LC4(%rip), %rcx
	vmovq	%xmm2, %r8
	movl	$-1445549170, %r15d
	movl	$4294966177, %r14d
	xorl	%esi, %esi
	movl	$1119, %r12d
	movl	$487078699, %edi
	call	__mingw_printf
	vmovsd	.LC0(%rip), %xmm8
	movl	$3, 56(%rsp)
	.p2align 4
	.p2align 3
.L344:
	movl	$0, 96(%rsp)
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	xorl	%ebp, %ebp
	movl	$4294966176, %r13d
	movq	%rax, 48(%rsp)
	jmp	.L341
	.p2align 4
	.p2align 3
.L456:
	movl	%r12d, %eax
	xorl	%edx, %edx
	movq	%rax, 32(%rsp)
	imulq	%rax, %rax
	imull	$-383821921, %eax, %ecx
	imulq	%r14, %rcx
	addq	%rcx, %rax
	adcq	$0, %rdx
	shrdq	$32, %rdx, %rax
	movl	%eax, %edx
	cmpq	%rax, %r13
	jnb	.L295
	addl	$1119, %edx
.L295:
	movl	%edx, %eax
	movl	$2849418126, %r8d
	xorl	%r9d, %r9d
	imulq	%rax, %r8
	imull	$-383821921, %r8d, %edx
	imulq	%r14, %rdx
	addq	%rdx, %r8
	adcq	$0, %r9
	shrdq	$32, %r9, %r8
	movl	%r8d, %ecx
	cmpq	%r8, %r13
	jnb	.L296
	addl	$1119, %ecx
.L296:
	imulq	32(%rsp), %rax
	xorl	%edx, %edx
	imull	$-383821921, %eax, %r8d
	imulq	%r14, %r8
	addq	%r8, %rax
	adcq	$0, %rdx
	shrdq	$32, %rdx, %rax
	movl	%eax, %edx
	cmpq	%rax, %r13
	jnb	.L297
	addl	$1119, %edx
.L297:
	movl	%edx, %eax
	xorl	%edx, %edx
	imulq	$487078699, %rax, %rax
	imull	$-383821921, %eax, %r8d
	imulq	%r14, %r8
	addq	%r8, %rax
	adcq	$0, %rdx
	shrdq	$32, %rdx, %rax
	movl	%eax, %r9d
	cmpq	%rax, %r13
	jnb	.L298
	addl	$1119, %r9d
.L298:
	cmpl	%r15d, %ecx
	je	.L454
	movl	%ecx, %r8d
	movl	$-1119, %eax
	subl	%r15d, %r8d
	subl	%r15d, %eax
	addl	%ecx, %eax
	cmpl	%r15d, %ecx
	movl	%r8d, %ecx
	movl	$-1119, %r8d
	cmovb	%eax, %ecx
	movl	%r9d, %eax
	subl	%edi, %r8d
	subl	%edi, %eax
	addl	%r9d, %r8d
	cmpl	%edi, %r9d
	cmovnb	%rax, %r8
	movq	%rcx, %rax
	xorl	%edx, %edx
	imulq	%rcx, %rax
	imull	$-383821921, %eax, %r9d
	imulq	%r14, %r9
	addq	%r9, %rax
	adcq	$0, %rdx
	shrdq	$32, %rdx, %rax
	movl	%eax, %r9d
	cmpq	%rax, %r13
	jnb	.L326
	addl	$1119, %r9d
.L326:
	movq	%rcx, %rax
	xorl	%edx, %edx
	imulq	%r9, %rax
	imull	$-383821921, %eax, %r10d
	imulq	%r14, %r10
	addq	%r10, %rax
	adcq	$0, %rdx
	shrdq	$32, %rdx, %rax
	movl	%eax, %r10d
	cmpq	%rax, %r13
	jnb	.L327
	addl	$1119, %r10d
.L327:
	movl	%r15d, %eax
	xorl	%edx, %edx
	imulq	%r9, %rax
	imull	$-383821921, %eax, %r9d
	imulq	%r14, %r9
	addq	%r9, %rax
	adcq	$0, %rdx
	shrdq	$32, %rdx, %rax
	movl	%eax, %r9d
	cmpq	%rax, %r13
	jnb	.L328
	addl	$1119, %r9d
.L328:
	movl	%r9d, %eax
	leal	(%r9,%r9), %r11d
	addq	%rax, %rax
	leal	1119(%r11), %edx
	cmpq	%rax, %r13
	movq	%r8, %rax
	cmovb	%edx, %r11d
	imulq	%r8, %rax
	imull	$-383821921, %eax, %edx
	imulq	%r14, %rdx
	movq	%rdx, %r12
	xorl	%edx, %edx
	addq	%r12, %rax
	adcq	$0, %rdx
	shrdq	$32, %rdx, %rax
	movl	%eax, %r15d
	cmpq	%rax, %r13
	jnb	.L330
	addl	$1119, %r15d
.L330:
	movl	$-1119, %eax
	movl	%r15d, %edx
	subl	%r10d, %eax
	subl	%r10d, %edx
	addl	%r15d, %eax
	cmpl	%r10d, %r15d
	movl	$-1119, %r15d
	cmovnb	%edx, %eax
	subl	%r11d, %r15d
	movl	%eax, %edx
	addl	%eax, %r15d
	subl	%r11d, %edx
	cmpl	%r11d, %eax
	movl	%r10d, %eax
	cmovnb	%edx, %r15d
	imulq	%rdi, %rax
	xorl	%edx, %edx
	imull	$-383821921, %eax, %r11d
	imulq	%r14, %r11
	addq	%r11, %rax
	adcq	$0, %rdx
	shrdq	$32, %rdx, %rax
	movl	%eax, %r10d
	cmpq	%rax, %r13
	jnb	.L335
	addl	$1119, %r10d
.L335:
	movl	%r9d, %edx
	leal	-1119(%r9), %eax
	subl	%r15d, %edx
	subl	%r15d, %eax
	cmpl	%r15d, %r9d
	cmovnb	%edx, %eax
	xorl	%edx, %edx
	imulq	%r8, %rax
	imull	$-383821921, %eax, %r8d
	imulq	%r14, %r8
	addq	%r8, %rax
	adcq	$0, %rdx
	shrdq	$32, %rdx, %rax
	movl	%eax, %r8d
	cmpq	%rax, %r13
	jnb	.L338
	addl	$1119, %r8d
.L338:
	movl	$-1119, %edi
	movl	%r8d, %eax
	subl	%r10d, %edi
	subl	%r10d, %eax
	addl	%r8d, %edi
	cmpl	%r10d, %r8d
	cmovnb	%rax, %rdi
	movq	32(%rsp), %rax
	xorl	%edx, %edx
	imulq	%rcx, %rax
	imull	$-383821921, %eax, %ecx
	imulq	%r14, %rcx
	addq	%rcx, %rax
	adcq	$0, %rdx
	shrdq	$32, %rdx, %rax
	movl	%eax, %r12d
	cmpq	%rax, %r13
	jnb	.L294
	addl	$1119, %r12d
	.p2align 4
	.p2align 3
.L294:
	incq	%rbp
	xorl	%r15d, 96(%rsp)
	movl	%r15d, (%rbx)
	cmpq	$3000000, %rbp
	je	.L455
.L341:
	movzbl	%bpl, %eax
	leaq	112(%rsp,%rax,4), %rbx
	testb	%sil, %sil
	je	.L456
	xorl	%esi, %esi
	movl	$1119, %r12d
	movl	$3875325879, %edi
	movl	$1633979660, %r15d
	jmp	.L294
	.p2align 4
	.p2align 3
.L406:
	xorl	%ebp, %ebp
	movl	$487078699, %edi
	movl	$-1445549170, %r15d
	jmp	.L226
.L451:
	leal	(%r15,%r15), %r11d
	cmpq	$2147483088, %rcx
	ja	.L207
	.p2align 4
	.p2align 3
.L445:
	xorl	%eax, %eax
	testl	%r11d, %r11d
	jne	.L444
.L202:
	movl	%r15d, %edx
	movl	%r11d, %r15d
	subl	%r11d, %edx
	jmp	.L216
	.p2align 4
	.p2align 3
.L199:
	imull	$-767643842, %esi, %r11d
	leal	(%rsi,%rsi), %eax
	xorl	%edx, %edx
	imulq	%rdi, %r11
	addq	%r11, %rax
	adcq	$0, %rdx
	shrdq	$32, %rdx, %rax
.L200:
	movq	%rax, %r11
	xorl	%ebx, %ebx
	movl	$1, %r13d
	movq	%rdi, %rax
	testq	%r11, %r11
	jne	.L204
	jmp	.L451
	.p2align 5
	.p2align 4
	.p2align 3
.L404:
	movq	%r14, %r13
.L204:
	cqto
	idivq	%r11
	imulq	%r13, %rax
	subq	%rax, %rbx
	movq	%r11, %rax
	movq	%rdx, %r11
	movq	%rbx, %r14
	movq	%r13, %rbx
	testq	%rdx, %rdx
	jne	.L404
	cmpq	$1, %rax
	jg	.L451
	testq	%r13, %r13
	leaq	0(%r13,%rdi), %rax
	cmovs	%rax, %r13
	xorl	%edx, %edx
	movl	%r13d, %eax
	imulq	$1252161, %rax, %rax
	imull	$-383821921, %eax, %r11d
	imulq	%rdi, %r11
	addq	%r11, %rax
	adcq	$0, %rdx
	shrdq	$32, %rdx, %rax
	movl	%eax, %edx
	cmpq	%rax, %r12
	jnb	.L209
	addl	$1119, %edx
.L209:
	movl	%r10d, %eax
	imulq	%rdx, %rax
	xorl	%edx, %edx
	imull	$-383821921, %eax, %r11d
	imulq	%rdi, %r11
	addq	%r11, %rax
	adcq	$0, %rdx
	shrdq	$32, %rdx, %rax
	cmpq	%rax, %r12
	jnb	.L443
	addl	$1119, %eax
.L443:
	movq	%rax, %r10
	xorl	%r11d, %r11d
	imulq	%rax, %r10
	imull	$-383821921, %r10d, %edx
	imulq	%rdi, %rdx
	addq	%rdx, %r10
	adcq	$0, %r11
	addq	%rcx, %rcx
	shrdq	$32, %r11, %r10
	leal	(%r15,%r15), %r11d
	cmpq	%rcx, %r12
	leal	1119(%r11), %edx
	cmovb	%edx, %r11d
	leal	1119(%r10), %edx
	cmpq	%r10, %r12
	cmovnb	%r10d, %edx
	cmpl	%r11d, %edx
	jb	.L203
	subl	%r11d, %edx
	movl	%edx, %r11d
	jmp	.L214
	.p2align 4
	.p2align 3
.L455:
	movq	48(%rsp), %rbx
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	subq	%rbx, %rax
	js	.L342
	vcvtsi2sdq	%rax, %xmm7, %xmm0
.L343:
	vdivsd	%xmm6, %xmm0, %xmm0
	decl	56(%rsp)
	movl	96(%rsp), %eax
	vminsd	%xmm8, %xmm0, %xmm8
	jne	.L344
	movq	72(%rsp), %rdx
	vmovapd	%xmm8, %xmm2
	leaq	.LC5(%rip), %rcx
	vmovq	%xmm8, %r8
	xorl	%ebp, %ebp
	movl	$487078699, %r13d
	movl	$-1445549170, %r14d
	movl	$4294966177, %r15d
	call	__mingw_printf
	vmovsd	.LC0(%rip), %xmm8
	movb	%bpl, 32(%rsp)
	movl	$3, 64(%rsp)
	movl	$1119, %ebp
	.p2align 4
	.p2align 3
.L400:
	movl	$0, 92(%rsp)
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	xorl	%r12d, %r12d
	movl	$4294966176, %r8d
	movq	%rax, 56(%rsp)
	jmp	.L395
	.p2align 4
	.p2align 3
.L459:
	movl	%ebp, %ecx
	xorl	%ebx, %ebx
	movq	%rcx, 48(%rsp)
	imulq	%rcx, %rcx
	imull	$-383821921, %ecx, %eax
	imulq	%r15, %rax
	addq	%rax, %rcx
	adcq	$0, %rbx
	shrdq	$32, %rbx, %rcx
	movl	%ecx, %eax
	cmpq	%rcx, %r8
	jnb	.L346
	addl	$1119, %eax
.L346:
	movl	%r14d, %ebx
	movl	$4005337200, %esi
	xorl	%edi, %edi
	imulq	%rbx, %rsi
	imull	$-383821921, %esi, %edx
	imulq	%r15, %rdx
	addq	%rdx, %rsi
	adcq	$0, %rdi
	shrdq	$32, %rdi, %rsi
	movl	%esi, %ecx
	cmpq	%rsi, %r8
	jnb	.L347
	addl	$1119, %ecx
.L347:
	movl	$3168653529, %esi
	xorl	%edi, %edi
	imulq	%rax, %rsi
	imull	$-383821921, %esi, %edx
	imulq	%r15, %rdx
	addq	%rdx, %rsi
	adcq	$0, %rdi
	shrdq	$32, %rdi, %rsi
	movl	%esi, %r10d
	cmpq	%rsi, %r8
	jnb	.L348
	addl	$1119, %r10d
.L348:
	imulq	$163980240, %r13, %rsi
	xorl	%edi, %edi
	imull	$-383821921, %esi, %edx
	imulq	%r15, %rdx
	addq	%rdx, %rsi
	adcq	$0, %rdi
	shrdq	$32, %rdi, %rsi
	movl	%esi, %r9d
	cmpq	%rsi, %r8
	jnb	.L349
	addl	$1119, %r9d
.L349:
	imulq	48(%rsp), %rax
	xorl	%edx, %edx
	imull	$-383821921, %eax, %esi
	imulq	%r15, %rsi
	addq	%rsi, %rax
	adcq	$0, %rdx
	shrdq	$32, %rdx, %rax
	movl	%eax, %edx
	cmpq	%rax, %r8
	jnb	.L350
	addl	$1119, %edx
.L350:
	movl	%edx, %eax
	xorl	%edx, %edx
	imulq	$99804595, %rax, %rax
	imull	$-383821921, %eax, %esi
	imulq	%r15, %rsi
	addq	%rsi, %rax
	adcq	$0, %rdx
	shrdq	$32, %rdx, %rax
	movl	%eax, %edi
	cmpq	%rax, %r8
	jnb	.L351
	addl	$1119, %edi
.L351:
	cmpl	%ecx, %r10d
	je	.L457
	movl	$-1119, %eax
	movl	%r10d, %ebx
	subl	%ecx, %eax
	subl	%ecx, %ebx
	addl	%r10d, %eax
	cmpl	%ecx, %r10d
	cmovb	%eax, %ebx
	movl	$-1119, %eax
	movl	%ebx, %ebp
	subl	%r9d, %eax
	movl	%edi, %ebx
	addl	%edi, %eax
	subl	%r9d, %ebx
	cmpl	%r9d, %edi
	cmovb	%eax, %ebx
	movq	%rbp, %rax
	xorl	%edx, %edx
	imulq	%rbp, %rax
	imull	$-383821921, %eax, %r10d
	imulq	%r15, %r10
	addq	%r10, %rax
	adcq	$0, %rdx
	shrdq	$32, %rdx, %rax
	movl	%eax, %edx
	cmpq	%rax, %r8
	jnb	.L379
	addl	$1119, %edx
.L379:
	movq	%rbp, %rsi
	xorl	%edi, %edi
	imulq	%rdx, %rsi
	imull	$-383821921, %esi, %eax
	imulq	%r15, %rax
	addq	%rax, %rsi
	adcq	$0, %rdi
	shrdq	$32, %rdi, %rsi
	movl	%esi, %r10d
	cmpq	%rsi, %r8
	jnb	.L380
	addl	$1119, %r10d
.L380:
	movl	%ecx, %eax
	imulq	%rdx, %rax
	xorl	%edx, %edx
	imull	$-383821921, %eax, %esi
	imulq	%r15, %rsi
	addq	%rsi, %rax
	adcq	$0, %rdx
	shrdq	$32, %rdx, %rax
	movl	%eax, %r13d
	cmpq	%rax, %r8
	jnb	.L381
	addl	$1119, %r13d
.L381:
	movl	%r13d, %eax
	leal	(%r13,%r13), %esi
	addq	%rax, %rax
	leal	1119(%rsi), %ecx
	cmpq	%rax, %r8
	movl	%ebx, %eax
	cmovb	%ecx, %esi
	movq	%rax, %rcx
	xorl	%ebx, %ebx
	imulq	%rax, %rcx
	imull	$-383821921, %ecx, %edi
	imulq	%r15, %rdi
	addq	%rdi, %rcx
	adcq	$0, %rbx
	shrdq	$32, %rbx, %rcx
	movl	%ecx, %edx
	cmpq	%rcx, %r8
	jnb	.L383
	addl	$1119, %edx
.L383:
	movl	$-1119, %ecx
	movl	%edx, %edi
	movl	$-1119, %r14d
	subl	%r10d, %ecx
	subl	%r10d, %edi
	addl	%edx, %ecx
	cmpl	%r10d, %edx
	cmovnb	%edi, %ecx
	subl	%esi, %r14d
	movl	%ecx, %ebx
	addl	%ecx, %r14d
	subl	%esi, %ebx
	cmpl	%esi, %ecx
	movl	%r10d, %ecx
	cmovnb	%ebx, %r14d
	imulq	%r9, %rcx
	xorl	%ebx, %ebx
	imull	$-383821921, %ecx, %esi
	imulq	%r15, %rsi
	addq	%rsi, %rcx
	adcq	$0, %rbx
	shrdq	$32, %rbx, %rcx
	movl	%ecx, %r9d
	cmpq	%rcx, %r8
	jnb	.L388
	addl	$1119, %r9d
.L388:
	movl	%r13d, %edx
	leal	-1119(%r13), %ecx
	subl	%r14d, %ecx
	subl	%r14d, %edx
	cmpl	%r14d, %r13d
	cmovb	%ecx, %edx
	imulq	%rdx, %rax
	xorl	%edx, %edx
	imull	$-383821921, %eax, %ecx
	imulq	%r15, %rcx
	addq	%rcx, %rax
	adcq	$0, %rdx
	shrdq	$32, %rdx, %rax
	movl	%eax, %edi
	cmpq	%rax, %r8
	jnb	.L391
	addl	$1119, %edi
.L391:
	movl	$-1119, %r13d
	movl	%edi, %eax
	subl	%r9d, %r13d
	subl	%r9d, %eax
	addl	%edi, %r13d
	cmpl	%r9d, %edi
	cmovnb	%rax, %r13
	imulq	$974157398, 48(%rsp), %rax
	xorl	%edx, %edx
	imull	$-383821921, %eax, %ecx
	imulq	%r15, %rcx
	addq	%rcx, %rax
	adcq	$0, %rdx
	shrdq	$32, %rdx, %rax
	movl	%eax, %edx
	cmpq	%rax, %r8
	jnb	.L394
	addl	$1119, %edx
.L394:
	movl	%edx, %eax
	xorl	%edx, %edx
	imulq	%rbp, %rax
	imull	$-383821921, %eax, %ecx
	imulq	%r15, %rcx
	addq	%rcx, %rax
	adcq	$0, %rdx
	shrdq	$32, %rdx, %rax
	movl	%eax, %ebp
	cmpq	%rax, %r8
	jnb	.L345
	addl	$1119, %ebp
	.p2align 4
	.p2align 3
.L345:
	incq	%r12
	xorl	%r14d, 92(%rsp)
	movl	%r14d, (%r11)
	cmpq	$3000000, %r12
	je	.L458
.L395:
	cmpb	$0, 32(%rsp)
	movzbl	%r12b, %eax
	leaq	112(%rsp,%rax,4), %r11
	je	.L459
	movb	$0, 32(%rsp)
	movl	$974157398, %ebp
	movl	$99804595, %r13d
	movl	$-1126313767, %r14d
	jmp	.L345
	.p2align 4
	.p2align 3
.L458:
	movq	56(%rsp), %rsi
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	subq	%rsi, %rax
	js	.L396
	vcvtsi2sdq	%rax, %xmm7, %xmm0
.L397:
	vdivsd	%xmm6, %xmm0, %xmm0
	decl	64(%rsp)
	movl	92(%rsp), %eax
	vminsd	%xmm8, %xmm0, %xmm2
	vmovapd	%xmm2, %xmm8
	jne	.L400
	vmovaps	1136(%rsp), %xmm6
	vmovaps	1152(%rsp), %xmm7
	leaq	.LC6(%rip), %rcx
	vmovq	%xmm2, %r8
	vmovaps	1168(%rsp), %xmm8
	movq	72(%rsp), %rdx
	addq	$1192, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	jmp	__mingw_printf
	.p2align 4
	.p2align 3
.L457:
	cmpl	%r9d, %edi
	je	.L460
	xorl	%ebp, %ebp
	xorl	%r13d, %r13d
	xorl	%r14d, %r14d
	movb	$1, 32(%rsp)
	jmp	.L345
	.p2align 4
	.p2align 3
.L454:
	cmpl	%r9d, %edi
	je	.L461
	xorl	%r12d, %r12d
	xorl	%edi, %edi
	xorl	%r15d, %r15d
	movl	$1, %esi
	jmp	.L294
	.p2align 4
	.p2align 3
.L452:
	cmpl	$487078699, %edi
	je	.L462
	xorl	%edi, %edi
	xorl	%r15d, %r15d
	movl	$1, %ebp
	jmp	.L226
	.p2align 4
	.p2align 3
.L449:
	testl	%r15d, %r15d
	jne	.L463
	xorl	%eax, %eax
	movl	$1445548051, %r9d
.L257:
	leal	-1119(%r15), %edx
	movl	%r9d, %r15d
	subl	%r9d, %edx
	jmp	.L258
.L463:
	xorl	%edx, %edx
	xorl	%eax, %eax
.L253:
	subl	%r15d, %edx
	subl	$1119, %edx
	jmp	.L254
	.p2align 4
	.p2align 3
.L342:
	movq	%rax, %rdx
	andl	$1, %eax
	shrq	%rdx
	orq	%rax, %rdx
	vcvtsi2sdq	%rdx, %xmm7, %xmm0
	vaddsd	%xmm0, %xmm0, %xmm0
	jmp	.L343
	.p2align 4
	.p2align 3
.L396:
	movq	%rax, %rdx
	andl	$1, %eax
	shrq	%rdx
	orq	%rax, %rdx
	vcvtsi2sdq	%rdx, %xmm7, %xmm0
	vaddsd	%xmm0, %xmm0, %xmm0
	jmp	.L397
	.p2align 4
	.p2align 3
.L262:
	movq	%rax, %rdx
	andl	$1, %eax
	shrq	%rdx
	orq	%rax, %rdx
	vcvtsi2sdq	%rdx, %xmm7, %xmm0
	vaddsd	%xmm0, %xmm0, %xmm0
	jmp	.L263
	.p2align 4
	.p2align 3
.L221:
	movq	%rax, %rdx
	andl	$1, %eax
	shrq	%rdx
	orq	%rax, %rdx
	vcvtsi2sdq	%rdx, %xmm7, %xmm0
	vaddsd	%xmm0, %xmm0, %xmm0
	jmp	.L222
	.p2align 4
	.p2align 3
.L289:
	movq	%rax, %rdx
	andl	$1, %eax
	shrq	%rdx
	orq	%rax, %rdx
	vcvtsi2sdq	%rdx, %xmm7, %xmm0
	vaddsd	%xmm0, %xmm0, %xmm0
	jmp	.L290
.L462:
	xorl	%r10d, %r10d
	movl	$1, %r11d
	movl	$1121630278, %r9d
	movq	%rbx, %rax
	jmp	.L228
	.p2align 5
	.p2align 4
	.p2align 3
.L408:
	movq	%rdi, %r11
.L228:
	cqto
	movq	%r10, %rdi
	movq	%r11, %r10
	idivq	%r9
	imulq	%r11, %rax
	subq	%rax, %rdi
	movq	%r9, %rax
	movq	%rdx, %r9
	testq	%rdx, %rdx
	jne	.L408
	cmpq	$1, %rax
	jg	.L409
	movl	$4294966177, %edx
	testq	%r11, %r11
	leaq	(%r11,%rdx), %rax
	cmovs	%rax, %r11
	movl	%r11d, %eax
	imulq	$1252161, %rax, %rax
	imull	$-383821921, %eax, %r9d
	imulq	%rdx, %r9
	xorl	%edx, %edx
	addq	%r9, %rax
	movl	$4294966176, %r9d
	adcq	$0, %rdx
	shrdq	$32, %rdx, %rax
	movl	%eax, %edx
	cmpq	%rax, %r9
	jnb	.L231
	addl	$1119, %edx
.L231:
	movl	%edx, %eax
	movl	$3457508611, %edx
	movl	$4294966177, %r10d
	imulq	%rdx, %rax
	xorl	%edx, %edx
	imull	$-383821921, %eax, %r9d
	imulq	%r10, %r9
	addq	%r9, %rax
	movl	$4294966176, %r9d
	adcq	$0, %rdx
	shrdq	$32, %rdx, %rax
	cmpq	%rax, %r9
	jnb	.L464
	leal	1119(%rax), %r9d
.L446:
	movq	%r9, %rax
	imulq	%r9, %rax
	imull	$-383821921, %eax, %edx
	imulq	%rdx, %r10
	xorl	%edx, %edx
	addq	%r10, %rax
	adcq	$0, %rdx
	shrdq	$32, %rdx, %rax
	shrq	$32, %rdx
	movq	%rax, 32(%rsp)
	movq	%rdx, 40(%rsp)
	movl	$4294966176, %edx
	cmpq	32(%rsp), %rdx
	movl	%eax, %r15d
	jnb	.L234
	leal	1119(%rax), %r15d
.L234:
	cmpl	$1403870074, %r15d
	jbe	.L235
	subl	$1403870075, %r15d
	cmpl	$-1445549170, %r15d
	ja	.L237
	movl	$-1445549170, %eax
	subl	%r15d, %eax
.L238:
	imulq	%r9, %rax
	movl	$4294966177, %edx
	imull	$-383821921, %eax, %r9d
	imulq	%rdx, %r9
	xorl	%edx, %edx
	addq	%r9, %rax
	adcq	$0, %rdx
	shrdq	$32, %rdx, %rax
	movl	$4294966176, %edx
	movl	%eax, %edi
	cmpq	%rax, %rdx
	jnb	.L229
	addl	$1119, %edi
.L229:
	cmpl	$487078698, %edi
	jbe	.L239
	subl	$487078699, %edi
	jmp	.L226
.L460:
	movq	%rbx, %rax
	movl	$4294966177, %edx
	imulq	%rbx, %rax
	imull	$-383821921, %eax, %ecx
	imulq	%rdx, %rcx
	xorl	%edx, %edx
	addq	%rcx, %rax
	adcq	$0, %rdx
	shrdq	$32, %rdx, %rax
	movl	$4294966176, %edx
	movl	%eax, %r9d
	cmpq	%rax, %rdx
	jnb	.L353
	addl	$1119, %r9d
.L353:
	movq	%r13, %rax
	movl	$4294966177, %edx
	imulq	%r13, %rax
	imull	$-383821921, %eax, %ecx
	imulq	%rdx, %rcx
	xorl	%edx, %edx
	addq	%rcx, %rax
	movl	$4294966176, %ecx
	adcq	$0, %rdx
	shrdq	$32, %rdx, %rax
	movl	%eax, %esi
	cmpq	%rax, %rcx
	jnb	.L354
	addl	$1119, %esi
.L354:
	leal	(%rsi,%rsi), %ecx
	cmpl	$2147483088, %esi
	movl	$4294966177, %edx
	movl	%esi, %edi
	leal	1119(%rcx), %eax
	cmovbe	%ecx, %eax
	imulq	%rbx, %rax
	imull	$-383821921, %eax, %ecx
	imulq	%rdx, %rcx
	xorl	%edx, %edx
	addq	%rcx, %rax
	movl	$4294966176, %ecx
	adcq	$0, %rdx
	shrdq	$32, %rdx, %rax
	movl	%eax, %esi
	cmpq	%rax, %rcx
	jnb	.L356
	addl	$1119, %esi
.L356:
	leal	(%rsi,%rsi), %ebx
	cmpl	$2147483088, %esi
	movl	%r9d, %ecx
	movl	$4294966176, %r10d
	leal	1119(%rbx), %eax
	cmova	%eax, %ebx
	leal	(%r9,%r9), %eax
	cmpl	$2147483088, %r9d
	leal	1119(%rax), %edx
	cmova	%edx, %eax
	movl	%eax, %edx
	addq	%rcx, %rdx
	leal	1119(%r9,%rax), %ecx
	addl	%r9d, %eax
	leal	(%rbx,%rbx), %r9d
	cmpq	%rdx, %r10
	movl	%ebx, %edx
	cmovb	%ecx, %eax
	addq	%rdx, %rdx
	leal	1119(%r9), %ecx
	movl	%eax, %esi
	cmpq	%rdx, %r10
	movl	$4294966177, %edx
	movq	%rsi, %rax
	cmovb	%ecx, %r9d
	imulq	%rsi, %rax
	imull	$-383821921, %eax, %ecx
	imulq	%rdx, %rcx
	xorl	%edx, %edx
	addq	%rcx, %rax
	adcq	$0, %rdx
	shrdq	$32, %rdx, %rax
	movl	%eax, %ecx
	cmpq	%rax, %r10
	jnb	.L362
	leal	1119(%rax), %ecx
.L362:
	movl	%ecx, %eax
	movl	$4294966177, %edx
	subl	%r9d, %eax
	cmpl	%r9d, %ecx
	leal	-1119(%rax), %r14d
	cmovnb	%eax, %r14d
	addl	%ebp, %ebp
	cmpq	$2147483088, 48(%rsp)
	leal	1119(%rbp), %eax
	cmovbe	%ebp, %eax
	imulq	%r13, %rax
	imull	$-383821921, %eax, %ecx
	imulq	%rdx, %rcx
	xorl	%edx, %edx
	addq	%rcx, %rax
	adcq	$0, %rdx
	shrdq	$32, %rdx, %rax
	movl	$4294966176, %edx
	movl	%eax, %ebp
	cmpq	%rax, %rdx
	jnb	.L366
	addl	$1119, %ebp
.L366:
	movq	%rdi, %rax
	movl	$4294966177, %edx
	imulq	%rdi, %rax
	imull	$-383821921, %eax, %ecx
	imulq	%rdx, %rcx
	xorl	%edx, %edx
	addq	%rcx, %rax
	adcq	$0, %rdx
	shrdq	$32, %rdx, %rax
	movl	$4294966176, %edx
	movl	%eax, %ecx
	cmpq	%rax, %rdx
	jnb	.L367
	addl	$1119, %ecx
.L367:
	leal	(%rcx,%rcx), %edx
	cmpl	$2147483088, %ecx
	leal	1119(%rdx), %eax
	cmova	%eax, %edx
	leal	(%rdx,%rdx), %eax
	cmpl	$2147483088, %edx
	leal	1119(%rax), %ecx
	cmova	%ecx, %eax
	leal	(%rax,%rax), %ecx
	cmpl	$2147483088, %eax
	leal	-1119(%rbx), %eax
	leal	1119(%rcx), %edx
	cmova	%edx, %ecx
	movl	%ebx, %edx
	subl	%r14d, %eax
	subl	%r14d, %edx
	cmpl	%r14d, %ebx
	cmovnb	%edx, %eax
	movl	$4294966177, %edx
	imulq	%rsi, %rax
	imull	$-383821921, %eax, %r9d
	imulq	%rdx, %r9
	xorl	%edx, %edx
	addq	%r9, %rax
	movl	$4294966176, %r9d
	adcq	$0, %rdx
	shrdq	$32, %rdx, %rax
	movl	%eax, %edi
	cmpq	%rax, %r9
	jnb	.L373
	addl	$1119, %edi
.L373:
	movl	%edi, %eax
	subl	%ecx, %eax
	cmpl	%ecx, %edi
	leal	-1119(%rax), %r13d
	cmovnb	%rax, %r13
	jmp	.L345
.L461:
	movl	%ecx, %r9d
	movl	$4294966177, %edx
	movq	%r9, %rax
	imulq	%r9, %rax
	imull	$-383821921, %eax, %ecx
	imulq	%rdx, %rcx
	xorl	%edx, %edx
	addq	%rcx, %rax
	adcq	$0, %rdx
	shrdq	$32, %rdx, %rax
	movl	$4294966176, %edx
	movl	%eax, %ecx
	cmpq	%rax, %rdx
	jnb	.L300
	addl	$1119, %ecx
.L300:
	movl	%edi, %r11d
	movl	$4294966177, %edx
	movq	%r11, %rax
	imulq	%r11, %rax
	imull	$-383821921, %eax, %r8d
	imulq	%rdx, %r8
	xorl	%edx, %edx
	addq	%r8, %rax
	movl	$4294966176, %r8d
	adcq	$0, %rdx
	shrdq	$32, %rdx, %rax
	movl	%eax, %edi
	cmpq	%rax, %r8
	jnb	.L301
	addl	$1119, %edi
.L301:
	leal	(%rdi,%rdi), %r8d
	movl	%edi, %eax
	cmpl	$2147483088, %edi
	movl	$4294966177, %edx
	movq	%rax, 64(%rsp)
	leal	1119(%r8), %eax
	cmovbe	%r8d, %eax
	imulq	%r9, %rax
	imull	$-383821921, %eax, %r8d
	imulq	%rdx, %r8
	xorl	%edx, %edx
	addq	%r8, %rax
	movl	$4294966176, %r8d
	adcq	$0, %rdx
	shrdq	$32, %rdx, %rax
	movl	%eax, %edi
	cmpq	%rax, %r8
	jnb	.L303
	addl	$1119, %edi
.L303:
	leal	(%rdi,%rdi), %r10d
	cmpl	$2147483088, %edi
	movl	%ecx, %r8d
	movl	$4294966176, %r9d
	leal	1119(%r10), %eax
	cmova	%eax, %r10d
	leal	(%rcx,%rcx), %eax
	cmpl	$2147483088, %ecx
	leal	1119(%rax), %edx
	cmova	%edx, %eax
	movl	%eax, %edx
	addq	%r8, %rdx
	leal	1119(%rcx,%rax), %r8d
	addl	%ecx, %eax
	leal	(%r10,%r10), %ecx
	cmpq	%rdx, %r9
	movl	%r10d, %edx
	cmovb	%r8d, %eax
	addq	%rdx, %rdx
	leal	1119(%rcx), %r8d
	movl	%eax, %edi
	cmpq	%rdx, %r9
	movl	$4294966177, %edx
	movq	%rdi, %rax
	cmovb	%r8d, %ecx
	imulq	%rdi, %rax
	imull	$-383821921, %eax, %r8d
	imulq	%rdx, %r8
	xorl	%edx, %edx
	addq	%r8, %rax
	adcq	$0, %rdx
	shrdq	$32, %rdx, %rax
	movl	%eax, %r15d
	cmpq	%rax, %r9
	jnb	.L309
	leal	1119(%rax), %r15d
.L309:
	movl	%r15d, %eax
	movl	$4294966177, %edx
	subl	%ecx, %eax
	cmpl	%ecx, %r15d
	leal	-1119(%rax), %r15d
	cmovnb	%eax, %r15d
	addl	%r12d, %r12d
	cmpq	$2147483088, 32(%rsp)
	leal	1119(%r12), %eax
	cmovbe	%r12d, %eax
	imulq	%r11, %rax
	imull	$-383821921, %eax, %ecx
	imulq	%rdx, %rcx
	xorl	%edx, %edx
	addq	%rcx, %rax
	adcq	$0, %rdx
	shrdq	$32, %rdx, %rax
	movl	$4294966176, %edx
	movl	%eax, %r12d
	cmpq	%rax, %rdx
	jnb	.L313
	addl	$1119, %r12d
.L313:
	movq	64(%rsp), %rax
	movl	$4294966177, %edx
	imulq	%rax, %rax
	imull	$-383821921, %eax, %ecx
	imulq	%rdx, %rcx
	xorl	%edx, %edx
	addq	%rcx, %rax
	adcq	$0, %rdx
	shrdq	$32, %rdx, %rax
	movl	$4294966176, %edx
	movl	%eax, %ecx
	cmpq	%rax, %rdx
	jnb	.L314
	addl	$1119, %ecx
.L314:
	leal	(%rcx,%rcx), %edx
	cmpl	$2147483088, %ecx
	leal	1119(%rdx), %eax
	cmova	%eax, %edx
	leal	(%rdx,%rdx), %eax
	cmpl	$2147483088, %edx
	leal	1119(%rax), %ecx
	cmova	%ecx, %eax
	leal	(%rax,%rax), %ecx
	cmpl	$2147483088, %eax
	leal	-1119(%r10), %eax
	leal	1119(%rcx), %edx
	cmova	%edx, %ecx
	movl	%r10d, %edx
	subl	%r15d, %eax
	subl	%r15d, %edx
	cmpl	%r15d, %r10d
	cmovnb	%edx, %eax
	movl	$4294966177, %edx
	imulq	%rdi, %rax
	imull	$-383821921, %eax, %r8d
	imulq	%rdx, %r8
	xorl	%edx, %edx
	addq	%r8, %rax
	movl	$4294966176, %r8d
	adcq	$0, %rdx
	shrdq	$32, %rdx, %rax
	movl	%eax, %r10d
	cmpq	%rax, %r8
	jnb	.L320
	addl	$1119, %r10d
.L320:
	movl	%r10d, %eax
	subl	%ecx, %eax
	cmpl	%ecx, %r10d
	leal	-1119(%rax), %edi
	cmovnb	%rax, %rdi
	jmp	.L294
.L453:
	movq	%rax, %r9
	imulq	%rax, %r9
	imull	$-383821921, %r9d, %edx
	movq	%r9, %r10
	imulq	%rbx, %rdx
	jmp	.L447
.L409:
	xorl	%edi, %edi
	movl	$-1403871194, %r15d
.L239:
	subl	$487079818, %edi
	jmp	.L226
.L464:
	movq	%rax, %r9
	jmp	.L446
.L235:
	subl	$1403871194, %r15d
.L237:
	movl	$-1445550289, %eax
	subl	%r15d, %eax
	jmp	.L238
	.seh_endproc
	.section	.text$_ZN2ec8JacobianIN2fp9FpBarrettILj4294966177EEEE3addERKS4_S6_,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZN2ec8JacobianIN2fp9FpBarrettILj4294966177EEEE3addERKS4_S6_
	.def	_ZN2ec8JacobianIN2fp9FpBarrettILj4294966177EEEE3addERKS4_S6_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN2ec8JacobianIN2fp9FpBarrettILj4294966177EEEE3addERKS4_S6_
_ZN2ec8JacobianIN2fp9FpBarrettILj4294966177EEEE3addERKS4_S6_:
.LFB4881:
	pushq	%r15
	.seh_pushreg	%r15
	pushq	%r14
	.seh_pushreg	%r14
	pushq	%r13
	.seh_pushreg	%r13
	pushq	%r12
	.seh_pushreg	%r12
	pushq	%rbp
	.seh_pushreg	%rbp
	pushq	%rdi
	.seh_pushreg	%rdi
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$40, %rsp
	.seh_stackalloc	40
	.seh_endprologue
	cmpb	$0, 12(%rdx)
	movq	%rcx, %r10
	movq	%rdx, %rcx
	je	.L466
	vmovdqu	(%r8), %xmm0
	vmovdqu	%xmm0, (%r10)
.L465:
	movq	%r10, %rax
	addq	$40, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	ret
	.p2align 4
	.p2align 3
.L466:
	cmpb	$0, 12(%r8)
	je	.L468
	vmovdqu	(%rdx), %xmm0
	vmovdqu	%xmm0, (%r10)
	jmp	.L465
	.p2align 4
	.p2align 3
.L468:
	movl	8(%rdx), %r9d
	movabsq	$4294968415, %rax
	movl	$4294966177, %r11d
	movl	%r9d, 28(%rsp)
	movq	%r9, %r14
	imulq	%r9, %r9
	mulq	%r9
	movl	$4294966176, %eax
	imulq	%r11, %rdx
	subq	%rdx, %r9
	movq	%r9, %r15
	cmpq	%r9, %rax
	jnb	.L469
	movq	%r9, %rdx
	subq	%r11, %rdx
	movq	%rdx, %r15
	cmpq	%rdx, %rax
	jnb	.L469
	movabsq	$-8589932354, %rax
	leaq	(%r9,%rax), %r15
.L469:
	movl	8(%r8), %r11d
	movabsq	$4294968415, %rax
	movl	$4294966177, %esi
	movq	%r11, %r9
	imulq	%r11, %r9
	mulq	%r9
	movq	%r9, %rax
	imulq	%rsi, %rdx
	subq	%rdx, %rax
	movl	$4294966176, %edx
	cmpq	%rax, %rdx
	jnb	.L470
	movq	%rax, %r9
	subq	%rsi, %r9
	cmpq	%r9, %rdx
	jnb	.L527
	movabsq	$-8589932354, %rdx
	addq	%rdx, %rax
.L470:
	movl	(%rcx), %ebx
	movl	%eax, %eax
	movq	%rax, %r12
	movq	%rbx, 16(%rsp)
	imulq	%rax, %rbx
	movabsq	$4294968415, %rax
	mulq	%rbx
	movl	$4294966177, %eax
	movq	%rbx, %r9
	imulq	%rax, %rdx
	subq	%rdx, %r9
	movq	%r9, %rbx
	movq	%r9, %rdi
	movl	$4294966176, %r9d
	cmpq	%rbx, %r9
	jnb	.L471
	movq	%rbx, %rdx
	subq	%rax, %rdx
	movq	%rdx, %rdi
	cmpq	%rdx, %r9
	jnb	.L471
	movabsq	$-8589932354, %rax
	leaq	(%rbx,%rax), %rdi
.L471:
	movl	(%r8), %eax
	movl	%r15d, %r9d
	movabsq	$4294968415, %rdx
	movl	$4294966177, %esi
	movl	%edi, %ebp
	imulq	%r9, %rax
	movq	%rax, 8(%rsp)
	mulq	%rdx
	movq	8(%rsp), %rax
	imulq	%rsi, %rdx
	subq	%rdx, %rax
	movl	$4294966176, %edx
	cmpq	%rax, %rdx
	jnb	.L472
	movq	%rax, %rbx
	subq	%rsi, %rbx
	cmpq	%rbx, %rdx
	jnb	.L529
	movabsq	$-8589932354, %rdx
	addq	%rdx, %rax
.L472:
	movl	%eax, %r15d
	movq	%r12, %rax
	movabsq	$4294968415, %rdx
	movl	$4294966177, %esi
	imulq	%r11, %rax
	movq	%rax, 8(%rsp)
	mulq	%rdx
	movq	8(%rsp), %rax
	imulq	%rsi, %rdx
	subq	%rdx, %rax
	movl	$4294966176, %edx
	cmpq	%rax, %rdx
	jnb	.L473
	movq	%rax, %rbx
	subq	%rsi, %rbx
	cmpq	%rbx, %rdx
	jnb	.L530
	movabsq	$-8589932354, %rdx
	addq	%rdx, %rax
.L473:
	movl	4(%rcx), %ebx
	movl	%eax, %ecx
	movabsq	$4294968415, %rax
	imulq	%rbx, %rcx
	movq	%rbx, %r13
	mulq	%rcx
	movl	$4294966177, %eax
	imulq	%rax, %rdx
	subq	%rdx, %rcx
	movl	$4294966176, %edx
	cmpq	%rcx, %rdx
	jnb	.L474
	movq	%rcx, %rsi
	subq	%rax, %rsi
	cmpq	%rsi, %rdx
	jnb	.L531
	movabsq	$-8589932354, %rax
	addq	%rax, %rcx
.L474:
	imulq	%r14, %r9
	movabsq	$4294968415, %rax
	movl	%ecx, %r12d
	mulq	%r9
	movl	$4294966177, %eax
	imulq	%rax, %rdx
	subq	%rdx, %r9
	movl	$4294966176, %edx
	cmpq	%r9, %rdx
	jnb	.L475
	movq	%r9, %rsi
	subq	%rax, %rsi
	cmpq	%rsi, %rdx
	jnb	.L532
	movabsq	$-8589932354, %rax
	addq	%rax, %r9
.L475:
	movl	4(%r8), %eax
	movl	%r9d, %r9d
	imulq	%rax, %r9
	movabsq	$4294968415, %rax
	mulq	%r9
	movl	$4294966177, %eax
	imulq	%rax, %rdx
	subq	%rdx, %r9
	movl	$4294966176, %edx
	cmpq	%r9, %rdx
	jnb	.L476
	movq	%r9, %r8
	subq	%rax, %r8
	cmpq	%r8, %rdx
	jnb	.L533
	movabsq	$-8589932354, %rax
	addq	%rax, %r9
.L476:
	cmpl	%ebp, %r15d
	je	.L549
	movl	$-1119, %eax
	movl	%r15d, %r8d
	movl	%eax, %edx
	subl	%ebp, %r8d
	subl	%ebp, %edx
	addl	%r15d, %edx
	cmpl	%ebp, %r15d
	cmovnb	%r8d, %edx
	movl	%r9d, %r8d
	subl	%r12d, %eax
	addl	%r9d, %eax
	subl	%r12d, %r8d
	cmpl	%r12d, %r9d
	movl	$4294966177, %r9d
	cmovb	%eax, %r8d
	movabsq	$4294968415, %rax
	movl	%r8d, %esi
	movl	%edx, %r8d
	movq	%r8, %rbp
	imulq	%r8, %r8
	mulq	%r8
	movq	%r8, %rax
	imulq	%r9, %rdx
	subq	%rdx, %rax
	movl	$4294966176, %edx
	cmpq	%rax, %rdx
	jnb	.L509
	movq	%rax, %r8
	subq	%r9, %r8
	cmpq	%r8, %rdx
	jnb	.L540
	movabsq	$-8589932354, %rdx
	addq	%rdx, %rax
.L509:
	movl	%eax, %r9d
	movq	%rbp, %r8
	movabsq	$4294968415, %rax
	imulq	%r9, %r8
	mulq	%r8
	movl	$4294966177, %eax
	imulq	%rax, %rdx
	subq	%rdx, %r8
	movq	%r8, %rbx
	movq	%r8, %r15
	movl	$4294966176, %r8d
	cmpq	%rbx, %r8
	jnb	.L510
	movq	%rbx, %rdx
	subq	%rax, %rdx
	movq	%rdx, %r15
	cmpq	%rdx, %r8
	jb	.L550
.L510:
	movl	%edi, %r8d
	movabsq	$4294968415, %rax
	movl	%r15d, %r13d
	imulq	%r9, %r8
	movl	$4294966177, %r9d
	mulq	%r8
	movl	$4294966176, %eax
	imulq	%r9, %rdx
	subq	%rdx, %r8
	cmpq	%r8, %rax
	jnb	.L511
	movq	%r8, %rdx
	subq	%r9, %rdx
	cmpq	%rdx, %rax
	jnb	.L542
	movabsq	$-8589932354, %rax
	addq	%rax, %r8
.L511:
	leal	(%r8,%r8), %r9d
	cmpl	$2147483088, %r8d
	movl	%r8d, %r12d
	movl	%esi, %r8d
	leal	1119(%r9), %eax
	movq	%r8, %rdi
	movl	$4294966176, %ebx
	cmova	%eax, %r9d
	imulq	%r8, %r8
	movabsq	$4294968415, %rax
	mulq	%r8
	movl	$4294966177, %eax
	movq	%rdx, %rsi
	movq	%r8, %rdx
	imulq	%rax, %rsi
	subq	%rsi, %rdx
	cmpq	%rdx, %rbx
	jnb	.L513
	movq	%rdx, %r8
	subq	%rax, %r8
	cmpq	%r8, %rbx
	jnb	.L543
	movabsq	$-8589932354, %rax
	addq	%rax, %rdx
.L513:
	movl	$-1119, %r8d
	movl	%edx, %ebx
	movl	%ecx, %ecx
	movl	%r8d, %eax
	subl	%r13d, %ebx
	subl	%r13d, %eax
	addl	%edx, %eax
	cmpl	%r13d, %edx
	cmovnb	%ebx, %eax
	subl	%r9d, %r8d
	movl	%eax, %edx
	addl	%eax, %r8d
	subl	%r9d, %edx
	cmpl	%r9d, %eax
	movl	%r15d, %eax
	movl	$4294966176, %r9d
	cmovnb	%edx, %r8d
	imulq	%rax, %rcx
	movabsq	$4294968415, %rax
	mulq	%rcx
	movl	$4294966177, %eax
	imulq	%rax, %rdx
	subq	%rdx, %rcx
	cmpq	%rcx, %r9
	jnb	.L518
	movq	%rcx, %rdx
	subq	%rax, %rdx
	cmpq	%rdx, %r9
	jnb	.L544
	movabsq	$-8589932354, %rax
	addq	%rax, %rcx
.L518:
	movl	%r12d, %edx
	leal	-1119(%r12), %eax
	movq	%rdi, %rsi
	movl	$4294966177, %ebx
	subl	%r8d, %edx
	subl	%r8d, %eax
	cmpl	%r8d, %r12d
	cmovnb	%edx, %eax
	movabsq	$4294968415, %rdx
	imulq	%rax, %rsi
	movq	%rsi, %rax
	movq	%rsi, 8(%rsp)
	mulq	%rdx
	movq	%rsi, %rax
	imulq	%rbx, %rdx
	subq	%rdx, %rax
	movl	$4294966176, %edx
	cmpq	%rax, %rdx
	jnb	.L521
	movq	%rax, %rsi
	subq	%rbx, %rsi
	cmpq	%rsi, %rdx
	jnb	.L545
	movabsq	$-8589932354, %rdx
	addq	%rdx, %rax
.L521:
	movl	%eax, %r9d
	subl	%ecx, %r9d
	cmpl	%ecx, %eax
	movabsq	$4294968415, %rax
	movl	$4294966177, %ecx
	leal	-1119(%r9), %edx
	cmovb	%edx, %r9d
	imulq	%r14, %r11
	movl	%r9d, %edi
	mulq	%r11
	movl	$4294966176, %eax
	imulq	%rcx, %rdx
	subq	%rdx, %r11
	cmpq	%r11, %rax
	jnb	.L524
	movq	%r11, %rdx
	subq	%rcx, %rdx
	cmpq	%rdx, %rax
	jnb	.L546
	movabsq	$-8589932354, %rax
	addq	%rax, %r11
.L524:
	movl	%r11d, %r11d
	movabsq	$4294968415, %rax
	movl	$4294966177, %r9d
	imulq	%rbp, %r11
	mulq	%r11
	movq	%r11, %rax
	imulq	%r9, %rdx
	subq	%rdx, %rax
	movl	$4294966176, %edx
	cmpq	%rax, %rdx
	jnb	.L525
	movq	%rax, %r11
	subq	%r9, %r11
	cmpq	%r11, %rdx
	jnb	.L547
	movabsq	$-8589932354, %rdx
	addq	%rdx, %rax
.L525:
	movl	%r8d, (%r10)
	movl	%edi, 4(%r10)
	movl	%eax, 8(%r10)
	movb	$0, 12(%r10)
	jmp	.L465
	.p2align 4
	.p2align 3
.L549:
	cmpl	%r12d, %r9d
	je	.L551
	movq	$0, (%r10)
	movl	$0, 8(%r10)
	movb	$1, 12(%r10)
	jmp	.L465
	.p2align 4
	.p2align 3
.L529:
	movq	%rbx, %rax
	jmp	.L472
	.p2align 4
	.p2align 3
.L527:
	movq	%r9, %rax
	jmp	.L470
	.p2align 4
	.p2align 3
.L533:
	movq	%r8, %r9
	jmp	.L476
	.p2align 4
	.p2align 3
.L532:
	movq	%rsi, %r9
	jmp	.L475
	.p2align 4
	.p2align 3
.L531:
	movq	%rsi, %rcx
	jmp	.L474
	.p2align 4
	.p2align 3
.L530:
	movq	%rbx, %rax
	jmp	.L473
	.p2align 4
	.p2align 3
.L547:
	movq	%r11, %rax
	jmp	.L525
	.p2align 4
	.p2align 3
.L546:
	movq	%rdx, %r11
	jmp	.L524
	.p2align 4
	.p2align 3
.L545:
	movq	%rsi, %rax
	jmp	.L521
	.p2align 4
	.p2align 3
.L544:
	movq	%rdx, %rcx
	jmp	.L518
	.p2align 4
	.p2align 3
.L543:
	movq	%r8, %rdx
	jmp	.L513
	.p2align 4
	.p2align 3
.L542:
	movq	%rdx, %r8
	jmp	.L511
	.p2align 4
	.p2align 3
.L550:
	movabsq	$-8589932354, %rax
	leaq	(%rbx,%rax), %r15
	jmp	.L510
	.p2align 4
	.p2align 3
.L540:
	movq	%r8, %rax
	jmp	.L509
	.p2align 4
	.p2align 3
.L551:
	movq	16(%rsp), %rax
	movl	$4294966177, %r8d
	movq	%rax, %rcx
	imulq	%rax, %rcx
	movabsq	$4294968415, %rax
	mulq	%rcx
	movl	$4294966176, %eax
	imulq	%r8, %rdx
	subq	%rdx, %rcx
	cmpq	%rcx, %rax
	jnb	.L479
	movq	%rcx, %rdx
	subq	%r8, %rdx
	cmpq	%rdx, %rax
	jnb	.L534
	movabsq	$-8589932354, %rax
	addq	%rax, %rcx
.L479:
	movq	%r13, %r9
	movabsq	$4294968415, %rax
	movl	$4294966177, %r11d
	movl	%ecx, %r8d
	imulq	%r13, %r9
	mulq	%r9
	movq	%r9, %rax
	imulq	%r11, %rdx
	subq	%rdx, %rax
	movl	$4294966176, %edx
	cmpq	%rax, %rdx
	jnb	.L480
	movq	%rax, %r9
	subq	%r11, %r9
	cmpq	%r9, %rdx
	jnb	.L535
	movabsq	$-8589932354, %rdx
	addq	%rdx, %rax
.L480:
	cmpl	$2147483088, %eax
	leal	1119(%rax,%rax), %r11d
	movl	%eax, %edi
	leal	(%rax,%rax), %eax
	cmova	%r11d, %eax
	movq	16(%rsp), %r11
	movl	$4294966177, %r9d
	movl	$4294966176, %esi
	imulq	%rax, %r11
	movabsq	$4294968415, %rax
	mulq	%r11
	movq	%r11, %rax
	imulq	%r9, %rdx
	subq	%rdx, %rax
	cmpq	%rax, %rsi
	jnb	.L548
	movq	%rax, %rdx
	movl	$4294966176, %esi
	subq	%r9, %rdx
	cmpq	%rdx, %rsi
	jnb	.L484
	movabsq	$-8589932354, %rdx
	addq	%rdx, %rax
.L548:
	movl	%eax, %r11d
.L483:
	addl	%r11d, %r11d
	cmpl	$2147483088, %eax
	leal	(%r8,%r8), %eax
	movl	%ecx, %r9d
	leal	1119(%r11), %edx
	movl	$4294966176, %esi
	movl	$4294966177, %ebx
	cmova	%edx, %r11d
	cmpl	$2147483088, %ecx
	leal	1119(%rax), %edx
	cmova	%edx, %eax
	movl	%eax, %edx
	leal	1119(%r8,%rax), %ecx
	addq	%r9, %rdx
	leal	(%r8,%rax), %r9d
	movl	%r11d, %eax
	cmpq	%rdx, %rsi
	cmovb	%ecx, %r9d
	leal	(%r11,%r11), %ecx
	addq	%rax, %rax
	cmpq	%rax, %rsi
	leal	1119(%rcx), %edx
	movq	%r9, %r8
	movabsq	$4294968415, %rax
	cmovb	%edx, %ecx
	imulq	%r9, %r8
	mulq	%r8
	movq	%r8, %rax
	imulq	%rbx, %rdx
	subq	%rdx, %rax
	cmpq	%rax, %rsi
	jnb	.L491
	movq	%rax, %rdx
	subq	%rbx, %rdx
	cmpq	%rdx, %rsi
	jnb	.L536
	movabsq	$-8589932354, %rdx
	addq	%rdx, %rax
.L491:
	movl	%eax, %edx
	movl	$4294966177, %esi
	subl	%ecx, %edx
	cmpl	%ecx, %eax
	movq	%r13, %rcx
	leal	-1119(%rdx), %r8d
	cmovnb	%edx, %r8d
	movl	28(%rsp), %edx
	addl	%edx, %edx
	cmpq	$2147483088, %r14
	leal	1119(%rdx), %eax
	cmovbe	%edx, %eax
	imulq	%rax, %rcx
	movabsq	$4294968415, %rax
	mulq	%rcx
	movq	%rcx, %rax
	movl	$4294966176, %ecx
	imulq	%rsi, %rdx
	subq	%rdx, %rax
	cmpq	%rax, %rcx
	jnb	.L495
	movq	%rax, %rdx
	subq	%rsi, %rdx
	cmpq	%rdx, %rcx
	jnb	.L537
	movabsq	$-8589932354, %rdx
	addq	%rdx, %rax
.L495:
	movq	%rdi, %rcx
	movl	%eax, %ebx
	movabsq	$4294968415, %rax
	movl	$4294966177, %esi
	imulq	%rdi, %rcx
	mulq	%rcx
	movq	%rcx, %rax
	imulq	%rsi, %rdx
	subq	%rdx, %rax
	movl	$4294966176, %edx
	cmpq	%rax, %rdx
	jnb	.L496
	movq	%rax, %rcx
	subq	%rsi, %rcx
	cmpq	%rcx, %rdx
	jnb	.L538
	movabsq	$-8589932354, %rdx
	addq	%rdx, %rax
.L496:
	leal	(%rax,%rax), %edx
	cmpl	$2147483088, %eax
	movl	$4294966176, %esi
	leal	1119(%rdx), %ecx
	cmova	%ecx, %edx
	leal	(%rdx,%rdx), %eax
	cmpl	$2147483088, %edx
	leal	1119(%rax), %ecx
	cmova	%ecx, %eax
	leal	(%rax,%rax), %ecx
	cmpl	$2147483088, %eax
	leal	-1119(%r11), %eax
	leal	1119(%rcx), %edx
	cmova	%edx, %ecx
	movl	%r11d, %edx
	subl	%r8d, %eax
	subl	%r8d, %edx
	cmpl	%r8d, %r11d
	cmovnb	%edx, %eax
	movabsq	$4294968415, %rdx
	imulq	%r9, %rax
	movl	$4294966177, %r9d
	movq	%rax, %r11
	mulq	%rdx
	movq	%r11, %rax
	imulq	%r9, %rdx
	subq	%rdx, %rax
	cmpq	%rax, %rsi
	jnb	.L502
	movq	%rax, %rdx
	subq	%r9, %rdx
	cmpq	%rdx, %rsi
	jnb	.L539
	movabsq	$-8589932354, %rdx
	addq	%rdx, %rax
.L502:
	movl	%eax, %r9d
	movl	%r8d, (%r10)
	movl	%ebx, 8(%r10)
	subl	%ecx, %r9d
	cmpl	%ecx, %eax
	movb	$0, 12(%r10)
	leal	-1119(%r9), %edx
	movl	%r9d, %eax
	cmovb	%edx, %eax
	movl	%eax, 4(%r10)
	jmp	.L465
.L539:
	movq	%rdx, %rax
	jmp	.L502
.L537:
	movq	%rdx, %rax
	jmp	.L495
.L538:
	movq	%rcx, %rax
	jmp	.L496
.L534:
	movq	%rdx, %rcx
	jmp	.L479
.L535:
	movq	%r9, %rax
	jmp	.L480
.L484:
	movl	%edx, %r11d
	movq	%rdx, %rax
	jmp	.L483
.L536:
	movq	%rdx, %rax
	jmp	.L491
	.seh_endproc
	.section	.text$_Z8bench_ecIN2fp9FpBarrettILj4294966177EEEEvPKc,"x"
	.linkonce discard
	.p2align 4
	.globl	_Z8bench_ecIN2fp9FpBarrettILj4294966177EEEEvPKc
	.def	_Z8bench_ecIN2fp9FpBarrettILj4294966177EEEEvPKc;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8bench_ecIN2fp9FpBarrettILj4294966177EEEEvPKc
_Z8bench_ecIN2fp9FpBarrettILj4294966177EEEEvPKc:
.LFB4624:
	pushq	%r15
	.seh_pushreg	%r15
	pushq	%r14
	.seh_pushreg	%r14
	pushq	%r13
	.seh_pushreg	%r13
	pushq	%r12
	.seh_pushreg	%r12
	pushq	%rbp
	.seh_pushreg	%rbp
	pushq	%rdi
	.seh_pushreg	%rdi
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$1240, %rsp
	.seh_stackalloc	1240
	vmovaps	%xmm6, 1184(%rsp)
	.seh_savexmm	%xmm6, 1184
	vmovaps	%xmm7, 1200(%rsp)
	.seh_savexmm	%xmm7, 1200
	vmovaps	%xmm8, 1216(%rsp)
	.seh_savexmm	%xmm8, 1216
	.seh_endprologue
	vmovsd	.LC0(%rip), %xmm8
	vmovsd	.LC1(%rip), %xmm6
	vxorps	%xmm7, %xmm7, %xmm7
	movl	$560815139, %esi
	movabsq	$4294968415, %rdi
	movl	$4294966176, %ebx
	movl	$1960037684, %ebp
	movq	%rcx, 72(%rsp)
	movl	$3, 40(%rsp)
	.p2align 4
	.p2align 3
.L581:
	movl	$0, 124(%rsp)
	movl	$4294966177, %r12d
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	xorl	%r11d, %r11d
	movq	%rax, 32(%rsp)
	.p2align 4
	.p2align 3
.L578:
	movl	%ebp, %r10d
	movzbl	%r11b, %eax
	movq	%r10, %rcx
	leaq	160(%rsp,%rax,4), %r13
	imulq	%r10, %rcx
	movq	%rcx, %rax
	mulq	%rdi
	movq	%rcx, %rax
	imulq	%r12, %rdx
	subq	%rdx, %rax
	cmpq	%rax, %rbx
	jnb	.L553
	movq	%rax, %rdx
	movabsq	$-8589932354, %r9
	subq	%r12, %rdx
	addq	%r9, %rax
	cmpq	%rdx, %rbx
	cmovnb	%rdx, %rax
.L553:
	movl	%eax, %ecx
	leal	(%rax,%rax), %r9d
	leaq	(%rcx,%rcx), %r8
	leal	1119(%r9), %edx
	cmpq	%r8, %rbx
	cmovb	%edx, %r9d
	movl	%r9d, %edx
	addq	%rcx, %rdx
	leal	1119(%r9,%rax), %ecx
	addl	%eax, %r9d
	leal	(%rsi,%rsi), %eax
	cmpq	%rdx, %rbx
	movl	%esi, %edx
	cmovb	%rcx, %r9
	addq	%rdx, %rdx
	leal	1119(%rax), %ecx
	cmpq	%rdx, %rbx
	jb	.L558
	movl	%eax, %ecx
	testl	%eax, %eax
	je	.L768
.L558:
	xorl	%r8d, %r8d
	movl	$1, %r14d
	movq	%r12, %rax
	jmp	.L563
	.p2align 5
	.p2align 4
	.p2align 3
.L710:
	movq	%r15, %r14
.L563:
	cqto
	movq	%r8, %r15
	movq	%r14, %r8
	idivq	%rcx
	imulq	%r14, %rax
	subq	%rax, %r15
	movq	%rcx, %rax
	movq	%rdx, %rcx
	testq	%rdx, %rdx
	jne	.L710
	cmpq	$1, %rax
	jg	.L769
	testq	%r14, %r14
	leaq	(%r14,%r12), %rax
	cmovs	%rax, %r14
	movl	%r14d, %r14d
	imulq	%r9, %r14
	movq	%r14, %rax
	mulq	%rdi
	imulq	%r12, %rdx
	subq	%rdx, %r14
	cmpq	%r14, %rbx
	jnb	.L770
	movq	%r14, %r8
	subq	%r12, %r8
	cmpq	%r8, %rbx
	jnb	.L764
	leal	2238(%r14), %r8d
.L764:
	movq	%r8, %rcx
	imulq	%r8, %rcx
	movq	%rcx, %rax
	mulq	%rdi
	movq	%rcx, %rax
	imulq	%r12, %rdx
	subq	%rdx, %rax
.L568:
	leal	(%rbp,%rbp), %ecx
	addq	%r10, %r10
	leal	1119(%rcx), %edx
	cmpq	%r10, %rbx
	cmovb	%edx, %ecx
	movq	%rax, %rdx
	cmpq	%rax, %rbx
	jnb	.L571
	movabsq	$-4294966177, %r10
	addq	%r10, %rdx
	movabsq	$-8589932354, %r10
	addq	%r10, %rax
	cmpq	%rdx, %rbx
	cmovb	%rax, %rdx
.L571:
	movl	%edx, %eax
	cmpl	%ecx, %edx
	jb	.L562
	subl	%ecx, %eax
	movl	%eax, %ecx
.L572:
	cmpl	%ecx, %ebp
	jnb	.L561
	leal	-1119(%rbp), %eax
	movl	%ecx, %ebp
	subl	%ecx, %eax
.L574:
	imulq	%rax, %r8
	movq	%r8, %rax
	mulq	%rdi
	movq	%r8, %rax
	imulq	%r12, %rdx
	subq	%rdx, %rax
	cmpq	%rax, %rbx
	jnb	.L575
	movq	%rax, %rdx
	movabsq	$-8589932354, %r10
	subq	%r12, %rdx
	addq	%r10, %rax
	cmpq	%rdx, %rbx
	cmovnb	%rdx, %rax
.L575:
	movl	%eax, %r8d
	movl	$-1119, %edx
	movl	%ecx, 0(%r13)
	subl	%esi, %edx
	subl	%esi, %r8d
	addl	%eax, %edx
	cmpl	%esi, %eax
	movl	%r8d, %esi
	cmovb	%edx, %esi
	incq	%r11
	xorl	%ecx, 124(%rsp)
	cmpq	$3000000, %r11
	jne	.L578
	movq	32(%rsp), %r14
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	subq	%r14, %rax
	js	.L579
	vcvtsi2sdq	%rax, %xmm7, %xmm0
.L580:
	vdivsd	%xmm6, %xmm0, %xmm0
	decl	40(%rsp)
	movl	124(%rsp), %eax
	vminsd	%xmm8, %xmm0, %xmm8
	jne	.L581
	movq	72(%rsp), %rdx
	vmovapd	%xmm8, %xmm2
	leaq	.LC2(%rip), %rcx
	vmovq	%xmm8, %r8
	xorl	%r14d, %r14d
	movl	$560815139, %r13d
	movl	$1960037684, %r12d
	movabsq	$4294968415, %rbp
	call	__mingw_printf
	vmovsd	.LC0(%rip), %xmm8
	movl	$3, 40(%rsp)
	.p2align 4
	.p2align 3
.L616:
	movl	$0, 120(%rsp)
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	movl	$4294966177, %ebx
	xorl	%r8d, %r8d
	movl	$4294966176, %esi
	movq	%rax, 32(%rsp)
	.p2align 4
	.p2align 3
.L613:
	movzbl	%r8b, %eax
	leaq	160(%rsp,%rax,4), %r10
	testb	%r14b, %r14b
	jne	.L714
	cmpl	$1960037684, %r12d
	je	.L771
	movl	$1960037684, %eax
	movl	$1960036565, %ecx
	movl	$560814020, %r11d
	movl	$1, %edi
	subl	%r12d, %eax
	subl	%r12d, %ecx
	cmpl	$1960037684, %r12d
	cmovbe	%eax, %ecx
	movl	$560815139, %eax
	subl	%r13d, %r11d
	subl	%r13d, %eax
	cmpl	$560815139, %r13d
	cmovbe	%rax, %r11
	xorl	%r9d, %r9d
	movq	%rbx, %rax
	jmp	.L598
	.p2align 5
	.p2align 4
	.p2align 3
.L721:
	movq	%r15, %rdi
.L598:
	cqto
	idivq	%rcx
	imulq	%rdi, %rax
	subq	%rax, %r9
	movq	%rcx, %rax
	movq	%rdx, %rcx
	movq	%r9, %r15
	movq	%rdi, %r9
	testq	%rdx, %rdx
	jne	.L721
	cmpq	$1, %rax
	jg	.L772
	movl	$4294966177, %ecx
	testq	%rdi, %rdi
	leaq	(%rdi,%rcx), %rax
	cmovs	%rax, %rdi
	movl	%edi, %edi
	imulq	%r11, %rdi
	movq	%rdi, %rax
	mulq	%rbp
	imulq	%rcx, %rdx
	subq	%rdx, %rdi
	movl	$4294966176, %edx
	movq	%rdi, %rax
	cmpq	%rdi, %rdx
	jnb	.L603
	subq	%rcx, %rax
	movabsq	$-8589932354, %rcx
	addq	%rcx, %rdi
	cmpq	%rax, %rdx
	cmovb	%rdi, %rax
.L603:
	movl	%eax, %ecx
	movl	$4294966177, %r11d
	movq	%rcx, %r9
	imulq	%rcx, %r9
	movq	%r9, %rax
	mulq	%rbp
	movq	%rdx, %rax
	movq	%r9, %rdx
	imulq	%r11, %rax
	subq	%rax, %rdx
	movl	$4294966176, %eax
	cmpq	%rdx, %rax
	jnb	.L605
	movq	%rdx, %r9
	movabsq	$-8589932354, %rdi
	subq	%r11, %r9
	addq	%rdi, %rdx
	cmpq	%r9, %rax
	cmovnb	%r9d, %edx
.L605:
	cmpl	%r12d, %edx
	jb	.L601
	subl	%r12d, %edx
.L607:
	leal	-1960038803(%rdx), %eax
	cmpl	$1960037684, %edx
	leal	-1960037684(%rdx), %edx
	cmovb	%eax, %edx
	cmpl	%edx, %r12d
	jb	.L600
	movl	%r12d, %eax
	movl	%edx, %r12d
	subl	%edx, %eax
.L610:
	imulq	%rax, %rcx
	movq	%rcx, %rax
	mulq	%rbp
	movq	%rcx, %rax
	imulq	%rbx, %rdx
	subq	%rdx, %rax
	cmpq	%rax, %rsi
	jnb	.L611
	movq	%rax, %rdx
	movabsq	$-8589932354, %rdi
	subq	%rbx, %rdx
	addq	%rdi, %rax
	cmpq	%rdx, %rsi
	cmovnb	%rdx, %rax
.L611:
	movl	$-1119, %edx
	movl	%eax, %ecx
	subl	%r13d, %edx
	subl	%r13d, %ecx
	addl	%eax, %edx
	cmpl	%r13d, %eax
	cmovb	%edx, %ecx
	movl	%ecx, %r13d
.L582:
	incq	%r8
	xorl	%r12d, 120(%rsp)
	movl	%r12d, (%r10)
	cmpq	$3000000, %r8
	jne	.L613
	movq	32(%rsp), %r15
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	subq	%r15, %rax
	js	.L614
	vcvtsi2sdq	%rax, %xmm7, %xmm0
.L615:
	vdivsd	%xmm6, %xmm0, %xmm0
	decl	40(%rsp)
	movl	120(%rsp), %eax
	vminsd	%xmm8, %xmm0, %xmm8
	jne	.L616
	movq	72(%rsp), %rdx
	vmovapd	%xmm8, %xmm2
	leaq	.LC3(%rip), %rcx
	vmovq	%xmm8, %r8
	movl	$1960037684, %ebp
	movl	$560815139, %ebx
	movabsq	$4294968415, %r12
	movl	$4294966177, %edi
	movl	$4294966176, %esi
	movl	%ebp, %r13d
	call	__mingw_printf
	vmovsd	.LC0(%rip), %xmm8
	movl	$3, 32(%rsp)
	.p2align 4
	.p2align 3
.L646:
	movl	$0, 116(%rsp)
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	movabsq	$-8589932354, %r15
	xorl	%r9d, %r9d
	movq	%rax, %rbp
	movl	$-1119, %r14d
	movl	%ebx, %r8d
	jmp	.L641
	.p2align 4
	.p2align 3
.L620:
	movq	%rax, %r8
	subq	%rdi, %r8
	cmpq	%r8, %rsi
	jb	.L622
	movl	%r8d, %edx
	movq	%r8, %rax
.L621:
	movl	%eax, %eax
	addl	%edx, %edx
	movl	%r13d, %r13d
	leal	(%rbx,%rbx), %r8d
	addq	%rax, %rax
	leal	1119(%rdx), %r11d
	cmpq	%rax, %rsi
	leal	1119(%r8), %eax
	cmovnb	%edx, %r11d
	leaq	(%r13,%r13), %rdx
	cmpq	%rdx, %rsi
	cmovb	%eax, %r8d
	movl	%r8d, %eax
	leal	(%r8,%rbx), %edx
	leal	1119(%r8,%rbx), %r8d
	leal	(%r11,%r11), %ebx
	addq	%r13, %rax
	cmpq	%rax, %rsi
	movl	%r11d, %eax
	cmovnb	%edx, %r8d
	addq	%rax, %rax
	leal	1119(%rbx), %edx
	cmpq	%rax, %rsi
	movq	%r8, %r13
	cmovb	%edx, %ebx
	imulq	%r8, %r13
	movq	%r13, %rax
	mulq	%r12
	movq	%r13, %rax
	imulq	%rdi, %rdx
	subq	%rdx, %rax
	cmpq	%rax, %rsi
	jnb	.L629
	movq	%rax, %rdx
	addq	%r15, %rax
	subq	%rdi, %rdx
	cmpq	%rdx, %rsi
	cmovnb	%rdx, %rax
.L629:
	movl	%r14d, %edx
	movl	%eax, %r13d
	subl	%ebx, %edx
	subl	%ebx, %r13d
	addl	%eax, %edx
	cmpl	%ebx, %eax
	cmovb	%edx, %r13d
	imulq	%rcx, %rcx
	movq	%rcx, %rax
	mulq	%r12
	imulq	%rdi, %rdx
	subq	%rdx, %rcx
	cmpq	%rcx, %rsi
	jnb	.L632
	movq	%rcx, %rax
	addq	%r15, %rcx
	subq	%rdi, %rax
	cmpq	%rax, %rsi
	cmovnb	%rax, %rcx
.L632:
	leal	(%rcx,%rcx), %edx
	movl	%ecx, %ecx
	addq	%rcx, %rcx
	leal	1119(%rdx), %eax
	cmpq	%rcx, %rsi
	cmovb	%rax, %rdx
	leal	(%rdx,%rdx), %eax
	addq	%rdx, %rdx
	cmpq	%rdx, %rsi
	leal	1119(%rax), %ecx
	cmovb	%rcx, %rax
	leal	(%rax,%rax), %ecx
	addq	%rax, %rax
	cmpq	%rax, %rsi
	leal	1119(%rcx), %edx
	movl	%r11d, %eax
	cmovb	%edx, %ecx
	leal	-1119(%r11), %edx
	subl	%r13d, %eax
	subl	%r13d, %edx
	cmpl	%r13d, %r11d
	cmovb	%edx, %eax
	imulq	%rax, %r8
	movq	%r8, %rax
	mulq	%r12
	movq	%r8, %rax
	imulq	%rdi, %rdx
	subq	%rdx, %rax
	cmpq	%rax, %rsi
	jnb	.L638
	movq	%rax, %rdx
	addq	%r15, %rax
	subq	%rdi, %rdx
	cmpq	%rdx, %rsi
	cmovnb	%rdx, %rax
.L638:
	movl	%r14d, %edx
	movl	%eax, %r8d
	movl	%r13d, (%r10)
	subl	%ecx, %edx
	subl	%ecx, %r8d
	addl	%eax, %edx
	cmpl	%ecx, %eax
	cmovb	%rdx, %r8
	incq	%r9
	xorl	%r13d, 116(%rsp)
	cmpq	$3000000, %r9
	je	.L773
.L641:
	movl	%r13d, %r11d
	movzbl	%r9b, %eax
	movq	%r11, %r13
	leaq	160(%rsp,%rax,4), %r10
	imulq	%r11, %r13
	movq	%r13, %rax
	mulq	%r12
	imulq	%rdi, %rdx
	subq	%rdx, %r13
	cmpq	%r13, %rsi
	jnb	.L617
	movq	%r13, %rax
	addq	%r15, %r13
	subq	%rdi, %rax
	cmpq	%rax, %rsi
	cmovnb	%rax, %r13
.L617:
	imulq	%r8, %r8
	movl	%r13d, %ebx
	movq	%r8, %rax
	mulq	%r12
	imulq	%rdi, %rdx
	subq	%rdx, %r8
	cmpq	%r8, %rsi
	jnb	.L618
	movq	%r8, %rax
	addq	%r15, %r8
	subq	%rdi, %rax
	cmpq	%rax, %rsi
	cmovnb	%rax, %r8
.L618:
	movl	%r8d, %ecx
	addl	%r8d, %r8d
	leaq	(%rcx,%rcx), %rdx
	leal	1119(%r8), %eax
	cmpq	%rdx, %rsi
	cmovnb	%r8d, %eax
	imulq	%r11, %rax
	movq	%rax, %r8
	mulq	%r12
	movq	%r8, %rax
	imulq	%rdi, %rdx
	subq	%rdx, %rax
	cmpq	%rax, %rsi
	jb	.L620
	movl	%eax, %edx
	jmp	.L621
	.p2align 4
	.p2align 3
.L714:
	xorl	%r14d, %r14d
	movl	$560815139, %r13d
	movl	$1960037684, %r12d
	jmp	.L582
	.p2align 4
	.p2align 3
.L769:
	addq	%r10, %r10
	leal	(%rbp,%rbp), %ecx
	cmpq	%r10, %rbx
	jb	.L565
	xorl	%r8d, %r8d
	testl	%ecx, %ecx
	jne	.L765
.L561:
	movl	%ebp, %eax
	movl	%ecx, %ebp
	subl	%ecx, %eax
	jmp	.L574
	.p2align 4
	.p2align 3
.L565:
	addl	$1119, %ecx
	xorl	%r8d, %r8d
.L765:
	xorl	%eax, %eax
.L562:
	movl	$-1119, %edx
	subl	%ecx, %edx
	leal	(%rdx,%rax), %ecx
	jmp	.L572
	.p2align 4
	.p2align 3
.L622:
	addq	%r15, %rax
	movl	%eax, %edx
	jmp	.L621
	.p2align 4
	.p2align 3
.L773:
	movl	%r8d, %ebx
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	subq	%rbp, %rax
	js	.L642
	vcvtsi2sdq	%rax, %xmm7, %xmm0
.L643:
	vdivsd	%xmm6, %xmm0, %xmm0
	decl	32(%rsp)
	movl	116(%rsp), %eax
	vminsd	%xmm8, %xmm0, %xmm2
	vmovapd	%xmm2, %xmm8
	jne	.L646
	movq	72(%rsp), %rdx
	leaq	.LC4(%rip), %rcx
	vmovq	%xmm2, %r8
	xorl	%esi, %esi
	movl	$1960037684, %r12d
	movabsq	$4294968415, %r13
	movl	$560815139, %ebx
	movl	$1, %r15d
	call	__mingw_printf
	vmovsd	.LC0(%rip), %xmm8
	movl	$3, 68(%rsp)
	.p2align 4
	.p2align 3
.L701:
	movl	$0, 112(%rsp)
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	movl	$4294966177, %r14d
	xorl	%r9d, %r9d
	movl	$4294966176, %ecx
	movl	%esi, %ebp
	movq	%rax, 56(%rsp)
	jmp	.L698
	.p2align 4
	.p2align 3
.L776:
	movl	%r15d, %r8d
	movq	%r8, 32(%rsp)
	imulq	%r8, %r8
	movq	%r8, %rax
	mulq	%r13
	imulq	%r14, %rdx
	subq	%rdx, %r8
	cmpq	%r8, %rcx
	jnb	.L648
	movq	%r8, %rax
	movabsq	$-8589932354, %rdi
	subq	%r14, %rax
	addq	%rdi, %r8
	cmpq	%rax, %rcx
	cmovnb	%rax, %r8
.L648:
	movl	%r8d, %r8d
	imulq	$1960037684, %r8, %r10
	movq	%r10, %rax
	mulq	%r13
	imulq	%r14, %rdx
	subq	%rdx, %r10
	cmpq	%r10, %rcx
	jnb	.L649
	movq	%r10, %rax
	movabsq	$-8589932354, %rdi
	subq	%r14, %rax
	addq	%rdi, %r10
	cmpq	%rax, %rcx
	cmovnb	%rax, %r10
.L649:
	imulq	32(%rsp), %r8
	movq	%r8, %rax
	mulq	%r13
	movq	%r8, %rax
	imulq	%r14, %rdx
	subq	%rdx, %rax
	cmpq	%rax, %rcx
	jnb	.L650
	movq	%rax, %rdx
	movabsq	$-8589932354, %rdi
	subq	%r14, %rdx
	addq	%rdi, %rax
	cmpq	%rdx, %rcx
	cmovnb	%rdx, %rax
.L650:
	movl	%eax, %eax
	imulq	$560815139, %rax, %r8
	movq	%r8, %rax
	mulq	%r13
	movq	%r8, %rax
	imulq	%r14, %rdx
	subq	%rdx, %rax
	cmpq	%rax, %rcx
	jnb	.L651
	movq	%rax, %rdx
	movabsq	$-8589932354, %rdi
	subq	%r14, %rdx
	addq	%rdi, %rax
	cmpq	%rdx, %rcx
	cmovnb	%rdx, %rax
.L651:
	cmpl	%r12d, %r10d
	je	.L774
	movl	$-1119, %r8d
	movl	%r10d, %edx
	movl	$-1119, %esi
	subl	%r12d, %r8d
	subl	%r12d, %edx
	addl	%r10d, %r8d
	cmpl	%r12d, %r10d
	cmovnb	%edx, %r8d
	movl	%eax, %edx
	subl	%ebx, %esi
	subl	%ebx, %edx
	addl	%eax, %esi
	movq	%r8, %rdi
	cmpl	%ebx, %eax
	cmovnb	%edx, %esi
	imulq	%r8, %rdi
	movq	%rdi, %rax
	mulq	%r13
	imulq	%r14, %rdx
	subq	%rdx, %rdi
	cmpq	%rdi, %rcx
	jnb	.L682
	movq	%rdi, %rax
	movabsq	$-8589932354, %r10
	subq	%r14, %rax
	addq	%r10, %rdi
	cmpq	%rax, %rcx
	cmovnb	%rax, %rdi
.L682:
	movl	%edi, %edi
	movq	%r8, %r10
	imulq	%rdi, %r10
	movq	%r10, %rax
	mulq	%r13
	imulq	%r14, %rdx
	subq	%rdx, %r10
	cmpq	%r10, %rcx
	jnb	.L683
	movq	%r10, %rax
	movabsq	$-8589932354, %r15
	subq	%r14, %rax
	addq	%r15, %r10
	cmpq	%rax, %rcx
	cmovnb	%rax, %r10
.L683:
	imulq	%rdi, %r12
	movl	%r10d, 40(%rsp)
	movq	%r12, %rax
	mulq	%r13
	movq	%r12, %rax
	imulq	%r14, %rdx
	subq	%rdx, %rax
	cmpq	%rax, %rcx
	jnb	.L684
	movq	%rax, %rdx
	movabsq	$-8589932354, %r15
	subq	%r14, %rdx
	addq	%r15, %rax
	cmpq	%rdx, %rcx
	cmovnb	%rdx, %rax
.L684:
	leal	(%rax,%rax), %r15d
	movl	%eax, %edi
	movl	%eax, %eax
	addq	%rax, %rax
	leal	1119(%r15), %edx
	cmpq	%rax, %rcx
	movl	%esi, %eax
	movq	%rax, %r12
	cmovb	%edx, %r15d
	movq	%rax, 40(%rsp)
	imulq	%rax, %r12
	movq	%r12, %rax
	mulq	%r13
	movq	%r12, %rax
	imulq	%r14, %rdx
	subq	%rdx, %rax
	cmpq	%rax, %rcx
	jnb	.L686
	movq	%rax, %rdx
	movabsq	$-8589932354, %rsi
	subq	%r14, %rdx
	addq	%rsi, %rax
	cmpq	%rdx, %rcx
	cmovnb	%rdx, %rax
.L686:
	movl	%eax, %r12d
	subl	%r10d, %r12d
	movl	%r12d, 48(%rsp)
	movl	$-1119, %r12d
	subl	%r10d, %r12d
	cmpl	%r10d, %eax
	movl	%r10d, %r10d
	leal	(%r12,%rax), %edx
	cmovnb	48(%rsp), %edx
	movl	$-1119, %r12d
	subl	%r15d, %r12d
	movl	%edx, %eax
	addl	%edx, %r12d
	subl	%r15d, %eax
	cmpl	%r15d, %edx
	cmovnb	%rax, %r12
	imulq	%rbx, %r10
	movq	%r10, %rax
	mulq	%r13
	movq	%r10, %rax
	imulq	%r14, %rdx
	subq	%rdx, %rax
	cmpq	%rax, %rcx
	jnb	.L691
	movq	%rax, %rdx
	movabsq	$-8589932354, %rbx
	subq	%r14, %rdx
	addq	%rbx, %rax
	cmpq	%rdx, %rcx
	cmovnb	%rdx, %rax
.L691:
	movl	%eax, %r10d
	movl	%edi, %edx
	leal	-1119(%rdi), %eax
	subl	%r12d, %edx
	subl	%r12d, %eax
	cmpl	%r12d, %edi
	cmovnb	%edx, %eax
	imulq	40(%rsp), %rax
	movq	%rax, %rbx
	mulq	%r13
	movq	%rbx, %rax
	imulq	%r14, %rdx
	subq	%rdx, %rax
	cmpq	%rax, %rcx
	jnb	.L694
	movq	%rax, %rdx
	movabsq	$-8589932354, %rdi
	subq	%r14, %rdx
	addq	%rdi, %rax
	cmpq	%rdx, %rcx
	cmovnb	%rdx, %rax
.L694:
	movq	32(%rsp), %r15
	movl	$-1119, %ebx
	movl	%eax, %edx
	subl	%r10d, %ebx
	subl	%r10d, %edx
	addl	%eax, %ebx
	cmpl	%r10d, %eax
	cmovnb	%rdx, %rbx
	imulq	%r8, %r15
	movq	%r15, %rax
	mulq	%r13
	imulq	%r14, %rdx
	subq	%rdx, %r15
	cmpq	%r15, %rcx
	jnb	.L647
	movq	%r15, %rax
	movabsq	$-8589932354, %rdi
	subq	%r14, %rax
	addq	%rdi, %r15
	cmpq	%rax, %rcx
	cmovnb	%rax, %r15
	.p2align 4
	.p2align 3
.L647:
	incq	%r9
	xorl	%r12d, 112(%rsp)
	movl	%r12d, (%r11)
	cmpq	$3000000, %r9
	je	.L775
.L698:
	movzbl	%r9b, %eax
	leaq	160(%rsp,%rax,4), %r11
	testb	%bpl, %bpl
	je	.L776
	xorl	%ebp, %ebp
	movl	$1, %r15d
	movl	$560815139, %ebx
	movl	$1960037684, %r12d
	jmp	.L647
	.p2align 4
	.p2align 3
.L775:
	movq	56(%rsp), %rdi
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	movl	%ebp, %esi
	subq	%rdi, %rax
	js	.L699
	vcvtsi2sdq	%rax, %xmm7, %xmm0
.L700:
	vdivsd	%xmm6, %xmm0, %xmm0
	decl	68(%rsp)
	movl	112(%rsp), %eax
	vminsd	%xmm8, %xmm0, %xmm8
	jne	.L701
	movq	72(%rsp), %rdx
	vmovapd	%xmm8, %xmm2
	leaq	.LC5(%rip), %rcx
	vmovq	%xmm8, %r8
	movl	$3, %edi
	movl	$1960037684, %esi
	call	__mingw_printf
	vmovsd	.LC0(%rip), %xmm8
	movabsq	$4855782435, %rax
	movb	$0, 140(%rsp)
	movq	%rax, 132(%rsp)
	movabsq	$-461202339323874386, %rax
	movq	$1121630278, 152(%rsp)
	movq	%rax, 144(%rsp)
	.p2align 4
	.p2align 3
.L707:
	movl	$0, 108(%rsp)
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	xorl	%ebx, %ebx
	movq	%rax, %rbp
	.p2align 4
	.p2align 3
.L702:
	leaq	128(%rsp), %rdx
	leaq	144(%rsp), %r8
	leaq	80(%rsp), %rcx
	movl	%esi, 128(%rsp)
	call	_ZN2ec8JacobianIN2fp9FpBarrettILj4294966177EEEE3addERKS4_S6_
	movq	88(%rsp), %rdx
	movq	80(%rsp), %rax
	xorl	%eax, 108(%rsp)
	movq	%rdx, 136(%rsp)
	movzbl	%bl, %edx
	incq	%rbx
	movq	%rax, 128(%rsp)
	movl	%eax, %esi
	movl	%eax, 160(%rsp,%rdx,4)
	cmpq	$3000000, %rbx
	jne	.L702
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	subq	%rbp, %rax
	js	.L703
	vcvtsi2sdq	%rax, %xmm7, %xmm0
.L704:
	vdivsd	%xmm6, %xmm0, %xmm0
	decl	%edi
	movl	108(%rsp), %eax
	vminsd	%xmm8, %xmm0, %xmm2
	vmovapd	%xmm2, %xmm8
	jne	.L707
	vmovaps	1184(%rsp), %xmm6
	vmovaps	1200(%rsp), %xmm7
	leaq	.LC6(%rip), %rcx
	vmovq	%xmm2, %r8
	vmovaps	1216(%rsp), %xmm8
	movq	72(%rsp), %rdx
	addq	$1240, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	jmp	__mingw_printf
	.p2align 4
	.p2align 3
.L774:
	cmpl	%eax, %ebx
	je	.L777
	xorl	%r15d, %r15d
	xorl	%ebx, %ebx
	xorl	%r12d, %r12d
	movl	$1, %ebp
	jmp	.L647
	.p2align 4
	.p2align 3
.L771:
	cmpl	$560815139, %r13d
	je	.L778
	xorl	%r13d, %r13d
	xorl	%r12d, %r12d
	movl	$1, %r14d
	jmp	.L582
	.p2align 4
	.p2align 3
.L772:
	xorl	%edx, %edx
	testl	%r12d, %r12d
	jne	.L601
	xorl	%ecx, %ecx
	movl	$-1960038803, %edx
.L600:
	leal	-1119(%r12), %eax
	movl	%edx, %r12d
	subl	%edx, %eax
	jmp	.L610
	.p2align 4
	.p2align 3
.L601:
	subl	%r12d, %edx
	subl	$1119, %edx
	jmp	.L607
	.p2align 4
	.p2align 3
.L768:
	addq	%r10, %r10
	leal	(%rbp,%rbp), %ecx
	cmpq	%r10, %rbx
	jb	.L560
	xorl	%r8d, %r8d
	testl	%ecx, %ecx
	jne	.L562
	movl	%ebp, %eax
	movl	%ecx, %ebp
	subl	%ecx, %eax
	jmp	.L574
	.p2align 4
	.p2align 3
.L699:
	movq	%rax, %rdx
	andl	$1, %eax
	shrq	%rdx
	orq	%rax, %rdx
	vcvtsi2sdq	%rdx, %xmm7, %xmm0
	vaddsd	%xmm0, %xmm0, %xmm0
	jmp	.L700
	.p2align 4
	.p2align 3
.L703:
	movq	%rax, %rdx
	andl	$1, %eax
	shrq	%rdx
	orq	%rax, %rdx
	vcvtsi2sdq	%rdx, %xmm7, %xmm0
	vaddsd	%xmm0, %xmm0, %xmm0
	jmp	.L704
	.p2align 4
	.p2align 3
.L642:
	movq	%rax, %rdx
	andl	$1, %eax
	shrq	%rdx
	orq	%rax, %rdx
	vcvtsi2sdq	%rdx, %xmm7, %xmm0
	vaddsd	%xmm0, %xmm0, %xmm0
	jmp	.L643
	.p2align 4
	.p2align 3
.L614:
	movq	%rax, %rdx
	andl	$1, %eax
	shrq	%rdx
	orq	%rax, %rdx
	vcvtsi2sdq	%rdx, %xmm7, %xmm0
	vaddsd	%xmm0, %xmm0, %xmm0
	jmp	.L615
	.p2align 4
	.p2align 3
.L579:
	movq	%rax, %rdx
	andl	$1, %eax
	shrq	%rdx
	orq	%rax, %rdx
	vcvtsi2sdq	%rdx, %xmm7, %xmm0
	vaddsd	%xmm0, %xmm0, %xmm0
	jmp	.L580
.L770:
	movq	%r14, %rcx
	movq	%r14, %r8
	imulq	%r14, %rcx
	movq	%rcx, %rax
	mulq	%rdi
	movq	%rcx, %rax
	imulq	%r12, %rdx
	subq	%rdx, %rax
	jmp	.L568
.L778:
	xorl	%r9d, %r9d
	movl	$1, %r11d
	movl	$1121630278, %ecx
	movl	$4294966177, %eax
	jmp	.L584
	.p2align 5
	.p2align 4
	.p2align 3
.L716:
	movq	%rdi, %r11
.L584:
	cqto
	movq	%r9, %rdi
	movq	%r11, %r9
	idivq	%rcx
	imulq	%r11, %rax
	subq	%rax, %rdi
	movq	%rcx, %rax
	movq	%rdx, %rcx
	testq	%rdx, %rdx
	jne	.L716
	cmpq	$1, %rax
	jg	.L717
	movl	$4294966177, %r9d
	testq	%r11, %r11
	leaq	(%r11,%r9), %rax
	cmovs	%rax, %r11
	movl	%r11d, %eax
	imulq	$989511900, %rax, %rcx
	movabsq	$4294968415, %rax
	mulq	%rcx
	movq	%rcx, %rax
	imulq	%r9, %rdx
	subq	%rdx, %rax
	movl	$4294966176, %edx
	movq	%rax, %rcx
	cmpq	%rax, %rdx
	jnb	.L587
	subq	%r9, %rcx
	movabsq	$-8589932354, %r9
	addq	%r9, %rax
	cmpq	%rcx, %rdx
	cmovb	%rax, %rcx
.L587:
	movl	%ecx, %ecx
	movabsq	$4294968415, %rax
	movl	$4294966177, %r11d
	movl	$4294966176, %edi
	movq	%rcx, %r9
	imulq	%rcx, %r9
	mulq	%r9
	imulq	%r11, %rdx
	subq	%rdx, %r9
	movq	%r9, %rax
	cmpq	%r9, %rdi
	jnb	.L588
	subq	%r11, %rax
	movabsq	$-8589932354, %rdx
	addq	%r9, %rdx
	cmpq	%rax, %rdi
	cmovb	%rdx, %rax
.L588:
	leal	374891928(%rax), %r12d
	cmpl	$-374891929, %eax
	jbe	.L779
.L590:
	movl	$1960037684, %eax
	subl	%r12d, %eax
.L592:
	imulq	%rax, %rcx
	movabsq	$4294968415, %rax
	movl	$4294966177, %r9d
	mulq	%rcx
	movq	%rcx, %rax
	movl	$4294966176, %ecx
	imulq	%r9, %rdx
	subq	%rdx, %rax
	movq	%rax, %r13
	cmpq	%rax, %rcx
	jnb	.L585
	subq	%r9, %r13
	movabsq	$-8589932354, %rdx
	addq	%rdx, %rax
	cmpq	%r13, %rcx
	cmovb	%rax, %r13
.L585:
	cmpl	$560815138, %r13d
	jbe	.L593
	subl	$560815139, %r13d
	jmp	.L582
.L560:
	addl	$1119, %ecx
	movl	$-1119, %edx
	xorl	%r8d, %r8d
	subl	%ecx, %edx
	leal	(%rdx,%rax), %ecx
	jmp	.L572
.L777:
	movl	%r10d, %edi
	movabsq	$4294968415, %rax
	movq	%rdi, %r8
	imulq	%rdi, %r8
	mulq	%r8
	movl	$4294966177, %eax
	movq	%r8, %rsi
	imulq	%rax, %rdx
	subq	%rdx, %rsi
	movl	$4294966176, %edx
	cmpq	%rsi, %rdx
	jnb	.L653
	movq	%rsi, %r8
	subq	%rax, %r8
	cmpq	%r8, %rdx
	jnb	.L736
	movabsq	$-8589932354, %rax
	addq	%rax, %rsi
.L653:
	movl	%ebx, %r8d
	movabsq	$4294968415, %rax
	movl	$4294966177, %r10d
	movl	%esi, %r12d
	movq	%r8, 40(%rsp)
	imulq	%r8, %r8
	mulq	%r8
	movq	%r8, %rax
	imulq	%r10, %rdx
	subq	%rdx, %rax
	movl	$4294966176, %edx
	cmpq	%rax, %rdx
	jnb	.L654
	movq	%rax, %r8
	subq	%r10, %r8
	cmpq	%r8, %rdx
	jnb	.L737
	movabsq	$-8589932354, %rdx
	addq	%rdx, %rax
.L654:
	leal	(%rax,%rax), %r8d
	cmpl	$2147483088, %eax
	movl	%eax, %ebx
	movabsq	$4294968415, %rax
	leal	1119(%r8), %edx
	movl	$4294966176, %r10d
	movq	%rbx, 48(%rsp)
	cmova	%edx, %r8d
	imulq	%rdi, %r8
	mulq	%r8
	movl	$4294966177, %eax
	imulq	%rax, %rdx
	subq	%rdx, %r8
	movl	%r8d, %edx
	cmpq	%r8, %r10
	jnb	.L658
	movq	%r8, %rbx
	subq	%rax, %rbx
	cmpq	%rbx, %r10
	jnb	.L657
	movabsq	$-8589932354, %rax
	addq	%rax, %r8
	movl	%r8d, %edx
.L658:
	addl	%edx, %edx
	cmpl	$2147483088, %r8d
	movl	$4294966176, %r10d
	leal	1119(%rdx), %eax
	cmovbe	%edx, %eax
	cmpl	$2147483088, %esi
	movl	%esi, %edx
	movl	%eax, %edi
	leal	(%r12,%r12), %eax
	leal	1119(%rax), %r8d
	leal	(%rdi,%rdi), %ebx
	cmova	%r8d, %eax
	movl	%eax, %r8d
	addq	%r8, %rdx
	leal	1119(%r12,%rax), %r8d
	addl	%r12d, %eax
	cmpq	%rdx, %r10
	movl	%edi, %edx
	cmovb	%r8d, %eax
	addq	%rdx, %rdx
	leal	1119(%rbx), %r8d
	cmpq	%rdx, %r10
	movl	%eax, %esi
	movabsq	$4294968415, %rax
	cmovb	%r8d, %ebx
	movq	%rsi, %r8
	imulq	%rsi, %r8
	mulq	%r8
	movl	$4294966177, %eax
	imulq	%rax, %rdx
	subq	%rdx, %r8
	cmpq	%r8, %r10
	jnb	.L665
	movq	%r8, %rdx
	subq	%rax, %rdx
	cmpq	%rdx, %r10
	jnb	.L738
	movabsq	$-8589932354, %rax
	addq	%rax, %r8
.L665:
	movl	%r8d, %eax
	subl	%ebx, %eax
	cmpl	%ebx, %r8d
	movl	$4294966176, %r8d
	leal	-1119(%rax), %r12d
	cmovnb	%rax, %r12
	cmpq	$2147483088, 32(%rsp)
	leal	(%r15,%r15), %eax
	leal	1119(%rax), %r15d
	cmovbe	%eax, %r15d
	imulq	40(%rsp), %r15
	movabsq	$4294968415, %rax
	mulq	%r15
	movl	$4294966177, %eax
	imulq	%rax, %rdx
	subq	%rdx, %r15
	cmpq	%r15, %r8
	jnb	.L669
	movq	%r15, %rdx
	subq	%rax, %rdx
	cmpq	%rdx, %r8
	jnb	.L739
	movabsq	$-8589932354, %rax
	addq	%rax, %r15
.L669:
	movq	48(%rsp), %r8
	movabsq	$4294968415, %rax
	imulq	%r8, %r8
	mulq	%r8
	movl	$4294966177, %eax
	imulq	%rax, %rdx
	subq	%rdx, %r8
	movl	$4294966176, %edx
	cmpq	%r8, %rdx
	jnb	.L670
	movq	%r8, %r10
	subq	%rax, %r10
	cmpq	%r10, %rdx
	jnb	.L740
	movabsq	$-8589932354, %rax
	addq	%rax, %r8
.L670:
	leal	(%r8,%r8), %edx
	cmpl	$2147483088, %r8d
	leal	-1119(%rdi), %ebx
	movl	$4294966176, %r10d
	leal	1119(%rdx), %eax
	cmova	%eax, %edx
	leal	(%rdx,%rdx), %eax
	cmpl	$2147483088, %edx
	leal	1119(%rax), %r8d
	cmova	%r8d, %eax
	leal	(%rax,%rax), %r8d
	cmpl	$2147483088, %eax
	movl	%edi, %eax
	leal	1119(%r8), %edx
	cmova	%edx, %r8d
	subl	%r12d, %eax
	subl	%r12d, %ebx
	cmpl	%r12d, %edi
	cmovnb	%eax, %ebx
	movabsq	$4294968415, %rax
	imulq	%rsi, %rbx
	mulq	%rbx
	movl	$4294966177, %eax
	imulq	%rax, %rdx
	subq	%rdx, %rbx
	cmpq	%rbx, %r10
	jnb	.L676
	movq	%rbx, %rdx
	subq	%rax, %rdx
	cmpq	%rdx, %r10
	jnb	.L741
	movabsq	$-8589932354, %rax
	addq	%rax, %rbx
.L676:
	movl	%ebx, %eax
	subl	%r8d, %eax
	cmpl	%r8d, %ebx
	leal	-1119(%rax), %edx
	cmovb	%edx, %eax
	movl	%eax, %ebx
	jmp	.L647
.L717:
	movl	$374890809, %r12d
	xorl	%r13d, %r13d
.L593:
	subl	$560816258, %r13d
	jmp	.L582
.L737:
	movq	%r8, %rax
	jmp	.L654
.L740:
	movq	%r10, %r8
	jmp	.L670
.L739:
	movq	%rdx, %r15
	jmp	.L669
.L657:
	movl	%ebx, %edx
	movq	%rbx, %r8
	jmp	.L658
.L741:
	movq	%rdx, %rbx
	jmp	.L676
.L738:
	movq	%rdx, %r8
	jmp	.L665
.L736:
	movq	%r8, %rsi
	jmp	.L653
.L779:
	leal	374890809(%rax), %r12d
	cmpl	$1960037684, %r12d
	jbe	.L590
	movl	$1960036565, %eax
	subl	%r12d, %eax
	jmp	.L592
	.seh_endproc
	.section	.text$_ZN2ec8JacobianIN2fp8FpPseudoILj4294966177EEEE3addERKS4_S6_,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZN2ec8JacobianIN2fp8FpPseudoILj4294966177EEEE3addERKS4_S6_
	.def	_ZN2ec8JacobianIN2fp8FpPseudoILj4294966177EEEE3addERKS4_S6_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN2ec8JacobianIN2fp8FpPseudoILj4294966177EEEE3addERKS4_S6_
_ZN2ec8JacobianIN2fp8FpPseudoILj4294966177EEEE3addERKS4_S6_:
.LFB4905:
	pushq	%r15
	.seh_pushreg	%r15
	pushq	%r14
	.seh_pushreg	%r14
	pushq	%r13
	.seh_pushreg	%r13
	pushq	%r12
	.seh_pushreg	%r12
	pushq	%rbp
	.seh_pushreg	%rbp
	pushq	%rdi
	.seh_pushreg	%rdi
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	.seh_endprologue
	cmpb	$0, 12(%rdx)
	movq	%rcx, %rax
	je	.L781
	vmovdqu	(%r8), %xmm0
	vmovdqu	%xmm0, (%rcx)
.L780:
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	ret
	.p2align 4
	.p2align 3
.L781:
	cmpb	$0, 12(%r8)
	je	.L783
	vmovdqu	(%rdx), %xmm0
	vmovdqu	%xmm0, (%rcx)
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	ret
	.p2align 4
	.p2align 3
.L783:
	movl	8(%rdx), %ecx
	movl	$4294966176, %esi
	movabsq	$-4294966177, %rdi
	movl	(%rdx), %ebx
	movl	4(%rdx), %edx
	movq	%rcx, %r14
	movl	%ecx, %r12d
	movq	%rcx, %rbp
	movq	%rbx, %r13
	imulq	%rcx, %rcx
	movq	%rcx, %r9
	movl	%ecx, %ecx
	shrq	$32, %r9
	imulq	$1119, %r9, %r9
	addq	%rcx, %r9
	movq	%r9, %rcx
	movl	%r9d, %r9d
	shrq	$32, %rcx
	imulq	$1119, %rcx, %rcx
	addq	%r9, %rcx
	cmpq	%rcx, %rsi
	leaq	(%rcx,%rdi), %r9
	cmovb	%r9, %rcx
	movl	8(%r8), %r9d
	movq	%r9, %r10
	imulq	%r9, %r10
	movq	%r10, %r11
	movl	%r10d, %r10d
	shrq	$32, %r11
	imulq	$1119, %r11, %r11
	addq	%r10, %r11
	movq	%r11, %r10
	movl	%r11d, %r11d
	shrq	$32, %r10
	imulq	$1119, %r10, %r10
	addq	%r11, %r10
	cmpq	%r10, %rsi
	leaq	(%r10,%rdi), %r11
	cmovb	%r11, %r10
	imulq	%r10, %rbx
	movq	%rbx, %r11
	movl	%ebx, %ebx
	shrq	$32, %r11
	imulq	$1119, %r11, %r11
	addq	%rbx, %r11
	movq	%r11, %rbx
	movl	%r11d, %r11d
	shrq	$32, %rbx
	imulq	$1119, %rbx, %rbx
	addq	%r11, %rbx
	cmpq	%rbx, %rsi
	leaq	(%rbx,%rdi), %r11
	cmovb	%r11, %rbx
	movl	(%r8), %r11d
	movl	4(%r8), %r8d
	imulq	%rcx, %r11
	movl	%r11d, %r15d
	shrq	$32, %r11
	imulq	$1119, %r11, %r11
	addq	%r15, %r11
	movq	%r11, %r15
	movl	%r11d, %r11d
	shrq	$32, %r15
	imulq	$1119, %r15, %r15
	addq	%r15, %r11
	cmpq	%r11, %rsi
	leaq	(%r11,%rdi), %r15
	cmovb	%r15, %r11
	imulq	%r9, %r10
	movq	%r10, %r15
	movl	%r10d, %r10d
	shrq	$32, %r15
	imulq	$1119, %r15, %r15
	addq	%r10, %r15
	movq	%r15, %r10
	movl	%r15d, %r15d
	shrq	$32, %r10
	imulq	$1119, %r10, %r10
	addq	%r15, %r10
	cmpq	%r10, %rsi
	leaq	(%r10,%rdi), %r15
	cmovb	%r15, %r10
	movq	%rdx, %r15
	imulq	%rdx, %r10
	movq	%r10, %rdx
	movl	%r10d, %r10d
	shrq	$32, %rdx
	imulq	$1119, %rdx, %rdx
	addq	%rdx, %r10
	movq	%r10, %rdx
	movl	%r10d, %r10d
	shrq	$32, %rdx
	imulq	$1119, %rdx, %rdx
	addq	%r10, %rdx
	cmpq	%rdx, %rsi
	leaq	(%rdx,%rdi), %r10
	cmovb	%r10, %rdx
	imulq	%r14, %rcx
	movq	%rcx, %r10
	movl	%ecx, %ecx
	shrq	$32, %r10
	imulq	$1119, %r10, %r10
	addq	%rcx, %r10
	movq	%r10, %rcx
	movl	%r10d, %r10d
	shrq	$32, %rcx
	imulq	$1119, %rcx, %rcx
	addq	%r10, %rcx
	cmpq	%rcx, %rsi
	leaq	(%rcx,%rdi), %r10
	cmovb	%r10, %rcx
	imulq	%r8, %rcx
	movq	%rcx, %r8
	movl	%ecx, %ecx
	shrq	$32, %r8
	imulq	$1119, %r8, %r8
	addq	%rcx, %r8
	movq	%r8, %rcx
	movl	%r8d, %r8d
	shrq	$32, %rcx
	imulq	$1119, %rcx, %rcx
	addq	%rcx, %r8
	leaq	(%r8,%rdi), %rcx
	cmpq	%r8, %rsi
	cmovb	%rcx, %r8
	cmpl	%ebx, %r11d
	je	.L842
	movl	$-1119, %ecx
	movl	%r11d, %r14d
	movl	%ecx, %r10d
	subl	%ebx, %r14d
	subl	%ebx, %r10d
	addl	%r11d, %r10d
	cmpl	%ebx, %r11d
	movl	%r8d, %r11d
	cmovnb	%r14d, %r10d
	subl	%edx, %ecx
	subl	%edx, %r11d
	addl	%r8d, %ecx
	cmpl	%edx, %r8d
	movq	%r10, %r8
	cmovb	%ecx, %r11d
	imulq	%r10, %r8
	movq	%r10, %rcx
	movl	%r11d, %r15d
	movq	%r8, %r11
	movl	%r8d, %r8d
	shrq	$32, %r11
	imulq	$1119, %r11, %r11
	addq	%r8, %r11
	movq	%r11, %r8
	movl	%r11d, %r11d
	shrq	$32, %r8
	imulq	$1119, %r8, %r8
	addq	%r11, %r8
	cmpq	%r8, %rsi
	leaq	(%r8,%rdi), %r11
	cmovb	%r11, %r8
	imulq	%r8, %rcx
	movq	%rcx, %r11
	movl	%ecx, %ecx
	shrq	$32, %r11
	imulq	$1119, %r11, %r11
	addq	%rcx, %r11
	movq	%r11, %rcx
	movl	%r11d, %r11d
	shrq	$32, %rcx
	imulq	$1119, %rcx, %rcx
	addq	%rcx, %r11
	cmpq	%r11, %rsi
	leaq	(%r11,%rdi), %rcx
	cmovb	%rcx, %r11
	imulq	%r8, %rbx
	movl	%r11d, %r14d
	movq	%rbx, %r8
	movl	%ebx, %ebx
	shrq	$32, %r8
	imulq	$1119, %r8, %r8
	addq	%rbx, %r8
	movq	%r8, %rbx
	movl	%r8d, %r8d
	shrq	$32, %rbx
	imulq	$1119, %rbx, %rbx
	addq	%rbx, %r8
	leal	(%r8,%rdi), %r12d
	cmpq	%r8, %rsi
	jb	.L827
	leaq	(%r8,%r8), %rbx
	movl	%r8d, %r12d
	cmpq	%rbx, %rsi
	jnb	.L827
	leal	1119(%r8,%r8), %r13d
.L828:
	movl	%r15d, %ecx
	movl	$4294966176, %edi
	movabsq	$-4294966177, %rsi
	movl	$-1119, %r15d
	movq	%rcx, %r8
	movb	$0, 12(%rax)
	imulq	%rcx, %r8
	movq	%r8, %rbx
	movl	%r8d, %r8d
	shrq	$32, %rbx
	imulq	$1119, %rbx, %rbx
	addq	%r8, %rbx
	movq	%rbx, %r8
	movl	%ebx, %ebx
	shrq	$32, %r8
	imulq	$1119, %r8, %r8
	addq	%rbx, %r8
	cmpq	%r8, %rdi
	leaq	(%r8,%rsi), %rbx
	cmovb	%rbx, %r8
	subl	%r14d, %r15d
	movl	%r8d, %ebx
	addl	%r8d, %r15d
	subl	%r14d, %ebx
	cmpl	%r14d, %r8d
	movl	$-1119, %r8d
	cmovb	%r15d, %ebx
	subl	%r13d, %r8d
	movl	%ebx, %r15d
	addl	%ebx, %r8d
	subl	%r13d, %r15d
	cmpl	%r13d, %ebx
	movl	%r12d, %ebx
	cmovnb	%r15d, %r8d
	imulq	%r11, %rdx
	movl	%r8d, (%rax)
	movq	%rdx, %r11
	movl	%edx, %edx
	shrq	$32, %r11
	imulq	$1119, %r11, %r11
	addq	%r11, %rdx
	movq	%rdx, %r11
	movl	%edx, %edx
	shrq	$32, %r11
	imulq	$1119, %r11, %r11
	addq	%r11, %rdx
	cmpq	%rdx, %rdi
	leaq	(%rdx,%rsi), %r11
	cmovnb	%rdx, %r11
	leal	-1119(%r12), %edx
	subl	%r8d, %ebx
	subl	%r8d, %edx
	cmpl	%r8d, %r12d
	cmovnb	%ebx, %edx
	imulq	%rcx, %rdx
	movq	%rdx, %rcx
	movl	%edx, %edx
	shrq	$32, %rcx
	imulq	$1119, %rcx, %rcx
	addq	%rdx, %rcx
	movq	%rcx, %rdx
	movl	%ecx, %ecx
	shrq	$32, %rdx
	imulq	$1119, %rdx, %rdx
	addq	%rcx, %rdx
	cmpq	%rdx, %rdi
	leaq	(%rdx,%rsi), %rcx
	cmovb	%rcx, %rdx
	movl	$-1119, %ecx
	subl	%r11d, %ecx
	movl	%edx, %ebx
	subl	%r11d, %ebx
	addl	%edx, %ecx
	cmpl	%r11d, %edx
	cmovnb	%ebx, %ecx
	imulq	%rbp, %r9
	movl	%ecx, 4(%rax)
	movq	%r9, %rdx
	movl	%r9d, %r9d
	shrq	$32, %rdx
	imulq	$1119, %rdx, %rdx
	addq	%rdx, %r9
	movq	%r9, %rdx
	movl	%r9d, %r9d
	shrq	$32, %rdx
	imulq	$1119, %rdx, %rdx
	addq	%r9, %rdx
	cmpq	%rdx, %rdi
	leaq	(%rdx,%rsi), %r9
	cmovb	%r9, %rdx
	imulq	%r10, %rdx
	movq	%rdx, %r9
	movl	%edx, %edx
	shrq	$32, %r9
	imulq	$1119, %r9, %r9
	addq	%rdx, %r9
	movq	%r9, %rdx
	movl	%r9d, %r9d
	shrq	$32, %rdx
	imulq	$1119, %rdx, %rdx
	addq	%r9, %rdx
	leaq	(%rdx,%rsi), %r9
	cmpq	%rdx, %rdi
	cmovb	%r9, %rdx
	movl	%edx, 8(%rax)
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	ret
	.p2align 4
	.p2align 3
.L842:
	cmpl	%edx, %r8d
	je	.L843
	movq	$0, (%rax)
	movl	$0, 8(%rax)
	movb	$1, 12(%rax)
	jmp	.L780
	.p2align 4
	.p2align 3
.L827:
	leal	(%r12,%r12), %r13d
	jmp	.L828
	.p2align 4
	.p2align 3
.L843:
	movq	%r13, %rdx
	imulq	%r13, %rdx
	movq	%rdx, %rcx
	movl	%edx, %edx
	shrq	$32, %rcx
	imulq	$1119, %rcx, %rcx
	addq	%rdx, %rcx
	movq	%rcx, %rdx
	movl	%ecx, %ecx
	shrq	$32, %rdx
	imulq	$1119, %rdx, %rdx
	addq	%rcx, %rdx
	cmpq	%rdx, %rsi
	leaq	(%rdx,%rdi), %rcx
	cmovb	%rcx, %rdx
	movq	%r15, %rcx
	imulq	%r15, %rcx
	movl	%edx, %r11d
	movq	%rcx, %r8
	movl	%ecx, %ecx
	shrq	$32, %r8
	imulq	$1119, %r8, %r8
	addq	%rcx, %r8
	movq	%r8, %rcx
	movl	%r8d, %r8d
	shrq	$32, %rcx
	imulq	$1119, %rcx, %rcx
	addq	%r8, %rcx
	cmpq	%rcx, %rsi
	jnb	.L795
	addq	%rdi, %rcx
	movl	%ecx, %r8d
.L796:
	addl	%r8d, %r8d
.L797:
	imulq	%r13, %r8
	movq	%r8, %r9
	movl	%r8d, %r8d
	shrq	$32, %r9
	imulq	$1119, %r9, %r9
	addq	%r9, %r8
	movq	%r8, %r9
	movl	%r8d, %r8d
	shrq	$32, %r9
	imulq	$1119, %r9, %r9
	addq	%r9, %r8
	movl	$4294966176, %r9d
	leal	1119(%r8), %r10d
	cmpq	%r8, %r9
	jb	.L799
	leaq	(%r8,%r8), %rbx
	movl	%r8d, %r10d
	cmpq	%rbx, %r9
	jnb	.L799
	leal	1119(%r8,%r8), %r10d
.L800:
	movl	$4294966176, %r9d
	leal	(%r11,%r11), %r8d
	leaq	(%rdx,%rdx), %rsi
	cmpq	%rsi, %r9
	leal	1119(%r8), %ebx
	leal	(%r10,%r10), %esi
	cmovb	%ebx, %r8d
	movl	%r8d, %ebx
	addq	%rbx, %rdx
	leal	1119(%r11,%r8), %ebx
	addl	%r11d, %r8d
	leal	1119(%rsi), %r11d
	cmpq	%rdx, %r9
	movl	%r10d, %edx
	cmovb	%ebx, %r8d
	addq	%rdx, %rdx
	movabsq	$-4294966177, %rbx
	cmpq	%rdx, %r9
	movq	%r8, %rdx
	cmovb	%r11d, %esi
	imulq	%r8, %rdx
	movq	%rdx, %r11
	movl	%edx, %edx
	shrq	$32, %r11
	imulq	$1119, %r11, %r11
	addq	%rdx, %r11
	movq	%r11, %rdx
	movl	%r11d, %r11d
	shrq	$32, %rdx
	imulq	$1119, %rdx, %rdx
	addq	%r11, %rdx
	leaq	(%rdx,%rbx), %r11
	cmpq	%rdx, %r9
	cmovb	%r11, %rdx
	movl	%edx, %edi
	subl	%esi, %edi
	cmpl	%esi, %edx
	leal	(%r12,%r12), %edx
	leal	-1119(%rdi), %r11d
	leal	1119(%rdx), %esi
	cmovnb	%edi, %r11d
	leaq	(%rbp,%rbp), %rdi
	cmpq	%rdi, %r9
	cmovnb	%edx, %esi
	imulq	%r15, %rsi
	movq	%rsi, %rdx
	movl	%esi, %esi
	shrq	$32, %rdx
	imulq	$1119, %rdx, %rdx
	addq	%rsi, %rdx
	movq	%rdx, %rsi
	movl	%edx, %edx
	shrq	$32, %rsi
	imulq	$1119, %rsi, %rsi
	addq	%rsi, %rdx
	addq	%rdx, %rbx
	cmpq	%rdx, %r9
	cmovnb	%rdx, %rbx
	imulq	%rcx, %rcx
	movq	%rcx, %rdx
	movl	%ecx, %ecx
	shrq	$32, %rdx
	imulq	$1119, %rdx, %rdx
	addq	%rcx, %rdx
	movq	%rdx, %rcx
	movl	%edx, %edx
	shrq	$32, %rcx
	imulq	$1119, %rcx, %rcx
	addq	%rcx, %rdx
	cmpq	%rdx, %r9
	jnb	.L810
	leal	8952(,%rdx,8), %ecx
.L811:
	movl	%ecx, %r9d
.L814:
	movl	%r10d, %ecx
	leal	-1119(%r10), %edx
	movl	%r11d, (%rax)
	movl	%ebx, 8(%rax)
	subl	%r11d, %ecx
	subl	%r11d, %edx
	cmpl	%r11d, %r10d
	movb	$0, 12(%rax)
	cmovnb	%ecx, %edx
	imulq	%r8, %rdx
	movl	$4294966176, %r8d
	movq	%rdx, %rcx
	movl	%edx, %edx
	shrq	$32, %rcx
	imulq	$1119, %rcx, %rcx
	addq	%rdx, %rcx
	movq	%rcx, %rdx
	movl	%ecx, %ecx
	shrq	$32, %rdx
	imulq	$1119, %rdx, %rdx
	addq	%rcx, %rdx
	movabsq	$-4294966177, %rcx
	addq	%rdx, %rcx
	cmpq	%rdx, %r8
	cmovb	%rcx, %rdx
	movl	%edx, %r8d
	subl	%r9d, %r8d
	cmpl	%r9d, %edx
	leal	-1119(%r8), %ecx
	movl	%r8d, %edx
	cmovb	%ecx, %edx
	movl	%edx, 4(%rax)
	jmp	.L780
.L795:
	leaq	(%rcx,%rcx), %r9
	movl	%ecx, %r8d
	cmpq	%r9, %rsi
	jnb	.L796
	leal	1119(%rcx,%rcx), %r8d
	jmp	.L797
.L810:
	leal	(%rdx,%rdx), %ecx
	addq	%rdx, %rdx
	cmpq	%rdx, %r9
	leal	1119(%rcx), %esi
	cmovb	%rsi, %rcx
	leal	(%rcx,%rcx), %edx
	addq	%rcx, %rcx
	cmpq	%rcx, %r9
	leal	1119(%rdx), %esi
	cmovb	%rsi, %rdx
	leal	(%rdx,%rdx), %ecx
	addq	%rdx, %rdx
	cmpq	%rdx, %r9
	jnb	.L811
	leal	1119(%rcx), %r9d
	jmp	.L814
.L799:
	addl	%r10d, %r10d
	jmp	.L800
	.seh_endproc
	.section	.text$_Z8bench_ecIN2fp8FpPseudoILj4294966177EEEEvPKc,"x"
	.linkonce discard
	.p2align 4
	.globl	_Z8bench_ecIN2fp8FpPseudoILj4294966177EEEEvPKc
	.def	_Z8bench_ecIN2fp8FpPseudoILj4294966177EEEEvPKc;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8bench_ecIN2fp8FpPseudoILj4294966177EEEEvPKc
_Z8bench_ecIN2fp8FpPseudoILj4294966177EEEEvPKc:
.LFB4636:
	pushq	%r15
	.seh_pushreg	%r15
	pushq	%r14
	.seh_pushreg	%r14
	pushq	%r13
	.seh_pushreg	%r13
	pushq	%r12
	.seh_pushreg	%r12
	pushq	%rbp
	.seh_pushreg	%rbp
	pushq	%rdi
	.seh_pushreg	%rdi
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$1240, %rsp
	.seh_stackalloc	1240
	vmovaps	%xmm6, 1184(%rsp)
	.seh_savexmm	%xmm6, 1184
	vmovaps	%xmm7, 1200(%rsp)
	.seh_savexmm	%xmm7, 1200
	vmovaps	%xmm8, 1216(%rsp)
	.seh_savexmm	%xmm8, 1216
	.seh_endprologue
	vmovsd	.LC0(%rip), %xmm8
	vmovsd	.LC1(%rip), %xmm6
	vxorps	%xmm7, %xmm7, %xmm7
	movl	$560815139, %ebx
	movl	$1960037684, %r15d
	movl	$4294966176, %edi
	movabsq	$-4294966177, %rsi
	movl	$3, 48(%rsp)
	movq	%rcx, 56(%rsp)
	.p2align 4
	.p2align 3
.L873:
	movl	$0, 124(%rsp)
	xorl	%r12d, %r12d
	movl	$-1119, %ebp
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	movq	%rax, 40(%rsp)
	.p2align 4
	.p2align 3
.L868:
	movl	%r15d, %r10d
	movzbl	%r12b, %eax
	movq	%r10, %rdx
	leaq	160(%rsp,%rax,4), %r13
	imulq	%r10, %rdx
	movq	%rdx, %rax
	movl	%edx, %edx
	shrq	$32, %rax
	imulq	$1119, %rax, %rax
	addq	%rdx, %rax
	movq	%rax, %rdx
	movl	%eax, %eax
	shrq	$32, %rdx
	imulq	$1119, %rdx, %rdx
	addq	%rdx, %rax
	cmpq	%rax, %rdi
	jnb	.L845
	addq	%rsi, %rax
	movl	%eax, %r11d
	leal	(%rax,%rax), %ecx
.L846:
	addl	%ecx, %r11d
.L848:
	movl	%ebx, %eax
	leal	(%rbx,%rbx), %ecx
	addq	%rax, %rax
	cmpq	%rax, %rdi
	jnb	.L849
	addl	$1119, %ecx
.L850:
	xorl	%r9d, %r9d
	movl	$1, %r8d
	movl	$4294966177, %eax
	jmp	.L852
	.p2align 5
	.p2align 4
	.p2align 3
.L1007:
	movq	%r14, %r8
.L852:
	cqto
	movq	%r9, %r14
	movq	%r8, %r9
	idivq	%rcx
	imulq	%r8, %rax
	subq	%rax, %r14
	movq	%rcx, %rax
	movq	%rdx, %rcx
	testq	%rdx, %rdx
	jne	.L1007
	cmpq	$1, %rax
	jg	.L1033
	movl	$4294966177, %eax
	addq	%r8, %rax
	testq	%r8, %r8
	cmovs	%rax, %r8
	movl	%r8d, %r8d
	imulq	%r11, %r8
	movq	%r8, %rax
	movl	%r8d, %r8d
	shrq	$32, %rax
	imulq	$1119, %rax, %rax
	leaq	(%rax,%r8), %rdx
	addl	%r8d, %eax
	shrq	$32, %rdx
	movl	%eax, %eax
	imulq	$1119, %rdx, %rdx
	addq	%rax, %rdx
	cmpq	%rdx, %rdi
	jnb	.L851
	addq	%rsi, %rdx
	movq	%rdx, %rcx
	imulq	%rdx, %rcx
	movq	%rcx, %rax
	movl	%ecx, %ecx
	shrq	$32, %rax
	imulq	$1119, %rax, %rax
	addq	%rcx, %rax
	movq	%rax, %rcx
	movl	%eax, %eax
	shrq	$32, %rcx
	negq	%rcx
	andl	$1119, %ecx
	addq	%rcx, %rax
.L859:
	leal	(%r15,%r15), %ecx
	addq	%r10, %r10
	leal	1119(%rcx), %r8d
	cmpq	%r10, %rdi
	cmovb	%r8d, %ecx
	leaq	(%rax,%rsi), %r8
	cmpq	%rax, %rdi
	cmovb	%r8, %rax
	movl	%eax, %r8d
	cmpl	%ecx, %eax
	jb	.L856
	subl	%ecx, %eax
	movl	%eax, %ecx
.L862:
	cmpl	%ecx, %r15d
	jnb	.L855
	leal	-1119(%r15), %eax
	movl	%ecx, %r15d
	subl	%ecx, %eax
.L864:
	imulq	%rdx, %rax
	movl	%ecx, 0(%r13)
	movq	%rax, %rdx
	movl	%eax, %eax
	shrq	$32, %rdx
	imulq	$1119, %rdx, %rdx
	addq	%rax, %rdx
	movq	%rdx, %rax
	movl	%edx, %edx
	shrq	$32, %rax
	imulq	$1119, %rax, %rax
	addq	%rdx, %rax
	cmpq	%rax, %rdi
	leaq	(%rax,%rsi), %rdx
	cmovb	%rdx, %rax
	movl	%ebp, %edx
	movl	%eax, %r8d
	subl	%ebx, %edx
	subl	%ebx, %r8d
	addl	%eax, %edx
	cmpl	%ebx, %eax
	movl	%r8d, %ebx
	cmovb	%edx, %ebx
	incq	%r12
	xorl	%ecx, 124(%rsp)
	cmpq	$3000000, %r12
	jne	.L868
	movq	40(%rsp), %r14
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	subq	%r14, %rax
	js	.L869
	vcvtsi2sdq	%rax, %xmm7, %xmm0
.L870:
	vdivsd	%xmm6, %xmm0, %xmm0
	decl	48(%rsp)
	movl	124(%rsp), %eax
	vminsd	%xmm8, %xmm0, %xmm2
	vmovapd	%xmm2, %xmm8
	jne	.L873
	movq	56(%rsp), %r12
	leaq	.LC2(%rip), %rcx
	vmovq	%xmm2, %r8
	xorl	%r14d, %r14d
	movl	$560815139, %r13d
	movl	$1960037684, %ebp
	movabsq	$-4294966177, %rsi
	movq	%r12, %rdx
	call	__mingw_printf
	vmovsd	.LC0(%rip), %xmm8
	movl	$3, 48(%rsp)
	movq	%r12, 56(%rsp)
	.p2align 4
	.p2align 3
.L909:
	movl	$0, 120(%rsp)
	movl	$4294966176, %ebx
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	xorl	%r9d, %r9d
	movq	%rax, 40(%rsp)
	.p2align 4
	.p2align 3
.L906:
	movzbl	%r9b, %eax
	leaq	160(%rsp,%rax,4), %r11
	testb	%r14b, %r14b
	jne	.L1009
	cmpl	$1960037684, %ebp
	je	.L1034
	movl	$1960037684, %eax
	movl	$1960036565, %ecx
	movl	$560814020, %r12d
	movl	$1, %r8d
	subl	%ebp, %eax
	subl	%ebp, %ecx
	cmpl	$1960037684, %ebp
	cmovbe	%eax, %ecx
	movl	$560815139, %eax
	subl	%r13d, %r12d
	subl	%r13d, %eax
	cmpl	$560815139, %r13d
	cmovbe	%rax, %r12
	xorl	%r10d, %r10d
	movl	$4294966177, %eax
	jmp	.L891
	.p2align 5
	.p2align 4
	.p2align 3
.L1013:
	movq	%r15, %r8
.L891:
	cqto
	movq	%r10, %r15
	movq	%r8, %r10
	idivq	%rcx
	imulq	%r8, %rax
	subq	%rax, %r15
	movq	%rcx, %rax
	movq	%rdx, %rcx
	testq	%rdx, %rdx
	jne	.L1013
	cmpq	$1, %rax
	jg	.L1035
	movl	$4294966177, %eax
	addq	%r8, %rax
	testq	%r8, %r8
	cmovs	%rax, %r8
	movl	%r8d, %r8d
	imulq	%r12, %r8
	movq	%r8, %rax
	movl	%r8d, %r8d
	shrq	$32, %rax
	imulq	$1119, %rax, %rax
	leaq	(%rax,%r8), %rdx
	addl	%r8d, %eax
	shrq	$32, %rdx
	movl	%eax, %eax
	imulq	$1119, %rdx, %rdx
	addq	%rax, %rdx
	movl	$4294966176, %eax
	cmpq	%rdx, %rax
	jnb	.L1036
	addq	%rsi, %rdx
	movq	%rdx, %rax
	imulq	%rdx, %rax
	movq	%rax, %rcx
	movl	%eax, %eax
	shrq	$32, %rcx
	imulq	$1119, %rcx, %rcx
	addq	%rax, %rcx
	movq	%rcx, %rax
	movl	%ecx, %ecx
	shrq	$32, %rax
	negq	%rax
	andl	$1119, %eax
	addq	%rcx, %rax
.L897:
	movl	$4294966176, %ecx
	cmpq	%rax, %rcx
	jb	.L1037
	movl	%eax, %ecx
	cmpl	%ebp, %eax
	jb	.L894
	subl	%ebp, %eax
.L900:
	leal	-1960037684(%rax), %r8d
	leal	-1960038803(%rax), %ecx
	cmpl	$1960037684, %eax
	cmovnb	%r8d, %ecx
	cmpl	%ecx, %ebp
	jb	.L893
	movl	%ebp, %eax
	movl	%ecx, %ebp
	subl	%ecx, %eax
.L903:
	imulq	%rdx, %rax
	movq	%rax, %rdx
	movl	%eax, %eax
	shrq	$32, %rdx
	imulq	$1119, %rdx, %rdx
	addq	%rax, %rdx
	movq	%rdx, %rax
	movl	%edx, %edx
	shrq	$32, %rax
	imulq	$1119, %rax, %rax
	addq	%rdx, %rax
	cmpq	%rax, %rbx
	leaq	(%rax,%rsi), %rdx
	cmovb	%rdx, %rax
	movl	$-1119, %edx
	subl	%r13d, %edx
	movl	%eax, %ecx
	subl	%r13d, %ecx
	addl	%eax, %edx
	cmpl	%r13d, %eax
	cmovb	%edx, %ecx
	movl	%ecx, %r13d
.L874:
	incq	%r9
	xorl	%ebp, 120(%rsp)
	movl	%ebp, (%r11)
	cmpq	$3000000, %r9
	jne	.L906
	movq	40(%rsp), %r12
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	subq	%r12, %rax
	js	.L907
	vcvtsi2sdq	%rax, %xmm7, %xmm0
.L908:
	vdivsd	%xmm6, %xmm0, %xmm0
	decl	48(%rsp)
	movl	120(%rsp), %eax
	vminsd	%xmm8, %xmm0, %xmm8
	jne	.L909
	movq	56(%rsp), %r12
	vmovapd	%xmm8, %xmm2
	leaq	.LC3(%rip), %rcx
	vmovq	%xmm8, %r8
	movl	$3, %ebx
	movl	$560815139, %r15d
	movl	$1960037684, %edi
	movl	$4294966176, %ebp
	movabsq	$-4294966177, %r13
	movl	$-1119, %r14d
	movq	%r12, %rdx
	call	__mingw_printf
	vmovsd	.LC0(%rip), %xmm8
	.p2align 4
	.p2align 3
.L943:
	movl	$0, 116(%rsp)
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	xorl	%edx, %edx
	movq	%rax, %rsi
	jmp	.L938
	.p2align 4
	.p2align 3
.L911:
	addq	%r13, %rax
	movl	%eax, %r11d
.L914:
	addl	%r11d, %r11d
.L913:
	imulq	%rdi, %r11
	movq	%r11, %r10
	movl	%r11d, %r11d
	shrq	$32, %r10
	imulq	$1119, %r10, %r10
	addq	%r11, %r10
	movq	%r10, %r11
	movl	%r10d, %r10d
	shrq	$32, %r11
	imulq	$1119, %r11, %r11
	addq	%r11, %r10
	cmpq	%r10, %rbp
	jnb	.L1038
	leal	(%r10,%r13), %r11d
.L918:
	addl	%r11d, %r11d
.L917:
	leal	(%r9,%r9), %r10d
	leaq	(%r8,%r8), %r15
	cmpq	%r15, %rbp
	leal	1119(%r10), %edi
	movl	%r14d, %r15d
	cmovb	%edi, %r10d
	movl	%r10d, %edi
	addq	%rdi, %r8
	leal	(%r10,%r9), %edi
	leal	1119(%r10,%r9), %r10d
	leal	(%r11,%r11), %r9d
	cmpq	%r8, %rbp
	movl	%r11d, %r8d
	cmovnb	%edi, %r10d
	addq	%r8, %r8
	leal	1119(%r9), %edi
	cmpq	%r8, %rbp
	movq	%r10, %r8
	cmovb	%edi, %r9d
	imulq	%r10, %r8
	movq	%r8, %rdi
	movl	%r8d, %r8d
	shrq	$32, %rdi
	imulq	$1119, %rdi, %rdi
	addq	%rdi, %r8
	movq	%r8, %rdi
	movl	%r8d, %r8d
	shrq	$32, %rdi
	imulq	$1119, %rdi, %rdi
	addq	%rdi, %r8
	cmpq	%r8, %rbp
	leaq	(%r8,%r13), %rdi
	cmovb	%rdi, %r8
	subl	%r9d, %r15d
	movl	%r8d, %edi
	addl	%r8d, %r15d
	subl	%r9d, %edi
	cmpl	%r9d, %r8d
	cmovb	%r15, %rdi
	imulq	%rax, %rax
	movq	%rax, %r8
	movl	%eax, %eax
	shrq	$32, %r8
	imulq	$1119, %r8, %r8
	addq	%r8, %rax
	movq	%rax, %r8
	movl	%eax, %eax
	shrq	$32, %r8
	imulq	$1119, %r8, %r8
	addq	%r8, %rax
	cmpq	%rax, %rbp
	jnb	.L926
	leal	8952(,%rax,8), %r8d
.L930:
	leal	-1119(%r11), %eax
	movl	%r11d, %r9d
	movl	%edi, (%rcx)
	subl	%edi, %eax
	subl	%edi, %r9d
	cmpl	%edi, %r11d
	cmovb	%eax, %r9d
	imulq	%r10, %r9
	movq	%r9, %rax
	movl	%r9d, %r9d
	shrq	$32, %rax
	imulq	$1119, %rax, %rax
	addq	%r9, %rax
	movq	%rax, %r9
	movl	%eax, %eax
	shrq	$32, %r9
	imulq	$1119, %r9, %r9
	addq	%r9, %rax
	cmpq	%rax, %rbp
	leaq	(%rax,%r13), %r9
	cmovb	%r9, %rax
	movl	%r14d, %r9d
	subl	%r8d, %r9d
	movl	%eax, %r15d
	addl	%eax, %r9d
	subl	%r8d, %r15d
	cmpl	%r8d, %eax
	cmovb	%r9, %r15
	incq	%rdx
	xorl	%edi, 116(%rsp)
	cmpq	$3000000, %rdx
	je	.L1039
.L938:
	movzbl	%dl, %eax
	leaq	160(%rsp,%rax,4), %rcx
	movq	%rdi, %rax
	imulq	%rdi, %rax
	movq	%rax, %r8
	movl	%eax, %eax
	shrq	$32, %r8
	imulq	$1119, %r8, %r8
	addq	%rax, %r8
	movq	%r8, %rax
	movl	%r8d, %r8d
	shrq	$32, %rax
	imulq	$1119, %rax, %rax
	addq	%rax, %r8
	cmpq	%r8, %rbp
	leaq	(%r8,%r13), %rax
	cmovb	%rax, %r8
	imulq	%r15, %r15
	movl	%r8d, %r9d
	movq	%r15, %rax
	movl	%r15d, %r15d
	shrq	$32, %rax
	imulq	$1119, %rax, %rax
	leaq	(%rax,%r15), %r10
	addl	%r15d, %eax
	shrq	$32, %r10
	movl	%eax, %eax
	imulq	$1119, %r10, %r10
	addq	%r10, %rax
	cmpq	%rax, %rbp
	jb	.L911
	leaq	(%rax,%rax), %r10
	movl	%eax, %r11d
	cmpq	%r10, %rbp
	jnb	.L914
	leal	1119(%rax,%rax), %r11d
	jmp	.L913
	.p2align 4
	.p2align 3
.L1009:
	xorl	%r14d, %r14d
	movl	$560815139, %r13d
	movl	$1960037684, %ebp
	jmp	.L874
	.p2align 4
	.p2align 3
.L1033:
	addq	%r10, %r10
	leal	(%r15,%r15), %ecx
	cmpq	%r10, %rdi
	jb	.L854
	xorl	%edx, %edx
	xorl	%r8d, %r8d
	testl	%ecx, %ecx
	jne	.L856
.L855:
	movl	%r15d, %eax
	movl	%ecx, %r15d
	subl	%ecx, %eax
	jmp	.L864
	.p2align 4
	.p2align 3
.L854:
	addl	$1119, %ecx
	xorl	%r8d, %r8d
	xorl	%edx, %edx
.L856:
	movl	%ebp, %eax
	subl	%ecx, %eax
	leal	(%rax,%r8), %ecx
	jmp	.L862
	.p2align 4
	.p2align 3
.L849:
	testl	%ecx, %ecx
	jne	.L850
	xorl	%edx, %edx
.L851:
	movq	%rdx, %rax
	imulq	%rdx, %rax
	movq	%rax, %r8
	movl	%eax, %eax
	shrq	$32, %r8
	imulq	$1119, %r8, %r8
	addq	%rax, %r8
	movq	%r8, %rax
	movl	%r8d, %r8d
	shrq	$32, %rax
	imulq	$1119, %rax, %rax
	addq	%r8, %rax
	jmp	.L859
	.p2align 4
	.p2align 3
.L845:
	leal	(%rax,%rax), %ecx
	leaq	(%rax,%rax), %r8
	movl	%eax, %r11d
	leal	1119(%rcx), %edx
	cmpq	%r8, %rdi
	cmovb	%edx, %ecx
	movl	%ecx, %edx
	addq	%rax, %rdx
	cmpq	%rdx, %rdi
	jnb	.L846
	leal	1119(%rcx,%rax), %r11d
	jmp	.L848
	.p2align 4
	.p2align 3
.L926:
	leal	(%rax,%rax), %r8d
	addq	%rax, %rax
	cmpq	%rax, %rbp
	leal	1119(%r8), %r9d
	cmovb	%r9, %r8
	leal	(%r8,%r8), %eax
	addq	%r8, %r8
	cmpq	%r8, %rbp
	leal	1119(%rax), %r9d
	cmovb	%r9, %rax
	leal	(%rax,%rax), %r8d
	addq	%rax, %rax
	cmpq	%rax, %rbp
	jnb	.L930
	addl	$1119, %r8d
	jmp	.L930
	.p2align 4
	.p2align 3
.L1038:
	leaq	(%r10,%r10), %rdi
	movl	%r10d, %r11d
	cmpq	%rdi, %rbp
	jnb	.L918
	leal	1119(%r10,%r10), %r11d
	jmp	.L917
	.p2align 4
	.p2align 3
.L1039:
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	subq	%rsi, %rax
	js	.L939
	vcvtsi2sdq	%rax, %xmm7, %xmm0
.L940:
	vdivsd	%xmm6, %xmm0, %xmm0
	decl	%ebx
	movl	116(%rsp), %eax
	vminsd	%xmm8, %xmm0, %xmm2
	vmovapd	%xmm2, %xmm8
	jne	.L943
	movq	%r12, %rdx
	leaq	.LC4(%rip), %rcx
	vmovq	%xmm2, %r8
	movl	$560815139, %r14d
	call	__mingw_printf
	vmovsd	.LC0(%rip), %xmm8
	movq	%r12, 72(%rsp)
	movl	$1960037684, %ebp
	movabsq	$-4294966177, %rbx
	movl	$3, 56(%rsp)
	movl	$1, %r12d
	xorl	%r13d, %r13d
	.p2align 4
	.p2align 3
.L999:
	movl	$0, 112(%rsp)
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	xorl	%ecx, %ecx
	movl	$4294966176, %r8d
	movq	%rax, 48(%rsp)
	jmp	.L996
	.p2align 4
	.p2align 3
.L1042:
	movl	%r12d, %r15d
	movq	%r15, %rdx
	imulq	%r15, %rdx
	movq	%rdx, %r9
	movl	%edx, %edx
	shrq	$32, %r9
	imulq	$1119, %r9, %r9
	addq	%r9, %rdx
	movq	%rdx, %r9
	movl	%edx, %edx
	shrq	$32, %r9
	imulq	$1119, %r9, %r9
	addq	%r9, %rdx
	cmpq	%rdx, %r8
	leaq	(%rdx,%rbx), %r9
	cmovb	%r9, %rdx
	imulq	$1960037684, %rdx, %r10
	movq	%r10, %r9
	movl	%r10d, %r10d
	shrq	$32, %r9
	imulq	$1119, %r9, %r9
	addq	%r10, %r9
	movq	%r9, %r10
	movl	%r9d, %r9d
	shrq	$32, %r10
	imulq	$1119, %r10, %r10
	addq	%r10, %r9
	cmpq	%r9, %r8
	leaq	(%r9,%rbx), %r10
	cmovnb	%r9, %r10
	imulq	%r15, %rdx
	movq	%rdx, %r9
	movl	%edx, %edx
	shrq	$32, %r9
	imulq	$1119, %r9, %r9
	addq	%r9, %rdx
	movq	%rdx, %r9
	movl	%edx, %edx
	shrq	$32, %r9
	imulq	$1119, %r9, %r9
	addq	%r9, %rdx
	cmpq	%rdx, %r8
	leaq	(%rdx,%rbx), %r9
	cmovb	%r9, %rdx
	imulq	$560815139, %rdx, %rdx
	movq	%rdx, %r9
	movl	%edx, %edx
	shrq	$32, %r9
	imulq	$1119, %r9, %r9
	addq	%rdx, %r9
	movq	%r9, %rdx
	movl	%r9d, %r9d
	shrq	$32, %rdx
	imulq	$1119, %rdx, %rdx
	addq	%r9, %rdx
	leaq	(%rdx,%rbx), %r9
	cmpq	%rdx, %r8
	cmovb	%r9, %rdx
	cmpl	%ebp, %r10d
	je	.L1040
	movl	$-1119, %r9d
	movl	%r10d, %r11d
	movl	%ebp, %esi
	subl	%ebp, %r9d
	subl	%ebp, %r11d
	addl	%r10d, %r9d
	cmpl	%ebp, %r10d
	movl	%edx, %r10d
	cmovnb	%r11d, %r9d
	movl	$-1119, %r11d
	subl	%r14d, %r10d
	subl	%r14d, %r11d
	addl	%edx, %r11d
	cmpl	%r14d, %edx
	cmovnb	%r10, %r11
	movq	%r9, %r10
	imulq	%r9, %r10
	movq	%r10, %rdx
	movl	%r10d, %r10d
	shrq	$32, %rdx
	imulq	$1119, %rdx, %rdx
	leaq	(%rdx,%r10), %rdi
	addl	%r10d, %edx
	shrq	$32, %rdi
	movl	%edx, %edx
	imulq	$1119, %rdi, %rdi
	addq	%rdx, %rdi
	cmpq	%rdi, %r8
	leaq	(%rdi,%rbx), %rdx
	cmovb	%rdx, %rdi
	movq	%r9, %rdx
	imulq	%rdi, %rdx
	movq	%rdx, %r10
	movl	%edx, %edx
	shrq	$32, %r10
	imulq	$1119, %r10, %r10
	addq	%r10, %rdx
	movq	%rdx, %r10
	movl	%edx, %edx
	shrq	$32, %r10
	imulq	$1119, %r10, %r10
	addq	%rdx, %r10
	cmpq	%r10, %r8
	leaq	(%r10,%rbx), %rdx
	cmovb	%rdx, %r10
	imulq	%rdi, %rsi
	movl	%r10d, %r12d
	movq	%rsi, %rdi
	movl	%esi, %esi
	shrq	$32, %rdi
	imulq	$1119, %rdi, %rdi
	leaq	(%rsi,%rdi), %rdx
	addl	%edi, %esi
	shrq	$32, %rdx
	movl	%esi, %esi
	imulq	$1119, %rdx, %rdx
	addq	%rsi, %rdx
	leal	(%rdx,%rbx), %edi
	cmpq	%rdx, %r8
	jb	.L982
	leaq	(%rdx,%rdx), %rsi
	movl	%edx, %edi
	cmpq	%rsi, %r8
	jnb	.L982
	leal	1119(%rdx,%rdx), %ebp
.L983:
	movq	%r11, %rsi
	imulq	%r11, %rsi
	movq	%rsi, %rdx
	movl	%esi, %esi
	shrq	$32, %rdx
	imulq	$1119, %rdx, %rdx
	addq	%rdx, %rsi
	movq	%rsi, %rdx
	movl	%esi, %esi
	shrq	$32, %rdx
	imulq	$1119, %rdx, %rdx
	addq	%rsi, %rdx
	cmpq	%rdx, %r8
	leaq	(%rdx,%rbx), %rsi
	cmovb	%rsi, %rdx
	movl	%edx, %esi
	subl	%r12d, %esi
	movl	%esi, 40(%rsp)
	movl	$-1119, %esi
	subl	%r12d, %esi
	addl	%edx, %esi
	cmpl	%r12d, %edx
	cmovnb	40(%rsp), %esi
	movl	$-1119, %edx
	subl	%ebp, %edx
	movl	%esi, %r12d
	addl	%esi, %edx
	subl	%ebp, %r12d
	cmpl	%ebp, %esi
	movl	%edi, %esi
	movl	%r12d, %ebp
	cmovb	%edx, %ebp
	imulq	%r10, %r14
	movq	%r14, %rdx
	movl	%r14d, %r14d
	shrq	$32, %rdx
	imulq	$1119, %rdx, %rdx
	leaq	(%rdx,%r14), %r10
	addl	%r14d, %edx
	movl	$-1119, %r14d
	shrq	$32, %r10
	movl	%edx, %edx
	imulq	$1119, %r10, %r10
	addq	%r10, %rdx
	cmpq	%rdx, %r8
	leaq	(%rdx,%rbx), %r10
	cmovnb	%rdx, %r10
	leal	-1119(%rdi), %edx
	subl	%ebp, %esi
	subl	%ebp, %edx
	cmpl	%ebp, %edi
	cmovnb	%esi, %edx
	imulq	%r11, %rdx
	movq	%rdx, %r11
	movl	%edx, %edx
	shrq	$32, %r11
	imulq	$1119, %r11, %r11
	addq	%r11, %rdx
	movq	%rdx, %r11
	movl	%edx, %edx
	shrq	$32, %r11
	imulq	$1119, %r11, %r11
	addq	%r11, %rdx
	cmpq	%rdx, %r8
	leaq	(%rdx,%rbx), %r11
	cmovb	%r11, %rdx
	subl	%r10d, %r14d
	movl	%edx, %r11d
	addl	%edx, %r14d
	subl	%r10d, %r11d
	cmpl	%r10d, %edx
	movq	%r15, %rdx
	cmovnb	%r11, %r14
	imulq	%r9, %rdx
	movq	%rdx, %r9
	movl	%edx, %edx
	shrq	$32, %r9
	imulq	$1119, %r9, %r9
	addq	%r9, %rdx
	movq	%rdx, %r9
	movl	%edx, %edx
	shrq	$32, %r9
	imulq	$1119, %r9, %r9
	addq	%r9, %rdx
	leaq	(%rdx,%rbx), %r12
	cmpq	%rdx, %r8
	cmovnb	%rdx, %r12
.L944:
	incq	%rcx
	xorl	%ebp, 112(%rsp)
	movl	%ebp, (%rax)
	cmpq	$3000000, %rcx
	je	.L1041
.L996:
	movzbl	%cl, %eax
	leaq	160(%rsp,%rax,4), %rax
	testb	%r13b, %r13b
	je	.L1042
	xorl	%r13d, %r13d
	movl	$1, %r12d
	movl	$560815139, %r14d
	movl	$1960037684, %ebp
	jmp	.L944
	.p2align 4
	.p2align 3
.L1041:
	movq	48(%rsp), %r15
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	subq	%r15, %rax
	js	.L997
	vcvtsi2sdq	%rax, %xmm7, %xmm0
.L998:
	vdivsd	%xmm6, %xmm0, %xmm0
	decl	56(%rsp)
	movl	112(%rsp), %eax
	vminsd	%xmm8, %xmm0, %xmm8
	jne	.L999
	movq	72(%rsp), %r12
	vmovapd	%xmm8, %xmm2
	leaq	.LC5(%rip), %rcx
	vmovq	%xmm8, %r8
	movl	$3, %edi
	movl	$1960037684, %esi
	movq	%r12, %rdx
	call	__mingw_printf
	vmovsd	.LC0(%rip), %xmm8
	movabsq	$4855782435, %rax
	movb	$0, 140(%rsp)
	movq	%rax, 132(%rsp)
	movabsq	$-461202339323874386, %rax
	movq	$1121630278, 152(%rsp)
	movq	%rax, 144(%rsp)
	.p2align 4
	.p2align 3
.L1005:
	movl	$0, 108(%rsp)
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	xorl	%ebx, %ebx
	movq	%rax, %rbp
	.p2align 4
	.p2align 3
.L1000:
	leaq	128(%rsp), %rdx
	leaq	144(%rsp), %r8
	leaq	80(%rsp), %rcx
	movl	%esi, 128(%rsp)
	call	_ZN2ec8JacobianIN2fp8FpPseudoILj4294966177EEEE3addERKS4_S6_
	movq	88(%rsp), %rdx
	movq	80(%rsp), %rax
	xorl	%eax, 108(%rsp)
	movq	%rdx, 136(%rsp)
	movzbl	%bl, %edx
	incq	%rbx
	movq	%rax, 128(%rsp)
	movl	%eax, %esi
	movl	%eax, 160(%rsp,%rdx,4)
	cmpq	$3000000, %rbx
	jne	.L1000
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	subq	%rbp, %rax
	js	.L1001
	vcvtsi2sdq	%rax, %xmm7, %xmm0
.L1002:
	vdivsd	%xmm6, %xmm0, %xmm0
	decl	%edi
	movl	108(%rsp), %eax
	vminsd	%xmm8, %xmm0, %xmm2
	vmovapd	%xmm2, %xmm8
	jne	.L1005
	vmovaps	1184(%rsp), %xmm6
	vmovaps	1200(%rsp), %xmm7
	movq	%r12, %rdx
	leaq	.LC6(%rip), %rcx
	vmovaps	1216(%rsp), %xmm8
	vmovq	%xmm2, %r8
	addq	$1240, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	jmp	__mingw_printf
	.p2align 4
	.p2align 3
.L1040:
	cmpl	%edx, %r14d
	je	.L1043
	xorl	%r12d, %r12d
	xorl	%r14d, %r14d
	xorl	%ebp, %ebp
	movl	$1, %r13d
	jmp	.L944
	.p2align 4
	.p2align 3
.L1034:
	cmpl	$560815139, %r13d
	je	.L1044
	xorl	%r13d, %r13d
	xorl	%ebp, %ebp
	movl	$1, %r14d
	jmp	.L874
	.p2align 4
	.p2align 3
.L982:
	leal	(%rdi,%rdi), %ebp
	jmp	.L983
	.p2align 4
	.p2align 3
.L1037:
	addq	%rsi, %rax
	movl	%eax, %ecx
	cmpl	%ebp, %eax
	jb	.L894
	subl	%ebp, %eax
	leal	-1960037684(%rax), %r8d
	leal	-1960038803(%rax), %ecx
	cmpl	$1960037684, %eax
	cmovnb	%r8d, %ecx
.L893:
	leal	-1119(%rbp), %eax
	movl	%ecx, %ebp
	subl	%ecx, %eax
	jmp	.L903
	.p2align 4
	.p2align 3
.L894:
	subl	%ebp, %ecx
	leal	-1119(%rcx), %eax
	jmp	.L900
	.p2align 4
	.p2align 3
.L1035:
	xorl	%edx, %edx
	testl	%ebp, %ebp
	jne	.L894
	movl	$-1960038803, %ecx
	leal	-1119(%rbp), %eax
	subl	%ecx, %eax
	movl	%ecx, %ebp
	jmp	.L903
	.p2align 4
	.p2align 3
.L1001:
	movq	%rax, %rdx
	andl	$1, %eax
	shrq	%rdx
	orq	%rax, %rdx
	vcvtsi2sdq	%rdx, %xmm7, %xmm0
	vaddsd	%xmm0, %xmm0, %xmm0
	jmp	.L1002
	.p2align 4
	.p2align 3
.L997:
	movq	%rax, %rdx
	andl	$1, %eax
	shrq	%rdx
	orq	%rax, %rdx
	vcvtsi2sdq	%rdx, %xmm7, %xmm0
	vaddsd	%xmm0, %xmm0, %xmm0
	jmp	.L998
	.p2align 4
	.p2align 3
.L939:
	movq	%rax, %rdx
	andl	$1, %eax
	shrq	%rdx
	orq	%rax, %rdx
	vcvtsi2sdq	%rdx, %xmm7, %xmm0
	vaddsd	%xmm0, %xmm0, %xmm0
	jmp	.L940
	.p2align 4
	.p2align 3
.L869:
	movq	%rax, %rdx
	andl	$1, %eax
	shrq	%rdx
	orq	%rax, %rdx
	vcvtsi2sdq	%rdx, %xmm7, %xmm0
	vaddsd	%xmm0, %xmm0, %xmm0
	jmp	.L870
	.p2align 4
	.p2align 3
.L907:
	movq	%rax, %rdx
	andl	$1, %eax
	shrq	%rdx
	orq	%rax, %rdx
	vcvtsi2sdq	%rdx, %xmm7, %xmm0
	vaddsd	%xmm0, %xmm0, %xmm0
	jmp	.L908
.L1044:
	xorl	%r8d, %r8d
	movl	$1, %r10d
	movl	$1121630278, %ecx
	movl	$4294966177, %eax
	jmp	.L876
	.p2align 5
	.p2align 4
	.p2align 3
.L1011:
	movq	%rbp, %r10
.L876:
	cqto
	idivq	%rcx
	imulq	%r10, %rax
	subq	%rax, %r8
	movq	%rcx, %rax
	movq	%rdx, %rcx
	movq	%r8, %rbp
	movq	%r10, %r8
	testq	%rdx, %rdx
	jne	.L1011
	cmpq	$1, %rax
	jg	.L1012
	movl	$4294966177, %ecx
	testq	%r10, %r10
	leaq	(%r10,%rcx), %rax
	cmovs	%rax, %r10
	movl	%r10d, %eax
	imulq	$989511900, %rax, %rax
	movq	%rax, %rdx
	movl	%eax, %eax
	shrq	$32, %rdx
	imulq	$1119, %rdx, %rdx
	addq	%rdx, %rax
	movq	%rax, %rdx
	movl	%eax, %eax
	shrq	$32, %rdx
	imulq	$1119, %rdx, %rdx
	addq	%rax, %rdx
	movl	$4294966176, %eax
	cmpq	%rdx, %rax
	jnb	.L1045
	subq	%rcx, %rdx
	movq	%rdx, %rcx
	imulq	%rdx, %rcx
	movq	%rcx, %rax
	movl	%ecx, %ecx
	shrq	$32, %rax
	imulq	$1119, %rax, %rax
	leaq	(%rax,%rcx), %rbp
	addl	%ecx, %eax
	shrq	$32, %rbp
	movl	%eax, %eax
	negq	%rbp
	andl	$1119, %ebp
	addq	%rax, %rbp
.L880:
	movl	$4294966176, %eax
	cmpq	%rbp, %rax
	jb	.L1046
	movl	$3920075367, %eax
	cmpq	%rbp, %rax
	jnb	.L882
	addl	$374891928, %ebp
.L877:
	movl	$1960037684, %eax
	subl	%ebp, %eax
.L884:
	imulq	%rdx, %rax
	movq	%rax, %rdx
	movl	%eax, %eax
	shrq	$32, %rdx
	imulq	$1119, %rdx, %rdx
	addq	%rdx, %rax
	movq	%rax, %rdx
	movl	%eax, %eax
	shrq	$32, %rdx
	imulq	$1119, %rdx, %rdx
	addq	%rdx, %rax
	movl	$4294966176, %edx
	leal	1119(%rax), %r13d
	cmpq	%rax, %rdx
	jb	.L886
	movl	%eax, %r13d
	cmpq	$560815138, %rax
	jbe	.L886
	leal	-560815139(%rax), %r13d
	jmp	.L874
.L1043:
	movl	%ebp, %edx
	movabsq	$-4294966177, %r11
	movq	%rdx, %r9
	imulq	%rdx, %r9
	movq	%r9, %r10
	movl	%r9d, %r9d
	shrq	$32, %r10
	imulq	$1119, %r10, %r10
	addq	%r10, %r9
	movq	%r9, %r10
	movl	%r9d, %r9d
	shrq	$32, %r10
	imulq	$1119, %r10, %r10
	leaq	(%r10,%r9), %rdi
	movl	$4294966176, %r10d
	cmpq	%rdi, %r10
	leaq	(%rdi,%r11), %r9
	cmovb	%r9, %rdi
	movl	%r14d, %r9d
	movq	%r9, 64(%rsp)
	imulq	%r9, %r9
	movl	%edi, %ebp
	movq	%r9, %rsi
	movl	%r9d, %r9d
	shrq	$32, %rsi
	imulq	$1119, %rsi, %rsi
	addq	%rsi, %r9
	movq	%r9, %rsi
	movl	%r9d, %r9d
	shrq	$32, %rsi
	imulq	$1119, %rsi, %rsi
	addq	%r9, %rsi
	cmpq	%rsi, %r10
	jb	.L1047
	leaq	(%rsi,%rsi), %r11
	movl	%esi, %r9d
	cmpq	%r11, %r10
	jnb	.L952
	leal	1119(%rsi,%rsi), %r9d
.L953:
	imulq	%r9, %rdx
	movq	%rdx, %r10
	movl	%edx, %edx
	shrq	$32, %r10
	imulq	$1119, %r10, %r10
	leaq	(%r10,%rdx), %r9
	movq	%r9, %rdx
	movl	%r9d, %r9d
	shrq	$32, %rdx
	imulq	$1119, %rdx, %rdx
	addq	%r9, %rdx
	movl	$4294966176, %r9d
	leal	1119(%rdx), %r10d
	cmpq	%rdx, %r9
	jb	.L955
	leaq	(%rdx,%rdx), %r11
	movl	%edx, %r10d
	cmpq	%r11, %r9
	jnb	.L955
	leal	1119(%rdx,%rdx), %edx
	movl	%edx, 40(%rsp)
.L956:
	movl	$4294966176, %r14d
	leal	(%rbp,%rbp), %edx
	leaq	(%rdi,%rdi), %r10
	cmpq	%r10, %r14
	leal	1119(%rdx), %r9d
	cmovb	%r9d, %edx
	movl	%edx, %r9d
	leal	1119(%rbp,%rdx), %r10d
	addl	%ebp, %edx
	addq	%rdi, %r9
	cmpq	%r9, %r14
	movl	40(%rsp), %r9d
	cmovb	%r10d, %edx
	movl	%edx, %edi
	movq	%rdi, %rdx
	leal	(%r9,%r9), %r10d
	addq	%r9, %r9
	cmpq	%r9, %r14
	leal	1119(%r10), %r11d
	cmovb	%r11d, %r10d
	imulq	%rdi, %rdx
	movabsq	$-4294966177, %r11
	movq	%rdx, %r9
	movl	%edx, %edx
	shrq	$32, %r9
	imulq	$1119, %r9, %r9
	addq	%r9, %rdx
	movq	%rdx, %r9
	movl	%edx, %edx
	shrq	$32, %r9
	imulq	$1119, %r9, %r9
	addq	%rdx, %r9
	leaq	(%r9,%r11), %rdx
	cmpq	%r9, %r14
	cmovb	%rdx, %r9
	movl	%r9d, %ebp
	subl	%r10d, %ebp
	cmpl	%r10d, %r9d
	leaq	(%r15,%r15), %r9
	leal	-1119(%rbp), %edx
	cmovb	%edx, %ebp
	addl	%r12d, %r12d
	cmpq	%r9, %r14
	leal	1119(%r12), %edx
	cmovnb	%r12d, %edx
	imulq	64(%rsp), %rdx
	movq	%rdx, %r9
	movl	%edx, %edx
	shrq	$32, %r9
	imulq	$1119, %r9, %r9
	addq	%r9, %rdx
	movq	%rdx, %r9
	movl	%edx, %edx
	shrq	$32, %r9
	imulq	$1119, %r9, %r9
	addq	%r9, %rdx
	addq	%rdx, %r11
	cmpq	%rdx, %r14
	cmovb	%r11, %rdx
	imulq	%rsi, %rsi
	movq	%rdx, %r12
	movq	%rsi, %rdx
	movl	%esi, %r9d
	shrq	$32, %rdx
	imulq	$1119, %rdx, %rdx
	addq	%r9, %rdx
	movq	%rdx, %r9
	movl	%edx, %edx
	shrq	$32, %r9
	imulq	$1119, %r9, %r9
	addq	%r9, %rdx
	cmpq	%rdx, %r14
	jnb	.L966
	leal	8952(,%rdx,8), %r10d
.L970:
	movl	40(%rsp), %esi
	movl	$4294966176, %r11d
	movl	%esi, %r9d
	leal	-1119(%rsi), %edx
	subl	%ebp, %r9d
	subl	%ebp, %edx
	cmpl	%ebp, %esi
	cmovnb	%r9d, %edx
	imulq	%rdi, %rdx
	movq	%rdx, %r9
	movl	%edx, %edx
	shrq	$32, %r9
	imulq	$1119, %r9, %r9
	addq	%rdx, %r9
	movq	%r9, %rdx
	movl	%r9d, %r9d
	shrq	$32, %rdx
	imulq	$1119, %rdx, %rdx
	addq	%r9, %rdx
	movabsq	$-4294966177, %r9
	addq	%rdx, %r9
	cmpq	%rdx, %r11
	cmovb	%r9, %rdx
	movl	%edx, %r9d
	subl	%r10d, %r9d
	cmpl	%r10d, %edx
	leal	-1119(%r9), %r14d
	cmovnb	%r9, %r14
	jmp	.L944
.L1036:
	movq	%rdx, %rax
	imulq	%rdx, %rax
	movq	%rax, %rcx
	movl	%eax, %eax
	shrq	$32, %rcx
	imulq	$1119, %rcx, %rcx
	addq	%rax, %rcx
	movq	%rcx, %rax
	movl	%ecx, %ecx
	shrq	$32, %rax
	imulq	$1119, %rax, %rax
	addq	%rcx, %rax
	jmp	.L897
.L1047:
	addq	%r11, %rsi
	movl	%esi, %r9d
.L952:
	addl	%r9d, %r9d
	jmp	.L953
.L882:
	addl	$374890809, %ebp
	cmpl	$1960037684, %ebp
	jbe	.L877
	movl	$1960036565, %eax
	subl	%ebp, %eax
	jmp	.L884
.L1046:
	addl	$374891928, %ebp
	jmp	.L877
.L886:
	subl	$560816258, %r13d
	jmp	.L874
.L955:
	leal	(%r10,%r10), %edx
	movl	%edx, 40(%rsp)
	jmp	.L956
.L966:
	leal	(%rdx,%rdx), %r9d
	addq	%rdx, %rdx
	cmpq	%rdx, %r14
	leal	1119(%r9), %r10d
	cmovb	%r10, %r9
	leal	(%r9,%r9), %edx
	addq	%r9, %r9
	leal	1119(%rdx), %r10d
	cmpq	%r9, %r14
	cmovb	%r10, %rdx
	leal	(%rdx,%rdx), %r10d
	addq	%rdx, %rdx
	cmpq	%rdx, %r14
	jnb	.L970
	addl	$1119, %r10d
	jmp	.L970
.L1012:
	xorl	%edx, %edx
	movl	$374890809, %ebp
	jmp	.L877
.L1045:
	movq	%rdx, %rcx
	imulq	%rdx, %rcx
	movq	%rcx, %rax
	movl	%ecx, %ecx
	shrq	$32, %rax
	imulq	$1119, %rax, %rax
	leaq	(%rax,%rcx), %rbp
	addl	%ecx, %eax
	shrq	$32, %rbp
	movl	%eax, %eax
	imulq	$1119, %rbp, %rbp
	addq	%rax, %rbp
	jmp	.L880
	.seh_endproc
	.section	.text$_ZNSt23mersenne_twister_engineIjLy32ELy624ELy397ELy31ELj2567483615ELy11ELj4294967295ELy7ELj2636928640ELy15ELj4022730752ELy18ELj1812433253EE11_M_gen_randEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt23mersenne_twister_engineIjLy32ELy624ELy397ELy31ELj2567483615ELy11ELj4294967295ELy7ELj2636928640ELy15ELj4022730752ELy18ELj1812433253EE11_M_gen_randEv
	.def	_ZNSt23mersenne_twister_engineIjLy32ELy624ELy397ELy31ELj2567483615ELy11ELj4294967295ELy7ELj2636928640ELy15ELj4022730752ELy18ELj1812433253EE11_M_gen_randEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt23mersenne_twister_engineIjLy32ELy624ELy397ELy31ELj2567483615ELy11ELj4294967295ELy7ELj2636928640ELy15ELj4022730752ELy18ELj1812433253EE11_M_gen_randEv
_ZNSt23mersenne_twister_engineIjLy32ELy624ELy397ELy31ELj2567483615ELy11ELj4294967295ELy7ELj2636928640ELy15ELj4022730752ELy18ELj1812433253EE11_M_gen_randEv:
.LFB5003:
	subq	$40, %rsp
	.seh_stackalloc	40
	vmovaps	%xmm6, (%rsp)
	.seh_savexmm	%xmm6, 0
	vmovaps	%xmm7, 16(%rsp)
	.seh_savexmm	%xmm7, 16
	.seh_endprologue
	movl	$-1727483681, %eax
	vpcmpeqd	%xmm2, %xmm2, %xmm2
	vmovd	%eax, %xmm3
	vpbroadcastd	%xmm3, %xmm3
	vpslld	$31, %xmm2, %xmm7
	vpsrld	$1, %xmm2, %xmm6
	vmovdqa	%xmm3, %xmm5
	vpsrld	$31, %xmm2, %xmm4
	leaq	896(%rcx), %rdx
	movq	%rcx, %rax
	.p2align 6
	.p2align 4
	.p2align 3
.L1049:
	vpand	4(%rax), %xmm6, %xmm1
	vpand	(%rax), %xmm7, %xmm0
	addq	$16, %rax
	vpor	%xmm1, %xmm0, %xmm0
	vpsrld	$1, %xmm0, %xmm1
	vpxor	1572(%rax), %xmm1, %xmm1
	vpand	%xmm4, %xmm0, %xmm0
	vpmulld	%xmm5, %xmm0, %xmm0
	vpxor	%xmm0, %xmm1, %xmm0
	vmovdqu	%xmm0, -16(%rax)
	cmpq	%rax, %rdx
	jne	.L1049
	movl	904(%rcx), %eax
	movl	908(%rcx), %edx
	vmovq	896(%rcx), %xmm0
	vmovq	.LC13(%rip), %xmm1
	vmovq	.LC14(%rip), %xmm4
	vpand	%xmm1, %xmm0, %xmm0
	vmovq	900(%rcx), %xmm1
	vpand	%xmm4, %xmm1, %xmm1
	vpor	%xmm1, %xmm0, %xmm0
	vmovq	2484(%rcx), %xmm1
	vpslld	$31, %xmm2, %xmm5
	vpsrld	$1, %xmm0, %xmm4
	vpxor	%xmm4, %xmm1, %xmm1
	vmovq	.LC15(%rip), %xmm4
	vpand	%xmm4, %xmm0, %xmm0
	andl	$2147483647, %edx
	andl	$-2147483648, %eax
	vmovq	.LC16(%rip), %xmm4
	vpmulld	%xmm4, %xmm0, %xmm0
	orl	%edx, %eax
	vpsrld	$1, %xmm2, %xmm4
	vpsrld	$31, %xmm2, %xmm2
	movl	%eax, %edx
	andl	$1, %eax
	shrl	%edx
	xorl	2492(%rcx), %edx
	negl	%eax
	vpxor	%xmm0, %xmm1, %xmm1
	andl	$-1727483681, %eax
	vmovq	%xmm1, 896(%rcx)
	xorl	%edx, %eax
	leaq	2492(%rcx), %rdx
	movl	%eax, 904(%rcx)
	leaq	908(%rcx), %rax
	.p2align 6
	.p2align 4
	.p2align 3
.L1050:
	vpand	4(%rax), %xmm4, %xmm1
	addq	$16, %rax
	vpand	-16(%rax), %xmm5, %xmm0
	vpor	%xmm1, %xmm0, %xmm0
	vpsrld	$1, %xmm0, %xmm1
	vpxor	-924(%rax), %xmm1, %xmm1
	vpand	%xmm2, %xmm0, %xmm0
	vpmulld	%xmm3, %xmm0, %xmm0
	vpxor	%xmm0, %xmm1, %xmm0
	vmovdqu	%xmm0, -16(%rax)
	cmpq	%rax, %rdx
	jne	.L1050
	movl	2492(%rcx), %eax
	movl	(%rcx), %edx
	movq	$0, 2496(%rcx)
	vmovaps	(%rsp), %xmm6
	vmovaps	16(%rsp), %xmm7
	andl	$2147483647, %edx
	andl	$-2147483648, %eax
	orl	%edx, %eax
	movl	%eax, %edx
	andl	$1, %eax
	shrl	%edx
	xorl	1584(%rcx), %edx
	negl	%eax
	andl	$-1727483681, %eax
	xorl	%edx, %eax
	movl	%eax, 2492(%rcx)
	addq	$40, %rsp
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC18:
	.ascii "FIELD,%s,add,%.3f\12\0"
.LC19:
	.ascii "FIELD,%s,sub,%.3f\12\0"
.LC20:
	.ascii "FIELD,%s,mul,%.3f\12\0"
.LC21:
	.ascii "FIELD,%s,sqr,%.3f\12\0"
.LC23:
	.ascii "FIELD,%s,inv,%.3f\12\0"
	.section	.text$_Z11bench_fieldIN2fp6FpMontILj4294966177EEEEvPKc,"x"
	.linkonce discard
	.p2align 4
	.globl	_Z11bench_fieldIN2fp6FpMontILj4294966177EEEEvPKc
	.def	_Z11bench_fieldIN2fp6FpMontILj4294966177EEEEvPKc;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z11bench_fieldIN2fp6FpMontILj4294966177EEEEvPKc
_Z11bench_fieldIN2fp6FpMontILj4294966177EEEEvPKc:
.LFB4586:
	pushq	%r14
	.seh_pushreg	%r14
	movl	$5728, %eax
	pushq	%r13
	.seh_pushreg	%r13
	pushq	%r12
	.seh_pushreg	%r12
	pushq	%rbp
	.seh_pushreg	%rbp
	pushq	%rdi
	.seh_pushreg	%rdi
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	call	___chkstk_ms
	subq	%rax, %rsp
	.seh_stackalloc	5728
	vmovaps	%xmm6, 5648(%rsp)
	.seh_savexmm	%xmm6, 5648
	vmovaps	%xmm7, 5664(%rsp)
	.seh_savexmm	%xmm7, 5664
	vmovaps	%xmm8, 5680(%rsp)
	.seh_savexmm	%xmm8, 5680
	vmovaps	%xmm9, 5696(%rsp)
	.seh_savexmm	%xmm9, 5696
	vmovaps	%xmm10, 5712(%rsp)
	.seh_savexmm	%xmm10, 5712
	.seh_endprologue
	movl	$1, %edx
	movq	%rcx, %rbx
	movl	$42, 3136(%rsp)
	leaq	3140(%rsp), %r8
	movl	$42, %ecx
	.p2align 6
	.p2align 4
	.p2align 3
.L1054:
	movl	%ecx, %eax
	addq	$4, %r8
	shrl	$30, %eax
	xorl	%ecx, %eax
	imull	$1812433253, %eax, %eax
	leal	(%rax,%rdx), %ecx
	incq	%rdx
	movl	%ecx, -4(%r8)
	cmpq	$624, %rdx
	jne	.L1054
	leaq	2112(%rsp), %r9
	vpcmpeqd	%xmm5, %xmm5, %xmm5
	movl	$-1727483681, %eax
	leaq	1088(%rsp), %r8
	vmovd	%eax, %xmm2
	leaq	64(%rsp), %r10
	movq	%r9, %rbp
	movq	%r9, %r11
	leaq	4032(%rsp), %rcx
	vpbroadcastd	%xmm2, %xmm2
	vpsrld	$1, %xmm5, %xmm4
	vpslld	$31, %xmm5, %xmm3
	vmovq	.LC14(%rip), %xmm10
	vmovq	.LC13(%rip), %xmm9
	vmovq	.LC15(%rip), %xmm8
	vmovq	.LC16(%rip), %xmm7
	jmp	.L1059
	.p2align 4
	.p2align 3
.L1130:
	movl	3136(%rsp,%rdx,4), %edi
	leaq	1(%rdx), %rsi
	movl	%edi, %eax
	shrl	$11, %eax
	xorl	%edi, %eax
	movl	%eax, %edx
	sall	$7, %edx
	andl	$-1658038656, %edx
	xorl	%edx, %eax
	movl	%eax, %edx
	sall	$15, %edx
	andl	$-272236544, %edx
	xorl	%edx, %eax
	movl	%eax, %edx
	shrl	$18, %edx
	xorl	%edx, %eax
	xorl	%edx, %edx
	cmpl	$-1119, %eax
	setnb	%dl
	imull	$-1119, %edx, %edx
	subl	%edx, %eax
	movl	%eax, (%r10)
.L1056:
	movl	3136(%rsp,%rsi,4), %eax
	leaq	1(%rsi), %rdx
	movl	$0, (%r9)
	movl	%eax, %esi
	shrl	$11, %esi
	xorl	%esi, %eax
	movl	%eax, %esi
	sall	$7, %esi
	andl	$-1658038656, %esi
	xorl	%esi, %eax
	movl	%eax, %esi
	sall	$15, %esi
	andl	$-272236544, %esi
	xorl	%esi, %eax
	movl	%eax, %esi
	shrl	$18, %esi
	xorl	%esi, %eax
	xorl	%esi, %esi
	cmpl	$-1119, %eax
	setnb	%sil
	addq	$4, %r8
	addq	$4, %r9
	addq	$4, %r10
	imull	$-1119, %esi, %esi
	subl	%esi, %eax
	movl	%eax, -4(%r8)
	cmpq	%r8, %r11
	je	.L1129
.L1059:
	cmpq	$623, %rdx
	jbe	.L1130
	leaq	3136(%rsp), %rax
	vpsrld	$31, %xmm5, %xmm6
	.p2align 6
	.p2align 4
	.p2align 3
.L1057:
	vpand	(%rax), %xmm3, %xmm1
	vpand	4(%rax), %xmm4, %xmm0
	addq	$16, %rax
	vpor	%xmm1, %xmm0, %xmm0
	vpsrld	$1, %xmm0, %xmm1
	vpxor	1572(%rax), %xmm1, %xmm1
	vpand	%xmm6, %xmm0, %xmm0
	vpmulld	%xmm2, %xmm0, %xmm0
	vpxor	%xmm0, %xmm1, %xmm0
	vmovdqa	%xmm0, -16(%rax)
	cmpq	%rax, %rcx
	jne	.L1057
	movl	4040(%rsp), %edx
	movl	4044(%rsp), %eax
	vmovq	4036(%rsp), %xmm0
	vmovq	4032(%rsp), %xmm1
	vpand	%xmm10, %xmm0, %xmm0
	vpand	%xmm9, %xmm1, %xmm1
	vmovq	5620(%rsp), %xmm6
	vpor	%xmm1, %xmm0, %xmm0
	vpsrld	$1, %xmm0, %xmm1
	vpand	%xmm8, %xmm0, %xmm0
	vpxor	%xmm6, %xmm1, %xmm1
	vpsrld	$31, %xmm5, %xmm6
	andl	$-2147483648, %edx
	andl	$2147483647, %eax
	vpmulld	%xmm7, %xmm0, %xmm0
	orl	%edx, %eax
	movl	%eax, %edx
	andl	$1, %eax
	shrl	%edx
	xorl	5628(%rsp), %edx
	negl	%eax
	vpxor	%xmm0, %xmm1, %xmm0
	andl	$-1727483681, %eax
	vmovq	%xmm0, 4032(%rsp)
	xorl	%edx, %eax
	leaq	5628(%rsp), %rdx
	movl	%eax, 4040(%rsp)
	leaq	4044(%rsp), %rax
	.p2align 6
	.p2align 4
	.p2align 3
.L1058:
	vpand	(%rax), %xmm3, %xmm1
	addq	$16, %rax
	vpand	-12(%rax), %xmm4, %xmm0
	vpor	%xmm1, %xmm0, %xmm0
	vpsrld	$1, %xmm0, %xmm1
	vpxor	-924(%rax), %xmm1, %xmm1
	vpand	%xmm6, %xmm0, %xmm0
	vpmulld	%xmm2, %xmm0, %xmm0
	vpxor	%xmm0, %xmm1, %xmm0
	vmovdqu	%xmm0, -16(%rax)
	cmpq	%rax, %rdx
	jne	.L1058
	movl	3136(%rsp), %edx
	movl	5628(%rsp), %eax
	movl	%edx, %esi
	andl	$-2147483648, %eax
	andl	$2147483647, %esi
	orl	%esi, %eax
	movl	%eax, %esi
	andl	$1, %eax
	shrl	%esi
	xorl	4720(%rsp), %esi
	negl	%eax
	andl	$-1727483681, %eax
	xorl	%eax, %esi
	movl	%edx, %eax
	shrl	$11, %eax
	movl	%esi, 5628(%rsp)
	movl	$1, %esi
	xorl	%edx, %eax
	movl	%eax, %edx
	sall	$7, %edx
	andl	$-1658038656, %edx
	xorl	%edx, %eax
	movl	%eax, %edx
	sall	$15, %edx
	andl	$-272236544, %edx
	xorl	%edx, %eax
	movl	%eax, %edx
	shrl	$18, %edx
	xorl	%edx, %eax
	xorl	%edx, %edx
	cmpl	$-1119, %eax
	setnb	%dl
	imull	$-1119, %edx, %edx
	subl	%edx, %eax
	movl	%eax, (%r10)
	jmp	.L1056
.L1129:
	vmovsd	.LC0(%rip), %xmm8
	vmovsd	.LC17(%rip), %xmm7
	vxorps	%xmm6, %xmm6, %xmm6
	movl	$5, %esi
	movl	$4294966176, %r12d
.L1068:
	movl	$0, 60(%rsp)
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	xorl	%edx, %edx
	movq	%rax, %rdi
	jmp	.L1063
	.p2align 6
	.p2align 4
	.p2align 3
.L1132:
	addl	%r8d, %eax
.L1128:
	incq	%rdx
	xorl	%eax, 60(%rsp)
	movl	%eax, (%r9)
	cmpq	$10000000, %rdx
	je	.L1131
.L1063:
	movzbl	%dl, %eax
	movl	1088(%rsp,%rax,4), %ecx
	movl	64(%rsp,%rax,4), %r10d
	leaq	0(%rbp,%rax,4), %r9
	movq	%rcx, %r8
	addq	%r10, %rcx
	movq	%r10, %rax
	cmpq	%rcx, %r12
	jnb	.L1132
	leal	1119(%r10,%r8), %eax
	jmp	.L1128
.L1131:
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	subq	%rdi, %rax
	js	.L1064
	vcvtsi2sdq	%rax, %xmm6, %xmm0
.L1065:
	vdivsd	%xmm7, %xmm0, %xmm0
	decl	%esi
	movl	60(%rsp), %eax
	vminsd	%xmm8, %xmm0, %xmm2
	vmovapd	%xmm2, %xmm8
	jne	.L1068
	movq	%rbx, %rdx
	leaq	.LC18(%rip), %rcx
	vmovq	%xmm2, %r8
	movl	$5, %esi
	call	__mingw_printf
	vmovsd	.LC0(%rip), %xmm8
.L1077:
	movl	$0, 56(%rsp)
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	xorl	%edx, %edx
	movq	%rax, %rdi
	.p2align 6
	.p2align 4
	.p2align 3
.L1072:
	movzbl	%dl, %eax
	movl	1088(%rsp,%rax,4), %ecx
	leaq	0(%rbp,%rax,4), %r8
	movl	64(%rsp,%rax,4), %eax
	cmpl	%ecx, %eax
	jnb	.L1069
	subl	$1119, %eax
.L1069:
	subl	%ecx, %eax
	incq	%rdx
	xorl	%eax, 56(%rsp)
	movl	%eax, (%r8)
	cmpq	$10000000, %rdx
	jne	.L1072
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	subq	%rdi, %rax
	js	.L1073
	vcvtsi2sdq	%rax, %xmm6, %xmm0
.L1074:
	vdivsd	%xmm7, %xmm0, %xmm0
	decl	%esi
	movl	56(%rsp), %eax
	vminsd	%xmm8, %xmm0, %xmm2
	vmovapd	%xmm2, %xmm8
	jne	.L1077
	movq	%rbx, %rdx
	leaq	.LC19(%rip), %rcx
	vmovq	%xmm2, %r8
	movl	$5, %esi
	call	__mingw_printf
	vmovsd	.LC0(%rip), %xmm8
	movl	$4294966177, %r13d
	movl	$4294966176, %r12d
.L1084:
	movl	$0, 52(%rsp)
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	xorl	%edx, %edx
	movq	%rax, %rdi
	.p2align 4
	.p2align 3
.L1079:
	movzbl	%dl, %r8d
	xorl	%r9d, %r9d
	movl	1088(%rsp,%r8,4), %eax
	leaq	0(%rbp,%r8,4), %rcx
	movl	64(%rsp,%r8,4), %r8d
	imulq	%r8, %rax
	imull	$-383821921, %eax, %r10d
	movq	%rax, %r8
	imulq	%r13, %r10
	addq	%r10, %r8
	adcq	$0, %r9
	shrdq	$32, %r9, %r8
	movl	%r8d, %eax
	cmpq	%r8, %r12
	jnb	.L1078
	addl	$1119, %eax
.L1078:
	incq	%rdx
	xorl	%eax, 52(%rsp)
	movl	%eax, (%rcx)
	cmpq	$10000000, %rdx
	jne	.L1079
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	subq	%rdi, %rax
	js	.L1080
	vcvtsi2sdq	%rax, %xmm6, %xmm0
.L1081:
	vdivsd	%xmm7, %xmm0, %xmm0
	decl	%esi
	movl	52(%rsp), %eax
	vminsd	%xmm8, %xmm0, %xmm2
	vmovapd	%xmm2, %xmm8
	jne	.L1084
	movq	%rbx, %rdx
	leaq	.LC20(%rip), %rcx
	vmovq	%xmm2, %r8
	movl	$5, %esi
	call	__mingw_printf
	vmovsd	.LC0(%rip), %xmm8
	movl	$4294966177, %r13d
	movl	$4294966176, %r12d
.L1091:
	movl	$0, 48(%rsp)
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	xorl	%edx, %edx
	movq	%rax, %rdi
	.p2align 4
	.p2align 3
.L1086:
	movzbl	%dl, %eax
	xorl	%r9d, %r9d
	leaq	0(%rbp,%rax,4), %rcx
	movl	64(%rsp,%rax,4), %eax
	imulq	%rax, %rax
	imull	$-383821921, %eax, %r10d
	movq	%rax, %r8
	imulq	%r13, %r10
	addq	%r10, %r8
	adcq	$0, %r9
	shrdq	$32, %r9, %r8
	movl	%r8d, %eax
	cmpq	%r8, %r12
	jnb	.L1085
	addl	$1119, %eax
.L1085:
	incq	%rdx
	xorl	%eax, 48(%rsp)
	movl	%eax, (%rcx)
	cmpq	$10000000, %rdx
	jne	.L1086
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	subq	%rdi, %rax
	js	.L1087
	vcvtsi2sdq	%rax, %xmm6, %xmm0
.L1088:
	vdivsd	%xmm7, %xmm0, %xmm0
	decl	%esi
	movl	48(%rsp), %eax
	vminsd	%xmm8, %xmm0, %xmm2
	vmovapd	%xmm2, %xmm8
	jne	.L1091
	movq	%rbx, %rdx
	leaq	.LC21(%rip), %rcx
	vmovq	%xmm2, %r8
	movl	$3, %esi
	call	__mingw_printf
	vmovsd	.LC0(%rip), %xmm7
	movl	$4294966177, %r12d
	vmovsd	.LC22(%rip), %xmm8
.L1101:
	movl	$0, 44(%rsp)
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	movl	$4294966176, %r13d
	xorl	%r10d, %r10d
	movq	%rax, %rdi
	.p2align 4
	.p2align 3
.L1096:
	movzbl	%r10b, %eax
	xorl	%edx, %edx
	leaq	0(%rbp,%rax,4), %r11
	movl	64(%rsp,%rax,4), %eax
	imull	$-383821921, %eax, %ecx
	imulq	%r12, %rcx
	addq	%rcx, %rax
	adcq	$0, %rdx
	shrdq	$32, %rdx, %rax
	cmpq	%r12, %rax
	je	.L1092
	movq	%rax, %rcx
	xorl	%r9d, %r9d
	movl	$1, %r8d
	movq	%r12, %rax
	testq	%rcx, %rcx
	jne	.L1093
	jmp	.L1092
	.p2align 5
	.p2align 4
	.p2align 3
.L1103:
	movq	%r14, %r8
.L1093:
	cqto
	movq	%r9, %r14
	movq	%r8, %r9
	idivq	%rcx
	imulq	%r8, %rax
	subq	%rax, %r14
	movq	%rcx, %rax
	movq	%rdx, %rcx
	testq	%rdx, %rdx
	jne	.L1103
	cmpq	$1, %rax
	jg	.L1092
	testq	%r8, %r8
	leaq	(%r8,%r12), %rax
	cmovs	%rax, %r8
	xorl	%edx, %edx
	movl	%r8d, %eax
	imulq	$1252161, %rax, %rax
	imull	$-383821921, %eax, %ecx
	imulq	%r12, %rcx
	addq	%rcx, %rax
	adcq	$0, %rdx
	shrdq	$32, %rdx, %rax
	movl	%eax, %ecx
	cmpq	%rax, %r13
	jnb	.L1094
	addl	$1119, %ecx
.L1094:
	incq	%r10
	xorl	%ecx, 44(%rsp)
	movl	%ecx, (%r11)
	cmpq	$250000, %r10
	jne	.L1096
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	subq	%rdi, %rax
	js	.L1097
	vcvtsi2sdq	%rax, %xmm6, %xmm0
.L1098:
	vdivsd	%xmm8, %xmm0, %xmm0
	decl	%esi
	movl	44(%rsp), %eax
	vminsd	%xmm7, %xmm0, %xmm2
	vmovapd	%xmm2, %xmm7
	jne	.L1101
	vmovaps	5648(%rsp), %xmm6
	vmovaps	5664(%rsp), %xmm7
	movq	%rbx, %rdx
	leaq	.LC23(%rip), %rcx
	vmovaps	5680(%rsp), %xmm8
	vmovaps	5696(%rsp), %xmm9
	vmovq	%xmm2, %r8
	vmovaps	5712(%rsp), %xmm10
	addq	$5728, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r12
	popq	%r13
	popq	%r14
	jmp	__mingw_printf
	.p2align 4
	.p2align 3
.L1092:
	xorl	%ecx, %ecx
	jmp	.L1094
.L1097:
	movq	%rax, %rdx
	andl	$1, %eax
	shrq	%rdx
	orq	%rax, %rdx
	vcvtsi2sdq	%rdx, %xmm6, %xmm0
	vaddsd	%xmm0, %xmm0, %xmm0
	jmp	.L1098
.L1087:
	movq	%rax, %rdx
	andl	$1, %eax
	shrq	%rdx
	orq	%rax, %rdx
	vcvtsi2sdq	%rdx, %xmm6, %xmm0
	vaddsd	%xmm0, %xmm0, %xmm0
	jmp	.L1088
.L1080:
	movq	%rax, %rdx
	andl	$1, %eax
	shrq	%rdx
	orq	%rax, %rdx
	vcvtsi2sdq	%rdx, %xmm6, %xmm0
	vaddsd	%xmm0, %xmm0, %xmm0
	jmp	.L1081
.L1073:
	movq	%rax, %rdx
	andl	$1, %eax
	shrq	%rdx
	orq	%rax, %rdx
	vcvtsi2sdq	%rdx, %xmm6, %xmm0
	vaddsd	%xmm0, %xmm0, %xmm0
	jmp	.L1074
.L1064:
	movq	%rax, %rdx
	andl	$1, %eax
	shrq	%rdx
	orq	%rax, %rdx
	vcvtsi2sdq	%rdx, %xmm6, %xmm0
	vaddsd	%xmm0, %xmm0, %xmm0
	jmp	.L1065
	.seh_endproc
	.section	.text$_Z11bench_fieldIN2fp7FpNaiveILj4294966177EEEEvPKc,"x"
	.linkonce discard
	.p2align 4
	.globl	_Z11bench_fieldIN2fp7FpNaiveILj4294966177EEEEvPKc
	.def	_Z11bench_fieldIN2fp7FpNaiveILj4294966177EEEEvPKc;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z11bench_fieldIN2fp7FpNaiveILj4294966177EEEEvPKc
_Z11bench_fieldIN2fp7FpNaiveILj4294966177EEEEvPKc:
.LFB4554:
	pushq	%r13
	.seh_pushreg	%r13
	movl	$5736, %eax
	pushq	%r12
	.seh_pushreg	%r12
	pushq	%rbp
	.seh_pushreg	%rbp
	pushq	%rdi
	.seh_pushreg	%rdi
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	call	___chkstk_ms
	subq	%rax, %rsp
	.seh_stackalloc	5736
	vmovaps	%xmm6, 5648(%rsp)
	.seh_savexmm	%xmm6, 5648
	vmovaps	%xmm7, 5664(%rsp)
	.seh_savexmm	%xmm7, 5664
	vmovaps	%xmm8, 5680(%rsp)
	.seh_savexmm	%xmm8, 5680
	vmovaps	%xmm9, 5696(%rsp)
	.seh_savexmm	%xmm9, 5696
	vmovaps	%xmm10, 5712(%rsp)
	.seh_savexmm	%xmm10, 5712
	.seh_endprologue
	movl	$1, %edx
	movq	%rcx, %rbx
	movl	$42, 3136(%rsp)
	leaq	3140(%rsp), %r8
	movl	$42, %ecx
	.p2align 6
	.p2align 4
	.p2align 3
.L1134:
	movl	%ecx, %eax
	addq	$4, %r8
	shrl	$30, %eax
	xorl	%ecx, %eax
	imull	$1812433253, %eax, %eax
	leal	(%rax,%rdx), %ecx
	incq	%rdx
	movl	%ecx, -4(%r8)
	cmpq	$624, %rdx
	jne	.L1134
	leaq	2112(%rsp), %r9
	vpcmpeqd	%xmm5, %xmm5, %xmm5
	movl	$-1727483681, %eax
	leaq	1088(%rsp), %r8
	vmovd	%eax, %xmm2
	leaq	64(%rsp), %r10
	movq	%r9, %rsi
	movq	%r9, %r11
	leaq	4032(%rsp), %rcx
	vpbroadcastd	%xmm2, %xmm2
	vpsrld	$1, %xmm5, %xmm4
	vpslld	$31, %xmm5, %xmm3
	vmovq	.LC13(%rip), %xmm10
	vmovq	.LC14(%rip), %xmm9
	vmovq	.LC15(%rip), %xmm8
	vmovq	.LC16(%rip), %xmm7
	jmp	.L1139
	.p2align 4
	.p2align 3
.L1210:
	movl	3136(%rsp,%rdx,4), %ebp
	leaq	1(%rdx), %rdi
	movl	%ebp, %eax
	shrl	$11, %eax
	xorl	%ebp, %eax
	movl	%eax, %edx
	sall	$7, %edx
	andl	$-1658038656, %edx
	xorl	%edx, %eax
	movl	%eax, %edx
	sall	$15, %edx
	andl	$-272236544, %edx
	xorl	%edx, %eax
	movl	%eax, %edx
	shrl	$18, %edx
	xorl	%edx, %eax
	xorl	%edx, %edx
	cmpl	$-1119, %eax
	setnb	%dl
	imull	$-1119, %edx, %edx
	subl	%edx, %eax
	movl	%eax, (%r10)
.L1136:
	movl	3136(%rsp,%rdi,4), %eax
	leaq	1(%rdi), %rdx
	movl	$0, (%r9)
	movl	%eax, %edi
	shrl	$11, %edi
	xorl	%edi, %eax
	movl	%eax, %edi
	sall	$7, %edi
	andl	$-1658038656, %edi
	xorl	%edi, %eax
	movl	%eax, %edi
	sall	$15, %edi
	andl	$-272236544, %edi
	xorl	%edi, %eax
	movl	%eax, %edi
	shrl	$18, %edi
	xorl	%edi, %eax
	xorl	%edi, %edi
	cmpl	$-1119, %eax
	setnb	%dil
	addq	$4, %r8
	addq	$4, %r9
	addq	$4, %r10
	imull	$-1119, %edi, %edi
	subl	%edi, %eax
	movl	%eax, -4(%r8)
	cmpq	%r11, %r8
	je	.L1209
.L1139:
	cmpq	$623, %rdx
	jbe	.L1210
	leaq	3136(%rsp), %rax
	vpsrld	$31, %xmm5, %xmm6
	.p2align 6
	.p2align 4
	.p2align 3
.L1137:
	vpand	(%rax), %xmm3, %xmm1
	vpand	4(%rax), %xmm4, %xmm0
	addq	$16, %rax
	vpor	%xmm1, %xmm0, %xmm0
	vpsrld	$1, %xmm0, %xmm1
	vpxor	1572(%rax), %xmm1, %xmm1
	vpand	%xmm6, %xmm0, %xmm0
	vpmulld	%xmm2, %xmm0, %xmm0
	vpxor	%xmm0, %xmm1, %xmm0
	vmovdqa	%xmm0, -16(%rax)
	cmpq	%rax, %rcx
	jne	.L1137
	movl	4040(%rsp), %edx
	movl	4044(%rsp), %eax
	vmovq	4036(%rsp), %xmm1
	vmovq	4032(%rsp), %xmm0
	vpand	%xmm9, %xmm1, %xmm1
	vpand	%xmm10, %xmm0, %xmm0
	vpor	%xmm1, %xmm0, %xmm0
	vmovq	5620(%rsp), %xmm1
	vpsrld	$1, %xmm0, %xmm6
	vpand	%xmm8, %xmm0, %xmm0
	vpxor	%xmm6, %xmm1, %xmm1
	vpsrld	$31, %xmm5, %xmm6
	andl	$-2147483648, %edx
	andl	$2147483647, %eax
	vpmulld	%xmm7, %xmm0, %xmm0
	orl	%edx, %eax
	movl	%eax, %edx
	andl	$1, %eax
	shrl	%edx
	xorl	5628(%rsp), %edx
	negl	%eax
	vpxor	%xmm0, %xmm1, %xmm1
	andl	$-1727483681, %eax
	vmovq	%xmm1, 4032(%rsp)
	xorl	%edx, %eax
	leaq	5628(%rsp), %rdx
	movl	%eax, 4040(%rsp)
	leaq	4044(%rsp), %rax
	.p2align 6
	.p2align 4
	.p2align 3
.L1138:
	vpand	(%rax), %xmm3, %xmm1
	addq	$16, %rax
	vpand	-12(%rax), %xmm4, %xmm0
	vpor	%xmm1, %xmm0, %xmm0
	vpsrld	$1, %xmm0, %xmm1
	vpxor	-924(%rax), %xmm1, %xmm1
	vpand	%xmm6, %xmm0, %xmm0
	vpmulld	%xmm2, %xmm0, %xmm0
	vpxor	%xmm0, %xmm1, %xmm0
	vmovdqu	%xmm0, -16(%rax)
	cmpq	%rdx, %rax
	jne	.L1138
	movl	3136(%rsp), %edi
	movl	5628(%rsp), %eax
	movl	%edi, %edx
	andl	$-2147483648, %eax
	andl	$2147483647, %edx
	orl	%edx, %eax
	movl	%eax, %edx
	andl	$1, %eax
	shrl	%edx
	xorl	4720(%rsp), %edx
	negl	%eax
	andl	$-1727483681, %eax
	xorl	%eax, %edx
	movl	%edx, 5628(%rsp)
	movl	%edi, %edx
	shrl	$11, %edx
	xorl	%edi, %edx
	movl	$1, %edi
	movl	%edx, %eax
	sall	$7, %eax
	andl	$-1658038656, %eax
	xorl	%edx, %eax
	movl	%eax, %edx
	sall	$15, %edx
	andl	$-272236544, %edx
	xorl	%eax, %edx
	movl	%edx, %eax
	shrl	$18, %eax
	xorl	%edx, %eax
	xorl	%edx, %edx
	cmpl	$-1119, %eax
	setnb	%dl
	imull	$-1119, %edx, %edx
	subl	%edx, %eax
	movl	%eax, (%r10)
	jmp	.L1136
.L1209:
	vmovsd	.LC0(%rip), %xmm8
	vmovsd	.LC17(%rip), %xmm7
	vxorps	%xmm6, %xmm6, %xmm6
	movl	$5, %edi
	movl	$4294966176, %r12d
.L1148:
	movl	$0, 60(%rsp)
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	xorl	%edx, %edx
	movq	%rax, %rbp
	jmp	.L1143
	.p2align 6
	.p2align 4
	.p2align 3
.L1212:
	addl	%r8d, %eax
.L1208:
	incq	%rdx
	xorl	%eax, 60(%rsp)
	movl	%eax, (%r9)
	cmpq	$10000000, %rdx
	je	.L1211
.L1143:
	movzbl	%dl, %eax
	movl	1088(%rsp,%rax,4), %ecx
	movl	64(%rsp,%rax,4), %r10d
	leaq	(%rsi,%rax,4), %r9
	movq	%rcx, %r8
	addq	%r10, %rcx
	movq	%r10, %rax
	cmpq	%rcx, %r12
	jnb	.L1212
	leal	1119(%r10,%r8), %eax
	jmp	.L1208
.L1211:
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	subq	%rbp, %rax
	js	.L1144
	vcvtsi2sdq	%rax, %xmm6, %xmm0
.L1145:
	vdivsd	%xmm7, %xmm0, %xmm0
	decl	%edi
	movl	60(%rsp), %eax
	vminsd	%xmm8, %xmm0, %xmm2
	vmovapd	%xmm2, %xmm8
	jne	.L1148
	movq	%rbx, %rdx
	leaq	.LC18(%rip), %rcx
	vmovq	%xmm2, %r8
	movl	$5, %edi
	call	__mingw_printf
	vmovsd	.LC0(%rip), %xmm8
.L1157:
	movl	$0, 56(%rsp)
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	xorl	%edx, %edx
	movq	%rax, %rbp
	.p2align 6
	.p2align 4
	.p2align 3
.L1152:
	movzbl	%dl, %eax
	movl	1088(%rsp,%rax,4), %ecx
	leaq	(%rsi,%rax,4), %r8
	movl	64(%rsp,%rax,4), %eax
	cmpl	%ecx, %eax
	jnb	.L1149
	subl	$1119, %eax
.L1149:
	subl	%ecx, %eax
	incq	%rdx
	xorl	%eax, 56(%rsp)
	movl	%eax, (%r8)
	cmpq	$10000000, %rdx
	jne	.L1152
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	subq	%rbp, %rax
	js	.L1153
	vcvtsi2sdq	%rax, %xmm6, %xmm0
.L1154:
	vdivsd	%xmm7, %xmm0, %xmm0
	decl	%edi
	movl	56(%rsp), %eax
	vminsd	%xmm8, %xmm0, %xmm2
	vmovapd	%xmm2, %xmm8
	jne	.L1157
	movq	%rbx, %rdx
	leaq	.LC19(%rip), %rcx
	vmovq	%xmm2, %r8
	movl	$5, %edi
	call	__mingw_printf
	vmovsd	.LC0(%rip), %xmm8
	movabsq	$-9223369633819947615, %r13
	movl	$4294966177, %r12d
.L1163:
	movl	$0, 52(%rsp)
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	xorl	%r8d, %r8d
	movq	%rax, %rbp
	.p2align 6
	.p2align 4
	.p2align 3
.L1158:
	movzbl	%r8b, %r9d
	incq	%r8
	movl	1088(%rsp,%r9,4), %eax
	movl	64(%rsp,%r9,4), %ecx
	imulq	%rax, %rcx
	movq	%rcx, %rax
	mulq	%r13
	shrq	$31, %rdx
	imulq	%r12, %rdx
	subq	%rdx, %rcx
	xorl	%ecx, 52(%rsp)
	movl	%ecx, 2112(%rsp,%r9,4)
	cmpq	$10000000, %r8
	jne	.L1158
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	subq	%rbp, %rax
	js	.L1159
	vcvtsi2sdq	%rax, %xmm6, %xmm0
.L1160:
	vdivsd	%xmm7, %xmm0, %xmm0
	decl	%edi
	movl	52(%rsp), %eax
	vminsd	%xmm8, %xmm0, %xmm2
	vmovapd	%xmm2, %xmm8
	jne	.L1163
	movq	%rbx, %rdx
	leaq	.LC20(%rip), %rcx
	vmovq	%xmm2, %r8
	movl	$5, %edi
	call	__mingw_printf
	vmovsd	.LC0(%rip), %xmm8
	movabsq	$-9223369633819947615, %r13
	movl	$4294966177, %r12d
.L1169:
	movl	$0, 48(%rsp)
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	xorl	%r8d, %r8d
	movq	%rax, %rbp
	.p2align 6
	.p2align 4
	.p2align 3
.L1164:
	movzbl	%r8b, %r9d
	incq	%r8
	movl	64(%rsp,%r9,4), %ecx
	imulq	%rcx, %rcx
	movq	%rcx, %rax
	mulq	%r13
	shrq	$31, %rdx
	imulq	%r12, %rdx
	subq	%rdx, %rcx
	xorl	%ecx, 48(%rsp)
	movl	%ecx, 2112(%rsp,%r9,4)
	cmpq	$10000000, %r8
	jne	.L1164
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	subq	%rbp, %rax
	js	.L1165
	vcvtsi2sdq	%rax, %xmm6, %xmm0
.L1166:
	vdivsd	%xmm7, %xmm0, %xmm0
	decl	%edi
	movl	48(%rsp), %eax
	vminsd	%xmm8, %xmm0, %xmm2
	vmovapd	%xmm2, %xmm8
	jne	.L1169
	movq	%rbx, %rdx
	leaq	.LC21(%rip), %rcx
	vmovq	%xmm2, %r8
	movl	$3, %edi
	call	__mingw_printf
	vmovsd	.LC0(%rip), %xmm7
	movl	$4294966177, %r12d
	vmovsd	.LC22(%rip), %xmm8
.L1180:
	movl	$0, 44(%rsp)
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	xorl	%r10d, %r10d
	movq	%rax, %rbp
	.p2align 4
	.p2align 3
.L1175:
	movzbl	%r10b, %eax
	movl	64(%rsp,%rax,4), %ecx
	leaq	(%rsi,%rax,4), %r11
	testq	%rcx, %rcx
	je	.L1170
	xorl	%r9d, %r9d
	movl	$1, %r8d
	movq	%r12, %rax
	jmp	.L1171
	.p2align 5
	.p2align 4
	.p2align 3
.L1181:
	movq	%r13, %r8
.L1171:
	cqto
	idivq	%rcx
	imulq	%r8, %rax
	subq	%rax, %r9
	movq	%rcx, %rax
	movq	%rdx, %rcx
	movq	%r9, %r13
	movq	%r8, %r9
	testq	%rdx, %rdx
	jne	.L1181
	cmpq	$1, %rax
	jg	.L1170
	leaq	(%r8,%r12), %rax
	testq	%r8, %r8
	cmovns	%r8, %rax
.L1173:
	incq	%r10
	xorl	%eax, 44(%rsp)
	movl	%eax, (%r11)
	cmpq	$250000, %r10
	jne	.L1175
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	subq	%rbp, %rax
	js	.L1176
	vcvtsi2sdq	%rax, %xmm6, %xmm0
.L1177:
	vdivsd	%xmm8, %xmm0, %xmm0
	decl	%edi
	movl	44(%rsp), %eax
	vminsd	%xmm7, %xmm0, %xmm2
	vmovapd	%xmm2, %xmm7
	jne	.L1180
	vmovaps	5648(%rsp), %xmm6
	vmovaps	5664(%rsp), %xmm7
	movq	%rbx, %rdx
	leaq	.LC23(%rip), %rcx
	vmovaps	5680(%rsp), %xmm8
	vmovaps	5696(%rsp), %xmm9
	vmovq	%xmm2, %r8
	vmovaps	5712(%rsp), %xmm10
	addq	$5736, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r12
	popq	%r13
	jmp	__mingw_printf
.L1170:
	xorl	%eax, %eax
	jmp	.L1173
.L1176:
	movq	%rax, %rdx
	andl	$1, %eax
	shrq	%rdx
	orq	%rax, %rdx
	vcvtsi2sdq	%rdx, %xmm6, %xmm0
	vaddsd	%xmm0, %xmm0, %xmm0
	jmp	.L1177
.L1165:
	movq	%rax, %rdx
	andl	$1, %eax
	shrq	%rdx
	orq	%rax, %rdx
	vcvtsi2sdq	%rdx, %xmm6, %xmm0
	vaddsd	%xmm0, %xmm0, %xmm0
	jmp	.L1166
.L1159:
	movq	%rax, %rdx
	andl	$1, %eax
	shrq	%rdx
	orq	%rax, %rdx
	vcvtsi2sdq	%rdx, %xmm6, %xmm0
	vaddsd	%xmm0, %xmm0, %xmm0
	jmp	.L1160
.L1153:
	movq	%rax, %rdx
	andl	$1, %eax
	shrq	%rdx
	orq	%rax, %rdx
	vcvtsi2sdq	%rdx, %xmm6, %xmm0
	vaddsd	%xmm0, %xmm0, %xmm0
	jmp	.L1154
.L1144:
	movq	%rax, %rdx
	andl	$1, %eax
	shrq	%rdx
	orq	%rax, %rdx
	vcvtsi2sdq	%rdx, %xmm6, %xmm0
	vaddsd	%xmm0, %xmm0, %xmm0
	jmp	.L1145
	.seh_endproc
	.section	.text$_Z11bench_fieldIN2fp9FpBarrettILj4294966177EEEEvPKc,"x"
	.linkonce discard
	.p2align 4
	.globl	_Z11bench_fieldIN2fp9FpBarrettILj4294966177EEEEvPKc
	.def	_Z11bench_fieldIN2fp9FpBarrettILj4294966177EEEEvPKc;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z11bench_fieldIN2fp9FpBarrettILj4294966177EEEEvPKc
_Z11bench_fieldIN2fp9FpBarrettILj4294966177EEEEvPKc:
.LFB4570:
	pushq	%r13
	.seh_pushreg	%r13
	movl	$5736, %eax
	pushq	%r12
	.seh_pushreg	%r12
	pushq	%rbp
	.seh_pushreg	%rbp
	pushq	%rdi
	.seh_pushreg	%rdi
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	call	___chkstk_ms
	subq	%rax, %rsp
	.seh_stackalloc	5736
	vmovaps	%xmm6, 5648(%rsp)
	.seh_savexmm	%xmm6, 5648
	vmovaps	%xmm7, 5664(%rsp)
	.seh_savexmm	%xmm7, 5664
	vmovaps	%xmm8, 5680(%rsp)
	.seh_savexmm	%xmm8, 5680
	vmovaps	%xmm9, 5696(%rsp)
	.seh_savexmm	%xmm9, 5696
	vmovaps	%xmm10, 5712(%rsp)
	.seh_savexmm	%xmm10, 5712
	.seh_endprologue
	movl	$1, %edx
	movq	%rcx, %rbx
	movl	$42, 3136(%rsp)
	leaq	3140(%rsp), %r8
	movl	$42, %ecx
	.p2align 6
	.p2align 4
	.p2align 3
.L1214:
	movl	%ecx, %eax
	addq	$4, %r8
	shrl	$30, %eax
	xorl	%ecx, %eax
	imull	$1812433253, %eax, %eax
	leal	(%rax,%rdx), %ecx
	incq	%rdx
	movl	%ecx, -4(%r8)
	cmpq	$624, %rdx
	jne	.L1214
	leaq	2112(%rsp), %r9
	vpcmpeqd	%xmm5, %xmm5, %xmm5
	movl	$-1727483681, %eax
	leaq	1088(%rsp), %r8
	vmovd	%eax, %xmm2
	leaq	64(%rsp), %r10
	movq	%r9, %rsi
	movq	%r9, %r11
	leaq	4032(%rsp), %rcx
	vpbroadcastd	%xmm2, %xmm2
	vpsrld	$1, %xmm5, %xmm4
	vpslld	$31, %xmm5, %xmm3
	vmovq	.LC13(%rip), %xmm10
	vmovq	.LC14(%rip), %xmm9
	vmovq	.LC15(%rip), %xmm8
	vmovq	.LC16(%rip), %xmm7
	jmp	.L1219
	.p2align 4
	.p2align 3
.L1294:
	movl	3136(%rsp,%rdx,4), %ebp
	leaq	1(%rdx), %rdi
	movl	%ebp, %eax
	shrl	$11, %eax
	xorl	%ebp, %eax
	movl	%eax, %edx
	sall	$7, %edx
	andl	$-1658038656, %edx
	xorl	%edx, %eax
	movl	%eax, %edx
	sall	$15, %edx
	andl	$-272236544, %edx
	xorl	%edx, %eax
	movl	%eax, %edx
	shrl	$18, %edx
	xorl	%edx, %eax
	xorl	%edx, %edx
	cmpl	$-1119, %eax
	setnb	%dl
	imull	$-1119, %edx, %edx
	subl	%edx, %eax
	movl	%eax, (%r10)
.L1216:
	movl	3136(%rsp,%rdi,4), %eax
	leaq	1(%rdi), %rdx
	movl	$0, (%r9)
	movl	%eax, %edi
	shrl	$11, %edi
	xorl	%edi, %eax
	movl	%eax, %edi
	sall	$7, %edi
	andl	$-1658038656, %edi
	xorl	%edi, %eax
	movl	%eax, %edi
	sall	$15, %edi
	andl	$-272236544, %edi
	xorl	%edi, %eax
	movl	%eax, %edi
	shrl	$18, %edi
	xorl	%edi, %eax
	xorl	%edi, %edi
	cmpl	$-1119, %eax
	setnb	%dil
	addq	$4, %r8
	addq	$4, %r9
	addq	$4, %r10
	imull	$-1119, %edi, %edi
	subl	%edi, %eax
	movl	%eax, -4(%r8)
	cmpq	%r8, %r11
	je	.L1293
.L1219:
	cmpq	$623, %rdx
	jbe	.L1294
	leaq	3136(%rsp), %rax
	vpsrld	$31, %xmm5, %xmm6
	.p2align 6
	.p2align 4
	.p2align 3
.L1217:
	vpand	(%rax), %xmm3, %xmm1
	vpand	4(%rax), %xmm4, %xmm0
	addq	$16, %rax
	vpor	%xmm1, %xmm0, %xmm0
	vpsrld	$1, %xmm0, %xmm1
	vpxor	1572(%rax), %xmm1, %xmm1
	vpand	%xmm6, %xmm0, %xmm0
	vpmulld	%xmm2, %xmm0, %xmm0
	vpxor	%xmm0, %xmm1, %xmm0
	vmovdqa	%xmm0, -16(%rax)
	cmpq	%rcx, %rax
	jne	.L1217
	movl	4040(%rsp), %edx
	movl	4044(%rsp), %eax
	vmovq	4036(%rsp), %xmm1
	vmovq	4032(%rsp), %xmm0
	vpand	%xmm9, %xmm1, %xmm1
	vpand	%xmm10, %xmm0, %xmm0
	vpor	%xmm1, %xmm0, %xmm0
	vmovq	5620(%rsp), %xmm1
	vpsrld	$1, %xmm0, %xmm6
	vpand	%xmm8, %xmm0, %xmm0
	vpxor	%xmm6, %xmm1, %xmm1
	vpsrld	$31, %xmm5, %xmm6
	andl	$-2147483648, %edx
	andl	$2147483647, %eax
	vpmulld	%xmm7, %xmm0, %xmm0
	orl	%edx, %eax
	movl	%eax, %edx
	andl	$1, %eax
	shrl	%edx
	xorl	5628(%rsp), %edx
	negl	%eax
	vpxor	%xmm0, %xmm1, %xmm1
	andl	$-1727483681, %eax
	vmovq	%xmm1, 4032(%rsp)
	xorl	%edx, %eax
	leaq	5628(%rsp), %rdx
	movl	%eax, 4040(%rsp)
	leaq	4044(%rsp), %rax
	.p2align 6
	.p2align 4
	.p2align 3
.L1218:
	vpand	(%rax), %xmm3, %xmm1
	addq	$16, %rax
	vpand	-12(%rax), %xmm4, %xmm0
	vpor	%xmm1, %xmm0, %xmm0
	vpsrld	$1, %xmm0, %xmm1
	vpxor	-924(%rax), %xmm1, %xmm1
	vpand	%xmm6, %xmm0, %xmm0
	vpmulld	%xmm2, %xmm0, %xmm0
	vpxor	%xmm0, %xmm1, %xmm0
	vmovdqu	%xmm0, -16(%rax)
	cmpq	%rdx, %rax
	jne	.L1218
	movl	3136(%rsp), %edi
	movl	5628(%rsp), %eax
	movl	%edi, %edx
	andl	$-2147483648, %eax
	andl	$2147483647, %edx
	orl	%edx, %eax
	movl	%eax, %edx
	andl	$1, %eax
	shrl	%edx
	xorl	4720(%rsp), %edx
	negl	%eax
	andl	$-1727483681, %eax
	xorl	%eax, %edx
	movl	%edx, 5628(%rsp)
	movl	%edi, %edx
	shrl	$11, %edx
	xorl	%edi, %edx
	movl	$1, %edi
	movl	%edx, %eax
	sall	$7, %eax
	andl	$-1658038656, %eax
	xorl	%edx, %eax
	movl	%eax, %edx
	sall	$15, %edx
	andl	$-272236544, %edx
	xorl	%eax, %edx
	movl	%edx, %eax
	shrl	$18, %eax
	xorl	%edx, %eax
	xorl	%edx, %edx
	cmpl	$-1119, %eax
	setnb	%dl
	imull	$-1119, %edx, %edx
	subl	%edx, %eax
	movl	%eax, (%r10)
	jmp	.L1216
.L1293:
	vmovsd	.LC0(%rip), %xmm8
	vmovsd	.LC17(%rip), %xmm7
	vxorps	%xmm6, %xmm6, %xmm6
	movl	$5, %edi
	movl	$4294966176, %r12d
.L1228:
	movl	$0, 60(%rsp)
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	xorl	%edx, %edx
	movq	%rax, %rbp
	jmp	.L1223
	.p2align 6
	.p2align 4
	.p2align 3
.L1296:
	addl	%r8d, %eax
.L1292:
	incq	%rdx
	xorl	%eax, 60(%rsp)
	movl	%eax, (%r9)
	cmpq	$10000000, %rdx
	je	.L1295
.L1223:
	movzbl	%dl, %eax
	movl	1088(%rsp,%rax,4), %ecx
	movl	64(%rsp,%rax,4), %r10d
	leaq	(%rsi,%rax,4), %r9
	movq	%rcx, %r8
	addq	%r10, %rcx
	movq	%r10, %rax
	cmpq	%rcx, %r12
	jnb	.L1296
	leal	1119(%r10,%r8), %eax
	jmp	.L1292
.L1295:
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	subq	%rbp, %rax
	js	.L1224
	vcvtsi2sdq	%rax, %xmm6, %xmm0
.L1225:
	vdivsd	%xmm7, %xmm0, %xmm0
	decl	%edi
	movl	60(%rsp), %eax
	vminsd	%xmm8, %xmm0, %xmm2
	vmovapd	%xmm2, %xmm8
	jne	.L1228
	movq	%rbx, %rdx
	leaq	.LC18(%rip), %rcx
	vmovq	%xmm2, %r8
	movl	$5, %edi
	call	__mingw_printf
	vmovsd	.LC0(%rip), %xmm8
.L1237:
	movl	$0, 56(%rsp)
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	xorl	%edx, %edx
	movq	%rax, %rbp
	.p2align 6
	.p2align 4
	.p2align 3
.L1232:
	movzbl	%dl, %eax
	movl	1088(%rsp,%rax,4), %ecx
	leaq	(%rsi,%rax,4), %r8
	movl	64(%rsp,%rax,4), %eax
	cmpl	%ecx, %eax
	jnb	.L1229
	subl	$1119, %eax
.L1229:
	subl	%ecx, %eax
	incq	%rdx
	xorl	%eax, 56(%rsp)
	movl	%eax, (%r8)
	cmpq	$10000000, %rdx
	jne	.L1232
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	subq	%rbp, %rax
	js	.L1233
	vcvtsi2sdq	%rax, %xmm6, %xmm0
.L1234:
	vdivsd	%xmm7, %xmm0, %xmm0
	decl	%edi
	movl	56(%rsp), %eax
	vminsd	%xmm8, %xmm0, %xmm2
	vmovapd	%xmm2, %xmm8
	jne	.L1237
	movq	%rbx, %rdx
	leaq	.LC19(%rip), %rcx
	vmovq	%xmm2, %r8
	movl	$5, %edi
	call	__mingw_printf
	vmovsd	.LC0(%rip), %xmm8
	movabsq	$4294968415, %r12
	movabsq	$-8589932354, %r13
.L1244:
	movl	$0, 52(%rsp)
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	xorl	%r8d, %r8d
	movl	$4294966177, %r11d
	movq	%rax, %rbp
	movl	$4294966176, %r9d
	.p2align 4
	.p2align 3
.L1239:
	movzbl	%r8b, %edx
	movl	1088(%rsp,%rdx,4), %eax
	leaq	(%rsi,%rdx,4), %r10
	movl	64(%rsp,%rdx,4), %edx
	imulq	%rdx, %rax
	movq	%rax, %rcx
	mulq	%r12
	movq	%rcx, %rax
	imulq	%r11, %rdx
	subq	%rdx, %rax
	cmpq	%rax, %r9
	jnb	.L1238
	movq	%rax, %rdx
	addq	%r13, %rax
	subq	%r11, %rdx
	cmpq	%rdx, %r9
	cmovnb	%rdx, %rax
.L1238:
	incq	%r8
	xorl	%eax, 52(%rsp)
	movl	%eax, (%r10)
	cmpq	$10000000, %r8
	jne	.L1239
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	subq	%rbp, %rax
	js	.L1240
	vcvtsi2sdq	%rax, %xmm6, %xmm0
.L1241:
	vdivsd	%xmm7, %xmm0, %xmm0
	decl	%edi
	movl	52(%rsp), %eax
	vminsd	%xmm8, %xmm0, %xmm2
	vmovapd	%xmm2, %xmm8
	jne	.L1244
	movq	%rbx, %rdx
	leaq	.LC20(%rip), %rcx
	vmovq	%xmm2, %r8
	movl	$5, %edi
	call	__mingw_printf
	vmovsd	.LC0(%rip), %xmm8
	movabsq	$4294968415, %r12
	movabsq	$-8589932354, %r13
.L1251:
	movl	$0, 48(%rsp)
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	xorl	%r8d, %r8d
	movl	$4294966177, %r11d
	movq	%rax, %rbp
	movl	$4294966176, %r9d
	.p2align 4
	.p2align 3
.L1246:
	movzbl	%r8b, %eax
	leaq	(%rsi,%rax,4), %r10
	movl	64(%rsp,%rax,4), %eax
	imulq	%rax, %rax
	movq	%rax, %rcx
	mulq	%r12
	movq	%rcx, %rax
	imulq	%r11, %rdx
	subq	%rdx, %rax
	cmpq	%rax, %r9
	jnb	.L1245
	movq	%rax, %rdx
	addq	%r13, %rax
	subq	%r11, %rdx
	cmpq	%rdx, %r9
	cmovnb	%rdx, %rax
.L1245:
	incq	%r8
	xorl	%eax, 48(%rsp)
	movl	%eax, (%r10)
	cmpq	$10000000, %r8
	jne	.L1246
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	subq	%rbp, %rax
	js	.L1247
	vcvtsi2sdq	%rax, %xmm6, %xmm0
.L1248:
	vdivsd	%xmm7, %xmm0, %xmm0
	decl	%edi
	movl	48(%rsp), %eax
	vminsd	%xmm8, %xmm0, %xmm2
	vmovapd	%xmm2, %xmm8
	jne	.L1251
	movq	%rbx, %rdx
	leaq	.LC21(%rip), %rcx
	vmovq	%xmm2, %r8
	movl	$3, %edi
	call	__mingw_printf
	vmovsd	.LC0(%rip), %xmm7
	movl	$4294966177, %r12d
	vmovsd	.LC22(%rip), %xmm8
.L1262:
	movl	$0, 44(%rsp)
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	xorl	%r10d, %r10d
	movq	%rax, %rbp
	.p2align 4
	.p2align 3
.L1257:
	movzbl	%r10b, %eax
	movl	64(%rsp,%rax,4), %ecx
	leaq	(%rsi,%rax,4), %r11
	testq	%rcx, %rcx
	je	.L1252
	xorl	%r9d, %r9d
	movl	$1, %r8d
	movq	%r12, %rax
	jmp	.L1253
	.p2align 5
	.p2align 4
	.p2align 3
.L1265:
	movq	%r13, %r8
.L1253:
	cqto
	idivq	%rcx
	imulq	%r8, %rax
	subq	%rax, %r9
	movq	%rcx, %rax
	movq	%rdx, %rcx
	movq	%r9, %r13
	movq	%r8, %r9
	testq	%rdx, %rdx
	jne	.L1265
	cmpq	$1, %rax
	jg	.L1252
	leaq	(%r8,%r12), %rax
	testq	%r8, %r8
	cmovns	%r8, %rax
.L1255:
	incq	%r10
	xorl	%eax, 44(%rsp)
	movl	%eax, (%r11)
	cmpq	$250000, %r10
	jne	.L1257
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	subq	%rbp, %rax
	js	.L1258
	vcvtsi2sdq	%rax, %xmm6, %xmm0
.L1259:
	vdivsd	%xmm8, %xmm0, %xmm0
	decl	%edi
	movl	44(%rsp), %eax
	vminsd	%xmm7, %xmm0, %xmm2
	vmovapd	%xmm2, %xmm7
	jne	.L1262
	vmovaps	5648(%rsp), %xmm6
	vmovaps	5664(%rsp), %xmm7
	movq	%rbx, %rdx
	leaq	.LC23(%rip), %rcx
	vmovaps	5680(%rsp), %xmm8
	vmovaps	5696(%rsp), %xmm9
	vmovq	%xmm2, %r8
	vmovaps	5712(%rsp), %xmm10
	addq	$5736, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r12
	popq	%r13
	jmp	__mingw_printf
.L1252:
	xorl	%eax, %eax
	jmp	.L1255
.L1258:
	movq	%rax, %rdx
	andl	$1, %eax
	shrq	%rdx
	orq	%rax, %rdx
	vcvtsi2sdq	%rdx, %xmm6, %xmm0
	vaddsd	%xmm0, %xmm0, %xmm0
	jmp	.L1259
.L1247:
	movq	%rax, %rdx
	andl	$1, %eax
	shrq	%rdx
	orq	%rax, %rdx
	vcvtsi2sdq	%rdx, %xmm6, %xmm0
	vaddsd	%xmm0, %xmm0, %xmm0
	jmp	.L1248
.L1240:
	movq	%rax, %rdx
	andl	$1, %eax
	shrq	%rdx
	orq	%rax, %rdx
	vcvtsi2sdq	%rdx, %xmm6, %xmm0
	vaddsd	%xmm0, %xmm0, %xmm0
	jmp	.L1241
.L1233:
	movq	%rax, %rdx
	andl	$1, %eax
	shrq	%rdx
	orq	%rax, %rdx
	vcvtsi2sdq	%rdx, %xmm6, %xmm0
	vaddsd	%xmm0, %xmm0, %xmm0
	jmp	.L1234
.L1224:
	movq	%rax, %rdx
	andl	$1, %eax
	shrq	%rdx
	orq	%rax, %rdx
	vcvtsi2sdq	%rdx, %xmm6, %xmm0
	vaddsd	%xmm0, %xmm0, %xmm0
	jmp	.L1225
	.seh_endproc
	.section	.text$_Z11bench_fieldIN2fp8FpPseudoILj4294966177EEEEvPKc,"x"
	.linkonce discard
	.p2align 4
	.globl	_Z11bench_fieldIN2fp8FpPseudoILj4294966177EEEEvPKc
	.def	_Z11bench_fieldIN2fp8FpPseudoILj4294966177EEEEvPKc;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z11bench_fieldIN2fp8FpPseudoILj4294966177EEEEvPKc
_Z11bench_fieldIN2fp8FpPseudoILj4294966177EEEEvPKc:
.LFB4602:
	pushq	%r13
	.seh_pushreg	%r13
	movl	$5736, %eax
	pushq	%r12
	.seh_pushreg	%r12
	pushq	%rbp
	.seh_pushreg	%rbp
	pushq	%rdi
	.seh_pushreg	%rdi
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	call	___chkstk_ms
	subq	%rax, %rsp
	.seh_stackalloc	5736
	vmovaps	%xmm6, 5648(%rsp)
	.seh_savexmm	%xmm6, 5648
	vmovaps	%xmm7, 5664(%rsp)
	.seh_savexmm	%xmm7, 5664
	vmovaps	%xmm8, 5680(%rsp)
	.seh_savexmm	%xmm8, 5680
	vmovaps	%xmm9, 5696(%rsp)
	.seh_savexmm	%xmm9, 5696
	vmovaps	%xmm10, 5712(%rsp)
	.seh_savexmm	%xmm10, 5712
	.seh_endprologue
	movl	$1, %edx
	movq	%rcx, %rbx
	movl	$42, 3136(%rsp)
	leaq	3140(%rsp), %r8
	movl	$42, %ecx
	.p2align 6
	.p2align 4
	.p2align 3
.L1298:
	movl	%ecx, %eax
	addq	$4, %r8
	shrl	$30, %eax
	xorl	%ecx, %eax
	imull	$1812433253, %eax, %eax
	leal	(%rax,%rdx), %ecx
	incq	%rdx
	movl	%ecx, -4(%r8)
	cmpq	$624, %rdx
	jne	.L1298
	leaq	2112(%rsp), %r9
	vpcmpeqd	%xmm5, %xmm5, %xmm5
	movl	$-1727483681, %eax
	leaq	1088(%rsp), %r8
	vmovd	%eax, %xmm2
	leaq	64(%rsp), %r10
	movq	%r9, %rsi
	movq	%r9, %r11
	leaq	4032(%rsp), %rcx
	vpbroadcastd	%xmm2, %xmm2
	vpsrld	$1, %xmm5, %xmm4
	vpslld	$31, %xmm5, %xmm3
	vmovq	.LC14(%rip), %xmm10
	vmovq	.LC13(%rip), %xmm9
	vmovq	.LC15(%rip), %xmm8
	vmovq	.LC16(%rip), %xmm7
	jmp	.L1303
	.p2align 4
	.p2align 3
.L1376:
	movl	3136(%rsp,%rdx,4), %ebp
	leaq	1(%rdx), %rdi
	movl	%ebp, %eax
	shrl	$11, %eax
	xorl	%ebp, %eax
	movl	%eax, %edx
	sall	$7, %edx
	andl	$-1658038656, %edx
	xorl	%edx, %eax
	movl	%eax, %edx
	sall	$15, %edx
	andl	$-272236544, %edx
	xorl	%edx, %eax
	movl	%eax, %edx
	shrl	$18, %edx
	xorl	%edx, %eax
	xorl	%edx, %edx
	cmpl	$-1119, %eax
	setnb	%dl
	imull	$-1119, %edx, %edx
	subl	%edx, %eax
	movl	%eax, (%r10)
.L1300:
	movl	3136(%rsp,%rdi,4), %eax
	leaq	1(%rdi), %rdx
	movl	$0, (%r9)
	movl	%eax, %edi
	shrl	$11, %edi
	xorl	%edi, %eax
	movl	%eax, %edi
	sall	$7, %edi
	andl	$-1658038656, %edi
	xorl	%edi, %eax
	movl	%eax, %edi
	sall	$15, %edi
	andl	$-272236544, %edi
	xorl	%edi, %eax
	movl	%eax, %edi
	shrl	$18, %edi
	xorl	%edi, %eax
	xorl	%edi, %edi
	cmpl	$-1119, %eax
	setnb	%dil
	addq	$4, %r8
	addq	$4, %r9
	addq	$4, %r10
	imull	$-1119, %edi, %edi
	subl	%edi, %eax
	movl	%eax, -4(%r8)
	cmpq	%r8, %r11
	je	.L1375
.L1303:
	cmpq	$623, %rdx
	jbe	.L1376
	leaq	3136(%rsp), %rax
	vpsrld	$31, %xmm5, %xmm6
	.p2align 6
	.p2align 4
	.p2align 3
.L1301:
	vpand	(%rax), %xmm3, %xmm1
	vpand	4(%rax), %xmm4, %xmm0
	addq	$16, %rax
	vpor	%xmm1, %xmm0, %xmm0
	vpsrld	$1, %xmm0, %xmm1
	vpxor	1572(%rax), %xmm1, %xmm1
	vpand	%xmm6, %xmm0, %xmm0
	vpmulld	%xmm2, %xmm0, %xmm0
	vpxor	%xmm0, %xmm1, %xmm0
	vmovdqa	%xmm0, -16(%rax)
	cmpq	%rcx, %rax
	jne	.L1301
	movl	4040(%rsp), %edx
	movl	4044(%rsp), %eax
	vmovq	4036(%rsp), %xmm0
	vmovq	4032(%rsp), %xmm1
	vpand	%xmm10, %xmm0, %xmm0
	vpand	%xmm9, %xmm1, %xmm1
	vmovq	5620(%rsp), %xmm6
	vpor	%xmm1, %xmm0, %xmm0
	vpsrld	$1, %xmm0, %xmm1
	vpand	%xmm8, %xmm0, %xmm0
	vpxor	%xmm6, %xmm1, %xmm1
	vpsrld	$31, %xmm5, %xmm6
	andl	$-2147483648, %edx
	andl	$2147483647, %eax
	vpmulld	%xmm7, %xmm0, %xmm0
	orl	%edx, %eax
	movl	%eax, %edx
	andl	$1, %eax
	shrl	%edx
	xorl	5628(%rsp), %edx
	negl	%eax
	vpxor	%xmm0, %xmm1, %xmm0
	andl	$-1727483681, %eax
	vmovq	%xmm0, 4032(%rsp)
	xorl	%edx, %eax
	leaq	5628(%rsp), %rdx
	movl	%eax, 4040(%rsp)
	leaq	4044(%rsp), %rax
	.p2align 6
	.p2align 4
	.p2align 3
.L1302:
	vpand	(%rax), %xmm3, %xmm1
	addq	$16, %rax
	vpand	-12(%rax), %xmm4, %xmm0
	vpor	%xmm1, %xmm0, %xmm0
	vpsrld	$1, %xmm0, %xmm1
	vpxor	-924(%rax), %xmm1, %xmm1
	vpand	%xmm6, %xmm0, %xmm0
	vpmulld	%xmm2, %xmm0, %xmm0
	vpxor	%xmm0, %xmm1, %xmm0
	vmovdqu	%xmm0, -16(%rax)
	cmpq	%rdx, %rax
	jne	.L1302
	movl	3136(%rsp), %edi
	movl	5628(%rsp), %eax
	movl	%edi, %edx
	andl	$-2147483648, %eax
	andl	$2147483647, %edx
	orl	%edx, %eax
	movl	%eax, %edx
	andl	$1, %eax
	shrl	%edx
	xorl	4720(%rsp), %edx
	negl	%eax
	andl	$-1727483681, %eax
	xorl	%eax, %edx
	movl	%edi, %eax
	shrl	$11, %eax
	movl	%edx, 5628(%rsp)
	xorl	%edi, %eax
	movl	$1, %edi
	movl	%eax, %edx
	sall	$7, %edx
	andl	$-1658038656, %edx
	xorl	%edx, %eax
	movl	%eax, %edx
	sall	$15, %edx
	andl	$-272236544, %edx
	xorl	%edx, %eax
	movl	%eax, %edx
	shrl	$18, %edx
	xorl	%edx, %eax
	xorl	%edx, %edx
	cmpl	$-1119, %eax
	setnb	%dl
	imull	$-1119, %edx, %edx
	subl	%edx, %eax
	movl	%eax, (%r10)
	jmp	.L1300
.L1375:
	vmovsd	.LC0(%rip), %xmm8
	vmovsd	.LC17(%rip), %xmm7
	vxorps	%xmm6, %xmm6, %xmm6
	movl	$5, %edi
	movl	$4294966176, %r12d
.L1312:
	movl	$0, 60(%rsp)
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	xorl	%edx, %edx
	movq	%rax, %rbp
	jmp	.L1307
	.p2align 6
	.p2align 4
	.p2align 3
.L1378:
	addl	%r8d, %eax
.L1374:
	incq	%rdx
	xorl	%eax, 60(%rsp)
	movl	%eax, (%r9)
	cmpq	$10000000, %rdx
	je	.L1377
.L1307:
	movzbl	%dl, %eax
	movl	1088(%rsp,%rax,4), %ecx
	movl	64(%rsp,%rax,4), %r10d
	leaq	(%rsi,%rax,4), %r9
	movq	%rcx, %r8
	addq	%r10, %rcx
	movq	%r10, %rax
	cmpq	%rcx, %r12
	jnb	.L1378
	leal	1119(%r10,%r8), %eax
	jmp	.L1374
.L1377:
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	subq	%rbp, %rax
	js	.L1308
	vcvtsi2sdq	%rax, %xmm6, %xmm0
.L1309:
	vdivsd	%xmm7, %xmm0, %xmm0
	decl	%edi
	movl	60(%rsp), %eax
	vminsd	%xmm8, %xmm0, %xmm2
	vmovapd	%xmm2, %xmm8
	jne	.L1312
	movq	%rbx, %rdx
	leaq	.LC18(%rip), %rcx
	vmovq	%xmm2, %r8
	movl	$5, %edi
	call	__mingw_printf
	vmovsd	.LC0(%rip), %xmm8
.L1321:
	movl	$0, 56(%rsp)
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	xorl	%edx, %edx
	movq	%rax, %rbp
	.p2align 6
	.p2align 4
	.p2align 3
.L1316:
	movzbl	%dl, %eax
	movl	1088(%rsp,%rax,4), %ecx
	leaq	(%rsi,%rax,4), %r8
	movl	64(%rsp,%rax,4), %eax
	cmpl	%ecx, %eax
	jnb	.L1313
	subl	$1119, %eax
.L1313:
	subl	%ecx, %eax
	incq	%rdx
	xorl	%eax, 56(%rsp)
	movl	%eax, (%r8)
	cmpq	$10000000, %rdx
	jne	.L1316
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	subq	%rbp, %rax
	js	.L1317
	vcvtsi2sdq	%rax, %xmm6, %xmm0
.L1318:
	vdivsd	%xmm7, %xmm0, %xmm0
	decl	%edi
	movl	56(%rsp), %eax
	vminsd	%xmm8, %xmm0, %xmm2
	vmovapd	%xmm2, %xmm8
	jne	.L1321
	movq	%rbx, %rdx
	leaq	.LC19(%rip), %rcx
	vmovq	%xmm2, %r8
	movl	$5, %edi
	call	__mingw_printf
	vmovsd	.LC0(%rip), %xmm8
	movl	$4294966176, %r13d
	movabsq	$-4294966177, %r12
.L1328:
	movl	$0, 52(%rsp)
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	xorl	%ecx, %ecx
	movq	%rax, %rbp
	.p2align 4
	.p2align 3
.L1323:
	movzbl	%cl, %r8d
	movl	64(%rsp,%r8,4), %eax
	movl	1088(%rsp,%r8,4), %edx
	imulq	%rax, %rdx
	movq	%rdx, %rax
	movl	%edx, %edx
	shrq	$32, %rax
	imulq	$1119, %rax, %rax
	addq	%rdx, %rax
	movq	%rax, %rdx
	movl	%eax, %eax
	shrq	$32, %rdx
	imulq	$1119, %rdx, %rdx
	addq	%rdx, %rax
	cmpq	%rax, %r13
	leaq	(%rax,%r12), %rdx
	cmovb	%rdx, %rax
	incq	%rcx
	xorl	%eax, 52(%rsp)
	movl	%eax, (%rsi,%r8,4)
	cmpq	$10000000, %rcx
	jne	.L1323
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	subq	%rbp, %rax
	js	.L1324
	vcvtsi2sdq	%rax, %xmm6, %xmm0
.L1325:
	vdivsd	%xmm7, %xmm0, %xmm0
	decl	%edi
	movl	52(%rsp), %eax
	vminsd	%xmm8, %xmm0, %xmm2
	vmovapd	%xmm2, %xmm8
	jne	.L1328
	movq	%rbx, %rdx
	leaq	.LC20(%rip), %rcx
	vmovq	%xmm2, %r8
	movl	$5, %edi
	call	__mingw_printf
	vmovsd	.LC0(%rip), %xmm8
	movl	$4294966176, %r13d
	movabsq	$-4294966177, %r12
.L1335:
	movl	$0, 48(%rsp)
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	xorl	%ecx, %ecx
	movq	%rax, %rbp
	.p2align 4
	.p2align 3
.L1330:
	movzbl	%cl, %r8d
	movl	64(%rsp,%r8,4), %edx
	imulq	%rdx, %rdx
	movq	%rdx, %rax
	movl	%edx, %edx
	shrq	$32, %rax
	imulq	$1119, %rax, %rax
	addq	%rdx, %rax
	movq	%rax, %rdx
	movl	%eax, %eax
	shrq	$32, %rdx
	imulq	$1119, %rdx, %rdx
	addq	%rdx, %rax
	cmpq	%rax, %r13
	leaq	(%rax,%r12), %rdx
	cmovb	%rdx, %rax
	incq	%rcx
	xorl	%eax, 48(%rsp)
	movl	%eax, (%rsi,%r8,4)
	cmpq	$10000000, %rcx
	jne	.L1330
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	subq	%rbp, %rax
	js	.L1331
	vcvtsi2sdq	%rax, %xmm6, %xmm0
.L1332:
	vdivsd	%xmm7, %xmm0, %xmm0
	decl	%edi
	movl	48(%rsp), %eax
	vminsd	%xmm8, %xmm0, %xmm2
	vmovapd	%xmm2, %xmm8
	jne	.L1335
	movq	%rbx, %rdx
	leaq	.LC21(%rip), %rcx
	vmovq	%xmm2, %r8
	movl	$3, %edi
	call	__mingw_printf
	vmovsd	.LC0(%rip), %xmm7
	movl	$4294966177, %r12d
	vmovsd	.LC22(%rip), %xmm8
.L1346:
	movl	$0, 44(%rsp)
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	xorl	%r10d, %r10d
	movq	%rax, %rbp
	.p2align 4
	.p2align 3
.L1341:
	movzbl	%r10b, %eax
	movl	64(%rsp,%rax,4), %ecx
	leaq	(%rsi,%rax,4), %r11
	testq	%rcx, %rcx
	je	.L1336
	xorl	%r9d, %r9d
	movl	$1, %r8d
	movq	%r12, %rax
	jmp	.L1337
	.p2align 5
	.p2align 4
	.p2align 3
.L1347:
	movq	%r13, %r8
.L1337:
	cqto
	idivq	%rcx
	imulq	%r8, %rax
	subq	%rax, %r9
	movq	%rcx, %rax
	movq	%rdx, %rcx
	movq	%r9, %r13
	movq	%r8, %r9
	testq	%rdx, %rdx
	jne	.L1347
	cmpq	$1, %rax
	jg	.L1336
	leaq	(%r8,%r12), %rax
	testq	%r8, %r8
	cmovns	%r8, %rax
.L1339:
	incq	%r10
	xorl	%eax, 44(%rsp)
	movl	%eax, (%r11)
	cmpq	$250000, %r10
	jne	.L1341
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	subq	%rbp, %rax
	js	.L1342
	vcvtsi2sdq	%rax, %xmm6, %xmm0
.L1343:
	vdivsd	%xmm8, %xmm0, %xmm0
	decl	%edi
	movl	44(%rsp), %eax
	vminsd	%xmm7, %xmm0, %xmm2
	vmovapd	%xmm2, %xmm7
	jne	.L1346
	vmovaps	5648(%rsp), %xmm6
	vmovaps	5664(%rsp), %xmm7
	movq	%rbx, %rdx
	leaq	.LC23(%rip), %rcx
	vmovaps	5680(%rsp), %xmm8
	vmovaps	5696(%rsp), %xmm9
	vmovq	%xmm2, %r8
	vmovaps	5712(%rsp), %xmm10
	addq	$5736, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r12
	popq	%r13
	jmp	__mingw_printf
.L1336:
	xorl	%eax, %eax
	jmp	.L1339
.L1342:
	movq	%rax, %rdx
	andl	$1, %eax
	shrq	%rdx
	orq	%rax, %rdx
	vcvtsi2sdq	%rdx, %xmm6, %xmm0
	vaddsd	%xmm0, %xmm0, %xmm0
	jmp	.L1343
.L1331:
	movq	%rax, %rdx
	andl	$1, %eax
	shrq	%rdx
	orq	%rax, %rdx
	vcvtsi2sdq	%rdx, %xmm6, %xmm0
	vaddsd	%xmm0, %xmm0, %xmm0
	jmp	.L1332
.L1324:
	movq	%rax, %rdx
	andl	$1, %eax
	shrq	%rdx
	orq	%rax, %rdx
	vcvtsi2sdq	%rdx, %xmm6, %xmm0
	vaddsd	%xmm0, %xmm0, %xmm0
	jmp	.L1325
.L1317:
	movq	%rax, %rdx
	andl	$1, %eax
	shrq	%rdx
	orq	%rax, %rdx
	vcvtsi2sdq	%rdx, %xmm6, %xmm0
	vaddsd	%xmm0, %xmm0, %xmm0
	jmp	.L1318
.L1308:
	movq	%rax, %rdx
	andl	$1, %eax
	shrq	%rdx
	orq	%rax, %rdx
	vcvtsi2sdq	%rdx, %xmm6, %xmm0
	vaddsd	%xmm0, %xmm0, %xmm0
	jmp	.L1309
	.seh_endproc
	.section .rdata,"dr"
.LC24:
	.ascii "naive\0"
.LC25:
	.ascii "barrett\0"
.LC26:
	.ascii "mont\0"
.LC27:
	.ascii "pseudo\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB4204:
	subq	$40, %rsp
	.seh_stackalloc	40
	.seh_endprologue
	call	__main
	leaq	.LC24(%rip), %rcx
	call	_Z11bench_fieldIN2fp7FpNaiveILj4294966177EEEEvPKc
	leaq	.LC25(%rip), %rcx
	call	_Z11bench_fieldIN2fp9FpBarrettILj4294966177EEEEvPKc
	leaq	.LC26(%rip), %rcx
	call	_Z11bench_fieldIN2fp6FpMontILj4294966177EEEEvPKc
	leaq	.LC27(%rip), %rcx
	call	_Z11bench_fieldIN2fp8FpPseudoILj4294966177EEEEvPKc
	leaq	.LC24(%rip), %rcx
	call	_Z8bench_ecIN2fp7FpNaiveILj4294966177EEEEvPKc
	leaq	.LC25(%rip), %rcx
	call	_Z8bench_ecIN2fp9FpBarrettILj4294966177EEEEvPKc
	leaq	.LC26(%rip), %rcx
	call	_Z8bench_ecIN2fp6FpMontILj4294966177EEEEvPKc
	leaq	.LC27(%rip), %rcx
	call	_Z8bench_ecIN2fp8FpPseudoILj4294966177EEEEvPKc
	xorl	%eax, %eax
	addq	$40, %rsp
	ret
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC0:
	.long	1733216256
	.long	1135329645
	.align 8
.LC1:
	.long	0
	.long	1095164768
	.align 8
.LC13:
	.long	-2147483648
	.long	-2147483648
	.align 8
.LC14:
	.long	2147483647
	.long	2147483647
	.align 8
.LC15:
	.long	1
	.long	1
	.align 8
.LC16:
	.long	-1727483681
	.long	-1727483681
	.align 8
.LC17:
	.long	0
	.long	1097011920
	.align 8
.LC22:
	.long	0
	.long	1091470464
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (x86_64-posix-seh-rev0, Built by MinGW-Builds project) 16.1.0"
	.def	_ZNSt6chrono3_V212steady_clock3nowEv;	.scl	2;	.type	32;	.endef
