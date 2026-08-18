Stalls: 18

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


// arguments
.equ apState,		%rdi
.equ apInput,		%rsi
.equ aNbrWords,		%rdx

// xor input into state section
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

  movq		rCe, rDa
  rolq		rDa

  movq		_bi(\iState), rCi
  xorq		_gi(\iState), rDi
  xorq		rCu, rDa
  xorq		_ki(\iState), rCi
  xorq		_mi(\iState), rDi
  xorq		rDi, rCi

  movq		rCi, rDe
  rolq		rDe

  movq		_bo(\iState), rCo
  xorq		_go(\iState), rDo
  xorq		rCa, rDe
  xorq		_ko(\iState), rCo
  xorq		_mo(\iState), rDo
  xorq		rDo, rCo

  movq		rCo, rDi
  rolq		rDi

  movq		rCu, rDo
  xorq		rCe, rDi
  rolq		rDo

  movq		rCa, rDu
  xorq		rCi, rDo
  rolq		rDu

  movq		_ba(\iState), rBa
  movq		_ge(\iState), rBe
  xorq		rCo, rDu
  movq		_ki(\iState), rBi
  movq		_mo(\iState), rBo
  movq		_su(\iState), rBu
  xorq		rDe, rBe
  rolq		$44, rBe
  xorq		rDi, rBi
  xorq		rDa, rBa
  rolq		$43, rBi

  movq		rBe, rCa
  movq		$\rc, rT1
  orq		rBi, rCa
  xorq		rBa, rT1
  xorq		rT1, rCa
  movq		rCa, _ba(\oState)

  xorq		rDu, rBu
  rolq		$14, rBu
  movq		rBa, rCu
  andq		rBe, rCu
  xorq		rBu, rCu
  movq		rCu, _bu(\oState)

  xorq		rDo, rBo
  rolq		$21, rBo
  movq		rBo, rT1
  andq		rBu, rT1
  xorq		rBi, rT1
  movq		rT1, _bi(\oState)

  notq		rBi
  orq		rBa, rBu
  orq		rBo, rBi
  xorq		rBo, rBu
  xorq		rBe, rBi
  movq		rBu, _bo(\oState)
  movq		rBi, _be(\oState)
  .if		\lastRound == 0
  movq		rBi, rCe
  .endif


  movq		_gu(\iState), rBe
  xorq		rDu, rBe
  movq		_ka(\iState), rBi
  rolq		$20, rBe
  xorq		rDa, rBi
  rolq		$3,  rBi
  movq		_bo(\iState), rBa
  movq		rBe, rT1
  orq		rBi, rT1
  xorq		rDo, rBa
  movq		_me(\iState), rBo
  movq		_si(\iState), rBu
  rolq		$28, rBa
  xorq		rBa, rT1
  movq		rT1, _ga(\oState)
  .if		\lastRound == 0
  xor 		rT1, rCa
  .endif

  xorq		rDe, rBo
  rolq		$45, rBo
  movq		rBi, rT1
  andq		rBo, rT1
  xorq		rBe, rT1
  movq		rT1, _ge(\oState)
  .if		\lastRound == 0
  xorq		rT1, rCe
  .endif

  xorq		rDi, rBu
  rolq		$61, rBu
  movq		rBu, rT1
  orq		rBa, rT1
  xorq		rBo, rT1
  movq		rT1, _go(\oState)

  andq		rBe, rBa
  xorq		rBu, rBa
  movq		rBa, _gu(\oState)
  notq		rBu
  .if		\lastRound == 0
  xorq		rBa, rCu
  .endif

  orq		rBu, rBo
  xorq		rBi, rBo
  movq		rBo, _gi(\oState)


  movq		_be(\iState), rBa
  movq		_gi(\iState), rBe
  movq		_ko(\iState), rBi
  movq		_mu(\iState), rBo
  movq		_sa(\iState), rBu
  xorq		rDi, rBe
  rolq		$6,  rBe
  xorq		rDo, rBi
  rolq		$25, rBi
  movq		rBe, rT1
  orq		rBi, rT1
  xorq		rDe, rBa
  rolq		$1,  rBa
  xorq		rBa, rT1
  movq		rT1, _ka(\oState)
  .if		\lastRound == 0
  xor 		rT1, rCa
  .endif

  xorq		rDu, rBo
  rolq		$8,  rBo
  movq		rBi, rT1
