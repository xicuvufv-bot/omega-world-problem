	.file	"asm_probe.cpp"
	.text
	.p2align 4
	.def	_ZN2fpL11inv_mod_u32Ejj.constprop.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZN2fpL11inv_mod_u32Ejj.constprop.0
_ZN2fpL11inv_mod_u32Ejj.constprop.0:
.LFB153:
	.seh_endprologue
	xorl	%r9d, %r9d
	movl	$1, %r8d
	movl	$4294966177, %eax
	movl	%ecx, %ecx
	testq	%rcx, %rcx
	jne	.L2
	jmp	.L4
	.p2align 5
	.p2align 4
	.p2align 3
.L7:
	movq	%r10, %r8
.L2:
	cqto
	movq	%r9, %r10
	movq	%r8, %r9
	idivq	%rcx
	imulq	%r8, %rax
	subq	%rax, %r10
	movq	%rcx, %rax
	movq	%rdx, %rcx
	testq	%rdx, %rdx
	jne	.L7
	cmpq	$1, %rax
	jg	.L4
	movl	$4294966177, %eax
	addq	%r8, %rax
	testq	%r8, %r8
	cmovns	%r8, %rax
	ret
	.p2align 4
	.p2align 3
.L4:
	xorl	%eax, %eax
	ret
	.seh_endproc
	.align 2
	.p2align 4
	.def	_ZNK2ec8JacobianIN2fp8FpPseudoILj4294966177EEEE7is_zeroEv.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNK2ec8JacobianIN2fp8FpPseudoILj4294966177EEEE7is_zeroEv.isra.0
_ZNK2ec8JacobianIN2fp8FpPseudoILj4294966177EEEE7is_zeroEv.isra.0:
.LFB154:
	.seh_endprologue
	movl	%ecx, %eax
	ret
	.seh_endproc
	.align 2
	.p2align 4
	.def	_ZNK2ec8JacobianIN2fp6FpMontILj4294966177EEEE7is_zeroEv.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNK2ec8JacobianIN2fp6FpMontILj4294966177EEEE7is_zeroEv.isra.0
_ZNK2ec8JacobianIN2fp6FpMontILj4294966177EEEE7is_zeroEv.isra.0:
.LFB155:
	.seh_endprologue
	movl	%ecx, %eax
	ret
	.seh_endproc
	.align 2
	.p2align 4
	.def	_ZNK2ec8JacobianIN2fp9FpBarrettILj4294966177EEEE7is_zeroEv.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNK2ec8JacobianIN2fp9FpBarrettILj4294966177EEEE7is_zeroEv.isra.0
_ZNK2ec8JacobianIN2fp9FpBarrettILj4294966177EEEE7is_zeroEv.isra.0:
.LFB156:
	.seh_endprologue
	movl	%ecx, %eax
	ret
	.seh_endproc
	.align 2
	.p2align 4
	.def	_ZNK2ec6AffineIN2fp7FpNaiveILj4294966177EEEE7is_zeroEv.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNK2ec6AffineIN2fp7FpNaiveILj4294966177EEEE7is_zeroEv.isra.0
_ZNK2ec6AffineIN2fp7FpNaiveILj4294966177EEEE7is_zeroEv.isra.0:
.LFB157:
	.seh_endprologue
	movl	%ecx, %eax
	ret
	.seh_endproc
	.align 2
	.p2align 4
	.def	_ZNK2ec8JacobianIN2fp7FpNaiveILj4294966177EEEE7is_zeroEv.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNK2ec8JacobianIN2fp7FpNaiveILj4294966177EEEE7is_zeroEv.isra.0
_ZNK2ec8JacobianIN2fp7FpNaiveILj4294966177EEEE7is_zeroEv.isra.0:
.LFB158:
	.seh_endprologue
	movl	%ecx, %eax
	ret
	.seh_endproc
	.section	.text$_ZN2fp7FpNaiveILj4294966177EE3mulEjj,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZN2fp7FpNaiveILj4294966177EE3mulEjj
	.def	_ZN2fp7FpNaiveILj4294966177EE3mulEjj;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN2fp7FpNaiveILj4294966177EE3mulEjj
_ZN2fp7FpNaiveILj4294966177EE3mulEjj:
.LFB111:
	.seh_endprologue
	movabsq	$-9223369633819947615, %rax
	movl	%edx, %edx
	movl	%ecx, %ecx
	imulq	%rdx, %rcx
	mulq	%rcx
	shrq	$31, %rdx
	imull	$1119, %edx, %edx
	leal	(%rdx,%rcx), %eax
	ret
	.seh_endproc
	.section	.text$_Z9probe_mulIN2fp7FpNaiveILj4294966177EEEEjjj,"x"
	.linkonce discard
	.p2align 4
	.globl	_Z9probe_mulIN2fp7FpNaiveILj4294966177EEEEjjj
	.def	_Z9probe_mulIN2fp7FpNaiveILj4294966177EEEEjjj;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9probe_mulIN2fp7FpNaiveILj4294966177EEEEjjj
_Z9probe_mulIN2fp7FpNaiveILj4294966177EEEEjjj:
.LFB98:
	.seh_endprologue
	jmp	_ZN2fp7FpNaiveILj4294966177EE3mulEjj
	.seh_endproc
	.text
	.p2align 4
	.globl	_Z8test_muljj
	.def	_Z8test_muljj;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8test_muljj
_Z8test_muljj:
.LFB95:
	.seh_endprologue
	jmp	_Z9probe_mulIN2fp7FpNaiveILj4294966177EEEEjjj
	.seh_endproc
	.section	.text$_ZN2fp7FpNaiveILj4294966177EE3invEj,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZN2fp7FpNaiveILj4294966177EE3invEj
	.def	_ZN2fp7FpNaiveILj4294966177EE3invEj;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN2fp7FpNaiveILj4294966177EE3invEj
_ZN2fp7FpNaiveILj4294966177EE3invEj:
.LFB112:
	.seh_endprologue
	jmp	_ZN2fpL11inv_mod_u32Ejj.constprop.0
	.seh_endproc
	.section	.text$_Z9probe_invIN2fp7FpNaiveILj4294966177EEEEjj,"x"
	.linkonce discard
	.p2align 4
	.globl	_Z9probe_invIN2fp7FpNaiveILj4294966177EEEEjj
	.def	_Z9probe_invIN2fp7FpNaiveILj4294966177EEEEjj;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9probe_invIN2fp7FpNaiveILj4294966177EEEEjj
_Z9probe_invIN2fp7FpNaiveILj4294966177EEEEjj:
.LFB99:
	.seh_endprologue
	jmp	_ZN2fp7FpNaiveILj4294966177EE3invEj
	.seh_endproc
	.text
	.p2align 4
	.globl	test_inv
	.def	test_inv;	.scl	2;	.type	32;	.endef
	.seh_proc	test_inv
test_inv:
.LFB96:
	.seh_endprologue
	jmp	_Z9probe_invIN2fp7FpNaiveILj4294966177EEEEjj
	.seh_endproc
	.section	.text$_ZN2fp6FpMontILj4294966177EE3mulEjj,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZN2fp6FpMontILj4294966177EE3mulEjj
	.def	_ZN2fp6FpMontILj4294966177EE3mulEjj;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN2fp6FpMontILj4294966177EE3mulEjj
_ZN2fp6FpMontILj4294966177EE3mulEjj:
.LFB115:
	.seh_endprologue
	movl	%ecx, %eax
	movl	%edx, %edx
	imulq	%rdx, %rax
	movl	$4294966177, %edx
	imull	$-383821921, %eax, %ecx
	imulq	%rdx, %rcx
	xorl	%edx, %edx
	addq	%rcx, %rax
	movl	$4294966176, %ecx
	adcq	$0, %rdx
	shrdq	$32, %rdx, %rax
	movl	%eax, %edx
	cmpq	%rax, %rcx
	jnb	.L21
	addl	$1119, %edx
.L21:
	movl	%edx, %eax
	ret
	.seh_endproc
	.section	.text$_Z9probe_mulIN2fp6FpMontILj4294966177EEEEjjj,"x"
	.linkonce discard
	.p2align 4
	.globl	_Z9probe_mulIN2fp6FpMontILj4294966177EEEEjjj
	.def	_Z9probe_mulIN2fp6FpMontILj4294966177EEEEjjj;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9probe_mulIN2fp6FpMontILj4294966177EEEEjjj
_Z9probe_mulIN2fp6FpMontILj4294966177EEEEjjj:
.LFB102:
	.seh_endprologue
	jmp	_ZN2fp6FpMontILj4294966177EE3mulEjj
	.seh_endproc
	.section	.text$_ZN2fp8FpPseudoILj4294966177EE3subEjj,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZN2fp8FpPseudoILj4294966177EE3subEjj
	.def	_ZN2fp8FpPseudoILj4294966177EE3subEjj;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN2fp8FpPseudoILj4294966177EE3subEjj
