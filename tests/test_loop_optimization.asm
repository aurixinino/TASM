; Test LOOP instruction variant selection
; Should automatically select 16-bit vs 32-bit based on displacement

.ORG 0x80000000

; Test 1: Short loop (fits in disp4/2) - should use 16-bit LOOP
test_short_loop:
    mov d4, #3
    loop d4, short_target    ; disp4/2 fits: 4 bytes / 2 = 2
    add d0, d0, #1
short_target:
    ret

; Test 2: Medium loop (needs disp15/2) - should use 32-bit LOOP  
test_long_loop:
    mov d4, #10
    loop d4, long_target     ; Need disp15/2 for longer distance
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
long_target:
    ret

; Test 3: Very short J (fits in disp8/2) - should use 16-bit J
test_short_j:
    j near_target           ; disp8/2 fits
    nop
near_target:
    ret
