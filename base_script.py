import subprocess

NANOBENCH_DIR = "../nanoBench" 
ASM = "ADD RAX, RBX; ADD RBX, RAX"
CONFIG = "configs/cfg_IceLake_common.txt"
OUT_FILE = "nanobench_output.txt"
# -----------------------------

def main():
    cmd = ["sudo", "./nanoBench.sh", "-asm", ASM, "-config", CONFIG]

    result = subprocess.run(
        cmd,
        cwd=NANOBENCH_DIR,
        capture_output=True,
        text=True,
    )

    output = result.stdout + result.stderr

    print(output)

    with open(OUT_FILE, "w") as f:
        f.write(output)

    print(f"\nOutput saved to {OUT_FILE}")

if __name__ == "__main__":
    main()