from enum import Enum 

class Opcode(Enum):
    LOAD = 0b0000011
    STORE = 0b0100011
    BRANCH = 0b1100011
    JALR = 0b1100111
    JAL = 0b1101111
    OP_IMM = 0b0010011
    OP = 0b0110011
    LUI = 0b0110111
    AUIPC = 0b0010111
    SYSTEM = 0b1110011

class Funct3(Enum):
    ADD_SUB = 0b000
    SLL = 0b001
    SLT = 0b010
    SLTU = 0b011
    XOR = 0b100
    SRL_SRA = 0b101
    OR = 0b110
    AND = 0b111

class Funct7(Enum):
    ADD = 0b0000000
    SUB = 0b0100000
    SRL = 0b0000000
    SRA = 0b0100000

class RISCV32_RegisterFile:
    """
    Support for named access with Register and ABI Name
    """
    def __init__(self):
        self.register_states = {
            "x0": 0x0,    # Hardwired zero
            "x1": 0x0,    # Return address
            "x2": 0x0,    # Stack pointer
            "x3": 0x0,    # Global pointer
            "x4": 0x0,    # Thread pointer
            "x5": 0x0,    # Temporary/Alternate link register
            "x6": 0x0,    # Temporary
            "x7": 0x0,    # Temporary
            "x8": 0x0,    # Saved register/frame pointer
            "x9": 0x0,    # Saved register
            "x10": 0x0,   # Function argument/return value
            "x11": 0x0,   # Function argument/return value
            "x12": 0x0,   # Function argument
            "x13": 0x0,   # Function argument
            "x14": 0x0,   # Function argument
            "x15": 0x0,   # Function argument
            "x16": 0x0,   # Function argument
            "x17": 0x0,   # Function argument
            "x18": 0x0,   # Saved register
            "x19": 0x0,   # Saved register
            "x20": 0x0,   # Saved register
            "x21": 0x0,   # Saved register
            "x22": 0x0,   # Saved register
            "x23": 0x0,   # Saved register
            "x24": 0x0,   # Saved register
            "x25": 0x0,   # Saved register
            "x26": 0x0,   # Saved register
            "x27": 0x0,   # Saved register
            "x28": 0x0,   # Temporary
            "x29": 0x0,   # Temporary
            "x30": 0x0,   # Temporary
            "x31": 0x0    # Temporary
        }

    def read_register(self, register_name):
        return self.register_states[register_name]
    
    def write_register(self, register_name, value):
        assert(register_name != "x0"), "Cannot write to x0"
        self.register_states[register_name] = value

    def reset_registers(self):
        for key, value in self.register_states.items():
            self.register_states[key] = 0x0

    def display(self):
        for key, value in self.register_states.items():
            print(f"{key}: {value}")
    

def IFetch(program_counter: int) -> int:
    """
    Program Counter: 32-bit integer
    Instructions are read from imem.txt in big endian format 
    where each line is a byte in binary format. For example, first word is at lines 0-3
    00000000: 00000000
    00000001: 00000000
    00000002: 00000000
    00000003: 00000000

    Given PC as base address, construct 32-bit instruction
    based on base + 3 next bytes on following lines
    """
    with open("imem.txt", "r") as file:
        lines = file.readlines()
        instruction = 0x0
        for i in range(4):
            # parse line as byte as binary format
            byte = int(lines[program_counter + i], 2)
            # reverse bits of byte
            # byte = int('{:08b}'.format(byte)[::-1], 2)
            instruction = instruction << 8
            instruction = instruction | byte
        
        # Reverse bits
        instruction = int('{:032b}'.format(instruction)[::-1], 2)
        print(bin(instruction))

        return instruction
    
def IDecode(instruction: int) -> str:
    """
    Decodes the given 32-bit instruction based on RV32I ISA.
    
    Args:
    instruction (int): The 32-bit instruction to decode.
    
    Returns:
    str: A human-readable form of the decoded instruction.
    """
    

    if Opcode(opcode) == Opcode.OP_IMM:
        if Funct3(funct3) == Funct3.ADD_SUB:
            return f"ADDI x{rd}, x{rs1}, {imm_i:#x}"
        elif Funct3(funct3) == Funct3.SLL:
            return f"SLLI x{rd}, x{rs1}, {imm_i & 0x1F}"
        # Add more cases for OP-IMM
    elif Opcode(opcode) == Opcode.OP:
        if Funct3(funct3) == Funct3.ADD_SUB:
            if Funct7(funct7) == Funct7.ADD:
                return f"ADD x{rd}, x{rs1}, x{rs2}"
            elif Funct7(funct7) == Funct7.SUB:
                return f"SUB x{rd}, x{rs1}, x{rs2}"
        elif Funct3(funct3) == Funct3.SRL_SRA:
            if Funct7(funct7) == Funct7.SRL:
                return f"SRL x{rd}, x{rs1}, x{rs2}"
            elif Funct7(funct7) == Funct7.SRA:
                return f"SRA x{rd}, x{rs1}, x{rs2}"
        # Add more cases for OP
    elif Opcode(opcode) == Opcode.LOAD:
        return f"LOAD x{rd}, {imm_i}(x{rs1})"
    elif Opcode(opcode) == Opcode.STORE:
        return f"STORE x{rs2}, {imm_s}(x{rs1})"
    elif Opcode(opcode) == Opcode.BRANCH:
        if Funct3(funct3) == Funct3.ADD_SUB:
            return f"BEQ x{rs1}, x{rs2}, {imm_b:#x}"
        # Add more cases for BRANCH
    elif Opcode(opcode) == Opcode.JAL:
        return f"JAL x{rd}, {imm_j:#x}"
    elif Opcode(opcode) == Opcode.JALR:
        return f"JALR x{rd}, {imm_i:#x}(x{rs1})"
    elif Opcode(opcode) == Opcode.LUI:
        return f"LUI x{rd}, {imm_u:#x}"
    elif Opcode(opcode) == Opcode.AUIPC:
        return f"AUIPC x{rd}, {imm_u:#x}"
    elif Opcode(opcode) == Opcode.SYSTEM:
        return f"SYSTEM call or ebreak"

    return "Unknown instruction"

    
    
    

class SingleStageRV:
    def __init__(self):
        self.registers = RISCV32_RegisterFile()
        self.program_counter = 0x0
        self.current_instruction = 0x0

    def print_registers(self) -> None:
        self.registers.display()
        self.registers.write_register("x1", 0x1234)
        print(self.registers.read_register("x1"))
        self.registers.display()
        self.registers.reset_registers()
        self.registers.display()

    def fetch(self) -> None:
        self.current_instruction = IFetch(0)

    def decode(self) -> None:
        IDecode(self.current_instruction)
       

if __name__ == '__main__':
    single_stage = SingleStageRV()
    single_stage.fetch()
    single_stage.decode()
    
