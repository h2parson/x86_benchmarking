import subprocess
import sys
from pathlib import Path

NANOBENCH_DIR = "../nanoBench" 
CONFIG = "configs/cfg_Bonnell_common.txt"
# -----------------------------

def test(src, unroll=None):
    with open(src, "r", encoding="utf-8") as asm:
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

    return output

def main(unroll=None):
    with open('test_all_results.txt', "w", encoding="utf-8") as file:
        for src in ['keccakRound_translated','keccakRound_translated_originals']:
            src_dir = Path(src)

            files = [p for p in src_dir.iterdir() if p.is_file()]
            if not files:
                print(f"No files found in {src_dir}")
                return

            for path in sorted(files):
                res = test(path, unroll=unroll)
                file.write(f"Results from: {path}\n")
                file.write(res)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(unroll=sys.argv[1])
    else:
        main()
