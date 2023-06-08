# This project is licensed under the Apache License Version 2.0.
# ©Matthew Obi 2023
from constants import *
from bm_constants import *
import yaml 

with open('./instr_dict.yaml') as f:
    x: dict = yaml.load(f, Loader=yaml.CLoader)

for k, v in x.items():
    v['extension'] = [ext[ext.find('riscv-opcodes')+14:] if 'riscv-opcodes' in ext else ext for ext in v['extension']]

macros = {
    'add': 'reg[rd(ins)] = reg[rs1(ins)] + reg[rs2(ins)];\npc += 4;\nreturn OK;',
    'slt': 'reg[rd(ins)] = ((sreg_t)reg[rs1(ins)] < (sreg_t)reg[rs2(ins)])? 1: 0;\npc += 4;\nreturn OK;',
    'sltu': 'reg[rd(ins)] = (reg[rs1(ins)] < reg[rs2(ins)])? 1: 0;\npc += 4;\nreturn OK;',
    'sub': 'reg[rd(ins)] = reg[rs1(ins)] - reg[rs2(ins)];\npc += 4;\nreturn OK;',
    'and': 'reg[rd(ins)] = reg[rs1(ins)] & reg[rs2(ins)];\npc += 4;\nreturn OK;',
    'or' : 'reg[rd(ins)] = reg[rs1(ins)] | reg[rs2(ins)];\npc += 4;\nreturn OK;',
    'xor': 'reg[rd(ins)] = reg[rs1(ins)] ^ reg[rs2(ins)];\npc += 4;\nreturn OK;',
    'sll': 'reg[rd(ins)] = reg[rs1(ins)] << (reg[rs2(ins)] & 0x1f);\npc += 4;\nreturn OK;',
    'srl': 'reg[rd(ins)] = reg[rs1(ins)] >> (reg[rs2(ins)] & 0x1f);\npc += 4;\nreturn OK;',
    'sra': 'reg[rd(ins)] = (sreg_t)reg[rs1(ins)] >> (reg[rs2(ins)] & 0x1f);\npc += 4;\nreturn OK;',
    'addi': 'reg[rd(ins)] = reg[rs1(ins)] + (sreg_t)imm12(ins);\npc += 4;\nreturn OK;',
    'slti': 'reg[rd(ins)] = ((sreg_t)reg[rs1(ins)] < (sreg_t)imm12(ins))? 1: 0;\npc += 4;\nreturn OK;',
    'xori': 'reg[rd(ins)] = reg[rs1(ins)] ^ (sreg_t)imm12(ins);\npc += 4;\nreturn OK;',
    'ori' : 'reg[rd(ins)] = reg[rs1(ins)] | (sreg_t)imm12(ins);\npc += 4;\nreturn OK;',
    'andi': 'reg[rd(ins)] = reg[rs1(ins)] & (sreg_t)imm12(ins);\npc += 4;\nreturn OK;',
    'slli': 'reg[rd(ins)] = reg[rs1(ins)] << (shamtd(ins));\npc += 4;\nreturn OK;',
    'srli': 'reg[rd(ins)] = reg[rs1(ins)] >> (shamtd(ins));\npc += 4;\nreturn OK;',
    'srai': 'reg[rd(ins)] = (sreg_t)reg[rs1(ins)] >> (shamtd(ins));\npc += 4;\nreturn OK;',
    'bne' : 'if(reg[rs1(ins)] != reg[rs2(ins)])\n    pc += (sreg_t)bimm12hl(ins);\nelse\n    pc += 4;\nreturn OK;',
    'beq' : 'if(reg[rs1(ins)] == reg[rs2(ins)])\n    pc += (sreg_t)bimm12hl(ins);\nelse\n    pc += 4;\nreturn OK;',
    'blt' : 'if((sreg_t)reg[rs1(ins)] <  (sreg_t)reg[rs2(ins)])\n    pc += (sreg_t)bimm12hl(ins);\nelse\n    pc += 4;\nreturn OK;',
    'bge' : 'if((sreg_t)reg[rs1(ins)] >= (sreg_t)reg[rs2(ins)])\n    pc += (sreg_t)bimm12hl(ins);\nelse\n    pc += 4;\nreturn OK;',
    'bltu': 'if(reg[rs1(ins)] <  reg[rs2(ins)])\n    pc += (sreg_t)bimm12hl(ins);\nelse\n    pc += 4;\nreturn OK;',
    'bgeu': 'if(reg[rs1(ins)] >= reg[rs2(ins)])\n    pc += (sreg_t)bimm12hl(ins);\nelse\n    pc += 4;\nreturn OK;',
    'lb': 'reg[rd(ins)] = (sreg_t)(int8_t)load(reg[rs1(ins)] + (sreg_t)imm12(ins), 8);\npc += 4;\nreturn OK;',
    'lbu': 'reg[rd(ins)] = (ureg_t)(uint8_t)load(reg[rs1(ins)] + (sreg_t)imm12(ins), 8);\npc += 4;\nreturn OK;',
    'lh': 'reg[rd(ins)] = (sreg_t)(int16_t)load(reg[rs1(ins)] + (sreg_t)imm12(ins), 16);\npc += 4;\nreturn OK;',
    'lhu': 'reg[rd(ins)] = (ureg_t)(uint16_t)load(reg[rs1(ins)] + (sreg_t)imm12(ins), 16);\npc += 4;\nreturn OK;',
    'lw': 'reg[rd(ins)] = (sreg_t)(int32_t)load(reg[rs1(ins)] + (sreg_t)imm12(ins), 32);\npc += 4;\nreturn OK;',
    'lwu': 'reg[rd(ins)] = (ureg_t)(uint32_t)load(reg[rs1(ins)] + (sreg_t)imm12(ins), 32);\npc += 4;\nreturn OK;',
    'sb': 'store(reg[rs1(ins)] + (sreg_t)imm12hl(ins), 8, (uint8_t)reg[rs2(ins)]);\npc += 4;\nreturn OK;',
    'sh': 'store(reg[rs1(ins)] + (sreg_t)imm12hl(ins), 16, (uint16_t)reg[rs2(ins)]);\npc += 4;\nreturn OK;',
    'sw': 'store(reg[rs1(ins)] + (sreg_t)imm12hl(ins), 32, (uint32_t)reg[rs2(ins)]);\npc += 4;\nreturn OK;',
    'lui': 'reg[rd(ins)] = imm20(ins);\npc += 4;\nreturn OK;',
    'auipc': 'reg[rd(ins)] = (ureg_t)(pc + (sreg_t)imm20(ins));\npc += 4;\nreturn OK;',
    'jal': 'reg[rd(ins)] = pc + 4;\npc = (pc + ((int64_t)jimm20(ins) << 1));\nreturn OK;',
    'jalr': 'reg[rd(ins)] = pc + 4;\npc = (reg[rs1(ins)] + ((int64_t)imm12(ins) << 1));\nreturn OK;',
    'c_lwsp' : 'reg[rd(ins)] = (sreg_t)(int32_t)load(reg[REG_SP] + (ureg_t)c_uimm8sphl(ins), 32);\npc += 2;\nreturn OK;',
    'c_ldsp' : 'reg[rd(ins)] = (sreg_t)(int64_t)load(reg[REG_SP] + (ureg_t)c_uimm9sphl(ins), 32);\npc += 2;\nreturn OK;',
    'c_lw' : 'reg[rd_p(ins)] = (sreg_t)(int32_t)load(reg[rs1_p(ins)] + (ureg_t)c_uimm7hl(ins), 32);\npc += 2;\nreturn OK;',
    'c_sw' : 'store(reg[rs1_p(ins)] + (ureg_t)c_uimm7hl(ins), 32, (uint32_t)reg[rs2_p(ins)]);\npc += 2;\nreturn OK;',
    'c_swsp' : 'store(reg[REG_SP] + (ureg_t)c_uimm8sp_s(ins), 32, (uint32_t)reg[c_rs2(ins)]);\npc += 2;\nreturn OK;',
    'c_mv' : 'reg[rd(ins)] = reg[c_rs2_n0(ins)];\npc += 2;\nreturn OK;',
    'c_add': 'reg[rd(ins)] += (sreg_t)reg[c_rs2_n0(ins)];\npc += 2;\nreturn OK;',
    'c_addi': 'reg[rd_rs1_n0(ins)] += (sreg_t)c_nzimm6hl(ins);\npc += 2;\nreturn OK;',
    'c_addi16sp': 'reg[REG_SP] += (sreg_t)c_nzimm10hl(ins);\npc += 2;\nreturn OK;',
    'c_addi4spn': 'reg[rd_p(ins)] = reg[REG_SP] + (ureg_t)c_nzuimm10(ins);\npc += 2;\nreturn OK;',
    'c_and': 'reg[rd_rs1_p(ins)] &= reg[rs2_p(ins)];\npc += 2;\nreturn OK;',
    'c_or' : 'reg[rd_rs1_p(ins)] |= reg[rs2_p(ins)];\npc += 2;\nreturn OK;',
    'c_xor': 'reg[rd_rs1_p(ins)] ^= reg[rs2_p(ins)];\npc += 2;\nreturn OK;',
    'c_j' : 'pc += ((sreg_t)c_imm12(ins) << 1);\nreturn OK;',
    'c_jr' : 'pc = reg[c_rs1_n0(ins)];\nreturn OK;',
    'c_jal' : 'reg[REG_RA] = pc + 2;\npc += ((sreg_t)c_imm12(ins));\nreturn OK;',
    'c_jalr' : 'reg[REG_RA] = pc + 2;\npc = reg[c_rs1_n0(ins)];\nreturn OK;',
    'c_beqz' : 'if(reg[rs1_p(ins)] == 0)\n    pc += (sreg_t)c_bimm9hl(ins);\nelse\n    pc += 2;\nreturn OK;',
    'c_bnez' : 'if(reg[rs1_p(ins)] != 0)\n    pc += (sreg_t)c_bimm9hl(ins);\nelse\n    pc += 2;\nreturn OK;',
    'c_li' : 'reg[rd(ins)] = (sreg_t)c_imm6hl(ins);\npc += 2;\nreturn OK;',
    'c_lui' : 'reg[rd(ins)] = (sreg_t)c_nzimm18hl(ins);\npc += 2;\nreturn OK;',
    'flw': 'freg[rd(ins)] = bitcast<float>((uint32_t)load(reg[rs1(ins)] + (sreg_t)imm12(ins), 32));\npc += 4;\nreturn OK;',
    'fsqrt_s': 'freg[rd(ins)] = sqrtf(freg[rs1(ins)]);\npc += 4;\nreturn OK;',
    'flt_s': 'reg[rd(ins)] = ((float)freg[rs1(ins)] < (float)freg[rs2(ins)])? 1: 0;\npc += 4;\nreturn OK;',
    'feq_s': 'reg[rd(ins)] = ((float)freg[rs1(ins)] == (float)freg[rs2(ins)])? 1: 0;\npc += 4;\nreturn OK;',
    'fle_s': 'reg[rd(ins)] = ((float)freg[rs1(ins)] <= (float)freg[rs2(ins)])? 1: 0;\npc += 4;\nreturn OK;',
    'fsgnj_s': 'freg[rd(ins)] = sgnj32(freg[rs1(ins)], freg[rs2(ins)], false, false);\npc += 4;\nreturn OK;',
    'fsgnjn_s': 'freg[rd(ins)] = sgnj32(freg[rs1(ins)], freg[rs2(ins)], true, false);\npc += 4;\nreturn OK;',
    'fsgnjx_s': 'freg[rd(ins)] = sgnj32(freg[rs1(ins)], freg[rs2(ins)], false, true);\npc += 4;\nreturn OK;',
    'fadd_s': 'freg[rd(ins)] = (float)freg[rs1(ins)] + (float)freg[rs2(ins)];\npc += 4;\nreturn OK;',
    'fmul_s': 'freg[rd(ins)] = (float)freg[rs1(ins)] * (float)freg[rs2(ins)];\npc += 4;\nreturn OK;',
    'fcvt_w_s': 'reg[rd(ins)] = (sreg_t)(int32_t)freg[rs1(ins)];\npc += 4;\nreturn OK;',
    'fcvt_s_w': 'freg[rd(ins)] = (float)reg[rs1(ins)];\npc += 4;\nreturn OK;',
    'ecall' : 'pc += 4;\nreturn ECALL;',
    'ebreak' : 'pc += 4;\nreturn EBREAK;'
}

