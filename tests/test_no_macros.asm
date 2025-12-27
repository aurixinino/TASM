; Test file for --no-macros option
; This file contains NO macro definitions, just raw assembly
; Use this to verify --no-macros skips the macro expansion phase

    .section .text
    .org 0x80000000

start:
    ; Simple instructions without any macros
    mov d0, #0x42
    mov d1, #0x10
    add d2, d0, d1
    ret

    .end
