; Comprehensive MOV Instruction Test Suite
; Tests all MOV variants and verifies smallest encoding is selected
; Target: TriCore TC1.6
; 
; MOV Instruction Variants:
; 1. MOV D[a], D[b]       - 16-bit (0x0002) if both regs fit, else 32-bit (0x01F0000B)
; 2. MOV D[a], const4     - 16-bit (0x0082) if const fits in 4 bits (-8 to 7)
; 3. MOV D[c], const16    - 32-bit (0x0000003B) for larger constants
; 4. MOV D[15], const8    - 16-bit (0x00DA) special case for D15 with 8-bit const
; 5. MOV E[a], const4     - 16-bit (0x00D2) for E register with 4-bit const
; 6. MOV E[c], const16    - 32-bit (0x000000FB) for E register with 16-bit const
; 7. MOV E[c], D[b]       - 32-bit (0x0800000B) E register from D register
; 8. MOV E[c], D[a], D[b] - 32-bit (0x0810000B) E register from two D registers

.ORG 0x80000000

;=============================================================================
; Section 1: MOV D[a], D[b] - Register to Register
; Should use 16-bit (0x0002) when both registers are D registers
;=============================================================================
test_mov_d_to_d_16bit:
    ; 16-bit variants - both registers < 16
    mov d0, d1          ; Should use 16-bit 0x0002
    mov d2, d3          ; Should use 16-bit 0x0002
    mov d4, d2          ; MISMATCH: was 32-bit, should be 16-bit
    mov d1, d2          ; Should use 16-bit 0x0002
    mov d5, d6          ; Should use 16-bit 0x0002
    mov d7, d8          ; Should use 16-bit 0x0002
    mov d9, d10         ; Should use 16-bit 0x0002
    mov d11, d12        ; Should use 16-bit 0x0002
    mov d13, d14        ; Should use 16-bit 0x0002
    mov d14, d15        ; Should use 16-bit 0x0002
    mov d15, d0         ; Should use 16-bit 0x0002

;=============================================================================
; Section 2: MOV D[a], const4 - Immediate 4-bit constant to D register
; Should use 16-bit (0x0082) when constant fits in 4 bits (0-15 unsigned, -8 to 7 signed)
;=============================================================================
test_mov_d_const4_16bit:
    ; 16-bit variants - constants 0 to 15 (fit in 4 bits unsigned)
    mov d0, #0          ; Should use 16-bit 0x0082
    mov d1, #1          ; Should use 16-bit 0x0082
    mov d2, #1          ; MISMATCH: was 32-bit, should be 16-bit
    mov d4, #1          ; MISMATCH: was 32-bit, should be 16-bit
    mov d3, #2          ; Should use 16-bit 0x0082
    mov d4, #3          ; Should use 16-bit 0x0082
    mov d5, #4          ; Should use 16-bit 0x0082
    mov d6, #5          ; Should use 16-bit 0x0082
    mov d7, #6          ; Should use 16-bit 0x0082
    mov d8, #7          ; Should use 16-bit 0x0082
    mov d9, #8          ; Should use 16-bit 0x0082
    mov d10, #9         ; Should use 16-bit 0x0082
    mov d11, #10        ; Should use 16-bit 0x0082
    mov d12, #11        ; Should use 16-bit 0x0082
    mov d13, #12        ; Should use 16-bit 0x0082
    mov d14, #13        ; Should use 16-bit 0x0082
    mov d15, #14        ; Should use 16-bit 0x0082
    mov d15, #15        ; Should use 16-bit 0x0082

;=============================================================================
; Section 3: MOV D[15], const8 - Special case for D15 with 8-bit constant
; Should use 16-bit (0x00DA) when target is D15 and constant fits in 8 bits
;=============================================================================
test_mov_d15_const8_16bit:
    ; 16-bit variants - D15 with 8-bit constants (-128 to 127)
    mov d15, #0         ; Could use const4 or const8
    mov d15, #126       ; Should use 16-bit 0x00DA (const8)
    mov d15, #127       ; Should use 16-bit 0x00DA
    mov d15, #-128      ; Should use 16-bit 0x00DA
    mov d15, #-1        ; Should use 16-bit 0x00DA
    mov d15, #100       ; Should use 16-bit 0x00DA
    mov d15, #255       ; Should use 16-bit 0x00DA (unsigned)

