all: fork_loop who_runs_first

who_runs_first: who_runs_first.c
	gcc -o who_runs_first who_runs_first.c

fork_loop: fork_loop.c
	gcc -o fork_loop fork_loop.c

clean:
	-rm -rf fork_loop who_runs_first