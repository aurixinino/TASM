; C-Code Operations Macro Library
; Common language operations for TriCore assembly
; Provides C-like syntax for common programming patterns

; ========================================================
; LOOP CONSTRUCTS
; ========================================================

; FOR(counter, count)
; Standard for loop with countdown: for(i=count; i>0; i--)
; Example: FOR(d4, #5) ... ENDFOR(d4)
; Uses __COUNTER__ for unique labels per invocation
#define FOR(counter, count) mov counter, count | for_loop_##__COUNTER__:

; ENDFOR(counter)
; End of FOR loop - must match the counter register
#define ENDFOR(counter) loop counter, for_loop_##__COUNTER__

; FOR_INLINE(counter, count, init_code, loop_code)
; Compact FOR loop with initialization and body in one macro call
; Example: FOR_INLINE(d4, #5, mov d0, #0, add d0, d0, d4)
; Note: Code blocks cannot contain commas outside of instruction operands
#define FOR_INLINE(counter, count, init_code, loop_code) init_code | mov counter, count | for_inline_##__COUNTER__: | loop_code | loop counter, for_inline_##__COUNTER__

; WHILE(condition_reg, value)
; While loop: while(reg == value) { body }
; Example: WHILE(d2, #0) ... ENDWHILE(d2, #0)
#define WHILE(reg, val) while_start_##__COUNTER__: | jne reg, val, while_end_##__COUNTER__

; ENDWHILE(condition_reg, value)
; End of WHILE loop
#define ENDWHILE(reg, val) j while_start_##__COUNTER__ | while_end_##__COUNTER__:

; WHILE_INLINE(condition_reg, condition_value, loop_code)
; Compact WHILE loop with body in one macro call
; Example: WHILE_INLINE(d2, #0, add d0, d0, #1)
; Note: Loop code cannot contain commas; condition is never satisfied initially
#define WHILE_INLINE(reg, val, loop_code) while_inline_##__COUNTER__: | jne reg, val, while_inline_end_##__COUNTER__ | loop_code | j while_inline_##__COUNTER__ | while_inline_end_##__COUNTER__:

; DO_WHILE()
; Do-while loop: do { body } while(condition)
; Example: DO_WHILE() ... LOOP_WHILE(d2, #0)
#define DO_WHILE() do_start_##__COUNTER__:

; LOOP_WHILE(condition_reg, value)
; End of do-while loop with condition
#define LOOP_WHILE(reg, val) jeq reg, val, do_start_##__COUNTER__

; DO_WHILE_INLINE(loop_code, condition_reg, condition_value)
; Compact DO-WHILE loop with body in one macro call
; Example: DO_WHILE_INLINE(add d0, d0, #1, d2, #0)
; Note: Loop code cannot contain commas
#define DO_WHILE_INLINE(loop_code, reg, val) do_inline_##__COUNTER__: | loop_code | jeq reg, val, do_inline_##__COUNTER__

; ========================================================
; CONDITIONAL CONSTRUCTS
; ========================================================

; IF(condition_reg, value, true_code)
; Simple if statement: if(reg == value) { code }
; Example: IF(d2, 0, mov d3, #1)
#define IF(reg, val, code) \
    jne reg, val, if_end_##reg##val \
    code \
if_end_##reg##val:

; IF_ELSE(condition_reg, value, true_code, false_code)
; If-else statement: if(reg == value) { code1 } else { code2 }
#define IF_ELSE(reg, val, true_code, false_code) \
    jne reg, val, else_branch_##reg##val \
    true_code \
    j endif_##reg##val \
else_branch_##reg##val: \
    false_code \
endif_##reg##val:

; IF_GT(reg, value, true_code)
; If greater than: if(reg > value) { code }
#define IF_GT(reg, val, code) \
    jle reg, val, if_gt_end_##reg##val \
    code \
if_gt_end_##reg##val:

; IF_LT(reg, value, true_code)
; If less than: if(reg < value) { code }
#define IF_LT(reg, val, code) \
    jge reg, val, if_lt_end_##reg##val \
    code \
if_lt_end_##reg##val:

; IF_GE(reg, value, true_code)
; If greater or equal: if(reg >= value) { code }
#define IF_GE(reg, val, code) \
    jlt reg, val, if_ge_end_##reg##val \
    code \
if_ge_end_##reg##val:

; IF_LE(reg, value, true_code)
; If less or equal: if(reg <= value) { code }
#define IF_LE(reg, val, code) \
    jgt reg, val, if_le_end_##reg##val \
    code \
if_le_end_##reg##val:

; IF_NEQ(reg, value, true_code)
; If not equal: if(reg != value) { code }
#define IF_NEQ(reg, val, code) \
    jeq reg, val, if_neq_end_##reg##val \
    code \
if_neq_end_##reg##val:

; ========================================================
; TERNARY OPERATOR
; ========================================================

; TERNARY(condition_reg, value, dest_reg, true_val, false_val)
; Ternary operator: dest = (reg == value) ? true_val : false_val
#define TERNARY(reg, val, dest, true_val, false_val) \
    jne reg, val, ternary_false_##dest \
    mov dest, true_val \
    j ternary_end_##dest \
ternary_false_##dest: \
    mov dest, false_val \
ternary_end_##dest:

; ========================================================
; SWITCH/CASE CONSTRUCTS
; ========================================================

; SWITCH_START(switch_reg)
; Begin switch statement
#define SWITCH(reg) ; Switch on register reg

; CASE(switch_reg, value)
; Case branch - jumps to next case if not matched
; Place case body immediately after
#define CASE(reg, val) jne reg, val, case_next_##__COUNTER__ | j switch_end_##__COUNTER__ | case_next_##__COUNTER__:

; DEFAULT()
; Default case - executes if no other case matches
#define DEFAULT() ; Default case body follows

; ENDSWITCH()
; End of switch statement
#define ENDSWITCH() switch_end_##__COUNTER__:

; ========================================================
; UTILITY MACROS
; ========================================================

; MAX(dest, reg1, reg2)
; Set dest to maximum of reg1 and reg2: dest = max(reg1, reg2)
#define MAX(dest, reg1, reg2) max dest, reg1, reg2

; MIN(dest, reg1, reg2)
; Set dest to minimum of reg1 and reg2: dest = min(reg1, reg2)
#define MIN(dest, reg1, reg2) min dest, reg1, reg2

; ABS_VAL(dest, src)
; Absolute value: dest = abs(src)
#define ABS_VAL(dest, src) abs dest, src

; INC(reg)
; Increment register: reg++
#define INC(reg) add reg, reg, #1

; DEC(reg)
; Decrement register: reg--
#define DEC(reg) add reg, reg, #-1

; -------------------------------------------------------
;                       EOF
; -------------------------------------------------------
