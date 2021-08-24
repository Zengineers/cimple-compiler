#include <stdio.h>


int main()
{
	int T_1, T_2, T_3, T_4, T_5;
	int rows, i, j, line;
	
	L_1:		// (begin_block, pyramid, _, _)
	L_2:  scanf("%d", &rows);		// (inp, rows, _, _)
	L_3:  i = 1;		// (:=, 1, _, i)
	L_4:  line = i;		// (:=, i, _, line)
	L_5:  if (i <= rows) goto L_7;		// (<=, i, rows, 7)
	L_6:  goto L_29;		// (jump, _, _, 29)
	L_7:  if (i == 1) goto L_9;		// (=, i, 1, 9)
	L_8:  goto L_11;		// (jump, _, _, 11)
	L_9:  printf("line: %d\n", line);		// (out, line, _, _)
	L_10:  goto L_11;		// (jump, _, _, 11)
	L_11:  if (i > 5) goto L_13;		// (>, i, 5, 13)
	L_12:  goto L_22;		// (jump, _, _, 22)
	L_13:  if (i > 10) goto L_15;		// (>, i, 10, 15)
	L_14:  goto L_18;		// (jump, _, _, 18)
	L_15:  T_1 = rows + 1;		// (+, rows, 1, T_1)
	L_16:  i = T_1;		// (:=, T_1, _, i)
	L_17:  goto L_21;		// (jump, _, _, 21)
	L_18:  T_2 = line / 10;		// (/, line, 10, T_2)
	L_19:  line = T_2;		// (:=, T_2, _, line)
	L_20:  printf("line: %d\n", line);		// (out, line, _, _)
	L_21:  goto L_26;		// (jump, _, _, 26)
	L_22:  T_3 = line * 10;		// (*, line, 10, T_3)
	L_23:  T_4 = T_3 + 1;		// (+, T_3, 1, T_4)
	L_24:  line = T_4;		// (:=, T_4, _, line)
	L_25:  printf("line: %d\n", line);		// (out, line, _, _)
	L_26:  T_5 = i + 1;		// (+, i, 1, T_5)
	L_27:  i = T_5;		// (:=, T_5, _, i)
	L_28:  goto L_5;		// (jump, _, _, 5)
	L_29:  {}		// (halt, _, _, _)
}		// (end_block, pyramid, _, _)