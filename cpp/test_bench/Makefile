CXX = g++
# Ensure NO spaces at the end of the line below!
SC_HOME = /usr/local/systemc-2.3.3

CXXFLAGS = -I$(SC_HOME)/include -L$(SC_HOME)/lib-linux64 -lsystemc -Wl,-rpath,$(SC_HOME)/lib-linux64

TARGET = run_testbench
SRCS = main.cpp

all:
	$(CXX) $(SRCS) $(CXXFLAGS) -o $(TARGET)

clean:
	rm -f $(TARGET) simulation_results.csv