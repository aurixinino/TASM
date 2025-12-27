; Test forward jump references with labels
; This tests multi-pass linking and correct displacement encoding

.ORG 0x80000000

; Test 1: Short forward JNZ (disp4)
test_jnz_short:
    JNZ D[4], target1    ; Should encode with disp=4
    mov d0, #0x10
    mov d1, #0x20
target1:
    mov d2, #0x30

; Test 2: Short forward J (disp8)
test_j_short:
    j target2            ; Should encode with disp=5
    mov d0, #0x40
target2:
    mov d1, #0x50

; Test 3: Longer forward jump
test_j_longer:
    j target3
    mov d0, #0x11
    mov d1, #0x22
    mov d2, #0x33
    mov d3, #0x44
target3:
    mov d4, #0x55

; Test 4: Multiple jumps to same target
test_multiple_to_same:
    JNZ D[2], common_target
    mov d0, #0x01
    j common_target
    mov d1, #0x02
common_target:
    ret

; Test 5: Nested labels
test_nested:
    j outer_target
    mov d0, #0xAA
inner_target:
    mov d1, #0xBB
outer_target:
    j end_test
    mov d2, #0xCC

end_test:
    ret
