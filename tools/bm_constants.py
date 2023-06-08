# This project is licensed under the Apache License Version 2.0.
# ©Matthew Obi 2023
# dictionary containing the mapping of the argument to the what the fields in
# the bits should be
bit_mapping = {}
bit_mapping['imm12'] = 'i[11:0]'
bit_mapping['rs1'] = 'u[4:0]'
bit_mapping['rs2'] = 'u[4:0]'
bit_mapping['rd'] = 'u[4:0]'
bit_mapping['rt'] = 'u[4:0]'
bit_mapping['rs3'] = 'u[4:0]'
bit_mapping['aqrl'] = 'u[1:0]'
bit_mapping['aq'] = 'u[0]'
bit_mapping['rl'] = 'u[0]'
bit_mapping['imm20'] = 'i[31:12]'
bit_mapping['bimm12hi'] = 'i[12|10:5]'
bit_mapping['bimm12lo'] = 'u[4:1|11]'
bit_mapping['imm12hi'] = 'i[11:5]'
bit_mapping['imm12lo'] = 'i[4:0]'
bit_mapping['jimm20'] = 'i[20|10:1|11|19:12]'
bit_mapping['zimm'] = 'u[5:0]'
bit_mapping['shamtw'] = 'u[4:0]'
bit_mapping['shamtd'] = 'u[5:0]'
bit_mapping['shamtq'] = 'u[6:0]'
# bit_mapping['rd_p'] = "u[3:0]"
# bit_mapping['rs1_p'] = "u[3:0]"
# bit_mapping['rs2_p'] = "u[3:0]"
bit_mapping['rd_rs1_n0'] = 'u[4:0]'
# bit_mapping['rd_rs1_p'] = "u[3:0]"
# bit_mapping['c_rs2'] = 'rs2'
# bit_mapping['c_rs2_n0'] = 'rs2!=0'
# bit_mapping['rd_n0'] = 'rd!=0'
# bit_mapping['rs1_n0'] = 'rs1!=0'
# bit_mapping['c_rs1_n0'] = 'rs1!=0'
# bit_mapping['rd_rs1'] = 'rd/rs1'
bit_mapping['zimm6hi'] = 'u[5]'
bit_mapping['zimm6lo'] = 'u[4:0]'
bit_mapping['c_nzuimm10'] = "u[5:4|9:6|2|3]"
bit_mapping['c_uimm7lo'] = 'u[2|6]'
bit_mapping['c_uimm7hi'] = 'u[5:3]'
bit_mapping['c_uimm8lo'] = 'u[7:6]'
bit_mapping['c_uimm8hi'] = 'u[5:3]'
bit_mapping['c_uimm9lo'] = 'u[7:6]'
bit_mapping['c_uimm9hi'] = 'u[5:4|8]'
bit_mapping['c_nzimm6lo'] = 'u[4:0]'
bit_mapping['c_nzimm6hi'] = 'i[5]'
bit_mapping['c_imm6lo'] = 'u[4:0]'
bit_mapping['c_imm6hi'] = 'i[5]'
bit_mapping['c_nzimm10hi'] = 'i[9]'
bit_mapping['c_nzimm10lo'] = 'u[4|6|8:7|5]'
bit_mapping['c_nzimm18hi'] = 'i[17]'
bit_mapping['c_nzimm18lo'] = 'u[16:12]'
bit_mapping['c_imm12'] = 'i[11|4|9:8|10|6|7|3:1|5]'
bit_mapping['c_bimm9lo'] = 'u[7:6|2:1|5]'
bit_mapping['c_bimm9hi'] = 'i[8|4:3]'
bit_mapping['c_nzuimm5'] = 'u[4:0]'
bit_mapping['c_nzuimm6lo'] = 'u[4:0]'
bit_mapping['c_nzuimm6hi'] = 'u[5]'
bit_mapping['c_uimm8splo'] = 'u[4:2|7:6]'
bit_mapping['c_uimm8sphi'] = 'u[5]'
bit_mapping['c_uimm8sp_s'] = 'u[5:2|7:6]'
bit_mapping['c_uimm10splo'] = 'u[4|9:6]'
bit_mapping['c_uimm10sphi'] = 'u[5]'
bit_mapping['c_uimm9splo'] = 'u[4:3|8:6]'
bit_mapping['c_uimm9sphi'] = 'u[5]'
bit_mapping['c_uimm10sp_s'] = 'u[5:4|9:6]'
bit_mapping['c_uimm9sp_s'] = 'u[5:3|8:6]'