print_macros = {
    'lw': ([
        ('imm12(ins) == 0', 'lw {}, [{}]', 'rd', 'rs1')], 
        'lw {}, [{} + {}]', 'rd', 'rs1', 'imm12'),
    'lh': ([
        ('imm12(ins) == 0', 'lh {}, [{}]', 'rd', 'rs1')], 
        'lh {}, [{} + {}]', 'rd', 'rs1', 'imm12'),
    'lb': ([
        ('imm12(ins) == 0', 'lb {}, [{}]', 'rd', 'rs1')], 
        'lb {}, [{} + {}]', 'rd', 'rs1', 'imm12'),
    'lbu': ([
        ('imm12(ins) == 0', 'lbu {}, [{}]', 'rd', 'rs1')], 
        'lbu {}, [{} + {}]', 'rd', 'rs1', 'imm12'),
    'sb': ([
        ('imm12hl(ins) == 0', 'sb [{}], {}', 'rs1', 'rs2')], 
        'sb [{} + {}], {}', 'rs1', 'imm12hl', 'rs2'),
    'sh': ([
        ('imm12hl(ins) == 0', 'sh [{}], {}', 'rs1', 'rs2')], 
        'sh [{} + {}], {}', 'rs1', 'imm12hl', 'rs2'),
    'sw': ([
        ('imm12hl(ins) == 0', 'sw [{}], {}', 'rs1', 'rs2')], 
        'sw [{} + {}], {}', 'rs1', 'imm12hl', 'rs2'),
    'c_lw': ([
        ('c_uimm7hl(ins) == 0', 'lw {}, [{}]', 'rd_p', 'rs1_p')], 
        'lw {}, [{} + {}]', 'rd_p', 'rs1_p', 'c_uimm7hl'),
    'c_sw': ([
        ('c_uimm7hl(ins) == 0', 'sw [{}], {}', 'rs1_p', 'rs2_p')], 
        'sw [{} + {}], {}', 'rs1_p', 'c_uimm7hl', 'rs2_p'),
    'c_swsp': ([], 'sw [sp + {}], {}', 'c_uimm8sp_s', 'c_rs2'),
    'c_addi4spn': ([], 'addi {}, sp, {}', 'rd_p', 'c_nzuimm10'),
    'c_addi16sp': ([], 'addi sp, sp, {}', 'c_nzimm10hl'),
    'c_li': ([], 'li {}, {}', 'rd', 'c_imm6hl'),
    'c_addi': ([], 'addi {}, {}, {}', 'rd_rs1_n0', 'rd_rs1_n0', 'c_nzimm6hl'),
    'c_lui': ([], 'lui {}, {}', 'rd', 'shr c_nzimm18hl'),
    'c_and': ([], 'and {}, {}, {}', 'rd_rs1_p', 'rd_rs1_p', 'rs2_p'),
    'c_or' : ([], 'or {}, {}, {}', 'rd_rs1_p', 'rd_rs1_p', 'rs2_p'),
    'c_xor': ([], 'xor {}, {}, {}', 'rd_rs1_p', 'rd_rs1_p', 'rs2_p'),
    'c_jr': ([
        ('c_rs1_n0(ins) == REG_RA', 'ret')], 
        'jr {}', 'c_rs1_n0'),
    'c_jal': ([], 'jal ra, {}', 'addr_rel c_imm12'),
    'lui':   ([], 'lui {}, {}', 'rd', 'shr imm20'),
    'auipc': ([], 'auipc {}, {}', 'rd', 'shr imm20'),
    'addi': ([
        ('rd(ins) == 0', 'nop'),
        ('imm12(ins) == 0', 'mv {}, {}', 'rd', 'rs1'),
        ('rs1(ins) == 0', 'li {}, {}', 'rd', 'imm12')], 
        'addi {}, {}, {}', 'rd', 'rs1', 'imm12'),
    'andi': ([], 
        'andi {}, {}, {}', 'rd', 'rs1', 'imm12'),
    'add': ([
        ('rs1(ins) == 0', 'mv {}, {}', 'rd', 'rs2'),
        ('rs2(ins) == 0', 'mv {}, {}', 'rd', 'rs1')], 
        'add {}, {}, {}', 'rd', 'rs1', 'rs2'),
    'sub': ([
        ('rs1(ins) == 0', 'neg {}, {}', 'rd', 'rs2')], 
        'sub {}, {}, {}', 'rd', 'rs1', 'rs2'),
    'and': ([], 
        'and {}, {}, {}', 'rd', 'rs1', 'rs2'),
    'or': ([], 
        'or {}, {}, {}', 'rd', 'rs1', 'rs2'),
    'xor': ([], 
        'xor {}, {}, {}', 'rd', 'rs1', 'rs2'),
    'slt': ([], 
        'slt {}, {}, {}', 'rd', 'rs1', 'rs2'),
    'sltu': ([
        ('rs1(ins) == 0', 'snez {}, {}', 'rd', 'rs2')], 
        'sltu {}, {}, {}', 'rd', 'rs1', 'rs2'),
    'blt' : ([
        ('rs2(ins) == 0', 'bltz {}, {}', 'rs1', 'addr_rel bimm12hl')], 
        'blt {}, {}, {}', 'rs1', 'rs2', 'addr_rel bimm12hl'),
    'bltu' : ([
        ('rs1(ins) == 0', 'bnez {}, {}', 'rs2', 'addr_rel bimm12hl')], 
        'bltu {}, {}, {}', 'rs1', 'rs2', 'addr_rel bimm12hl'),
    'bge' : ([
        ('rs2(ins) == 0', 'bgez {}, {}', 'rs1', 'addr_rel bimm12hl')], 
        'bge {}, {}, {}', 'rs1', 'rs2', 'addr_rel bimm12hl'),
    'bgeu' : ([
        ('rs1(ins) == 0', 'beqz {}, {}', 'rs2', 'addr_rel bimm12hl')], 
        'bgeu {}, {}, {}', 'rs1', 'rs2', 'addr_rel bimm12hl'),
    'beq' : ([
        ('rs2(ins) == 0', 'beqz {}, {}', 'rs1', 'addr_rel bimm12hl')], 
        'beq {}, {}, {}', 'rs1', 'rs2', 'addr_rel bimm12hl'),
    'bne' : ([
        ('rs2(ins) == 0', 'bnez {}, {}', 'rs1', 'addr_rel bimm12hl')], 
        'bne {}, {}, {}', 'rs1', 'rs2', 'addr_rel bimm12hl'),
    'c_mv' : ([], 'mv {}, {}', 'rd', 'c_rs2_n0'),
    'c_add': ([], 'add {}, {}, {}', 'rd', 'rd', 'c_rs2_n0'),
    'c_beqz' : ([], 'beqz {}, {}', 'rs1_p', 'addr_rel c_bimm9hl'),
    'c_bnez' : ([], 'bnez {}, {}', 'rs1_p', 'addr_rel c_bimm9hl'),
    'flw': ([
        ('imm12(ins) == 0', 'flw {}, [{}]', 'frd', 'rs1')], 
        'flw {}, [{} + {}]', 'frd', 'rs1', 'imm12'),
    'fsqrt_s': ([], 'fsqrt.s {}, {}', 'frd', 'frs1'),
    'fadd_s': ([], 'fadd.s {}, {}, {}', 'frd', 'frs1', 'frs2'),
    'fmul_s': ([], 'fmul.s {}, {}, {}', 'frd', 'frs1', 'frs2'),
    'flt_s': ([], 'flt.s {}, {}, {}', 'rd', 'frs1', 'frs2'),
    'feq_s': ([], 'feq.s {}, {}, {}', 'rd', 'frs1', 'frs2'),
    'fle_s': ([], 'fle.s {}, {}, {}', 'rd', 'frs1', 'frs2'),
    'fsgnj_s': ([
        ('rs1(ins) == rs2(ins)', 'fmv.s {}, {}', 'frd', 'frs1')], 
        'fsgnj.s {}, {}, {}', 'frd', 'frs1', 'frs2'),
    'fsgnjn_s': ([
        ('rs1(ins) == rs2(ins)', 'fneg.s {}, {}', 'frd', 'frs1')], 
        'fsgnjn.s {}, {}, {}', 'frd', 'frs1', 'frs2'),
    'fsgnjx_s': ([
        ('rs1(ins) == rs2(ins)', 'fabs.s {}, {}', 'frd', 'frs1')], 
        'fsgnjx.s {}, {}, {}', 'frd', 'frs1', 'frs2'),
    'fcvt_w_s': ([], 'fcvt.w.s {}, {}, {}', 'rd', 'frs1', 'rm'),
    'fcvt_s_w': ([], 'fcvt.s.w {}, {}, {}', 'frd', 'rs1', 'rm'),
    'ecall': ([], 'ecall {}', 'a7')
}

