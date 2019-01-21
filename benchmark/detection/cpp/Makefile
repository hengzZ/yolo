SDIR=./
ODIR=./obj


TARGET=evaluate_object
CXX=g++
CXXFLAGS=-O3 -Wall \
	 -std=c++11 \
	 -I/usr/local/include/png++/ \
	 -I/usr/include/libpng12 
CXXLIBS=\
	-L/usr/lib/x86_64-linux-gnu \
	-lpng12

SRCS=$(wildcard $(SDIR)/*.cpp)
OBJS=$(patsubst %.cpp, $(ODIR)/%.o, $(notdir $(SRCS)))


all: dir $(TARGET)

$(TARGET): $(OBJS)
	$(CXX) -o $@ $^ $(CXXFLAGS) $(CXXLIBS)

$(ODIR)/%.o: $(SDIR)/%.cpp
	$(CXX) -c -o $@ $< $(CXXFLAGS)

dir:
	mkdir -p $(ODIR)

clean:
	rm -rf $(ODIR) $(TARGET)

.PHONY: clean
