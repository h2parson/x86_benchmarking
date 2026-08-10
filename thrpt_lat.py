import subprocess
import re

NANOBENCH_DIR = "../nanoBench" 
ASM = "ADD RAX, RBX; ADD RBX, RAX"
CONFIG = "configs/cfg_Bonnell_common.txt"
OUT_FILE = "nanobench_output.txt"
# -----------------------------

def test_single(asm):
    cmd = ["sudo", "./nanoBench.sh", "-asm", asm, "-config", CONFIG]

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
            cycles = line.split(" ")[1]
        elif line.startswith("INST_RETIRED:"):
            insts = line.split(" ")[1]

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


def latency_single(asm_temp, sz):
    args = n_regs(sz, len(re.findall(r"\{\d*\}", asm_temp)))
    inst1 = asm_temp.format(*args)
    inst2 = asm_temp.format(*args[::-1])
    asm = inst1 + "; " + inst2

    cycles, insts = test_single(asm)

    latency = cycles / insts

    print(f"latency = {latency}")

    return latency


def main():
    add_temp = r"ADD {0}, {1}"
    sz = "QW"

    latency_single(add_temp, sz)

    # with open(out_file, "w") as f:
    #         f.write(stdout)

if __name__ == "__main__":
    main()