_ZN2fp8FpPseudoILj4294966177EE3subEjj:
.LFB117:
	.seh_endprologue
	movl	%ecx, %r8d
	movl	%edx, %ecx
	movl	%r8d, %edx
	subl	%ecx, %edx
	cmpl	%ecx, %r8d
	leal	-1119(%rdx), %eax
	cmovnb	%edx, %eax
	ret
	.seh_endproc
	.section	.text$_Z9probe_subIN2fp8FpPseudoILj4294966177EEEEjjj,"x"
	.linkonce discard
	.p2align 4
	.globl	_Z9probe_subIN2fp8FpPseudoILj4294966177EEEEjjj
	.def	_Z9probe_subIN2fp8FpPseudoILj4294966177EEEEjjj;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9probe_subIN2fp8FpPseudoILj4294966177EEEEjjj
_Z9probe_subIN2fp8FpPseudoILj4294966177EEEEjjj:
.LFB104:
	.seh_endprologue
	jmp	_ZN2fp8FpPseudoILj4294966177EE3subEjj
	.seh_endproc
	.section	.text$_ZN2fp7FpNaiveILj4294966177EE3sqrEj,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZN2fp7FpNaiveILj4294966177EE3sqrEj
	.def	_ZN2fp7FpNaiveILj4294966177EE3sqrEj;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN2fp7FpNaiveILj4294966177EE3sqrEj
_ZN2fp7FpNaiveILj4294966177EE3sqrEj:
.LFB125:
	.seh_endprologue
	movabsq	$-9223369633819947615, %rax
	movl	%ecx, %ecx
	imulq	%rcx, %rcx
	mulq	%rcx
	shrq	$31, %rdx
	imull	$1119, %edx, %edx
	leal	(%rdx,%rcx), %eax
	ret
	.seh_endproc
	.section	.text$_ZN2fp7FpNaiveILj4294966177EE3addEjj,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZN2fp7FpNaiveILj4294966177EE3addEjj
	.def	_ZN2fp7FpNaiveILj4294966177EE3addEjj;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN2fp7FpNaiveILj4294966177EE3addEjj
_ZN2fp7FpNaiveILj4294966177EE3addEjj:
.LFB126:
	.seh_endprologue
	movl	%edx, %r8d
	movl	%ecx, %eax
	addq	%r8, %rax
	leal	1119(%rcx,%rdx), %r8d
	addl	%edx, %ecx
	movl	$4294966176, %edx
	cmpq	%rax, %rdx
	movl	%r8d, %eax
	cmovnb	%ecx, %eax
	ret
	.seh_endproc
	.section	.text$_ZN2fp7FpNaiveILj4294966177EE3subEjj,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZN2fp7FpNaiveILj4294966177EE3subEjj
	.def	_ZN2fp7FpNaiveILj4294966177EE3subEjj;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN2fp7FpNaiveILj4294966177EE3subEjj
_ZN2fp7FpNaiveILj4294966177EE3subEjj:
.LFB127:
	.seh_endprologue
	movl	%ecx, %r8d
	movl	%edx, %ecx
	movl	%r8d, %edx
	subl	%ecx, %edx
	cmpl	%ecx, %r8d
	leal	-1119(%rdx), %eax
	cmovnb	%edx, %eax
	ret
	.seh_endproc
	.section	.text$_ZN2ec8JacobianIN2fp7FpNaiveILj4294966177EEEE14from_affine_xzEjjj,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZN2ec8JacobianIN2fp7FpNaiveILj4294966177EEEE14from_affine_xzEjjj
	.def	_ZN2ec8JacobianIN2fp7FpNaiveILj4294966177EEEE14from_affine_xzEjjj;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN2ec8JacobianIN2fp7FpNaiveILj4294966177EEEE14from_affine_xzEjjj
_ZN2ec8JacobianIN2fp7FpNaiveILj4294966177EEEE14from_affine_xzEjjj:
.LFB128:
	.seh_endprologue
	movq	%rcx, %rax
	movl	%edx, (%rcx)
	movl	%r8d, 4(%rcx)
	movl	%r9d, 8(%rcx)
	movb	$0, 12(%rcx)
	ret
	.seh_endproc
	.section	.text$_ZN2ec8JacobianIN2fp7FpNaiveILj4294966177EEEE3dblERKS4_,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZN2ec8JacobianIN2fp7FpNaiveILj4294966177EEEE3dblERKS4_
	.def	_ZN2ec8JacobianIN2fp7FpNaiveILj4294966177EEEE3dblERKS4_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN2ec8JacobianIN2fp7FpNaiveILj4294966177EEEE3dblERKS4_
_ZN2ec8JacobianIN2fp7FpNaiveILj4294966177EEEE3dblERKS4_:
.LFB113:
	pushq	%r15
	.seh_pushreg	%r15
	pushq	%r14
	.seh_pushreg	%r14
	pushq	%rbp
	.seh_pushreg	%rbp
	pushq	%rdi
	.seh_pushreg	%rdi
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$56, %rsp
	.seh_stackalloc	56
	.seh_endprologue
	movq	%rcx, %rbp
	movzbl	12(%rdx), %ecx
	movq	%rdx, %rbx
	call	_ZNK2ec8JacobianIN2fp7FpNaiveILj4294966177EEEE7is_zeroEv.isra.0
	testb	%al, %al
	je	.L37
	vmovdqu	(%rdx), %xmm0
	movq	%rbp, %rax
	vmovdqu	%xmm0, 0(%rbp)
	addq	$56, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r14
	popq	%r15
	ret
	.p2align 4
	.p2align 3
.L37:
	movl	(%rdx), %esi
	movl	%esi, %ecx
	call	_ZN2fp7FpNaiveILj4294966177EE3sqrEj
	movl	4(%rbx), %r9d
	movl	%eax, %edi
	movl	%r9d, %ecx
	movl	%r9d, 44(%rsp)
	call	_ZN2fp7FpNaiveILj4294966177EE3sqrEj
	movl	%eax, %edx
	movl	%eax, %ecx
	movl	%eax, 40(%rsp)
	call	_ZN2fp7FpNaiveILj4294966177EE3addEjj
	movl	%esi, %ecx
	movl	%eax, %edx
	call	_ZN2fp7FpNaiveILj4294966177EE3mulEjj
	movl	%eax, %edx
	movl	%eax, %ecx
	call	_ZN2fp7FpNaiveILj4294966177EE3addEjj
	movl	%edi, %edx
	movl	%edi, %ecx
	movl	%eax, %esi
	call	_ZN2fp7FpNaiveILj4294966177EE3addEjj
	movl	%edi, %ecx
	movl	%eax, %edx
	call	_ZN2fp7FpNaiveILj4294966177EE3addEjj
	movl	%esi, %edx
	movl	%esi, %ecx
	movl	%eax, %r14d
	call	_ZN2fp7FpNaiveILj4294966177EE3addEjj
	movl	%r14d, %ecx
	movl	%eax, %edi
	call	_ZN2fp7FpNaiveILj4294966177EE3sqrEj
	movl	%edi, %edx
	movl	%eax, %ecx
	call	_ZN2fp7FpNaiveILj4294966177EE3subEjj
	movl	8(%rbx), %ecx
	movl	%eax, %edi
	movl	%ecx, %edx
	call	_ZN2fp7FpNaiveILj4294966177EE3addEjj
	movl	44(%rsp), %edx
	movl	%eax, %ecx
	call	_ZN2fp7FpNaiveILj4294966177EE3mulEjj
	movl	40(%rsp), %ecx
	movl	%eax, %ebx
	call	_ZN2fp7FpNaiveILj4294966177EE3sqrEj
	movl	%eax, %edx
	movl	%eax, %ecx
	call	_ZN2fp7FpNaiveILj4294966177EE3addEjj
	movl	%eax, %edx
	movl	%eax, %ecx
	call	_ZN2fp7FpNaiveILj4294966177EE3addEjj
	movl	%eax, %edx
	movl	%eax, %ecx
	call	_ZN2fp7FpNaiveILj4294966177EE3addEjj
	movl	%edi, %edx
	movl	%esi, %ecx
	movl	%eax, %r15d
	call	_ZN2fp7FpNaiveILj4294966177EE3subEjj
	movl	%r14d, %ecx
	movl	%eax, %edx
	call	_ZN2fp7FpNaiveILj4294966177EE3mulEjj
	movl	%r15d, %edx
	movl	%eax, %ecx
	call	_ZN2fp7FpNaiveILj4294966177EE3subEjj
	movl	%ebx, %r9d
	movl	%edi, %edx
	movq	%rbp, %rcx
	movl	%eax, %r8d
	call	_ZN2ec8JacobianIN2fp7FpNaiveILj4294966177EEEE14from_affine_xzEjjj
	movq	%rbp, %rax
	addq	$56, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r14
	popq	%r15
	ret
	.seh_endproc
	.section	.text$_Z10probe_jdblIN2fp7FpNaiveILj4294966177EEEEN2ec8JacobianIT_EES6_,"x"
	.linkonce discard
	.p2align 4
	.globl	_Z10probe_jdblIN2fp7FpNaiveILj4294966177EEEEN2ec8JacobianIT_EES6_
	.def	_Z10probe_jdblIN2fp7FpNaiveILj4294966177EEEEN2ec8JacobianIT_EES6_;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10probe_jdblIN2fp7FpNaiveILj4294966177EEEEN2ec8JacobianIT_EES6_
