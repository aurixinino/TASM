; ========================================================
; Simple C-Macro Test - Basic Functionality
; Tests core C-like macros with verifiable output
; ========================================================

    .section .text
    .org 0x80000000

    .global test_start

test_start:
    ; Initialize base registers
    mov     d0, #0
    mov     d1, #0
    mov     d2, #0
    mov     d3, #0

; ========================================================
; Test 1: Utility - MAX
; ========================================================
test_max:
    mov     d1, #25
    mov     d2, #10
    MAX(d0, d1, d2)
    ; Result: d0 should be 25

; ========================================================
; Test 2: Utility - MIN
; ========================================================
test_min:
    mov     d1, #25
    mov     d2, #10
    MIN(d0, d1, d2)
    ; Result: d0 should be 10

; ========================================================
; Test 3: Utility - INC
; ========================================================
test_inc:
    mov     d0, #10
    INC(d0)          ; d0 = 11
    ; Result: d0 should be 11

; ========================================================
; Test 4: Utility - DEC
; ========================================================
test_dec:
    mov     d0, #10
    DEC(d0)          ; d0 = 9
    ; Result: d0 should be 9

; ========================================================
; Test 5: ABS_VAL
; ========================================================
test_abs:
    mov     d1, #-5
    ABS_VAL(d0, d1)
    ; Result: d0 should be 5

; ========================================================
; Test 6: FOR Loop
; ========================================================
test_for_loop:
    mov     d0, #0              ; counter
    FOR(d4, #5)
    add     d0, d0, #1          ; increment counter
    ENDFOR(d4)
    ; Result: d0 should be 5

; ========================================================
; Test 7: WHILE Loop
; ========================================================
test_while_loop:
    mov     d2, #3              ; condition counter
    mov     d0, #0              ; result counter
    WHILE(d2, #0)
    add     d0, d0, #1          ; won't execute (d2=3, not 0)
    ENDWHILE(d2, #0)
    ; Result: d0 should be 0 (loop didn't run)

; ========================================================
; Test 8: DO_WHILE Loop
; ========================================================
test_do_while:
    mov     d2, #1              ; condition (non-zero)
    mov     d0, #0              ; counter
    DO_WHILE()
    add     d0, d0, #1          ; runs once
    mov     d2, #0              ; set condition to exit
    LOOP_WHILE(d2, #0)
    ; Result: d0 should be 1

; ========================================================
; Test 9: SWITCH/CASE Statement
; ========================================================
test_switch:
    mov     d2, #2              ; switch value
    mov     d3, #0              ; result
    SWITCH(d2)
    CASE(d2, #0)
    mov     d3, #10             ; case 0
    CASE(d2, #1)
    mov     d3, #20             ; case 1
    CASE(d2, #2)
    mov     d3, #30             ; case 2
    DEFAULT()
    mov     d3, #99             ; default
    ENDSWITCH()
    ; Result: d3 should be 30

; ========================================================
; Test 10: FOR_INLINE - Compact Loop
; ========================================================
test_for_inline:
    ; Using quoted strings to allow commas in code blocks
    FOR_INLINE(d4, #3, 'mov d0, #0', 'add d0, d0, d4')
    ; Result: d0 should be 6 (3+2+1)

; ========================================================
; Test 11: DO_WHILE_INLINE - Compact Do-While
; ========================================================
test_do_while_inline:
    mov     d2, #0              ; set condition to false
    mov     d0, #100            ; initial value
    ; Using quoted strings for code with commas
    DO_WHILE_INLINE('add d0, d0, #1', d2, #0)
    ; Result: d0 should be 101 (executed once)

; ========================================================
; End of Tests - Success Marker
; ========================================================
test_complete:
    mov     d15, #0x1234    ; Success marker
    ret

    .end
