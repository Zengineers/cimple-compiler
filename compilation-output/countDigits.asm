L_1:
	# 1 begin_block countDigits _ _ #
	add	$sp, $sp, 28
	move	$s0, $sp
L_2:
	# 2 inp x _ _ #
	li	$v0, 5
	syscall
	sw	$v0, -12($s0)
L_3:
	# 3 := 0 _ count #
	li	$t1, 0
	sw	$t1, -16($s0)
L_4:
	# 4 > x 0 6 #
	lw	$t1, -12($s0)
	li	$t2, 0
	bgt	$t1, $t2, L_6
L_5:
	# 5 jump _ _ 11 #
	j	L_11
L_6:
	# 6 / x 10 T_1 #
	lw	$t1, -12($s0)
	li	$t2, 10
	div	$t1, $t1, $t2
	sw	$t1, -20($s0)
L_7:
	# 7 := T_1 _ x #
	lw	$t1, -20($s0)
	sw	$t1, -12($s0)
L_8:
	# 8 + count 1 T_2 #
	lw	$t1, -16($s0)
	li	$t2, 1
	add	$t1, $t1, $t2
	sw	$t1, -24($s0)
L_9:
	# 9 := T_2 _ count #
	lw	$t1, -24($s0)
	sw	$t1, -16($s0)
L_10:
	# 10 jump _ _ 4 #
	j	L_4
L_11:
	# 11 out count _ _ #
	li	$v0, 1
	lw	$a0, -16($s0)
	syscall
L_12:
	# 12 halt _ _ _ #
L_13:
	# 13 end_block countDigits _ _ #
	lw	$ra, ($sp)
	jr	$ra