_Z10probe_jdblIN2fp7FpNaiveILj4294966177EEEEN2ec8JacobianIT_EES6_:
.LFB100:
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$48, %rsp
	.seh_stackalloc	48
	.seh_endprologue
	vmovdqu	(%rdx), %xmm0
	movq	%rcx, %rbx
	leaq	32(%rsp), %rdx
	vmovdqa	%xmm0, 32(%rsp)
	call	_ZN2ec8JacobianIN2fp7FpNaiveILj4294966177EEEE3dblERKS4_
	movq	%rbx, %rax
	addq	$48, %rsp
	popq	%rbx
	ret
	.seh_endproc
	.text
	.p2align 4
	.globl	test_jdbl
	.def	test_jdbl;	.scl	2;	.type	32;	.endef
	.seh_proc	test_jdbl
test_jdbl:
.LFB97:
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$48, %rsp
	.seh_stackalloc	48
	.seh_endprologue
	vmovdqu	(%rdx), %xmm0
	movq	%rcx, %rbx
	leaq	32(%rsp), %rdx
	vmovdqa	%xmm0, 32(%rsp)
	call	_Z10probe_jdblIN2fp7FpNaiveILj4294966177EEEEN2ec8JacobianIT_EES6_
	movq	%rbx, %rax
	addq	$48, %rsp
	popq	%rbx
	ret
	.seh_endproc
	.section	.text$_ZN2fp9FpBarrettILj4294966177EE8reduce64Ey,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZN2fp9FpBarrettILj4294966177EE8reduce64Ey
	.def	_ZN2fp9FpBarrettILj4294966177EE8reduce64Ey;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN2fp9FpBarrettILj4294966177EE8reduce64Ey
_ZN2fp9FpBarrettILj4294966177EE8reduce64Ey:
.LFB129:
	.seh_endprologue
	movabsq	$4294968415, %rax
	movl	$4294966177, %r8d
	mulq	%rcx
	movl	$4294966176, %eax
	imulq	%r8, %rdx
	subq	%rdx, %rcx
	cmpq	%rcx, %rax
	jnb	.L42
	movq	%rcx, %rdx
	subq	%r8, %rdx
	cmpq	%rdx, %rax
	jnb	.L43
	movabsq	$-8589932354, %rax
	addq	%rax, %rcx
.L42:
	movl	%ecx, %eax
	ret
	.p2align 4
	.p2align 3
.L43:
	movq	%rdx, %rcx
	movl	%ecx, %eax
	ret
	.seh_endproc
	.section	.text$_ZN2fp9FpBarrettILj4294966177EE3mulEjj,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZN2fp9FpBarrettILj4294966177EE3mulEjj
	.def	_ZN2fp9FpBarrettILj4294966177EE3mulEjj;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN2fp9FpBarrettILj4294966177EE3mulEjj
_ZN2fp9FpBarrettILj4294966177EE3mulEjj:
.LFB114:
	.seh_endprologue
	movl	%edx, %edx
	movl	%ecx, %ecx
	imulq	%rdx, %rcx
	jmp	_ZN2fp9FpBarrettILj4294966177EE8reduce64Ey
	.seh_endproc
	.section	.text$_Z9probe_mulIN2fp9FpBarrettILj4294966177EEEEjjj,"x"
	.linkonce discard
	.p2align 4
	.globl	_Z9probe_mulIN2fp9FpBarrettILj4294966177EEEEjjj
	.def	_Z9probe_mulIN2fp9FpBarrettILj4294966177EEEEjjj;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9probe_mulIN2fp9FpBarrettILj4294966177EEEEjjj
_Z9probe_mulIN2fp9FpBarrettILj4294966177EEEEjjj:
.LFB101:
	.seh_endprologue
	jmp	_ZN2fp9FpBarrettILj4294966177EE3mulEjj
	.seh_endproc
	.section	.text$_ZN2fp8FpPseudoILj4294966177EE8reduce64Ey,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZN2fp8FpPseudoILj4294966177EE8reduce64Ey
	.def	_ZN2fp8FpPseudoILj4294966177EE8reduce64Ey;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN2fp8FpPseudoILj4294966177EE8reduce64Ey
_ZN2fp8FpPseudoILj4294966177EE8reduce64Ey:
.LFB130:
	.seh_endprologue
	movq	%rcx, %rax
	movl	%ecx, %ecx
	shrq	$32, %rax
	imulq	$1119, %rax, %rax
	leaq	(%rax,%rcx), %rdx
	addl	%ecx, %eax
	movl	$4294966176, %ecx
	shrq	$32, %rdx
	movl	%eax, %eax
	imulq	$1119, %rdx, %rdx
	addq	%rax, %rdx
	movabsq	$-4294966177, %rax
	addq	%rdx, %rax
	cmpq	%rdx, %rcx
	cmovnb	%rdx, %rax
	ret
	.seh_endproc
	.section	.text$_ZN2fp8FpPseudoILj4294966177EE3mulEjj,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZN2fp8FpPseudoILj4294966177EE3mulEjj
	.def	_ZN2fp8FpPseudoILj4294966177EE3mulEjj;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN2fp8FpPseudoILj4294966177EE3mulEjj
_ZN2fp8FpPseudoILj4294966177EE3mulEjj:
.LFB116:
	.seh_endprologue
	movl	%edx, %edx
	movl	%ecx, %ecx
	imulq	%rdx, %rcx
	jmp	_ZN2fp8FpPseudoILj4294966177EE8reduce64Ey
	.seh_endproc
	.section	.text$_Z9probe_mulIN2fp8FpPseudoILj4294966177EEEEjjj,"x"
	.linkonce discard
	.p2align 4
	.globl	_Z9probe_mulIN2fp8FpPseudoILj4294966177EEEEjjj
	.def	_Z9probe_mulIN2fp8FpPseudoILj4294966177EEEEjjj;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9probe_mulIN2fp8FpPseudoILj4294966177EEEEjjj
_Z9probe_mulIN2fp8FpPseudoILj4294966177EEEEjjj:
.LFB103:
	.seh_endprologue
	jmp	_ZN2fp8FpPseudoILj4294966177EE3mulEjj
	.seh_endproc
	.section	.text$_ZN2fp6FpMontILj4294966177EE7to_montEj,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZN2fp6FpMontILj4294966177EE7to_montEj
	.def	_ZN2fp6FpMontILj4294966177EE7to_montEj;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN2fp6FpMontILj4294966177EE7to_montEj
_ZN2fp6FpMontILj4294966177EE7to_montEj:
.LFB131:
	.seh_endprologue
	movl	$1252161, %edx
	jmp	_ZN2fp6FpMontILj4294966177EE3mulEjj
	.seh_endproc
	.section	.text$_ZN2fp6FpMontILj4294966177EE9from_montEj,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZN2fp6FpMontILj4294966177EE9from_montEj
	.def	_ZN2fp6FpMontILj4294966177EE9from_montEj;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN2fp6FpMontILj4294966177EE9from_montEj
_ZN2fp6FpMontILj4294966177EE9from_montEj:
.LFB132:
	.seh_endprologue
	movl	$1, %edx
	jmp	_ZN2fp6FpMontILj4294966177EE3mulEjj
	.seh_endproc
	.section	.text$_ZN2fp6FpMontILj4294966177EE3invEj,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZN2fp6FpMontILj4294966177EE3invEj
	.def	_ZN2fp6FpMontILj4294966177EE3invEj;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN2fp6FpMontILj4294966177EE3invEj
_ZN2fp6FpMontILj4294966177EE3invEj:
.LFB118:
	subq	$40, %rsp
	.seh_stackalloc	40
	.seh_endprologue
	call	_ZN2fp6FpMontILj4294966177EE9from_montEj
	movl	%eax, %ecx
	call	_ZN2fpL11inv_mod_u32Ejj.constprop.0
	movl	%eax, %ecx
	vzeroupper
	addq	$40, %rsp
	jmp	_ZN2fp6FpMontILj4294966177EE7to_montEj
	.seh_endproc
	.section	.text$_Z9probe_invIN2fp6FpMontILj4294966177EEEEjj,"x"
	.linkonce discard
	.p2align 4
	.globl	_Z9probe_invIN2fp6FpMontILj4294966177EEEEjj
	.def	_Z9probe_invIN2fp6FpMontILj4294966177EEEEjj;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9probe_invIN2fp6FpMontILj4294966177EEEEjj
