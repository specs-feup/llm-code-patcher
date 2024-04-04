static int global = 0;

struct s {
	int d;
	float f;
};

int foo(int a, int b) {
	struct s si;
	
	
	
	return 0 + global + si.d;
}


int bar(int a, int b) {
	return 1 + foo(a, b);
}	