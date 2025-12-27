;/*********************************************************************************************************************/
;/* Test file for GCC-style labels (starting with dot)                                                               */
;/*********************************************************************************************************************/

.ORG 0x80000000                     ; Set FLASH address

.global test_function

.sect ".text"
.align 4

test_function:	.type	func
	mov	d2, #0
	j	.L2
.L1:
	add	d2, #1
.L2:
	jlt	d2, #10, .L1
	ret


fix16_moving_average_init:
	mov.aa	%a2, %a4			; tmp_a:=a2 = *buffer:=a4
	jnz	%d4, 1f					; if (size:=d4) != 0 then continue (use forward ref instead)
.L12:
	ret							; early exit if size <= 0
1:
	mov.a	%a3, %d4			; tmp_cnt:=a3 = size:=d4
	add.a	%a3, %a3, %a3		; tmp_cnt:=a3 = a3 + a3 = size + size = size *2 [in bytes]
	mov	%d2, 0					; tmp:=d2 = 0
	j	2f						; jump to label 2 forward
	0:
	st.b	[%a2+]1, %d2		; *tmp_a = 0:=d2 -- ST.B A[b], off10, D[a] (BO) (Post-increment Addressing Mode) - byte-word
	2:
	loop	%a3, 0b				; if (tmp_cnt:=a3)!=0 then (tmp_cnt:=a3) -= 1 
	ret	