_Z9probe_invIN2fp6FpMontILj4294966177EEEEjj:
.LFB105:
	.seh_endprologue
	jmp	_ZN2fp6FpMontILj4294966177EE3invEj
	.seh_endproc
	.section	.text$_ZN2ec8JacobianIN2fp7FpNaiveILj4294966177EEEE4zeroEv,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZN2ec8JacobianIN2fp7FpNaiveILj4294966177EEEE4zeroEv
	.def	_ZN2ec8JacobianIN2fp7FpNaiveILj4294966177EEEE4zeroEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN2ec8JacobianIN2fp7FpNaiveILj4294966177EEEE4zeroEv
_ZN2ec8JacobianIN2fp7FpNaiveILj4294966177EEEE4zeroEv:
.LFB133:
	.seh_endprologue
	movq	%rcx, %rax
	movq	$0, (%rcx)
	movl	$0, 8(%rcx)
	movb	$1, 12(%rcx)
	ret
	.seh_endproc
	.section	.text$_ZN2ec8JacobianIN2fp7FpNaiveILj4294966177EEEE3addERKS4_S6_,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZN2ec8JacobianIN2fp7FpNaiveILj4294966177EEEE3addERKS4_S6_
	.def	_ZN2ec8JacobianIN2fp7FpNaiveILj4294966177EEEE3addERKS4_S6_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN2ec8JacobianIN2fp7FpNaiveILj4294966177EEEE3addERKS4_S6_
_ZN2ec8JacobianIN2fp7FpNaiveILj4294966177EEEE3addERKS4_S6_:
.LFB119:
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
	subq	$56, %rsp
	.seh_stackalloc	56
	.seh_endprologue
	movq	%rcx, %rdi
	movzbl	12(%rdx), %ecx
	movq	%rdx, %rbx
	movq	%r8, %rsi
	call	_ZNK2ec8JacobianIN2fp7FpNaiveILj4294966177EEEE7is_zeroEv.isra.0
	testb	%al, %al
	je	.L56
	vmovdqu	(%r8), %xmm0
	vmovdqu	%xmm0, (%rdi)
.L55:
	movq	%rdi, %rax
	addq	$56, %rsp
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
.L56:
	movzbl	12(%r8), %ecx
	call	_ZNK2ec8JacobianIN2fp7FpNaiveILj4294966177EEEE7is_zeroEv.isra.0
	testb	%al, %al
	je	.L58
	vmovdqu	(%rdx), %xmm0
	vmovdqu	%xmm0, (%rdi)
	jmp	.L55
	.p2align 4
	.p2align 3
.L58:
	movl	8(%rdx), %r14d
	movl	%r14d, %ecx
	movl	%r14d, %r13d
	call	_ZN2fp7FpNaiveILj4294966177EE3sqrEj
	movl	8(%rsi), %r15d
	movl	%eax, %r12d
	movl	%r15d, %ecx
	movl	%r15d, 44(%rsp)
	call	_ZN2fp7FpNaiveILj4294966177EE3sqrEj
	movl	(%rbx), %ecx
	movl	%eax, %edx
	movl	%eax, 40(%rsp)
	call	_ZN2fp7FpNaiveILj4294966177EE3mulEjj
	movl	(%rsi), %ecx
	movl	%r12d, %edx
	movl	%eax, %ebp
	call	_ZN2fp7FpNaiveILj4294966177EE3mulEjj
	movl	40(%rsp), %ecx
	movl	%r15d, %edx
	movl	%eax, 36(%rsp)
	call	_ZN2fp7FpNaiveILj4294966177EE3mulEjj
	movl	4(%rbx), %ecx
	movl	%eax, %edx
	call	_ZN2fp7FpNaiveILj4294966177EE3mulEjj
	movl	%r14d, %edx
	movl	%r12d, %ecx
	movl	%eax, %r15d
	call	_ZN2fp7FpNaiveILj4294966177EE3mulEjj
	movl	4(%rsi), %ecx
	movl	%eax, %edx
	call	_ZN2fp7FpNaiveILj4294966177EE3mulEjj
	movl	36(%rsp), %r9d
	movl	%eax, %esi
	cmpl	%r9d, %ebp
	je	.L61
	movl	%r9d, %ecx
	movl	%ebp, %edx
	movl	%ebp, %r14d
	movl	%r15d, %ebp
	call	_ZN2fp7FpNaiveILj4294966177EE3subEjj
	movl	%r15d, %edx
	movl	%esi, %ecx
	movl	%eax, %ebx
	call	_ZN2fp7FpNaiveILj4294966177EE3subEjj
	movl	%ebx, %ecx
	movl	%eax, %esi
	call	_ZN2fp7FpNaiveILj4294966177EE3sqrEj
	movl	%ebx, %ecx
	movl	%eax, %edx
	movl	%eax, 36(%rsp)
	call	_ZN2fp7FpNaiveILj4294966177EE3mulEjj
	movl	%r14d, %ecx
	movl	36(%rsp), %edx
	movl	%eax, %r15d
	call	_ZN2fp7FpNaiveILj4294966177EE3mulEjj
	movl	%eax, %edx
	movl	%eax, %ecx
	movl	%eax, 36(%rsp)
	call	_ZN2fp7FpNaiveILj4294966177EE3addEjj
	movl	%esi, %ecx
	movl	%eax, %r14d
	call	_ZN2fp7FpNaiveILj4294966177EE3sqrEj
	movl	%r15d, %edx
	movl	%eax, %ecx
	call	_ZN2fp7FpNaiveILj4294966177EE3subEjj
	movl	%r14d, %edx
	movl	%eax, %ecx
	call	_ZN2fp7FpNaiveILj4294966177EE3subEjj
	movl	%r15d, %edx
	movl	%ebp, %ecx
	movl	%eax, %r14d
	call	_ZN2fp7FpNaiveILj4294966177EE3mulEjj
	movl	36(%rsp), %ecx
	movl	%r14d, %edx
	movl	%eax, %r15d
	call	_ZN2fp7FpNaiveILj4294966177EE3subEjj
	movl	%esi, %ecx
	movl	%eax, %edx
	call	_ZN2fp7FpNaiveILj4294966177EE3mulEjj
	movl	%r15d, %edx
	movl	%eax, %ecx
	call	_ZN2fp7FpNaiveILj4294966177EE3subEjj
	movl	44(%rsp), %edx
	movl	%r13d, %ecx
	movl	%eax, %esi
	call	_ZN2fp7FpNaiveILj4294966177EE3mulEjj
	movl	%ebx, %edx
	movl	%eax, %ecx
	call	_ZN2fp7FpNaiveILj4294966177EE3mulEjj
	movl	%esi, %r8d
	movl	%r14d, %edx
	movq	%rdi, %rcx
	movl	%eax, %r9d
	call	_ZN2ec8JacobianIN2fp7FpNaiveILj4294966177EEEE14from_affine_xzEjjj
	jmp	.L55
	.p2align 4
	.p2align 3
.L61:
	cmpl	%eax, %r15d
	je	.L62
	movq	%rdi, %rcx
	call	_ZN2ec8JacobianIN2fp7FpNaiveILj4294966177EEEE4zeroEv
	jmp	.L55
	.p2align 4
	.p2align 3
.L62:
	movq	%rbx, %rdx
	movq	%rdi, %rcx
	call	_ZN2ec8JacobianIN2fp7FpNaiveILj4294966177EEEE3dblERKS4_
	jmp	.L55
	.seh_endproc
	.section	.text$_Z10probe_jaddIN2fp7FpNaiveILj4294966177EEEEN2ec8JacobianIT_EES6_S6_,"x"
	.linkonce discard
	.p2align 4
	.globl	_Z10probe_jaddIN2fp7FpNaiveILj4294966177EEEEN2ec8JacobianIT_EES6_S6_
	.def	_Z10probe_jaddIN2fp7FpNaiveILj4294966177EEEEN2ec8JacobianIT_EES6_S6_;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10probe_jaddIN2fp7FpNaiveILj4294966177EEEEN2ec8JacobianIT_EES6_S6_
