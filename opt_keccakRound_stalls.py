import subprocess
import sys

NANOBENCH_DIR = "../nanoBench" 
CONFIG = "configs/cfg_Bonnell_common.txt"
# -----------------------------

def main(unroll, loops):
    with open('./keccakRound/opt_formatted.s', "r", encoding="utf-8") as asm:
        asm_code = asm.read()
        unroll_txt = ("-unroll_count=" + unroll) if unroll else ""
        loops_txt = ("-loop_count=" + loops) if loops else ""
        cmd = ["sudo", "./nanoBench.sh", "-asm", asm_code, "-config", CONFIG, unroll_txt, loops_txt]

        result = subprocess.run(
            cmd,
            cwd=NANOBENCH_DIR,
            capture_output=True,
            text=True,
        )

    output = result.stdout + result.stderr

    print(output)

if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2])