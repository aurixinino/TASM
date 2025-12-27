; Test file for NASM-compatible numeric constants
; Tests all numeric formats from NASM 3.4.1 specification
; https://www.nasm.us/docs/3.01/nasm03.html#section-3.4.1

.ORG 0x80000000

; ===== Decimal Formats =====
decimal_tests:
    DB 200              ; Plain decimal
    DB 0200             ; Leading zeros (still decimal in NASM, not octal)
    DB 0200d            ; Explicit decimal suffix
    DB 0d200            ; Explicit decimal prefix

; ===== Hexadecimal Formats =====
hex_tests:
    DB 0xc8             ; Standard 0x prefix
    DB 0Xc8             ; Uppercase X
    DB 0c8h             ; Suffix h (must start with 0 if A-F)
    DB 0hc8             ; Prefix 0h
    DB $0c8             ; Deprecated $ format (must have leading 0)
    DB 0abh             ; Hex A-F must start with 0
    DB 0FFh             ; Uppercase hex
    DB 0xff             ; Lowercase hex

; ===== Octal Formats =====
octal_tests:
    DB 310q             ; Suffix q (= 200 decimal)
    DB 310o             ; Suffix o (= 200 decimal)
    DB 0o310            ; Prefix 0o (= 200 decimal)
    DB 0q310            ; Prefix 0q (= 200 decimal)
    DW 0O777            ; Uppercase O prefix (= 511 decimal, needs word)
    DW 0Q777            ; Uppercase Q prefix (= 511 decimal, needs word)

; ===== Binary Formats =====
binary_tests:
    DB 11001000b        ; Suffix b
    DB 1100_1000b       ; Underscores for readability
    DB 1100_1000y       ; Suffix y
    DB 0b1100_1000      ; Prefix 0b
    DB 0y1100_1000      ; Prefix 0y
    DB 0B11110000       ; Uppercase B
    DB 0Y11110000       ; Uppercase Y

; ===== Underscores for Readability =====
underscore_tests:
    DD 1_000_000        ; One million
    DD 0xFF_FF_FF_FF    ; Max 32-bit with underscores
    DB 0b1111_0000      ; Binary with underscores
    DW 0x12_34          ; Hex with underscores (16-bit)
    DD 0x1234_5678      ; Hex with underscores (32-bit)

; ===== Mixed Tests =====
mixed_tests:
    DB 0xAB, 0o253, 0b10101011, 171, 0d171    ; All same value (171)
    DW 0xc8, 200, 310o, 0b11001000            ; All same value (200)

; ===== Negative Numbers =====
negative_tests:
    DB -42              ; Negative decimal
    DW -1000            ; Negative word
    DD -1_000_000       ; Negative with underscores

; ===== Large Numbers with Underscores =====
large_numbers:
    DD 4_294_967_295    ; Max 32-bit unsigned
    DD 0xFFFF_FFFF      ; Same as above in hex
    DD 0b1111_1111_1111_1111_1111_1111_1111_1111  ; Same in binary

; ===== Zero in Different Formats =====
zero_tests:
    DB 0                ; Decimal zero
    DB 0x0              ; Hex zero
    DB 0b0              ; Binary zero
    DB 0o0              ; Octal zero
    DB 0d0              ; Explicit decimal zero

; ===== Constants with EQU =====
MAX_VALUE   EQU 0xFF
BUFFER_SIZE EQU 1024
FLAG_ENABLE EQU 0b0000_0001
PORT_ADDR   EQU 0x8000_0000

constant_usage:
    DB MAX_VALUE
    DW BUFFER_SIZE
    DB FLAG_ENABLE
    DD PORT_ADDR
