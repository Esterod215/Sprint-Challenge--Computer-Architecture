"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram     = [0b00000000] * 256
        self.pc      = 0 #program count
        self.running = True
        self.reg     = [0] * 8 #8 registers
        self.sp      = 7

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1
        if len(sys.argv) != 2:
            print(f"must be in this format: {sys.argv[0]} filename")
            sys.exit(1)
        try:
            with open(f"examples/{sys.argv[1]}") as f:
                for line in f:
                    byte = line.split('#',1)[0].strip()
                    if byte == '':
                        continue
                   
                    self.ram[address] = int(byte,2)
                    # print(self.ram[address])
                    address+=1
            f.close()
                   
                                       
        
        except FileNotFoundError:
            print(f"{sys.argv[1]} not found")
            sys.exit(2)


    def ram_read(self,MAR):
        return self.reg[MAR]

    def ram_write(self,MAR, MDR):
        self.reg[MAR] = MDR

    def h(self):
        self.running = False

    def mult(self,v1,v2):
        self.reg[v1] = self.reg[v1] * self.reg[v2]

    def push(self):
        self.reg[self.sp] -= 1
        value = self.reg[operand_a]
        self.ram[self.reg[self.sp]] = value

        


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        

        if op == "ADD":
            print('inside ADD')
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        HLT               = 0b00000001
        PRN               = 0b01000111
        LDI               = 0b10000010
        MUL               = 0b10100010
        IR                = self.reg[0]
        PUSH              = 0b01000101
        POP               = 0b01000110
        CALL              = 0b01010000
        RETURN            = 0b00010001
        ADD               = 0b10100000
        self.reg[self.sp] = 0b11110100  #F4
               
        while self.running:
            IR = self.ram[self.pc]
            operand_a = self.ram[self.pc+1]
            operand_b = self.ram[self.pc+2]
            # print(IR)
            
            if IR == LDI:
                # print('entered LDI')
                self.ram_write(operand_a,operand_b)
                self.pc +=3
            
            elif IR == PRN:
                # print('print')
                print(self.ram_read(operand_a))
                self.pc+=2
            
            elif IR == HLT:
                # print('HLT')
                self.h()
            
            elif IR == MUL:
                
                self.alu('MUL',operand_a,operand_b)
                self.pc+=3
            
            elif IR == PUSH:
                self.push()
                self.pc +=2

            elif IR == POP:
                
                value = self.ram[self.reg[self.sp]]
                self.reg[operand_a] = value
                self.reg[self.sp] += 1
                self.pc += 2

            elif IR == CALL:
                print('inside call')
                ret_address = self.pc + 2
                self.reg[self.sp] -= 1
                self.ram[self.reg[self.sp]] = ret_address
                subroutine_address = self.reg[operand_a]
                self.pc = subroutine_address 

            elif IR == RETURN:
                return_address = self.ram[self.reg[self.sp]]
                self.reg[self.sp] += 1
                self.pc = return_address

            elif IR == ADD:
                
                self.alu('ADD',operand_a,operand_b)
                self.pc += 3




            else:
                print('command not supported')
                self.h()



            

