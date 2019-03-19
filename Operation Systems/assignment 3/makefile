HEADERS = ls.h inbuilt.h pinfo.h

default: bash

bash.o : bash.c $(HEADERS)
	gcc -c bash.c -o bash.o

bash: bash.o
	gcc bash.o -o bash

clean:
	-rm -f bash.o
	-rm -f bash
