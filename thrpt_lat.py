import subprocess
import re

NANOBENCH_DIR = "../nanoBench" 
ASM = "ADD RAX, RBX; ADD RBX, RAX"
CONFIG = "configs/cfg_Bonnell_common.txt"
OUT_FILE = "nanobench_output.txt"
# -----------------------------

def test_single(asm):
    asm_init = "MOV RAX, R14; MOV RBX, R14; MOV RCX, R14; MOV RDX, R14;"
    cmd = ["sudo", "./nanoBench.sh", "-asm_init", asm_init, "-asm", asm, "-config", CONFIG, "-unroll_count=500"]

    result = subprocess.run(
        cmd,
        cwd=NANOBENCH_DIR,
        capture_output=True,
        text=True,
    )

    lines, stderr = result.stdout.splitlines(), result.stderr

    if stderr is not None and stderr != "":
        print(f"Skipping line \"{asm}\", due to stderr output of \"{stderr}\"!")
        return None

    for line in lines:
        if line.startswith("CORE_CYCLES:"):
            cycles = float(line.split(" ")[1])
        elif line.startswith("INST_RETIRED:"):
            insts = float(line.split(" ")[1])

    return cycles, insts

byte_regs =    ["AL", "BL", "CL", "DL"]
word_regs =    ["AX", "BX", "CX", "DX"]
dblword_regs = ["EAX", "EBX", "ECX", "EDX"]
qdword_regs =  ["RAX", "RBX", "RCX", "RDX"]
xmm_regs =     [f"XMM{i}" for i in range(16)]
ymm_regs =     [f"YMM{i}" for i in range(16)]

def n_regs(sz, n):
    if sz == 'HW':
        return byte_regs[:n]
    elif sz == 'SW':
        return word_regs[:n]
    elif sz == 'DW':
        return dblword_regs[:n]
    elif sz == 'QW':
        return qdword_regs[:n]
    elif sz == 'X':
        return xmm_regs[:n]
    elif sz == 'Y':
        return ymm_regs[:n]
    return None

def thruput_single(asm_temp, sz):
    n = len(re.findall(r"\{\d*\}", asm_temp))
    args = n_regs(sz, 2*n)
    inst1 = asm_temp.format(*(args[:n]))
    inst2 = asm_temp.format(*(args[n:]))
    asm = inst1 + "; " + inst2

    cycles, insts = test_single(asm)

    thruput = cycles / insts

    print(f"inverse throughput = {thruput}")


def latency_single(asm_temp, sz):
    n = len(re.findall(r"\{\d*\}", asm_temp))
    args = n_regs(sz, n)
    inst1 = asm_temp.format(*args)
    if "ptr" not in asm_temp:
        inst2 = asm_temp.format(*args[::-1])
    else:
        print("latency not tested!")
        return 
    asm = inst1 + "; " + inst2

    cycles, insts = test_single(asm)

    latency = cycles / insts

    print(f"latency = {latency}")

one_arg_temp                        = r"{mn} {0}"
two_arg_temp                        = r"{mn} {0}, {1}"
two_arg_with_imm_temp               = r"{mn} {0}, 1"
two_arg_from_ptr_temp               = r"{mn} {0}, {ptr_sz} ptr[{1}]"
two_arg_to_ptr_temp                 = r"{mn} {ptr_sz} ptr[{0}], {1}"
two_arg_imm_to_ptr_temp             = r"{mn} {ptr_sz} ptr[{0}], 1"
two_arg_from_ptr_with_offset_temp   = r"{mn} {0}, {ptr_sz} ptr[{1}+8]"
two_arg_to_ptr_with_offset_temp     = r"{mn} {ptr_sz} ptr[{0}+8], {1}"
two_arg_imm_to_ptr_with_offset_temp = r"{mn} {ptr_sz} ptr[{0}+8], 1"

inst_dict = {
    "add"                        : two_arg_temp.replace("{mn}","ADD"),
    "add_with_imm"               : two_arg_with_imm_temp.replace("{mn}","ADD"),
    "mov"                        : two_arg_temp.replace("{mn}","MOV"),
    "mov_with_imm"               : two_arg_with_imm_temp.replace("{mn}","MOV"),
    "mov_from_ptr"               : two_arg_from_ptr_temp.replace("{mn}", "MOV"),
    "mov_to_ptr"                 : two_arg_to_ptr_temp.replace("{mn}", "MOV"),
    "mov_imm_to_ptr"             : two_arg_imm_to_ptr_temp.replace("{mn}", "MOV"),
    "mov_from_ptr_with_offset"   : two_arg_from_ptr_with_offset_temp.replace("{mn}", "MOV"),
    "mov_to_ptr_with_offset"     : two_arg_to_ptr_with_offset_temp.replace("{mn}", "MOV"),
    "mov_imm_to_ptr_with_offset" : two_arg_imm_to_ptr_with_offset_temp.replace("{mn}", "MOV"),
    "not"                        : one_arg_temp.replace("{mn}","NOT"),
    "or"                         : two_arg_temp.replace("{mn}","OR"),
    "pop"                        : one_arg_temp.replace("{mn}","POP"),
    "push"                       : one_arg_temp.replace("{mn}","PUSH"),
    "rol_with_imm"               : two_arg_with_imm_temp.replace("{mn}","ROL"),
    "rol_with_implicit_shift"    : one_arg_temp.replace("{mn}","ROL"),
    "shr_with_imm"               : two_arg_with_imm_temp.replace("{mn}","SHR"),
    "sub_with_imm"               : two_arg_with_imm_temp.replace("{mn}","SUB"),
    "xchg"                       : two_arg_temp.replace("{mn}","XCHG"),
    "xor_with_imm"               : two_arg_with_imm_temp.replace("{mn}","XOR"),
    "xor"                        : two_arg_temp.replace("{mn}","XOR"),
    "xor_from_ptr_with_offset"   : two_arg_from_ptr_with_offset_temp.replace("{mn}", "XOR"),
    "xor_to_ptr_with_offset"     : two_arg_to_ptr_with_offset_temp.replace("{mn}", "XOR"),
    "xor_imm_to_ptr_with_offset" : two_arg_imm_to_ptr_with_offset_temp.replace("{mn}", "XOR"),
}

def replace_ptr_sz(inst, sz):
    res = inst
    # I'm only using QW for now so just keep it simple
    if "{ptr_sz}" in inst:
        res = inst.replace("{ptr_sz}","qword")
    return res

def thruputs():
    for name, inst in inst_dict.items():
        print(f"Inverse throughput for instruction {name}:")
        inst = replace_ptr_sz(inst, "QW")
        thruput_single(inst, "QW")

    return

def latencies():
    for name, inst in inst_dict.items():
        print(f"Latency for instruction {name}:")
        inst = replace_ptr_sz(inst, "QW")
        latency_single(inst, "QW")

    return

def main():

    thruputs()
    latencies()

if __name__ == "__main__":
    main()