def gen_print_macro(k):
    out_str = ''
    if k in print_macros.keys():
        for cond in print_macros[k][0]:
            format_vars = []
            format_specs = []
            for vf in cond[2:]:
                if vf == 'rm':
                    format_vars.append('rm_name[rm(ins)]')
                    format_specs.append('%s')
                elif vf.startswith('r') or vf.startswith('c_r'):
                    format_vars.append('reg_name[{}(ins)]'.format(vf))
                    format_specs.append('%s')
                elif vf.startswith('f'):
                    format_vars.append('freg_name[{}(ins)]'.format(vf[1:]))
                    format_specs.append('%s')
                elif vf.startswith('addr_rel '):
                    format_vars.append('pc + (sreg_t){}(ins), (int64_t)(sreg_t){}(ins)'.format(vf[9:], vf[9:]))
                    format_specs.append('0x%08llX (pc%+lld)')
                elif vf.startswith('shr '):
                    format_vars.append('{}(ins) >> 12'.format(vf[4:], vf[4:]))
                    format_specs.append('%lld')
                elif vf == 'a7':
                    format_vars.append('reg_name[REG_A(7)], (int64_t)(sreg_t)reg[REG_A(7)]')
                    format_specs.append('%s (%lld)')
                else:
                    format_vars.append('{}(ins)'.format(vf))
                    format_specs.append('%lld')
            fmt_str = cond[1].format(*format_specs)
            ins_str = 'pinstr("{}\\n"'.format(fmt_str)
            for i in format_vars:
                ins_str += ', ' + i
            out_str += 'if({}) {});\n        else '.format(cond[0], ins_str)
        format_vars = []
        format_specs = []
        for vf in print_macros[k][2:]:
            if vf == 'rm':
                format_vars.append('rm_name[rm(ins)]')
                format_specs.append('%s')
            elif vf.startswith('r') or vf.startswith('c_r'):
                format_vars.append('reg_name[{}(ins)]'.format(vf))
                format_specs.append('%s')
            elif vf.startswith('f'):
                format_vars.append('freg_name[{}(ins)]'.format(vf[1:]))
                format_specs.append('%s')
            elif vf.startswith('addr_rel '):
                format_vars.append('pc + (sreg_t){}(ins), (int64_t)(sreg_t){}(ins)'.format(vf[9:], vf[9:]))
                format_specs.append('0x%08llX (pc%+lld)')
            elif vf.startswith('shr '):
                format_vars.append('{}(ins) >> 12'.format(vf[4:], vf[4:]))
                format_specs.append('%lld')
            elif vf == 'a7':
                format_vars.append('reg_name[REG_A(7)], (int64_t)(sreg_t)reg[REG_A(7)]')
                format_specs.append('%s (%lld)')
            else:
                format_vars.append('{}(ins)'.format(vf))
                format_specs.append('%lld')
        fmt_str = print_macros[k][1].format(*format_specs)
        out_str += 'pinstr("{}\\n"'.format(fmt_str)
        for i in format_vars:
            out_str += ', ' + i
        return out_str + ')'
    else:
        return 'pinstr("{}\\n")'.format(k)

