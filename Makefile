NAME := riscv-emu
CC = cc
CXX = c++
COPY := cp

SRCSC := $(wildcard src/*.c)
SRCSCXX := $(wildcard src/*.cpp)
OBJS := $(patsubst %.c,%.o,$(SRCSC)) $(patsubst %.cpp,%.o,$(SRCSCXX))

RM := rm -rf 

DEPS := $(OBJS:.o=.d)

CCFLAGS = -MMD -O2 -std=c99
CXXFLAGS = -MMD -O2 -std=c++17

all: $(NAME).exe

$(NAME).exe: src/riscv.hpp $(OBJS) 
	$(CXX) -o $@ $^

-include $(DEPS)

%.o: %.c 
	$(CC) -c -o $@ $(CCFLAGS) $<

%.o: %.cpp 
	$(CXX) -c -o $@ $(CXXFLAGS) $<

src/riscv.hpp: src/encoding.out.h instr_dict.yaml tools/constants.py
	python tools/generate.py

src/encoding.out.h: encoding.out.h 
	$(COPY) ./encoding.out.h ./src/encoding.out.h

encoding.out.h: 
	python riscv-opcodes/parse.py -c rv* 

instr_dict.yaml: encoding.out.h

tools/constants.py: encoding.out.h
	$(COPY) riscv-opcodes/constants.py ./tools/constants.py 

.PHONY:
clean:
	$(RM) $(NAME).exe src/*.o 

clean_emu:
	$(RM) src/riscv.hpp 

clean_all: clean clean_emu
	$(RM) instr_dict.yaml src/encoding.out.h encoding.out.h