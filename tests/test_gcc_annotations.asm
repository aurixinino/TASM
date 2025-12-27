;/*********************************************************************************************************************/
;/* Test file for GCC-style annotations (like #function_name)                                                       */
;/*********************************************************************************************************************/

.ORG 0x80000000                     ; Set FLASH address

.global test_gcc_annotations

#APP
	# 670 "C:\Users\Atti\AURIX-v1.10.24-workspace\Fixed_Num\Libraries\iLLD\TC27D\Tricore\Cpu\Std/IfxCpu.h" 1 	enable
	# 0 "" 2
#NO_APP

.sect ".text"
.align 4

test_gcc_annotations:	.type	func
	add	d2, #5		; regular semicolon comment
	add	d3, #0xF	#hex_immediate_annotation
	jlt	d2, #7, .L1	#branch_annotation
.L1:
	ret	#test_gcc_annotations
	
test_another:	.type	func
	add	d0, d1	#some_comment
	sub	d0, #-5		#negative_immediate
	ret	#test_another
