.equ UseSIMD, 1


.equ _ba,  0*8
.equ _be,  1*8
.equ _bi,  2*8
.equ _bo,  3*8
.equ _bu,  4*8
.equ _ga,  5*8
.equ _ge,  6*8
.equ _gi,  7*8
.equ _go,  8*8
.equ _gu,  9*8
.equ _ka, 10*8
.equ _ke, 11*8
.equ _ki, 12*8
.equ _ko, 13*8
.equ _ku, 14*8
.equ _ma, 15*8
.equ _me, 16*8
.equ _mi, 17*8
.equ _mo, 18*8
.equ _mu, 19*8
.equ _sa, 20*8
.equ _se, 21*8
.equ _si, 22*8
.equ _so, 23*8
.equ _su, 24*8


//	arguments
.equ apState,		%rdi
.equ apInput,		%rsi
.equ aNbrWords,		%rdx

//	xor input into state section
.equ xpState,		%r9

// round vars
.equ rT1,		%rax
.equ rpState,		%rdi
.equ rpStack,		%rsp

.equ rDa,		%rbx
.equ rDe,		%rcx
.equ rDi,		%rdx
.equ rDo,		%r8
.equ rDu,		%r9

.equ rBa,		%r10 
.equ rBe,		%r11
.equ rBi,		%r12
.equ rBo,		%r13
.equ rBu,		%r14

.equ rCa,		%rsi
.equ rCe,		%rbp
.equ rCi,		rBi
.equ rCo,		rBo
.equ rCu,		%r15

.macro	mKeccakRound	iState, oState, rc, lastRound

    xor 64(\iState), %r8  
    mov %rbp, %rbx     
    mov 24(\iState), %r13 
    mov $0x0, %rax     
    rol %rbx           
    mov %rsi, %r9      
    xor 104(\iState), %r13
    xor 144(\iState), %r8 
    xor %r15, %rbx     
    mov 0(\iState), %r10  
    xor %r8, %r13      
    xor 56(\iState), %rdx 
    mov %r15, %r8      
    xor %rbx, %r10     
    mov 192(\iState), %r12
    rol %r9            
    mov %r10, %r15     
    mov 16(\iState), %r14 
    xor %r10, %rax     
    xor %r13, %r9      
    xor 136(\iState), %rdx
    xor 96(\iState), %r14 
    xor %r9, %r12      
    mov 24(\iState), %r11 
    xor %rdx, %r14     
    mov %r13, %rdx     
    rol %r8            
    rol %rdx           
    mov %r14, %rcx     
    xor %rbp, %rdx     
    rol %rcx           
    xor %rsi, %rcx     
    mov 48(\iState), %rbp 
    xor %r14, %r8      
    mov 144(\iState), %r14
    rol $14, %r12      
    xor %r8, %r14      
    xor %rcx, %rbp     
    rol $21, %r14      
    xor %r8, %r11      
    rol $44, %rbp      
    mov %r14, %r13     
    and %rbp, %r15     
    and %r12, %r13     
    xor %r12, %r15     
    or %r10, %r12      
    mov 96(\iState), %r10 
    xor %r14, %r12     
    rol $28, %r11      
    xor %rdx, %r10     
    mov %r12, 24(%\oState) 
    rol $43, %r10      
    mov %rbp, %rsi     
    mov 80(\iState), %r12 
    or %r10, %rsi      
    xor %r10, %r13     
    not %r10           
    or %r14, %r10      
    mov %r15, 32(%\oState) 
    mov 176(\iState), %r14
    xor %rbp, %r10     
    mov %r10, %rbp     
    mov %r10, 8(%\oState)  
    mov 72(\iState), %r10 
    xor %rbx, %r12     
    rol $3, %r12       
    xor %rax, %rsi     
    mov %r13, 16(%\oState) 
    xor %r9, %r10      
    xor %rdx, %r14     
    rol $20, %r10      
    mov 128(\iState), %rax
    mov %r10, %r13     
    rol $61, %r14      
    or %r12, %r13      
    xor %rcx, %rax     
    xor %r11, %r13     
    mov %rsi, 0(%\oState)  
    xor %r13, %rsi     
    mov %r13, 40(%\oState) 
    mov %r14, %r13     
    or %r11, %r13      
    rol $45, %rax      
    xor %rax, %r13     
    and %r10, %r11     
    mov %r13, 64(%\oState) 
    mov %r12, %r13     
    xor %r14, %r11     
    and %rax, %r13     
    xor %r10, %r13     
    mov 56(\iState), %r10 
    xor %r13, %rbp     
    mov %r13, 48(%\oState) 
    xor %rdx, %r10     
    mov 104(\iState), %r13
    not %r14           
    rol $6, %r10       
    xor %r8, %r13      
    mov %r11, 72(%\oState) 
    or %r14, %rax      
    rol $25, %r13      
    xor %r11, %r15     
    mov 8(\iState), %r11  
    xor %r12, %rax     
    mov 152(\iState), %r12
    mov %rax, 56(%\oState) 
    xor %rcx, %r11     
    mov %r10, %r14     
    or %r13, %r14      
    mov 160(\iState), %rax
    xor %r9, %r12      
    rol $1, %r11       
    xor %rbx, %rax     
    xor %r11, %r14     
    rol $18, %rax      
    xor %r14, %rsi     
    mov %r14, 80(%\oState) 
    mov %rax, %r14     
    or %r11, %r14      
    and %r10, %r11     
    xor %rax, %r11     
    xor %r11, %r15     
    rol $8, %r12       
    mov %r11, 112(%\oState)
    mov %r13, %r11     
    and %r12, %r11     
    not %r12           
    xor %r12, %r14     
    xor %r10, %r11     
    mov %r14, 104(%\oState)
    mov %r12, %r14     
    mov 88(\iState), %r12 
    and %rax, %r14     
    xor %r13, %r14     
    mov 136(\iState), %r13
    mov 16(\iState), %r10 
    xor %r11, %rbp     
    mov %r14, 96(%\oState) 
    xor %rdx, %r13     
    xor %rdx, %r10     
    mov 40(\iState), %rdx 
    xor %rcx, %r12     
    mov 112(\iState), %rax
    rol $10, %r12      
    xor %r9, %rax      
    mov 168(\iState), %r14
    mov %r11, 88(%\oState) 
    mov %r12, %r11     
    rol $15, %r13      
    xor %rcx, %r14     
    xor %rbx, %rdx     
    mov 32(\iState), %rcx 
    or %r13, %r11      
    rol $36, %rdx      
    xor %r9, %rcx      
    xor %rdx, %r11     
    xor %r11, %rbp     
    mov %r11, 128(%\oState)
    not %r13           
    mov 184(\iState), %r11
    rol $27, %rcx      
    mov %rdx, %r9      
    xor %r8, %r11      
    or %rcx, %rdx      
    rol $56, %r11      
    and %r12, %r9      
    xor %r11, %rdx     
    rol $2, %r14       
    xor %rdx, %r15     
    mov %rdx, 152(%\oState)
    mov %r13, %rdx     
    rol $39, %rax      
    or %r11, %rdx      
    and %rcx, %r11     
    xor %r12, %rdx     
    mov 120(\iState), %r12
    xor %r13, %r11     
    mov %rdx, 136(%\oState)
    xor %rbx, %r12     
    mov %r11, 144(%\oState)
    xor %rcx, %r9      
    mov 64(\iState), %r11 
    rol $62, %r10      
    mov %rax, %rbx     
    xor %r8, %r11      
    rol $41, %r12      
    mov %r10, %r13     
    xor %r9, %rsi      
    or %r12, %rbx      
    rol $55, %r11      
    mov %r14, %r8      
    and %r11, %r13     
    not %r11           
    xor %r14, %r13     
    xor %r11, %rbx     
    mov %r13, 192(%\oState)
    xor %rbx, %rbp     
    mov %r11, %r11     
    mov %rbx, 168(%\oState)
    mov %r12, %rdx     
    mov %r9, 120(%\oState) 
    and %rax, %r11     
    or %r10, %r8       
    and %r14, %rdx     
    xor %rax, %rdx     
    xor %r12, %r8      
    xor %r13, %r15     
    mov %rdx, 176(%\oState)
    xor %r10, %r11     
    mov %r8, 184(%\oState) 
    xor %r11, %rsi     
    mov %r11, 160(%\oState)

