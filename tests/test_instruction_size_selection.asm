; Test file for intelligent instruction size selection
; Tests that the encoder selects the smallest instruction that can fit the operand

.ORG 0x80000000

; ===== J (Jump) Instruction Size Selection =====
; J has two variants in tricore_tc1.6_instruction_set.xlsx:
; 1. J disp8/2  (16-bit, opcode=0x003C, op1_len=8)  -> range: 0 to 510 (0-255 after /2)
; 2. J disp24/2 (32-bit, opcode=0x0000001D, op1_len=24) -> larger range

; Small jumps - should use 16-bit instruction (disp8/2)
test_j_small:
    J 0x10          ; +16 (fits after /2) -> should use 16-bit
    J 0x7E          ; +126 (fits after /2) -> should use 16-bit
    J 0xFE          ; +254 (127 after /2, fits in 8 bits) -> should use 16-bit
    J 0             ; 0 (fits after /2) -> should use 16-bit
    J 2             ; 2 (1 after /2) -> should use 16-bit
    J 50            ; 50 (25 after /2) -> should use 16-bit

; Large jumps - should use 32-bit instruction (disp24/2)
test_j_large:
    J 0x200         ; +512 (256 after /2, doesn't fit in 8 bits) -> should use 32-bit
    J 0x400         ; +1024 (512 after /2) -> should use 32-bit
    J 0x1000        ; +4096 (2048 after /2) -> should use 32-bit
    J 0xFFFF        ; +65535 (large value) -> should use 32-bit
    J 1000          ; Decimal 1000 (500 after /2) -> should use 32-bit

; Edge cases
test_j_edge:
    J 254           ; Decimal 254 (127 after /2, max for 8-bit) -> should use 16-bit
    J 256           ; Decimal 256 (128 after /2, doesn't fit) -> should use 32-bit
    J 510           ; Decimal 510 (255 after /2, max for disp8) -> should use 16-bit
    J 512           ; Decimal 512 (256 after /2, min for 32-bit) -> should use 32-bit

; Various numeric formats (all should work)
test_j_formats:
    J 0x10          ; Hex (16, 8 after /2) -> 16-bit
    J 0b0001_0000   ; Binary (16, 8 after /2) -> 16-bit
    J 20            ; Decimal (10 after /2) -> 16-bit
    J 0o20          ; Octal (16, 8 after /2) -> 16-bit
    J 0x400         ; Hex (1024, 512 after /2) -> 32-bit

; ===== Additional test instructions =====
; (Add more instructions here as needed that have multiple size variants)

; Test with labels (should default to larger variant for safety)
test_j_labels:
    J forward_label
    J backward_label

backward_label:
    ; Placeholder (labels only)

forward_label:
    ; Placeholder (labels only)

; ===== Expected Results =====
; The listing file should show:
; - Small jumps (0-510, i.e., 0-255 after /2): 16-bit instructions (2 bytes per instruction)
; - Large jumps (>510, i.e., >255 after /2): 32-bit instructions (4 bytes per instruction)
