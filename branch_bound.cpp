//https://github.com/MinaMeh/Knapsack-problem/raw/master/BranchAndBound.py
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <time.h>


typedef unsigned long long ll;
typedef struct item {
	ll weight;
	ll value;
} item;


typedef struct knapsack_solution {
	ll optweight;
	ll optvalue;
	ssize_t* taken_items; // indices of the taken items
} knapsack_solution;

ll cycles;
clock_t times;

size_t compare_density(item* A, item* B)
{
	int density_A = A->value / A->weight;
	int density_B = B->value / B->weight;
	if (density_A < density_B) return 1;
	if (density_A > density_B) return -1;
	return 0;
}

knapsack_solution* knapsack_bb(item* items, size_t n, int capacity)
{
	// sort from max to least
	times = clock();
	asm("rdtsc;"\
		"shl rdx, 32;"\
		"add rax,rdx;"\
		"mov [cycles],rax"\
	);
	qsort(items, n, sizeof(item), (comparison_fn_t) compare_density);
	ssize_t* tab = (ssize_t*)malloc(n * sizeof(item));
	memset(tab, 0, n*sizeof(ssize_t));
	ll max_weight=capacity;
	ll current_value = 0;
	ll maximum;
	for (ssize_t i = 0; i < n; i++)
	{
		maximum = max_weight / items[i].weight;
		if (maximum < 0) maximum = 0;
		tab[i] = maximum;
		current_value += maximum * items[i].value;
		max_weight -= maximum*items[i].weight;
	}
	ll max_value = current_value;
	
	ssize_t* set = (ssize_t*) malloc(n * sizeof(ssize_t));
	memcpy(set, tab, n*sizeof(ssize_t));
	char flag = 1;
	while (flag)
	{
		int leastSignificant = n - 1;
		for (size_t i = leastSignificant; i >= 0; i--)
			if (set[i] != 0)
			{
				leastSignificant = i;
				break;
			}
		if (leastSignificant == n-1)
		{
			max_weight += set[leastSignificant]*items[leastSignificant].weight;
			set[leastSignificant] = 0;
		}
		else
		{
			max_weight += items[leastSignificant].weight;
			set[leastSignificant] -= 1;
			for (size_t i = leastSignificant+1; i < n; i++)
			{
				maximum = max_weight / items[i].weight;
				if (maximum > 0)
					set[i] = maximum;
				else
					maximum = 0;
				max_weight -= maximum * items[i].weight;
			}
			//current_value=sum(items[i][VALUE] * n for i, n in enumerate(set))
			current_value = 0;
			for (size_t i = 0; i < n; i++)
				current_value += items[i].value * set[i];
			
			if (current_value > max_value)
			{
				max_value = current_value;
				memcpy(tab, set, n*sizeof(item));
			}
		}
		int itemcount = 0;
		for (size_t i = 0; i < n; i++)
			itemcount += set[i];
		if (itemcount == 0) flag = 0;
	}
	times = clock();
	asm("rdtsc;"\
		"shl rdx, 32;"\
		"add rax,rdx;"\
		"mov [cycles],rax"\
	);
	knapsack_solution* sol = (knapsack_solution*) malloc(sizeof(knapsack_solution));
	sol->optweight = max_weight;
	sol->optvalue = max_value;
	sol->taken_items = tab;
	return sol;
}

int main()
{
	if (freopen("data.txt", "r", stdin) == NULL)
	{
		perror(strerror(errno));
		exit(1);
	}
	ssize_t num_items, capacity;
	scanf("%d %d", &num_items, &capacity);
	item* items = (item*)malloc(num_items * sizeof(item));
	if (items == NULL)
	{
		perror(strerror(errno));
		exit(1);
	}
	for (ssize_t k = 0; k < num_items; k++)
		scanf("%d %d", &items[k].weight, &items[k].value);
	printf("[*] Objects are:\n");
	for (ssize_t k = 0; k < num_items; k++)
		printf("\t - {weight = %d, value = %d}\n", items[k].weight, items[k].value);
	printf("[*] Knapsack capacity = %d\n", capacity);
	knapsack_solution* sol = knapsack_bb(items, num_items, capacity);
	printf("[+] solution:\n\t - weight = %d\n\t - value = %d\n\t - items:\n", sol->optweight, sol->optvalue);
	for (ssize_t k = 0; k < num_items; k++)
		printf("\t\t - %d of {weight=%d, value=%d}\n", sol->taken_items[k], items[k].weight, items[k].value);

    printf("cycles: %lld\ntime: %g s\n", cycles, (float)times/CLOCKS_PER_SEC);
}
