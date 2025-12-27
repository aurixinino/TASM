; Test the three specific MOV mismatches from the user's report

; Test case 1: mov d4, d2
; Expected: 0x2402 (using MOV D[a], D[b] - opcode 0x0002)
mov d4, d2

; Test case 2: mov d4, #1  
; Expected: 0x1482 (using MOV D[a], const4 - opcode 0x0082)
mov d4, #1

; Test case 3: mov d2, #1
; Expected: 0x1282 (using MOV D[a], const4 - opcode 0x0082)
mov d2, #1