_Z10probe_jaddIN2fp7FpNaiveILj4294966177EEEEN2ec8JacobianIT_EES6_S6_:
.LFB106:
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$64, %rsp
	.seh_stackalloc	64
	.seh_endprologue
	vmovdqu	(%rdx), %xmm0
	movq	%rcx, %rbx
	leaq	48(%rsp), %rdx
	vmovdqa	%xmm0, 48(%rsp)
	vmovdqu	(%r8), %xmm0
	leaq	32(%rsp), %r8
	vmovdqa	%xmm0, 32(%rsp)
	call	_ZN2ec8JacobianIN2fp7FpNaiveILj4294966177EEEE3addERKS4_S6_
	movq	%rbx, %rax
	addq	$64, %rsp
	popq	%rbx
	ret
	.seh_endproc
	.section	.text$_ZN2fp9FpBarrettILj4294966177EE3sqrEj,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZN2fp9FpBarrettILj4294966177EE3sqrEj
	.def	_ZN2fp9FpBarrettILj4294966177EE3sqrEj;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN2fp9FpBarrettILj4294966177EE3sqrEj
_ZN2fp9FpBarrettILj4294966177EE3sqrEj:
.LFB137:
	.seh_endprologue
	movl	%ecx, %ecx
	imulq	%rcx, %rcx
	jmp	_ZN2fp9FpBarrettILj4294966177EE8reduce64Ey
	.seh_endproc
	.section	.text$_ZN2fp9FpBarrettILj4294966177EE3addEjj,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZN2fp9FpBarrettILj4294966177EE3addEjj
	.def	_ZN2fp9FpBarrettILj4294966177EE3addEjj;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN2fp9FpBarrettILj4294966177EE3addEjj
_ZN2fp9FpBarrettILj4294966177EE3addEjj:
.LFB138:
	.seh_endprologue
	movl	%edx, %r8d
	movl	%ecx, %eax
	addq	%r8, %rax
	leal	1119(%rcx,%rdx), %r8d
	addl	%edx, %ecx
	movl	$4294966176, %edx
	cmpq	%rax, %rdx
	movl	%r8d, %eax
	cmovnb	%ecx, %eax
	ret
	.seh_endproc
	.section	.text$_ZN2fp9FpBarrettILj4294966177EE3subEjj,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZN2fp9FpBarrettILj4294966177EE3subEjj
	.def	_ZN2fp9FpBarrettILj4294966177EE3subEjj;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN2fp9FpBarrettILj4294966177EE3subEjj
_ZN2fp9FpBarrettILj4294966177EE3subEjj:
.LFB139:
	.seh_endprologue
	movl	%ecx, %r8d
	movl	%edx, %ecx
	movl	%r8d, %edx
	subl	%ecx, %edx
	cmpl	%ecx, %r8d
	leal	-1119(%rdx), %eax
	cmovnb	%edx, %eax
	ret
	.seh_endproc
	.section	.text$_ZN2ec8JacobianIN2fp9FpBarrettILj4294966177EEEE14from_affine_xzEjjj,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZN2ec8JacobianIN2fp9FpBarrettILj4294966177EEEE14from_affine_xzEjjj
	.def	_ZN2ec8JacobianIN2fp9FpBarrettILj4294966177EEEE14from_affine_xzEjjj;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN2ec8JacobianIN2fp9FpBarrettILj4294966177EEEE14from_affine_xzEjjj
_ZN2ec8JacobianIN2fp9FpBarrettILj4294966177EEEE14from_affine_xzEjjj:
.LFB140:
	.seh_endprologue
	movq	%rcx, %rax
	movl	%edx, (%rcx)
	movl	%r8d, 4(%rcx)
	movl	%r9d, 8(%rcx)
	movb	$0, 12(%rcx)
	ret
	.seh_endproc
	.section	.text$_ZN2ec8JacobianIN2fp9FpBarrettILj4294966177EEEE3dblERKS4_,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZN2ec8JacobianIN2fp9FpBarrettILj4294966177EEEE3dblERKS4_
	.def	_ZN2ec8JacobianIN2fp9FpBarrettILj4294966177EEEE3dblERKS4_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN2ec8JacobianIN2fp9FpBarrettILj4294966177EEEE3dblERKS4_
_ZN2ec8JacobianIN2fp9FpBarrettILj4294966177EEEE3dblERKS4_:
.LFB121:
	pushq	%r15
	.seh_pushreg	%r15
	pushq	%r14
	.seh_pushreg	%r14
	pushq	%rbp
	.seh_pushreg	%rbp
	pushq	%rdi
	.seh_pushreg	%rdi
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$56, %rsp
	.seh_stackalloc	56
	.seh_endprologue
	movq	%rcx, %rbp
	movzbl	12(%rdx), %ecx
	movq	%rdx, %rbx
	call	_ZNK2ec8JacobianIN2fp9FpBarrettILj4294966177EEEE7is_zeroEv.isra.0
	testb	%al, %al
	je	.L73
	vmovdqu	(%rdx), %xmm0
	movq	%rbp, %rax
	vmovdqu	%xmm0, 0(%rbp)
	addq	$56, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r14
	popq	%r15
	ret
	.p2align 4
	.p2align 3
.L73:
	movl	(%rdx), %esi
	movl	%esi, %ecx
	call	_ZN2fp9FpBarrettILj4294966177EE3sqrEj
	movl	4(%rbx), %r9d
	movl	%eax, %edi
	movl	%r9d, %ecx
	movl	%r9d, 44(%rsp)
	call	_ZN2fp9FpBarrettILj4294966177EE3sqrEj
	movl	%eax, %edx
	movl	%eax, %ecx
	movl	%eax, 40(%rsp)
	call	_ZN2fp9FpBarrettILj4294966177EE3addEjj
	movl	%esi, %ecx
	movl	%eax, %edx
	call	_ZN2fp9FpBarrettILj4294966177EE3mulEjj
	movl	%eax, %edx
	movl	%eax, %ecx
	call	_ZN2fp9FpBarrettILj4294966177EE3addEjj
	movl	%edi, %edx
	movl	%edi, %ecx
	movl	%eax, %esi
	call	_ZN2fp9FpBarrettILj4294966177EE3addEjj
	movl	%edi, %ecx
	movl	%eax, %edx
	call	_ZN2fp9FpBarrettILj4294966177EE3addEjj
	movl	%esi, %edx
	movl	%esi, %ecx
	movl	%eax, %r14d
	call	_ZN2fp9FpBarrettILj4294966177EE3addEjj
	movl	%r14d, %ecx
	movl	%eax, %edi
	call	_ZN2fp9FpBarrettILj4294966177EE3sqrEj
	movl	%edi, %edx
	movl	%eax, %ecx
	call	_ZN2fp9FpBarrettILj4294966177EE3subEjj
	movl	8(%rbx), %ecx
	movl	%eax, %edi
	movl	%ecx, %edx
	call	_ZN2fp9FpBarrettILj4294966177EE3addEjj
	movl	44(%rsp), %edx
	movl	%eax, %ecx
	call	_ZN2fp9FpBarrettILj4294966177EE3mulEjj
	movl	40(%rsp), %ecx
	movl	%eax, %ebx
	call	_ZN2fp9FpBarrettILj4294966177EE3sqrEj
	movl	%eax, %edx
	movl	%eax, %ecx
	call	_ZN2fp9FpBarrettILj4294966177EE3addEjj
	movl	%eax, %edx
	movl	%eax, %ecx
	call	_ZN2fp9FpBarrettILj4294966177EE3addEjj
	movl	%eax, %edx
	movl	%eax, %ecx
	call	_ZN2fp9FpBarrettILj4294966177EE3addEjj
	movl	%edi, %edx
	movl	%esi, %ecx
	movl	%eax, %r15d
	call	_ZN2fp9FpBarrettILj4294966177EE3subEjj
	movl	%r14d, %ecx
	movl	%eax, %edx
	call	_ZN2fp9FpBarrettILj4294966177EE3mulEjj
	movl	%r15d, %edx
	movl	%eax, %ecx
	call	_ZN2fp9FpBarrettILj4294966177EE3subEjj
	movl	%ebx, %r9d
	movl	%edi, %edx
	movq	%rbp, %rcx
	movl	%eax, %r8d
	call	_ZN2ec8JacobianIN2fp9FpBarrettILj4294966177EEEE14from_affine_xzEjjj
	movq	%rbp, %rax
	addq	$56, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r14
	popq	%r15
	ret
	.seh_endproc
	.section	.text$_Z10probe_jdblIN2fp9FpBarrettILj4294966177EEEEN2ec8JacobianIT_EES6_,"x"
	.linkonce discard
	.p2align 4
	.globl	_Z10probe_jdblIN2fp9FpBarrettILj4294966177EEEEN2ec8JacobianIT_EES6_
	.def	_Z10probe_jdblIN2fp9FpBarrettILj4294966177EEEEN2ec8JacobianIT_EES6_;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10probe_jdblIN2fp9FpBarrettILj4294966177EEEEN2ec8JacobianIT_EES6_
_Z10probe_jdblIN2fp9FpBarrettILj4294966177EEEEN2ec8JacobianIT_EES6_:
.LFB108:
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$48, %rsp
	.seh_stackalloc	48
	.seh_endprologue
	vmovdqu	(%rdx), %xmm0
	movq	%rcx, %rbx
	leaq	32(%rsp), %rdx
	vmovdqa	%xmm0, 32(%rsp)
	call	_ZN2ec8JacobianIN2fp9FpBarrettILj4294966177EEEE3dblERKS4_
	movq	%rbx, %rax
	addq	$48, %rsp
	popq	%rbx
	ret
	.seh_endproc
	.section	.text$_ZN2fp6FpMontILj4294966177EE3sqrEj,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZN2fp6FpMontILj4294966177EE3sqrEj
	.def	_ZN2fp6FpMontILj4294966177EE3sqrEj;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN2fp6FpMontILj4294966177EE3sqrEj
_ZN2fp6FpMontILj4294966177EE3sqrEj:
.LFB142:
	.seh_endprologue
	movl	%ecx, %edx
	jmp	_ZN2fp6FpMontILj4294966177EE3mulEjj
	.seh_endproc
	.section	.text$_ZN2fp6FpMontILj4294966177EE3addEjj,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZN2fp6FpMontILj4294966177EE3addEjj
	.def	_ZN2fp6FpMontILj4294966177EE3addEjj;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN2fp6FpMontILj4294966177EE3addEjj
_ZN2fp6FpMontILj4294966177EE3addEjj:
.LFB143:
	.seh_endprologue
	movl	%edx, %r8d
	movl	%ecx, %eax
	addq	%r8, %rax
	leal	1119(%rcx,%rdx), %r8d
	addl	%edx, %ecx
	movl	$4294966176, %edx
	cmpq	%rax, %rdx
	movl	%r8d, %eax
	cmovnb	%ecx, %eax
	ret
	.seh_endproc
	.section	.text$_ZN2fp6FpMontILj4294966177EE3subEjj,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZN2fp6FpMontILj4294966177EE3subEjj
	.def	_ZN2fp6FpMontILj4294966177EE3subEjj;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN2fp6FpMontILj4294966177EE3subEjj
_ZN2fp6FpMontILj4294966177EE3subEjj:
.LFB144:
	.seh_endprologue
	movl	%ecx, %r8d
	movl	%edx, %ecx
	movl	%r8d, %edx
	subl	%ecx, %edx
	cmpl	%ecx, %r8d
	leal	-1119(%rdx), %eax
	cmovnb	%edx, %eax
	ret
	.seh_endproc
	.section	.text$_ZN2ec8JacobianIN2fp6FpMontILj4294966177EEEE14from_affine_xzEjjj,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZN2ec8JacobianIN2fp6FpMontILj4294966177EEEE14from_affine_xzEjjj
	.def	_ZN2ec8JacobianIN2fp6FpMontILj4294966177EEEE14from_affine_xzEjjj;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN2ec8JacobianIN2fp6FpMontILj4294966177EEEE14from_affine_xzEjjj
_ZN2ec8JacobianIN2fp6FpMontILj4294966177EEEE14from_affine_xzEjjj:
.LFB145:
	.seh_endprologue
	movq	%rcx, %rax
	movl	%edx, (%rcx)
	movl	%r8d, 4(%rcx)
	movl	%r9d, 8(%rcx)
	movb	$0, 12(%rcx)
	ret
	.seh_endproc
	.section	.text$_ZN2ec8JacobianIN2fp6FpMontILj4294966177EEEE3dblERKS4_,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZN2ec8JacobianIN2fp6FpMontILj4294966177EEEE3dblERKS4_
	.def	_ZN2ec8JacobianIN2fp6FpMontILj4294966177EEEE3dblERKS4_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN2ec8JacobianIN2fp6FpMontILj4294966177EEEE3dblERKS4_
_ZN2ec8JacobianIN2fp6FpMontILj4294966177EEEE3dblERKS4_:
.LFB122:
	pushq	%r15
	.seh_pushreg	%r15
	pushq	%r14
	.seh_pushreg	%r14
	pushq	%rbp
	.seh_pushreg	%rbp
	pushq	%rdi
	.seh_pushreg	%rdi
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$56, %rsp
	.seh_stackalloc	56
	.seh_endprologue
	movq	%rcx, %rbp
	movzbl	12(%rdx), %ecx
	movq	%rdx, %rbx
	call	_ZNK2ec8JacobianIN2fp6FpMontILj4294966177EEEE7is_zeroEv.isra.0
	testb	%al, %al
	je	.L85
	vmovdqu	(%rdx), %xmm0
	movq	%rbp, %rax
	vmovdqu	%xmm0, 0(%rbp)
	addq	$56, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r14
	popq	%r15
	ret
	.p2align 4
	.p2align 3
.L85:
	movl	(%rdx), %esi
	movl	%esi, %ecx
	call	_ZN2fp6FpMontILj4294966177EE3sqrEj
	movl	4(%rbx), %r9d
	movl	%eax, %edi
	movl	%r9d, %ecx
	movl	%r9d, 44(%rsp)
	call	_ZN2fp6FpMontILj4294966177EE3sqrEj
	movl	%eax, %edx
	movl	%eax, %ecx
	movl	%eax, 40(%rsp)
	call	_ZN2fp6FpMontILj4294966177EE3addEjj
	movl	%esi, %ecx
	movl	%eax, %edx
	call	_ZN2fp6FpMontILj4294966177EE3mulEjj
	movl	%eax, %edx
	movl	%eax, %ecx
	call	_ZN2fp6FpMontILj4294966177EE3addEjj
	movl	%edi, %edx
	movl	%edi, %ecx
	movl	%eax, %esi
	call	_ZN2fp6FpMontILj4294966177EE3addEjj
	movl	%edi, %ecx
	movl	%eax, %edx
	call	_ZN2fp6FpMontILj4294966177EE3addEjj
	movl	%esi, %edx
	movl	%esi, %ecx
	movl	%eax, %r14d
	call	_ZN2fp6FpMontILj4294966177EE3addEjj
	movl	%r14d, %ecx
	movl	%eax, %edi
	call	_ZN2fp6FpMontILj4294966177EE3sqrEj
	movl	%edi, %edx
	movl	%eax, %ecx
	call	_ZN2fp6FpMontILj4294966177EE3subEjj
	movl	8(%rbx), %ecx
	movl	%eax, %edi
	movl	%ecx, %edx
	call	_ZN2fp6FpMontILj4294966177EE3addEjj
	movl	44(%rsp), %edx
	movl	%eax, %ecx
	call	_ZN2fp6FpMontILj4294966177EE3mulEjj
	movl	40(%rsp), %ecx
	movl	%eax, %ebx
	call	_ZN2fp6FpMontILj4294966177EE3sqrEj
	movl	%eax, %edx
	movl	%eax, %ecx
	call	_ZN2fp6FpMontILj4294966177EE3addEjj
	movl	%eax, %edx
	movl	%eax, %ecx
	call	_ZN2fp6FpMontILj4294966177EE3addEjj
	movl	%eax, %edx
	movl	%eax, %ecx
	call	_ZN2fp6FpMontILj4294966177EE3addEjj
	movl	%edi, %edx
	movl	%esi, %ecx
	movl	%eax, %r15d
	call	_ZN2fp6FpMontILj4294966177EE3subEjj
	movl	%r14d, %ecx
	movl	%eax, %edx
	call	_ZN2fp6FpMontILj4294966177EE3mulEjj
	movl	%r15d, %edx
	movl	%eax, %ecx
	call	_ZN2fp6FpMontILj4294966177EE3subEjj
	movl	%ebx, %r9d
	movl	%edi, %edx
	movq	%rbp, %rcx
	movl	%eax, %r8d
	call	_ZN2ec8JacobianIN2fp6FpMontILj4294966177EEEE14from_affine_xzEjjj
	movq	%rbp, %rax
	addq	$56, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r14
	popq	%r15
	ret
	.seh_endproc
	.section	.text$_Z10probe_jdblIN2fp6FpMontILj4294966177EEEEN2ec8JacobianIT_EES6_,"x"
	.linkonce discard
	.p2align 4
	.globl	_Z10probe_jdblIN2fp6FpMontILj4294966177EEEEN2ec8JacobianIT_EES6_
	.def	_Z10probe_jdblIN2fp6FpMontILj4294966177EEEEN2ec8JacobianIT_EES6_;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10probe_jdblIN2fp6FpMontILj4294966177EEEEN2ec8JacobianIT_EES6_
_Z10probe_jdblIN2fp6FpMontILj4294966177EEEEN2ec8JacobianIT_EES6_:
.LFB109:
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$48, %rsp
	.seh_stackalloc	48
	.seh_endprologue
	vmovdqu	(%rdx), %xmm0
	movq	%rcx, %rbx
	leaq	32(%rsp), %rdx
	vmovdqa	%xmm0, 32(%rsp)
	call	_ZN2ec8JacobianIN2fp6FpMontILj4294966177EEEE3dblERKS4_
	movq	%rbx, %rax
	addq	$48, %rsp
	popq	%rbx
	ret
	.seh_endproc
	.section	.text$_ZN2fp8FpPseudoILj4294966177EE3sqrEj,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZN2fp8FpPseudoILj4294966177EE3sqrEj
	.def	_ZN2fp8FpPseudoILj4294966177EE3sqrEj;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN2fp8FpPseudoILj4294966177EE3sqrEj
