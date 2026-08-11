import translate as t
import sys

def main(file_path, out_file):
    with open(file_path, "r") as file:
        text = [line.strip() for line in file]

        atat_code = t.Atat_Code(text=text)
        atat_code.parse_source()
        atat_code.to_intel()
        intel_code =  atat_code

        with open(out_file, "w", encoding="utf-8") as file:
            for line in intel_code.lines[:-1]:
                if line.text is not None:
                    file.write(line.text + "; ")
            line = intel_code.lines[-1]
            file.write(line.text)

if __name__ == "__main__":
    # main('./keccakRound/keccakRound_MACROPARAMS-rdi_rsp_0x0_1__SPLITPARAMS-3_1_6_2.s', \
    #       './translater/keccakRound_MACROPARAMS-rdi_rsp_0x0_1__SPLITPARAMS-3_1_6_2.s')

    main('./keccakRound/keccakRound_orig_rdi_rsp_0x0_1.s', './translater/orig_formatted.s')
