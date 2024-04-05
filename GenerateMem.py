import re, os
import sys, getopt

bld_dir = "./build/test/"
test_info = bld_dir+"test_info"
filepath_current = "./build/test/test_info"
outdir = "./"

with open(test_info, 'r+', encoding='utf-8') as file_read:
  while True:
    lines = file_read.readline()
    if not lines:
      break;
    if re.match('^.*.hex', lines):
      regular = re.findall(r"(.+?).hex",lines)
      # print(regular[0])
      filein  = bld_dir + regular[0] + '.hex'
      fileout = bld_dir + regular[0] + '.mem'
      cmd     = 'python3 Hex2Mem.py -i ' + filein + ' -o ' + fileout
      cmd1    = 'python3 Hex2Mem_32x2.py -i ' + filein + ' -o ' + fileout + '_dual'
      cmd2    = 'python3 Hex2Mem_32x8.py -i ' + filein + ' -o ' + fileout + '_oct'
      os.system(cmd)
      os.system(cmd1)
      os.system(cmd2)

