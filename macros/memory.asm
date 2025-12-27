; Memory Operations Macro Library
; Common memory operations for TriCore assembly

; Memory base addresses
#define RAM_BASE 0x80000000
#define ROM_BASE 0x00000000
#define PERIPHERAL_BASE 0xF0000000

; Memory size constants
#define WORD_SIZE 4
#define HALF_WORD_SIZE 2
#define BYTE_SIZE 1

; Memory access macros
#define LOAD_WORD(dest, base, offset) LD.W dest, [base + offset]
#define STORE_WORD(base, offset, src) ST.W [base + offset], src
#define LOAD_HALFWORD(dest, base, offset) LD.H dest, [base + offset]
#define STORE_HALFWORD(base, offset, src) ST.H [base + offset], src
#define LOAD_BYTE(dest, base, offset) LD.B dest, [base + offset]
#define STORE_BYTE(base, offset, src) ST.B [base + offset], src

; Block memory operations
#define MEMSET_WORD(base, count, value) \
    MOV A[0], base ; \
    MOV D[0], count ; \
    MOV D[1], value ; \
memset_loop: ; \
    ST.W [A[0]+], D[1] ; \
    SUB D[0], D[0], #1 ; \
    JNE memset_loop

#define MEMCPY_WORD(dest, src, count) \
    MOV A[0], dest ; \
    MOV A[1], src ; \
    MOV D[0], count ; \
memcpy_loop: ; \
    LD.W D[1], [A[1]+] ; \
    ST.W [A[0]+], D[1] ; \
    SUB D[0], D[0], #1 ; \
    JNE memcpy_loop

; Stack operations
#define PUSH_REG(reg) ST.W [A[10]-], reg ; SUB A[10], A[10], #WORD_SIZE
#define POP_REG(reg) ADD A[10], A[10], #WORD_SIZE ; LD.W reg, [A[10]]

; Array indexing
#define ARRAY_INDEX_WORD(dest, base, index) \
    SHL dest, index, #2 ; \
    ADD dest, base, dest

#define ARRAY_INDEX_HALFWORD(dest, base, index) \
    SHL dest, index, #1 ; \
    ADD dest, base, dest