spc = '    '
hstr = '''// This file was generated using riscvhpp (https://github.com/MatthewObi/riscvhpp)
#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <memory.h>
#include <math.h>
#include "encoding.out.h"

#define REG_RA 1
#define REG_SP 2
#define REG_A(_n) (10 + _n)

namespace riscv {
struct DRAM
{
    enum err_t {
        ERR_OK,
        ERR_OOB,
        ERR_INVALID_SIZE,
    };

    struct DRAMAccRes {
        uint64_t value;
        err_t error;
    };

    static constexpr uint64_t SIZE = 16*1024*1024;
    uint8_t memory[SIZE];

    uint8_t load8(uint64_t address) { return memory[address]; }
    uint16_t load16(uint64_t address) { 
        return (uint16_t)memory[address] 
            | ((uint16_t)memory[address + 1] << 8); }
    uint32_t load32(uint64_t address) { 
        return (uint32_t)memory[address] 
            | ((uint32_t)memory[address + 1] << 8)
            | ((uint32_t)memory[address + 2] << 16)
            | ((uint32_t)memory[address + 3] << 24); }
    uint64_t load64(uint64_t address) { 
        return (uint64_t)memory[address] 
            | ((uint64_t)memory[address + 1] << 8)
            | ((uint64_t)memory[address + 2] << 16)
            | ((uint64_t)memory[address + 3] << 24)
            | ((uint64_t)memory[address + 4] << 32)
            | ((uint64_t)memory[address + 5] << 40)
            | ((uint64_t)memory[address + 6] << 48)
            | ((uint64_t)memory[address + 7] << 56); }
    DRAMAccRes load(uint64_t address, uint64_t size) { 
        if(address >= SIZE)
            return {address, ERR_OOB};
        if(address + size > SIZE)
            return {address + size, ERR_OOB};
        switch(size) { 
            case 8: return  {(uint64_t)load8(address), ERR_OK}; 
            case 16: return {(uint64_t)load16(address), ERR_OK}; 
            case 32: return {(uint64_t)load32(address), ERR_OK}; 
            case 64: return {(uint64_t)load64(address), ERR_OK}; 
            default: return {size, ERR_INVALID_SIZE};
        } 
    }

    void store8(uint64_t address, uint8_t value) { memory[address] = value; }
    void store16(uint64_t address, uint16_t value) {
        memory[address]   = (uint8_t)(value & 0xff);
        memory[address+1] = (uint8_t)((value >> 8) & 0xff); }
    void store32(uint64_t address, uint32_t value) {
        memory[address]   = (uint8_t)(value & 0xff);
        memory[address+1] = (uint8_t)((value >> 8) & 0xff); 
        memory[address+2] = (uint8_t)((value >> 16) & 0xff); 
        memory[address+3] = (uint8_t)((value >> 24) & 0xff); }
    void store64(uint64_t address, uint64_t value) {
        memory[address]   = (uint8_t)(value & 0xff);
        memory[address+1] = (uint8_t)((value >> 8) & 0xff); 
        memory[address+2] = (uint8_t)((value >> 16) & 0xff); 
        memory[address+3] = (uint8_t)((value >> 24) & 0xff); 
        memory[address+4] = (uint8_t)((value >> 32) & 0xff); 
        memory[address+5] = (uint8_t)((value >> 40) & 0xff); 
        memory[address+6] = (uint8_t)((value >> 48) & 0xff); 
        memory[address+7] = (uint8_t)((value >> 56) & 0xff); }
    DRAMAccRes store(uint64_t address, uint64_t size, uint64_t value) {
        if(address >= SIZE)
            return {address, ERR_OOB};
        if(address + size > SIZE)
            return {address + size, ERR_OOB};
        switch(size) {
            case 8:  store8 (address,  (uint8_t)value); return { (uint8_t)value, ERR_OK};
            case 16: store16(address, (uint16_t)value); return {(uint16_t)value, ERR_OK};
            case 32: store32(address, (uint32_t)value); return {(uint32_t)value, ERR_OK};
            case 64: store64(address,           value); return {          value, ERR_OK};
            default: return {size, ERR_INVALID_SIZE};
        }
    }
};

inline void print_error(const DRAM::DRAMAccRes& err) {
    switch(err.error) {
        case DRAM::ERR_INVALID_SIZE: 
            fprintf(stderr, "Attempted read of invalid size %llu.\\n", err.value);
            exit(-1);
        case DRAM::ERR_OOB: 
            fprintf(stderr, "Out of bounds read at address 0x%08llX.\\n", err.value);
            exit(-1);
        case DRAM::ERR_OK: exit(0);
    }
    exit(-1);
}

struct Bus
{
    DRAM dram;

    uint64_t load(uint64_t address, uint64_t size) { 
        if(address >= 0x80000000) {
            auto res = dram.load(address & 0x7fffffff, size);
            if(res.error == DRAM::ERR_OK)
                return res.value;
            print_error(res);
        }
        return ~0;
    }
    void store(uint64_t address, uint64_t size, uint64_t value) {
        if(address >= 0x80000000) {
            auto res = dram.store(address & 0x7fffffff, size, value);
            if(res.error == DRAM::ERR_OK)
                return;
            print_error(res);
        }
        print_error({address, DRAM::ERR_OOB});
    }
};

#define PRINT_INSTR 1

#if PRINT_INSTR
#define pinstr(fmt, ...) printf("%08llX: " fmt, pc, ##__VA_ARGS__)
#else 
#define pinstr(fmt, ...)
#endif
const char reg_name[][5] = {
    "Zero",
    "ra",
    "sp",
    "gp",
    "tp",
    "t0",
    "t1",
    "t2",
    "fp",
    "s1",
    "a0",
    "a1",
    "a2",
    "a3",
    "a4",
    "a5",
    "a6",
    "a7",
    "s2",
    "s3",
    "s4",
    "s5",
    "s6",
    "s7",
    "s8",
    "s9",
    "s10",
    "s11",
    "t3",
    "t4",
    "t5",
    "t6"
};

const char freg_name[][5] = {
    "ft0",
    "ft1",
    "ft2",
    "ft3",
    "ft4",
    "ft5",
    "ft6",
    "ft7",
    "fs0",
    "fs1",
    "fa0",
    "fa1",
    "fa2",
    "fa3",
    "fa4",
    "fa5",
    "fa6",
    "fa7",
    "fs2",
    "fs3",
    "fs4",
    "fs5",
    "fs6",
    "fs7",
    "fs8",
    "fs9",
    "fs10",
    "fs11",
    "ft8",
    "ft9",
    "ft10",
    "ft11"
};

const char rm_name[][4] = {
    "rne",
    "rtz",
    "rdn",
    "rup",
    "rmm",
    "rm5",
    "rm6",
    "dyn"
};

template<class To, class From>
constexpr To bitcast(From from) {
    static_assert(sizeof(From) == sizeof(To), "Bad bitcast!");
    To ret;
    memcpy(&ret, &from, sizeof(From));
    return ret;
}

const char strJumpedTo[] = "Jumped to %#08llx.\\n";
const char strBranchedTo[] = "Branched to %#08llx.\\n";

template<int a, int b>
constexpr int32_t extract_bits(uint32_t x) {
    static_assert(a >= b && a <= 31);
    int32_t y = (int32_t)x;
    y = (y >> b) & ((1 << (a-b + 1)) - 1);
    y = y << (31 - (a-b));
    y = y >> (31 - (a-b));
    return y;
}

template<int a, int b>
constexpr uint32_t extract_bits_u(uint32_t x) {
    static_assert(a >= b && a <= 31);
    x = x >> b;
    x = x & ((1 << (a-b + 1)) - 1);
    return x;
}

#define F32_SIGN ((uint32_t)1 << 31)
float sgnj32(float x, float y, bool neg, bool xr) {
    uint32_t a = bitcast<uint32_t>(x);
    uint32_t b = bitcast<uint32_t>(y);
    return bitcast<float>((a & ~F32_SIGN) | ((((xr) ? a : (neg) ? F32_SIGN : 0) ^ b) & F32_SIGN));
}
'''

