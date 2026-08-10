import subprocess

NANOBENCH_DIR = "../nanoBench" 
ASM = "ADD RAX, RBX; ADD RBX, RAX"
CONFIG = "configs/cfg_IceLake_common.txt"
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

    stdout, stderr = result.stdout, result.stderr

    if stderr is not None and stderr != "":
        print(f"Skipping line \"{asm}\", due to stderr output of \"{stderr}\"!")
        return None

    with open(out_file, "w") as f:
        f.write(stdout)

    print(f"\nOutput saved to {out_file}")


def main():
    test_single(ASM, OUT_FILE)

if __name__ == "__main__":
    main()