;=============================================================================
; Section 4: MOV D[c], const16 - 16-bit constant to D register
; Must use 32-bit (0x0000003B) when constant doesn't fit in 4 or 8 bits
;=============================================================================
test_mov_d_const16_32bit:
    ; 32-bit variants - constants that don't fit in 4/8 bits
    mov d0, #256        ; Requires 32-bit 0x0000003B
    mov d1, #1000       ; Requires 32-bit 0x0000003B
    mov d2, #0x1234     ; Requires 32-bit 0x0000003B
    mov d3, #-30000     ; Requires 32-bit 0x0000003B
    mov d4, #32767      ; Requires 32-bit 0x0000003B
    mov d5, #-32768     ; Requires 32-bit 0x0000003B
    mov d6, #0xFFFF     ; Requires 32-bit 0x0000003B
    mov d7, #0xABCD     ; Requires 32-bit 0x0000003B

;=============================================================================
; Section 5: MOV E[a], const4 - 4-bit constant to E register
; Should use 16-bit (0x00D2) when constant fits in 4 bits
;=============================================================================
test_mov_e_const4_16bit:
    ; 16-bit variants - E register with 4-bit constants
    mov e0, #0          ; Should use 16-bit 0x00D2
    mov e2, #1          ; Should use 16-bit 0x00D2
    mov e4, #2          ; Should use 16-bit 0x00D2
    mov e6, #3          ; Should use 16-bit 0x00D2
    mov e8, #4          ; Should use 16-bit 0x00D2
    mov e10, #5         ; Should use 16-bit 0x00D2
    mov e12, #6         ; Should use 16-bit 0x00D2
    mov e14, #7         ; Should use 16-bit 0x00D2
    mov e0, #8          ; Should use 16-bit 0x00D2
    mov e2, #9          ; Should use 16-bit 0x00D2
    mov e4, #10         ; Should use 16-bit 0x00D2
    mov e6, #11         ; Should use 16-bit 0x00D2
    mov e8, #12         ; Should use 16-bit 0x00D2
    mov e10, #13        ; Should use 16-bit 0x00D2
    mov e12, #14        ; Should use 16-bit 0x00D2
    mov e14, #15        ; Should use 16-bit 0x00D2
    mov e0, #0xE        ; Sign-extended: e0 = 0xFFFFFFFFFFFFFFFE

;=============================================================================
; Section 6: MOV E[c], const16 - 16-bit constant to E register
; Must use 32-bit (0x000000FB) for larger constants
;=============================================================================
test_mov_e_const16_32bit:
    ; 32-bit variants - E register with 16-bit constants
    mov e0, #0x1234     ; e0 = 0x0000000000001234 (zero-extended)
    mov e2, #256        ; Requires 32-bit 0x000000FB
    mov e4, #1000       ; Requires 32-bit 0x000000FB
    mov e6, #0xABCD     ; Requires 32-bit 0x000000FB
    mov e8, #32767      ; Requires 32-bit 0x000000FB
    mov e10, #-32768    ; Requires 32-bit 0x000000FB

;=============================================================================
; Section 7: MOV E[c], D[b] - D register to E register (sign-extend)
; Must use 32-bit (0x0800000B)
;=============================================================================
test_mov_e_from_d_32bit:
    ; 32-bit variants - E from D (sign-extended)
    mov e0, d1          ; e0 = sign_ext(d1)
    mov e0, d5          ; e0 = sign_ext(d5)
    mov e2, d3          ; e2 = sign_ext(d3)
    mov e4, d6          ; e4 = sign_ext(d6)
    mov e6, d7          ; e6 = sign_ext(d7)
    mov e8, d9          ; e8 = sign_ext(d9)
    mov e10, d11        ; e10 = sign_ext(d11)
    mov e12, d13        ; e12 = sign_ext(d13)
    mov e14, d15        ; e14 = sign_ext(d15)

