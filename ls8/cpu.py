"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # self.r1 = [0] * 8
        # self.r2 = [0] * 8
        # self.r3 = [0] * 8
        # self.r4 = [0] * 8
        # self.r5 = [0] * 8
        # self.r6 = [0] * 8
        # self.r7 = [0] * 8
        # self.r8 = [0] * 8

        self.reg = [0] * 8

        self.ram = [0] * 256

        self.pc = 0

        self.HLT = 0b00000001

    def ram_read(self, mar):
        # MAR is the memory address register
        return self.ram[mar]

    def ram_write(self, mdr, mar):
        # MDR is the memory data register
        self.ram[mar] = mdr



    def load(self):
        """Load a program into memory."""

        self.address_num = 0

        # For now, we've just hardcoded a program:

        if len(sys.argv) == 1:
            program = [
                # From print8.ls8
                0b10000010, # LDI R0,8
                0b00000000,
                0b00001000,
                0b01000111, # PRN R0
                0b00000000,
                0b00000001, # HLT
            ]

            for instruction in program:
                self.ram[self.address_num] = instruction
                self.address_num += 1

        else:
            new_program = sys.argv[1]
            with open(new_program) as f:
                for line in f:
                    try:
                        line = line.split('#',1)[0]
                        line = int(line, 2)
                        self.ram[self.address_num] = line
                        self.address_num += 1
                        #print(self.ram)
                        #self.branchcode[line] = 
                    except ValueError:
                        pass

                #sys.exit(0)


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]

            # NEED TO ADD IN OPERATIONS HERE

        elif op == "MULT":
            self.reg[reg_a] *= self.reg[reg_b]

        #elif op == "SUB": etc
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


    def run(self):
        """Run the CPU."""
        running = True
        # branchtable = {}

        # while running:
        #     IR = self.ram[self.pc]
        #     #IR = self.pc
        #     operand_a = self.ram_read(self.pc+1)
        #     operand_b = self.ram_read(self.pc+2)

        # class Branch:
        #     def __init__(self):
        #         self.branchtable = {}
        #         self.branchtable[OP1] = self.handle_op1
        #         self.branchtable[OP2] = self.handle_op2

        #     def handle_op1(self, x):
        #         print('op 1:', + x)

        #     def handle_op2(self, x):
        #         print('op 1:', + x)

        #self.reg[7] = 1
        self.counter = 0

        while running:
            #print(self.pc)
            #print(self.address_num)
            
            IR = self.ram[self.pc]
            #IR = self.pc
            #print(IR)
            operand_a = self.ram_read(self.pc+1)
            operand_b = self.ram_read(self.pc+2)

            if IR == 0b10000010:
                print('load')
                # loads 8 into the register
                self.reg[operand_a] = operand_b

                if self.counter < 0:
                    self.pc = self.address_num - 1
                    self.counter += 1
                else:
                    self.pc += 3

            elif IR == 0b01000111:
                # print 8(or whatevers in the next register)
                print(self.reg[operand_a])

                if self.counter < 0:
                    self.pc = self.address_num -1
                    self.counter += 1
                else:
                    self.pc += 2

            elif IR == self.HLT:
                # halt the cpu
                running = False

            elif IR == 0b10100010:
                print('mult')
                # the register key is 72 when the key should be 0 and value 72
                self.alu('MULT',operand_a,operand_b)
                
                if self.counter < 0:
                    self.pc = self.address_num - 1
                    self.counter += 1
                else:
                    self.pc += 3


            elif IR == 0b01000101:
                # PUSH FROM REGISTER TO MEMORY
                # decrement stack pointer(stack pointer is the 8th value in the stack)
                self.reg[7] -= 1

                # get register value
                #reg_num = operand_a #self.ram[pc + 1]
                value = self.reg[operand_a]   #operand_a instead of reg_num

                # store in memory at stack pointer
                address_to_push_to = self.reg[7]
                self.ram[address_to_push_to] = value

                if self.counter < 0:
                    self.pc = self.address_num - 1
                    self.counter += 1
                else:
                    self.pc += 2
    
            # ~~ THE STACK POINTER HOLDS THE ADDRESSES AND THE RAM HOLDS VALUES ~~
            elif IR == 0b01000110:
                # POP STACK VALUE
                # get value from ram
                address = self.reg[7]
                value = self.ram[address]

                # store in the given register
                self.reg[operand_a] = value

                # increment SP
                self.reg[7] += 1

                if self.reg[7] < 0:
                    self.pc = self.address_num - 1
                    self.counter += 1
                else:
                    self.pc += 2

            elif IR == 0b01010000:
                print('call')
                # CALL
                # get address of the next instruction
                return_addr = self.pc + 2

                # push it onto the stack
                self.reg[7] -= 1
                address_to_push_to = self.reg[7]
                self.ram[address_to_push_to] = return_addr

                # set the pc to the subroutine address
                subroutine_addr = self.reg[operand_a]

                self.pc = subroutine_addr

                self.counter -= 1

                # problem occurs when 

            elif IR == 0B00010001:
                print('return')
                # RETURN
                # get return address from the top of the stack
                address_to_pop_from = self.reg[7]
                return_addr = self.ram[address_to_pop_from]
                self.reg[7] += 1

                # set the pc to the return address
                self.pc = return_addr


            elif IR == 0b10100000:
                print('add')
                # ADD
                self.alu('ADD',operand_a,operand_b)
                if self.counter < 0:
                    self.pc = self.address_num - 1
                    self.counter += 1
                else:
                    self.pc += 3

    




