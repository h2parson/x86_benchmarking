import translater.translate_file as t
import sys
import subprocess
import os
from pathlib import Path

START_LINE = 355
END_LINE = 566

NANOBENCH_DIR = "../nanoBench" 
CONFIG = "configs/cfg_Bonnell_common.txt"

def process_file(path: Path) -> None:
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        print(f"Skipping {"temp0.s"} (not valid UTF-8 text)")
        return
    except OSError as e:
        print(f"Skipping {"temp0.s"} (could not read: {e})")
        return

    first = lines[0].strip()
    stalls = first.split(' ')[1]

    # Slice lines 355-566 (1-indexed, inclusive) -> 0-indexed [354:566]
    selected = lines[START_LINE - 1:END_LINE]

    if not selected:
        print(f"Skipping {"temp0.s"} (fewer than {START_LINE} lines, nothing in range)")
        return

    processed = []
    for line in selected:
        # Strip everything after and including the first "//"
        idx = line.find("//")
        if idx != -1:
            line = line[:idx]
        # Strip leading/trailing whitespace
        line = line.strip()
        processed.append(line)

    new_content = "\n".join(processed) + "\n"

    try:
        with open("temp0.s", "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Rewrote {"temp0.s"} ({len(processed)} lines)")
        return stalls
    except OSError as e:
        print(f"Failed to write {"temp0.s"}: {e}")

def main(path):
    # Get the desired lines
    process_file(path)

    # translate it into temp file 1
    t.main("temp0.s", 'temp1.s')

    # print out the results
    with open("temp1.s", "r", encoding="utf-8") as asm:
        asm_code = asm.read()
        unroll_txt = "-unroll_count=1"
        cmd = ["sudo", "./nanoBench.sh", "-asm", asm_code, "-config", CONFIG, unroll_txt]

        result = subprocess.run(
                    cmd,
                    cwd=NANOBENCH_DIR,
                    capture_output=True,
                    text=True,
                )
        
        out, err = result.stdout, result.stderr
        print(out+err)

    # clean up temp files
    os.remove("temp0.s")
    os.remove("temp1.s")

if __name__ == "__main__":
    # args are file name
    main(sys.argv[1])
    # main('keccakRound/keccakRound_MACROPARAMS-rdi_rsp_0x0_0__SPLITPARAMS-4_1_8_2.s')
