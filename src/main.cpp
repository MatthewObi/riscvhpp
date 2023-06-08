// This project is licensed under the Apache License Version 2.0.
// ©Matthew Obi 2023
#include "./riscv.hpp"
#include <memory>

void load_program(riscv::DRAM& dram) {
    FILE* f = fopen("test.bin", "rb");
    if(f) {
        fseek(f, 0, SEEK_END);
        size_t size = ftell(f);
        fseek(f, 0, SEEK_SET);
        fread(dram.memory, 1, size, f);
        fclose(f);
        return;
    }
    fprintf(stderr, "Could not open file '%s'.\n", "test.bin");
    exit(-1);
}

// rv32icafm_zifencei
constexpr uint64_t isa = riscv::ISA_BASE_32I | ISA_EXT('C') | ISA_EXT('A') | riscv::ISA_EXT_F | ISA_EXT('M') | riscv::ISA_EXT_ZIFENCEI;
using cpu_t = riscv::CPU<isa>;

cpu_t::err_t ecall(cpu_t& cpu) {
    switch(cpu.reg[REG_A(7)])
    {
        case 64:
        {
            printf("Write 0x%08llx, %llu chars\n", cpu.reg[REG_A(1)], cpu.reg[REG_A(2)]);
            char dest[cpu.reg[REG_A(2)] + 1];
            for(cpu_t::sreg_t i = 0; i < cpu.reg[REG_A(2)]; ++i) {
                dest[i] = cpu.load(cpu.reg[REG_A(1)] + i, 8);
            }
            dest[cpu.reg[REG_A(2)]] = 0;
            cpu.reg[REG_A(0)] = printf("%s", dest);
            return cpu_t::OK;
        }

        case 93:
            return cpu_t::END_OF_PROG;

        default:
            return cpu_t::MISC_ERR;
    }
}

int main() {
    std::unique_ptr<cpu_t> cpu = std::make_unique<cpu_t>();
    cpu->pc = 0x80000000;
    cpu->reg[REG_SP] = 0x80001000;
    load_program(cpu->bus.dram);

    cpu_t::err_t err;
    while(1) 
    {
        do {
            err = cpu->execute();
        } while(err == cpu_t::OK);

        if(err == cpu_t::ECALL) {
            err = ecall(*cpu);
            if(err == cpu_t::OK)
                continue;
        }

        switch(err)
        {
        case cpu_t::ILLEGAL_INSTRUCTION:
            printf("Illegal instruction.\n");
            return err;
        case cpu_t::EBREAK:
            printf("ebreak\n");
            return err;
        case cpu_t::END_OF_PROG:
            printf("Program returned %lld.\n", (int64_t)(cpu_t::sreg_t)cpu->reg[REG_A(0)]);
            return 0;
        default:
            printf("Unknown error.\n");
            return err;
        }
    }
    return 0;
}