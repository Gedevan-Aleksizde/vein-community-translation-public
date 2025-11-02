#! /usr/bin/env python3

from pathlib import Path

import polib
import warnings
from modules.pofile import po2pddf
from modules.env import settings

dp_input = settings.inputdir.joinpath("fromcrowdin")
dp_output = settings.inputdir.joinpath("fromcrowdin-csv")


def convertpo2csv(fp: Path) -> bool:
    lang = fp.parent.name
    if lang != "en":
        print(f"reading {lang} files: {fp}")
        fp_output = dp_output.joinpath(f"{settings.version}/{lang}/vein0.csv")
        pof = polib.pofile(fp, encoding="utf-8")
        df = po2pddf(pof)
        if not fp_output.parent.exists():
            fp_output.parent.mkdir(parents=True)
        df.to_csv(fp_output, index=False)
        return True
    else:
        print("English files skipped")
        return True


def main():
    for fp_po in dp_input.rglob("*.po"):
        convertpo2csv(fp_po)


if __name__ == "__main__":
    main()
