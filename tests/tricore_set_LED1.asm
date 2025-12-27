
;/*********************************************************************************************************************/
;/*---------------------------------------------Function Implementations----------------------------------------------*/
;/*********************************************************************************************************************/



;/*********************************************************************************************************************/
;/*---------------------------------------------      START-UP CODE     ----------------------------------------------*/
;/*********************************************************************************************************************/
.ORG 0x80000000                     ; Set FLASH address

DB 0x00
DB 0x00
DB 0x00
DB 0x00
DB 0x70
DB 0x00
DB 0x59
DB 0xB3
DB 0x00
DB 0x00
DB 0x00
DB 0x00
DB 0x00
DB 0x00
DB 0x00
DB 0x00
DB 0x00
DB 0x00
DB 0x00
DB 0x00
DB 0x00
DB 0x00
DB 0x00
DB 0x00
DB 0x64
DB 0xB8
DB 0x1E
DB 0x79
DB 0x9B
DB 0x47
DB 0xE1
DB 0x86

/*********************************************************************************************************************/
;/*------------------------------------------------Function Prototypes------------------------------------------------*/
;/*********************************************************************************************************************/
.global set_LED1_State_Assembly     ; Declare global section symbol (define the prototype of the function)

.ORG 0x8000002c                     ; Set origin address

.sdecl ".text", CODE                ; Declare a section with name, type and attributes
.sect ".text"                       ; Activate a declared section
.align 4                            ; Align the location counter on 4 bytes
    
set_LED1_State_Assembly:
.type func
    
    ;jne d4, #0, switch_on           ; Check the passed value, stored in D4
    JNZ    D[4], switch_on

    mov d0, #0x20                   ; If 0 "LED_OFF", switch off LED1: by writing 0x20 
    j common
    
switch_on:                          ; Else 1 "LED_ON", switch on LED1 by writing 0x200000 
    mov d1, #0x20  
    sh d0, d1, #16                  ; Shift of 16 bits
    
common:
    movh.a a0, #0xF003              ; Load the address of "P00_OMR" register into A0 "0xF003A004" 
    ;lea a0, [a0]+0x7000
    ;lea a0, [a0]+0x3004
    lea a0, a0, 0xA004
    
    st.w [a0], d0                   ; Store the D0 value to the target register
    
    ret                             ; Return from the call needed to restore the context
