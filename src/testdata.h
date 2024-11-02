/* This file was generated by json2code.py */

#ifndef INPUT_H
#define INPUT_H

#ifndef __cplusplus
extern "C" {
#endif /* __cplusplus */

typedef struct {
	int int_var;
	double decimal;
	double another_one;
	char string_var[12];
	int b1;
	int b2;
	int int_arr[3];
	double dbl_arr[3];
	double promoted_arr[3];
	int bool_arr[2];
	char string_arr[4][9];
	double nested[3][3];
} inputType;

inputType input = {
	1,
	1.234,
	0.034,
	"hello world",
	1,
	0,
	{1, 2, 3},
	{1.2, 1e-10, 2.2},
	{1, 2, 1.3},
	{1, 0},
	{"hello", "world", "again", "computer"},
	{{1, 2, 3}, {3, 2}, {1, 2.3}}
};

#ifndef __cplusplus
}
#endif /* __cplusplus */

#endif /* INPUT_H */