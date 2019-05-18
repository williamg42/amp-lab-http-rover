# main compiler
CXX := g++

TARGET1 := main

all: $(TARGET1)

$(TARGET1): 
	@echo "Compiling C++ program"
	$(CXX) $(CFLAGS) *.cpp -o PWM.exe $(LDFLAGS) -l$(LIB)

clean:
	@rm -rf $(TARGET1) $(TARGET2)