_ZN2fp8FpPseudoILj4294966177EE3sqrEj:
.LFB147:
	.seh_endprologue
	movl	%ecx, %ecx
	imulq	%rcx, %rcx
	jmp	_ZN2fp8FpPseudoILj4294966177EE8reduce64Ey
	.seh_endproc
	.section	.text$_ZN2fp8FpPseudoILj4294966177EE3addEjj,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZN2fp8FpPseudoILj4294966177EE3addEjj
	.def	_ZN2fp8FpPseudoILj4294966177EE3addEjj;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN2fp8FpPseudoILj4294966177EE3addEjj
_ZN2fp8FpPseudoILj4294966177EE3addEjj:
.LFB148:
	.seh_endprologue
	movl	%edx, %r8d
	movl	%ecx, %eax
	addq	%r8, %rax
	leal	1119(%rcx,%rdx), %r8d
	addl	%edx, %ecx
	movl	$4294966176, %edx
	cmpq	%rax, %rdx
	movl	%r8d, %eax
	cmovnb	%ecx, %eax
	ret
	.seh_endproc
	.section	.text$_ZN2ec8JacobianIN2fp8FpPseudoILj4294966177EEEE14from_affine_xzEjjj,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZN2ec8JacobianIN2fp8FpPseudoILj4294966177EEEE14from_affine_xzEjjj
	.def	_ZN2ec8JacobianIN2fp8FpPseudoILj4294966177EEEE14from_affine_xzEjjj;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN2ec8JacobianIN2fp8FpPseudoILj4294966177EEEE14from_affine_xzEjjj
_ZN2ec8JacobianIN2fp8FpPseudoILj4294966177EEEE14from_affine_xzEjjj:
.LFB149:
	.seh_endprologue
	movq	%rcx, %rax
	movl	%edx, (%rcx)
	movl	%r8d, 4(%rcx)
	movl	%r9d, 8(%rcx)
	movb	$0, 12(%rcx)
	ret
	.seh_endproc
	.section	.text$_ZN2ec8JacobianIN2fp8FpPseudoILj4294966177EEEE3dblERKS4_,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZN2ec8JacobianIN2fp8FpPseudoILj4294966177EEEE3dblERKS4_
	.def	_ZN2ec8JacobianIN2fp8FpPseudoILj4294966177EEEE3dblERKS4_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN2ec8JacobianIN2fp8FpPseudoILj4294966177EEEE3dblERKS4_
_ZN2ec8JacobianIN2fp8FpPseudoILj4294966177EEEE3dblERKS4_:
.LFB123:
	pushq	%r15
	.seh_pushreg	%r15
	pushq	%r14
	.seh_pushreg	%r14
	pushq	%rbp
	.seh_pushreg	%rbp
	pushq	%rdi
	.seh_pushreg	%rdi
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$56, %rsp
	.seh_stackalloc	56
	.seh_endprologue
	movq	%rcx, %rbp
	movzbl	12(%rdx), %ecx
	movq	%rdx, %rbx
	call	_ZNK2ec8JacobianIN2fp8FpPseudoILj4294966177EEEE7is_zeroEv.isra.0
	testb	%al, %al
	je	.L94
	vmovdqu	(%rdx), %xmm0
	movq	%rbp, %rax
	vmovdqu	%xmm0, 0(%rbp)
	addq	$56, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r14
	popq	%r15
	ret
	.p2align 4
	.p2align 3
.L94:
	movl	(%rdx), %esi
	movl	%esi, %ecx
	call	_ZN2fp8FpPseudoILj4294966177EE3sqrEj
	movl	4(%rbx), %r9d
	movl	%eax, %edi
	movl	%r9d, %ecx
	movl	%r9d, 44(%rsp)
	call	_ZN2fp8FpPseudoILj4294966177EE3sqrEj
	movl	%eax, %edx
	movl	%eax, %ecx
	movl	%eax, 40(%rsp)
	call	_ZN2fp8FpPseudoILj4294966177EE3addEjj
	movl	%esi, %ecx
	movl	%eax, %edx
	call	_ZN2fp8FpPseudoILj4294966177EE3mulEjj
	movl	%eax, %edx
	movl	%eax, %ecx
	call	_ZN2fp8FpPseudoILj4294966177EE3addEjj
	movl	%edi, %edx
	movl	%edi, %ecx
	movl	%eax, %esi
	call	_ZN2fp8FpPseudoILj4294966177EE3addEjj
	movl	%edi, %ecx
	movl	%eax, %edx
	call	_ZN2fp8FpPseudoILj4294966177EE3addEjj
	movl	%esi, %edx
	movl	%esi, %ecx
	movl	%eax, %r14d
	call	_ZN2fp8FpPseudoILj4294966177EE3addEjj
	movl	%r14d, %ecx
	movl	%eax, %edi
	call	_ZN2fp8FpPseudoILj4294966177EE3sqrEj
	movl	%edi, %edx
	movl	%eax, %ecx
	call	_ZN2fp8FpPseudoILj4294966177EE3subEjj
	movl	8(%rbx), %ecx
	movl	%eax, %edi
	movl	%ecx, %edx
	call	_ZN2fp8FpPseudoILj4294966177EE3addEjj
	movl	44(%rsp), %edx
	movl	%eax, %ecx
	call	_ZN2fp8FpPseudoILj4294966177EE3mulEjj
	movl	40(%rsp), %ecx
	movl	%eax, %ebx
	call	_ZN2fp8FpPseudoILj4294966177EE3sqrEj
	movl	%eax, %edx
	movl	%eax, %ecx
	call	_ZN2fp8FpPseudoILj4294966177EE3addEjj
	movl	%eax, %edx
	movl	%eax, %ecx
	call	_ZN2fp8FpPseudoILj4294966177EE3addEjj
	movl	%eax, %edx
	movl	%eax, %ecx
	call	_ZN2fp8FpPseudoILj4294966177EE3addEjj
	movl	%edi, %edx
	movl	%esi, %ecx
	movl	%eax, %r15d
	call	_ZN2fp8FpPseudoILj4294966177EE3subEjj
	movl	%r14d, %ecx
	movl	%eax, %edx
	call	_ZN2fp8FpPseudoILj4294966177EE3mulEjj
	movl	%r15d, %edx
	movl	%eax, %ecx
	call	_ZN2fp8FpPseudoILj4294966177EE3subEjj
	movl	%ebx, %r9d
	movl	%edi, %edx
	movq	%rbp, %rcx
	movl	%eax, %r8d
	call	_ZN2ec8JacobianIN2fp8FpPseudoILj4294966177EEEE14from_affine_xzEjjj
	movq	%rbp, %rax
	addq	$56, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r14
	popq	%r15
	ret
	.seh_endproc
	.section	.text$_Z10probe_jdblIN2fp8FpPseudoILj4294966177EEEEN2ec8JacobianIT_EES6_,"x"
	.linkonce discard
	.p2align 4
	.globl	_Z10probe_jdblIN2fp8FpPseudoILj4294966177EEEEN2ec8JacobianIT_EES6_
	.def	_Z10probe_jdblIN2fp8FpPseudoILj4294966177EEEEN2ec8JacobianIT_EES6_;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10probe_jdblIN2fp8FpPseudoILj4294966177EEEEN2ec8JacobianIT_EES6_
_Z10probe_jdblIN2fp8FpPseudoILj4294966177EEEEN2ec8JacobianIT_EES6_:
.LFB110:
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$48, %rsp
	.seh_stackalloc	48
	.seh_endprologue
	vmovdqu	(%rdx), %xmm0
	movq	%rcx, %rbx
	leaq	32(%rsp), %rdx
	vmovdqa	%xmm0, 32(%rsp)
	call	_ZN2ec8JacobianIN2fp8FpPseudoILj4294966177EEEE3dblERKS4_
	movq	%rbx, %rax
	addq	$48, %rsp
	popq	%rbx
	ret
	.seh_endproc
	.section	.text$_ZN2fp7FpNaiveILj4294966177EE8from_rawEj,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZN2fp7FpNaiveILj4294966177EE8from_rawEj
	.def	_ZN2fp7FpNaiveILj4294966177EE8from_rawEj;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN2fp7FpNaiveILj4294966177EE8from_rawEj