class_str = '''
enum: uint64_t {
    ISA_BASE_32I = (1ull << 62ull),
    ISA_BASE_64I = (2ull << 62ull),
    ISA_BASE_128I = (3ull << 62ull)
};

#define ISA_EXT(_c) (1 << (_c - 'A'))

enum {
    ISA_EXT_ZIFENCEI = (1 << 26),
    ISA_EXT_ZICSR = (1 << 27),
    ISA_EXT_ZFH = (1 << 28),
    ISA_EXT_F = ISA_EXT('F') | ISA_EXT_ZICSR,
};

constexpr uint64_t RV_32GC = ISA_BASE_32I | ISA_EXT('F') | ISA_EXT('C');

template<int xlen>
struct RegType {
    typedef void ureg_t;
    typedef void sreg_t;
};
template<> struct RegType<32> { 
    typedef uint32_t ureg_t; 
    typedef int32_t sreg_t; 
};
template<> struct RegType<64> { 
    typedef uint64_t ureg_t; 
    typedef int64_t sreg_t; 
};

template<int flen>
struct FRegType {
    typedef void freg_t;
};
template<> struct FRegType<32> { 
    typedef float freg_t;
};
template<> struct FRegType<64> { 
    typedef double freg_t;
};

template<uint64_t _isa>
struct IsaData
{
    static constexpr int xlen() { switch(_isa >> 62) { 
        default: 
        case 1: 
            return 32; 
        case 2: 
            return 64; 
        case 3: 
            return 128; 
    } }
    static constexpr bool is_32bit() { return xlen() == 32; }
    static constexpr bool is_64bit() { return xlen() == 64; }
    static constexpr bool is_128bit() { return xlen() == 128; }
    static constexpr bool supports_ext(char ext) { return (_isa >> (ext - 'A')) & 1; }
    static constexpr bool supports_compressed() { return supports_ext('C'); }
    static constexpr bool supports_float() { return supports_ext('F') || supports_ext('D'); }
    static constexpr bool supports_zicsr() { return (_isa & ISA_EXT_ZICSR) || supports_float(); }
    static constexpr bool supports_zifencei() { return _isa & ISA_EXT_ZIFENCEI; }
    static constexpr bool supports_zfh() { return _isa & ISA_EXT_ZFH; }

    static constexpr int flen() { if(!supports_float()) return 0; else if(supports_ext('D')) return 64; else return 32; }
    
    typedef typename RegType<xlen()>::sreg_t sreg_t;
    typedef typename RegType<xlen()>::ureg_t ureg_t;
    typedef typename FRegType<flen()>::freg_t freg_t;
};


template<uint64_t _isa> constexpr bool isa_supports_float() { return IsaData<_isa>::supports_float(); }
template<uint64_t _isa> constexpr bool isa_supports_ext(char c) { return IsaData<_isa>::supports_ext(c); }
template<uint64_t _isa> constexpr bool isa_supports_compressed() { return IsaData<_isa>::supports_compressed(); }

template<uint64_t _isa>
struct CPU
{
    using ureg_t = typename IsaData<_isa>::ureg_t;
    using sreg_t = typename IsaData<_isa>::sreg_t;
    using freg_t = typename IsaData<_isa>::freg_t;

    static constexpr uint64_t isa = _isa;

    enum err_t {
        OK,
        ILLEGAL_INSTRUCTION,
        MISALIGNED_INSTRUCTION,
        ECALL,
        EBREAK,
        END_OF_PROG,
        MISC_ERR
    };

    ureg_t reg[32];
    uint64_t pc;

    freg_t freg[32];
    uint64_t csr[4096];

    Bus bus;

    uint32_t fetch() { auto data = (uint32_t)bus.load(pc, 32); /* printf("Fetched %u from address 0x%08llX.\\n", data, pc); */ return data; }

    uint64_t load(uint64_t address, uint64_t size) { 
        printf("Loading %lld-bit value from address 0x%08llx.\\n", size, address);
        return bus.load(address, size); 
    }
    void store(uint64_t address, uint64_t size, uint64_t value) { 
        printf("Storing %lld-bit value %lld to address 0x%08llx.\\n", size, value, address);
        return bus.store(address, size, value); 
    }

    CPU() {
        pc = 0x80000000;
        reg[REG_SP] = pc + 0x10000;
        reg[0] = 0;
    }

'''

