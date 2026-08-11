import subprocess
import sys

NANOBENCH_DIR = "../nanoBench" 
CONFIG = "configs/cfg_Bonnell_common.txt"
# -----------------------------

def main(unroll=None):
    with open('./keccakRound/opt_formatted.s', "r", encoding="utf-8") as asm:
        asm_code = asm.read()
        unroll_txt = ("-unroll_count=" + unroll) if unroll else ""
        cmd = ["sudo", "./nanoBench.sh", "-asm", asm_code, "-config", CONFIG, unroll_txt]

        result = subprocess.run(
            cmd,
            cwd=NANOBENCH_DIR,
            capture_output=True,
            text=True,
        )

    output = result.stdout + result.stderr

    print(output)

if __name__ == "__main__":
    if len(sys.argv) >= 2:
    	main(unroll=sys.argv[1])
    else:
    	main()
