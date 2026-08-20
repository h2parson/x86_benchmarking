import translater.translate_file as t
import sys
import subprocess
import os

NANOBENCH_DIR = "../nanoBench" 
CONFIG = "configs/cfg_Bonnell_common.txt"

def main(path, start, end):
    # Get the desired lines
    with open(path, "r") as file_in:
        lines = file_in.readlines() # Use human indices not zero indexed
        # Write them to temp file 0
        with open("temp0.s", "w") as file0:
            for line in lines:
                if line is not None:
                    file0.write(line)

    # translate it into temp file 1
    t.main("temp0.s", 'temp1.s')

    # print out the results
    with open("temp1.s", "r", encoding="utf-8") as asm:
        asm_code = asm.read()
        unroll_txt = "-unroll_count=2"
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
    # args are file name, start line, end line
    main(sys.argv[1], sys.argv[2], sys.argv[3])
    # main('keccakRound/keccakRound_MACROPARAMS-rdi_rsp_0x0_0__SPLITPARAMS-4_1_8_2.s', '355', '358')