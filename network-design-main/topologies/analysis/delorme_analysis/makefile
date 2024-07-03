CC      = g++
CPPFLAGS= -O3 -c -std=c++11 -w 
LDFLAGS = -m64 
SOURCES = main.cpp 
OBJECTS = $(SOURCES:.cpp=.o)

all: $(SOURCES) analyze 

analyze : $(OBJECTS)  

	$(CC) $(OBJECTS) $(LDFLAGS) -o $@

.cpp.o : 
	$(CC) $(CPPFLAGS) $< -o $@

clean:
	rm -f *.o analyze core* 
