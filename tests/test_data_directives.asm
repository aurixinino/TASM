; Test file for NASM-compatible data directives
; Tests DB, DW, DD, EQU, RESB, TIMES

.ORG 0x80000000

; EQU directive - define constants
BUFFER_SIZE EQU 256
MAX_COUNT EQU 100
FLAG_ENABLED EQU 1

; DB directive - define bytes
test_start:
    DB 0x01, 0x02, 0x03, 0x04          ; Define 4 bytes
    DB 'H', 'e', 'l', 'l', 'o'         ; Define string as bytes
    DB 'hello'                         ; string constant 
    DB "World", 0                      ; String with null terminator

; DW directive - define words (16-bit)
test_words:
    DW 0x1234, 0x5678                  ; Two 16-bit values
    DW MAX_COUNT                       ; Use EQU constant

; DD directive - define double-words (32-bit)
test_dwords:
    DD 0x12345678                      ; 32-bit value
    DD BUFFER_SIZE                     ; Use EQU constant
    DD test_start                      ; Use label as address

; RESB - reserve bytes (uninitialized)
buffer:
    RESB 64                            ; Reserve 64 bytes
    RESB BUFFER_SIZE                   ; Reserve using constant

; TIMES - repeat instructions/data
test_times:
    TIMES 4 DB 0xFF                    ; Repeat byte 4 times
    TIMES 8 DB 0                       ; 8 zero bytes
    TIMES 2 DW 0x1234                  ; Repeat word 2 times

; Simple instruction after data
end_marker:
    mov d0, #0x20
    ret
