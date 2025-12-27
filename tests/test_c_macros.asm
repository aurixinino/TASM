; ========================================================
; Test Suite for C-Code Macro Library
; Tests all C-like syntax macros from C_instructions.asm
; ========================================================

    .section .text
    .org 0x80000000

    .global main

main:
    ; Initialize test registers
    mov     d0, #0
    mov     d1, #1
    mov     d2, #5
    mov     d3, #10

; ========================================================
; Test 1: Utility - MAX
; ========================================================
test_max:
    mov     d1, #15
    mov     d2, #10
    MAX(d0, d1, d2)
    ; Expected: d0 = 15

; ========================================================
; Test 2: Utility - MIN
; ========================================================
test_min:
    mov     d1, #15
    mov     d2, #10
    MIN(d0, d1, d2)
    ; Expected: d0 = 10

; ========================================================
; Test 3: Utility - ABS
; ========================================================
test_abs:
    mov     d1, #-5
    ABS_VAL(d0, d1)
    ; Expected: d0 = 5

; ========================================================
; Test 4: Utility - INC
; ========================================================
test_inc:
    mov     d0, #5
    INC(d0)
    INC(d0)
    ; Expected: d0 = 7

; ========================================================
; Test 5: Utility - DEC
; ========================================================
test_dec:
    mov     d0, #10
    DEC(d0)
    DEC(d0)
    ; Expected: d0 = 8

; ========================================================
; Test 6: Multiple Operations
; ========================================================
test_combined:
    mov     d1, #100
    mov     d2, #50
    MAX(d3, d1, d2)     ; d3 = 100
    MIN(d4, d1, d2)     ; d4 = 50
    INC(d3)             ; d3 = 101
    DEC(d4)             ; d4 = 49

; ========================================================
; Test 7: FOR Loop - Sum 1 to 10
; ========================================================
test_for_sum:
    mov     d0, #0              ; sum accumulator
    mov     d5, #10             ; loop counter value
    FOR(d4, d5)
    add     d0, d0, d4          ; add counter to sum
    ENDFOR(d4)
    ; Result: d0 = 55 (sum of 1..10)

; ========================================================
; Test 8: WHILE Loop - Count down
; ========================================================
test_while_countdown:
    mov     d2, #5              ; counter
    mov     d0, #0              ; iterations
    WHILE(d2, #0)
    add     d0, d0, #1
    ENDWHILE(d2, #0)
    ; Result: d0 = 0 (condition false from start)

; ========================================================
; Test 9: DO_WHILE Loop - Execute Once
; ========================================================
test_do_while_once:
    mov     d2, #5              ; initial non-zero
    mov     d0, #0              ; counter
    DO_WHILE()
    add     d0, d0, #1          ; executes once
    mov     d2, #0              ; exit condition
    LOOP_WHILE(d2, #0)
    ; Result: d0 = 1

; ========================================================
; Test 10: SWITCH with Multiple Cases
; ========================================================
test_switch_multi:
    mov     d2, #1              ; switch on value 1
    mov     d3, #0              ; result
    SWITCH(d2)
    CASE(d2, #0)
    mov     d3, #100
    CASE(d2, #1)
    mov     d3, #200
    CASE(d2, #2)
    mov     d3, #300
    DEFAULT()
    mov     d3, #999
    ENDSWITCH()
    ; Result: d3 = 200 (case 1)

; ========================================================
; Test 11: SWITCH Default Case
; ========================================================
test_switch_default:
    mov     d2, #99             ; value not in cases
    mov     d3, #0              ; result
    SWITCH(d2)
    CASE(d2, #0)
    mov     d3, #10
    CASE(d2, #1)
    mov     d3, #20
    DEFAULT()
    mov     d3, #777            ; should execute this
    ENDSWITCH()
    ; Result: d3 = 777 (default case)

; ========================================================
; Test 12: Nested FOR Loop (manual)
; ========================================================
test_nested_for:
    mov     d0, #0              ; total counter
    
    ; Outer loop: 3 times
    mov     d6, #3              ; outer counter value
    FOR(d4, d6)
    
    ; Inner loop: 2 times
    mov     d7, #2              ; inner counter value
    FOR(d5, d7)
    add     d0, d0, #1          ; increment total
    ENDFOR(d5)
    
    ENDFOR(d4)
    ; Result: d0 = 6 (3 * 2)


; ========================================================
; Test 13: FOR_INLINE - Compact FOR loop
; ========================================================
test_for_inline:
    ; Initialize sum to 0, count 1 to 5, add counter to sum
    FOR_INLINE(d4, #5, 'mov d0, #0', 'add d0, d0, d4')
    ; Result: d0 = 15 (5+4+3+2+1)

; ========================================================
; Test 14: WHILE_INLINE - Compact WHILE loop
; ========================================================
test_while_inline:
    mov     d2, #3              ; set to non-zero (condition false)
    mov     d0, #0              ; counter
    ; Loop body: increment d0 with quoted string
    WHILE_INLINE(d2, #0, 'add d0, d0, #1')
    ; Result: d0 = 0 (loop never executes)

; ========================================================
; Test 15: DO_WHILE_INLINE - Compact DO-WHILE loop
; ========================================================
test_do_while_inline:
    mov     d2, #1              ; set to non-zero initially
    mov     d0, #0              ; counter
    ; Loop once, incrementing d0 with quoted string
    DO_WHILE_INLINE('add d0, d0, #1', d2, #1)
    mov     d2, #0              ; condition now false
    ; Result: d0 = 1 (executed once but would loop if d2 stays 1)

; ========================================================
; Test 16: Utility Macro Combinations
; ========================================================
test_utility_combos:
    mov     d1, #-10
    mov     d2, #15
    ABS_VAL(d1, d1)             ; d1 = 10
    MAX(d3, d1, d2)             ; d3 = 15
    MIN(d4, d1, d2)             ; d4 = 10
    INC(d3)                     ; d3 = 16
    DEC(d4)                     ; d4 = 9
    ; Results: d1=10, d2=15, d3=16, d4=9

; ========================================================
; End of Tests
; ========================================================
test_end:
    ; Set success indicator
    mov     d15, #0xCAFE
    ret

    .end
