import subprocess
from pathlib import Path
import csv
from datetime import datetime
import os

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

    out, _ = result.stdout, result.stderr

    # Now extract the data
    lines = out.splitlines()
    for line in lines:
        if line.startswith("CORE_CYCLES:"):
            cycles = float(line.split(" ")[1])
        elif line.startswith("INST_RETIRED:"):
            insts = float(line.split(" ")[1])
        elif line.startswith('L1D_CACHE.ALL_REF:'):
            cacherefs = float(line.split(" ")[1])

    return {'name':str(src), 'cycles':cycles, 'insts':insts, 'cacherefs':cacherefs}

def main():
    now = datetime.now()
    month = now.strftime("%b")
    day = str(now.day)
    date = month+day

    for unroll in [2]:
        out = f'Results/{date}/results_unroll_{str(unroll)}_{date}.csv'
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", newline='') as file:
            fieldnames = ['name', 'cycles', 'insts', 'cacherefs']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            data = []

            for src in [f'Code_Translated/{date}/keccakRound_translated']:
                src_dir = Path(src)

                files = [p for p in src_dir.iterdir() if p.is_file()]
                if not files:
                    print(f"No files found in {src_dir}")
                    return

                for path in sorted(files):
                    res = test(path, unroll=str(unroll))
                    print(f"results from {path}:")
                    print(res)
                    data.append(res)

                writer.writeheader()
                writer.writerows(data)

if __name__ == "__main__":
    main()
