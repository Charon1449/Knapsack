all:
	g++ branch_bound.cpp -obranch -O3 -masm=intel -no-pie