exec_str = '''
    err_t execute()
    {
        if(pc == 0)
            return END_OF_PROG;
        reg[0] = 0;
        if constexpr(isa_supports_compressed<isa>())
        {
            uint32_t ins = fetch();
            if((ins & 3) == 3) {
                return execute32(ins);
            }
            else {
                return execute16((uint16_t)(ins & 0xffff));
            }
        }
        else 
        {
            if((pc & 3) != 0)
                return MISALIGNED_INSTRUCTION;
            return execute32(fetch());
        }
    }
'''

exec32_str = '''

    err_t execute32(uint32_t ins) {
'''

exec16_str = '''

    err_t execute16(uint16_t ins) {
'''

comb_args = []

def gen_decode_func(name):
    ins_range = arg_lut[name]
    if name not in bit_mapping:
        return 'extract_bits_u<{}, {}>(ins)'.format(ins_range[0], ins_range[1]) + (' + 8' if name.endswith('_p') else ''), False
    map_str = bit_mapping[name]
    signed = map_str[0] == 'i'
    groups = map_str[2:-1].split('|')
    decoded = []
    for group in groups:
        segment = group.split(':')
        if len(segment) == 1:
            decoded.append((int(segment[0]),int(segment[0])))
        else:
            decoded.append(tuple([int(i) for i in segment]))
    if signed:
        if 31 - ins_range[0] == 0:
            s = '(extract_bits<{}, {}>(ins){})'.format(ins_range[0], ins_range[0] - (decoded[0][0] - decoded[0][1]), '' if decoded[0][1] == 0 else ' << {}'.format(decoded[0][1]))
        else:
            s = '(extract_bits<{}, {}>(ins) << {})'.format(ins_range[0], ins_range[0] - (decoded[0][0] - decoded[0][1]), decoded[0][1])
        st = ins_range[0] - (decoded[0][0] - decoded[0][1]) - 1
        for dc in decoded[1:]:
            ed = st - (dc[0] - dc[1])
            shft = dc[1]
            shft_s = '' if shft == 0 else ' << {}'.format(shft)
            s += ' | (extract_bits_u<{}, {}>(ins){})'.format(st, ed, shft_s)
            st = ed - 1
    else:
        st = ins_range[0] - (decoded[0][0] - decoded[0][1]) - 1
        shft = decoded[0][1]
        shft_s = '' if shft == 0 else ' << {}'.format(shft)
        s = '(extract_bits_u<{}, {}>(ins){})'.format(ins_range[0], ins_range[0] - (decoded[0][0] - decoded[0][1]), shft_s)
        for dc in decoded[1:]:
            ed = st - (dc[0] - dc[1])
            shft = dc[1]
            shft_s = '' if shft == 0 else ' << {}'.format(shft)
            s += ' | (extract_bits_u<{}, {}>(ins){})'.format(st, ed, shft_s)
            st = ed - 1
    return s, signed

