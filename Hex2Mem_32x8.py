import re
import sys, getopt

infile  = None
outfile = None
drambase = 0x80000000
start_pc = 0x00000

argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(argv, "i:o:")  
except:
    print("Error")
for opt, arg in opts:
    if opt in ['-i']:
        infile = arg
    elif opt in ['-o']:
        outfile = arg
 
# print(infile + " " + outfile)

file_input = open(infile, mode='r')
file_output = open(outfile, mode='w')

lines_input = file_input.readlines()
merge_data = []
merge_buffer = []
lines_output = []
reversed_list = []
addr = 0x00

for i in range(len(lines_input)):
    line = lines_input[i].strip()
    
    if line.startswith('@'):
        m = re.match('^@([0-9A-Fa-f]{8})$', line)
        addr_8 = int(str(m.group(1)), 16)

        if addr_8 != addr:
            if (addr_8 // 32) == (addr // 32): #如果在同一个32byte align中
                while addr < addr_8:
                    merge_data.append('00')
                    addr += 0x10
            else:
                addr = addr_8;
                addr_32 = int((addr_8 - drambase) / 32)
                addr_32_hex = "{0:08X}".format(addr_32)
                if merge_data: #输出buffer中还未输出的结果
                    while len(merge_data) < 32:
                        merge_data.append('00')
                    merge_line = "".join(reversed(merge_data[:32]))
                    lines_output.append(merge_line + '\n')
                lines_output.append("@" + addr_32_hex + "\n")
                merge_data = []
         
    else:
        addr += len(line.split())
        merge_data.extend(line.split())

        if len(merge_data) >= 32:
            while len(merge_data) < 32:
                merge_data.append('00')
            merge_line = "".join(reversed(merge_data[:32]))
            lines_output.append(merge_line + '\n')            
            merge_data = merge_data[32:]




if merge_data:
    while len(merge_data) < 32:
                merge_data.append('00')
    merge_line = "".join(merge_data[::-1])
    lines_output.append(merge_line + '\n')
    
file_output.writelines(lines_output)