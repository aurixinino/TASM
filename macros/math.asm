; Mathematical Operations Macro Library
; Common mathematical operations for TriCore assembly

; Mathematical constants
#define PI_FIXED 3141          ; PI * 1000 for fixed-point math
#define E_FIXED 2718           ; E * 1000 for fixed-point math
#define MAX_INT32 0x7FFFFFFF
#define MIN_INT32 0x80000000

; Basic arithmetic macros
#define ADD_IMM(dest, src, imm) MOV dest, src ; ADD dest, #imm
#define SUB_IMM(dest, src, imm) MOV dest, src ; SUB dest, #imm
#define MUL_BY_2(dest, src) SHL dest, src, #1
#define MUL_BY_4(dest, src) SHL dest, src, #2
#define DIV_BY_2(dest, src) SHR dest, src, #1
#define DIV_BY_4(dest, src) SHR dest, src, #2

; Absolute value macro
#define ABS_VALUE(dest, src) \
    MOV dest, src ; \
    CMP src, #0 ; \
    JGE abs_done ; \
    NEG dest, dest ; \
abs_done:

; Min/Max macros
#define MAX_VALUE(dest, a, b) \
    CMP a, b ; \
    JGE max_first ; \
    MOV dest, b ; \
    JMP max_done ; \
max_first: ; \
    MOV dest, a ; \
max_done:

#define MIN_VALUE(dest, a, b) \
    CMP a, b ; \
    JLE min_first ; \
    MOV dest, b ; \
    JMP min_done ; \
min_first: ; \
    MOV dest, a ; \
min_done:

; Swap macro
#define SWAP_REGS(a, b) \
    XOR a, b ; \
    XOR b, a ; \
    XOR a, b