#Makefile fo user lib
ROOTCFLAGS  = `root-config --cflags`
ROOTLIBS    = `root-config --libs`
ROOTGLIBS   = `root-config --glibs`

CXX        = g++
CXXFLAGS   = -g -Wall -fPIC
LD         = g++

CXXFLAGS  += $(ROOTCFLAGS) 
LIBS       = $(ROOTLIBS) 
GLIBS      = $(ROOTGLIBS)
LDFLAGS    = -Wl,--no-as-needed $(LIBS) $(GLIBS)
SOFLAGS    = -shared

libTreeProcess.so: treeProcess.o
	$(CXX) $(SOFLAGS) -o libTreeProcess.so treeProcess.o $(CXXFLAGS) $(LIBS) 
treeProcess.o: treeProcess.cc
	$(CXX) $(SOFLAGS) -c $(CXXFLAGS) treeProcess.cc -o treeProcess.o
clean:
	rm -f *.o