_ZN2fp7FpNaiveILj4294966177EE8from_rawEj:
.LFB151:
	.seh_endprologue
	xorl	%eax, %eax
	cmpl	$-1119, %ecx
	setnb	%al
	imull	$-1119, %eax, %edx
	movl	%ecx, %eax
	subl	%edx, %eax
	ret
	.seh_endproc
	.section	.text$_ZN2ec8JacobianIN2fp7FpNaiveILj4294966177EEEE11from_affineEjj,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZN2ec8JacobianIN2fp7FpNaiveILj4294966177EEEE11from_affineEjj
	.def	_ZN2ec8JacobianIN2fp7FpNaiveILj4294966177EEEE11from_affineEjj;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN2ec8JacobianIN2fp7FpNaiveILj4294966177EEEE11from_affineEjj
_ZN2ec8JacobianIN2fp7FpNaiveILj4294966177EEEE11from_affineEjj:
.LFB134:
	pushq	%rdi
	.seh_pushreg	%rdi
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$32, %rsp
	.seh_stackalloc	32
	.seh_endprologue
	movl	%edx, %edi
	movq	%rcx, %rbx
	movl	%r8d, %ecx
	call	_ZN2fp7FpNaiveILj4294966177EE8from_rawEj
	movl	%edi, %ecx
	movl	%eax, %esi
	call	_ZN2fp7FpNaiveILj4294966177EE8from_rawEj
	movl	$1, %r9d
	movq	%rbx, %rcx
	movl	%eax, %edx
	movl	%esi, %r8d
	call	_ZN2ec8JacobianIN2fp7FpNaiveILj4294966177EEEE14from_affine_xzEjjj
	movq	%rbx, %rax
	addq	$32, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	ret
	.seh_endproc
	.text
	.p2align 4
	.def	_ZN2ec8JacobianIN2fp7FpNaiveILj4294966177EEEE10add_affineERKS4_RKNS_6AffineIS3_EE.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZN2ec8JacobianIN2fp7FpNaiveILj4294966177EEEE10add_affineERKS4_RKNS_6AffineIS3_EE.isra.0
_ZN2ec8JacobianIN2fp7FpNaiveILj4294966177EEEE10add_affineERKS4_RKNS_6AffineIS3_EE.isra.0:
.LFB159:
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
	subq	$56, %rsp
	.seh_stackalloc	56
	.seh_endprologue
	movq	%rcx, %rsi
	movzbl	12(%rdx), %ecx
	movq	%rdx, %rbx
	movl	%r8d, %ebp
	movl	%r9d, %edi
	call	_ZNK2ec8JacobianIN2fp7FpNaiveILj4294966177EEEE7is_zeroEv.isra.0
	testb	%al, %al
	je	.L100
	movl	%r9d, %r8d
	movl	%ebp, %edx
	movq	%rsi, %rcx
	call	_ZN2ec8JacobianIN2fp7FpNaiveILj4294966177EEEE11from_affineEjj
.L99:
	movq	%rsi, %rax
	addq	$56, %rsp
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
.L100:
	movzbl	160(%rsp), %ecx
	call	_ZNK2ec6AffineIN2fp7FpNaiveILj4294966177EEEE7is_zeroEv.isra.0
	testb	%al, %al
	je	.L102
	vmovdqu	(%rdx), %xmm0
	vmovdqu	%xmm0, (%rsi)
	jmp	.L99
	.p2align 4
	.p2align 3
.L102:
	movl	8(%rdx), %r14d
	movl	%r14d, %ecx
	movl	%r14d, %r13d
	call	_ZN2fp7FpNaiveILj4294966177EE3sqrEj
	movl	%ebp, %ecx
	movl	%eax, %edx
	movl	%eax, 44(%rsp)
	call	_ZN2fp7FpNaiveILj4294966177EE3mulEjj
	movl	%r14d, %edx
	movl	44(%rsp), %ecx
	movl	%eax, %r15d
	call	_ZN2fp7FpNaiveILj4294966177EE3mulEjj
	movl	%edi, %ecx
	movl	%eax, %edx
	call	_ZN2fp7FpNaiveILj4294966177EE3mulEjj
	movl	(%rbx), %edi
	movl	4(%rbx), %ebp
	cmpl	%edi, %r15d
	je	.L105
	movl	%edi, %edx
	movl	%r15d, %ecx
	movl	%eax, 44(%rsp)
	call	_ZN2fp7FpNaiveILj4294966177EE3subEjj
	movl	%ebp, %edx
	movl	44(%rsp), %ecx
	movl	%eax, %ebx
	call	_ZN2fp7FpNaiveILj4294966177EE3subEjj
	movl	%ebx, %ecx
	movl	%eax, %r12d
	call	_ZN2fp7FpNaiveILj4294966177EE3sqrEj
	movl	%ebx, %ecx
	movl	%eax, %edx
	movl	%eax, 44(%rsp)
	call	_ZN2fp7FpNaiveILj4294966177EE3mulEjj
	movl	%edi, %ecx
	movl	44(%rsp), %edx
	movl	%eax, %r14d
	call	_ZN2fp7FpNaiveILj4294966177EE3mulEjj
	movl	%eax, %edx
	movl	%eax, %ecx
	movl	%eax, %edi
	call	_ZN2fp7FpNaiveILj4294966177EE3addEjj
	movl	%r12d, %ecx
	movl	%eax, %r15d
	call	_ZN2fp7FpNaiveILj4294966177EE3sqrEj
	movl	%r14d, %edx
	movl	%eax, %ecx
	call	_ZN2fp7FpNaiveILj4294966177EE3subEjj
	movl	%r15d, %edx
	movl	%eax, %ecx
	call	_ZN2fp7FpNaiveILj4294966177EE3subEjj
	movl	%r14d, %edx
	movl	%ebp, %ecx
	movl	%eax, %r15d
	call	_ZN2fp7FpNaiveILj4294966177EE3mulEjj
	movl	%edi, %ecx
	movl	%r15d, %edx
	movl	%eax, %ebp
	call	_ZN2fp7FpNaiveILj4294966177EE3subEjj
	movl	%r12d, %ecx
	movl	%eax, %edx
	call	_ZN2fp7FpNaiveILj4294966177EE3mulEjj
	movl	%ebp, %edx
	movl	%eax, %ecx
	call	_ZN2fp7FpNaiveILj4294966177EE3subEjj
	movl	%ebx, %edx
	movl	%r13d, %ecx
	movl	%eax, %edi
	call	_ZN2fp7FpNaiveILj4294966177EE3mulEjj
	movl	%r15d, %edx
	movq	%rsi, %rcx
	movl	%eax, %r9d
	movl	%edi, %r8d
	call	_ZN2ec8JacobianIN2fp7FpNaiveILj4294966177EEEE14from_affine_xzEjjj
	jmp	.L99
	.p2align 4
	.p2align 3
.L105:
	cmpl	%eax, %ebp
	je	.L106
	movq	%rsi, %rcx
	call	_ZN2ec8JacobianIN2fp7FpNaiveILj4294966177EEEE4zeroEv
	jmp	.L99
	.p2align 4
	.p2align 3
.L106:
	movq	%rbx, %rdx
	movq	%rsi, %rcx
	call	_ZN2ec8JacobianIN2fp7FpNaiveILj4294966177EEEE3dblERKS4_
	jmp	.L99
	.seh_endproc
	.section	.text$_Z12probe_jmixedIN2fp7FpNaiveILj4294966177EEEEN2ec8JacobianIT_EES6_NS3_6AffineIS5_EE,"x"
	.linkonce discard
	.p2align 4
	.globl	_Z12probe_jmixedIN2fp7FpNaiveILj4294966177EEEEN2ec8JacobianIT_EES6_NS3_6AffineIS5_EE
	.def	_Z12probe_jmixedIN2fp7FpNaiveILj4294966177EEEEN2ec8JacobianIT_EES6_NS3_6AffineIS5_EE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z12probe_jmixedIN2fp7FpNaiveILj4294966177EEEEN2ec8JacobianIT_EES6_NS3_6AffineIS5_EE
_Z12probe_jmixedIN2fp7FpNaiveILj4294966177EEEEN2ec8JacobianIT_EES6_NS3_6AffineIS5_EE:
.LFB107:
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$64, %rsp
	.seh_stackalloc	64
	.seh_endprologue
	vmovdqu	(%rdx), %xmm0
	movzbl	8(%r8), %eax
	movl	%eax, 32(%rsp)
	movl	4(%r8), %r9d
	movl	(%r8), %r8d
	movq	%rcx, %rbx
	leaq	48(%rsp), %rdx
	vmovdqa	%xmm0, 48(%rsp)
	call	_ZN2ec8JacobianIN2fp7FpNaiveILj4294966177EEEE10add_affineERKS4_RKNS_6AffineIS3_EE.isra.0
	movq	%rbx, %rax
	addq	$64, %rsp
	popq	%rbx
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev0, Built by MinGW-Builds project) 16.1.0"
