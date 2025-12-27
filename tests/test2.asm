; Test file 2  
.org 0xA0001000

start2:
    MOV D[1], 0x5678
    
       ; ABS instructions
    ABS D[5],D[3]           ; Should generate 0x51C0300B 
    ABS D[15],D[7]          ; Should generate 0xF1C0700B
    ABS D[0],D[0]           ; Should generate 0x01C0000B
    
    ; ABS.B instructions  
    ABS.B D[5],D[3]         ; Should generate 0x55C0300B
    ABS.B D[15],D[7]        ; Should generate 0xF5C0700B
    ABS.B D[0],D[0]         ; Should generate 0x05C0000B
    
end2: