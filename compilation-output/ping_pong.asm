L_1:
	# 1 begin_block pingpong _ _ #
	add	$sp, $sp, 56
	move	$s0, $sp
L_2:
	# 2 := 0 _ CONTINUE #
	li	$t1, 0
	sw	$t1, -20($s0)
L_3:
	# 3 := 0 _ counter #
	li	$t1, 0
	sw	$t1, -24($s0)
L_4:
	# 4 := 0 _ ping #
	li	$t1, 0
	sw	$t1, -12($s0)
L_5:
	# 5 := 111111110 _ pong #
	li	$t1, 111111110
	sw	$t1, -16($s0)
L_6:
	# 6 <> CONTINUE 0 47 #
	lw	$t1, -20($s0)
	li	$t2, 0
	bne	$t1, $t2, L_47
L_7:
	# 7 jump _ _ 8 #
	j	L_8
L_8:
	# 8 >= ping 0 10 #
	lw	$t1, -12($s0)
	li	$t2, 0
	bge	$t1, $t2, L_10
L_9:
	# 9 jump _ _ 47 #
	j	L_47
L_10:
	# 10 >= pong 0 12 #
	lw	$t1, -16($s0)
	li	$t2, 0
	bge	$t1, $t2, L_12
L_11:
	# 11 jump _ _ 47 #
	j	L_47
L_12:
	# 12 < ping pong 14 #
	lw	$t1, -12($s0)
	lw	$t2, -16($s0)
	blt	$t1, $t2, L_14
L_13:
	# 13 jump _ _ 23 #
	j	L_23
L_14:
	# 14 out ping _ _ #
	li	$v0, 1
	lw	$a0, -12($s0)
	syscall
L_15:
	# 15 = ping 0 17 #
	lw	$t1, -12($s0)
	li	$t2, 0
	beq	$t1, $t2, L_17
L_16:
	# 16 jump _ _ 19 #
	j	L_19
L_17:
	# 17 := 10 _ ping #
	li	$t1, 10
	sw	$t1, -12($s0)
L_18:
	# 18 jump _ _ 22 #
	j	L_22
L_19:
	# 19 * ping 10 T_1 #
	lw	$t1, -12($s0)
	li	$t2, 10
	mul	$t1, $t1, $t2
	sw	$t1, -32($s0)
L_20:
	# 20 + T_1 10 T_2 #
	lw	$t1, -32($s0)
	li	$t2, 10
	add	$t1, $t1, $t2
	sw	$t1, -36($s0)
L_21:
	# 21 := T_2 _ ping #
	lw	$t1, -36($s0)
	sw	$t1, -12($s0)
L_22:
	# 22 jump _ _ 34 #
	j	L_34
L_23:
	# 23 = pong 0 25 #
	lw	$t1, -16($s0)
	li	$t2, 0
	beq	$t1, $t2, L_25
L_24:
	# 24 jump _ _ 30 #
	j	L_30
L_25:
	# 25 := pong _ ping #
	lw	$t1, -16($s0)
	sw	$t1, -12($s0)
L_26:
	# 26 := 111111110 _ pong #
	li	$t1, 111111110
	sw	$t1, -16($s0)
L_27:
	# 27 + counter 1 T_3 #
	lw	$t1, -24($s0)
	li	$t2, 1
	add	$t1, $t1, $t2
	sw	$t1, -40($s0)
L_28:
	# 28 := T_3 _ counter #
	lw	$t1, -40($s0)
	sw	$t1, -24($s0)
L_29:
	# 29 jump _ _ 34 #
	j	L_34
L_30:
	# 30 out pong _ _ #
	li	$v0, 1
	lw	$a0, -16($s0)
	syscall
L_31:
	# 31 / pong 10 T_4 #
	lw	$t1, -16($s0)
	li	$t2, 10
	div	$t1, $t1, $t2
	sw	$t1, -44($s0)
L_32:
	# 32 - T_4 1 T_5 #
	lw	$t1, -44($s0)
	li	$t2, 1
	sub	$t1, $t1, $t2
	sw	$t1, -48($s0)
L_33:
	# 33 := T_5 _ pong #
	lw	$t1, -48($s0)
	sw	$t1, -16($s0)
L_34:
	# 34 := 9999999 _ delay #
	li	$t1, 9999999
	sw	$t1, -28($s0)
L_35:
	# 35 > delay 0 37 #
	lw	$t1, -28($s0)
	li	$t2, 0
	bgt	$t1, $t2, L_37
L_36:
	# 36 jump _ _ 40 #
	j	L_40
L_37:
	# 37 - delay 1 T_6 #
	lw	$t1, -28($s0)
	li	$t2, 1
	sub	$t1, $t1, $t2
	sw	$t1, -52($s0)
L_38:
	# 38 := T_6 _ delay #
	lw	$t1, -52($s0)
	sw	$t1, -28($s0)
L_39:
	# 39 jump _ _ 35 #
	j	L_35
L_40:
	# 40 = counter 50 42 #
	lw	$t1, -24($s0)
	li	$t2, 50
	beq	$t1, $t2, L_42
L_41:
	# 41 jump _ _ 46 #
	j	L_46
L_42:
	# 42 out CONTINUE _ _ #
	li	$v0, 1
	lw	$a0, -20($s0)
	syscall
L_43:
	# 43 inp CONTINUE _ _ #
	li	$v0, 5
	syscall
	sw	$v0, -20($s0)
L_44:
	# 44 := 0 _ counter #
	li	$t1, 0
	sw	$t1, -24($s0)
L_45:
	# 45 jump _ _ 46 #
	j	L_46
L_46:
	# 46 jump _ _ 6 #
	j	L_6
L_47:
	# 47 halt _ _ _ #
L_48:
	# 48 end_block pingpong _ _ #
	lw	$ra, ($sp)
	jr	$ra