for k, v in arg_lut.items():
    expr, is_signed = gen_decode_func(k)
    hstr += 'constexpr {}int64_t {}({} ins) {{ return {}; }}\n'.format('' if is_signed else 'u', k, 'uint16_t' if k.startswith('c_') else 'uint32_t', expr)
    if k.endswith('hi'):
        comb_args.append((k[:-2], v))

for pair in comb_args:
    hstr += 'constexpr uint64_t {}hl({} x) {{ return ({}hi(x) << {}) | {}lo(x); }}\n'.format(pair[0], ('uint16_t' if pair[0].startswith('c_') else 'uint32_t'), pair[0], 0, pair[0])

hstr += class_str

for k, v in x.items():
    if k.startswith('c_'):
        hstr += spc + 'err_t ins_{}(uint16_t ins) {{\n'.format(k)
        ext_guard = ''
        ext_conds = []
        if len(v['extension']) == 1:
            if v['extension'][0].startswith('rv32'):
                ext_conds.append('IsaData<isa>::xlen() == 32')
            elif v['extension'][0].startswith('rv64'):
                ext_conds.append('IsaData<isa>::xlen() == 64')
            if '_' in v['extension'][0]:
                parts = v['extension'][0].split('_')[1:]
                if 'd' in parts:
                    ext_conds.append('IsaData<isa>::supports_ext(\'D\')')
                elif 'f' in parts:
                    ext_conds.append('IsaData<isa>::supports_float()')
                if 'zfh' in parts:
                    ext_conds.append('IsaData<isa>::supports_zfh()')
                if 'm' in parts:
                    ext_conds.append('IsaData<isa>::supports_ext(\'M\')')
                if 'a' in parts:
                    ext_conds.append('IsaData<isa>::supports_ext(\'A\')')
                if 'v' in parts:
                    ext_conds.append('IsaData<isa>::supports_ext(\'V\')')
                if 'zifencei' in parts:
                    ext_conds.append('IsaData<isa>::supports_zifencei()')
                if 'zicsr' in parts:
                    ext_conds.append('IsaData<isa>::supports_zicsr()')
            if len(ext_conds) > 0:
                ext_guard += 'if constexpr(' + ext_conds[0]
                for c in ext_conds[1:]:
                    ext_guard += ' && ' + c
                ext_guard += ') '
        exec16_str += (spc*2) + ext_guard + 'if((ins & MASK_{}) == MATCH_{}) return ins_{}(ins);\n'.format(k.upper(), k.upper(), k)
    else:
        hstr += spc + 'err_t ins_{}(uint32_t ins) {{\n'.format(k)
        ext_guard = ''
        ext_conds = []
        if len(v['extension']) == 1:
            if v['extension'][0].startswith('rv32'):
                ext_conds.append('IsaData<isa>::xlen() == 32')
            elif v['extension'][0].startswith('rv64'):
                ext_conds.append('IsaData<isa>::xlen() == 64')
            if '_' in v['extension'][0]:
                parts = v['extension'][0].split('_')[1:]
                if 'd' in parts:
                    ext_conds.append('IsaData<isa>::supports_ext(\'D\')')
                elif 'f' in parts:
                    ext_conds.append('IsaData<isa>::supports_float()')
                if 'zfh' in parts:
                    ext_conds.append('IsaData<isa>::supports_zfh()')
                if 'm' in parts:
                    ext_conds.append('IsaData<isa>::supports_ext(\'M\')')
                if 'a' in parts:
                    ext_conds.append('IsaData<isa>::supports_ext(\'A\')')
                if 'v' in parts:
                    ext_conds.append('IsaData<isa>::supports_ext(\'V\')')
                if 'zifencei' in parts:
                    ext_conds.append('IsaData<isa>::supports_zifencei()')
                if 'zicsr' in parts:
                    ext_conds.append('IsaData<isa>::supports_zicsr()')
            if len(ext_conds) > 0:
                ext_guard += 'if constexpr(' + ext_conds[0]
                for c in ext_conds[1:]:
                    ext_guard += ' && ' + c
                ext_guard += ') '
        exec32_str += (spc*2) + ext_guard + 'if((ins & MASK_{}) == MATCH_{}) return ins_{}(ins); // {}\n'.format(k.upper(), k.upper(), k, v['extension'][0])
    # for i in v['variable_fields']:
    #     cstr += (spc * 1) + '// {}\n'.format(i)
    hstr += (spc*2) + gen_print_macro(k) + ';\n'
    if k not in macros.keys():
        hstr += (spc*2) + 'return ILLEGAL_INSTRUCTION;\n'.format(k.upper())
    else:
        for ln in macros[k].splitlines():
            hstr += (spc*2) + '{}\n'.format(ln)
    hstr += '    }\n\n'

exec16_str += (spc*2) + 'return ILLEGAL_INSTRUCTION;\n}\n\n'
exec32_str += (spc*2) + 'return ILLEGAL_INSTRUCTION;\n}\n\n'

hstr += exec16_str + exec32_str + exec_str

hstr += '};\n} // namespace riscv\n'

with open('src/riscv.hpp', 'w') as f:
    f.write(hstr)