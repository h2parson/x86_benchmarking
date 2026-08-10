import subprocess

NANOBENCH_DIR = "../nanoBench" 
CONFIG = "configs/cfg_Bonnell_common.txt"
# -----------------------------

def main():
    with open('./keccakRound/opt_formatted.s', "r", encoding="utf-8") as asm:
        asm_code = asm.read()
        cmd = ["sudo", "./nanoBench.sh", "-asm", asm_code, "-config", CONFIG]

        result = subprocess.run(
            cmd,
            cwd=NANOBENCH_DIR,
            capture_output=True,
            text=True,
        )

    output = result.stdout + result.stderr

    print(output)

if __name__ == "__main__":
    main()