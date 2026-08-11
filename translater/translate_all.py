import translate as t
from pathlib import Path

def translate(file_path, out_file):
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
            if line.text is not None:
                file.write(line.text)

def main():
    for src, out in [('keccakRound','keccakRound_translated'),('keccakRound_originals','keccakRound_translated_originals')]:
        src_dir = Path(src)
        out_dir = Path(out)

        files = [p for p in src_dir.iterdir() if p.is_file()]
        if not files:
            print(f"No files found in {src_dir}")
            return

        for path in sorted(files):
            out_file = out_dir / path.name
            translate(path, out_file)

        

if __name__ == "__main__":
    main()
