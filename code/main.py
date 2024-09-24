


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
    


class SingleStageRV:
    def __init__(self):
        self.registers = RISCV32_RegisterFile()

    def print_registers(self):
        self.registers.display()
        self.registers.write_register("x1", 0x1234)
        print(self.registers.read_register("x1"))
        self.registers.display()
        self.registers.reset_registers()
        self.registers.display()

if __name__ == '__main__':
    single_stage = SingleStageRV()
    single_stage.print_registers()  
    
