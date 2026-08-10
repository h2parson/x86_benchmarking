import subprocess

NANOBENCH_DIR = "../nanoBench" 
ASM = "ADD RAX, RBX; ADD RBX, RAX"
CONFIG = "configs/cfg_Bonnell_common.txt"
OUT_FILE = "nanobench_output.txt"
# -----------------------------

def test_single(asm, out_file):
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

    print(f"Cycles = {cycles}")
    print(f"insts = {insts}")


def main():
    test_single(ASM, OUT_FILE)

    # with open(out_file, "w") as f:
    #         f.write(stdout)

if __name__ == "__main__":
    main()