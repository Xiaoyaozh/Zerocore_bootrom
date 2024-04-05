#!/bin/sh
 
if [ $# != 1 ]
then
    echo "name: The name of .elf file"
else
    echo "The executable file name is:" $1.elf
    riscv64-unknown-elf-objdump -D -D -w -x -S $1.elf > $1.dump
    riscv64-unknown-elf-objcopy -O verilog $1.elf $1.hex
    python3 Hex2Mem_32x8.py -i $1.hex -o $1.mem_oct	
    python3 Hex2Coe_32x8.py -i $1.hex -o $1.coe	
fi