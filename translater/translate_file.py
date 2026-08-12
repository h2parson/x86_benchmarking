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
    main(sys.argv[1], sys.argv[2])
