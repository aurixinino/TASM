; Test TIMES and RESB directives
.ORG 0x80000000

; Test TIMES with various patterns
times_test:
    TIMES 4 DB 0xFF                    ; Four 0xFF bytes
    TIMES 3 DB 0xAA                    ; Three 0xAA bytes
    TIMES 2 DW 0x1234                  ; Two words (4 bytes total)

; Test RESB
reserve_test:
    RESB 8                             ; 8 bytes of zeros
    DB 0x99                            ; Marker byte

; Test alignment patterns
align_test:
    TIMES 16 DB 0                      ; 16 zero bytes

end_marker:
    mov d0, #0x20
    ret
