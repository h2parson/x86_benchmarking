import translate as t
from pathlib import Path
from itertools import product

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
    dates = [path.name for path in Path('Code_ATAT').iterdir() if path.is_dir()]
    folder_endings = ['keccakRound', 'keccakRound_originals']
    srcs = [Path('Code_ATAT')/Path(date)/Path(folder_ending) for date, folder_ending in product(dates, folder_endings)]
    folder_endings = ['keccakRound_translated', 'keccakRound_translated_originals']
    outs = [Path('Code_Translated')/Path(date)/Path(folder_ending) for date, folder_ending in product(dates, folder_endings)]
    src_outs = zip(srcs, outs)
    
    for src, out in src_outs:
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