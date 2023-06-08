# riscvhpp
 A user-level C++17 header-only RISC-V emulator generator using [riscv-opcodes](https://github.com/riscv/riscv-opcodes).

## Generating the emulator

To build just the emulator, type:

```sh
make src/riscv.hpp
```

then just copy it and src/encoding.out.h into your project.

To build the full emulator, including test code, type:

```sh
make
```

## Using the emulator

Below is a snippet of code representing a minimal working example of the emulator:

```c++
// The emulator
#include "riscv.hpp"

// For std::unique_ptr
#include <memory>

// For std::printf
#include <cstdio>

// For std::memcpy
#include <cstring>

using cpu_t = riscv::CPU<riscv::ISA_BASE_32I>; // Creates CPU with ISA rv32i

int main() {
    std::unique_ptr<cpu_t> cpu = std::make_unique<cpu_t>();

    // Copy program to dram.
    const uint8_t program[] = { 
        0x93, 0x08, 0xd0, 0x05, // li a7, 93
        0x73, 0x00, 0x00, 0x00, // ecall
    };
    std::memcpy(cpu->bus.dram.memory, program, sizeof(program));
    
    cpu_t::err_t err;
    while(1) {
        do {
            err = cpu->execute();
        } while(err == cpu_t::OK);

        if(err == cpu_t::ECALL) {
            switch(cpu.reg[REG_A(7)])
            {
                case 64:
                {
                    std::printf("Write 0x%08llx, %llu chars\n", cpu.reg[REG_A(1)], cpu.reg[REG_A(2)]);
                    char dest[cpu.reg[REG_A(2)] + 1];
                    for(cpu_t::sreg_t i = 0; i < cpu.reg[REG_A(2)]; ++i) {
                        dest[i] = cpu.load(cpu.reg[REG_A(1)] + i, 8);
                    }
                    dest[cpu.reg[REG_A(2)]] = 0;
                    cpu.reg[REG_A(0)] = printf("%s", dest);
                    break;
                }

                case 93:
                    printf("Program returned %lld.\n", (int64_t)(cpu_t::sreg_t)cpu->reg[REG_A(0)]);
                    return 0;

                default:
                    printf("Error, unsupported ecall number %llu.\n", (uint64_t)cpu.reg[REG_A(7)]);
                    return -1;
            }
        }
        else {
            printf("CPU returned error code %llu.\n", (uint64_t)err);
            return -1;
        }
    }
}
```

`ecall` and `ebreak` are not implemented by the emulator. Instead, when encountering the instruction, the emulator will return the code back to the programmer as a `cpu_t`, allowing the programmer to define how to handle different ecall codes. This allows a great deal of flexibility with how the emulator interacts with the host system.

## Conclusion

This emulator is still in progress, so things may not work as expected and a lot of features and instructions still do not have implementations yet. Keep this is mind if you plan to build software with this emulator.

## License

This project is licensed under the Apache License Version 2.0. © 2023 Matthew Obi.
