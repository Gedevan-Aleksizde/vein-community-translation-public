from pathlib import Path

import polib
import warnings
from modules.pofile import po2pddf

dp_input = Path("input")
dp_output = Path("intermed")


def convertpo2csv(fp: Path) -> bool:
    lang = fp.parent.name
    print(f"reading {lang} files: {fp}")
    fp_output = dp_output.joinpath(f"{lang}/vein0.csv")
    pof = polib.pofile(fp, encoding="utf-8")
    df = po2pddf(pof)
    if not fp_output.parent.exists():
        fp_output.parent.mkdir(parents=True)
    df.to_csv(fp_output, index=False)
    return True


def main():
    for fp_po in dp_input.rglob("*.po"):
        convertpo2csv(fp_po)


if __name__ == "__main__":
    main()