.endm

.macro	mKeccakPermutation	

	subq		$8*25, %rsp

	movq		_ba(rpState), rCa             
	movq		_be(rpState), rCe
	movq		_bu(rpState), rCu

	xorq		_ga(rpState), rCa             
	xorq		_ge(rpState), rCe
	xorq		_gu(rpState), rCu             

	xorq		_ka(rpState), rCa             
	xorq		_ke(rpState), rCe
	xorq		_ku(rpState), rCu             

	xorq		_ma(rpState), rCa             
	xorq		_me(rpState), rCe
	xorq		_mu(rpState), rCu             

	xorq		_sa(rpState), rCa
	xorq		_se(rpState), rCe
	movq		_si(rpState), rDi
	movq		_so(rpState), rDo
	xorq		_su(rpState), rCu             


	mKeccakRound	rpState, rpStack, 0x0000000000000001, 0
	mKeccakRound	rpStack, rpState, 0x0000000000008082, 0
	mKeccakRound	rpState, rpStack, 0x800000000000808a, 0
	mKeccakRound	rpStack, rpState, 0x8000000080008000, 0
	mKeccakRound	rpState, rpStack, 0x000000000000808b, 0
	mKeccakRound	rpStack, rpState, 0x0000000080000001, 0

	mKeccakRound	rpState, rpStack, 0x8000000080008081, 0
	mKeccakRound	rpStack, rpState, 0x8000000000008009, 0
	mKeccakRound	rpState, rpStack, 0x000000000000008a, 0
	mKeccakRound	rpStack, rpState, 0x0000000000000088, 0
	mKeccakRound	rpState, rpStack, 0x0000000080008009, 0
	mKeccakRound	rpStack, rpState, 0x000000008000000a, 0

	mKeccakRound	rpState, rpStack, 0x000000008000808b, 0
	mKeccakRound	rpStack, rpState, 0x800000000000008b, 0
	mKeccakRound	rpState, rpStack, 0x8000000000008089, 0
	mKeccakRound	rpStack, rpState, 0x8000000000008003, 0
	mKeccakRound	rpState, rpStack, 0x8000000000008002, 0
	mKeccakRound	rpStack, rpState, 0x8000000000000080, 0

	mKeccakRound	rpState, rpStack, 0x000000000000800a, 0
	mKeccakRound	rpStack, rpState, 0x800000008000000a, 0
	mKeccakRound	rpState, rpStack, 0x8000000080008081, 0
	mKeccakRound	rpStack, rpState, 0x8000000000008080, 0
	mKeccakRound	rpState, rpStack, 0x0000000080000001, 0
	mKeccakRound	rpStack, rpState, 0x8000000080008008, 1

	addq		$8*25, %rsp

.endm

start:
    mKeccakRound rpState, rpStack, 0x0, 0