;=============================================================================
; Section 8: MOV E[c], D[a], D[b] - Two D registers to E register
; Must use 32-bit (0x0810000B)
;=============================================================================
test_mov_e_from_two_d_32bit:
    ; 32-bit variants - E from two D registers (concatenation)
    mov e0, d1, d0      ; e0[63:32] = d1, e0[31:0] = d0
    mov e0, d6, d3      ; e0 = d6_d3 (d1=d6, d0=d3)
    mov e2, d3, d2      ; e2 = d3_d2
    mov e4, d5, d4      ; e4 = d5_d4
    mov e6, d7, d6      ; e6 = d7_d6
    mov e8, d9, d8      ; e8 = d9_d8
    mov e10, d11, d10   ; e10 = d11_d10
    mov e12, d13, d12   ; e12 = d13_d12
    mov e14, d15, d14   ; e14 = d15_d14

;=============================================================================
; Section 9: Mixed MOV operations from user examples
;=============================================================================
test_mov_mixed:
    ; User-provided examples
    mov d3, #-30000     ; 32-bit const16
    mov e0, 0x1234      ; 32-bit const16 to E
    mov d3, d1          ; 16-bit D to D
    mov e0, d5          ; 32-bit D to E (sign-extend)
    mov e0, d6, d3      ; 32-bit two D to E
    mov d15, #126       ; 16-bit const8 for D15
    mov d1, #6          ; 16-bit const4
    mov e0, #0xE        ; 16-bit const4 (sign-extended)
    mov d1, d2          ; 16-bit D to D

;=============================================================================
; Section 10: Edge cases and boundary testing
;=============================================================================
test_mov_edge_cases:
    ; Boundary values for const4 (0-15 unsigned, -8 to 7 signed)
    mov d0, #-8         ; Min signed 4-bit
    mov d1, #7          ; Max signed 4-bit
    mov d2, #0          ; Min unsigned 4-bit
    mov d3, #15         ; Max unsigned 4-bit

    ; Boundary values for const8 (-128 to 127 signed, 0-255 unsigned)
    mov d15, #-128      ; Min signed 8-bit
    mov d15, #127       ; Max signed 8-bit
    mov d15, #0         ; Min unsigned 8-bit
    mov d15, #255       ; Max unsigned 8-bit

    ; Boundary values for const16 (-32768 to 32767 signed, 0-65535 unsigned)
    mov d0, #-32768     ; Min signed 16-bit
    mov d1, #32767      ; Max signed 16-bit
    mov d2, #0          ; Min unsigned 16-bit
    mov d3, #65535      ; Max unsigned 16-bit (0xFFFF)

    ; All register combinations for D to D
    mov d0, d15         ; First to last
    mov d15, d0         ; Last to first
    mov d7, d7          ; Self-move (identity)
    mov d8, d8          ; Self-move (identity)

;=============================================================================
; Section 11: Negative immediate values
;=============================================================================
test_mov_negative_immediates:
    ; Negative values that fit in different sizes
    mov d0, #-1         ; Should use const4 (16-bit)
    mov d1, #-2         ; Should use const4 (16-bit)
    mov d2, #-8         ; Should use const4 (16-bit) - min 4-bit signed
    mov d3, #-9         ; Should use const16 (32-bit) - doesn't fit in 4-bit
    mov d15, #-50       ; Should use const8 (16-bit) for D15
    mov d15, #-128      ; Should use const8 (16-bit) - min 8-bit signed
    mov d4, #-129       ; Should use const16 (32-bit) - doesn't fit in 8-bit
    mov d5, #-30000     ; Should use const16 (32-bit)

;=============================================================================
; Section 12: Zero and positive edge cases
;=============================================================================
test_mov_zero_positive:
    ; Zero in all formats
    mov d0, #0          ; const4 (16-bit)
    mov d15, #0         ; const8 (16-bit) or const4
    mov e0, #0          ; E const4 (16-bit)
    
    ; Positive boundary values
    mov d0, #15         ; Max const4 unsigned (16-bit)
    mov d1, #16         ; Needs const16 (32-bit) - doesn't fit in 4-bit
    mov d15, #127       ; Max const8 signed (16-bit)
    mov d15, #255       ; Max const8 unsigned (16-bit)
    mov d2, #256        ; Needs const16 (32-bit) - doesn't fit in 8-bit
    mov d3, #32767      ; Max const16 signed (32-bit)
    mov d4, #65535      ; Max const16 unsigned (32-bit)

test_end:
    ret
