#include <stdio.h>


int main()
{
	int T_1, T_2;
	int x, count;
	
	L_1:		// (begin_block, countDigits, _, _)
	L_2:  scanf("%d", &x);		// (inp, x, _, _)
	L_3:  count = 0;		// (:=, 0, _, count)
	L_4:  if (x > 0) goto L_6;		// (>, x, 0, 6)
	L_5:  goto L_11;		// (jump, _, _, 11)
	L_6:  T_1 = x / 10;		// (/, x, 10, T_1)
	L_7:  x = T_1;		// (:=, T_1, _, x)
	L_8:  T_2 = count + 1;		// (+, count, 1, T_2)
	L_9:  count = T_2;		// (:=, T_2, _, count)
	L_10:  goto L_4;		// (jump, _, _, 4)
	L_11:  printf("count: %d\n", count);		// (out, count, _, _)
	L_12:  {}		// (halt, _, _, _)
}		// (end_block, countDigits, _, _)