L_1:
	# 1 begin_block pyramid _ _ #
	add	$sp, $sp, 48
	move	$s0, $sp
L_2:
	# 2 inp rows _ _ #
	li	$v0, 5
	syscall
	sw	$v0, -12($s0)
L_3:
	# 3 := 1 _ i #
	li	$t1, 1
	sw	$t1, -16($s0)
L_4:
	# 4 := i _ line #
	lw	$t1, -16($s0)
	sw	$t1, -24($s0)
L_5:
	# 5 <= i rows 7 #
	lw	$t1, -16($s0)
	lw	$t2, -12($s0)
	ble	$t1, $t2, L_7
L_6:
	# 6 jump _ _ 29 #
	j	L_29
L_7:
	# 7 = i 1 9 #
	lw	$t1, -16($s0)
	li	$t2, 1
	beq	$t1, $t2, L_9
L_8:
	# 8 jump _ _ 11 #
	j	L_11
L_9:
	# 9 out line _ _ #
	li	$v0, 1
	lw	$a0, -24($s0)
	syscall
L_10:
	# 10 jump _ _ 11 #
	j	L_11
L_11:
	# 11 > i 5 13 #
	lw	$t1, -16($s0)
	li	$t2, 5
	bgt	$t1, $t2, L_13
L_12:
	# 12 jump _ _ 22 #
	j	L_22
L_13:
	# 13 > i 10 15 #
	lw	$t1, -16($s0)
	li	$t2, 10
	bgt	$t1, $t2, L_15
L_14:
	# 14 jump _ _ 18 #
	j	L_18
L_15:
	# 15 + rows 1 T_1 #
	lw	$t1, -12($s0)
	li	$t2, 1
	add	$t1, $t1, $t2
	sw	$t1, -28($s0)
L_16:
	# 16 := T_1 _ i #
	lw	$t1, -28($s0)
	sw	$t1, -16($s0)
L_17:
	# 17 jump _ _ 21 #
	j	L_21
L_18:
	# 18 / line 10 T_2 #
	lw	$t1, -24($s0)
	li	$t2, 10
	div	$t1, $t1, $t2
	sw	$t1, -32($s0)
L_19:
	# 19 := T_2 _ line #
	lw	$t1, -32($s0)
	sw	$t1, -24($s0)
L_20:
	# 20 out line _ _ #
	li	$v0, 1
	lw	$a0, -24($s0)
	syscall
L_21:
	# 21 jump _ _ 26 #
	j	L_26
L_22:
	# 22 * line 10 T_3 #
	lw	$t1, -24($s0)
	li	$t2, 10
	mul	$t1, $t1, $t2
	sw	$t1, -36($s0)
L_23:
	# 23 + T_3 1 T_4 #
	lw	$t1, -36($s0)
	li	$t2, 1
	add	$t1, $t1, $t2
	sw	$t1, -40($s0)
L_24:
	# 24 := T_4 _ line #
	lw	$t1, -40($s0)
	sw	$t1, -24($s0)
L_25:
	# 25 out line _ _ #
	li	$v0, 1
	lw	$a0, -24($s0)
	syscall
L_26:
	# 26 + i 1 T_5 #
	lw	$t1, -16($s0)
	li	$t2, 1
	add	$t1, $t1, $t2
	sw	$t1, -44($s0)
L_27:
	# 27 := T_5 _ i #
	lw	$t1, -44($s0)
	sw	$t1, -16($s0)
L_28:
	# 28 jump _ _ 5 #
	j	L_5
L_29:
	# 29 halt _ _ _ #
L_30:
	# 30 end_block pyramid _ _ #
	lw	$ra, ($sp)
	jr	$ra
